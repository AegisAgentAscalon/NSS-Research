"""DatasetSnapshot001: immutable manifest/receipt store and revocation-aware reads.

There is no training executor, authorization lease or cross-database transaction.
An archive batch read is the eligibility observation; a later consumer must
recheck. Admin inspection can expose retained bytes without granting their use.
Local trusted-operator prototype, not hostile-disk tamper/rollback protection.
"""
from contextlib import contextmanager
from copy import deepcopy
from datetime import datetime, timezone
from functools import wraps
from hashlib import sha256
import json
import os
from pathlib import Path
import sqlite3

from .dataset_contracts import (FORMAT, MAX_MANIFEST_BYTES, MAX_TOKENIZER_BYTES,
    SPLITS, make_manifest, normalize_request, receipt, references, validate_manifest)
from .experience_contracts import hash_id, identifier
from .experience_store import ExperienceArchive
from .runtime import ContractError, fail
from .serialization import decode


def _json(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False)


def _success(data, *, replayed=False, historical=False):
    return {'status': 'SUCCESS', 'data': deepcopy(data), 'detail': '',
            'replayed': replayed, 'historical': historical}


def _public(method):
    @wraps(method)
    def call(*args, **kwargs):
        try:
            return method(*args, **kwargs)
        except ContractError as exc:
            return {'status': exc.code, 'data': None, 'detail': str(exc),
                    'replayed': False, 'historical': False}
        except (OSError, sqlite3.Error, UnicodeError, RecursionError) as exc:
            return {'status': 'INTERNAL_FAILURE', 'data': None,
                'detail': 'Snapshot storage operation failed; no grant implied. ' + type(exc).__name__,
                'replayed': False, 'historical': False}
    return call


def _path(value):
    if not isinstance(value, (str, os.PathLike)):
        fail('VALIDATION_FAILED', 'Expected a local filesystem path')
    try:
        p = Path(value).resolve()
        if '\x00' in str(p): fail('VALIDATION_FAILED', 'NUL in local path')
        return p
    except (ValueError, TypeError, OSError):
        fail('VALIDATION_FAILED', 'Invalid local path')


def _unwrap(result):
    if result['status'] != 'SUCCESS': fail(result['status'], result['detail'])
    return result['data']


def _binding(archive):
    if not isinstance(archive, ExperienceArchive):
        fail('VALIDATION_FAILED', 'Expected the public local ExperienceArchive adapter')
    return _unwrap(archive.binding())['sha256']


def _tokenizer(path, expected):
    p = _path(path)
    if not p.is_file(): fail('INSUFFICIENT_EVIDENCE', 'Pinned tokenizer artifact is missing')
    with p.open('rb') as f: raw = f.read(MAX_TOKENIZER_BYTES + 1)
    if len(raw) > MAX_TOKENIZER_BYTES:
        fail('BUDGET_EXHAUSTED', 'Tokenizer identity artifact exceeds local byte budget')
    if sha256(raw).hexdigest() != expected:
        fail('VALIDATION_FAILED', 'Tokenizer bytes differ from the pinned digest')
    # Identity check only. Never import/execute a tokenizer or any stored content.


def _decode_body(value):
    if type(value) is not str or len(value.encode('utf-8')) > MAX_MANIFEST_BYTES:
        fail('VALIDATION_FAILED', 'Malformed or oversized stored JSON body')
    return decode(value)


def _fault(point, selected):
    if point == selected: os._exit(76)


class DatasetSnapshots:
    """One owner of local immutable dataset manifests, never of archive/runtime heads."""
    def __init__(self, directory):
        self.path = _path(directory) / 'snapshots.sqlite3'
        try:
            with self._db(): pass
        except (OSError, sqlite3.Error):
            fail('RECOVERY_REQUIRED', 'Snapshot store cannot be opened; no implicit repair')

    @classmethod
    def create(cls, directory, *, archive):
        binding = _binding(archive); directory = _path(directory)
        try:
            if directory.exists() and (not directory.is_dir() or any(directory.iterdir())):
                fail('CONSTRAINT_CONFLICT', 'Snapshot initialization needs an empty/new directory')
            directory.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(directory / 'snapshots.sqlite3', timeout=5)
            try:
                db.execute('PRAGMA synchronous=FULL'); db.execute('BEGIN IMMEDIATE')
                db.execute('CREATE TABLE metadata(key TEXT PRIMARY KEY,value TEXT NOT NULL)')
                db.execute('CREATE TABLE snapshots(id TEXT PRIMARY KEY,sha256 TEXT NOT NULL UNIQUE,body TEXT NOT NULL)')
                db.execute('CREATE TABLE operations(id TEXT PRIMARY KEY,request_sha256 TEXT NOT NULL,body TEXT NOT NULL,result_id TEXT NOT NULL UNIQUE,result_sha256 TEXT NOT NULL)')
                db.executemany('INSERT INTO metadata VALUES (?,?)',
                    [('format', FORMAT), ('schema_version', '1'), ('archive_binding', binding)])
                db.commit()
            except BaseException:
                db.rollback(); raise
            finally:
                db.close()
            return cls(directory)
        except (OSError, sqlite3.Error):
            fail('INTERNAL_FAILURE', 'Could not initialize snapshot store; no destructive auto-cleanup')

    @contextmanager
    def _db(self):
        if not self.path.is_file():
            fail('RECOVERY_REQUIRED', 'Snapshot database missing; open does not recreate it')
        db = sqlite3.connect(self.path.as_uri() + '?mode=rw', uri=True, timeout=5)
        db.row_factory = sqlite3.Row
        try:
            db.execute('PRAGMA synchronous=FULL'); db.execute('BEGIN IMMEDIATE')
            try: metadata = dict(db.execute('SELECT key,value FROM metadata'))
            except sqlite3.Error: fail('RECOVERY_REQUIRED', 'File is not an initialized snapshot store')
            if (set(metadata) != {'format', 'schema_version', 'archive_binding'}
                    or metadata['format'] != FORMAT or metadata['schema_version'] != '1'):
                fail('INCOMPATIBLE_CONFIGURATION', 'Unknown snapshot format/schema; explicit migration required')
            hash_id(metadata['archive_binding'])
            yield db, metadata['archive_binding']
            db.commit()
        except BaseException:
            db.rollback(); raise
        finally:
            db.close()

    def _stored(self, db, binding, id):
        identifier(id)
        row = db.execute('SELECT * FROM snapshots WHERE id=?', (id,)).fetchone()
        if row is None: fail('INSUFFICIENT_EVIDENCE', 'Unknown dataset snapshot')
        m = validate_manifest(_decode_body(row['body'])); r = receipt(m)
        if r['snapshot_id'] != id or r['sha256'] != row['sha256'] or m['archive_binding'] != binding:
            fail('VALIDATION_FAILED', 'Snapshot identity, digest or archive binding is inconsistent')
        op = db.execute('SELECT * FROM operations WHERE id=?', (m['request']['operation_id'],)).fetchone()
        if (op is None or op['result_id'] != id or op['result_sha256'] != r['sha256']
                or op['request_sha256'] != m['request_sha256']
                or _decode_body(op['body']) != m['request']):
            fail('VALIDATION_FAILED', 'Manifest lacks its exact published operation receipt')
        return m

    @_public
    def build(self, request, *, archive, tokenizer_path, fault_at=None):
        """Publish exact point-in-time membership, not a continuing use permission."""
        if fault_at not in (None, 'after_manifest', 'after_operation', 'before_commit', 'after_commit'):
            fail('VALIDATION_FAILED', 'Unknown explicit test fault point')
        request = normalize_request(request)
        actual_binding = _binding(archive)
        _tokenizer(tokenizer_path, request['tokenizer']['sha256'])
        with self._db() as (db, binding):
            if actual_binding != binding:
                fail('INCOMPATIBLE_CONFIGURATION', 'Another archive cannot be substituted')
            prior = db.execute('SELECT * FROM operations WHERE id=?', (request['operation_id'],)).fetchone()
            if prior is not None:
                original = self._stored(db, binding, prior['result_id'])
                if original['request'] != request:
                    fail('CONSTRAINT_CONFLICT', 'Operation ID already binds a different request')
                return _success(receipt(original), replayed=True, historical=True)
            if db.execute('SELECT 1 FROM snapshots WHERE id=?', (request['snapshot_id'],)).fetchone():
                fail('CONSTRAINT_CONFLICT', 'Snapshot membership cannot be overwritten; use a new ID')
            batch = _unwrap(archive.read_batch_for_use(references(request), purpose='training'))
            if batch['archive_binding']['sha256'] != binding:
                fail('INCOMPATIBLE_CONFIGURATION', 'Archive binding changed during build')
            m = make_manifest(request, batch); r = receipt(m)
            body = _json(m)
            if len(body.encode('utf-8')) > MAX_MANIFEST_BYTES:
                fail('BUDGET_EXHAUSTED', 'Materialized manifest exceeds local byte budget')
            db.execute('INSERT INTO snapshots VALUES (?,?,?)', (r['snapshot_id'], r['sha256'], body))
            _fault('after_manifest', fault_at)
            db.execute('INSERT INTO operations VALUES (?,?,?,?,?)', (request['operation_id'],
                m['request_sha256'], _json(request), r['snapshot_id'], r['sha256']))
            _fault('after_operation', fault_at); _fault('before_commit', fault_at)
        _fault('after_commit', fault_at)
        return _success(r)

    @_public
    def inspect(self, snapshot_id):
        """Administrative retained material, NOT an authorized training read."""
        with self._db() as (db, binding):
            m = self._stored(db, binding, snapshot_id)
            return _success({'reference': receipt(m), 'manifest': m, 'use_authorized': False}, historical=True)

    @_public
    def operation_receipt(self, operation_id):
        identifier(operation_id)
        with self._db() as (db, binding):
            row = db.execute('SELECT result_id FROM operations WHERE id=?', (operation_id,)).fetchone()
            if row is None: return _success(None, historical=True)
            m = self._stored(db, binding, row['result_id'])
            if m['request']['operation_id'] != operation_id:
                fail('VALIDATION_FAILED', 'Operation points to another publication')
            return _success(receipt(m), historical=True)

    @_public
    def list_snapshots(self, *, limit=100, after=None):
        if type(limit) is not int or not 1 <= limit <= 1000:
            fail('VALIDATION_FAILED', 'List limit must be 1..1000')
        if after is not None: identifier(after)
        with self._db() as (db, binding):
            ids = [r[0] for r in db.execute('SELECT id FROM snapshots WHERE id>? ORDER BY id LIMIT ?', (after or '', limit))]
            return _success([receipt(self._stored(db, binding, id)) for id in ids], historical=True)

    @_public
    def read_for_use(self, snapshot_id, *, expected_manifest_hash, purpose, split, archive, tokenizer_path):
        """Gate the whole snapshot on EVERY read, then return one split.

        A prior read, build receipt or audit is never reused as a permission grant.
        All members must still be exact-current, including the unrequested split.
        Returned bytes cannot be recalled after later revocation; no running trainer
        or protected holdout interface is implemented here.
        """
        hash_id(expected_manifest_hash)
        if type(purpose) is not str or purpose != 'training':
            fail('VALIDATION_FAILED', 'This consumer supports the training purpose only')
        if type(split) is not str or split not in SPLITS:
            fail('VALIDATION_FAILED', 'Unknown dataset split')
        # Release the read-only snapshot transaction before querying the archive.
        with self._db() as (db, binding):
            m = self._stored(db, binding, snapshot_id)
        if receipt(m)['sha256'] != expected_manifest_hash:
            fail('CONSTRAINT_CONFLICT', 'Expected manifest identity does not match')
        if _binding(archive) != binding:
            fail('INCOMPATIBLE_CONFIGURATION', 'Dataset is bound to another local archive')
        _tokenizer(tokenizer_path, m['request']['tokenizer']['sha256'])
        batch = _unwrap(archive.read_batch_for_use(references(m['request']), purpose='training'))
        if make_manifest(m['request'], batch) != m:
            fail('VALIDATION_FAILED', 'Current permitted archive views differ from the fixed dataset')
        selected = [x for x in m['members'] if x['split'] == split]
        if not selected: fail('INSUFFICIENT_EVIDENCE', 'The requested split has no members')
        examples = [{'reference': x['view']['reference'], 'split': split,
            'family_id': x['view']['family_id'], 'text': x['text'], 'text_sha256': x['text_sha256'],
            'uncertainty': x['view']['statement']['uncertainty'],
            'source_hashes': sorted({s['sha256'] for s in x['view']['sources']}),
            'origin': 'reviewed-statement-not-verified-truth'} for x in selected]
        return _success({'snapshot': receipt(m), 'purpose': 'training', 'split': split,
            'checked_at': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
            'examples': examples, 'scope': 'Point-in-time local gate; recheck at each later consumption boundary. '
                'No durable grant, authenticated rights, protected holdout or export recall.'})

    @_public
    def audit(self):
        """Static integrity only. Does not certify current archive eligibility."""
        with self._db() as (db, binding):
            if [r[0] for r in db.execute('PRAGMA integrity_check')] != ['ok']:
                fail('VALIDATION_FAILED', 'Snapshot SQLite integrity check failed')
            ids = [r[0] for r in db.execute('SELECT id FROM snapshots')]
            for id in ids: self._stored(db, binding, id)
            operations = list(db.execute('SELECT * FROM operations'))
            if len(operations) != len(ids): fail('VALIDATION_FAILED', 'Orphan/duplicate operation receipt')
            for op in operations:
                m = self._stored(db, binding, op['result_id'])
                if m['request']['operation_id'] != op['id']:
                    fail('VALIDATION_FAILED', 'Operation linked to the wrong manifest')
            return _success({'snapshots': len(ids), 'operations': len(operations),
                'scope': 'Stored structural/hash checks only, not permission, semantic truth or authenticated lineage.'})
