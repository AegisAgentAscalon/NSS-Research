"""Real process exits exercise the new evidence format through existing journals."""
from pathlib import Path
import subprocess
import sys
from candidate_acceptance_helpers import CandidateCase
from nss_base.generation_store import Generations
from nss_base.neural_contracts import encoded,fingerprint
from nss_base.qualificationevidence002 import review_for
from nss_base.qualification_store import Qualifications

ROOT=Path(__file__).resolve().parents[1]
CHILD='''
import sys
from pathlib import Path
from nss_base.neural_contracts import read_document
from nss_base.qualification_candidate import from_config
from nss_base.qualification_store import Qualifications
from nss_base.generation_store import Generations
import nss_base.generation_store as clock
root=Path(sys.argv[1]);clock.now_seconds=lambda:int(sys.argv[2])
source=from_config(read_document(root/'learner_owners.json'));q=Qualifications(root/'qualification')
phase=sys.argv[3];hook=sys.argv[4]
if phase=='decide':q.decide(read_document(root/'decision.json'),source=source,fault_at=hook)
else:
 g=Generations(root/'generations');ev={'qualifications':q,'source':source}
 if phase=='issue':g.issue(read_document(root/'release.json'),issuer_id='release-owner',ttl_seconds=300,fault_at=hook,**ev)
 else:getattr(g,phase)('candidate-release',grant_sha256=sys.argv[5],caller_id='local-runner',fault_at=hook,**ev)
'''


class CandidateCrashTests(CandidateCase):
    def child(self,phase,hook,h='0'*64):
        run=subprocess.run([sys.executable,'-c',CHILD,str(self.root),str(self.clock),phase,hook,h],
            cwd=ROOT,capture_output=True,text=True,timeout=150)
        self.assertEqual(run.returncode,79 if phase=='decide' else 83,run.stdout+run.stderr)

    def qualification_crash(self,hook,expected):
        req=self.fresh();self.q.prepare(req,source=self.source)
        (self.root/'decision.json').write_bytes(encoded(review_for(req)))
        self.child('decide',hook)
        self.q=Qualifications(self.root/'qualification')
        self.assertEqual(self.q.inspect(req['request_id'])['status'],expected)
        result=self.q.decide(review_for(req),source=self.source)
        self.assertEqual(result['verdict'],'QUALIFIED')
        self.assertEqual(self.manager.inspect()['current'],self.parent)
        self.assert_no_training_or_effect()

    def release_crash(self,phase,when,expected):
        req=self.request();(self.root/'release.json').write_bytes(encoded(req));opts=None
        if phase!='issue':
            opts=self.issue()
            if phase in ('stage','publish'):self.manager.prepare('candidate-release',**opts)
            if phase=='publish':self.manager.stage('candidate-release',**opts)
        self.child(phase,when+'_'+phase+'_commit',opts['grant_sha256'] if opts else '0'*64)
        self.manager=Generations(self.root/'generations')
        if expected=='ABSENT':self.error('INSUFFICIENT_EVIDENCE',self.manager.inspect_release,'candidate-release')
        else:self.assertEqual(self.manager.inspect_release('candidate-release')['status'],expected)
        self.assertEqual(self.manager.inspect()['current']['epoch'],self.parent['epoch']+int(expected=='PUBLISHED'))
        issued=self.manager.issue(req,issuer_id='release-owner',ttl_seconds=300,**self.ev)
        opts={'caller_id':'local-runner','grant_sha256':fingerprint(issued['grant']),**self.ev}
        for fn in (self.manager.prepare,self.manager.stage,self.manager.publish):fn('candidate-release',**opts)
        self.assertEqual(self.manager.inspect()['current']['generation_sha256'],self.target)
        self.assert_no_training_or_effect()

    def test_expired_staged_resume_does_not_publish(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts)
        self.child('stage','after_stage_commit',opts['grant_sha256']);self.clock+=300
        self.manager=Generations(self.root/'generations')
        self.error('AUTHORIZATION_DENIED',self.manager.publish,'candidate-release',**opts)
        self.assertEqual(self.manager.inspect()['current'],self.parent)
        self.manager.abandon('candidate-release',caller_id='local-runner',reason='Expired interrupted release')
        self.error('CONSTRAINT_CONFLICT',self.manager.stage,'candidate-release',**opts)

    def test_new_use_rechecks_revocation_after_restart(self):
        opts=self.issue();self.manager.prepare('candidate-release',**opts)
        self.child('stage','after_stage_commit',opts['grant_sha256']);self.withdraw('candidate-a2')
        self.manager=Generations(self.root/'generations')
        self.error('AUTHORIZATION_DENIED',self.manager.publish,'candidate-release',**opts)
        self.assertEqual(self.manager.inspect()['current'],self.parent)


for hook,state in [('after_verification','PREPARED'),('before_decision_commit','PREPARED'),('after_decision_commit','QUALIFIED')]:
    def test(self,hook=hook,state=state):self.qualification_crash(hook,state)
    setattr(CandidateCrashTests,'test_qualification_crash_'+hook,test)
for phase,when,state in [('issue','before','ABSENT'),('issue','after','GRANTED'),
    ('prepare','before','GRANTED'),('prepare','after','PREPARED'),('stage','before','PREPARED'),
    ('stage','after','STAGED'),('publish','before','STAGED'),('publish','after','PUBLISHED')]:
    def test(self,phase=phase,when=when,state=state):self.release_crash(phase,when,state)
    setattr(CandidateCrashTests,'test_release_crash_'+when+'_'+phase,test)
