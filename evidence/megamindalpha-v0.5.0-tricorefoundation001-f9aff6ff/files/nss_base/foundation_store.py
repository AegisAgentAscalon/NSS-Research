"""Current-role methods of the existing Generations owner, not a parallel task DB."""
from copy import deepcopy
import time
from .foundation_contracts import FORMAT, POLICY_SHA256, task_view, configuration
from .foundation_events import idle, command_binding
from .foundation_lock import worker_lock
from .neural_contracts import fingerprint, fields
from .generation_contracts import exact, role
from .state_contracts import command, attest, POLICY
from .state_updates import apply_delta
from .state_sources import check_delta_sources, check_state_sources
from .task_records import validate_task_record, source_document
from .runtime import fail


def current_time():
    from .local_journal import epoch
    return epoch(int(time.time()))


def foundation(m):
    if m.get('format') != FORMAT:
        fail('INCOMPATIBLE_CONFIGURATION', 'Open an explicitly created current-role store; legacy migration is not automatic')


def prepare_state(view, *, operation_id, proposer_id, proposer_version, deltas):
    return command({'schema_version': 3, 'store_id': view['store_id'],
        'task_id': view['record']['task_id'], 'operation_id': operation_id, 'caller_id': view['caller_id'],
        'action': 'UPDATE_STATE', 'scope': deepcopy(view['owner_scope']),
        'expected_revision': view['record']['revision'], 'expected_record_sha256': fingerprint(view['record']),
        'expected_configuration_sha256': view['configuration_sha256'],
        'proposer': {'id': proposer_id, 'version': proposer_version}, 'review': None, 'deltas': deepcopy(deltas)})


def prepare_admission(store_info, record, *, caller_id, owner_scope, operation_id,
                      proposer_id, proposer_version, archive_binding=None, max_record_bytes=65536):
    validate_task_record(record)
    return command({'schema_version': 3, 'store_id': store_info['store_id'], 'task_id': record['task_id'],
        'operation_id': operation_id, 'caller_id': caller_id, 'action': 'BIND_STATE',
        'scope': deepcopy(owner_scope), 'expected_revision': record['revision'],
        'expected_record_sha256': fingerprint(record),
        'expected_configuration_sha256': store_info['current']['generation_sha256'],
        'proposer': {'id': proposer_id, 'version': proposer_version}, 'review': None,
        'policy': {'policy_id': POLICY, 'instruction_policy_sha256': POLICY_SHA256, 'max_record_bytes': max_record_bytes},
        'archive_binding': deepcopy(archive_binding)})


class FoundationOperations:
    def foundation_snapshot(self):
        """Trusted-local operator inspection, not an API exposed to a model."""
        with self.journal.transaction() as db:
            m, s, meta = self._read(db); foundation(m)
            return {'store_id': m['store_id'], 'current': deepcopy(s['current']),
                    'configuration': deepcopy(s['configurations'][s['current']['generation_sha256']]),
                    'busy': deepcopy(s['busy']), 'events': meta['count'],
                    'task_ids': sorted(s['tasks']), 'scope': 'TEST_ADAPTERS_ONLY',
                    'runtime_execution_permit': False, 'training_authorized': False}

    def foundation_read(self, task_id, *, caller_id, owner_scope, evidence_root, archive=None,
                        expected_record_sha256=None, historical=False):
        with self.journal.transaction() as db:
            m, s, _ = self._read(db); foundation(m)
            t = task_view(s, m, task_id, caller_id, owner_scope, live=not historical)
            if expected_record_sha256 is not None and fingerprint(t['record']) != expected_record_sha256:
                fail('CONSTRAINT_CONFLICT', 'Stale symbolic record')
            if not historical:
                check_state_sources(t['record'], root=evidence_root, archive=archive, at=current_time())
            identity = fingerprint({'store_id': m['store_id'], 'task_id': task_id,
                'scope': t['scope'], 'configuration_sha256': t['configuration_sha256'],
                'record_sha256': fingerprint(t['record']), 'ticks': t['ticks'], 'closed': t['closed']})
            cfg = s['configurations'][t['configuration_sha256']]
            return {**deepcopy(t), 'store_id': m['store_id'], 'owner_scope': deepcopy(t['scope']),
                'task_state_identity': identity,
                'context_configuration': {'generation_sha256': t['configuration_sha256'],
                    'primary_generation': cfg['primary_generation'], 'context_abi': cfg['context_abi'],
                    'component_revisions': {r: c['revision'] if c else None for r,c in cfg['components'].items()}},
                'historical': historical, 'runtime_execution_permit': False, 'training_authorized': False}

    def foundation_admit(self, record, value, *, evidence_root, archive=None, fault_at=None):
        c = command(value); validate_task_record(record)
        # Existing immutable source reader; never promote generated content to observed sources.
        originals = {src['id']: source_document(evidence_root, src)['fields'] for src in record['sources']}
        if not any(f['value'] == record['original_request']['text'] for f in originals[record['original_request']['source_id']].values()):
            fail('CONSTRAINT_CONFLICT', 'Initial request must match an admitted exact field')
        for f in record['facts']:
            original = originals[f['source_id']].get(f['source_field'])
            if original is None or any(f[k] is not None and f[k] != original[k] for k in ('value','unit')):
                fail('CONSTRAINT_CONFLICT', 'Initial fact differs from exact admitted evidence')
        with self.journal.transaction() as db:
            m,s,meta = self._read(db); foundation(m); command_binding(c,m,s); idle(s)
            updated = apply_delta(record,c,m,current_time(),configuration_sha256=s['current']['generation_sha256'])
            check_state_sources(updated, root=evidence_root, archive=archive, at=current_time())
            self._write(db,meta,'F_ADMIT',{'record':deepcopy(record),'command':c},fault_at)
        return self.foundation_read(c['task_id'], caller_id=c['caller_id'], owner_scope=c['scope'], evidence_root=evidence_root, archive=archive)

    def foundation_update(self, value, *, evidence_root, archive=None, fault_at=None):
        c=command(value)
        with self.journal.transaction() as db:
            m,s,meta=self._read(db); foundation(m); command_binding(c,m,s)
            # Scope is checked before an idempotent history response; never disclose another task.
            t=task_view(s,m,c['task_id'],c['caller_id'],c['scope'],live=False)
            if c['operation_id'] in s['state_operations']:
                saved=s['state_operations'][c['operation_id']]; exact(c,saved['command'])
                return {'historical':True,'record_sha256':saved['record_sha256'],'state_changed':False}
            task_view(s,m,c['task_id'],c['caller_id'],c['scope']); idle(s)
            check_delta_sources(t['record'],c,root=evidence_root,archive=archive)
            updated=apply_delta(t['record'],c,m,current_time(),configuration_sha256=t['configuration_sha256'])
            check_state_sources(updated,root=evidence_root,archive=archive,at=current_time())
            self._write(db,meta,'F_UPDATE',{'command':c},fault_at)
            return {'historical':False,'record_sha256':fingerprint(updated),'state_changed':True}

    def _foundation_event(self, kind, body, *, fault_at=None):
        """Installed runner only. This is not a model-callable general event interface."""
        with self.journal.transaction() as db:
            m,_,meta=self._read(db); foundation(m)
            self._write(db,meta,kind,deepcopy(body),fault_at)

    def foundation_operation(self, operation_id, *, caller_id, owner_scope):
        with self.journal.transaction() as db:
            m,s,_=self._read(db); foundation(m)
            if operation_id not in s['operations']: fail('INSUFFICIENT_EVIDENCE','No completed/interrupted operation')
            op=s['operations'][operation_id]
            task_view(s,m,op['task_id'],caller_id,owner_scope,live=False)
            return deepcopy(op)

    def foundation_recover(self, *, caller_id, reason):
        # A live thread/process retains this OS lock. Do not release a reservation
        # based merely on a timeout/PID while its auxiliary can still execute.
        with worker_lock(self.journal.path.parent):
            snap=self.foundation_snapshot()
            if snap['busy'] is None: return {'status':'IDLE','computation_claimed':False}
            job=snap['busy']
            self._foundation_event('F_INTERRUPT',{'operation_id':job['operation_id'],'caller_id':caller_id,'reason':reason})
            return {'status':'INTERRUPTED','operation_id':job['operation_id'],
                    'restored':'LAST_COMMITTED_STATE','external_effects_replayed':False}

    def foundation_close(self,task_id,*,caller_id,owner_scope):
        self._foundation_event('F_CLOSE',{'task_id':task_id,'caller_id':caller_id,'scope':deepcopy(owner_scope)})

    def foundation_switch_test_configuration(self, config, *, expected_current, caller_id,
                                             reviewer_id, issuer_id, test_evidence_sha256):
        self._foundation_event('F_SWITCH_TEST_CONFIGURATION', {'configuration':configuration(config),
            'expected_current':deepcopy(expected_current),'caller_id':caller_id,'reviewer_id':reviewer_id,
            'issuer_id':issuer_id,'test_evidence_sha256':test_evidence_sha256,
            'qualification_scope':'STRUCTURAL_TEST_ATTESTATION_NOT_MODEL_QUALIFICATION'})
        return self.foundation_snapshot()
