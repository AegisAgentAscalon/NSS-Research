"""Fixed local replay executor and durable result receipts, not generic tools.

The coordinator invokes this owner only after consuming/checking a host grant.
It can rebuild the existing synthetic neural transition and inspect old mock action
receipts; it cannot execute new external actions or publish a production checkpoint.
"""
from contextlib import contextmanager
from copy import deepcopy
import os
from pathlib import Path
import sqlite3

from .neural_contracts import encoded, fields, fingerprint, pairs
from .permission_contracts import completion, request, ZERO
from .permission_journal import document, fault
from .qualification_contracts import digest_value
from .qualification_sources import require_source
from .runtime import fail

FORMAT = 'MegaMindAlpha.BoundedPermissionReplay.v1'


def state_digest(state):
    return fingerprint({k: (v.tolist() if k == 'cache' else v) for k, v in state.items()})


def action_receipts(ledger, task_id):
    # Explicit owner interface. No private SQL, no implicit action execution.
    return [{'key': k, 'receipt': ledger.inspect(k)['receipt']} for k in ledger.action_keys(task_id)]


def source_state(req, source, ledger):
    from .neural_backend import deterministic_cpu
    from .neural_execution import NeuralSession
    req = request(req); source = require_source(source); b = req['binding']
    view = source.view(b['run_id'], b['trial_seed'], b['precision'])
    if view[4] != b:
        fail('INCOMPATIBLE_CONFIGURATION', 'Execution source differs from authorized binding')
    if action_receipts(ledger, req['task_id']) != req['action_receipts']:
        fail('RECOVERY_REQUIRED', 'Mock action history differs from the bound request')
    with deterministic_cpu(b['trial_seed']):
        session = NeuralSession(view[1]['artifacts'], b['runtime_sha256'])
        state = session.state(req['claim']['source'], req['inputs'], req['task_id'])
        if state_digest(state) != req['source_state_sha256']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Prepared source neural state differs')
    return session, state


class ReplayExecutor:
    def __init__(self, directory):
        if not isinstance(directory, (str, os.PathLike)):
            fail('VALIDATION_FAILED', 'Local executor directory required')
        self.path = Path(directory).resolve() / 'permission_replay.sqlite3'
        self.audit()

    @classmethod
    def create(cls, directory):
        root = Path(directory)
        if root.exists() and (not root.is_dir() or any(root.iterdir())):
            fail('CONSTRAINT_CONFLICT', 'Replay executor requires an empty directory')
        db = None
        try:
            root.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(root/'permission_replay.sqlite3')
            db.execute('PRAGMA synchronous=FULL')
            db.execute('CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), format TEXT NOT NULL, count INTEGER NOT NULL, head TEXT NOT NULL)')
            db.execute('CREATE TABLE results(seq INTEGER PRIMARY KEY, request_id TEXT UNIQUE NOT NULL, body TEXT NOT NULL, previous TEXT NOT NULL, sha256 TEXT NOT NULL)')
            db.execute('INSERT INTO meta VALUES(1,?,0,?)', (FORMAT, ZERO)); db.commit()
        except (OSError, sqlite3.Error):
            fail('RECOVERY_REQUIRED', 'Executor store creation failed; inspect partial directory')
        finally:
            if db: db.close()
        return cls(root)

    @contextmanager
    def _db(self):
        if not self.path.is_file():
            fail('RECOVERY_REQUIRED', 'Executor journal missing; no recreation')
        db = None
        try:
            db = sqlite3.connect(self.path.as_uri()+'?mode=rw', uri=True, timeout=5)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA synchronous=FULL'); db.execute('BEGIN IMMEDIATE')
            yield db; db.commit()
        except sqlite3.Error:
            if db: db.rollback()
            fail('RECOVERY_REQUIRED', 'Executor journal corrupt/unavailable')
        except BaseException:
            if db: db.rollback()
            raise
        finally:
            if db: db.close()

    def _read(self, db):
        meta = db.execute('SELECT * FROM meta').fetchall()
        if len(meta) != 1 or meta[0]['id'] != 1 or meta[0]['format'] != FORMAT:
            fail('VALIDATION_FAILED', 'Invalid executor metadata')
        meta = meta[0]; n = meta['count']
        if type(n) is not int or not 0 <= n <= 1000:
            fail('BUDGET_EXHAUSTED', 'Executor journal capacity exceeded')
        rows = db.execute('SELECT * FROM results ORDER BY seq LIMIT 1001').fetchall()
        if len(rows) != n:
            fail('VALIDATION_FAILED', 'Executor receipt history incomplete')
        head = ZERO; out = {}
        for seq, row in enumerate(rows, 1):
            body = document(row['body']); fields(body, ('request', 'grant_sha256', 'result', 'receipt'))
            req = request(body['request']); h = digest_value(body['grant_sha256'])
            result = body['result']; encoded(result)
            fields(result, ('task_id', 'source_ecid', 'destination_ecid', 'input_sha256',
                            'values', 'draft', 'action_receipts', 'status', 'publication_scope'))
            c = req['claim']; b = req['binding']
            if (result['task_id'] != req['task_id'] or result['source_ecid'] != b['profile_ecids'][c['source']]
                    or result['destination_ecid'] != b['profile_ecids'][c['destination']]
                    or result['input_sha256'] != fingerprint(req['inputs']) or result['draft'] != ''
                    or result['action_receipts'] != req['action_receipts'] or result['status'] != 'SUCCESS'
                    or result['publication_scope'] != 'LOCAL_EXPERIMENT_RESULT_ONLY'):
                fail('VALIDATION_FAILED', 'Rebuilt result binding mismatch')
            values = result['values']
            if (type(values) is not list or len(values) != 4
                    or any(type(p) is not list or len(p) != 2 for p in values)
                    or any(type(v) is not list or len(v) != 16 for p in values for v in p)
                    or any(type(x) is not float for p in values for v in p for x in v)):
                fail('VALIDATION_FAILED', 'Invalid bounded neural result tensor')
            receipt = completion(body['receipt'], req, h)
            if receipt['result_sha256'] != fingerprint(result):
                fail('VALIDATION_FAILED', 'Runtime receipt does not match result')
            event = {'seq': seq, 'body': body, 'previous': head}
            if (row['seq'] != seq or row['request_id'] != req['request_id'] or row['previous'] != head
                    or row['sha256'] != fingerprint(event) or req['request_id'] in out):
                fail('VALIDATION_FAILED', 'Executor receipt chain differs')
            head = row['sha256']; out[req['request_id']] = body
        if head != meta['head']:
            fail('VALIDATION_FAILED', 'Executor receipt head differs')
        return out, {'count': n, 'head': head}

    def lookup(self, document_value, grant_sha256):
        req = request(document_value); digest_value(grant_sha256)
        with self._db() as db:
            records, _ = self._read(db); old = records.get(req['request_id'])
            if old is None: return None
            if old['request'] != req or old['grant_sha256'] != grant_sha256:
                fail('CONSTRAINT_CONFLICT', 'Executor request identity reused with other parameters/grant')
            return deepcopy(old['receipt'])

    def perform(self, document_value, grant_sha256, *, source, ledger, fault_at=None):
        """Internal adapter operation, callable Python is NOT a security sandbox."""
        from .neural_backend import deterministic_cpu
        req = request(document_value); digest_value(grant_sha256)
        if fault_at not in (None, 'before_executor_commit', 'after_executor_commit'):
            fail('VALIDATION_FAILED', 'Unknown executor fault point')
        old = self.lookup(req, grant_sha256)
        if old is not None: return old  # Inspect history; no re-execution.
        session, state = source_state(req, source, ledger)
        b = req['binding']
        with deterministic_cpu(b['trial_seed']):
            recovered = session.recover(state, req['claim']['destination'], req['task_id'], ledger, authorized=True)
        if recovered['status'] != 'SUCCESS':
            fail(recovered['status'], 'Authorized local probe replay failed')
        target = recovered['state']
        result = {'task_id': req['task_id'], 'source_ecid': state['ecid'], 'destination_ecid': target['ecid'],
                  'input_sha256': target['input_sha256'], 'values': target['cache'].tolist(), 'draft': target['draft'],
                  'action_receipts': action_receipts(ledger, req['task_id']), 'status': 'SUCCESS',
                  'publication_scope': 'LOCAL_EXPERIMENT_RESULT_ONLY'}
        receipt = {'schema_version': 1, 'request_id': req['request_id'], 'request_sha256': fingerprint(req),
                   'grant_sha256': grant_sha256, 'executor_id': 'bounded_neural_replay_v1',
                   'result_sha256': fingerprint(result), 'status': 'COMMITTED', 'deployment_authorized': False}
        body = {'request': req, 'grant_sha256': grant_sha256, 'result': result, 'receipt': receipt}
        with self._db() as db:
            records, meta = self._read(db)
            if req['request_id'] in records:
                if records[req['request_id']] != body:
                    fail('CONSTRAINT_CONFLICT', 'Conflicting concurrent replay publication')
                return deepcopy(records[req['request_id']]['receipt'])
            if meta['count'] >= 1000: fail('BUDGET_EXHAUSTED', 'Executor result journal full')
            event = {'seq': meta['count']+1, 'body': body, 'previous': meta['head']}
            h = fingerprint(event)
            db.execute('INSERT INTO results VALUES(?,?,?,?,?)', (event['seq'], req['request_id'], encoded(body).decode(), meta['head'], h))
            db.execute('UPDATE meta SET count=?,head=? WHERE id=1', (event['seq'], h))
            self._read(db); fault(fault_at, 'before_executor_commit')
        fault(fault_at, 'after_executor_commit')
        return receipt

    def audit(self):
        with self._db() as db:
            _, meta = self._read(db)
            return {'status': 'SUCCESS', 'committed_results': meta['count'], 'head': meta['head'],
                    'production_checkpoint_modified': False}


def require_executor(value):
    if type(value) is not ReplayExecutor:
        fail('VALIDATION_FAILED', 'Only the fixed local replay executor is supported')
    return value
