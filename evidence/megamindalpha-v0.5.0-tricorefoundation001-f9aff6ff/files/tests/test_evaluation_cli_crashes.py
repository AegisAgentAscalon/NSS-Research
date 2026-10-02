from copy import deepcopy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from nss_base.evaluation_store import EvaluationRuns
from nss_base.evaluationrun001 import run
from dataset_helpers import revoke
from evaluation_helpers import EvaluationCase, ROOT, ok

class EvaluationCLITests(EvaluationCase):
    def cli(self,*args,expected=0):
        p=subprocess.run([sys.executable,'-m','nss_base.evaluation_cli','--store',str(self.root/'evaluations'),
            '--root',str(self.inputs),*map(str,args)],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(p.returncode,expected,p.stdout+p.stderr);return json.loads(p.stdout)
    def file(self):
        p=self.root/'plan.json';p.write_text(json.dumps(self.plan));return p
    def test_cli_prepare_execute_inspect_current_compare_audit_and_list(self):
        p=self.file();self.cli('prepare',p);ref=ok(self.cli('execute',p))
        self.cli('inspect','run-1');self.cli('verify-current','run-1','--expected-report-sha256',ref['report_sha256'])
        self.cli('compare','run-1','run-1');self.cli('audit');self.cli('list');self.cli('identity')
    def test_cli_nonpass_verdict_is_nonzero_but_report_is_preserved(self):
        self.plan['max_evaluations']=1;r=self.cli('execute',self.file(),expected=2)
        self.assertEqual(r['status'],'SUCCESS');self.assertEqual(r['data']['verdict'],'INCONCLUSIVE')
        self.cli('inspect','run-1')
    def test_cli_failed_verdict_is_not_success_exit(self):
        self.edit_suite(lambda s:s['tests'][0].update(expected=[0]))
        self.assertEqual(self.cli('execute',self.file(),expected=2)['data']['verdict'],'FAIL')
    def test_cli_plan_preparation_does_not_run_or_approve(self):
        p=self.cli('prepare-plan','--run-id','manual','--candidate','candidate/manifest.json','--suite','suite.json',
            '--profile','A','--operator','local-operator','--reason','Explicit development fixture evaluation.')
        self.assertEqual(p['candidate']['profile'],'A');self.assertEqual(ok(self.store.audit())['runs'],0)
        self.assertEqual(p['actor']['kind'],'HUMAN')
    def test_cli_unknown_duplicate_deep_and_nonfinite_input_rejected(self):
        p=self.file()
        for raw in ('{"schema_version":1,"schema_version":1}', '{"x":NaN}', '['*2000+'0'+']'*2000, '{}'):
            p.write_text(raw);self.assertEqual(self.cli('execute',p,expected=2)['status'],'VALIDATION_FAILED')
    def test_cli_current_check_demands_exact_report_hash(self):
        ok(self.execute());self.assertEqual(self.cli('verify-current','run-1','--expected-report-sha256','0'*64,expected=2)['status'],'CONSTRAINT_CONFLICT')
    def test_cli_missing_store_does_not_initialize(self):
        p=subprocess.run([sys.executable,'-m','nss_base.evaluation_cli','--store',str(self.root/'missing'),'audit'],
            cwd=ROOT,capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,2);self.assertFalse((self.root/'missing').exists())
    def test_cli_existing_store_init_refused(self):
        self.assertEqual(self.cli('init',expected=2)['status'],'CONSTRAINT_CONFLICT')
    def test_cli_partial_development_adapter_arguments_rejected(self):
        p=subprocess.run([sys.executable,'-m','nss_base.evaluation_cli','--store',str(self.root/'evaluations'),
            '--root',str(self.inputs),'--snapshots',str(self.root/'snapshots'),'execute',str(self.file())],
            cwd=ROOT,capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,2);self.assertEqual(json.loads(p.stdout)['status'],'VALIDATION_FAILED')

class EvaluationCrashTests(EvaluationCase):
    def crash(self,point):
        (self.root/'plan.json').write_text(json.dumps(self.plan))
        p=subprocess.run([sys.executable,str(ROOT/'tests/evaluation_crash_worker.py'),str(self.root),point],
            cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(p.returncode,77,p.stdout+p.stderr);self.store=EvaluationRuns(self.root/'evaluations')
    def test_crash_after_prepare_resumes_without_partial_result(self):
        self.crash('after_prepare');self.assertEqual(ok(self.store.audit())['prepared'],1)
        self.assertIsNone(self.report());self.assertEqual(ok(self.execute())['verdict'],'PASS')
    def test_crash_after_computation_replays_only_pure_checks(self):
        self.crash('after_compute');self.assertIsNone(self.report());ok(self.execute())
        self.assertEqual(ok(self.store.audit())['finalized'],1)
    def test_crash_between_report_and_receipt_rolls_back_both(self):
        self.crash('after_report_write');self.assertIsNone(self.report());ok(self.execute())
        self.assertEqual(ok(self.store.audit())['runs'],1)
    def test_crash_before_commit_remains_prepared(self):
        self.crash('before_commit');self.assertIsNone(self.report());ok(self.execute())
        self.assertEqual(ok(self.store.audit())['finalized'],1)
    def test_crash_after_commit_returns_same_historical_receipt(self):
        self.crash('after_commit');old=self.inspect();r=self.execute()
        self.assertTrue(r['replayed']);self.assertTrue(r['historical']);self.assertEqual(old,self.inspect())
    def test_crash_resume_after_revocation_blocks(self):
        self.add_dataset();self.crash('after_prepare');ok(revoke(self.archive,'val'))
        self.assertEqual(self.execute()['status'],'TRAINING_RESTRICTED');self.assertIsNone(self.report())
    def test_committed_crash_retry_after_revocation_is_history_only(self):
        self.add_dataset();self.crash('after_commit');ok(revoke(self.archive,'val'));old=self.inspect()
        self.assertTrue(self.execute()['historical']);self.assertEqual(self.verify()['status'],'TRAINING_RESTRICTED')
        self.assertEqual(old,self.inspect())
    def test_crash_resume_rejects_substituted_plan(self):
        self.crash('after_prepare');self.plan['repeats']=3
        self.assertEqual(self.execute()['status'],'CONSTRAINT_CONFLICT');self.assertIsNone(self.report())
    def test_unknown_fault_point_is_rejected_without_changes(self):
        self.assertEqual(self.store.execute(self.plan,root=self.inputs,fault_at='anything')['status'],'VALIDATION_FAILED')
        self.assertEqual(ok(self.store.audit())['runs'],0)

class EvaluationIntegrationTests(unittest.TestCase):
    def test_connected_pipeline_preserves_state_and_revocation(self):
        with TemporaryDirectory() as root:
            r=run(root)
        self.assertEqual(r['status'],'SUCCESS');self.assertEqual(r['committed_mock_effects'],1)
        self.assertTrue(r['runtime_checkpoint_unchanged']);self.assertTrue(r['historical_report_unchanged'])
        self.assertEqual([x['verdict'] for x in r['results']],['PASS','FAIL','INCONCLUSIVE'])
        self.assertEqual(r['verify_after_revocation'],'TRAINING_RESTRICTED');self.assertTrue(r['repeat_reproducible'])
        self.assertFalse(r['authorizes_deployment']);self.assertEqual(r['audit']['runs'],3)
