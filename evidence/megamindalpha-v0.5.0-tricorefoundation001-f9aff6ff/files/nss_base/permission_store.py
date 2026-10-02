"""Owned local operation grants: qualify != authorize != execute.

Consumption burns the grant BEFORE dispatch. An interrupted consumed grant cannot
be automatically replayed. Explicit reconciliation either records an authoritative
executor receipt or abandons the grant permanently. Actor IDs are local assertions.
"""
from copy import deepcopy
from datetime import datetime, timezone
import time

from .neural_contracts import encoded, fields, fingerprint
from .permission_contracts import (AUTHORITY, POLICY, POLICY_HASH, completion, epoch,
    grant, manifest, request, role)
from .permission_journal import PermissionJournal, fault
from .qualification_contracts import digest_value, identifier, text
from .qualification_sources import require_source
from .qualification_store import Qualifications
from .runtime import ContractError, fail


def now_seconds():
    """Trusted local wall clock. Tests patch this dependency, not request timestamps."""
    return epoch(int(time.time()))


def reduce_events(m, events):
    states = {}; denials = []; revocations = {}
    for event in events:
        kind = event['kind']; body = event['body']; at = event['at']
        if kind == 'DENY':
            fields(body, ('request_id', 'actor_id', 'operation', 'reason', 'observed_at'))
            identifier(body['request_id']); identifier(body['actor_id']); epoch(body['observed_at'])
            if body['operation'] not in ('ISSUE', 'BEGIN', 'DISPATCH'):
                fail('VALIDATION_FAILED', 'Unknown denied operation')
            text(body['reason'], 96); denials.append(body); continue
        if kind == 'ISSUE':
            fields(body, ('request', 'grant'))
            req = request(body['request']); g = grant(body['grant'], req, m); key = req['request_id']
            if key in states or g['issued_at'] != at:
                fail('VALIDATION_FAILED', 'Repeated grant or invalid issue time')
            states[key] = {'request': req, 'grant': g, 'status': 'GRANTED', 'revoked': False,
                           'completion': None, 'revocations': [], 'consumed_at': None, 'dispatch_at': None}
            continue
        if type(body) is not dict or 'request_id' not in body:
            fail('VALIDATION_FAILED', 'Event has no grant target')
        key = identifier(body['request_id'])
        if key not in states:
            fail('VALIDATION_FAILED', 'Event precedes its grant')
        s = states[key]; h = fingerprint(s['grant'])
        if kind == 'BEGIN':
            fields(body, ('request_id', 'grant_sha256', 'caller_id'))
            role(m, body['caller_id'], 'EXECUTOR')
            if (body['grant_sha256'] != h or body['caller_id'] != s['request']['caller_id']
                    or s['status'] != 'GRANTED' or s['revoked']
                    or not s['grant']['issued_at'] <= at < s['grant']['expires_at']):
                fail('VALIDATION_FAILED', 'Invalid or repeated grant consumption')
            s['status'] = 'STARTED'; s['consumed_at'] = at
        elif kind == 'DISPATCH':
            fields(body, ('request_id', 'grant_sha256', 'caller_id'))
            role(m, body['caller_id'], 'EXECUTOR')
            if (body['grant_sha256'] != h or body['caller_id'] != s['request']['caller_id']
                    or s['status'] != 'STARTED' or s['revoked']
                    or not s['grant']['issued_at'] <= at < s['grant']['expires_at']):
                fail('VALIDATION_FAILED', 'Invalid/repeated dispatch admission')
            s['status'] = 'DISPATCHED'; s['dispatch_at'] = at
        elif kind == 'REVOKE':
            fields(body, ('revocation_id', 'request_id', 'grant_sha256', 'actor_id', 'reason'))
            identifier(body['revocation_id']); role(m, body['actor_id'], 'ISSUER'); text(body['reason'])
            if body['grant_sha256'] != h or body['revocation_id'] in revocations:
                fail('VALIDATION_FAILED', 'Invalid/duplicate permission revocation')
            revocations[body['revocation_id']] = body
            s['revoked'] = True; s['revocations'].append(body)
        elif kind == 'UNCERTAIN':
            fields(body, ('request_id', 'grant_sha256', 'reason'))
            text(body['reason'], 96)
            if body['grant_sha256'] != h or s['status'] not in ('STARTED', 'DISPATCHED'):
                fail('VALIDATION_FAILED', 'Invalid uncertainty transition')
            s['status'] = 'UNCERTAIN'
        elif kind in ('COMPLETE', 'RECONCILE'):
            fields(body, ('request_id', 'grant_sha256', 'actor_id', 'receipt'))
            role(m, body['actor_id'], 'EXECUTOR' if kind == 'COMPLETE' else 'RECONCILER')
            if kind == 'COMPLETE' and body['actor_id'] != s['request']['caller_id']:
                fail('VALIDATION_FAILED', 'Completion actor differs from caller')
            if body['grant_sha256'] != h or s['status'] not in ('STARTED', 'DISPATCHED', 'UNCERTAIN'):
                fail('VALIDATION_FAILED', 'Invalid completion transition')
            if s['dispatch_at'] is None:
                fail('VALIDATION_FAILED', 'A result cannot complete an undispatched grant')
            completion(body['receipt'], s['request'], h)
            s['status'] = 'COMMITTED'; s['completion'] = body['receipt']
        elif kind == 'ABANDON':
            fields(body, ('request_id', 'grant_sha256', 'actor_id', 'executor_absence_sha256'))
            role(m, body['actor_id'], 'RECONCILER'); digest_value(body['executor_absence_sha256'])
            if body['grant_sha256'] != h or s['status'] not in ('STARTED', 'DISPATCHED', 'UNCERTAIN'):
                fail('VALIDATION_FAILED', 'Invalid abandonment transition')
            s['status'] = 'ABANDONED'
        else:
            fail('VALIDATION_FAILED', 'Unknown permission event kind')
    return {'grants': states, 'denials': denials, 'revocations': revocations}


def _source_check(req, qs, source, at):
    if type(qs) is not Qualifications:
        fail('VALIDATION_FAILED', 'Only the local QualificationEvidence002 owner is supported')
    source = require_source(source)
    observation = qs.check_use(req['qualification_id'], certificate_sha256=req['certificate_sha256'],
        expected_claim=req['claim'], expected_binding=req['binding'], source=source)
    cert = qs.inspect(req['qualification_id'])['certificate']
    issued = int(datetime.strptime(cert['issued_at'], '%Y-%m-%dT%H:%M:%SZ').replace(tzinfo=timezone.utc).timestamp())
    if issued > at:
        fail('AUTHORIZATION_DENIED', 'Qualification evidence is future-dated')
    return observation


class Permissions:
    def __init__(self, directory):
        self.journal = PermissionJournal(directory)
        self.audit()

    @classmethod
    def create(cls, directory, operators):
        PermissionJournal.create(directory, operators)
        return cls(directory)

    def _read(self, db):
        return self.journal.read(db, reduce_events)

    def _append(self, db, meta, kind, at, body):
        self.journal.append(db, reduce_events, meta, kind, at, body)

    def _deny(self, req, actor, operation, code):
        # Malformed requests are rejected before this boundary. Stored denials omit
        # arbitrary exception strings, source data and output contents.
        with self.journal.transaction() as db:
            _, _, meta, _ = self._read(db); observed = now_seconds()
            self._append(db, meta, 'DENY', max(meta['last_at'], observed),
                {'request_id': req['request_id'], 'actor_id': actor, 'operation': operation,
                 'reason': code, 'observed_at': observed})

    def _target(self, m, states, req, h, actor, *, control=False):
        role(m, actor, 'RECONCILER' if control else 'EXECUTOR')
        s = states['grants'].get(req['request_id'])
        if s is None:
            fail('INSUFFICIENT_EVIDENCE', 'No issued grant for this request')
        if s['request'] != req or fingerprint(s['grant']) != h:
            fail('INCOMPATIBLE_CONFIGURATION', 'Request/grant substitution is forbidden')
        if not control and actor != req['caller_id']:
            fail('AUTHORIZATION_DENIED', 'Grant belongs to a different caller')
        return s

    @staticmethod
    def _live(s, at, last):
        if at < last or at < s['grant']['issued_at']:
            fail('AUTHORIZATION_DENIED', 'Clock rollback or grant not yet valid')
        if s['revoked'] or at >= s['grant']['expires_at']:
            fail('AUTHORIZATION_DENIED', 'Grant revoked or expired')

    def inspect(self, request_id):
        identifier(request_id)
        with self.journal.transaction() as db:
            _, states, _, _ = self._read(db)
            if request_id not in states['grants']:
                fail('INSUFFICIENT_EVIDENCE', 'Unknown permission request')
            return {**deepcopy(states['grants'][request_id]), 'historical': True,
                    'deployment_authorized': False, 'runtime_execution_permit': False}

    def issue(self, document, *, issuer_id, ttl_seconds, qualifications, source, fault_at=None):
        req = request(document); identifier(issuer_id)
        if type(ttl_seconds) is not int or not 1 <= ttl_seconds <= POLICY['max_ttl_seconds']:
            fail('VALIDATION_FAILED', 'Grant TTL outside local policy')
        if fault_at not in (None, 'before_issue_commit', 'after_issue_commit'):
            fail('VALIDATION_FAILED', 'Unknown issue fault point')
        try:
            with self.journal.transaction() as db:
                m, states, meta, _ = self._read(db)
                role(m, issuer_id, 'ISSUER'); role(m, req['caller_id'], 'EXECUTOR')
                if issuer_id == req['caller_id']:
                    fail('AUTHORIZATION_DENIED', 'Self-issued operation grant denied')
                existing = states['grants'].get(req['request_id'])
                if existing:
                    g = existing['grant']
                    if (existing['request'] != req or g['issuer_id'] != issuer_id
                            or g['expires_at']-g['issued_at'] != ttl_seconds):
                        fail('CONSTRAINT_CONFLICT', 'Request ID already binds another grant')
                    return {**deepcopy(existing), 'historical': True}
                at = now_seconds()
                if at < meta['last_at']:
                    fail('AUTHORIZATION_DENIED', 'Observed clock rollback')
                _source_check(req, qualifications, source, at)
                at = now_seconds()
                _source_check(req, qualifications, source, at)
                g = grant({'schema_version': 1, 'store_id': m['store_id'], 'request_id': req['request_id'],
                    'request_sha256': fingerprint(req), 'caller_id': req['caller_id'], 'issuer_id': issuer_id,
                    'issued_at': at, 'expires_at': at+ttl_seconds, 'policy_sha256': POLICY_HASH,
                    'max_uses': 1, 'authority': AUTHORITY, 'deployment_authorized': False,
                    'runtime_execution_permit': False, 'delegable': False}, req, m)
                self._append(db, meta, 'ISSUE', at, {'request': req, 'grant': g})
                fault(fault_at, 'before_issue_commit')
            fault(fault_at, 'after_issue_commit')
        except ContractError as exc:
            self._deny(req, issuer_id, 'ISSUE', exc.code); raise
        return {**self.inspect(req['request_id']), 'historical': False}

    def begin(self, document, *, grant_sha256, caller_id, qualifications, source, fault_at=None):
        req = request(document); digest_value(grant_sha256); identifier(caller_id)
        if fault_at not in (None, 'before_consume_commit', 'after_consume_commit'):
            fail('VALIDATION_FAILED', 'Unknown consumption fault point')
        try:
            with self.journal.transaction() as db:
                m, states, meta, _ = self._read(db)
                s = self._target(m, states, req, grant_sha256, caller_id)
                if s['status'] == 'COMMITTED':
                    return {'status': 'COMMITTED', 'receipt': deepcopy(s['completion']), 'historical': True}
                if s['status'] != 'GRANTED':
                    fail('RECOVERY_REQUIRED', 'Spent grant requires explicit reconciliation or a new request')
                self._live(s, now_seconds(), meta['last_at'])
                _source_check(req, qualifications, source, now_seconds())
                at = now_seconds(); self._live(s, at, meta['last_at'])
                self._append(db, meta, 'BEGIN', at,
                    {'request_id': req['request_id'], 'grant_sha256': grant_sha256, 'caller_id': caller_id})
                fault(fault_at, 'before_consume_commit')
            fault(fault_at, 'after_consume_commit')
            return {'status': 'STARTED', 'historical': False, 'deployment_authorized': False}
        except ContractError as exc:
            self._deny(req, caller_id, 'BEGIN', exc.code); raise

    def check_dispatch(self, document, *, grant_sha256, caller_id, qualifications, source):
        req = request(document); digest_value(grant_sha256); identifier(caller_id)
        try:
            with self.journal.transaction() as db:
                m, states, meta, _ = self._read(db)
                s = self._target(m, states, req, grant_sha256, caller_id)
                if s['status'] != 'STARTED':
                    fail('RECOVERY_REQUIRED', 'Only the newly consumed grant may dispatch')
                self._live(s, now_seconds(), meta['last_at'])
                _source_check(req, qualifications, source, now_seconds())
                at = now_seconds(); self._live(s, at, meta['last_at'])
                self._append(db, meta, 'DISPATCH', at,
                    {'request_id': req['request_id'], 'grant_sha256': grant_sha256, 'caller_id': caller_id})
            return {'status': 'SUCCESS', 'scope': 'POINT_IN_TIME_LOCAL_DISPATCH_ONLY'}
        except ContractError as exc:
            self._deny(req, caller_id, 'DISPATCH', exc.code); raise

    def mark_uncertain(self, request_id, grant_sha256, reason):
        identifier(request_id); digest_value(grant_sha256); text(reason, 96)
        with self.journal.transaction() as db:
            _, states, meta, _ = self._read(db)
            s = states['grants'].get(request_id)
            if s is None or fingerprint(s['grant']) != grant_sha256:
                fail('INCOMPATIBLE_CONFIGURATION', 'Unknown spent grant')
            if s['status'] in ('STARTED', 'DISPATCHED'):
                self._append(db, meta, 'UNCERTAIN', max(now_seconds(), meta['last_at']),
                    {'request_id': request_id, 'grant_sha256': grant_sha256, 'reason': reason})

    def revoke(self, request_id, *, grant_sha256, actor_id, revocation_id, reason, fault_at=None):
        identifier(request_id); identifier(actor_id); identifier(revocation_id); digest_value(grant_sha256); text(reason)
        if fault_at not in (None, 'before_revoke_commit', 'after_revoke_commit'):
            fail('VALIDATION_FAILED', 'Unknown revocation fault point')
        body = {'revocation_id': revocation_id, 'request_id': request_id, 'grant_sha256': grant_sha256,
                'actor_id': actor_id, 'reason': reason}
        with self.journal.transaction() as db:
            m, states, meta, _ = self._read(db); role(m, actor_id, 'ISSUER')
            old = states['revocations'].get(revocation_id)
            if old:
                if old != body: fail('CONSTRAINT_CONFLICT', 'Revocation ID collision')
                return {'revoked': True, 'historical': True}
            s = states['grants'].get(request_id)
            if s is None or fingerprint(s['grant']) != grant_sha256:
                fail('INCOMPATIBLE_CONFIGURATION', 'Wrong revocation target')
            self._append(db, meta, 'REVOKE', now_seconds(), body); fault(fault_at, 'before_revoke_commit')
        fault(fault_at, 'after_revoke_commit')
        return {'revoked': True, 'historical': False}

    def finish(self, document, *, grant_sha256, actor_id, executor, reconcile=False, fault_at=None):
        # Receipt owner is separate; no arbitrary caller scores/completion values.
        from .permission_executor import require_executor
        req = request(document); digest_value(grant_sha256); identifier(actor_id)
        executor = require_executor(executor)
        if type(reconcile) is not bool or fault_at not in (None, 'before_completion_commit', 'after_completion_commit'):
            fail('VALIDATION_FAILED', 'Unknown completion mode/fault')
        with self.journal.transaction() as db:
            m, states, meta, _ = self._read(db)
            s = self._target(m, states, req, grant_sha256, actor_id, control=reconcile)
            receipt = executor.lookup(req, grant_sha256)
            if s['status'] == 'COMMITTED':
                if receipt != s['completion']:
                    fail('RECOVERY_REQUIRED', 'Committed permission has no matching executor receipt')
                return {'status': 'COMMITTED', 'receipt': deepcopy(receipt), 'historical': True}
            if s['status'] == 'ABANDONED' and reconcile:
                if receipt is not None: fail('RECOVERY_REQUIRED', 'Abandoned request later acquired a result')
                return {'status': 'ABANDONED', 'historical': True}
            if s['status'] not in ('STARTED', 'DISPATCHED', 'UNCERTAIN'):
                fail('CONSTRAINT_CONFLICT', 'Only a spent grant can complete/reconcile')
            body = {'request_id': req['request_id'], 'grant_sha256': grant_sha256, 'actor_id': actor_id}
            if receipt is None:
                if not reconcile: fail('RECOVERY_REQUIRED', 'Executor result is absent')
                body['executor_absence_sha256'] = fingerprint({'request_sha256': fingerprint(req),
                    'grant_sha256': grant_sha256, 'receipt': None, 'policy': 'ABANDON_WITHOUT_RETRY'})
                kind = 'ABANDON'; status = 'ABANDONED'
            else:
                if s['dispatch_at'] is None:
                    fail('RECOVERY_REQUIRED', 'Executor receipt exists without dispatch admission')
                body['receipt'] = completion(receipt, req, grant_sha256)
                kind = 'RECONCILE' if reconcile else 'COMPLETE'; status = 'COMMITTED'
            # Recording an already performed operation does not need renewed data
            # permission or an unexpired grant; it cannot dispatch new computation.
            self._append(db, meta, kind, max(now_seconds(), meta['last_at']), body)
            fault(fault_at, 'before_completion_commit')
        fault(fault_at, 'after_completion_commit')
        return {'status': status, 'receipt': deepcopy(receipt), 'historical': False,
                'deployment_authorized': False}

    def audit(self):
        with self.journal.transaction() as db:
            _, states, meta, _ = self._read(db)
            return {'status': 'SUCCESS', 'grants': len(states['grants']), 'denials': len(states['denials']),
                    'events': meta['count'], 'head': meta['head'],
                    'scope': 'STORED_STRUCTURE_NOT_CURRENT_AUTHORIZATION', 'deployment_authorized': False}

    def history(self):
        with self.journal.transaction() as db:
            _, _, _, events = self._read(db)
            return {'historical': True, 'events': deepcopy(events)}
