from contextlib import closing
from copy import deepcopy
from pathlib import Path
import sqlite3
import subprocess
import sys
from unittest.mock import patch
from learner_helpers import LearnerCase, CLOCK
from nss_base.learner_contracts import numerical_input, operation_id
from nss_base.learner_store import _reduce
from nss_base.boundedlearnercoordinator001 import OPERATORS,plan_from_reviewed_data
from nss_base.neural_contracts import encoded, fingerprint
from nss_base.runtime import ContractError
ROOT=Path(__file__).resolve().parents[1]


class LearningRecoveryTests(LearnerCase):
    def test_process_crash_boundaries_preserve_dispatch_rules(self):
        safe=('after_snapshot_dispatch','after_snapshot_sealed','after_training_sealed','after_train_receipt',
            'after_evaluation_sealed','after_evaluate_receipt','before_propose_commit','after_propose_commit')
        uncertain=('after_train_dispatch','after_training_prepared','after_training_computed',
            'after_evaluate_dispatch','after_evaluation_prepared','after_evaluation_computed')
        for point in (*safe,*uncertain):
            with self.subTest(point=point):
                self.setUp();self.ready()
                cfg=self.root/'owners.json';cfg.write_bytes(encoded(self.config));plan=self.root/'plan.json';plan.write_bytes(encoded(self.plan))
                p=subprocess.run([sys.executable,str(ROOT/'tests/learner_crash_worker.py'),str(cfg),str(plan),point,str(CLOCK)],
                    cwd=ROOT,capture_output=True,text=True,timeout=90)
                self.assertEqual(p.returncode,83,p.stdout+p.stderr)
                if point in uncertain:
                    before=self.co.training.audit()['attempts']
                    with patch('nss_base.learner_recipe.train_candidate',side_effect=AssertionError('blind retraining')):
                        self.error('RECOVERY_REQUIRED',self.co.advance,'learn-001',caller_id='learner-worker')
                    self.assertEqual(self.co.training.audit()['attempts'],before)
                else:
                    forbid_training=point not in ('after_snapshot_dispatch','after_snapshot_sealed')
                    if forbid_training:
                        with patch('nss_base.learner_recipe.train_candidate',side_effect=AssertionError('completed work repeated')):
                            result=self.co.advance('learn-001',caller_id='learner-worker')
                    else:result=self.co.advance('learn-001',caller_id='learner-worker')
                    self.assertEqual(result['status'],'PROPOSED')
                    self.assertEqual(self.co.training.audit()['attempts'],1)

    def test_plan_publication_survives_process_death(self):
        cfg=self.root/'owners.json';cfg.write_bytes(encoded(self.config));plan=self.root/'plan.json';plan.write_bytes(encoded(self.plan))
        p=subprocess.run([sys.executable,str(ROOT/'tests/learner_crash_worker.py'),str(cfg),str(plan),'after_plan_commit',str(CLOCK)],
            cwd=ROOT,capture_output=True,text=True,timeout=90)
        self.assertEqual(p.returncode,83,p.stderr)
        self.assertEqual(self.co.cycles.inspect('learn-001')['plan'],self.plan)
        self.assertEqual(self.co.training.audit()['attempts'],0)

    def test_unresolved_dispatch_can_be_abandoned_not_implicitly_retried(self):
        self.ready();self.co.cycles.begin('learn-001','SNAPSHOT',at=CLOCK)
        s=self.co.snapshots.build(self.plan['snapshot_request'],archive=self.co.archive,tokenizer_path=self.co.tokenizer_path)['data']
        self.co.cycles.complete('learn-001','SNAPSHOT',s,at=CLOCK);self.co.cycles.begin('learn-001','TRAIN',at=CLOCK)
        self.error('RECOVERY_REQUIRED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.co.cycles.cancel('learn-001',actor_id='human-operator',reason='abandon uncertain attempt',at=CLOCK)
        p=plan_from_reviewed_data(self.co,cycle_id='learn-002',steps=180)
        self.co.prepare(p);self.co.cycles.approve('learn-002',approver_id='human-operator',expires_at=CLOCK+600,at=CLOCK)
        self.assertEqual(self.co.advance('learn-002',caller_id='learner-worker')['status'],'PROPOSED')
        self.assertEqual(self.co.cycles.inspect('learn-001')['status'],'CANCELLED')

    def test_revocation_after_sealed_training_blocks_evaluation(self):
        self.ready();original=self.co.cycles.complete
        def complete(cycle,phase,reference,**kw):
            result=original(cycle,phase,reference,**kw)
            if phase=='TRAIN':self.data.revoke_for_test()
            return result
        with patch.object(self.co.cycles,'complete',side_effect=complete):
            self.error('TRAINING_RESTRICTED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.candidate()['status'],'FINALIZED');self.assertEqual(self.co.evaluations.audit()['attempts'],0)
        self.error('TRAINING_RESTRICTED',self.co.advance,'learn-001',caller_id='learner-worker')

    def test_expiry_during_training_stops_without_final_report(self):
        self.ready();real=self.co._gate;calls=0
        def gate(*a,**kw):
            nonlocal calls
            calls+=1
            if calls==8:self.co.clock=lambda:CLOCK+601
            return real(*a,**kw)
        with patch.object(self.co,'_gate',side_effect=gate):
            self.error('AUTHORIZATION_DENIED',self.co.advance,'learn-001',caller_id='learner-worker')
        self.assertEqual(self.candidate()['status'],'PREPARED');self.assertEqual(self.co.evaluations.audit()['attempts'],0)

    def test_durable_journal_chain_tampering_is_rejected(self):
        self.ready()
        with closing(sqlite3.connect(self.co.cycles.path)) as db, db:db.execute("UPDATE events SET body='{}' WHERE seq=1")
        self.error('VALIDATION_FAILED',self.co.cycles.inspect,'learn-001')

    def test_missing_candidate_owner_receipt_blocks_current_use(self):
        self.complete()
        with closing(sqlite3.connect(self.co.training.path)) as db, db:db.execute('DELETE FROM attempts')
        self.error('INSUFFICIENT_EVIDENCE',self.co.check_proposal,'learn-001')
        self.assertEqual(self.co.cycles.inspect('learn-001')['status'],'PROPOSED')

    def test_wrong_candidate_store_format_is_not_probe_evidence(self):
        from nss_base.neural_records import ProbeRuns
        import shutil
        other=self.root/'wrong-owner';other.mkdir()
        shutil.copy2(self.co.training.path,other/'neural_runs.sqlite3')
        self.error('INCOMPATIBLE_CONFIGURATION',ProbeRuns,other)

    def test_malformed_journal_events_return_typed_failure(self):
        plan_event={'kind':'PLAN','at':CLOCK,'body':self.plan}
        for body in [None,{'cycle_id':[]},{'cycle_id':'missing'},{'cycle_id':'learn-001','phase':[]}]:
            with self.subTest(body=body):
                with self.assertRaises(ContractError):_reduce(OPERATORS,[plan_event,{'kind':'START','at':CLOCK,'body':body}])

    def test_incomplete_candidate_cannot_reenter_training_owner(self):
        self.ready();s=self.co.snapshots.build(self.plan['snapshot_request'],archive=self.co.archive,tokenizer_path=self.co.tokenizer_path)['data']
        np=numerical_input(self.plan,s);rid=operation_id(self.plan,'TRAIN');self.co.training.prepare(rid,np)
        from nss_base.learner_recipe import train_candidate
        self.error('RECOVERY_REQUIRED',train_candidate,self.co.training,rid,np,artifacts={},train_pairs=[],gate=lambda:None)

    def test_swapped_report_between_cycles_rejected(self):
        self.complete();e=deepcopy(self.evaluation());t=self.candidate();e['plan']['learning_plan']['cycle_id']='different'
        from nss_base.learner_recipe import verify_candidate
        self.error('CONSTRAINT_CONFLICT',verify_candidate,e,t,gate=lambda:None)
