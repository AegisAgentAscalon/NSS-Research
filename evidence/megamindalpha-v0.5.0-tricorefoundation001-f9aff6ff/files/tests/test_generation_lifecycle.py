"""Observable lifecycle, permissions and managed-stage invariants."""
from copy import deepcopy
from generation_helpers import GenerationCase
from nss_base.generation_store import Generations
from nss_base.neural_contracts import fingerprint
from nss_base.neural_data import ProbeData
from nss_base.ledger import Ledger
from nss_base.runtime import ContractError


class GenerationLifecycleTests(GenerationCase):
    def test_atomic_adoption_archive_rollback_and_stale_history(self):
        first, one = self.adopted(); before=self.manager.inspect()['current']
        key, opts=self.issued(1,'second','UPDATE');self.manager.prepare(key,**opts);self.manager.stage(key,**opts)
        self.assertEqual(self.manager.inspect()['current'],before)
        result=self.manager.publish(key,**opts);self.assertEqual(result['status'],'PUBLISHED')
        self.assertEqual(self.manager.inspect()['generations'][self.hashes[0]],'ARCHIVED')
        self.assertEqual(result['receipt']['previous'],before)
        self.adopted(0,'back','ROLLBACK');current=self.manager.inspect()['current']
        self.assertEqual(current,{'epoch':3,'generation_sha256':self.hashes[0]})
        self.assertTrue(self.manager.publish(key,**opts)['historical'])
        self.assertEqual(self.manager.inspect()['current'],current)
        self.assertTrue(self.manager.publish(first,**one)['historical'])
        self.assertEqual(Ledger(self.root/'probe/mock_actions').effect_count(),1)

    def test_target_and_archive_content_immutable(self):
        self.adopted();self.adopted(1,'second','UPDATE')
        for i in (0,1):self.assertEqual(self.manager.inspect_generation(self.hashes[i])['manifest'],self.gs[i])

    def test_prepared_grant_resumes_only_safe_local_operations(self):
        key,opts=self.issued();self.manager.prepare(key,**opts)
        self.assertTrue(self.manager.prepare(key,**opts)['historical'])
        self.manager.stage(key,**opts);self.assertTrue(self.manager.stage(key,**opts)['historical'])
        self.assertEqual(self.manager.publish(key,**opts)['status'],'PUBLISHED')

    def test_cannot_skip_required_lifecycle_states(self):
        key,opts=self.issued()
        for f in (self.manager.stage,self.manager.publish):
            with self.subTest(method=f.__name__):self.error('CONSTRAINT_CONFLICT',f,key,**opts)
        self.assertEqual(self.manager.inspect()['current']['epoch'],0)

    def test_wrong_caller_and_hash_fail_before_mutation(self):
        key,opts=self.issued()
        for field,value in [('caller_id','release-owner'),('grant_sha256','0'*64)]:
            x=dict(opts);x[field]=value
            with self.subTest(field=field):self.error('AUTHORIZATION_DENIED',self.manager.prepare,key,**x)
        self.assertEqual(self.manager.inspect_release(key)['status'],'GRANTED')

    def test_self_issued_release_rejected(self):
        from nss_base.overlaygenerationmanager001 import OPERATORS
        ops=deepcopy(OPERATORS);ops[-1]['roles'].append('ISSUER')
        m=Generations.create(self.root/'self-grant',ops)
        m.propose(self.gs[0],**self.ev);m.qualify(self.hashes[0],reviewer_id='generation-reviewer',**self.ev)
        r=m.make_request(self.hashes[0],release_id='self',caller_id='local-runner',mode='BOOTSTRAP',reason='test')
        self.error('AUTHORIZATION_DENIED',m.issue,r,issuer_id='local-runner',ttl_seconds=100,**self.ev)

    def test_expiry_blocks_each_not_yet_published_phase(self):
        for phase in ('prepare','stage','publish'):
            with self.subTest(phase=phase):
                key,opts=self.issued(id=phase)
                if phase!='prepare':self.manager.prepare(key,**opts)
                if phase=='publish':self.manager.stage(key,**opts)
                self.clock+=300
                self.error('AUTHORIZATION_DENIED',getattr(self.manager,phase),key,**opts)
                self.assertEqual(self.manager.inspect()['current']['epoch'],0)

    def test_clock_cannot_move_backwards(self):
        key,opts=self.issued();self.clock-=1
        self.error('AUTHORIZATION_DENIED',self.manager.prepare,key,**opts)

    def test_request_cas_detects_competing_publish_and_aba(self):
        self.adopted();stale=self.request(1,'stale','UPDATE')
        self.adopted(1,'second','UPDATE');self.adopted(0,'back','ROLLBACK')
        self.error('CONSTRAINT_CONFLICT',self.manager.issue,stale,issuer_id='release-owner',ttl_seconds=100,**self.ev)

    def test_two_issued_bootstraps_cannot_both_publish(self):
        a,ao=self.issued();b,bo=self.issued(1,'other')
        for f in (self.manager.prepare,self.manager.stage):f(b,**bo)
        for f in (self.manager.prepare,self.manager.stage,self.manager.publish):f(a,**ao)
        self.error('CONSTRAINT_CONFLICT',self.manager.publish,b,**bo)
        self.assertEqual(self.manager.inspect()['current']['generation_sha256'],self.hashes[0])

    def test_rollback_requires_previously_published_target(self):
        self.adopted();req=self.request(1,'back','ROLLBACK')
        self.error('INCOMPATIBLE_CONFIGURATION',self.manager.issue,req,issuer_id='release-owner',ttl_seconds=100,**self.ev)

    def test_return_to_archived_generation_requires_explicit_rollback_mode(self):
        self.adopted();self.adopted(1,'next','UPDATE');req=self.request(0,'wrong','UPDATE')
        self.error('INCOMPATIBLE_CONFIGURATION',self.manager.issue,req,issuer_id='release-owner',ttl_seconds=100,**self.ev)

    def test_release_revocation_blocks_resume(self):
        key,opts=self.issued();self.manager.prepare(key,**opts)
        self.manager.revoke(key,kind='RELEASE',actor_id='release-owner',reason='Withdraw')
        self.error('AUTHORIZATION_DENIED',self.manager.stage,key,**opts)

    def test_child_qualification_revocation_after_stage_preserves_source(self):
        self.adopted();before=self.manager.inspect()['current'];key,opts=self.issued(1,'next','UPDATE')
        self.manager.prepare(key,**opts);self.manager.stage(key,**opts);self.withdraw_child()
        self.error('AUTHORIZATION_DENIED',self.manager.publish,key,**opts)
        self.assertEqual(self.manager.inspect()['current'],before)

    def test_source_training_permission_revocation_after_stage_blocks_publish(self):
        key,opts=self.issued();self.manager.prepare(key,**opts);self.manager.stage(key,**opts)
        ProbeData(self.root/'probe/data').revoke_for_test()
        self.error('TRAINING_RESTRICTED',self.manager.publish,key,**opts)
        self.assertEqual(self.manager.inspect()['current']['epoch'],0)

    def test_generation_qualification_revocation_blocks_new_use_not_history(self):
        key,opts=self.adopted();before=self.manager.inspect()['current']
        self.manager.revoke(self.hashes[0],kind='QUALIFICATION',actor_id='generation-reviewer',reason='Withdraw')
        self.error('AUTHORIZATION_DENIED',self.manager.pin_stage,'blocked',profile='CORE',caller_id='local-runner',**self.ev)
        self.assertTrue(self.manager.publish(key,**opts)['historical']);self.assertEqual(self.manager.inspect()['current'],before)

    def test_immutable_grant_retry_cannot_extend_duration(self):
        r=self.request();a=self.manager.issue(r,issuer_id='release-owner',ttl_seconds=100,**self.ev)
        self.clock+=10;b=self.manager.issue(r,issuer_id='release-owner',ttl_seconds=100,**self.ev)
        self.assertTrue(b['historical']);self.assertEqual(a['grant'],b['grant'])
        self.error('CONSTRAINT_CONFLICT',self.manager.issue,r,issuer_id='release-owner',ttl_seconds=200,**self.ev)

    def test_abandoned_release_is_permanently_spent(self):
        key,opts=self.issued();self.manager.prepare(key,**opts)
        self.manager.abandon(key,caller_id='local-runner',reason='Stop')
        self.assertEqual(self.manager.abandon(key,caller_id='local-runner',reason='Stop')['status'],'ABANDONED')
        self.error('CONSTRAINT_CONFLICT',self.manager.stage,key,**opts)

    def test_published_release_cannot_be_abandoned(self):
        key,_=self.adopted()
        self.error('CONSTRAINT_CONFLICT',self.manager.abandon,key,caller_id='local-runner',reason='Undo')

    def test_stage_pin_blocks_publication_and_second_simultaneous_stage(self):
        self.adopted();key,opts=self.issued(1,'next','UPDATE');self.manager.prepare(key,**opts);self.manager.stage(key,**opts)
        ticket=self.manager.pin_stage('working',profile='A',caller_id='local-runner',**self.ev)
        self.error('RECOVERY_REQUIRED',self.manager.publish,key,**opts)
        self.error('RECOVERY_REQUIRED',self.manager.pin_stage,'other',profile='CORE',caller_id='local-runner',**self.ev)
        reopened=Generations(self.root/'generations');self.assertEqual(reopened.inspect_stage('working')['ticket'],ticket)
        reopened.close_stage(ticket,caller_id='local-runner');self.manager.publish(key,**opts)
        self.error('INCOMPATIBLE_CONFIGURATION',reopened.read_stage,ticket,caller_id='local-runner',**self.ev)

    def test_profile_scope_and_exact_returned_members(self):
        self.adopted(1)
        for profile,roles in [('CORE',['core']),('A',['A','core']),('AB',['A','B','core'])]:
            with self.subTest(profile=profile):
                t=self.manager.pin_stage('s-'+profile,profile=profile,caller_id='local-runner',**self.ev)
                self.assertEqual(sorted(self.manager.read_stage(t,caller_id='local-runner',**self.ev)['artifacts']),roles)
                self.manager.close_stage(t,caller_id='local-runner')
        self.error('INCOMPATIBLE_CONFIGURATION',self.manager.pin_stage,'unlisted',profile='B',caller_id='local-runner',**self.ev)

    def test_stage_identity_and_closed_ticket_cannot_be_reused(self):
        self.adopted();t=self.manager.pin_stage('stage',profile='A',caller_id='local-runner',**self.ev)
        altered=deepcopy(t);altered['configuration']['epoch']+=1
        self.error('VALIDATION_FAILED',self.manager.read_stage,altered,caller_id='local-runner',**self.ev)
        self.manager.close_stage(t,caller_id='local-runner')
        self.error('CONSTRAINT_CONFLICT',self.manager.pin_stage,'stage',profile='A',caller_id='local-runner',**self.ev)

    def test_ticket_epoch_differs_after_rollback_to_same_weights(self):
        self.adopted();t1=self.manager.pin_stage('first',profile='A',caller_id='local-runner',**self.ev)
        self.manager.close_stage(t1,caller_id='local-runner')
        self.adopted(1,'next','UPDATE');self.adopted(0,'back','ROLLBACK')
        t2=self.manager.pin_stage('later',profile='A',caller_id='local-runner',**self.ev)
        self.assertEqual(t1['profile_ecid'],t2['profile_ecid']);self.assertNotEqual(fingerprint(t1),fingerprint(t2))
        self.error('INCOMPATIBLE_CONFIGURATION',self.manager.read_stage,t1,caller_id='local-runner',**self.ev)

    def test_source_permission_rechecked_on_each_stage_read(self):
        self.adopted();t=self.manager.pin_stage('active',profile='A',caller_id='local-runner',**self.ev)
        ProbeData(self.root/'probe/data').revoke_for_test()
        self.error('TRAINING_RESTRICTED',self.manager.read_stage,t,caller_id='local-runner',**self.ev)
        self.assertEqual(self.manager.close_stage(t,caller_id='local-runner')['status'],'CLOSED')

    def test_bad_hook_cannot_silently_disable_fault_test(self):
        key,opts=self.issued()
        self.error('VALIDATION_FAILED',self.manager.prepare,key,**opts,fault_at='typo')

    def test_no_neighboring_store_or_effect_is_changed(self):
        from nss_base.neural_records import ProbeRuns
        before=ProbeRuns(self.root/'probe/journal').inspect('probe-001');self.adopted()
        self.assertEqual(before,ProbeRuns(self.root/'probe/journal').inspect('probe-001'))
        self.assertEqual(Ledger(self.root/'probe/mock_actions').effect_count(),1)
