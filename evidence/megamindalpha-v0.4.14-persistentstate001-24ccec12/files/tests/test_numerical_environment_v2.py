"""A new, stricter recorded execution contract; no post-hoc tolerance relaxation."""
from copy import deepcopy
from pathlib import Path
import os
import subprocess
import sys
from unittest.mock import patch
from qualification_helpers import QualificationCase
from nss_base.neural_backend import deterministic_cpu,environment,evaluate_checkpoints,numerical_environment
from nss_base.neural_contracts import fingerprint,read_document
from nss_base.neural_records import validate_plan
from nss_base.neuralprobe001 import check_current,verify_numerics
from nss_base.neural_data import ProbeData

ROOT=Path(__file__).resolve().parents[1]

class NumericalEnvironmentV2Tests(QualificationCase):
    def setUp(self):
        super().setUp()
        from nss_base.neural_records import ProbeRuns
        self.final=ProbeRuns(self.root/'probe/journal').inspect('probe-001')
        self.data=ProbeData(self.root/'probe/data')
    def test_new_plan_records_backend_execution_contract(self):
        self.assertEqual(self.final['plan']['schema_version'],2)
        n=self.final['plan']['environment']['numerics']
        self.assertEqual(n['score_path'],'reloaded_checkpoints_no_grad_v2')
        self.assertEqual(n['mse_rule'],'torch_fp32_mean_exact')
        self.assertEqual(len(n['cpu_identity_sha256']),64)
        self.assertEqual(len(n['torch_build_sha256']),64)
    def test_fresh_stored_checkpoints_reproduce_all_metrics_exactly(self):
        self.assertEqual(verify_numerics(self.final,self.data)['numerical_trials_recomputed'],1)
    def test_tiny_mse_change_is_still_rejected(self):
        x=deepcopy(self.final);x['report']['trials'][0]['result']['metrics']['AB']['mse']+=1e-12
        self.error('VALIDATION_FAILED',verify_numerics,x,self.data)
    def test_backend_environment_change_blocks_current_reuse(self):
        with patch.dict(os.environ,{'MKL_CBWR':'COMPATIBLE'}):
            self.error('INCOMPATIBLE_CONFIGURATION',check_current,self.final['plan'],self.data)
    def test_backend_build_identity_change_blocks_reuse(self):
        p=deepcopy(self.final['plan']);p['environment']['numerics']['torch_build_sha256']='0'*64
        self.error('INCOMPATIBLE_CONFIGURATION',check_current,p,self.data)
    def test_cpu_identity_change_blocks_reuse(self):
        p=deepcopy(self.final['plan']);p['environment']['numerics']['cpu_identity_sha256']='0'*64
        self.error('INCOMPATIBLE_CONFIGURATION',check_current,p,self.data)
    def test_missing_numerical_field_invalid(self):
        p=deepcopy(self.final['plan']);del p['environment']['numerics']['cpu_capability']
        self.error('VALIDATION_FAILED',validate_plan,p)
    def test_numerical_policy_cannot_switch_to_tolerance(self):
        p=deepcopy(self.final['plan']);p['environment']['numerics']['mse_rule']='within_tolerance'
        self.error('INCOMPATIBLE_CONFIGURATION',validate_plan,p)
    def test_unknown_backend_env_key_invalid(self):
        p=deepcopy(self.final['plan']);p['environment']['numerics']['backend_environment']['ANYTHING']='x'
        self.error('VALIDATION_FAILED',validate_plan,p)
    def test_oversize_env_value_invalid(self):
        p=deepcopy(self.final['plan']);p['environment']['numerics']['backend_environment']['MKL_CBWR']='x'*129
        self.error('VALIDATION_FAILED',validate_plan,p)
    def test_legacy_plan_readable_but_not_current_evidence(self):
        p=deepcopy(self.final['plan']);p['schema_version']=1;p['environment'].pop('numerics')
        self.assertEqual(validate_plan(p),p)
        self.error('INCOMPATIBLE_CONFIGURATION',check_current,p,self.data)
    def test_historical_archive_is_still_legacy_readable(self):
        old=read_document(ROOT/'docs/audits/neuralprobe001/confirmation_report.json')
        self.assertEqual(validate_plan(old['plan'])['schema_version'],1)
    def test_separate_process_replays_fresh_artifacts_exactly(self):
        code='''from pathlib import Path
import sys
from nss_base.neural_records import ProbeRuns
from nss_base.neural_data import ProbeData
from nss_base.neuralprobe001 import verify_numerics
p=Path(sys.argv[1]);print(verify_numerics(ProbeRuns(p/'journal').inspect('probe-001'),ProbeData(p/'data')))'''
        r=subprocess.run([sys.executable,'-c',code,str(self.root/'probe')],cwd=ROOT,capture_output=True,text=True,timeout=90)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr);self.assertIn('SUCCESS',r.stdout)
    def test_separate_process_changed_backend_fails_before_scoring(self):
        code='''from pathlib import Path
import sys
from nss_base.neural_records import ProbeRuns
from nss_base.neural_data import ProbeData
from nss_base.neuralprobe001 import check_current
from nss_base.runtime import ContractError
p=Path(sys.argv[1])
try:check_current(ProbeRuns(p/'journal').inspect('probe-001')['plan'],ProbeData(p/'data'))
except ContractError as e:
 print(e.code);sys.exit(0 if e.code=='INCOMPATIBLE_CONFIGURATION' else 2)
sys.exit(1)'''
        env=dict(os.environ);env['MKL_CBWR']='COMPATIBLE'
        r=subprocess.run([sys.executable,'-c',code,str(self.root/'probe')],cwd=ROOT,env=env,capture_output=True,text=True,timeout=90)
        self.assertEqual(r.returncode,0,r.stdout+r.stderr)
    def test_execution_guard_restores_default_dtype_precision_and_rng(self):
        import torch
        dtype=torch.get_default_dtype();precision=torch.get_float32_matmul_precision();rng=torch.random.get_rng_state()
        try:
            torch.set_default_dtype(torch.float64);torch.set_float32_matmul_precision('medium')
            with deterministic_cpu(99):
                self.assertEqual(torch.get_default_dtype(),torch.float32)
                self.assertEqual(torch.get_float32_matmul_precision(),'highest');torch.randn(3)
            self.assertEqual(torch.get_default_dtype(),torch.float64)
            self.assertEqual(torch.get_float32_matmul_precision(),'medium')
            self.assertTrue(torch.equal(rng,torch.random.get_rng_state()))
        finally:
            torch.set_default_dtype(dtype);torch.set_float32_matmul_precision(precision);torch.random.set_rng_state(rng)
    def test_autocast_disabled_inside_bound_guard(self):
        import torch
        with torch.autocast('cpu',dtype=torch.bfloat16):
            with deterministic_cpu(99):self.assertFalse(torch.is_autocast_enabled('cpu'))
            self.assertTrue(torch.is_autocast_enabled('cpu'))
