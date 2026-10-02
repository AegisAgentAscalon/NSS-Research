"""Local generation catalogue, release journal and single-worker stage boundary.

Owns only its generation database. Child qualifications and neural sources are read
through public APIs. This does not modify the integer RecoveryStore, replay grants,
active serving processes or generic Aegis Runtime. Public adoption is registry-level.
"""
from copy import deepcopy
from pathlib import Path
import os
import secrets
import time

from .generation_contracts import (FORMAT, OPERATION, POLICY, POLICY_HASH, artifact_bundle,
    exact, generation, generation_certificate, release_grant, release_request, role, store_manifest)
from .generation_evidence import check_family
from .generation_state import (family, qualified, quiescent, receipt_for, reduce_events,
    release, source_matches, ticket_for, usable)
from .local_journal import EventJournal, epoch, fault
from .neural_contracts import fingerprint
from .qualification_contracts import digest_value, identifier, text
from .runtime import fail
from .catalog_contracts import (command, descriptor, select_profile, selection_request,
    task_identity, verify_document_sizes)
from .catalog_tasks import catalog_entry, require_current, source_task, receipt, followup_request
from .ledger import Ledger
from .task_records import advance_record, validate_receipts, source_fields, finish_record
from .state_contracts import ACTIONS as STATE_ACTIONS, check_scope, revision_check
from .state_updates import apply_delta
from .state_sources import check_state_sources, check_delta_sources


def now_seconds():
    return epoch(int(time.time()))


def _journal_manifest(value):
    if type(value) is dict and value.get('format') == 'NSS.TriCoreFoundation001':
        from .foundation_contracts import store_manifest as current_manifest
        return current_manifest(value)
    return store_manifest(value)


from .foundation_store import FoundationOperations


class GenerationJournal(EventJournal):
    filename = 'generations.sqlite3'
    validate_manifest = staticmethod(_journal_manifest)
    max_history_bytes = 32 * 1024 * 1024


def _hook(value, choices):
    if value is not None and value not in choices:
        fail('VALIDATION_FAILED', 'Unknown generation fault hook')


def _summary(r, historical=False):
    return {**deepcopy(r), 'historical': historical, 'runtime_execution_permit': False,
            'production_deployment_authorized': False}


class Generations(FoundationOperations):
    """One trusted-local worker; declared roles are not authenticated identities.

    PREPARED consumes the local release grant. Resumption revalidates current evidence
    and expiry before each remaining LOCAL operation. No external side effect is
    replayed. PUBLISHED is definitive durable history, never permission to republish.
    """
    def __init__(self, directory):
        self.journal = GenerationJournal(directory)
        with self.journal.transaction() as db:
            self.journal.read(db, reduce_events)

    @classmethod
    def create(cls, directory, operators):
        GenerationJournal.create_document(directory, {'schema_version': 1, 'format': FORMAT,
            'store_id': secrets.token_hex(16), 'policy_sha256': POLICY_HASH, 'operators': operators})
        return cls(directory)

    @classmethod
    def create_foundation(cls, directory, operators, config):
        from .foundation_contracts import configuration, FORMAT, POLICY_SHA256
        configuration(config)
        GenerationJournal.create_document(directory, {'schema_version': 2, 'format': FORMAT,
            'store_id': secrets.token_hex(16), 'policy_sha256': POLICY_SHA256,
            'operators': deepcopy(operators), 'initial_configuration': deepcopy(config)})
        return cls(directory)

    def _read(self, db):
        m, s, meta, _ = self.journal.read(db, reduce_events)
        return m, s, meta

    def _write(self, db, meta, kind, body, fault_at=None, *, at=None):
        self.journal.append(db, reduce_events, meta, kind, now_seconds() if at is None else at, body)
        fault(fault_at, 'before_' + kind.lower() + '_commit')

    def inspect(self):
        with self.journal.transaction() as db:
            m, s, meta = self._read(db)
            if m.get('format') == 'NSS.TriCoreFoundation001':
                return {'format': m['format'], 'current': deepcopy(s['current']),
                    'events': meta['count'], 'open_tasks': sum(not t['closed'] for t in s['tasks'].values()),
                    'busy': deepcopy(s['busy']), 'runtime_execution_permit': False}
            states = {h: ('CURRENT' if h == s['current']['generation_sha256'] else
                         'ARCHIVED' if h in s['published'] else
                         'QUALIFIED' if f['certificate'] else 'CANDIDATE')
                      for h, f in s['generations'].items()}
            return {'current': deepcopy(s['current']), 'generations': states,
                    'open_stages': sum(not t['closed'] for t in s['tickets'].values()),
                    'events': meta['count'], 'historical': True,
                    'scope': 'STRUCTURE_ONLY_NOT_CURRENT_ELIGIBILITY'}

    def inspect_generation(self, generation_sha256):
        with self.journal.transaction() as db:
            _, s, _ = self._read(db)
            return {**deepcopy(family(s, generation_sha256)), 'historical': True}

    def inspect_release(self, release_id):
        with self.journal.transaction() as db:
            _, s, _ = self._read(db)
            return _summary(release(s, release_id), True)

    def inspect_stage(self, ticket_id, *, caller_id=None, scope=None):
        identifier(ticket_id)
        with self.journal.transaction() as db:
            _, s, _ = self._read(db)
            if ticket_id not in s['tickets']:
                fail('INSUFFICIENT_EVIDENCE', 'Unknown managed stage')
            saved = s['tickets'][ticket_id]
            self._scope_history(saved, caller_id, scope)
            return {**deepcopy(saved), 'historical': True}

    def propose(self, document, *, qualifications, source):
        g = generation(document); h = fingerprint(g)
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, g['producer_id'], 'PRODUCER')
            if h in s['generations']:
                return {'generation_sha256': h, 'historical': True}
            if any(g['generation_id'] == f['manifest']['generation_id'] for f in s['generations'].values()):
                fail('CONSTRAINT_CONFLICT', 'Generation ID already binds another immutable manifest')
            check_family(g, qualifications=qualifications, source=source)
            self._write(db, meta, 'PROPOSE', g)
        return {'generation_sha256': h, 'historical': False}

    def qualify(self, generation_sha256, *, reviewer_id, qualifications, source):
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); f = family(s, generation_sha256)
            role(m, reviewer_id, 'REVIEWER')
            if f['certificate'] is not None:
                if f['certificate']['reviewer_id'] != reviewer_id:
                    fail('CONSTRAINT_CONFLICT', 'Generation qualification already sealed by another reviewer')
                return {**deepcopy(f['certificate']), 'historical': True}
            if reviewer_id == f['manifest']['producer_id']:
                fail('AUTHORIZATION_DENIED', 'Producer cannot qualify its own generation')
            check_family(f['manifest'], qualifications=qualifications, source=source)
            c = generation_certificate(f['manifest'], reviewer_id, now_seconds(), m)
            self._write(db, meta, 'QUALIFY', {'generation_sha256': generation_sha256, 'certificate': c}, at=c['issued_at'])
        return {**c, 'historical': False}

    def make_request(self, target_sha256, *, release_id, caller_id, mode, reason):
        """Construct a request; no authority is conferred by construction."""
        with self.journal.transaction() as db:
            m, s, _ = self._read(db); role(m, caller_id, 'OPERATOR'); f = qualified(s, target_sha256)
            return release_request({'schema_version': 1, 'release_id': release_id, 'operation': OPERATION,
                'caller_id': caller_id, 'target_sha256': target_sha256,
                'generation_certificate_sha256': fingerprint(f['certificate']),
                'expected_current': deepcopy(s['current']), 'mode': mode, 'reason': reason})

    def issue(self, document, *, issuer_id, ttl_seconds, qualifications, source, fault_at=None):
        req = release_request(document)
        _hook(fault_at, ('before_issue_commit', 'after_issue_commit'))
        if type(ttl_seconds) is not int or not 1 <= ttl_seconds <= POLICY['max_ttl_seconds']:
            fail('VALIDATION_FAILED', 'Invalid release grant duration')
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, issuer_id, 'ISSUER')
            if req['release_id'] in s['releases']:
                r = s['releases'][req['release_id']]
                exact(req, r['request'])
                if r['grant']['issuer_id'] != issuer_id or r['grant']['expires_at']-r['grant']['issued_at'] != ttl_seconds:
                    fail('CONSTRAINT_CONFLICT', 'Retry cannot rewrite grant identity/lifetime')
                return _summary(r, True)
            f = qualified(s, req['target_sha256']); source_matches(s, req)
            if fingerprint(f['certificate']) != req['generation_certificate_sha256']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Request names different qualification')
            if issuer_id == f['manifest']['binding'].get('candidate_lineage', {}).get('producer_id'):
                fail('AUTHORIZATION_DENIED','Candidate producer cannot issue its own release approval')
            check_family(f['manifest'], qualifications=qualifications, source=source)
            now = now_seconds(); g = release_grant(req, issuer_id, now, now+ttl_seconds, m)
            self._write(db, meta, 'ISSUE', {'request': req, 'grant': g}, fault_at, at=now)
        fault(fault_at, 'after_issue_commit')
        return {**self.inspect_release(req['release_id']), 'historical': False}

    def _advance(self, kind, release_id, grant_sha256, caller_id, qualifications, source, fault_at):
        _hook(fault_at, ('before_'+kind.lower()+'_commit', 'after_'+kind.lower()+'_commit'))
        digest_value(grant_sha256)
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, caller_id, 'OPERATOR'); r = release(s, release_id)
            if r['request']['caller_id'] != caller_id or fingerprint(r['grant']) != grant_sha256:
                fail('AUTHORIZATION_DENIED', 'Wrong release caller or grant identity')
            if r['status'] == 'PUBLISHED':
                return _summary(r, True)  # history cannot change the current pointer
            usable(s, r, now_seconds()); quiescent(s)
            g = qualified(s, r['request']['target_sha256'])['manifest']
            artifacts = check_family(g, qualifications=qualifications, source=source)
            expected = {'PREPARE': 'GRANTED', 'STAGE': 'PREPARED', 'PUBLISH': 'STAGED'}[kind]
            if r['status'] != expected:
                if (kind == 'PREPARE' and r['status'] in ('PREPARED', 'STAGED')) or (kind == 'STAGE' and r['status'] == 'STAGED'):
                    return _summary(r, True)  # live guard still ran; not a fresh authority
                fail('CONSTRAINT_CONFLICT', 'Release has not reached the required preceding state')
            b = {'release_id': release_id, 'caller_id': caller_id}
            if kind == 'STAGE': b['artifacts'] = artifacts
            if kind == 'PUBLISH':
                artifact_bundle(r['artifacts'], g); exact(artifacts, r['artifacts'])
                b['receipt'] = receipt_for(s, r)
            # Reducer rechecks observed time, pointer, revocation and quiescence here.
            self._write(db, meta, kind, b, fault_at)
        fault(fault_at, 'after_'+kind.lower()+'_commit')
        return {**self.inspect_release(release_id), 'historical': False}

    def prepare(self, release_id, *, grant_sha256, caller_id, qualifications, source, fault_at=None):
        return self._advance('PREPARE', release_id, grant_sha256, caller_id, qualifications, source, fault_at)

    def stage(self, release_id, *, grant_sha256, caller_id, qualifications, source, fault_at=None):
        return self._advance('STAGE', release_id, grant_sha256, caller_id, qualifications, source, fault_at)

    def publish(self, release_id, *, grant_sha256, caller_id, qualifications, source, fault_at=None):
        return self._advance('PUBLISH', release_id, grant_sha256, caller_id, qualifications, source, fault_at)

    def abandon(self, release_id, *, caller_id, reason):
        text(reason)
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, caller_id, 'OPERATOR'); r = release(s, release_id)
            if r['request']['caller_id'] != caller_id: fail('AUTHORIZATION_DENIED', 'Wrong release caller')
            if r['status'] == 'PUBLISHED': fail('CONSTRAINT_CONFLICT', 'Published world cannot be undone by abandonment')
            if r['status'] != 'ABANDONED':
                self._write(db, meta, 'ABANDON', {'release_id': release_id, 'caller_id': caller_id, 'reason': reason})
        return self.inspect_release(release_id)

    def revoke(self, identity, *, kind, actor_id, reason):
        if kind not in ('RELEASE', 'QUALIFICATION'):
            fail('VALIDATION_FAILED', 'Unknown revocation kind')
        text(reason)
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, actor_id, 'ISSUER' if kind == 'RELEASE' else 'REVIEWER')
            obj = release(s, identity) if kind == 'RELEASE' else family(s, identity)
            if not obj['revoked']:
                self._write(db, meta, 'REVOKE_'+kind, {'id': identity, 'actor_id': actor_id, 'reason': reason})
        return {'status': 'REVOKED', 'identity': identity, 'current_pointer_changed': False}

    def pin_stage(self, ticket_id, *, profile, caller_id, qualifications, source):
        """All work in this single-worker catalogue must register a managed stage."""
        identifier(ticket_id)
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, caller_id, 'OPERATOR')
            if ticket_id in s['tickets']: fail('CONSTRAINT_CONFLICT', 'Stage IDs cannot be recycled')
            quiescent(s); t = ticket_for(s, m['store_id'], ticket_id, profile, caller_id)
            f = qualified(s, s['current']['generation_sha256'])
            check_family(f['manifest'], qualifications=qualifications, source=source)
            self._write(db, meta, 'PIN', {'ticket': t})
        return deepcopy(t)

    def read_stage(self, ticket, *, caller_id, qualifications, source):
        """Return sealed artifacts, not a serving execution permit or a cache."""
        with self.journal.transaction() as db:
            m, s, _ = self._read(db); role(m, caller_id, 'OPERATOR')
            saved = self._ticket(s, ticket, caller_id)
            if 'work' in saved:
                fail('CONSTRAINT_CONFLICT', 'Use read_task_stage for task-bound reads and receipt checks')
            if saved['closed'] or ticket['configuration'] != s['current']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Closed/stale stage; rebuild from portable inputs')
            f = qualified(s, s['current']['generation_sha256'])
            check_family(f['manifest'], qualifications=qualifications, source=source)
            published = release(s, s['published'][s['current']['generation_sha256']])
            artifacts = artifact_bundle(published['artifacts'], f['manifest'])
            p = next(p for p in f['manifest']['profiles'] if p['id'] == ticket['profile'])
            artifacts = {k: artifacts[k] for k in ['core'] + p['members']}
            return {'ticket': deepcopy(ticket), 'state_identity': fingerprint(ticket), 'artifacts': artifacts,
                    'runtime_execution_permit': False}

    @staticmethod
    def _ticket(s, ticket, caller_id):
        if type(ticket) is not dict or type(ticket.get('ticket_id')) is not str or ticket['ticket_id'] not in s['tickets']:
            fail('VALIDATION_FAILED', 'Unknown managed stage')
        saved = s['tickets'][ticket['ticket_id']]; exact(ticket, saved['ticket'])
        if ticket['caller_id'] != caller_id: fail('AUTHORIZATION_DENIED', 'Wrong stage caller')
        return saved

    def close_stage(self, ticket, *, caller_id):
        # Closing after revocation is allowed; it authorizes no new computation.
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, caller_id, 'OPERATOR')
            saved = self._ticket(s, ticket, caller_id)
            if 'work' in saved:
                fail('CONSTRAINT_CONFLICT', 'Use the task CLOSE/CANCEL contract; plain unpin loses task semantics')
            if not saved['closed']: self._write(db, meta, 'UNPIN', {'ticket': deepcopy(ticket)})
        return {'status': 'CLOSED', 'ticket_id': ticket['ticket_id']}

    def register_catalog(self, document, *, reviewer_id, qualifications, source):
        """Seal reviewed routing metadata. This is NOT new neural qualification."""
        if type(document) is not dict or 'generation_sha256' not in document:
            fail('VALIDATION_FAILED', 'Exact descriptor required')
        with self.journal.transaction() as db:
            m, s, meta = self._read(db)
            g = qualified(s, document['generation_sha256'])['manifest']
            d = descriptor(document, g); h = fingerprint(d)
            role(m, d['author_id'], 'PRODUCER'); role(m, reviewer_id, 'REVIEWER')
            if reviewer_id == d['author_id']:
                fail('AUTHORIZATION_DENIED', 'Author cannot review its own routing declarations')
            if h in s['catalogs']:
                exact(s['catalogs'][h], {'descriptor': d, 'reviewer_id': reviewer_id})
                return {'catalog_sha256': h, 'historical': True, 'runtime_execution_permit': False}
            artifacts = check_family(g, qualifications=qualifications, source=source)
            verify_document_sizes(d, g, artifacts)
            self._write(db, meta, 'CATALOG_REGISTER', {'descriptor': d, 'reviewer_id': reviewer_id})
        return {'catalog_sha256': h, 'historical': False, 'runtime_execution_permit': False}

    def inspect_task(self, task_id, *, caller_id=None, scope=None):
        """History only: never authorizes computation or restores a closed stage."""
        identifier(task_id)
        with self.journal.transaction() as db:
            _, s, _ = self._read(db)
            if task_id not in s['task_heads']: fail('INSUFFICIENT_EVIDENCE', 'Unknown task')
            saved = s['tickets'][s['task_heads'][task_id]]
            self._scope_history(saved, caller_id, scope)
            return {**deepcopy(saved), 'historical': True}

    @staticmethod
    def _scope_history(saved, caller_id, scope):
        if 'work' in saved and saved['work']['record']['schema_version'] == 2:
            check_scope(saved['work']['record'], scope)
            if caller_id != saved['ticket']['caller_id']:
                fail('AUTHORIZATION_DENIED', 'Scoped historical read belongs to another task holder')

    def inspect_state_history(self, task_id, *, caller_id, scope):
        """Scoped local inspection, including source/review lineage; no renewed use."""
        identifier(task_id)
        with self.journal.transaction() as db:
            _, s, _, events = self.journal.read(db, reduce_events)
            if task_id not in s['task_heads']: fail('INSUFFICIENT_EVIDENCE', 'Unknown task')
            saved = s['tickets'][s['task_heads'][task_id]]
            if saved['work']['record']['schema_version'] != 2:
                fail('INCOMPATIBLE_CONFIGURATION', 'No scope was established for this legacy history')
            self._scope_history(saved, caller_id, scope)
            history = [{'sequence': e['seq'], 'committed_at': e['at'],
                        'command': deepcopy(e['body']['command']), 'record': deepcopy(e['body']['record']),
                        'receipt': deepcopy(e['body']['receipt'])}
                       for e in events if e['kind'] == 'CATALOG_TASK' and e['body']['record']['task_id'] == task_id]
            return {'task_id': task_id, 'scope': deepcopy(scope), 'history': history,
                    'historical': True, 'training_authorized': False, 'runtime_execution_permit': False}

    def _catalog_current(self, s, req, qualifications, source):
        d, g = require_current(s, req)
        artifacts = check_family(g, qualifications=qualifications, source=source)
        verify_document_sizes(d, g, artifacts)
        return d, g, artifacts

    def describe_catalog(self, *, expected_current, catalog_sha256=None, qualifications, source):
        """Live exact metadata lookup; no artifacts or serving authority returned."""
        from .generation_contracts import configuration
        configuration(expected_current)
        with self.journal.transaction() as db:
            _, s, _ = self._read(db)
            if expected_current != s['current']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Catalogue lookup targets a stale generation epoch')
            if catalog_sha256 is None:
                keys = [h for h, item in s['catalogs'].items()
                        if item['descriptor']['generation_sha256'] == s['current']['generation_sha256']]
                if not keys: fail('CAPABILITY_UNAVAILABLE', 'Current generation has no reviewed catalogue')
                if len(keys) != 1: fail('NEEDS_CLARIFICATION', 'Specify an exact reviewed catalogue version')
                catalog_sha256 = keys[0]
            digest_value(catalog_sha256)
            req = {'expected_current': expected_current, 'catalog_sha256': catalog_sha256}
            d, _, _ = self._catalog_current(s, req, qualifications, source)
            return {'catalog_sha256': catalog_sha256, 'configuration': deepcopy(s['current']),
                    'descriptor': deepcopy(d), 'reviewer_id': catalog_entry(s, catalog_sha256)['reviewer_id'],
                    'historical': False, 'runtime_execution_permit': False}

    def select_stage(self, request, *, caller_id, qualifications, source, source_ticket=None,
                     expected_record_sha256=None, scope=None):
        req = selection_request(request)
        with self.journal.transaction() as db:
            m, s, _ = self._read(db); role(m, caller_id, 'OPERATOR')
            d, g, _ = self._catalog_current(s, req, qualifications, source)
            previous = None
            if source_ticket is not None:
                digest_value(expected_record_sha256)
                previous = source_task(s, source_ticket, caller_id, expected_record_sha256, scope)
                followup_request(previous, req)
            elif req['task_id'] in s['task_heads']:
                fail('CONSTRAINT_CONFLICT', 'Existing task requires an exact current stage ticket')
            return select_profile(d, g, req, previous['ticket']['profile'] if previous else None)

    @staticmethod
    def _input_owners(ledger, evidence_root):
        if type(ledger) is not Ledger:
            fail('VALIDATION_FAILED', 'Installed local mock Ledger required; no arbitrary action callbacks')
        if not isinstance(evidence_root, (str, os.PathLike)):
            fail('VALIDATION_FAILED', 'Local source root path required')
        return {'source_root': str(Path(evidence_root).resolve()),
                'ledger_path': str(ledger.path.resolve()), 'world_path': str(ledger.world.resolve())}

    def task_operation(self, value, *, ledger, evidence_root, qualifications=None, source=None, archive=None, fault_at=None):
        """Atomically mutate record + pin + history. Never executes/replays effects.

        START/MOVE/state deltas recheck current source/certificate eligibility.
        FINISH/CLOSE/CANCEL
        preserve already-performed work after revocation and authorize no new use.
        """
        c = command(value); action = c['action'].lower()
        _hook(fault_at, ('before_'+action+'_commit', 'after_'+action+'_commit'))
        owners = self._input_owners(ledger, evidence_root)
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); role(m, c['caller_id'], 'OPERATOR')
            prior = s['task_operations'].get(c['operation_id'])
            if prior is not None:
                exact(c, prior['command'])
                return {**deepcopy(prior['receipt']), 'historical': True}
            old = None
            if c['action'] != 'START':
                old = source_task(s, c['source_ticket'], c['caller_id'],
                    None if c['action'] in STATE_ACTIONS else c['expected_record_sha256'],
                    None if c['action'] == 'BIND_STATE' else c.get('scope'))
                if c['action'] in STATE_ACTIONS: revision_check(old['work']['record'], c, old['ticket']['profile_ecid'])
                exact(owners, old['work']['inputs'])
            if c['action'] in ('START', 'MOVE'):
                req = c['request']; d, g, _ = self._catalog_current(s, req, qualifications, source)
                selected = select_profile(d, g, req, old['ticket']['profile'] if old else None)
                if old:
                    record = advance_record(old['work']['record'], req['stage'], evidence_root=owners['source_root'])
                else:
                    record = deepcopy(c['record'])
                    # Check required facts against exact sources on fresh admission too.
                    facts = {f['id']: f for f in record['facts']}
                    sources = {v['id']: v for v in record['sources']}
                    for required in record['stage']['required_facts']:
                        f = facts.get(required['fact_id'])
                        if f is None: fail('NEEDS_CLARIFICATION', 'Initial fact is absent')
                        original = source_fields(owners['source_root'], sources[f['source_id']]).get(f['source_field'])
                        if original is None or any(f[k] is None for k in required['fields']):
                            fail('NEEDS_CLARIFICATION', 'Initial required value is absent')
                        if any(f[k] is not None and f[k] != original[k] for k in ('value', 'unit')):
                            fail('CONSTRAINT_CONFLICT', 'Initial required fact contradicts exact source')
                ticket = ticket_for(s, m['store_id'], c['ticket_id'], selected['profile'], c['caller_id'])
                phase = 'RUNNING'
            else:
                ticket = old['ticket']; selected = old['work']['selection']; record = old['work']['record']
                if c['action'] in STATE_ACTIONS:
                    self._catalog_current(s, old['work']['request'], qualifications, source)
                    record = apply_delta(record, c, m, now_seconds()); phase = 'RUNNING'
                    check_delta_sources(record, c, root=owners['source_root'], archive=archive)
                elif c['action'] == 'FINISH':
                    record = finish_record(record, ticket['profile_ecid'], c['results'], c['receipts']); phase = 'SEALED'
                elif c['action'] == 'CANCEL':
                    record = finish_record(record, ticket['profile_ecid'], [], c['receipts'], cancel=True); phase = 'CANCELLED'
                else:
                    if not record['stage']['sealed']:
                        fail('CONSTRAINT_CONFLICT', 'Finish or explicitly cancel before closing task')
                    phase = 'COMPLETED'
            validate_receipts(record, ledger)
            if c['action'] in ('START','MOVE') + STATE_ACTIONS:
                check_state_sources(record, root=owners['source_root'], archive=archive, at=now_seconds())
            r = receipt(c, ticket, record, phase)
            b = {'command': c, 'ticket': ticket, 'record': record, 'selection': selected,
                 'inputs': owners, 'receipt': r}
            if c['action'] in STATE_ACTIONS:
                # Recheck rights immediately before journal write; no cross-store lease claimed.
                check_delta_sources(record, c, root=owners['source_root'], archive=archive)
                check_state_sources(record, root=owners['source_root'], archive=archive, at=now_seconds())
            self._write(db, meta, 'CATALOG_TASK', b)
            fault(fault_at, 'before_'+action+'_commit')
        fault(fault_at, 'after_'+action+'_commit')
        return {**deepcopy(r), 'historical': False}

    def read_task_stage(self, ticket, *, caller_id, expected_record_sha256,
                        qualifications, source, ledger, evidence_root, scope=None, archive=None):
        """Live selected artifacts + exact task state. No cache migration or permit."""
        digest_value(expected_record_sha256)
        with self.journal.transaction() as db:
            m, s, _ = self._read(db); role(m, caller_id, 'OPERATOR')
            old = source_task(s, ticket, caller_id, expected_record_sha256, scope); w = old['work']
            if w['phase'] != 'RUNNING':
                fail('CONSTRAINT_CONFLICT', 'Finished work may be inspected, not used as a live stage')
            exact(self._input_owners(ledger, evidence_root), w['inputs'])
            _, g, artifacts = self._catalog_current(s, w['request'], qualifications, source)
            validate_receipts(w['record'], ledger)
            check_state_sources(w['record'], root=evidence_root, archive=archive, at=now_seconds())
            published = release(s, s['published'][s['current']['generation_sha256']])
            exact(artifact_bundle(published['artifacts'], g), artifacts)
            p = next(p for p in g['profiles'] if p['id'] == ticket['profile'])
            return {'ticket': deepcopy(ticket), 'record': deepcopy(w['record']),
                'pairs': deepcopy(w['request']['pairs']),
                'task_state_identity': task_identity(ticket, w['record'], w['request']['pairs']),
                'artifacts': {k: deepcopy(artifacts[k]) for k in ['core'] + p['members']},
                'runtime_execution_permit': False, 'learned_routing': False,
                'residency_scope': 'SEALED_JSON_DOCUMENTS_NOT_VRAM_PAGING'}

    def audit(self):
        report = self.inspect()
        return {**report, 'status': 'SUCCESS', 'scope': 'STRUCTURE_NOT_NEURAL_PROOF_OR_LIVE_ELIGIBILITY'}
