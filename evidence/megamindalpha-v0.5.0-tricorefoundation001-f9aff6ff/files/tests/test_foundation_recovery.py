"""Actual process-exit recovery and cross-process worker exclusion tests."""
from pathlib import Path
from tempfile import TemporaryDirectory
import os
import subprocess
import sys
import time
import unittest
from nss_base.foundation_demo import setup, context_for, live_view, SCOPE
from nss_base.runtime import ContractError
from nss_base.generation_store import Generations

ROOT=Path(__file__).resolve().parents[1]
CRASH_SCRIPT='''
from pathlib import Path
import sys
from nss_base.generation_store import Generations
from nss_base.foundation_adapters import test_configuration
from nss_base.foundation_runner import CycleRunner
from nss_base.foundation_context import FoundationContextSource
from nss_base.context_service import ContextService
from nss_base.foundation_demo import context_for
root=Path(sys.argv[1]);store=Generations(root/'generations')
_,adapters=test_configuration(wrong_validator=True)
service=ContextService(FoundationContextSource(store,evidence_root=root/'evidence'))
runner=CycleRunner(store,service,adapters)
runner.run_tick(context_for(store,service,root),operation_id='crash-tick',phase='LEARN',experience_cutoff=1,fault_at=sys.argv[2])
'''


class FoundationRecoveryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'run'
        self.store,self.service,self.runner,self.adapters,_=setup(self.root)

    def crash(self,point):
        result=subprocess.run([sys.executable,'-c',CRASH_SCRIPT,str(self.root),point],cwd=ROOT,
            env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True,timeout=20)
        self.assertEqual(result.returncode,83,result.stdout+result.stderr)

    def interrupted(self,point):
        before=live_view(self.store,self.root);self.crash(point)
        reopened=Generations(self.root/'generations')
        self.assertEqual(live_view(reopened,self.root),before)
        self.assertIsNotNone(reopened.foundation_snapshot()['busy'])
        recovered=reopened.foundation_recover(caller_id='builder',reason='Crashed test subprocess has exited')
        self.assertEqual(recovered['status'],'INTERRUPTED');self.assertFalse(recovered['external_effects_replayed'])
        result=self.runner.run_tick(context_for(self.store,self.service,self.root),operation_id='resume',phase='LEARN',experience_cutoff=1)
        self.assertEqual(result['states']['PRIMARY']['payload']['calls'],2)
        self.assertEqual(result['candidate_states']['SECONDARY']['payload']['calls'],1)

    def test_exit_after_reservation(self):self.interrupted('after_begin')
    def test_exit_after_primary_before_secondary(self):self.interrupted('after_primary_pre')
    def test_exit_after_secondary_learning_step(self):self.interrupted('after_auxiliary')
    def test_exit_before_atomic_complete_commit(self):self.interrupted('before_f_complete_commit')

    def test_exit_after_commit_returns_history_without_second_execution(self):
        packet=context_for(self.store,self.service,self.root);self.crash('after_complete_commit')
        view=live_view(self.store,self.root);self.assertEqual(view['ticks'],1)
        self.assertIsNone(self.store.foundation_snapshot()['busy'])
        result=self.runner.run_tick(packet,operation_id='crash-tick',phase='LEARN',experience_cutoff=1)
        self.assertEqual(result['status'],'ALREADY_COMMITTED');self.assertEqual(result['model_calls'],0)
        self.assertEqual(sum(a.calls for a in self.adapters.values()),0)

    def test_recovery_cannot_be_claimed_by_another_operator(self):
        self.crash('after_begin')
        with self.assertRaises(ContractError) as e:self.store.foundation_recover(caller_id='reviewer',reason='Wrong caller')
        self.assertEqual(e.exception.code,'AUTHORIZATION_DENIED')
        self.assertIsNotNone(self.store.foundation_snapshot()['busy'])

    def test_cross_process_lock_cannot_be_stolen_before_worker_exit(self):
        ready=self.root/'worker-ready'
        script='''
from pathlib import Path
import sys,time
from nss_base.foundation_lock import worker_lock
root=Path(sys.argv[1])
with worker_lock(root/'generations'):
    (root/'worker-ready').write_text('ready')
    time.sleep(15)
'''
        child=subprocess.Popen([sys.executable,'-c',script,str(self.root)],cwd=ROOT,
            stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
        try:
            deadline=time.monotonic()+5
            while not ready.exists() and time.monotonic()<deadline and child.poll() is None:time.sleep(.01)
            self.assertTrue(ready.exists())
            with self.assertRaises(ContractError) as e:self.store.foundation_recover(caller_id='builder',reason='Cannot steal live lock')
            self.assertEqual(e.exception.code,'CONSTRAINT_CONFLICT')
            with self.assertRaises(ContractError) as e:
                self.runner.run_tick(context_for(self.store,self.service,self.root),operation_id='parallel',phase='REFLECT',experience_cutoff=1)
            self.assertEqual(e.exception.code,'CONSTRAINT_CONFLICT')
        finally:
            child.terminate();child.communicate(timeout=5)
        self.assertEqual(self.store.foundation_recover(caller_id='builder',reason='Worker stopped')['status'],'IDLE')


if __name__=='__main__':unittest.main()
