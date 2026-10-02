"""Storage, operator surface and ownership checks; not a security proof."""
import ast
from contextlib import closing
from copy import deepcopy
from pathlib import Path
import sqlite3
import subprocess
import sys
from generation_helpers import GenerationCase
from nss_base.generation_state import source_matches
from nss_base.generation_store import Generations
from nss_base.neural_contracts import encoded, fingerprint
from nss_base.runtime import ContractError

ROOT = Path(__file__).resolve().parents[1]


class GenerationIntegrityTests(GenerationCase):
    def test_missing_store_is_not_recreated(self):
        self.manager.journal.path.unlink()
        self.error('RECOVERY_REQUIRED',Generations,self.root/'generations')
        self.assertFalse(self.manager.journal.path.exists())

    def test_existing_directory_cannot_be_overwritten(self):
        from nss_base.overlaygenerationmanager001 import OPERATORS
        self.error('CONSTRAINT_CONFLICT',Generations.create,self.root/'generations',OPERATORS)

    def test_corrupt_stage_blocks_publication_without_current_update(self):
        key,opts=self.issued();self.manager.prepare(key,**opts);self.manager.stage(key,**opts)
        with closing(sqlite3.connect(self.manager.journal.path)) as db,db:
            db.execute("UPDATE events SET body='{}' WHERE kind='STAGE'")
        self.error('VALIDATION_FAILED',self.manager.publish,key,**opts)
        with closing(sqlite3.connect(self.manager.journal.path)) as db:
            self.assertEqual(db.execute("SELECT COUNT(*) FROM events WHERE kind='PUBLISH'").fetchone()[0],0)

    def test_core_replacement_is_not_an_overlay_update(self):
        from nss_base.generation_state import core_identity
        original=deepcopy(self.gs[0]);altered=deepcopy(original);altered['binding']['checkpoint_hashes']['core']='0'*64
        h=fingerprint(altered);s={'current':{'epoch':1,'generation_sha256':self.hashes[0]},
             'core_identity':core_identity(original),'generations':{h:{'manifest':altered}},'published':{}}
        req={'expected_current':s['current'],'target_sha256':h,'mode':'UPDATE'}
        self.error('INCOMPATIBLE_CONFIGURATION',source_matches,s,req)

    def test_cli_help_and_read_only_surface(self):
        for args in (['--help'],['--store',str(self.root/'generations'),'inspect'],
                     ['--store',str(self.root/'generations'),'audit']):
            p=subprocess.run([sys.executable,'-m','nss_base.generation_cli',*args],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(p.returncode,0,p.stderr)

    def test_cli_request_issue_and_publish_use_exact_contracts(self):
        request=self.request();path=self.root/'release.json';path.write_bytes(encoded(request))
        def cli(*args):
            p=subprocess.run([sys.executable,'-m','nss_base.generation_cli','--store',str(self.root/'generations'),*args],cwd=ROOT,capture_output=True,text=True,timeout=120)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            from nss_base.serialization import decode
            return decode(p.stdout)
        ev=['--qualification',str(self.root/'q'),'--journal',str(self.root/'probe/journal'),'--data',str(self.root/'probe/data')]
        grant=cli('issue','--request',str(path),'--issuer','release-owner','--ttl','300',*ev)['grant']
        for step in ('prepare','stage','publish'):
            result=cli(step,'--release','release-1','--grant-hash',fingerprint(grant),'--caller','local-runner',*ev)
        self.assertEqual(result['status'],'PUBLISHED')
        self.assertFalse(result['production_deployment_authorized'])

    def test_cli_malformed_json_fails_with_typed_error(self):
        p=self.root/'bad.json';p.write_text('{"x":1,"x":2}')
        child=subprocess.run([sys.executable,'-m','nss_base.generation_cli','--store',str(self.root/'generations'),
             'issue','--request',str(p),'--issuer','release-owner','--qualification',str(self.root/'q'),
             '--journal',str(self.root/'probe/journal'),'--data',str(self.root/'probe/data')],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(child.returncode,1);self.assertIn('VALIDATION_FAILED',child.stderr)

    def test_no_private_qualification_sql_or_general_runtime_execution(self):
        for path in (ROOT/'nss_base').glob('generation*.py'):
            for n in ast.walk(ast.parse(path.read_text())):
                if isinstance(n,ast.Import):
                    self.assertFalse(any(x.name in ('sqlite3','subprocess','requests','pickle') for x in n.names),path)
                if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id in ('source','qualifications'):
                    self.assertFalse(n.attr.startswith('_'),(path,n.attr))
        self.assertIn('EventJournal',(ROOT/'nss_base/generation_store.py').read_text())
        self.assertIn('EventJournal',(ROOT/'nss_base/permission_journal.py').read_text())


MUTATIONS = {'deleted_event': 'DELETE FROM events WHERE seq=1',
             'deleted_metadata': 'DELETE FROM meta',
             'changed_head': "UPDATE meta SET head='bad'",
             'changed_manifest': "UPDATE meta SET manifest='{}'",
             'injected_kind': "UPDATE events SET kind='DEPLOY_NOW' WHERE seq=1",
             'changed_count': 'UPDATE meta SET count=count+1',
             'changed_time': 'UPDATE events SET at=0 WHERE seq=1'}
for name,sql in MUTATIONS.items():
    def test(self, sql=sql):
        with closing(sqlite3.connect(self.manager.journal.path)) as db,db:db.execute(sql)
        self.error('VALIDATION_FAILED',self.manager.audit)
    setattr(GenerationIntegrityTests,'test_corruption_'+name,test)
