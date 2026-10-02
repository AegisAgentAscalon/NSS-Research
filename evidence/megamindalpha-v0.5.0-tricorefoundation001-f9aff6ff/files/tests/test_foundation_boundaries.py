"""Additional boundary regressions for the foundation rather than neural claims."""
from copy import deepcopy
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
import subprocess
import sys
import unittest
from nss_base.foundation_demo import setup, context_for, live_view, SCOPE
from nss_base.foundation_contracts import configuration
from nss_base.foundation_adapters import test_configuration
from nss_base.foundation_store import prepare_state
from nss_base.runtime import ContractError
from nss_base.neural_contracts import fingerprint
from nss_base.research.nbr01 import ClockEstimator


class FoundationBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)/'run'
        self.store,self.service,self.runner,self.adapters,_=setup(self.root)

    def test_oversize_component_state_cannot_partially_commit(self):
        old=self.adapters['SECONDARY'].step
        def oversized(req,state):
            r=old(req,state);r['state']={'blob':'x'*65536};return r
        with patch.object(self.adapters['SECONDARY'],'step',side_effect=oversized):
            with self.assertRaises(ContractError) as e:
                self.runner.run_tick(context_for(self.store,self.service,self.root),operation_id='large',phase='TASK',experience_cutoff=1)
        self.assertEqual(e.exception.code,'BUDGET_EXHAUSTED');self.assertEqual(live_view(self.store,self.root)['states'],{})

    def test_budget_overrun_is_detected_not_claimed_to_be_preempted(self):
        with patch('nss_base.foundation_runner.perf_counter_ns',side_effect=[0,2000000000]):
            with self.assertRaises(ContractError) as e:
                self.runner.run_tick(context_for(self.store,self.service,self.root),operation_id='slow',phase='TASK',experience_cutoff=1)
        self.assertEqual(e.exception.code,'BUDGET_EXHAUSTED')
        self.assertIsNotNone(self.store.foundation_snapshot()['busy'])
        self.assertEqual(self.adapters['SECONDARY'].calls,0)

    def test_current_path_does_not_call_overlay_family_qualification(self):
        with patch('nss_base.generation_store.check_family',side_effect=AssertionError('Legacy overlay path invoked')):
            result=self.runner.run_tick(context_for(self.store,self.service,self.root),operation_id='no-overlays',phase='TASK',experience_cutoff=1)
        self.assertEqual(result['status'],'COMMITTED')

    def test_new_source_path_runs_without_site_packages(self):
        code='''
import sys
from tempfile import TemporaryDirectory
from pathlib import Path
from nss_base.foundation_demo import run_demo
with TemporaryDirectory() as d:
    result=run_demo(Path(d)/'demo')
    if result['status']!='PASS':raise RuntimeError('Demo failed')
if 'torch' in sys.modules or 'numpy' in sys.modules:raise RuntimeError('Optional numeric dependencies imported')
print('STDLIB_ONLY_PASS')
'''
        result=subprocess.run([sys.executable,'-S','-c',code],cwd=Path(__file__).resolve().parents[1],capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,0,result.stdout+result.stderr);self.assertIn('STDLIB_ONLY_PASS',result.stdout)

    def test_malformed_capability_and_source_lists_fail_as_contract_errors(self):
        cfg,_=test_configuration();cfg['components']['PRIMARY']['capabilities']=[{}]
        with self.assertRaises(ContractError) as e:configuration(cfg)
        self.assertEqual(e.exception.code,'VALIDATION_FAILED')
        old=self.adapters['SECONDARY'].step
        def malformed(req,state):
            r=old(req,state);r['source_references']=[{}];return r
        with patch.object(self.adapters['SECONDARY'],'step',side_effect=malformed):
            with self.assertRaises(ContractError):
                self.runner.run_tick(context_for(self.store,self.service,self.root),operation_id='bad-refs',phase='TASK',experience_cutoff=1)
        self.assertEqual(live_view(self.store,self.root)['ticks'],0)

    def test_estimator_boolean_schema_rejected(self):
        state=ClockEstimator('a').checkpoint();state['schema_version']=True
        state['sha256']=fingerprint({k:v for k,v in state.items() if k!='sha256'})
        with self.assertRaises(ContractError):ClockEstimator.restore(state,owner_scope='a')

    def test_wrong_context_owner_never_reads_another_task(self):
        req=context_for(self.store,self.service,self.root)['request'];req['store_id']='wrong-owner'
        result=self.service.build(req)
        self.assertEqual(result['status'],'INCOMPATIBLE_CONFIGURATION');self.assertIsNone(result['data'])


if __name__=='__main__':unittest.main()
