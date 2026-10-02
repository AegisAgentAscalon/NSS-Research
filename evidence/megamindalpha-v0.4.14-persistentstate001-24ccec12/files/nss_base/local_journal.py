"""Shared bounded journal mechanics; each owner selects its own file and reducer.

No hidden materialized revocation index. A reducer checks every event on read and
before publication. The reducer is installed code, never a JSON supplied callback.
Hash chaining detects partial/accidental edits, not a coherent privileged rewrite.
"""
from contextlib import contextmanager
from pathlib import Path
import os
import sqlite3
from .neural_contracts import encoded, fingerprint
from .runtime import fail
from .serialization import decode


def fault(selected, point):
    if selected == point:
        os._exit(83)


def document(raw):
    if type(raw) is not str or len(raw) > 2 * 1024 * 1024:
        fail('VALIDATION_FAILED', 'Invalid bounded journal document')
    try:
        value = decode(raw); encoded(value); return value
    except (RecursionError, UnicodeError):
        fail('VALIDATION_FAILED', 'Invalid journal JSON')


ZERO = '0' * 64


def epoch(value):
    if type(value) is not int or not 0 <= value <= 253402300799:
        fail('VALIDATION_FAILED', 'Expected bounded whole UTC epoch seconds')
    return value


class EventJournal:
    """Reusable local storage mechanics; subclasses own schema, policy and reducer.

    Reducers and validators are installed Python, never names supplied by JSON.
    Instances retain separate files and histories. This is not a shared authority.
    """
    filename = None
    validate_manifest = None
    max_events = 2000
    max_history_bytes = 16 * 1024 * 1024

    def __init__(self, directory):
        if not isinstance(directory, (str, os.PathLike)):
            fail('VALIDATION_FAILED', 'Local journal directory required')
        self.path = Path(directory).resolve() / self.filename

    @classmethod
    def create_document(cls, directory, value):
        m = cls.validate_manifest(value)
        root = Path(directory)
        if root.exists() and (not root.is_dir() or any(root.iterdir())):
            fail('CONSTRAINT_CONFLICT', 'New store requires an empty directory')
        db = None
        try:
            root.mkdir(parents=True, exist_ok=True)
            with sqlite3.connect(root / cls.filename) as db:
                db.execute('PRAGMA synchronous=FULL')
                db.execute('CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), manifest TEXT NOT NULL, manifest_hash TEXT NOT NULL, count INTEGER NOT NULL, head TEXT NOT NULL)')
                db.execute('CREATE TABLE events(seq INTEGER PRIMARY KEY, kind TEXT NOT NULL, at INTEGER NOT NULL, body TEXT NOT NULL, previous TEXT NOT NULL, sha256 TEXT NOT NULL)')
                db.execute('INSERT INTO meta VALUES(1,?,?,0,?)', (encoded(m).decode(), fingerprint(m), ZERO))
        except (OSError, sqlite3.Error):
            fail('RECOVERY_REQUIRED', 'Store creation failed; inspect partial directory')
        finally:
            if db is not None: db.close()
        return cls(root)

    @contextmanager
    def transaction(self):
        if not self.path.is_file():
            fail('RECOVERY_REQUIRED', 'Local journal missing; no automatic recreation')
        db = None
        try:
            db = sqlite3.connect(self.path.as_uri() + '?mode=rw', uri=True, timeout=5)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA synchronous=FULL'); db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except sqlite3.Error:
            if db: db.rollback()
            fail('RECOVERY_REQUIRED', 'Local journal unavailable/corrupt')
        except BaseException:
            if db: db.rollback()
            raise
        finally:
            if db: db.close()

    def read(self, db, reducer):
        meta = db.execute('SELECT * FROM meta').fetchall()
        if len(meta) != 1 or meta[0]['id'] != 1:
            fail('VALIDATION_FAILED', 'Invalid local journal metadata')
        meta = meta[0]; m = self.validate_manifest(document(meta['manifest']))
        if fingerprint(m) != meta['manifest_hash']:
            fail('VALIDATION_FAILED', 'Local manifest mismatch')
        count = meta['count']
        if type(count) is not int or not 0 <= count <= self.max_events:
            fail('BUDGET_EXHAUSTED', 'Local history capacity exceeded')
        rows = db.execute('SELECT * FROM events ORDER BY seq LIMIT ?', (self.max_events+1,)).fetchall()
        if len(rows) != count:
            fail('VALIDATION_FAILED', 'Local history is incomplete')
        events = []; head = ZERO; used = 0; last = 0
        for seq, row in enumerate(rows, 1):
            body = document(row['body']); at = epoch(row['at'])
            used += len(row['body'].encode())
            if used > self.max_history_bytes:
                fail('BUDGET_EXHAUSTED', 'Local history byte bound exceeded')
            event = {'seq': seq, 'kind': row['kind'], 'at': at, 'body': body, 'previous': head}
            if (row['seq'] != seq or row['previous'] != head or row['sha256'] != fingerprint(event) or at < last):
                fail('VALIDATION_FAILED', 'Local chain/order mismatch')
            head = row['sha256']; last = at; events.append(event)
        if head != meta['head']:
            fail('VALIDATION_FAILED', 'Local head mismatch')
        state = reducer(m, events)
        return m, state, {'count': count, 'head': head, 'bytes': used, 'last_at': last}, events

    def append(self, db, reducer, meta, kind, at, body):
        epoch(at)
        if at < meta['last_at']:
            fail('AUTHORIZATION_DENIED', 'Observed clock moved backwards')
        if meta['count'] >= self.max_events or meta['bytes'] + len(encoded(body)) > self.max_history_bytes:
            fail('BUDGET_EXHAUSTED', 'Local journal full')
        event = {'seq': meta['count']+1, 'kind': kind, 'at': at, 'body': body, 'previous': meta['head']}
        h = fingerprint(event)
        db.execute('INSERT INTO events VALUES(?,?,?,?,?,?)', (event['seq'], kind, at, encoded(body).decode(), meta['head'], h))
        db.execute('UPDATE meta SET count=?,head=? WHERE id=1', (event['seq'], h))
        self.read(db, reducer)
