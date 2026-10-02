"""Trusted-local, append-only qualification decisions with current-use checks.

SQLite owns only this subsystem's events. No production pointer or authorization
permit is written. Hash chaining detects incomplete/accidental edits, not an actor
who controls and consistently rewrites the entire store and its metadata.
"""
from contextlib import contextmanager
from copy import deepcopy
import os
from pathlib import Path
import sqlite3

from .neural_contracts import encoded, fields, fingerprint
from .qualification_contracts import (AUTHORITY, FORMAT, POLICY, POLICY_HASH, authorize,
    binding, claim, decision, digest_value, identifier, manifest, request,
    required_profiles, revocation, verification, checker_name, review_actor)
from .qualification_sources import require_source
from .runtime import fail
from .serialization import decode

ZERO = '0' * 64
MAX_EVENTS = 2000
MAX_HISTORY_BYTES = 32 * 1024 * 1024


def _decode_stored(value):
    if type(value) is not str:
        fail('VALIDATION_FAILED', 'Stored event must be UTF-8 JSON text')
    try:
        if len(value.encode('utf-8')) > 2 * 1024 * 1024:
            fail('BUDGET_EXHAUSTED', 'Stored event exceeds its byte bound')
        result = decode(value)
        encoded(result)
        return result
    except (RecursionError, UnicodeError):
        fail('VALIDATION_FAILED', 'Malformed or over-nested stored JSON')


def _fault(point, chosen):
    if point == chosen:
        os._exit(79)


def _local(states, revoked, identity, active=None):
    """Resolve exact accepted prerequisites; never infer subset/transition claims."""
    active = set() if active is None else active
    if identity in active:
        fail('VALIDATION_FAILED', 'Cyclic qualification prerequisites')
    if identity not in states:
        fail('INSUFFICIENT_EVIDENCE', 'Missing prerequisite decision')
    state = states[identity]
    if state['status'] != 'QUALIFIED' or state['certificate'] is None:
        fail('INSUFFICIENT_EVIDENCE', 'An unqualified decision cannot support use')
    if identity in revoked:
        fail('AUTHORIZATION_DENIED', 'Qualification evidence has been revoked')
    active.add(identity)
    req = state['request']; profiles = []
    for dep in req['prerequisites']:
        parent = _local(states, revoked, dep, active)
        if parent['request']['binding'] != req['binding'] or parent['request']['claim']['kind'] != 'PROFILE':
            fail('INCOMPATIBLE_CONFIGURATION', 'Prerequisite targets a different exact candidate')
        profiles.append(parent['request']['claim']['profile'])
    active.remove(identity)
    if sorted(profiles) != required_profiles(req['claim'], source_format=req['binding'].get('source_format')):
        fail('INCOMPATIBLE_CONFIGURATION', 'Core-only/endpoint prerequisite scopes do not match')
    return state


def _prerequisites(req, states, revoked):
    profiles = []
    for identity in req['prerequisites']:
        p = _local(states, revoked, identity)
        if p['request']['binding'] != req['binding'] or p['request']['claim']['kind'] != 'PROFILE':
            fail('INCOMPATIBLE_CONFIGURATION', 'Prerequisite binding mismatch')
        profiles.append(p['request']['claim']['profile'])
    if sorted(profiles) != required_profiles(req['claim'], source_format=req['binding'].get('source_format')):
        fail('INCOMPATIBLE_CONFIGURATION', 'Exact Core/endpoint claims required')


def _source_current(req, source, states, revoked):
    """Check current evidence and its separately bound parent certificate in this owner.

    This avoids cross-owner private reads and recursive SQLite connections. The
    closed source adapter supplies a parent reference, never its own approval.
    """
    view = source.guard(req)
    if 'source_format' in req['binding']:
        dep = source.upstream(req)
        parent = _local(states, revoked, dep['request_id'])
        if (fingerprint(parent['certificate']) != dep['certificate_sha256'] or
                parent['request']['binding'] != dep['binding'] or parent['request']['claim'] != dep['claim']):
            fail('INCOMPATIBLE_CONFIGURATION', 'Candidate parent approval was substituted')
        pv = dep['source'].guard(parent['request'])
        if parent['verification']['checker_identity'] != pv[5]:
            fail('INCOMPATIBLE_CONFIGURATION','Parent verifier environment changed')
    return view


def _publication(req, d, v, states):
    verdict = ('QUALIFIED' if v['verdict'] == 'PASS' else
               'REJECTED' if v['verdict'] == 'FAIL' else 'INCONCLUSIVE') if d['recommendation'] == 'ACCEPT' else (
               'REJECTED' if d['recommendation'] == 'REJECT' else 'INCONCLUSIVE')
    certificate = None
    if verdict == 'QUALIFIED':
        certificate = {'schema_version': 1, 'evidence_id': req['request_id'],
            'request_sha256': fingerprint(req), 'claim': deepcopy(req['claim']),
            'binding': deepcopy(req['binding']), 'policy_sha256': POLICY_HASH,
            'verification_sha256': fingerprint(v), 'producer_id': req['producer_id'],
            'reviewer_id': d['reviewer_id'], 'issued_at': d['at'],
            'prerequisites': [{'id': k, 'sha256': fingerprint(states[k]['certificate'])} for k in req['prerequisites']],
            'scope': POLICY['scope'], 'authority': AUTHORITY, 'deployment_authorized': False}
    receipt = {'schema_version': 1, 'operation_id': d['operation_id'], 'request_id': req['request_id'],
        'request_sha256': fingerprint(req), 'decision_sha256': fingerprint(d),
        'verification_sha256': fingerprint(v), 'verdict': verdict,
        'certificate_sha256': fingerprint(certificate) if certificate else None,
        'authority': AUTHORITY, 'deployment_authorized': False}
    return {'decision': d, 'verification': v, 'certificate': certificate, 'receipt': receipt}


def _unrun(req):
    return {'schema_version': 1, 'request_sha256': fingerprint(req), 'binding_sha256': fingerprint(req['binding']),
        'claim': deepcopy(req['claim']), 'policy_sha256': POLICY_HASH, 'verdict': 'NOT_RUN',
        'checks': [], 'repeats': [], 'checker_identity': {'name': checker_name(req['binding']),
            'code_sha256': req['binding']['code_sha256'], 'numerical_backend_sha256': ZERO},
        'limits': ['Human rejection/inconclusive attestation; numerical checks were not executed.'],
        'deployment_authorized': False}


class Qualifications:
    """Single trusted-local authority owner; roles are operator assertions, not auth."""
    def __init__(self, directory):
        if not isinstance(directory, (str, os.PathLike)):
            fail('VALIDATION_FAILED', 'Expected a local qualification directory')
        self.path = Path(directory).resolve() / 'qualification.sqlite3'
        with self._db() as db:
            self._read(db)

    @classmethod
    def create(cls, directory, operators):
        m = manifest({'schema_version': 1, 'format': FORMAT, 'operators': deepcopy(operators), 'policy_sha256': POLICY_HASH})
        root = Path(directory)
        if root.exists() and (not root.is_dir() or any(root.iterdir())):
            fail('CONSTRAINT_CONFLICT', 'New qualification store needs an empty directory')
        try:
            root.mkdir(parents=True, exist_ok=True)
            db = sqlite3.connect(root/'qualification.sqlite3')
            try:
                db.execute('PRAGMA synchronous=FULL')
                db.execute('CREATE TABLE meta(id INTEGER PRIMARY KEY CHECK(id=1), manifest TEXT NOT NULL, manifest_hash TEXT NOT NULL, count INTEGER NOT NULL, head TEXT NOT NULL)')
                db.execute('CREATE TABLE events(seq INTEGER PRIMARY KEY, kind TEXT NOT NULL, body TEXT NOT NULL, previous TEXT NOT NULL, sha256 TEXT NOT NULL)')
                db.execute('INSERT INTO meta VALUES(1,?,?,0,?)', (encoded(m).decode(), fingerprint(m), ZERO))
                db.commit()
            finally:
                db.close()
        except (OSError, sqlite3.Error):
            fail('RECOVERY_REQUIRED', 'Qualification store creation failed; inspect partial directory')
        return cls(root)

    @contextmanager
    def _db(self):
        if not self.path.is_file():
            fail('RECOVERY_REQUIRED', 'Qualification store missing; no implicit recreation')
        db = None
        try:
            db = sqlite3.connect(self.path.as_uri()+'?mode=rw', uri=True, timeout=5)
            db.row_factory = sqlite3.Row
            db.execute('PRAGMA synchronous=FULL'); db.execute('BEGIN IMMEDIATE')
            yield db
            db.commit()
        except sqlite3.Error:
            if db is not None:
                db.rollback()
            fail('RECOVERY_REQUIRED', 'Unavailable or corrupt qualification store')
        except BaseException:
            if db is not None:
                db.rollback()
            raise
        finally:
            if db is not None:
                db.close()

    def _read(self, db):
        meta = db.execute('SELECT * FROM meta').fetchall()
        if len(meta) != 1 or meta[0]['id'] != 1:
            fail('VALIDATION_FAILED', 'Missing or duplicate journal metadata')
        meta = meta[0]; m = manifest(_decode_stored(meta['manifest']))
        if fingerprint(m) != meta['manifest_hash']:
            fail('VALIDATION_FAILED', 'Role/policy manifest hash differs')
        if type(meta['count']) is not int or not 0 <= meta['count'] <= MAX_EVENTS:
            fail('BUDGET_EXHAUSTED', 'Bounded qualification journal capacity exceeded')
        rows = db.execute('SELECT * FROM events ORDER BY seq LIMIT ?', (MAX_EVENTS+1,)).fetchall()
        if len(rows) != meta['count']:
            fail('VALIDATION_FAILED', 'Journal count differs: incomplete or deleted event')
        states = {}; revoked = {}; operations = {}; head = ZERO; used = 0
        for index, row in enumerate(rows, 1):
            body = _decode_stored(row['body'])
            used += len(row['body'].encode())
            if used > MAX_HISTORY_BYTES:
                fail('BUDGET_EXHAUSTED', 'Bounded journal history exceeded')
            event = {'seq': index, 'kind': row['kind'], 'previous': head, 'body': body}
            if row['seq'] != index or row['previous'] != head or row['sha256'] != fingerprint(event):
                fail('VALIDATION_FAILED', 'Journal chain mismatch')
            head = row['sha256']
            if row['kind'] == 'PREPARE':
                req = request(body); key = req['request_id']
                if key in states:
                    fail('VALIDATION_FAILED', 'Repeated request preparation')
                authorize(m, req['producer_id'], 'PRODUCER')
                _prerequisites(req, states, revoked)
                states[key] = {'request': req, 'status': 'PREPARED', 'decision': None,
                    'verification': None, 'certificate': None, 'receipt': None}
            elif row['kind'] == 'DECIDE':
                fields(body, ('decision', 'verification', 'certificate', 'receipt'))
                d = decision(body['decision']); key = d['request_id']
                if key not in states or states[key]['status'] != 'PREPARED' or d['operation_id'] in operations:
                    fail('VALIDATION_FAILED', 'Decision without a unique prepared request')
                req = states[key]['request']; v = verification(body['verification'])
                authorize(m, d['reviewer_id'], 'REVIEWER', req['producer_id']); review_actor(req, d['reviewer_id'])
                if (d['request_sha256'] != fingerprint(req) or d['at'] < req['at']
                        or v['request_sha256'] != fingerprint(req) or v['binding_sha256'] != fingerprint(req['binding'])
                        or v['claim'] != req['claim'] or v['checker_identity']['name'] != checker_name(req['binding'])
                        or v['checker_identity']['code_sha256'] != req['binding']['code_sha256']):
                    fail('VALIDATION_FAILED', 'Decision/evidence binding differs')
                if (d['recommendation'] == 'ACCEPT') == (v['verdict'] == 'NOT_RUN'):
                    fail('VALIDATION_FAILED', 'Review/check execution mismatch')
                if d['recommendation'] == 'ACCEPT' and v['verdict'] == 'PASS':
                    _prerequisites(req, states, revoked)
                if body != _publication(req, d, v, states):
                    fail('VALIDATION_FAILED', 'Certificate or receipt does not match the review')
                states[key].update(deepcopy(body)); states[key]['status'] = body['receipt']['verdict']
                operations[d['operation_id']] = {'kind': 'DECIDE', 'value': d, 'receipt': body['receipt']}
            elif row['kind'] == 'REVOKE':
                fields(body, ('revocation', 'receipt'))
                r = revocation(body['revocation']); key = r['request_id']
                authorize(m, r['reviewer_id'], 'REVIEWER')
                if key not in states or states[key]['status'] != 'QUALIFIED' or r['operation_id'] in operations:
                    fail('VALIDATION_FAILED', 'Revocation target is not an accepted claim')
                if r['certificate_sha256'] != fingerprint(states[key]['certificate']) or r['at'] < states[key]['decision']['at']:
                    fail('VALIDATION_FAILED', 'Revocation certificate/time mismatch')
                receipt = {'operation_id': r['operation_id'], 'request_id': key,
                    'certificate_sha256': r['certificate_sha256'], 'revocation_sha256': fingerprint(r),
                    'revoked': True, 'deployment_authorized': False}
                if body['receipt'] != receipt:
                    fail('VALIDATION_FAILED', 'Revocation receipt mismatch')
                revoked.setdefault(key, []).append(r)
                operations[r['operation_id']] = {'kind': 'REVOKE', 'value': r, 'receipt': receipt}
            else:
                fail('VALIDATION_FAILED', 'Unknown journal event')
        if head != meta['head']:
            fail('VALIDATION_FAILED', 'Journal head mismatch')
        return m, states, revoked, operations, {'count': meta['count'], 'head': head, 'bytes': used}

    def _append(self, db, kind, body, meta):
        if meta['count'] >= MAX_EVENTS or meta['bytes'] + len(encoded(body)) > MAX_HISTORY_BYTES:
            fail('BUDGET_EXHAUSTED', 'Qualification journal is full')
        event = {'seq': meta['count']+1, 'kind': kind, 'previous': meta['head'], 'body': body}
        h = fingerprint(event)
        db.execute('INSERT INTO events VALUES(?,?,?,?,?)',
                   (event['seq'], kind, encoded(body).decode(), meta['head'], h))
        db.execute('UPDATE meta SET count=?,head=? WHERE id=1', (event['seq'], h))
        # Check invariants before committing, not only when it is read next time.
        self._read(db)

    def inspect(self, request_id):
        identifier(request_id)
        with self._db() as db:
            _, states, _, _, _ = self._read(db)
            if request_id not in states:
                fail('INSUFFICIENT_EVIDENCE', 'Request does not exist')
            return {**deepcopy(states[request_id]), 'historical': True, 'deployment_authorized': False}

    def prepare(self, document, *, source, fault_at=None):
        req = request(document)
        if fault_at not in (None, 'after_prepare'):
            fail('VALIDATION_FAILED', 'Unknown prepare fault hook')
        source = require_source(source)
        with self._db() as db:
            m, states, revoked, _, meta = self._read(db)
            authorize(m, req['producer_id'], 'PRODUCER')
            if req['request_id'] in states:
                if states[req['request_id']]['request'] != req:
                    fail('CONSTRAINT_CONFLICT', 'Request identity already binds different content')
                return {**deepcopy(states[req['request_id']]), 'historical': True, 'deployment_authorized': False}
            _prerequisites(req, states, revoked); _source_current(req, source, states, revoked)
            self._append(db, 'PREPARE', req, meta)
        _fault('after_prepare', fault_at)
        return self.inspect(req['request_id'])

    def decide(self, document, *, source=None, fault_at=None):
        d = decision(document)
        if fault_at not in (None, 'after_verification', 'before_decision_commit', 'after_decision_commit'):
            fail('VALIDATION_FAILED', 'Unknown decision fault hook')
        with self._db() as db:
            m, states, revoked, operations, _ = self._read(db)
            if d['request_id'] not in states:
                fail('INSUFFICIENT_EVIDENCE', 'Decision requires a prepared request')
            s = states[d['request_id']]; req = s['request']
            authorize(m, d['reviewer_id'], 'REVIEWER', req['producer_id']); review_actor(req, d['reviewer_id'])
            if d['request_sha256'] != fingerprint(req) or d['at'] < req['at']:
                fail('CONSTRAINT_CONFLICT', 'Review targets another request or predates it')
            if d['operation_id'] in operations:
                op = operations[d['operation_id']]
                if op['kind'] != 'DECIDE' or op['value'] != d:
                    fail('CONSTRAINT_CONFLICT', 'Operation ID collision')
                return {**deepcopy(op['receipt']), 'historical': True}
            if s['status'] != 'PREPARED':
                fail('CONSTRAINT_CONFLICT', 'Decision is immutable; create a new request')
            if d['recommendation'] == 'ACCEPT':
                _prerequisites(req, states, revoked)
                _source_current(req, require_source(source), states, revoked)
        # Long numerical checks outside the owner transaction. Revalidate on publish.
        v = require_source(source).verify(req) if d['recommendation'] == 'ACCEPT' else _unrun(req)
        verification(v)
        _fault('after_verification', fault_at)
        with self._db() as db:
            m, states, revoked, operations, meta = self._read(db)
            s = states[d['request_id']]
            if d['operation_id'] in operations:
                op = operations[d['operation_id']]
                if op['kind'] == 'DECIDE' and op['value'] == d:
                    return {**deepcopy(op['receipt']), 'historical': True}
                fail('CONSTRAINT_CONFLICT', 'Operation ID collision')
            if s['status'] != 'PREPARED' or s['request'] != req:
                fail('CONSTRAINT_CONFLICT', 'Request changed while checking')
            authorize(m, d['reviewer_id'], 'REVIEWER', req['producer_id']); review_actor(req, d['reviewer_id'])
            if d['recommendation'] == 'ACCEPT':
                _source_current(req, require_source(source), states, revoked)
                if v['verdict'] == 'PASS':
                    _prerequisites(req, states, revoked)
            body = _publication(req, d, v, states)
            self._append(db, 'DECIDE', body, meta)
            _fault('before_decision_commit', fault_at)
        _fault('after_decision_commit', fault_at)
        return {**deepcopy(body['receipt']), 'historical': False}

    def revoke(self, document, *, fault_at=None):
        r = revocation(document)
        if fault_at not in (None, 'before_revocation_commit', 'after_revocation_commit'):
            fail('VALIDATION_FAILED', 'Unknown revocation fault hook')
        with self._db() as db:
            m, states, _, operations, meta = self._read(db)
            authorize(m, r['reviewer_id'], 'REVIEWER')
            if r['operation_id'] in operations:
                op = operations[r['operation_id']]
                if op['kind'] != 'REVOKE' or op['value'] != r:
                    fail('CONSTRAINT_CONFLICT', 'Revocation operation collision')
                return {**deepcopy(op['receipt']), 'historical': True}
            key = r['request_id']
            if key not in states or states[key]['status'] != 'QUALIFIED':
                fail('INSUFFICIENT_EVIDENCE', 'No accepted claim to revoke')
            if r['certificate_sha256'] != fingerprint(states[key]['certificate']) or r['at'] < states[key]['decision']['at']:
                fail('CONSTRAINT_CONFLICT', 'Revocation identity/time mismatch')
            receipt = {'operation_id': r['operation_id'], 'request_id': key,
                       'certificate_sha256': r['certificate_sha256'], 'revocation_sha256': fingerprint(r),
                       'revoked': True, 'deployment_authorized': False}
            self._append(db, 'REVOKE', {'revocation': r, 'receipt': receipt}, meta)
            _fault('before_revocation_commit', fault_at)
        _fault('after_revocation_commit', fault_at)
        return {**receipt, 'historical': False}

    def check_use(self, request_id, *, certificate_sha256, expected_claim, expected_binding, source):
        identifier(request_id); digest_value(certificate_sha256)
        expected_binding = binding(expected_binding)
        expected_claim = claim(expected_claim, source_format=expected_binding.get('source_format'))
        source = require_source(source)
        with self._db() as db:
            _, states, revoked, _, _ = self._read(db)
            state = _local(states, revoked, request_id)
            if (fingerprint(state['certificate']) != certificate_sha256 or state['request']['claim'] != expected_claim
                    or state['request']['binding'] != expected_binding):
                fail('INCOMPATIBLE_CONFIGURATION', 'Certificate cannot be widened or substituted')
            # Same exact binding for all prerequisites; one live source gate suffices.
            view = _source_current(state['request'], source, states, revoked)
            if state['verification']['checker_identity'] != view[5]:
                fail('INCOMPATIBLE_CONFIGURATION', 'Numerical verifier backend changed')
            return {'status': 'SUCCESS', 'request_id': request_id, 'certificate_sha256': certificate_sha256,
                    'claim': expected_claim, 'binding_sha256': fingerprint(expected_binding),
                    'evidence_satisfies_claim': True, 'historical': False,
                    'authority': AUTHORITY, 'deployment_authorized': False}

    def history(self, request_id):
        identifier(request_id)
        with self._db() as db:
            _, states, revoked, _, _ = self._read(db)
            if request_id not in states:
                fail('INSUFFICIENT_EVIDENCE', 'Request does not exist')
            return {'record': deepcopy(states[request_id]), 'revocations': deepcopy(revoked.get(request_id, [])),
                    'historical': True, 'deployment_authorized': False}

    def audit(self):
        with self._db() as db:
            _, states, revoked, _, meta = self._read(db)
            return {'status': 'SUCCESS', 'requests': len(states), 'events': meta['count'],
                    'chain_head': meta['head'], 'locally_revoked_claims': len(revoked),
                    'scope': 'STORED_STRUCTURE_ONLY_NOT_CURRENT_ELIGIBILITY', 'deployment_authorized': False}
