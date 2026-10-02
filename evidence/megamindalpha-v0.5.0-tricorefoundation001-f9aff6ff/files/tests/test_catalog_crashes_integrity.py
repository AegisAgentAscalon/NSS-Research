"""Real process loss plus semantic journal corruption; one harness per boundary."""
from copy import deepcopy
from pathlib import Path
import json
import subprocess
import sys
from catalog_helpers import CatalogCase, CALLER, ROOT
from nss_base.catalog_controller import CatalogController
from nss_base.generation_store import Generations
from nss_base.generation_state import reduce_events
from nss_base.neural_contracts import encoded, fingerprint
from nss_base.runtime import ContractError

CHILD = '''
from pathlib import Path
import sys
from nss_base.catalog_controller import CatalogController
from nss_base.generation_store import Generations
import nss_base.generation_store as clock
from nss_base.qualification_store import Qualifications
from nss_base.qualification_neural import NeuralEvidence
from nss_base.ledger import Ledger
from nss_base.neural_contracts import read_document
root=Path(sys.argv[1]);clock.now_seconds=lambda:int(sys.argv[2])
c=CatalogController(Generations(root/'generations'),qualifications=Qualifications(root/'q'),
 source=NeuralEvidence(root/'probe/journal',root/'probe/data'),ledger=Ledger(root/'probe/mock_actions'),evidence_root=sys.argv[3])
c.apply(read_document(root/'command.json'),fault_at=sys.argv[4])
'''


class CatalogDurabilityTests(CatalogCase):
    def crash_case(self, action, when):
        if action == 'START': c=self.start_command()
        else:
            self.started()
            if action in ('MOVE','CLOSE'):self.finished()
            c=self.move_command() if action=='MOVE' else self.command(action)
        before=self.manager.inspect(); (self.root/'command.json').write_bytes(encoded(c))
        child=subprocess.run([sys.executable,'-c',CHILD,str(self.root),str(self.clock),str(self.sources),
            when+'_'+action.lower()+'_commit'],cwd=ROOT,capture_output=True,text=True,timeout=120)
        self.assertEqual(child.returncode,83,child.stdout+child.stderr)
        self.manager=Generations(self.root/'generations')
        self.ctl=CatalogController(self.manager,ledger=self.ledger,evidence_root=self.sources,**self.ev)
        after=self.manager.inspect()
        self.assertEqual(after['events'],before['events']+int(when=='after'))
        r=self.ctl.apply(c);self.assertEqual(r['historical'],when=='after')
        final=self.ctl.inspect('catalog-task')
        expected={'START':'RUNNING','MOVE':'RUNNING','FINISH':'SEALED','CLOSE':'COMPLETED','CANCEL':'CANCELLED'}[action]
        self.assertEqual(final['work']['phase'],expected)
        self.assertEqual(final['closed'],action in ('CLOSE','CANCEL'))
        if action=='MOVE':
            self.assertEqual(final['ticket']['profile'],'A')
            self.assertTrue(self.manager.inspect_stage(c['source_ticket']['ticket_id'])['closed'])
        self.assertEqual(self.ledger.effect_count(),1)
        count=self.manager.inspect()['events'];self.assertTrue(self.ctl.apply(c)['historical'])
        self.assertEqual(self.manager.inspect()['events'],count)

    def test_restart_retains_unfinished_ticket_and_blocks_release(self):
        self.started();self.manager=Generations(self.root/'generations')
        self.assertEqual(self.manager.inspect()['open_stages'],1)
        key,opts=self.issued(0,'release-later','UPDATE')
        self.error('RECOVERY_REQUIRED',self.manager.prepare,key,**opts)

    def test_semantic_reducer_rejects_forged_task_events(self):
        self.started();self.finished();self.ctl.apply(self.move_command())
        with self.manager.journal.transaction() as db:
            manifest,_,_,events=self.manager.journal.read(db,reduce_events)
        for target in ('profile','record','receipt','input_pairs','ticket','missing_core_descriptor'):
            with self.subTest(target=target):
                bad=deepcopy(events);body=bad[-1]['body']
                if target=='profile':body['selection']['profile']='AB'
                elif target=='record':body['record']['assumptions']=[]
                elif target=='receipt':body['receipt']['record_sha256']='0'*64
                elif target=='input_pairs':body['command']['request']['pairs']=[[15,15]]
                elif target=='ticket':body['ticket']['configuration']['epoch']+=1
                else:
                    b=next(e['body'] for e in bad if e['kind']=='CATALOG_REGISTER')
                    b['descriptor']['profiles']=[p for p in b['descriptor']['profiles'] if p['id']!='CORE']
                with self.assertRaises(ContractError):reduce_events(manifest,bad)

    def test_plain_unpin_event_cannot_bypass_task_close_semantics(self):
        _,r=self.started()
        with self.manager.journal.transaction() as db:
            m,_,_,events=self.manager.journal.read(db,reduce_events)
        events.append({'kind':'UNPIN','body':{'ticket':r['ticket']},'at':self.clock})
        self.error('CONSTRAINT_CONFLICT',reduce_events,m,events)

    def test_uncertain_external_effect_requires_explicit_reconciliation_before_cancel(self):
        self.started()
        action={'schema_version':1,'task_id':'catalog-task','key':'uncertain-output',
            'payload':{'operation':'append_marker','value':'mock presented output'},'status':'PENDING','receipt':None}
        path=self.root/'action.json';path.write_bytes(encoded(action))
        child=subprocess.run([sys.executable,'-c',
            'import sys; from nss_base.ledger import Ledger; from nss_base.neural_contracts import read_document; Ledger(sys.argv[1]).perform(read_document(sys.argv[2]),crash_at="after_effect")',
            str(self.root/'probe/mock_actions'),str(path)],cwd=ROOT,capture_output=True,text=True,timeout=60)
        self.assertEqual(child.returncode,73,child.stdout+child.stderr)
        from nss_base.ledger import Ledger
        self.ledger=Ledger(self.root/'probe/mock_actions')
        self.ctl=CatalogController(self.manager,ledger=self.ledger,evidence_root=self.sources,**self.ev)
        self.error('RECOVERY_REQUIRED',self.ctl.apply,self.command('CANCEL'))
        self.assertEqual(self.manager.inspect()['open_stages'],1)
        self.assertEqual(self.ledger.reconcile('uncertain-output'),'COMMITTED')
        r=self.ledger.inspect('uncertain-output')['receipt']
        self.ctl.apply(self.command('CANCEL',receipts=[{'key':'uncertain-output','kind':'presented_output','receipt':r}]))
        self.assertEqual(self.ledger.effect_count(),2);self.assertEqual(self.manager.inspect()['open_stages'],0)

    def test_raw_event_mutation_is_detected(self):
        import sqlite3
        from contextlib import closing
        self.started()
        with closing(sqlite3.connect(self.manager.journal.path)) as db,db:
            db.execute("UPDATE events SET body='{}' WHERE kind='CATALOG_TASK'")
        self.error('VALIDATION_FAILED',self.manager.audit)

    def test_cli_selection_inspection_apply_and_read(self):
        c=self.start_command();op=self.root/'operation.json';op.write_bytes(encoded(c))
        req=self.root/'request.json';req.write_bytes(encoded(c['request']))
        ev=['--qualification',str(self.root/'q'),'--journal',str(self.root/'probe/journal'),
            '--data',str(self.root/'probe/data'),'--ledger',str(self.root/'probe/mock_actions'),'--sources',str(self.sources)]
        def cli(*args):
            p=subprocess.run([sys.executable,'-c',
                'import sys; import nss_base.generation_store as clock; clock.now_seconds=lambda:'+str(self.clock)+'; from nss_base.catalog_cli import main; raise SystemExit(main(sys.argv[1:]))',
                '--store',str(self.root/'generations'),*args],
                cwd=ROOT,capture_output=True,text=True,timeout=120)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr);return json.loads(p.stdout)
        self.assertEqual(cli('select','--request',str(req),'--caller',CALLER,*ev)['profile'],'AB')
        result=cli('apply','--operation',str(op),*ev)
        ticket=self.root/'ticket.json';ticket.write_bytes(encoded(result['ticket']))
        v=cli('read','--ticket',str(ticket),'--record-hash',result['record_sha256'],'--caller',CALLER,*ev)
        self.assertEqual(set(v['artifacts']),{'core','A','B'});self.assertFalse(v['runtime_execution_permit'])
        self.assertTrue(cli('inspect','--task','catalog-task')['historical'])

    def test_cli_duplicate_fields_fail_typed_without_writes(self):
        bad=self.root/'bad.json';bad.write_text('{"a":1,"a":2}')
        p=subprocess.run([sys.executable,'-m','nss_base.catalog_cli','--store',str(self.root/'generations'),
            'apply','--operation',str(bad),'--qualification',str(self.root/'q'),'--journal',str(self.root/'probe/journal'),
            '--data',str(self.root/'probe/data'),'--ledger',str(self.root/'probe/mock_actions'),'--sources',str(self.sources)],
            cwd=ROOT,capture_output=True,text=True,timeout=120)
        self.assertEqual(p.returncode,1);self.assertIn('VALIDATION_FAILED',p.stderr)
        self.assertEqual(self.manager.inspect()['open_stages'],0)


for action in ('START','MOVE','FINISH','CLOSE','CANCEL'):
    for when in ('before','after'):
        def test(self,action=action,when=when):self.crash_case(action,when)
        setattr(CatalogDurabilityTests,'test_process_exit_'+when+'_'+action.lower(),test)
