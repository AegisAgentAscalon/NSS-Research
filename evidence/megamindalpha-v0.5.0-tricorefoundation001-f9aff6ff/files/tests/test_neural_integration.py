from copy import deepcopy
from contextlib import closing
import json
import os
from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest
try:
    import torch
    from nss_base.neuralprobe001 import (check_current,execute,plan_for,run,verify_numerics)
    HAVE_TORCH=True
except ImportError:HAVE_TORCH=False
from nss_base.ledger import Ledger
from nss_base.neural_contracts import encoded,fingerprint,read_document
from nss_base.neural_data import ProbeData
from nss_base.neural_records import ProbeRuns,validate_plan,validate_report
from nss_base.runtime import ContractError
ROOT=Path(__file__).resolve().parents[1]

class NeuralDataTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name);self.data=ProbeData.create(self.root/'data')
    def test_actual_data_through_snapshot(self):
        self.assertEqual(len(self.data.read('train')),128);self.assertEqual(len(self.data.read('validation')),64);self.assertEqual(len(self.data.read('test')),64)
    def test_restart_same_manifest(self):self.assertEqual(ProbeData(self.root/'data').gate(),self.data.gate())
    def test_training_revocation_blocks(self):
        self.data.revoke_for_test()
        with self.assertRaises(ContractError) as e:self.data.gate()
        self.assertEqual(e.exception.code,'TRAINING_RESTRICTED')
    def test_changed_test_fixture_rejected(self):
        path=self.root/'data/test.json';path.write_bytes(encoded({'pairs':[[1,2]],'codec':'one_hot_16_pair_v1'}))
        with self.assertRaises(ContractError):self.data.gate()
    def test_changed_codec_rejected(self):
        (self.root/'data/codec.json').write_text('{}')
        with self.assertRaises(ContractError):self.data.gate()
    def test_changed_binding_rejected(self):
        (self.root/'data/binding.json').write_text('{}')
        with self.assertRaises(ContractError):self.data.gate()
    def test_create_does_not_overwrite(self):
        with self.assertRaises(ContractError):ProbeData.create(self.root/'data')
    def test_no_private_conversation(self):
        self.assertEqual(set(self.data.gate()['source_hashes']),{'train','validation'})
        self.assertNotIn('Yumi',self.data.read('train'))

@unittest.skipUnless(HAVE_TORCH,'optional PyTorch backend not installed')
class NeuralRunTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.data=ProbeData.create(self.root/'data');self.store=ProbeRuns.create(self.root/'journal');self.ledger=Ledger(self.root/'actions')
        self.p=read_document(ROOT/'fixtures/neuralprobe001/protocol.json')
        self.p.update(seeds=[101],precisions=['fp32'],core_steps=3,overlay_steps=3,max_optimizer_steps=100)
        self.plan=plan_for(self.p,self.data)
    def finish(self):return execute(self.store,'test',self.plan,self.data,self.ledger)
    def test_tiny_training_failure_is_not_software_error(self):
        r=self.finish();self.assertEqual(r['status'],'FINALIZED');self.assertEqual(r['report']['verdict'],'FAIL')
    def test_scores_recomputed_from_weights(self):
        r=self.finish();self.assertEqual(verify_numerics(r,self.data)['numerical_trials_recomputed'],1)
    def test_no_deployment_authority(self):
        r=self.finish();self.assertEqual(r['authority'],'NONE');self.assertEqual(r['receipt']['authority'],'NONE')
    def test_insufficient_budget_inconclusive(self):
        p=deepcopy(self.plan);p['protocol']['max_optimizer_steps']=1
        r=execute(self.store,'low',p,self.data,self.ledger)
        self.assertEqual(r['report']['verdict'],'INCONCLUSIVE');self.assertEqual(r['report']['completed_trials'],0);self.assertEqual(self.ledger.effect_count(),0)
    def test_finalized_retry_history(self):self.assertEqual(self.finish(),self.finish())
    def test_revoked_finalized_retry_does_not_retrain(self):
        r=self.finish();self.data.revoke_for_test();self.assertEqual(self.finish(),r)
        with self.assertRaises(ContractError) as e:verify_numerics(r,self.data)
        self.assertEqual(e.exception.code,'TRAINING_RESTRICTED')
    def test_revoked_new_attempt_rejected(self):
        self.data.revoke_for_test()
        with self.assertRaises(ContractError):self.finish()
        with self.assertRaises(ContractError):self.store.inspect('test')
    def test_resume_revocation_blocked(self):
        self.store.prepare('test',self.plan);self.data.revoke_for_test()
        with self.assertRaises(ContractError):self.finish()
        self.assertEqual(self.store.inspect('test')['status'],'PREPARED')
    def test_changed_plan_rejected(self):
        self.finish();p=deepcopy(self.plan);p['protocol']['learning_rate']=.02
        with self.assertRaises(ContractError):execute(self.store,'test',p,self.data,self.ledger)
    def test_changed_implementation_rejected(self):
        p=deepcopy(self.plan);p['code_sha256']='0'*64
        with self.assertRaises(ContractError):execute(self.store,'test',p,self.data,self.ledger)
    def test_changed_environment_rejected(self):
        p=deepcopy(self.plan);p['environment']['torch']='wrong'
        with self.assertRaises(ContractError):execute(self.store,'test',p,self.data,self.ledger)
    def test_missing_journal_not_recreated(self):
        self.store.path.unlink()
        with self.assertRaises(ContractError):ProbeRuns(self.root/'journal')
        self.assertFalse(self.store.path.exists())
    def test_invalid_run_id(self):
        with self.assertRaises(ContractError):self.store.prepare('../bad',self.plan)
    def test_tampered_report(self):
        r=self.finish()
        with closing(sqlite3.connect(self.store.path)) as db, db:
            body=deepcopy(r['report']);body['verdict']='PASS';db.execute('UPDATE attempts SET report=?',(encoded(body).decode(),))
        with self.assertRaises(ContractError):self.store.inspect('test')
    def test_missing_receipt(self):
        self.finish()
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute('UPDATE attempts SET receipt=NULL')
        with self.assertRaises(ContractError):self.store.inspect('test')
    def test_no_partial_report_in_prepared(self):
        self.store.prepare('test',self.plan)
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute('UPDATE attempts SET report=?',('{}',))
        with self.assertRaises(ContractError):self.store.inspect('test')
    def test_missing_result_fields_typed_failure(self):
        r=self.finish();report=deepcopy(r['report']);del report['trials'][0]['result']['metrics']
        with self.assertRaises(ContractError):validate_report(self.plan,report)
    def test_fabricated_metrics_detected_by_numerical_check(self):
        r=self.finish();r['report']['trials'][0]['result']['metrics']['core']['mse']+=.1
        # A schema/hash report alone is not proof; actual forward replay detects it.
        with self.assertRaises(ContractError):verify_numerics(r,self.data)
    def test_finalized_report_cannot_be_replaced(self):
        r=self.finish();changed=deepcopy(r['report']);changed['data_permission_scope']='replacement'
        with self.assertRaises(ContractError):self.store.finalize('test',changed)
    def test_store_audit(self):self.finish();self.assertEqual(self.store.audit()['attempts'],1)
    def test_protocol_authority_claim_rejected(self):
        p=deepcopy(self.plan);p['authority']='DEPLOY'
        with self.assertRaises(ContractError):validate_plan(p)
    def test_core_package_dtype_change_rejected(self):
        p=deepcopy(self.plan);p['environment']['dtype']='float16'
        with self.assertRaises(ContractError):validate_plan(p)
    def crash(self,point):
        (self.root/'plan.json').write_bytes(encoded(self.plan))
        code='''import sys
from pathlib import Path
from nss_base.neuralprobe001 import execute
from nss_base.neural_contracts import read_document
from nss_base.neural_data import ProbeData
from nss_base.neural_records import ProbeRuns
from nss_base.ledger import Ledger
r=Path(sys.argv[1]);execute(ProbeRuns(r/'journal'),'test',read_document(r/'plan.json'),ProbeData(r/'data'),Ledger(r/'actions'),crash_at=sys.argv[2])
'''
        result=subprocess.run([sys.executable,'-c',code,str(self.root),point],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(result.returncode,79,result.stdout+result.stderr)
        state=self.store.inspect('test')
        self.assertEqual(state['status'],'FINALIZED' if point=='after_commit' else 'PREPARED')
        final=self.finish();self.assertEqual(final['status'],'FINALIZED');self.assertEqual(self.ledger.effect_count(),1)
    def test_process_crash_after_prepare(self):self.crash('after_prepared')
    def test_process_crash_after_neural_training(self):self.crash('after_training')
    def test_process_crash_before_publication_commit(self):self.crash('before_commit')
    def test_process_crash_after_publication_commit(self):self.crash('after_commit')
