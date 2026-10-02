from copy import deepcopy
from unittest.mock import patch
from candidate_acceptance_helpers import CandidateCase
from nss_base.generation_store import Generations
from nss_base.neural_contracts import fingerprint,pairs
from nss_base.neural_data import ProbeData
from nss_base.runtime import ContractError


class CandidateReleaseTests(CandidateCase):
    def test_evaluation_and_qualification_do_not_publish(self):
        self.assertEqual(self.manager.inspect()['current'],self.parent)
        self.assertFalse(self.co.cycles.inspect(self.plan['cycle_id'])['proposal']['deployment_authorized'])
        self.assertEqual(self.manager.inspect()['generations'][self.target],'QUALIFIED')

    def test_source_stays_current_until_atomic_publication(self):
        opts=self.issue()
        for fn in (self.manager.prepare,self.manager.stage):
            fn('candidate-release',**opts);self.assertEqual(self.manager.inspect()['current'],self.parent)
        out=self.manager.publish('candidate-release',**opts)
        self.assertEqual(out['receipt']['current']['epoch'],self.parent['epoch']+1)
        self.assertEqual(self.manager.inspect()['generations'][self.parent['generation_sha256']],'ARCHIVED')
        self.assert_no_training_or_effect()

    def test_publish_without_fresh_release_grant_fails(self):
        self.error('INSUFFICIENT_EVIDENCE',self.manager.publish,'missing',grant_sha256='0'*64,
            caller_id='local-runner',**self.ev)
        self.assertEqual(self.manager.inspect()['current'],self.parent)

    def test_wrong_issuer_or_caller_cannot_release(self):
        self.error('AUTHORIZATION_DENIED',self.manager.issue,self.request(),issuer_id='learner-worker',ttl_seconds=300,**self.ev)
        opts=self.issue();opts['caller_id']='fixture-builder'
        self.error('AUTHORIZATION_DENIED',self.manager.prepare,'candidate-release',**opts)

    def test_learner_approval_is_not_a_release_grant(self):
        approval=self.co.cycles.inspect(self.plan['cycle_id'])['approval']
        self.error('VALIDATION_FAILED',self.manager.issue,approval,issuer_id='release-owner',ttl_seconds=300,**self.ev)

    def test_old_replay_permission_cannot_expand_to_candidate(self):
        from nss_base.permission_contracts import request as check
        # Pure claim/binding forms cannot be re-used as a different operation type.
        with self.assertRaises(ContractError):check(self.reqs[3])

    def test_open_parent_stage_blocks_candidate_adoption(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts);self.manager.stage('candidate-release',**opts)
        t=self.manager.pin_stage('busy',profile='CORE',caller_id='local-runner',**self.parent_ev)
        self.error('RECOVERY_REQUIRED',self.manager.publish,'candidate-release',**opts)
        self.assertEqual(self.manager.inspect()['current'],self.parent)
        self.manager.close_stage(t,caller_id='local-runner');self.manager.publish('candidate-release',**opts)
        self.error('INCOMPATIBLE_CONFIGURATION',self.manager.read_stage,t,caller_id='local-runner',**self.ev)

    def test_expiry_between_staging_and_publication_fails(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts);self.manager.stage('candidate-release',**opts)
        self.clock+=300;self.error('AUTHORIZATION_DENIED',self.manager.publish,'candidate-release',**opts)
        self.assertEqual(self.manager.inspect()['current'],self.parent)

    def test_revocation_between_staging_and_publication_fails(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts);self.manager.stage('candidate-release',**opts)
        self.withdraw('candidate-core')
        self.error('AUTHORIZATION_DENIED',self.manager.publish,'candidate-release',**opts)
        self.assertEqual(self.manager.inspect()['current'],self.parent)

    def test_data_withdrawal_between_stage_and_publish_fails(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts);self.manager.stage('candidate-release',**opts)
        ProbeData(self.root/'learning-data').revoke_for_test()
        self.error('TRAINING_RESTRICTED',self.manager.publish,'candidate-release',**opts)
        self.assertEqual(self.manager.inspect()['current'],self.parent)

    def test_candidate_proposal_withdrawal_blocks_publication(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts)
        self.co.cycles.withdraw(self.plan['cycle_id'],actor_id='human-operator',reason='Stop release',at=self.clock)
        self.error('AUTHORIZATION_DENIED',self.manager.stage,'candidate-release',**opts)

    def test_release_withdrawal_blocks_resume(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts)
        self.manager.revoke('candidate-release',kind='RELEASE',actor_id='release-owner',reason='Stop')
        self.error('AUTHORIZATION_DENIED',self.manager.stage,'candidate-release',**opts)

    def test_whole_candidate_generation_core_only_rule_retained(self):
        from nss_base.generation_contracts import generation
        g=deepcopy(self.family);g['profiles']=[p for p in g['profiles'] if p['id']!='CORE']
        self.error('INCOMPATIBLE_CONFIGURATION',generation,g)
        g=deepcopy(self.family);g['transitions']=[]
        self.error('INCOMPATIBLE_CONFIGURATION',generation,g)

    def test_candidate_ecid_and_hashes_are_not_parent_aliases(self):
        b=self.family['binding'];parent=self.plan['parent']
        self.assertNotEqual(b['profile_ecids']['A2'],parent['profile_ecids']['A'])
        self.assertNotEqual(b['checkpoint_hashes']['A2'],parent['checkpoint_hashes']['A'])
        self.assertEqual(b['checkpoint_hashes']['core'],parent['checkpoint_hashes']['core'])

    def test_staged_candidate_runs_and_is_source_hash_bound(self):
        self.adopt();ticket=self.manager.pin_stage('candidate-forward',profile='A2B',caller_id='local-runner',**self.ev)
        v=self.manager.read_stage(ticket,caller_id='local-runner',**self.ev)
        self.assertEqual(set(v['artifacts']),{'core','A2','B'})
        self.assertEqual(fingerprint(v['artifacts']['A2']),self.family['binding']['checkpoint_hashes']['A2'])
        from nss_base.neural_backend import deterministic_cpu,load_checkpoint,encode_pairs
        import torch
        with deterministic_cpu(31),torch.no_grad():
            ms={k:load_checkpoint(a,fingerprint(a)) for k,a in v['artifacts'].items()}
            actual=ms['core'](encode_pairs(pairs('test')[:4]),a=ms['A2'],b=ms['B'])
            session=self.source.view(self.plan['cycle_id'],31,'fp32')[3]
            self.assertTrue(torch.equal(actual,session.predict('A2B',pairs('test')[:4])))

    def test_rollback_requires_fresh_approval_and_preserves_old_core(self):
        opts=self.adopt();req=self.request('rollback',self.parent['generation_sha256'],'ROLLBACK')
        issued=self.manager.issue(req,issuer_id='release-owner',ttl_seconds=300,**self.parent_ev)
        back={'caller_id':'local-runner','grant_sha256':fingerprint(issued['grant']),**self.parent_ev}
        for fn in (self.manager.prepare,self.manager.stage,self.manager.publish):fn('rollback',**back)
        at=self.manager.inspect()['current'];self.assertEqual(at['generation_sha256'],self.parent['generation_sha256'])
        receipt=self.manager.publish('candidate-release',**opts)
        self.assertTrue(receipt['historical']);self.assertEqual(self.manager.inspect()['current'],at)
        self.assert_no_training_or_effect()

    def test_historical_acceptance_does_not_renew_data_permission(self):
        opts=self.adopt();ProbeData(self.root/'learning-data').revoke_for_test()
        self.assertTrue(self.manager.publish('candidate-release',**opts)['historical'])
        self.error('TRAINING_RESTRICTED',self.manager.pin_stage,'after-withdrawal',profile='CORE',caller_id='local-runner',**self.ev)

    def test_changed_source_epoch_rejects_other_old_grant(self):
        old=self.issue('stale');self.adopt('accepted')
        self.error('CONSTRAINT_CONFLICT',self.manager.prepare,'stale',**old)

    def test_wrong_source_format_fails_current_stage_use(self):
        self.adopt();t=self.manager.pin_stage('source-test',profile='CORE',caller_id='local-runner',**self.ev)
        with self.assertRaises(ContractError):self.manager.read_stage(t,caller_id='local-runner',**self.parent_ev)

    def test_learner_plan_and_candidate_weights_unchanged_by_acceptance(self):
        old=self.co.cycles.inspect(self.plan['cycle_id']);candidate=self.co.training.audit()
        self.adopt();self.assertEqual(self.co.cycles.inspect(self.plan['cycle_id']),old)
        self.assertEqual(self.co.training.audit(),candidate)
