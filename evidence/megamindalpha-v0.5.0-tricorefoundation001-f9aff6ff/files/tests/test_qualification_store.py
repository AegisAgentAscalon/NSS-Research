from copy import deepcopy
from contextlib import closing
import sqlite3
from unittest.mock import patch

from qualification_helpers import QualificationCase,AT,OPERATORS,review_for
from nss_base.neural_contracts import encoded,fingerprint,read_document
from nss_base.neural_data import ProbeData
from nss_base.neural_records import ProbeRuns
from nss_base.qualification_neural import NeuralEvidence
from nss_base.qualification_store import Qualifications
from nss_base.runtime import ContractError


class QualificationStoreTests(QualificationCase):
    def test_all_exact_claims_are_usable_but_not_permits(self):
        for key in self.requests:
            with self.subTest(key=key):
                r=self.use(key);self.assertTrue(r['evidence_satisfies_claim']);self.assertFalse(r['deployment_authorized'])
    def test_evaluation_alone_creates_no_qualification(self):
        q=Qualifications.create(self.root/'emptyq',OPERATORS)
        self.assertEqual(q.audit()['requests'],0)
        self.error('INSUFFICIENT_EVIDENCE',q.inspect,'core')
    def test_prepared_is_not_accepted(self):
        r=self.req();s=self.q.prepare(r,source=self.source);self.assertEqual(s['status'],'PREPARED')
        self.assertIsNone(s['certificate'])
    def test_unprepared_decision_is_denied(self):
        self.error('INSUFFICIENT_EVIDENCE',self.q.decide,review_for(self.req()),source=self.source)
    def test_same_producer_reviewer_rejected(self):
        r=self.req(producer='fixture-both');self.q.prepare(r,source=self.source)
        self.error('AUTHORIZATION_DENIED',self.q.decide,review_for(r,reviewer='fixture-both'),source=self.source)
        self.assertEqual(self.q.inspect('new')['status'],'PREPARED')
    def test_unknown_reviewer_rejected(self):
        r=self.req();self.q.prepare(r,source=self.source)
        self.error('AUTHORIZATION_DENIED',self.q.decide,review_for(r,reviewer='unknown'),source=self.source)
    def test_unknown_producer_rejected(self):
        r=self.req(producer='unknown');self.error('AUTHORIZATION_DENIED',self.q.prepare,r,source=self.source)
    def test_wrong_request_digest_rejected(self):
        r=self.req();self.q.prepare(r,source=self.source);d=review_for(r);d['request_sha256']='b'*64
        self.error('CONSTRAINT_CONFLICT',self.q.decide,d,source=self.source)
    def test_manual_rejection_has_no_certificate(self):
        r=self.req();self.q.prepare(r,source=self.source)
        result=self.q.decide(review_for(r,'REJECT'))
        self.assertEqual(result['verdict'],'REJECTED');self.assertIsNone(result['certificate_sha256'])
        self.assertEqual(self.q.inspect('new')['verification']['verdict'],'NOT_RUN')
    def test_manual_inconclusive_has_no_certificate(self):
        r=self.req();self.q.prepare(r,source=self.source)
        result=self.q.decide(review_for(r,'INCONCLUSIVE'));self.assertEqual(result['verdict'],'INCONCLUSIVE')
        self.assertIsNone(result['certificate_sha256'])
    def test_rejected_cannot_be_promoted_by_retry(self):
        r=self.req();self.q.prepare(r,source=self.source);self.q.decide(review_for(r,'REJECT'))
        d=review_for(r);d['operation_id']='new-op';self.error('CONSTRAINT_CONFLICT',self.q.decide,d,source=self.source)
    def test_acceptance_requires_real_checker(self):
        r=self.req();self.q.prepare(r,source=self.source)
        self.error('VALIDATION_FAILED',self.q.decide,review_for(r),source={'verdict':'PASS'})
    def test_changed_plan_binding_blocked_at_prepare(self):
        r=self.req();r['binding']['plan_sha256']='c'*64
        self.error('INCOMPATIBLE_CONFIGURATION',self.q.prepare,r,source=self.source)
    def test_scope_cannot_be_widened_to_subset(self):
        self.error('INCOMPATIBLE_CONFIGURATION',self.use,'ab',scope={'kind':'PROFILE','profile':'A'})
    def test_profile_is_not_transition_evidence(self):
        self.error('INCOMPATIBLE_CONFIGURATION',self.use,'ab',scope=self.requests['edge']['claim'])
    def test_reverse_transition_cannot_be_inferred(self):
        self.error('INCOMPATIBLE_CONFIGURATION',self.use,'edge',scope={'kind':'TRANSITION','source':'A','destination':'AB','mode':'replay'})
    def test_other_trial_binding_cannot_be_substituted(self):
        b=deepcopy(self.requests['edge']['binding']);b['trial_seed']=211
        self.error('INCOMPATIBLE_CONFIGURATION',self.use,bind=b)
    def test_other_precision_cannot_be_substituted(self):
        b=deepcopy(self.requests['edge']['binding']);b['precision']='ternary_core_reference'
        self.error('INCOMPATIBLE_CONFIGURATION',self.use,bind=b)
    def test_certificate_hash_must_be_exact(self):
        self.error('INCOMPATIBLE_CONFIGURATION',self.use,sha='e'*64)
    def test_missing_prerequisite(self):
        r=self.req(profile='A',parents=['unknown']);self.error('INSUFFICIENT_EVIDENCE',self.q.prepare,r,source=self.source)
    def test_ab_cannot_substitute_for_core_prerequisite(self):
        r=self.req(profile='A',parents=['ab']);self.error('INCOMPATIBLE_CONFIGURATION',self.q.prepare,r,source=self.source)
    def test_prepared_prerequisite_not_usable(self):
        r=self.req();self.q.prepare(r,source=self.source)
        second=self.req('dependent','A',['new']);self.error('INSUFFICIENT_EVIDENCE',self.q.prepare,second,source=self.source)
    def test_core_revocation_invalidates_profile(self):
        self.q.revoke(self.revoke());self.error('AUTHORIZATION_DENIED',self.use,'a')
    def test_core_revocation_invalidates_transition_transitively(self):
        self.q.revoke(self.revoke());self.error('AUTHORIZATION_DENIED',self.use,'edge')
    def test_endpoint_revocation_invalidates_only_dependents(self):
        self.q.revoke(self.revoke('a'));self.error('AUTHORIZATION_DENIED',self.use,'edge')
        self.assertEqual(self.use('ab')['status'],'SUCCESS')
    def test_revocation_preserves_original_decision(self):
        old=self.q.inspect('core');self.q.revoke(self.revoke());self.assertEqual(self.q.inspect('core'),old)
        self.assertEqual(len(self.q.history('core')['revocations']),1)
    def test_old_decision_retry_after_revocation_is_history_only(self):
        self.q.revoke(self.revoke());out=self.q.decide(review_for(self.requests['core']),source=self.source)
        self.assertTrue(out['historical']);self.error('AUTHORIZATION_DENIED',self.use,'core')
    def test_revocation_retry_no_duplicate_event(self):
        r=self.revoke();self.q.revoke(r);n=self.q.audit()['events'];out=self.q.revoke(r)
        self.assertTrue(out['historical']);self.assertEqual(self.q.audit()['events'],n)
    def test_revocation_operation_collision(self):
        r=self.revoke();self.q.revoke(r);r['reason']='Different explanation'
        self.error('CONSTRAINT_CONFLICT',self.q.revoke,r)
    def test_revocation_wrong_certificate(self):
        r=self.revoke();r['certificate_sha256']='f'*64;self.error('CONSTRAINT_CONFLICT',self.q.revoke,r)
    def test_unknown_revoker_denied(self):
        r=self.revoke();r['reviewer_id']='fixture-builder';self.error('AUTHORIZATION_DENIED',self.q.revoke,r)
    def test_permission_withdrawal_blocks_new_issuance(self):
        r=self.req();self.q.prepare(r,source=self.source);ProbeData(self.root/'probe/data').revoke_for_test()
        self.error('TRAINING_RESTRICTED',self.q.decide,review_for(r),source=self.source)
        self.assertEqual(self.q.inspect('new')['status'],'PREPARED')
    def test_permission_withdrawal_blocks_current_use(self):
        ProbeData(self.root/'probe/data').revoke_for_test();self.error('TRAINING_RESTRICTED',self.use,'core')
    def test_old_decision_history_does_not_need_live_data(self):
        ProbeData(self.root/'probe/data').revoke_for_test()
        out=self.q.decide(review_for(self.requests['core']));self.assertTrue(out['historical'])
    def test_changed_test_fixture_blocks_use(self):
        p=self.root/'probe/data/test.json';data=read_document(p);data['pairs'][0]=[15,15];p.write_bytes(encoded(data))
        self.error('VALIDATION_FAILED',self.use,'core')
    def test_missing_source_journal_fails_closed(self):
        (self.root/'probe/journal/neural_runs.sqlite3').unlink()
        self.error('RECOVERY_REQUIRED',self.use,'core')
    def test_changed_code_identity_fails_closed(self):
        with patch('nss_base.neuralprobe001.implementation',return_value={'sha256':'0'*64}):
            self.error('INCOMPATIBLE_CONFIGURATION',self.use,'core')
    def test_changed_backend_identity_blocks_use(self):
        import torch
        with patch.object(torch.__config__,'show',return_value='changed build'):
            self.error('INCOMPATIBLE_CONFIGURATION',self.use,'core')
    def test_source_report_unchanged_and_effect_not_repeated(self):
        from nss_base.ledger import Ledger
        before=ProbeRuns(self.root/'probe/journal').inspect('probe-001')
        r=self.req();self.q.prepare(r,source=self.source);self.q.decide(review_for(r),source=self.source)
        self.assertEqual(before,ProbeRuns(self.root/'probe/journal').inspect('probe-001'))
        self.assertEqual(Ledger(self.root/'probe/mock_actions').effect_count(),1)
    def test_reopen_all_owners_and_consume(self):
        self.q=Qualifications(self.root/'q');self.source=NeuralEvidence(self.root/'probe/journal',self.root/'probe/data')
        self.assertEqual(self.use()['status'],'SUCCESS')
    def test_prepare_idempotent(self):
        old=self.q.audit()['events'];out=self.q.prepare(self.requests['core'],source=self.source)
        self.assertTrue(out['historical']);self.assertEqual(self.q.audit()['events'],old)
    def test_prepare_id_collision(self):
        r=deepcopy(self.requests['core']);r['at']='2026-09-11T13:00:00Z'
        self.error('CONSTRAINT_CONFLICT',self.q.prepare,r,source=self.source)
    def test_decision_operation_cannot_revoke(self):
        r=self.revoke();r['operation_id']='review:core';self.error('CONSTRAINT_CONFLICT',self.q.revoke,r)
    def test_decision_timestamp_cannot_predate_request(self):
        r=self.req();self.q.prepare(r,source=self.source);d=review_for(r);d['at']='2025-01-01T00:00:00Z'
        self.error('CONSTRAINT_CONFLICT',self.q.decide,d,source=self.source)
    def test_no_implicit_store_creation(self):
        self.error('RECOVERY_REQUIRED',Qualifications,self.root/'missing')
    def test_no_overwriting_existing_store(self):
        self.error('CONSTRAINT_CONFLICT',Qualifications.create,self.root/'q',OPERATORS)
    def test_unknown_crash_hook_rejected(self):
        self.error('VALIDATION_FAILED',self.q.revoke,self.revoke(),fault_at='imagined')
    def test_store_is_structural_audit_not_live_permissions(self):
        ProbeData(self.root/'probe/data').revoke_for_test()
        self.assertEqual(self.q.audit()['scope'],'STORED_STRUCTURE_ONLY_NOT_CURRENT_ELIGIBILITY')
    def test_invalid_source_path_types_are_typed_failures(self):
        self.error('VALIDATION_FAILED',NeuralEvidence,False,self.root)
    def test_invalid_store_path_type_is_typed_failure(self):
        self.error('VALIDATION_FAILED',Qualifications,True)
