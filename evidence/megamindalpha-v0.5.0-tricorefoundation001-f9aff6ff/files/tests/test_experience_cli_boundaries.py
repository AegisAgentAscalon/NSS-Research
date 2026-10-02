import ast
from contextlib import contextmanager
from hashlib import sha256
import importlib.util
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from nss_base.experience_store import ExperienceArchive
from nss_base.experiencearchive001 import run
from test_experiencearchive001 import capture,evidence,HUMAN,AT,sql

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('exp_boundary_checker',ROOT/'tools/check_dependencies.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)

class ExtraAuditTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.store=ExperienceArchive.create(self.root/'archive')

    def test_purpose_validation_never_leaks_type_errors(self):
        h=self.store.capture(capture())['data']['reference']['sha256']
        for value in ([],{},None,False,3,'unknown'):
            result=self.store.read_for_use('exp1',purpose=value,expected_revision_hash=h)
            self.assertEqual(result['status'],'VALIDATION_FAILED',result)

    def test_malformed_public_inputs_return_typed_failures(self):
        values=[None,False,0,1.5,'',[],{}, {'payload':[]}, {'action':[]}, {'action':{}}]
        for method in (self.store.capture,self.store.change,self.store.revoke_source):
            for value in values:
                with self.subTest(method=method.__name__,value=value):
                    self.assertEqual(method(value)['status'],'VALIDATION_FAILED')

    def test_unknown_evidence_fields_and_duplicate_added_sources_rejected(self):
        h=self.store.capture(capture())['data']['reference']['sha256'];e=evidence('e2','new')
        cmd={'schema_version':1,'operation_id':'m1','experience_id':'exp1','expected_revision_hash':h,
            'actor':HUMAN,'at':AT,'reason':'review','action':'CORRECT','payload':{
                'statement':{'text':'new claim','uncertainty':'LOW','support_ids':['e2']},'evidence':[e,e]}}
        self.assertEqual(self.store.change(cmd)['status'],'VALIDATION_FAILED')
        cmd['payload']['evidence']=[dict(e,extra='bad')]
        self.assertEqual(self.store.change(cmd)['status'],'VALIDATION_FAILED')

    def test_corrupt_revocation_evidence_fails_closed(self):
        self.store.capture(capture())
        req={'schema_version':1,'operation_id':'r1','actor':HUMAN,'at':AT,
            'reason':'revoke','permission_ref':'p1','source_sha256':evidence()['sha256'],'purpose':'retrieval'}
        self.store.revoke_source(req)
        with sql(self.store.path) as db:db.execute("UPDATE revocations SET purpose='training'")
        self.assertEqual(self.store.audit()['status'],'VALIDATION_FAILED')

    def test_corrupt_database_file_open_is_typed_and_not_repaired(self):
        self.store.path.write_bytes(b'not a database')
        with self.assertRaises(Exception) as cm:ExperienceArchive(self.root/'archive')
        self.assertEqual(getattr(cm.exception,'code',None),'RECOVERY_REQUIRED')
        self.assertEqual(self.store.path.read_bytes(),b'not a database')

    def test_missing_evidence_cannot_be_used_even_with_review(self):
        self.store.capture(capture())
        with sql(self.store.path) as db:db.execute('DELETE FROM evidence')
        self.assertEqual(self.store.inspect('exp1')['status'],'INSUFFICIENT_EVIDENCE')

    def test_capture_size_bounds_fail_before_storage(self):
        req=capture();req['evidence']=[evidence(f'e{i}','x'*262144) for i in range(17)]
        req['statement']['support_ids']=['e0']
        self.assertEqual(self.store.capture(req)['status'],'VALIDATION_FAILED')
        self.assertEqual(self.store.audit()['data']['records'],0)

    def test_readonly_operation_lookup_is_bound_and_side_effect_free(self):
        initial=self.store.capture(capture());before=self.store.audit()['data']
        result=self.store.operation_receipt('capture:exp1')
        self.assertEqual(result['status'],'SUCCESS');self.assertEqual(result['data']['result_sha256'],initial['data']['reference']['sha256'])
        self.assertEqual(self.store.operation_receipt('missing')['data'],None)
        self.assertEqual(self.store.audit()['data'],before)

    def test_revision_budget_has_explicit_failure(self):
        # Unit-test boundary on pure reducer; avoids manufacturing 512 real reviews.
        from nss_base.experience_contracts import next_revision
        from nss_base.runtime import ContractError,digest
        s=self.store.capture(capture())['data']['record'];s['revision']=511;s['parent_hash']='a'*64
        cmd={'experience_id':'exp1','expected_revision_hash':digest(s),'action':'REVIEW',
            'payload':{'decision':'APPROVED'},'actor':HUMAN,'at':AT,'reason':'review'}
        with self.assertRaises(ContractError) as cm:next_revision(s,cmd)
        self.assertEqual(cm.exception.code,'BUDGET_EXHAUSTED')

    def test_demo_is_connected_and_training_remains_restricted(self):
        report=run(self.root/'demo')
        self.assertEqual(report['status'],'SUCCESS');self.assertTrue(report['runtime_checkpoint_unchanged'])
        self.assertEqual(report['committed_mock_effects'],1)
        self.assertEqual(report['training_without_permission'],'TRAINING_RESTRICTED')
        self.assertEqual(report['retrieval_after_source_revocation'],'TRAINING_RESTRICTED')

    def test_new_modules_obey_import_map(self):
        self.assertEqual(checker.check(ROOT),[])

    def test_store_to_runtime_reachthrough_import_is_forbidden(self):
        with TemporaryDirectory() as temp:
            root=Path(temp);shutil.copytree(ROOT/'nss_base',root/'nss_base',ignore=shutil.ignore_patterns('__pycache__'))
            (root/'spec').mkdir();shutil.copy(ROOT/'spec/python_dependencies.json',root/'spec/python_dependencies.json')
            f=root/'nss_base/experience_store.py';f.write_text(f.read_text()+'\nfrom .publication import RecoveryStore\n')
            self.assertTrue(any('forbidden' in x for x in checker.check(root)))

    def test_intake_has_no_direct_sql_or_runtime_mutator_calls(self):
        text=(ROOT/'nss_base/experience_intake.py').read_text();tree=ast.parse(text)
        forbidden={'connect','execute','executemany','perform','publish_initial','publish_task_revision','prepare','stage','publish'}
        for node in ast.walk(tree):
            if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute):
                self.assertNotIn(node.func.attr,forbidden)

class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.path=self.root/'archive';self.request=self.root/'capture.json';self.request.write_text(json.dumps(capture()))

    def call(self,*args):
        result=subprocess.run([sys.executable,'-m','nss_base.experience_cli','--archive',str(self.path),*args],
            cwd=ROOT,text=True,capture_output=True,timeout=10)
        return result,json.loads(result.stdout)

    def test_cli_manual_review_workflow_and_explicit_training_restriction(self):
        rc,data=self.call('init');self.assertEqual(rc.returncode,0,data)
        self.assertEqual(self.call('capture',str(self.request))[0].returncode,0)
        rc,cmd=self.call('prepare-review','exp1','--decision','APPROVED','--reviewer','local:operator',
            '--operation-id','human-review:1','--reason','I checked the fixture source.','--at',AT)
        self.assertEqual(rc.returncode,0,cmd)
        # Preparing a review does not mutate the record.
        self.assertEqual(self.call('show','exp1')[1]['data']['record']['review']['status'],'PENDING_REVIEW')
        review=self.root/'review.json';review.write_text(json.dumps(cmd))
        result=self.call('apply',str(review));self.assertEqual(result[0].returncode,0,result)
        h=result[1]['data']['reference']['sha256']
        rc,data=self.call('use','exp1','--purpose','training','--expected',h)
        self.assertEqual(rc.returncode,2);self.assertEqual(data['status'],'TRAINING_RESTRICTED')
        self.assertEqual(self.call('history','exp1')[0].returncode,0)
        self.assertEqual(self.call('list')[0].returncode,0)
        self.assertEqual(self.call('audit')[0].returncode,0)

    def test_cli_rejects_duplicate_fields_and_nonfinite_values(self):
        self.call('init')
        for text in ('{"schema_version":1,"schema_version":1}', '{"x":NaN}'):
            self.request.write_text(text);rc,data=self.call('capture',str(self.request))
            self.assertEqual(rc.returncode,2);self.assertEqual(data['status'],'VALIDATION_FAILED')

    def test_cli_does_not_initialize_on_read(self):
        rc,data=self.call('list');self.assertEqual(rc.returncode,2);self.assertEqual(data['status'],'RECOVERY_REQUIRED')
        self.assertFalse(self.path.exists())

    def test_cli_deep_and_oversized_requests_fail_typed(self):
        self.call('init')
        for text in ('['*2000+']'*2000,' '* (4*1024*1024+1)):
            self.request.write_text(text);rc,data=self.call('capture',str(self.request))
            self.assertEqual(rc.returncode,2);self.assertEqual(data['status'],'VALIDATION_FAILED')
