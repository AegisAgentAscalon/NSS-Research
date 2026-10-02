"""Real process exits around state commits, including uncertain external work."""
from copy import deepcopy
from pathlib import Path
import subprocess
import sys
from state_helpers import StateCase,SCOPE,CALLER
from nss_base.generation_store import Generations
from nss_base.neural_contracts import encoded,fingerprint
from nss_base.runtime import ContractError

ROOT=Path(__file__).resolve().parents[1]
CHILD='''
import sys
from pathlib import Path
from nss_base.catalog_controller import CatalogController
from nss_base.generation_store import Generations
import nss_base.generation_store as clock
from nss_base.ledger import Ledger
from nss_base.experience_store import ExperienceArchive
from nss_base.qualification_neural import NeuralEvidence
from nss_base.qualification_store import Qualifications
from nss_base.neural_contracts import read_document
root=Path(sys.argv[1]);clock.now_seconds=lambda:int(sys.argv[2])
ctl=CatalogController(Generations(root/'generations'), ledger=Ledger(root/'probe/mock_actions'),
    evidence_root=root/'context-sources',archive=ExperienceArchive(root/'context-archive'),
    qualifications=Qualifications(root/'q'),source=NeuralEvidence(root/'probe/journal',root/'probe/data'))
ctl.apply(read_document(root/'state-command.json'),fault_at=sys.argv[3])
'''

class PersistentStateCrashTests(StateCase):
    def run_window(self,action,when):
        if action=='BIND_STATE':c=self.bind_command();old=self.ctl.inspect('catalog-task')
        else:self.bind();old=self.history();c=self.approve(self.proposal([self.note()]))
        (self.root/'state-command.json').write_bytes(encoded(c));effects=self.ledger.effect_count()
        p=subprocess.run([sys.executable,'-c',CHILD,str(self.root),str(self.clock),when+'_'+action.lower()+'_commit'],
            cwd=ROOT,text=True,capture_output=True,timeout=120)
        self.assertEqual(p.returncode,83,p.stdout+p.stderr)
        fresh=Generations(self.root/'generations')
        if action=='BIND_STATE' and when=='before':now=fresh.inspect_task('catalog-task')
        else:now=fresh.inspect_task('catalog-task',caller_id=CALLER,scope=SCOPE)
        self.assertEqual(now['work']['record']['revision'],old['work']['record']['revision']+(when=='after'))
        self.assertEqual(now['ticket'],old['ticket'])
        result=self.ctl.apply(c);self.assertEqual(result['historical'],when=='after')
        again=self.ctl.apply(c);self.assertTrue(again['historical'])
        self.assertEqual(result['record_sha256'],again['record_sha256']);self.assertEqual(self.ledger.effect_count(),effects)
        self.assertEqual(fresh.inspect()['current'],self.manager.inspect()['current'])

    def test_pending_external_action_blocks_state_until_reconciled(self):
        self.bind();c=self.approve(self.proposal([self.note()]));before=self.history();effects=self.ledger.effect_count()
        child='''
import sys
from nss_base.ledger import Ledger
l=Ledger(sys.argv[1]);l.perform({'schema_version':1,'key':'uncertain-state-action','task_id':'catalog-task',
'payload':{'operation':'append_marker','value':'outside'},'status':'PENDING','receipt':None},crash_at='after_pending')
'''
        p=subprocess.run([sys.executable,'-c',child,str(self.root/'probe/mock_actions')],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(p.returncode,73,p.stdout+p.stderr)
        from nss_base.ledger import Ledger
        new_ledger=Ledger(self.root/'probe/mock_actions')
        self.assertEqual(new_ledger.inspect('uncertain-state-action')['status'],'UNCERTAIN')
        with self.assertRaises(ContractError) as e:self.ctl.apply(c)
        self.assertEqual(e.exception.code,'RECOVERY_REQUIRED')
        self.assertEqual(self.history(),before);self.assertEqual(new_ledger.effect_count(),effects)

for action in ('BIND_STATE','UPDATE_STATE'):
    for when in ('before','after'):
        def test(self,action=action,when=when):self.run_window(action,when)
        setattr(PersistentStateCrashTests,'test_crash_'+when+'_'+action.lower(),test)
