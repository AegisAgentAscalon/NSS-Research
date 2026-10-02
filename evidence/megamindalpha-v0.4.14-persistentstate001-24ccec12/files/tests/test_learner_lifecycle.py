from copy import deepcopy
from unittest.mock import patch
from learner_helpers import LearnerCase, CLOCK
from nss_base.learner_contracts import numerical_input, operation_id
from nss_base.learner_coordinator import unwrap
from nss_base.learner_recipe import verify_candidate
from nss_base.neural_contracts import fingerprint
from nss_base.runtime import ContractError


class LearningLifecycleTests(LearnerCase):
    def test_unapproved_work_does_not_create_candidate(self):
        self.co.prepare(self.plan)
        self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.co.training.audit()['attempts'],0)

    def test_self_and_unknown_approver_rejected(self):
        self.co.prepare(self.plan)
        for actor in ['learner-worker','unknown']:
            with self.subTest(actor=actor):
                self.error('AUTHORIZATION_DENIED',self.co.cycles.approve,'learn-001',approver_id=actor,expires_at=CLOCK+100,at=CLOCK)

    def test_expired_approval_denies_no_work(self):
        self.ready();self.co.clock=lambda:CLOCK+600
        self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.co.training.audit()['attempts'],0)

    def test_changed_approval_cannot_renew_cycle(self):
        self.ready()
        self.error('AUTHORIZATION_DENIED',self.co.cycles.approve,'learn-001',approver_id='human-operator',expires_at=CLOCK+800,at=CLOCK)

    def test_clock_rollback_denied(self):
        self.ready();self.co.clock=lambda:CLOCK-1
        self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='learner-worker')

    def test_budget_denied_before_snapshot_dispatch(self):
        self.plan['budget']['optimizer_updates']=1;self.ready()
        self.error('BUDGET_EXHAUSTED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.co.cycles.inspect('learn-001')['started'],[])

    def test_evaluation_budget_denied_before_training(self):
        self.plan['budget']['evaluation_passes']=1;self.ready()
        self.error('BUDGET_EXHAUSTED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.co.training.audit()['attempts'],0)

    def test_wrong_caller_cannot_dispatch(self):
        self.ready();self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='human-operator')

    def test_revocation_before_training_blocks_later_steps(self):
        self.ready();self.data.revoke_for_test()
        self.error('TRAINING_RESTRICTED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.co.training.audit()['attempts'],0)

    def test_withdrawn_operator_approval_does_not_return_on_retry(self):
        self.ready();self.co.cycles.withdraw('learn-001',actor_id='human-operator',reason='withdraw',at=CLOCK)
        self.co.cycles.approve('learn-001',approver_id='human-operator',expires_at=CLOCK+600,at=CLOCK)
        self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='learner-worker')

    def test_cancel_before_dispatch_is_terminal_history(self):
        self.ready();self.co.cycles.cancel('learn-001',actor_id='learner-worker',reason='stop',at=CLOCK)
        r=self.co.advance('learn-001',caller_id='learner-worker')
        self.assertEqual(r['status'],'CANCELLED');self.assertEqual(self.co.training.audit()['attempts'],0)

    def test_unknown_cancel_actor_rejected(self):
        self.ready();self.error('AUTHORIZATION_DENIED',self.co.cycles.cancel,'learn-001',actor_id='unknown',reason='stop',at=CLOCK)

    def test_real_frozen_core_training_then_proposal(self):
        r=self.complete();t=self.candidate();e=self.evaluation()
        self.assertEqual(e['report']['verdict'],'PASS');self.assertEqual(r['status'],'PROPOSED')
        self.assertTrue(all(t['report']['invariants'].values()))
        for k in ('core','A','B'):self.assertEqual(t['report']['checkpoint_hashes'][k],self.plan['parent']['checkpoint_hashes'][k])
        self.assertFalse(r['proposal']['deployment_authorized']);self.assertEqual(r['proposal']['qualification_status'],'INSUFFICIENT_EVIDENCE')

    def test_insufficient_training_records_fail_without_fake_success(self):
        self.plan['recipe']['steps']=1;self.plan['budget']['optimizer_updates']=1
        r=self.complete();self.assertEqual(r['proposal']['numerical_verdict'],'FAIL')
        self.assertEqual(r['proposal']['recommendation'],'NOT_RECOMMENDED')

    def test_terminal_retry_never_trains_or_evaluates(self):
        r=self.complete();self.data.revoke_for_test()
        with (patch('nss_base.learner_recipe.train_candidate',side_effect=AssertionError('must not train')),
              patch('nss_base.learner_recipe.evaluate_candidate',side_effect=AssertionError('must not score'))):
            self.assertEqual(self.co.advance('learn-001',caller_id='learner-worker'),r)
        self.assertEqual(self.co.training.audit()['attempts'],1)

    def test_current_proposal_rechecks_source_permissions(self):
        self.complete();self.assertEqual(self.co.check_proposal('learn-001')['status'],'INSUFFICIENT_EVIDENCE')
        self.data.revoke_for_test();self.error('TRAINING_RESTRICTED',self.co.check_proposal,'learn-001')

    def test_current_proposal_blocks_withdrawn_plan(self):
        r=self.complete();self.co.cycles.withdraw('learn-001',actor_id='human-operator',reason='withdraw',at=CLOCK)
        self.error('AUTHORIZATION_DENIED',self.co.check_proposal,'learn-001')
        self.assertEqual(self.co.cycles.inspect('learn-001')['proposal'],r['proposal'])

    def test_cancel_during_optimizer_preserves_unfinished_attempt(self):
        self.ready();old=self.co._gate;calls=0
        def gate(*args,**kw):
            nonlocal calls
            calls+=1
            if calls==8:self.co.cycles.cancel('learn-001',actor_id='human-operator',reason='during training',at=CLOCK)
            return old(*args,**kw)
        with patch.object(self.co,'_gate',side_effect=gate):
            self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.co.cycles.inspect('learn-001')['status'],'CANCELLED')
        self.assertEqual(self.co.training.audit()['attempts'],1)
        self.assertEqual(self.candidate()['status'],'PREPARED')

    def test_evaluator_rejects_tiny_metric_tampering(self):
        self.complete();e=deepcopy(self.evaluation());t=self.candidate()
        for row in e['report']['repeats']:row['A2']['mse']+=1e-12
        self.error('VALIDATION_FAILED',verify_candidate,e,t,gate=lambda:None)

    def test_accepted_parent_qualification_revocation_stops_training(self):
        self.ready();self.q.revoke(self.revoke('core'))
        self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='learner-worker')

    def test_selected_revision_change_blocks_stale_plan(self):
        self.ready();v=unwrap(self.co.archive.inspect('neural-train'))
        # Explicit HUMAN reviewer already present in these synthetic records.
        from nss_base.neural_data import ACTOR,AT
        unwrap(self.co.archive.change({'schema_version':1,'operation_id':'later-review','experience_id':'neural-train',
            'expected_revision_hash':v['reference']['sha256'],'actor':ACTOR,'at':AT,'reason':'new review revision',
            'action':'REVIEW','payload':{'decision':'APPROVED'}}))
        self.error('CONSTRAINT_CONFLICT',self.co.advance,'learn-001',caller_id='learner-worker')

    def test_unknown_proposal_and_incomplete_proposal_are_not_evidence(self):
        self.ready();self.error('INSUFFICIENT_EVIDENCE',self.co.check_proposal,'learn-001')
        self.error('INSUFFICIENT_EVIDENCE',self.co.check_proposal,'missing')
