"""Data-driven real process-loss tests retain all distinct publication windows."""
from pathlib import Path
import subprocess
import sys
from generation_helpers import GenerationCase
from nss_base.generation_store import Generations
from nss_base.neural_contracts import encoded, fingerprint
from nss_base.ledger import Ledger

ROOT = Path(__file__).resolve().parents[1]
CHILD = '''
from pathlib import Path
import sys
from nss_base.generation_store import Generations
import nss_base.generation_store as clock
from nss_base.neural_contracts import read_document
from nss_base.qualification_neural import NeuralEvidence
from nss_base.qualification_store import Qualifications
root=Path(sys.argv[1]);clock.now_seconds=lambda:int(sys.argv[2])
store=Generations(root/'generations');ev={'qualifications':Qualifications(root/'q'),'source':NeuralEvidence(root/'probe/journal',root/'probe/data')}
if sys.argv[3]=='issue': store.issue(read_document(root/'release.json'),issuer_id='release-owner',ttl_seconds=300,fault_at=sys.argv[4],**ev)
else:getattr(store,sys.argv[3])('release-1',grant_sha256=sys.argv[5],caller_id='local-runner',fault_at=sys.argv[4],**ev)
'''


class GenerationCrashTests(GenerationCase):
    def crash_case(self, phase, when, expected):
        req = self.request(); (self.root/'release.json').write_bytes(encoded(req))
        opts = None
        if phase != 'issue':
            _, opts = self.issued()
            if phase in ('stage','publish'):self.manager.prepare('release-1',**opts)
            if phase == 'publish':self.manager.stage('release-1',**opts)
        h = opts['grant_sha256'] if opts else '0'*64
        child = subprocess.run([sys.executable,'-c',CHILD,str(self.root),str(self.clock),phase,
            when+'_'+phase+'_commit',h],cwd=ROOT,capture_output=True,text=True,timeout=120)
        self.assertEqual(child.returncode,83,child.stdout+child.stderr)
        self.manager = Generations(self.root/'generations')
        if expected == 'ABSENT':
            self.error('INSUFFICIENT_EVIDENCE',self.manager.inspect_release,'release-1')
        else:self.assertEqual(self.manager.inspect_release('release-1')['status'],expected)
        self.assertEqual(self.manager.inspect()['current']['epoch'],int(expected=='PUBLISHED'))
        # Same request resumes only safe local work, rechecks authority, and never
        # creates a second publish or touches the mock-world ledger.
        issued = self.manager.issue(req,issuer_id='release-owner',ttl_seconds=300,**self.ev)
        opts = {'grant_sha256':fingerprint(issued['grant']),'caller_id':'local-runner',**self.ev}
        for fn in (self.manager.prepare,self.manager.stage,self.manager.publish):fn('release-1',**opts)
        self.assertEqual(self.manager.inspect()['current']['epoch'],1)
        self.assertEqual(Ledger(self.root/'probe/mock_actions').effect_count(),1)

    def test_expired_consumed_grant_after_restart_requires_abandonment(self):
        key,opts=self.issued();self.manager.prepare(key,**opts)
        self.manager=Generations(self.root/'generations');self.clock+=300
        self.error('AUTHORIZATION_DENIED',self.manager.stage,key,**opts)
        self.manager.abandon(key,caller_id='local-runner',reason='Expired interrupted work')
        self.error('CONSTRAINT_CONFLICT',self.manager.prepare,key,**opts)
        self.adopted(id='fresh-release')
        self.assertEqual(self.manager.inspect()['current']['epoch'],1)


WINDOWS = [('issue','before','ABSENT'),('issue','after','GRANTED'),
           ('prepare','before','GRANTED'),('prepare','after','PREPARED'),
           ('stage','before','PREPARED'),('stage','after','STAGED'),
           ('publish','before','STAGED'),('publish','after','PUBLISHED')]
for phase,when,expected in WINDOWS:
    def test(self, phase=phase, when=when, expected=expected):
        self.crash_case(phase,when,expected)
    setattr(GenerationCrashTests,'test_crash_'+when+'_'+phase,test)
