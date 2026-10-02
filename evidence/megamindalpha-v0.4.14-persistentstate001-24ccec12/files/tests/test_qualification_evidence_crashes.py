from contextlib import closing
from copy import deepcopy
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from unittest.mock import patch

from qualification_helpers import QualificationCase,AT,OPERATORS,review_for
from nss_base.neural_contracts import encoded,fingerprint,read_document
from nss_base.neural_data import ProbeData
from nss_base.neural_records import ProbeRuns
from nss_base.qualification_neural import NeuralEvidence
from nss_base.qualification_store import Qualifications

ROOT=Path(__file__).resolve().parents[1]


class QualificationEvidenceTests(QualificationCase):
    def test_actual_failed_neural_run_cannot_qualify(self):
        from nss_base.neuralprobe001 import run,DEFAULT
        p=read_document(DEFAULT);p.update(seeds=[101],precisions=['fp32'],core_steps=1,overlay_steps=1)
        result=run(self.root/'failed',p,withdraw=False);self.assertEqual(result['verdict'],'FAIL')
        source=NeuralEvidence(self.root/'failed/journal',self.root/'failed/data')
        r=source.propose(run_id='probe-001',seed=101,precision='fp32',scope={'kind':'PROFILE','profile':'CORE'},
            producer_id='fixture-builder',request_id='failed',at=AT)
        self.q.prepare(r,source=source);out=self.q.decide(review_for(r),source=source)
        self.assertEqual(out['verdict'],'REJECTED');self.assertIsNone(out['certificate_sha256'])
    def test_actual_inconclusive_neural_run_has_no_candidate_evidence(self):
        from nss_base.neuralprobe001 import run,DEFAULT
        p=read_document(DEFAULT);p.update(seeds=[101],precisions=['fp32'],max_optimizer_steps=1)
        result=run(self.root/'inconclusive',p,withdraw=False);self.assertEqual(result['verdict'],'INCONCLUSIVE')
        source=NeuralEvidence(self.root/'inconclusive/journal',self.root/'inconclusive/data')
        self.error('INSUFFICIENT_EVIDENCE',source.propose,run_id='probe-001',seed=101,precision='fp32',
            scope={'kind':'PROFILE','profile':'CORE'},producer_id='fixture-builder',request_id='inconclusive',at=AT)
    def test_prepared_upstream_journal_is_not_evidence(self):
        prior=ProbeRuns(self.root/'probe/journal').inspect('probe-001')
        upstream=ProbeRuns.create(self.root/'prepared-source');upstream.prepare('pending',prior['plan'])
        source=NeuralEvidence(self.root/'prepared-source',self.root/'probe/data')
        self.error('INSUFFICIENT_EVIDENCE',source.view,'pending',101,'fp32')
    def test_fabricated_score_recomputed_not_trusted(self):
        prior=ProbeRuns(self.root/'probe/journal').inspect('probe-001')
        report=deepcopy(prior['report']);report['trials'][0]['result']['metrics']['core']['mse']+=0.0001
        upstream=ProbeRuns.create(self.root/'forged-source');upstream.prepare('forged',prior['plan'])
        upstream.finalize('forged',report)
        source=NeuralEvidence(self.root/'forged-source',self.root/'probe/data')
        r=source.propose(run_id='forged',seed=101,precision='fp32',scope={'kind':'PROFILE','profile':'CORE'},
            producer_id='fixture-builder',request_id='forged',at=AT)
        self.q.prepare(r,source=source)
        self.error('VALIDATION_FAILED',self.q.decide,review_for(r),source=source)
        self.assertEqual(self.q.inspect('forged')['status'],'PREPARED')
    def test_changed_checkpoint_fails_current_use(self):
        with closing(sqlite3.connect(self.root/'probe/journal/neural_runs.sqlite3')) as db:
            row=db.execute("SELECT report FROM attempts WHERE id='probe-001'").fetchone()
            obj=json.loads(row[0]);obj['trials'][0]['artifacts']['core']['tensors']['w1']['values'][0]+=1
            db.execute("UPDATE attempts SET report=? WHERE id='probe-001'",(json.dumps(obj),));db.commit()
        self.error('VALIDATION_FAILED',self.use,'core')
    def test_revocation_after_verification_blocks_publish(self):
        r=self.req();self.q.prepare(r,source=self.source);original=NeuralEvidence.verify
        def withdraw(source,req):
            result=original(source,req);ProbeData(source.data_path).revoke_for_test();return result
        with patch.object(NeuralEvidence,'verify',withdraw):
            self.error('TRAINING_RESTRICTED',self.q.decide,review_for(r),source=self.source)
        self.assertEqual(self.q.inspect('new')['status'],'PREPARED')
    def test_prerequisite_revoked_while_checking_blocks_publish(self):
        r=self.req(profile='A',parents=['core']);self.q.prepare(r,source=self.source);original=NeuralEvidence.verify
        def withdraw(source,req):
            result=original(source,req);self.q.revoke(self.revoke());return result
        with patch.object(NeuralEvidence,'verify',withdraw):
            self.error('AUTHORIZATION_DENIED',self.q.decide,review_for(r),source=self.source)
        self.assertEqual(self.q.inspect('new')['status'],'PREPARED')
    def test_changed_neural_ecid_report_is_rejected(self):
        prior=ProbeRuns(self.root/'probe/journal').inspect('probe-001')
        report=deepcopy(prior['report']);report['trials'][0]['recovery']['ecids']['A']='a'*64
        upstream=ProbeRuns.create(self.root/'wrong-ecid');upstream.prepare('bad',prior['plan']);upstream.finalize('bad',report)
        self.error('VALIDATION_FAILED',NeuralEvidence(self.root/'wrong-ecid',self.root/'probe/data').view,'bad',101,'fp32')


class QualificationJournalTests(QualificationCase):
    def sql(self,statement,params=()):
        with closing(sqlite3.connect(self.q.path)) as db:
            db.execute(statement,params);db.commit()
    def test_deleted_middle_event_fails_closed(self):
        self.sql('DELETE FROM events WHERE seq=2');self.error('VALIDATION_FAILED',self.q.audit)
    def test_deleted_tail_revocation_cannot_restore_use(self):
        self.q.revoke(self.revoke());self.sql('DELETE FROM events WHERE seq=(SELECT MAX(seq) FROM events)')
        self.error('VALIDATION_FAILED',self.use,'core')
    def test_repointed_head_is_rejected(self):
        self.sql('UPDATE meta SET head=?',('0'*64,));self.error('VALIDATION_FAILED',self.q.audit)
    def test_changed_role_manifest_is_rejected(self):
        self.sql("UPDATE meta SET manifest='{}'");self.error('VALIDATION_FAILED',self.q.audit)
    def test_missing_meta_is_rejected(self):
        self.sql('DELETE FROM meta');self.error('VALIDATION_FAILED',self.q.audit)
    def test_corrupt_json_event_is_rejected(self):
        self.sql("UPDATE events SET body='not-json' WHERE seq=1");self.error('VALIDATION_FAILED',self.q.audit)
    def test_duplicate_key_event_is_rejected(self):
        self.sql('UPDATE events SET body=? WHERE seq=1',('{"schema_version":1,"schema_version":1}',))
        self.error('VALIDATION_FAILED',self.q.audit)
    def test_wrong_event_hash_is_rejected(self):
        self.sql('UPDATE events SET sha256=? WHERE seq=1',('f'*64,));self.error('VALIDATION_FAILED',self.q.audit)
    def test_new_event_without_head_update_is_rejected(self):
        self.sql("INSERT INTO events VALUES(100,'REVOKE','{}',?,?)",('0'*64,'0'*64));self.error('VALIDATION_FAILED',self.q.audit)
    def test_journal_event_budget_enforced(self):
        with patch('nss_base.qualification_store.MAX_EVENTS',8):
            self.error('BUDGET_EXHAUSTED',self.q.prepare,self.req(),source=self.source)
    def test_journal_total_byte_budget_enforced(self):
        with patch('nss_base.qualification_store.MAX_HISTORY_BYTES',1):
            self.error('BUDGET_EXHAUSTED',self.q.audit)
    def test_dropped_table_is_typed_recovery_failure(self):
        self.sql('DROP TABLE events');self.error('RECOVERY_REQUIRED',self.q.audit)


    def test_over_nested_stored_event_is_typed_failure(self):
        self.sql('UPDATE events SET body=? WHERE seq=1',('['*1500+'0'+']'*1500,))
        self.error('VALIDATION_FAILED',self.q.audit)
    def test_nontext_stored_event_is_typed_failure(self):
        self.sql('UPDATE events SET body=? WHERE seq=1',(sqlite3.Binary(b'{}'),))
        self.error('VALIDATION_FAILED',self.q.audit)
    def test_oversized_stored_event_is_typed_failure(self):
        self.sql('UPDATE events SET body=? WHERE seq=1',('x'*(2*1024*1024+1),))
        self.error('BUDGET_EXHAUSTED',self.q.audit)


class QualificationCrashTests(QualificationCase):
    def worker(self,op,document,point):
        path=self.root/'operation.json';path.write_bytes(encoded(document))
        code='''from pathlib import Path
import sys
from nss_base.neural_contracts import read_document
from nss_base.qualification_store import Qualifications
from nss_base.qualification_neural import NeuralEvidence
r=Path(sys.argv[1]);q=Qualifications(r/'q');s=NeuralEvidence(r/'probe/journal',r/'probe/data')
x=read_document(r/'operation.json');method=getattr(q,sys.argv[2]);kw={'fault_at':sys.argv[3]}
if sys.argv[2]!='revoke':kw['source']=s
method(x,**kw)
'''
        result=subprocess.run([sys.executable,'-c',code,str(self.root),op,point],cwd=ROOT,capture_output=True,text=True,timeout=60)
        self.assertEqual(result.returncode,79,result.stdout+result.stderr)
        self.q=Qualifications(self.root/'q');self.q.audit()
    def decision_crash(self,point,committed):
        r=self.req();self.q.prepare(r,source=self.source);d=review_for(r)
        self.worker('decide',d,point)
        self.assertEqual(self.q.inspect('new')['status'],'QUALIFIED' if committed else 'PREPARED')
        result=self.q.decide(d,source=self.source)
        self.assertEqual(result['verdict'],'QUALIFIED');self.assertEqual(result['historical'],committed)
    def test_crash_after_prepare(self):
        r=self.req();self.worker('prepare',r,'after_prepare')
        self.assertEqual(self.q.inspect('new')['status'],'PREPARED')
        self.assertEqual(self.q.decide(review_for(r),source=self.source)['verdict'],'QUALIFIED')
    def test_crash_after_verification(self):self.decision_crash('after_verification',False)
    def test_crash_before_decision_commit(self):self.decision_crash('before_decision_commit',False)
    def test_crash_after_decision_commit(self):self.decision_crash('after_decision_commit',True)
    def test_crash_before_revocation_commit(self):
        r=self.revoke();self.worker('revoke',r,'before_revocation_commit')
        self.assertEqual(self.use('core')['status'],'SUCCESS');self.q.revoke(r)
        self.error('AUTHORIZATION_DENIED',self.use,'core')
    def test_crash_after_revocation_commit(self):
        r=self.revoke();self.worker('revoke',r,'after_revocation_commit')
        self.error('AUTHORIZATION_DENIED',self.use,'edge');self.assertTrue(self.q.revoke(r)['historical'])


class QualificationCLITests(QualificationCase):
    def command(self,*args):
        return subprocess.run([sys.executable,'-m','nss_base.qualification_cli','--store',str(self.root/'q'),*args],
            cwd=ROOT,capture_output=True,text=True,timeout=60)
    def test_inspect_json(self):
        r=self.command('inspect','--request-id','core');self.assertEqual(r.returncode,0,r.stderr)
        self.assertTrue(json.loads(r.stdout)['historical'])
    def test_audit_json(self):
        r=self.command('audit');self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['requests'],4)
    def test_cli_reject_and_history(self):
        req=self.req();self.q.prepare(req,source=self.source);p=self.root/'review.json';p.write_bytes(encoded(review_for(req,'REJECT')))
        r=self.command('review','--decision',str(p));self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(json.loads(r.stdout)['verdict'],'REJECTED')
    def test_cli_missing_request_has_typed_failure(self):
        r=self.command('inspect','--request-id','missing');self.assertEqual(r.returncode,1)
        self.assertEqual(json.loads(r.stderr)['status'],'INSUFFICIENT_EVIDENCE')
    def test_cli_duplicate_json_rejected(self):
        p=self.root/'bad.json';p.write_text('{"schema_version":1,"schema_version":1}')
        r=self.command('review','--decision',str(p));self.assertEqual(r.returncode,1)
        self.assertEqual(json.loads(r.stderr)['status'],'VALIDATION_FAILED')
    def test_cli_check_exact_scope(self):
        p=self.root/'request.json';p.write_bytes(encoded(self.requests['edge']))
        r=self.command('check','--request',str(p),'--certificate-sha256',self.receipts['edge']['certificate_sha256'],
            '--journal',str(self.root/'probe/journal'),'--data',str(self.root/'probe/data'))
        self.assertEqual(r.returncode,0,r.stderr);self.assertFalse(json.loads(r.stdout)['deployment_authorized'])
    def test_non_neural_inspection_needs_no_torch(self):
        code='''import sys
class BlockTorch:
 def find_spec(self,fullname,path=None,target=None):
  if fullname=='torch' or fullname.startswith('torch.'):raise ImportError('PyTorch deliberately unavailable')
sys.meta_path.insert(0,BlockTorch())
from nss_base.qualification_store import Qualifications
from nss_base.qualification_cli import main
assert 'torch' not in sys.modules
raise SystemExit(main(['--store',sys.argv[1],'audit']))
'''
        r=subprocess.run([sys.executable,'-c',code,str(self.root/'q')],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode,0,r.stderr)
