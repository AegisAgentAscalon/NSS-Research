from contextlib import closing
from copy import deepcopy
import json
import sqlite3
from unittest.mock import patch

from nss_base.evaluation_inputs import capture_inputs, implementation_identity
from nss_base.evaluation_store import EvaluationRuns
from nss_base.evaluationrun001 import plan_for
from nss_base.runtime import ContractError, digest
from evaluation_helpers import EvaluationCase, ok

class EvaluationStoreTests(EvaluationCase):
    def test_prepare_is_durable_but_has_no_verdict_or_receipt(self):
        r=ok(self.store.prepare(self.plan,**self.kw));self.assertEqual(r['state'],'PREPARED');self.assertIsNone(r['verdict'])
        self.store=EvaluationRuns(self.root/'evaluations');self.assertIsNone(self.report())
        self.assertEqual(ok(self.store.audit())['prepared'],1)

    def test_incomplete_run_cannot_be_consumed_as_evidence(self):
        ok(self.store.prepare(self.plan,**self.kw))
        r=self.store.verify_current('run-1',expected_report_sha256='0'*64,**self.kw)
        self.assertEqual(r['status'],'INSUFFICIENT_EVIDENCE')

    def test_exact_retry_returns_immutable_historical_receipt(self):
        first=ok(self.execute());original=self.inspect();second=self.execute()
        self.assertEqual(first,ok(second));self.assertTrue(second['historical']);self.assertTrue(second['replayed'])
        self.assertEqual(original,self.inspect());self.assertEqual(ok(self.store.audit())['runs'],1)

    def test_changed_plan_under_same_run_id_is_rejected(self):
        ok(self.execute());changed=deepcopy(self.plan);changed['reason']='Different attempt'
        self.assertEqual(self.execute(changed)['status'],'CONSTRAINT_CONFLICT')

    def test_exact_historical_retry_does_not_regrant_or_require_current_files(self):
        ok(self.execute());(self.inputs/'suite.json').unlink()
        self.assertTrue(self.execute()['historical']);self.assertEqual(self.verify()['status'],'INSUFFICIENT_EVIDENCE')

    def test_prepared_resume_rejects_modified_inputs(self):
        ok(self.store.prepare(self.plan,**self.kw));(self.inputs/'case_1.json').write_text('{}')
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION');self.assertIsNone(self.report())

    def test_prepared_resume_rejects_changed_code_identity(self):
        ok(self.store.prepare(self.plan,**self.kw));code=implementation_identity();code['sha256']='0'*64
        with patch('nss_base.evaluation_inputs.implementation_identity',return_value=code):
            self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')
        self.assertIsNone(self.report())

    def test_repeated_new_runs_share_computation_not_run_identity(self):
        a=ok(self.execute());p=deepcopy(self.plan);p['run_id']='run-2';b=ok(self.execute(p))
        self.assertNotEqual(a['report_sha256'],b['report_sha256'])
        r2=ok(self.store.inspect('run-2'))['report'];self.assertEqual(self.report()['repeats'],r2['repeats'])

    def test_comparison_same_suite_different_candidate_profiles(self):
        ok(self.execute());p=plan_for(self.inputs,'run-AB',profile='AB');ok(self.execute(p))
        c=self.store.compare('run-1','run-AB');self.assertTrue(c['historical']);self.assertFalse(c['authorizes_deployment'])
        self.assertEqual(ok(c)['left']['receipt']['verdict'],'PASS');self.assertEqual(ok(c)['right']['receipt']['verdict'],'FAIL')

    def test_comparison_changed_threshold_or_budget_refused(self):
        ok(self.execute());p=deepcopy(self.plan);p.update(run_id='budget',max_evaluations=1);ok(self.execute(p))
        self.assertEqual(self.store.compare('run-1','budget')['status'],'INCOMPATIBLE_CONFIGURATION')
        self.edit_suite(lambda s:s.update(minimum_pass_basis_points=0));self.plan['run_id']='threshold';ok(self.execute())
        self.assertEqual(self.store.compare('run-1','threshold')['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_comparison_unfinished_is_not_valid(self):
        ok(self.store.prepare(self.plan,**self.kw));self.assertEqual(self.store.compare('run-1','run-1')['status'],'INSUFFICIENT_EVIDENCE')

    def test_expected_report_hash_is_required_for_current_verification(self):
        ok(self.execute());self.assertEqual(self.store.verify_current('run-1',expected_report_sha256='0'*64,**self.kw)['status'],'CONSTRAINT_CONFLICT')
        self.assertEqual(self.verify()['status'],'SUCCESS')

    def test_altered_report_body_and_digest_fail_closed(self):
        ok(self.execute());self.tamper_report(lambda r:r.update(verdict='FAIL'))
        self.assertEqual(self.store.inspect('run-1')['status'],'VALIDATION_FAILED')
        self.assertEqual(self.store.audit()['status'],'VALIDATION_FAILED')

    def test_recomputed_hashes_do_not_allow_fabricated_observation(self):
        ok(self.execute());self.tamper_report(lambda r:r['trials'][0].update(observed=[123]),rehash=True,receipt=True)
        self.assertEqual(self.store.inspect('run-1')['status'],'VALIDATION_FAILED')

    def test_removed_completion_receipt_rejects_finalized_run(self):
        ok(self.execute())
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute('DELETE FROM receipts')
        self.assertEqual(self.store.audit()['status'],'VALIDATION_FAILED')

    def test_substituted_completion_receipt_rejected(self):
        ok(self.execute())
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute("UPDATE receipts SET body='{}'")
        self.assertEqual(self.store.audit()['status'],'VALIDATION_FAILED')

    def test_orphan_receipt_rejected(self):
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute("INSERT INTO receipts VALUES ('orphan','{}')")
        self.assertEqual(self.store.audit()['status'],'VALIDATION_FAILED')

    def test_raw_material_tamper_rejected(self):
        ok(self.execute())
        with closing(sqlite3.connect(self.store.path)) as db, db:
            m=json.loads(db.execute('SELECT material FROM runs').fetchone()[0]);m['files'][0]['text']='{}'
            db.execute('UPDATE runs SET material=?,material_sha256=?',(json.dumps(m),digest(m)))
        self.assertEqual(self.store.inspect('run-1')['status'],'VALIDATION_FAILED')

    def test_unknown_database_schema_rejected_without_repair(self):
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute("UPDATE metadata SET value='99' WHERE key='schema_version'")
        self.assertEqual(self.store.audit()['status'],'INCOMPATIBLE_CONFIGURATION')
        with self.assertRaises(ContractError):EvaluationRuns(self.root/'evaluations')

    def test_missing_database_open_does_not_create(self):
        path=self.root/'missing'
        with self.assertRaises(ContractError):EvaluationRuns(path)
        self.assertFalse(path.exists())

    def test_corrupt_database_fails_without_truncating(self):
        self.store.path.write_bytes(b'broken sqlite bytes');raw=self.store.path.read_bytes()
        with self.assertRaises(ContractError):EvaluationRuns(self.root/'evaluations')
        self.assertEqual(raw,self.store.path.read_bytes())

    def test_existing_store_is_not_reinitialized(self):
        ok(self.execute())
        with self.assertRaises(ContractError):EvaluationRuns.create(self.root/'evaluations')
        self.assertEqual(self.report()['verdict'],'PASS')

    def test_missing_run_bad_identifier_and_bad_list_limits_are_typed(self):
        self.assertEqual(self.store.inspect('missing')['status'],'INSUFFICIENT_EVIDENCE')
        for value in (None,[],True,'../../bad'):
            self.assertEqual(self.store.inspect(value)['status'],'VALIDATION_FAILED')
        for value in (0,True,1001,'1'):self.assertEqual(self.store.list_runs(limit=value)['status'],'VALIDATION_FAILED')

    def test_pagination_returns_exact_historical_receipts(self):
        ok(self.execute());p=deepcopy(self.plan);p['run_id']='run-2';ok(self.execute(p))
        a=ok(self.store.list_runs(limit=1));self.assertEqual(a[0]['run_id'],'run-1')
        b=ok(self.store.list_runs(after='run-1'));self.assertEqual([r['run_id'] for r in b],['run-2'])

    def test_changed_files_before_finalization_leave_prepared(self):
        original=__import__('nss_base.evaluation_store',fromlist=['make_report']).make_report
        def mutate(*a,**kw):
            report=original(*a,**kw);(self.inputs/'case_2.json').write_text('{}');return report
        with patch('nss_base.evaluation_store.make_report',side_effect=mutate):
            self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')
        self.assertEqual(ok(self.store.audit())['prepared'],1)

    def test_storage_failure_does_not_return_pass(self):
        with patch('nss_base.evaluation_store.capture_inputs',side_effect=OSError('disk')):
            self.assertEqual(self.execute()['status'],'INTERNAL_FAILURE')
        self.assertEqual(ok(self.store.audit())['runs'],0)

    def test_all_result_envelopes_deny_deployment_authority(self):
        result=self.execute();self.assertFalse(result['authorizes_deployment']);self.assertEqual(result['data']['authority'],'NONE')
        for r in (self.store.inspect('run-1'),self.store.audit(),self.store.list_runs(),self.verify(),self.store.inspect('missing')):
            self.assertFalse(r['authorizes_deployment'])
