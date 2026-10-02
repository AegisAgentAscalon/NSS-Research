from copy import deepcopy
import json
from unittest.mock import patch

from nss_base.dataset_store import DatasetSnapshots
from nss_base.evaluation_store import EvaluationRuns
from nss_base.experience_store import ExperienceArchive
from dataset_helpers import change, revoke, approved, build_request
from evaluation_helpers import EvaluationCase, ok

class EvaluationDataTests(EvaluationCase):
    def test_development_snapshot_is_bound_but_not_promoted_to_hidden_exam(self):
        ref=self.add_dataset();ok(self.execute());m=self.inspect()['material']
        self.assertEqual(m['development_observation']['sha256'],ref['sha256'])
        self.assertEqual(m['development_observation']['member_count'],1)
        self.assertEqual(self.report()['scope'],'DEVELOPMENT_SYNTHETIC_NOT_RELEASE_QUALIFICATION')
        self.assertNotIn('Reviewed fixture val',json.dumps(m))

    def test_optional_snapshot_requires_all_public_adapters(self):
        self.add_dataset();self.kw.pop('snapshots')
        self.assertEqual(self.execute()['status'],'CAPABILITY_UNAVAILABLE')

    def test_unbound_snapshot_arguments_are_rejected(self):
        self.add_dataset();self.plan['development_snapshot']=None
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_only_declared_development_validation_split_is_supported(self):
        self.add_dataset();self.plan['development_snapshot']['split']='protected_holdout'
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_pending_review_blocks_new_evaluation(self):
        self.add_dataset();ok(change(self.archive,'val','CORRECT',{
            'statement':{'text':'Needs new review','uncertainty':'LOW','support_ids':['source1']},'evidence':[]}))
        self.assertNotEqual(self.execute()['status'],'SUCCESS');self.assertEqual(ok(self.store.audit())['runs'],0)

    def test_revocation_blocks_new_attempt_and_current_use(self):
        self.add_dataset();ok(self.execute());ok(revoke(self.archive,'val'))
        self.assertEqual(self.verify()['status'],'TRAINING_RESTRICTED')
        p=deepcopy(self.plan);p['run_id']='run-after-revocation'
        self.assertEqual(self.execute(p)['status'],'TRAINING_RESTRICTED');self.assertEqual(ok(self.store.audit())['runs'],1)

    def test_revocation_does_not_rewrite_historical_report_or_regrant_on_retry(self):
        self.add_dataset();ok(self.execute());history=self.inspect();ok(revoke(self.archive,'val'))
        self.assertEqual(history,self.inspect());result=self.execute()
        self.assertTrue(result['historical']);self.assertFalse(result['authorizes_deployment'])
        self.assertEqual(self.verify()['status'],'TRAINING_RESTRICTED')

    def test_prepared_resume_rechecks_current_training_permission(self):
        self.add_dataset();ok(self.store.prepare(self.plan,**self.kw));ok(revoke(self.archive,'val'))
        self.store=EvaluationRuns(self.root/'evaluations')
        self.assertEqual(self.execute()['status'],'TRAINING_RESTRICTED');self.assertIsNone(self.report())

    def test_each_repeat_and_finalization_recheck_snapshot(self):
        self.add_dataset();original=self.snapshots.read_for_use
        with patch.object(self.snapshots,'read_for_use',wraps=original) as wrapped:
            ok(self.execute());self.assertEqual(wrapped.call_count,4)  # prepare, repeat1, repeat2, final gate
            self.assertTrue(all(c.kwargs['purpose']=='training' for c in wrapped.call_args_list))

    def test_revocation_between_repeats_stops_publication(self):
        self.add_dataset();original=self.snapshots.read_for_use;count=0
        def gated(*a,**kw):
            nonlocal count
            count+=1;result=original(*a,**kw)
            if count==2:ok(revoke(self.archive,'val'))
            return result
        with patch.object(self.snapshots,'read_for_use',side_effect=gated):
            self.assertEqual(self.execute()['status'],'TRAINING_RESTRICTED')
        self.assertEqual(count,3);self.assertIsNone(self.report())

    def test_revocation_before_finalization_blocks_report(self):
        self.add_dataset()
        from nss_base.evaluation_store import make_report
        def mutate(*a,**kw):
            report=make_report(*a,**kw);ok(revoke(self.archive,'train'));return report
        with patch('nss_base.evaluation_store.make_report',side_effect=mutate):
            self.assertEqual(self.execute()['status'],'TRAINING_RESTRICTED')
        self.assertEqual(ok(self.store.audit())['prepared'],1)

    def test_training_member_revocation_also_blocks_validation_read(self):
        self.add_dataset();ok(revoke(self.archive,'train'))
        self.assertEqual(self.execute()['status'],'TRAINING_RESTRICTED')

    def test_tokenizer_substitution_is_not_ignored(self):
        self.add_dataset();self.token_path.write_text('changed')
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_alternate_archive_cannot_be_substituted(self):
        self.add_dataset();self.kw['archive']=ExperienceArchive.create(self.root/'other-archive')
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_wrong_snapshot_hash_rejected(self):
        self.add_dataset();self.plan['development_snapshot']['sha256']='0'*64
        self.assertEqual(self.execute()['status'],'CONSTRAINT_CONFLICT')

    def test_evaluation_does_not_mutate_snapshot_or_experience(self):
        self.add_dataset();before=ok(self.snapshots.inspect('snapshot1'));record=ok(self.archive.inspect('val'))
        ok(self.execute());self.assertEqual(before,ok(self.snapshots.inspect('snapshot1')))
        self.assertEqual(record,ok(self.archive.inspect('val')))
