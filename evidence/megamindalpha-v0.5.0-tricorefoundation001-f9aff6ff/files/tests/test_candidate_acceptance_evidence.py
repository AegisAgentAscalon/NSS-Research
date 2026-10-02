from copy import deepcopy
from unittest.mock import patch
from candidate_acceptance_helpers import CandidateCase
from nss_base.candidate_records import CandidateRuns
from nss_base.generation_contracts import generation, generation_certificate
from nss_base.generation_evidence import from_evidence
from nss_base.neural_contracts import encoded, fingerprint
from nss_base.qualification_candidate import CandidateEvidence, from_config
from nss_base.qualification_contracts import binding, request, review_actor, verification
from nss_base.qualification_sources import require_source
from nss_base.qualificationevidence002 import review_for
from nss_base.runtime import ContractError


class CandidateEvidenceTests(CandidateCase):
    def test_new_source_is_explicit_and_bound_to_all_owner_receipts(self):
        b=self.reqs[0]['binding'];c=self.co.cycles.inspect(self.plan['cycle_id'])
        self.assertEqual(b['source_format'],'MegaMindAlpha.CandidateEvidence001')
        self.assertEqual(set(b['checkpoint_hashes']),{'core','A','B','A2'})
        self.assertEqual(set(b['profile_ecids']),{'CORE','A2','A2B'})
        self.assertEqual(b['candidate_lineage']['training_receipt'],c['receipts']['TRAIN'])
        self.assertEqual(b['candidate_lineage']['evaluation_receipt'],c['receipts']['EVALUATE'])
        self.assertEqual(b['candidate_lineage']['proposal_sha256'],fingerprint(c['proposal']))
        self.assertEqual(b['candidate_lineage']['parent_binding_sha256'],fingerprint(self.plan['parent']))

    def test_every_new_claim_has_current_evidence_but_no_deployment_authority(self):
        for r in self.reqs:
            with self.subTest(claim=r['claim']):
                out=self.use(r['request_id']);self.assertTrue(out['evidence_satisfies_claim'])
                self.assertFalse(out['deployment_authorized'])
                self.assertEqual(self.q.inspect(r['request_id'])['verification']['checker_identity']['name'],'qualification_candidate_v1')
        self.assert_no_training_or_effect()

    def test_independent_checker_repeats_saved_weights_without_training(self):
        before=self.co.training.audit();v=self.source.verify(self.reqs[1])
        self.assertEqual(v['verdict'],'PASS');self.assertEqual(v['repeats'][0],v['repeats'][1])
        self.assertEqual(self.co.training.audit(),before)

    def test_wrong_source_adapter_cannot_read_candidate_certificate(self):
        with self.assertRaises(ContractError):self.use(source=self.co.source)
        with self.assertRaises(ContractError):self.q.check_use('a',certificate_sha256=fingerprint(self.q.inspect('a')['certificate']),
            expected_claim={'kind':'PROFILE','profile':'A'},expected_binding=self.plan['parent'],source=self.source)

    def test_cannot_relabel_a2_as_a_or_import_old_core_approval(self):
        req=self.fresh(profile='A2',prerequisites=['core'])
        self.error('INCOMPATIBLE_CONFIGURATION',self.q.prepare,req,source=self.source)
        for name in ('A','B','AB'):
            with self.subTest(name=name):
                with self.assertRaises(ContractError):self.fresh(profile=name,prerequisites=['candidate-core'])

    def test_stripping_source_tag_does_not_make_candidate_legacy(self):
        b=deepcopy(self.reqs[0]['binding']);b.pop('source_format');b.pop('candidate_lineage')
        self.error('VALIDATION_FAILED',binding,b)

    def test_request_cannot_bind_new_profile_to_legacy_evidence(self):
        r=deepcopy(self.reqs[1]);r['binding']=deepcopy(self.plan['parent'])
        self.error('INCOMPATIBLE_CONFIGURATION',request,r)

    def test_substituted_binding_components_fail_current_guard(self):
        for key in ('plan_sha256','report_sha256','data_binding_sha256','protocol_sha256','runtime_sha256'):
            with self.subTest(key=key):
                r=deepcopy(self.reqs[0]);r['request_id']='substitute';r['binding'][key]='f'*64
                self.error('INCOMPATIBLE_CONFIGURATION',self.q.prepare,r,source=self.source)

    def test_substituted_candidate_lineage_fails(self):
        for key in ('cycle_sha256','proposal_sha256','parent_binding_sha256','criteria_sha256','retention_pairs_sha256'):
            with self.subTest(key=key):
                r=deepcopy(self.reqs[0]);r['request_id']='lineage';r['binding']['candidate_lineage'][key]='d'*64
                self.error('INCOMPATIBLE_CONFIGURATION',self.q.prepare,r,source=self.source)

    def test_candidate_owner_receipt_cannot_be_swapped(self):
        r=deepcopy(self.reqs[0]);r['request_id']='other-receipt'
        r['binding']['candidate_lineage']['training_receipt']['report_sha256']='c'*64
        self.error('INCOMPATIBLE_CONFIGURATION',self.q.prepare,r,source=self.source)

    def test_profile_union_and_reverse_edges_not_inferred(self):
        scopes=[{'kind':'PROFILE','profile':'B'}, {'kind':'PROFILE','profile':'A2+B+A'},
            {'kind':'TRANSITION','source':'A2','destination':'A2B','mode':'replay'},
            {'kind':'TRANSITION','source':'A2B','destination':'CORE','mode':'replay'}]
        for scope in scopes:
            with self.subTest(scope=scope):
                with self.assertRaises(ContractError):self.use(expected_claim=scope)

    def test_missing_and_wrong_endpoint_prerequisites_rejected(self):
        r=deepcopy(self.reqs[3]);r['request_id']='missing-parent';r['prerequisites'][1]='not-exists'
        self.error('INSUFFICIENT_EVIDENCE',self.q.prepare,r,source=self.source)
        r['prerequisites']=['core','a','ab']
        self.error('INCOMPATIBLE_CONFIGURATION',self.q.prepare,r,source=self.source)

    def test_parent_qualification_withdrawal_blocks_candidate_use(self):
        before=self.q.inspect('candidate-a2b');self.withdraw('core')
        self.error('AUTHORIZATION_DENIED',self.use)
        self.assertEqual(self.q.inspect('candidate-a2b'),before)

    def test_parent_qualification_withdrawal_blocks_new_decision(self):
        r=self.fresh();self.q.prepare(r,source=self.source);self.withdraw('core')
        self.error('AUTHORIZATION_DENIED',self.q.decide,review_for(r),source=self.source)
        self.assertEqual(self.q.inspect(r['request_id'])['status'],'PREPARED')

    def test_actual_training_producer_is_not_its_own_reviewer(self):
        self.error('AUTHORIZATION_DENIED',review_actor,self.reqs[0],'learner-worker')
        review_actor(self.reqs[0],'fixture-reviewer')
        r=self.fresh();r['producer_id']='fixture-both';self.q.prepare(r,source=self.source)
        self.error('AUTHORIZATION_DENIED',self.q.decide,review_for(r,reviewer='fixture-both'),source=self.source)

    def test_candidate_producer_not_generation_reviewer(self):
        manifest={'operators':[{'id':'learner-worker','roles':['REVIEWER']}]}
        self.error('AUTHORIZATION_DENIED',generation_certificate,self.family,'learner-worker',self.clock,manifest)

    def test_source_config_is_closed_and_does_not_create_owners(self):
        self.assertIs(type(from_config(self.config)),CandidateEvidence)
        cfg=deepcopy(self.config);cfg['candidates']=str(self.root/'missing-candidate')
        self.error('RECOVERY_REQUIRED',from_config,cfg)
        self.assertFalse((self.root/'missing-candidate').exists())
        self.error('VALIDATION_FAILED',from_config,dict(self.config,extra='ignored'))
        self.error('VALIDATION_FAILED',require_source,{'status':'PASS'})
        class Fake(CandidateEvidence):pass
        self.error('VALIDATION_FAILED',require_source,object.__new__(Fake))

    def test_candidate_data_withdrawal_blocks_use_not_history(self):
        from nss_base.neural_data import ProbeData
        before=self.q.inspect('candidate-a2b');ProbeData(self.root/'learning-data').revoke_for_test()
        self.error('TRAINING_RESTRICTED',self.use)
        self.assertEqual(self.q.inspect('candidate-a2b'),before)
        out=self.q.decide(review_for(self.reqs[2]),source=self.source)
        self.assertTrue(out['historical']);self.assert_no_training_or_effect()

    def test_parent_data_withdrawal_also_blocks_candidate(self):
        from nss_base.neural_data import ProbeData
        ProbeData(self.root/'probe/data').revoke_for_test();self.error('TRAINING_RESTRICTED',self.use)

    def test_withdrawn_learning_proposal_blocks_accepted_candidate(self):
        self.co.cycles.withdraw(self.plan['cycle_id'],actor_id='human-operator',reason='Withdraw plan',at=self.clock)
        self.error('AUTHORIZATION_DENIED',self.use)

    def test_changed_dataset_revision_blocks_use(self):
        from nss_base.learner_coordinator import unwrap
        a=self.co.archive;r=unwrap(a.inspect('neural-train'))
        change={'schema_version':1,'operation_id':'candidate:correct','experience_id':'neural-train',
            'expected_revision_hash':r['reference']['sha256'],'actor':{'id':'fixture-human','kind':'HUMAN','version':'1'},
            'at':'2026-09-11T12:00:00Z','action':'REVIEW','payload':{'decision':'REJECTED'},'reason':'Stop use'}
        unwrap(a.change(change))
        with self.assertRaises(ContractError):self.use()

    def test_missing_owner_artifacts_fail_closed(self):
        self.co.training.path.rename(self.co.training.path.with_suffix('.missing'))
        with self.assertRaises(ContractError):self.use()

    def test_altered_saved_metrics_not_accepted(self):
        ev=self.co.evaluations.inspect(self.reqs[0]['binding']['candidate_lineage']['evaluation_receipt']['id'])
        altered=deepcopy(ev);altered['report']['repeats'][0]['A2']['mse']+=1e-12
        with patch.object(type(self.co.evaluations),'inspect',return_value=altered):
            with self.assertRaises(ContractError):self.source.verify(self.reqs[1])

    def test_corrupted_candidate_payload_is_detected(self):
        runid=self.reqs[0]['binding']['candidate_lineage']['training_receipt']['id']
        tr=self.co.training.inspect(runid);bad=deepcopy(tr);bad['report']['checkpoint_hashes']['A2']='b'*64
        with patch.object(CandidateRuns,'inspect',return_value=bad):
            self.error('VALIDATION_FAILED',self.use)

    def test_reject_and_inconclusive_produce_no_certificate(self):
        for kind in ('REJECT','INCONCLUSIVE'):
            r=self.fresh(name='review-'+kind);self.q.prepare(r,source=self.source)
            out=self.q.decide(review_for(r,kind));self.assertIsNone(out['certificate_sha256'])
            self.assertEqual(self.q.inspect(r['request_id'])['verification']['verdict'],'NOT_RUN')

    def test_old_and_new_families_cannot_mix_certificates(self):
        self.error('INCOMPATIBLE_CONFIGURATION',from_evidence,'mixed','fixture-builder',
            ['core','candidate-a2'],['candidate-to-core'],qualifications=self.q)
        for key,val in [('purpose','BOUNDED_NEURAL_PROBE_GENERATION'),('binding',self.plan['parent'])]:
            g=deepcopy(self.family);g[key]=val
            with self.subTest(key=key),self.assertRaises(ContractError):generation(g)

    def test_unknown_or_altered_source_format_rejected(self):
        for value in ('other',None,False):
            r=deepcopy(self.reqs[0]);r['binding']['source_format']=value
            with self.subTest(value=value):self.error('INCOMPATIBLE_CONFIGURATION',request,r)

    def test_numerical_environment_is_bound(self):
        with patch('nss_base.neural_backend.environment',return_value={'changed':True}):
            self.error('INCOMPATIBLE_CONFIGURATION',self.use)

    def test_checker_identity_cannot_be_changed_to_legacy(self):
        v=self.q.inspect('candidate-core')['verification'];v=deepcopy(v)
        v['checker_identity']['name']='unknown';self.error('INCOMPATIBLE_CONFIGURATION',verification,v)

    def test_legacy_evidence_remains_valid_independently(self):
        c=self.q.inspect('core');out=self.q.check_use('core',certificate_sha256=fingerprint(c['certificate']),
            expected_claim=c['request']['claim'],expected_binding=c['request']['binding'],source=self.co.source)
        self.assertEqual(out['status'],'SUCCESS');self.assert_no_training_or_effect()

    def test_actually_undertrained_candidate_is_rejected(self):
        from nss_base.boundedlearnercoordinator001 import plan_from_reviewed_data
        p=plan_from_reviewed_data(self.co,cycle_id='insufficient-learning',steps=1)
        self.co.prepare(p);self.co.cycles.approve(p['cycle_id'],approver_id='human-operator',
            expires_at=self.co.now()+600,at=self.co.now())
        self.co.advance(p['cycle_id'],caller_id='learner-worker')
        r=self.source.propose(run_id=p['cycle_id'],seed=p['recipe']['seed'],precision=p['parent']['precision'],
            scope={'kind':'PROFILE','profile':'CORE'},producer_id='fixture-builder',request_id='failed-candidate',at=p['snapshot_request']['at'])
        self.q.prepare(r,source=self.source);out=self.q.decide(review_for(r),source=self.source)
        self.assertEqual(out['verdict'],'REJECTED');self.assertIsNone(out['certificate_sha256'])
        self.assertEqual(self.manager.inspect()['current'],self.parent)

    def test_revoked_parent_blocks_before_numerical_verification(self):
        r=self.fresh();self.q.prepare(r,source=self.source);self.withdraw('core')
        with patch.object(CandidateEvidence,'verify',side_effect=AssertionError('Unapproved numerical work')) as check:
            self.error('AUTHORIZATION_DENIED',self.q.decide,review_for(r),source=self.source)
            check.assert_not_called()
        self.assertEqual(self.q.inspect(r['request_id'])['status'],'PREPARED')

    def test_legacy_claim_parser_stays_strict_unless_candidate_format_is_explicit(self):
        from nss_base.qualification_contracts import claim, CANDIDATE_FORMAT
        c={'kind':'PROFILE','profile':'A2'}
        self.error('INCOMPATIBLE_CONFIGURATION',claim,c)
        self.assertEqual(claim(c,source_format=CANDIDATE_FORMAT),c)
        self.error('INCOMPATIBLE_CONFIGURATION',claim,{'kind':'PROFILE','profile':'A'},source_format=CANDIDATE_FORMAT)
