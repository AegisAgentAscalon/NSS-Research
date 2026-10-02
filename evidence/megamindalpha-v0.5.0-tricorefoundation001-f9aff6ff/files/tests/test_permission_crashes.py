"""Actual os._exit injection; no simulated exceptions standing in for process loss."""
import json
from pathlib import Path
import subprocess
import sys
from permission_helpers import PermissionCase
from nss_base.permission_store import Permissions
from nss_base.permission_executor import ReplayExecutor

ROOT=Path(__file__).resolve().parents[1]
CHILD='''
import json,sys
from pathlib import Path
from nss_base.permission_store import Permissions
import nss_base.permission_store as clock
from nss_base.permission_executor import ReplayExecutor
from nss_base.permission_replay import execute_once
from nss_base.qualification_store import Qualifications
from nss_base.qualification_neural import NeuralEvidence
from nss_base.ledger import Ledger
root=Path(sys.argv[1]);clock.now_seconds=lambda:int(sys.argv[2])
req=json.loads((root/'operation.json').read_text());point=sys.argv[3];mode=sys.argv[4]
p=Permissions(root/'permissions');q=Qualifications(root/'q');s=NeuralEvidence(root/'probe/journal',root/'probe/data')
if mode=='issue':p.issue(req,issuer_id='local-owner',ttl_seconds=100,qualifications=q,source=s,fault_at=point)
elif mode=='revoke':p.revoke(req['request_id'],grant_sha256=sys.argv[5],actor_id='local-owner',revocation_id='crash-withdraw',reason='Crash test',fault_at=point)
else:execute_once(p,req,grant_sha256=sys.argv[5],caller_id='local-runner',qualifications=q,source=s,executor=ReplayExecutor(root/'executor'),ledger=Ledger(root/'probe/mock_actions'),fault_at=point)
'''

class PermissionCrashTests(PermissionCase):
    def child(self,point,mode,h='0'*64):
        (self.root/'operation.json').write_text(json.dumps(self.operation))
        r=subprocess.run([sys.executable,'-c',CHILD,str(self.root),str(self.clock),point,mode,h],cwd=ROOT,capture_output=True,text=True,timeout=120)
        self.assertEqual(r.returncode,83,r.stdout+r.stderr)
        self.permits=Permissions(self.root/'permissions');self.executor=ReplayExecutor(self.root/'executor')
    def probe(self,point,expected,receipt):
        h=self.granted();self.child(point,'execute',h)
        self.assertEqual(self.permits.inspect('permission-1')['status'],expected)
        self.assertEqual(self.executor.audit()['committed_results'],int(receipt))
        self.assertEqual(self.ledger.effect_count(),1)
        if expected=='GRANTED':
            self.assertEqual(self.execute_permission(h)['status'],'COMMITTED')
        elif expected=='COMMITTED':
            self.assertTrue(self.execute_permission(h)['historical'])
        else:
            self.error('RECOVERY_REQUIRED',self.execute_permission,h)
            self.assertEqual(self.reconcile(h)['status'],'COMMITTED' if receipt else 'ABANDONED')
        self.assertEqual(self.ledger.effect_count(),1)
    def test_crash_before_consume(self):self.probe('before_consume_commit','GRANTED',False)
    def test_crash_after_consume(self):self.probe('after_consume_commit','STARTED',False)
    def test_crash_after_dispatch(self):self.probe('after_dispatch_check','DISPATCHED',False)
    def test_crash_before_executor_commit(self):self.probe('before_executor_commit','DISPATCHED',False)
    def test_crash_after_executor_commit(self):self.probe('after_executor_commit','DISPATCHED',True)
    def test_crash_before_completion(self):self.probe('before_completion_commit','DISPATCHED',True)
    def test_crash_after_completion(self):self.probe('after_completion_commit','COMMITTED',True)
    def test_crash_before_issue(self):
        self.child('before_issue_commit','issue');self.assertEqual(self.permits.audit()['grants'],0)
        self.assertFalse(self.issue()['historical'])
    def test_crash_after_issue(self):
        self.child('after_issue_commit','issue');self.assertEqual(self.permits.audit()['grants'],1)
        self.assertTrue(self.issue()['historical'])
    def test_crash_before_revoke(self):
        h=self.granted();self.child('before_revoke_commit','revoke',h)
        self.assertFalse(self.permits.inspect('permission-1')['revoked'])
    def test_crash_after_revoke(self):
        h=self.granted();self.child('after_revoke_commit','revoke',h)
        self.assertTrue(self.permits.inspect('permission-1')['revoked'])
        self.error('AUTHORIZATION_DENIED',self.begin,h)
