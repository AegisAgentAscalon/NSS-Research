from contextlib import closing
from copy import deepcopy
import sqlite3
from unittest.mock import patch
from permission_helpers import PermissionCase
from nss_base.neural_contracts import encoded,fingerprint
from nss_base.permission_store import Permissions
from nss_base.permission_executor import ReplayExecutor
from nss_base.neural_data import ProbeData


class PermissionStoreTests(PermissionCase):
    def test_qualification_alone_does_not_issue_grant(self):
        self.assertEqual(self.permits.audit()['grants'],0)
        self.error('INSUFFICIENT_EVIDENCE',self.begin,'0'*64)
    def test_issue_exact_grant_has_no_deployment_authority(self):
        s=self.issue();g=s['grant'];self.assertEqual(g['max_uses'],1)
        self.assertFalse(g['deployment_authorized']);self.assertFalse(g['runtime_execution_permit']);self.assertFalse(g['delegable'])
    def test_self_issue_denied(self):
        self.error('AUTHORIZATION_DENIED',self.issue,issuer_id='local-runner')
        self.assertEqual(self.permits.audit()['denials'],1)
    def test_unknown_issuer_denied(self): self.error('AUTHORIZATION_DENIED',self.issue,issuer_id='unknown')
    def test_unknown_caller_denied(self):
        r=deepcopy(self.operation);r['caller_id']='unknown';self.error('AUTHORIZATION_DENIED',self.issue,r)
    def test_expired_retry_does_not_renew_grant(self):
        s=self.issue();self.clock+=200;t=self.issue()
        self.assertEqual(s['grant'],t['grant']);self.assertTrue(t['historical'])
        self.error('AUTHORIZATION_DENIED',self.begin,fingerprint(s['grant']))
    def test_issue_same_id_other_ttl_conflicts(self):
        self.issue();self.error('CONSTRAINT_CONFLICT',self.issue,ttl_seconds=50)
    def test_issue_same_id_other_request_conflicts(self):
        self.issue();r=deepcopy(self.operation);r['task_id']='other';self.error('CONSTRAINT_CONFLICT',self.issue,r)
    def test_wrong_request_fields_cannot_reuse_grant(self):
        h=self.granted()
        for k,v in [('task_id','another'),('caller_id','other-runner'),('source_state_sha256','1'*64),('certificate_sha256','2'*64)]:
            with self.subTest(field=k):
                r=deepcopy(self.operation);r[k]=v;self.error('INCOMPATIBLE_CONFIGURATION',self.begin,h,r)
        self.assertEqual(self.permits.inspect('permission-1')['status'],'GRANTED')
    def test_wrong_grant_hash_denied(self):
        self.granted();self.error('INCOMPATIBLE_CONFIGURATION',self.begin,'0'*64)
    def test_wrong_actor_cannot_consume(self):
        h=self.granted();self.error('AUTHORIZATION_DENIED',self.begin,h,caller_id='other-runner')
    def test_expiry_at_boundary_denied(self):
        h=self.granted();self.clock+=100;self.error('AUTHORIZATION_DENIED',self.begin,h)
    def test_just_before_expiry_allowed(self):
        h=self.granted();self.clock+=99;self.assertEqual(self.begin(h)['status'],'STARTED')
    def test_clock_rollback_denied(self):
        h=self.granted();self.clock-=1;self.error('AUTHORIZATION_DENIED',self.begin,h)
    def test_consumption_is_single_use(self):
        h=self.granted();self.begin(h);self.error('RECOVERY_REQUIRED',self.begin,h)
    def test_second_owner_cannot_consume_same_grant(self):
        h=self.granted();self.begin(h);self.permits=Permissions(self.root/'permissions')
        self.error('RECOVERY_REQUIRED',self.begin,h)
    def test_dispatch_requires_consumption(self):
        h=self.granted();self.error('RECOVERY_REQUIRED',self.dispatch,h)
    def test_dispatch_cannot_repeat(self):
        h=self.granted();self.begin(h);self.dispatch(h);self.error('RECOVERY_REQUIRED',self.dispatch,h)
    def test_expiry_between_consume_and_dispatch(self):
        h=self.granted();self.begin(h);self.clock+=100;self.error('AUTHORIZATION_DENIED',self.dispatch,h)
    def test_grant_revocation_before_use(self):
        h=self.granted();self.withdraw(h);self.error('AUTHORIZATION_DENIED',self.begin,h)
    def test_grant_revocation_after_consumption(self):
        h=self.granted();self.begin(h);self.withdraw(h);self.error('AUTHORIZATION_DENIED',self.dispatch,h)
    def test_revocation_idempotent_and_not_reversible(self):
        h=self.granted();self.withdraw(h);self.assertTrue(self.withdraw(h)['historical'])
        self.error('CONSTRAINT_CONFLICT',self.withdraw,h,reason='different content')
        self.assertTrue(self.issue()['revoked'])
    def test_wrong_revoker(self):
        h=self.granted();self.error('AUTHORIZATION_DENIED',self.withdraw,h,actor_id='local-runner')
    def test_revoked_qualification_blocks_issue(self):
        self.q.revoke(self.revoke());self.error('AUTHORIZATION_DENIED',self.issue)
    def test_revoked_prerequisite_blocks_consumption(self):
        h=self.granted();self.q.revoke(self.revoke());self.error('AUTHORIZATION_DENIED',self.begin,h)
    def test_revoked_prerequisite_blocks_dispatch(self):
        h=self.granted();self.begin(h);self.q.revoke(self.revoke());self.error('AUTHORIZATION_DENIED',self.dispatch,h)
    def test_source_withdrawal_blocks_issue(self):
        ProbeData(self.root/'probe/data').revoke_for_test();self.error('TRAINING_RESTRICTED',self.issue)
    def test_source_withdrawal_blocks_consumption(self):
        h=self.granted();ProbeData(self.root/'probe/data').revoke_for_test();self.error('TRAINING_RESTRICTED',self.begin,h)
    def test_source_withdrawal_blocks_dispatch(self):
        h=self.granted();self.begin(h);ProbeData(self.root/'probe/data').revoke_for_test();self.error('TRAINING_RESTRICTED',self.dispatch,h)
    def test_source_binding_changed_rejected(self):
        r=deepcopy(self.operation);r['binding']['trial_seed']=211;self.error('INCOMPATIBLE_CONFIGURATION',self.issue,r)
    def test_policy_and_role_mutation_detected(self):
        self.issue()
        with closing(sqlite3.connect(self.permits.journal.path)) as db,db:
            db.execute("UPDATE meta SET manifest_hash=?",('0'*64,))
        self.error('VALIDATION_FAILED',self.permits.audit)
    def test_deleted_event_detected(self):
        h=self.granted();self.withdraw(h)
        with closing(sqlite3.connect(self.permits.journal.path)) as db,db: db.execute('DELETE FROM events WHERE seq=2')
        self.error('VALIDATION_FAILED',self.permits.audit)
    def test_missing_head_detected(self):
        self.issue()
        with closing(sqlite3.connect(self.permits.journal.path)) as db,db: db.execute('DELETE FROM meta')
        self.error('VALIDATION_FAILED',self.permits.audit)
    def test_mutated_event_detected(self):
        self.issue()
        with closing(sqlite3.connect(self.permits.journal.path)) as db,db: db.execute("UPDATE events SET body='{}'")
        self.error('VALIDATION_FAILED',self.permits.audit)
    def test_unknown_fault_points_do_not_issue(self):
        self.error('VALIDATION_FAILED',self.issue,fault_at='random')
        self.assertEqual(self.permits.audit()['grants'],0)
    def test_self_issue_denied_even_when_actor_has_both_roles(self):
        from nss_base.localnexuspermissions002 import OPERATORS
        m=deepcopy(OPERATORS)
        for o in m:
            if o['id']=='local-owner':o['roles'].append('EXECUTOR')
        self.permits=Permissions.create(self.root/'multi-role',m)
        r=deepcopy(self.operation);r['caller_id']='local-owner'
        self.error('AUTHORIZATION_DENIED',self.issue,r)
    def test_completion_receipt_never_upgrades_host_to_runtime_permit(self):
        h=self.granted();self.execute_permission(h)
        s=self.permits.inspect('permission-1')
        self.assertFalse(s['runtime_execution_permit']);self.assertFalse(s['grant']['runtime_execution_permit'])
        self.assertFalse(s['grant']['deployment_authorized'])
