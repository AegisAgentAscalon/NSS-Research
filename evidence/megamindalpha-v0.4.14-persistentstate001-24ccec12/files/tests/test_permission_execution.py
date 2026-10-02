from contextlib import closing
from copy import deepcopy
import sqlite3
from unittest.mock import patch
from permission_helpers import PermissionCase
from nss_base.neural_contracts import fingerprint
from nss_base.permission_executor import ReplayExecutor
from nss_base.permission_store import Permissions
from nss_base.neural_data import ProbeData


class PermissionExecutionTests(PermissionCase):
    def test_success_has_bound_receipt_and_one_old_effect(self):
        h=self.granted();r=self.execute_permission(h)
        self.assertEqual(r['status'],'COMMITTED');self.assertFalse(r['historical'])
        self.assertEqual(r['receipt'],self.executor.lookup(self.operation,h))
        self.assertEqual(self.ledger.effect_count(),1)
        self.assertEqual(self.executor.audit()['committed_results'],1)
        self.assertEqual(self.permits.inspect('permission-1')['status'],'COMMITTED')
    def test_retry_does_not_dispatch_or_recompute(self):
        h=self.granted();a=self.execute_permission(h)
        with patch.object(ReplayExecutor,'perform',side_effect=AssertionError('Repeated execution')):
            b=self.execute_permission(h)
        self.assertEqual(a['receipt'],b['receipt']);self.assertTrue(b['historical'])
    def test_committed_history_survives_expiry_and_revocation(self):
        h=self.granted();r=self.execute_permission(h);self.clock+=300;self.withdraw(h)
        self.q.revoke(self.revoke());ProbeData(self.root/'probe/data').revoke_for_test()
        x=self.execute_permission(h);self.assertEqual(r['receipt'],x['receipt']);self.assertTrue(x['historical'])
    def test_no_grant_no_result(self):
        self.error('INSUFFICIENT_EVIDENCE',self.execute_permission,'0'*64)
        self.assertEqual(self.executor.audit()['committed_results'],0)
    def test_wrong_source_state_burns_grant_without_execution(self):
        r=deepcopy(self.operation);r['source_state_sha256']='0'*64
        h=fingerprint(self.issue(r)['grant'])
        self.error('INCOMPATIBLE_CONFIGURATION',self.execute_permission,h,r)
        self.assertEqual(self.permits.inspect('permission-1')['status'],'UNCERTAIN')
        self.assertEqual(self.executor.audit()['committed_results'],0)
    def test_missing_mock_world_receipt_blocks_replay(self):
        h=self.granted()
        with closing(sqlite3.connect(self.ledger.world)) as db,db: db.execute('DELETE FROM records')
        self.error('RECOVERY_REQUIRED',self.execute_permission,h)
        self.assertEqual(self.executor.audit()['committed_results'],0)
        self.assertEqual(self.permits.inspect('permission-1')['status'],'UNCERTAIN')
    def test_request_with_missing_old_actions_cannot_dispatch(self):
        r=deepcopy(self.operation);r['action_receipts']=[];h=fingerprint(self.issue(r)['grant'])
        self.error('RECOVERY_REQUIRED',self.execute_permission,h,r)
        self.assertEqual(self.executor.audit()['committed_results'],0)
    def test_reconcile_without_consumption_forbidden(self):
        h=self.granted();self.error('CONSTRAINT_CONFLICT',self.reconcile,h)
    def test_consumed_without_result_requires_explicit_abandonment(self):
        h=self.granted();self.begin(h)
        self.error('RECOVERY_REQUIRED',self.execute_permission,h)
        r=self.reconcile(h);self.assertEqual(r['status'],'ABANDONED')
        self.error('RECOVERY_REQUIRED',self.execute_permission,h)
        self.assertTrue(self.reconcile(h)['historical'])
    def test_dispatched_without_result_abandoned_not_reissued(self):
        h=self.granted();self.begin(h);self.dispatch(h);self.clock+=300;self.withdraw(h)
        self.assertEqual(self.reconcile(h)['status'],'ABANDONED')
        self.assertEqual(self.issue()['status'],'ABANDONED')
    def test_reconcile_existing_result_no_new_execution(self):
        h=self.granted();self.begin(h);self.dispatch(h)
        receipt=self.executor.perform(self.operation,h,source=self.source,ledger=self.ledger)
        self.clock+=300;self.withdraw(h);self.q.revoke(self.revoke())
        with patch.object(ReplayExecutor,'perform',side_effect=AssertionError('Recomputed')):
            r=self.reconcile(h)
        self.assertEqual(r['receipt'],receipt);self.assertEqual(r['status'],'COMMITTED')
    def test_completion_needs_authoritative_receipt(self):
        h=self.granted();self.begin(h);self.dispatch(h)
        self.error('RECOVERY_REQUIRED',self.permits.finish,self.operation,grant_sha256=h,actor_id='local-runner',executor=self.executor)
    def test_executor_cannot_complete_undispatched_grant(self):
        h=self.granted();self.begin(h)
        self.executor.perform(self.operation,h,source=self.source,ledger=self.ledger)
        self.error('RECOVERY_REQUIRED',self.reconcile,h)
    def test_wrong_reconciliation_role(self):
        h=self.granted();self.begin(h);self.error('AUTHORIZATION_DENIED',self.reconcile,h,actor_id='local-runner')
    def test_caller_cannot_fabricate_executor_receipt(self):
        h=self.granted();self.begin(h)
        self.error('VALIDATION_FAILED',self.permits.finish,self.operation,grant_sha256=h,actor_id='local-runner',executor={'status':'COMMITTED'})
    def test_missing_executor_store_fails_without_recreating(self):
        h=self.granted();self.execute_permission(h);self.executor.path.unlink()
        self.error('RECOVERY_REQUIRED',self.execute_permission,h)
        self.assertFalse(self.executor.path.exists())
    def test_deleted_runtime_result_blocks_committed_retry(self):
        h=self.granted();self.execute_permission(h)
        with closing(sqlite3.connect(self.executor.path)) as db,db: db.execute('DELETE FROM results')
        self.error('VALIDATION_FAILED',self.execute_permission,h)
    def test_tampered_runtime_result_fails_closed(self):
        h=self.granted();self.execute_permission(h)
        with closing(sqlite3.connect(self.executor.path)) as db,db: db.execute("UPDATE results SET body='{}'")
        self.error('VALIDATION_FAILED',self.executor.audit)
    def test_reopened_owners_return_same_historical_receipt(self):
        h=self.granted();a=self.execute_permission(h)
        self.permits=Permissions(self.root/'permissions');self.executor=ReplayExecutor(self.root/'executor')
        b=self.execute_permission(h);self.assertEqual(a['receipt'],b['receipt'])
    def test_result_identity_collision_rejected(self):
        h=self.granted();self.execute_permission(h)
        r=deepcopy(self.operation);r['task_id']='other-task'
        self.error('CONSTRAINT_CONFLICT',self.executor.lookup,r,h)
    def test_qualification_history_unchanged_by_permission_execution(self):
        before=self.q.inspect('edge')
        h=self.granted();self.execute_permission(h)
        after=self.q.inspect('edge')
        self.assertEqual(before,after)
    def test_denial_does_not_disclose_raw_values(self):
        h=self.granted();self.clock+=101;self.error('AUTHORIZATION_DENIED',self.begin,h)
        d=self.permits.history()['events'][-1]['body']
        self.assertEqual(set(d),{'request_id','actor_id','operation','reason','observed_at'})
    def test_unknown_execute_fault_fails_before_consumption(self):
        h=self.granted();self.error('VALIDATION_FAILED',self.execute_permission,h,fault_at='unknown')
        self.assertEqual(self.permits.inspect('permission-1')['status'],'GRANTED')
    def test_separately_qualified_return_to_core_is_permitted(self):
        from nss_base.qualificationevidence002 import AT,review_for
        from nss_base.permission_replay import prepare_request
        r=self.source.propose(run_id='probe-001',seed=101,precision='fp32',scope={'kind':'TRANSITION','source':'A','destination':'CORE','mode':'replay'},producer_id='fixture-builder',request_id='return-core',at=AT,prerequisites=['core','a'])
        self.q.prepare(r,source=self.source);self.assertEqual(self.q.decide(review_for(r),source=self.source)['verdict'],'QUALIFIED')
        req=prepare_request(qualifications=self.q,source=self.source,qualification_id='return-core',request_id='return-operation',caller_id='local-runner',task_id='neural-probe-replay',ledger=self.ledger)
        h=fingerprint(self.issue(req)['grant']);result=self.execute_permission(h,req)
        self.assertEqual(result['status'],'COMMITTED');self.assertEqual(self.ledger.effect_count(),1)
