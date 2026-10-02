"""Shared schema/logic tools, CLI, and process exits around read-only operations."""
from pathlib import Path
import json
import subprocess
import sys
import unittest
from context_helpers import ContextCase, CALLER
from dataset_helpers import ok
from nss_base.neural_contracts import encoded, fingerprint
from nss_base.logic_atlas import load_atlas
ROOT=Path(__file__).resolve().parents[1]


class ContextProcessTests(ContextCase):
    def test_process_exits_during_reads_leave_no_published_task_or_archive_change(self):
        req=self.start_context();self.add_experience(req,required=True);p=self.built(req)
        (self.root/'context-request.json').write_bytes(encoded(req));(self.root/'saved-context.json').write_bytes(encoded(p))
        task=self.ctl.inspect('catalog-task');audit=ok(self.archive.audit());effect=self.ledger.effect_count()
        for point in ('after_task_read','after_archive_read','before_return'):
            with self.subTest(point=point):
                r=subprocess.run([sys.executable,str(ROOT/'tests/context_crash_worker.py'),str(self.root),point],cwd=ROOT,capture_output=True,text=True,timeout=90)
                self.assertEqual(r.returncode,81,r.stderr);self.assertEqual(r.stdout,'')
                self.assertEqual(task,self.ctl.inspect('catalog-task'));self.assertEqual(audit,ok(self.archive.audit()));self.assertEqual(effect,self.ledger.effect_count())
        r=subprocess.run([sys.executable,str(ROOT/'tests/context_crash_worker.py'),str(self.root),'consume'],cwd=ROOT,capture_output=True,text=True,timeout=90)
        self.assertEqual(r.returncode,0,r.stderr);self.assertEqual(json.loads(r.stdout)['data']['payload'],p['payload'])

    def test_cli_build_consume_and_revoked_current_read(self):
        from dataset_helpers import revoke
        req=self.start_context();self.add_experience(req,required=True)
        path=self.root/'context-request.json';path.write_bytes(encoded(req))
        cmd=[sys.executable,'-m','nss_base.context_cli','--store',str(self.root/'generations'),
            '--qualification',str(self.root/'q'),'--journal',str(self.root/'probe/journal'),'--data',str(self.root/'probe/data'),
            '--ledger',str(self.root/'probe/mock_actions'),'--sources',str(self.sources),'--archive',str(self.root/'context-archive')]
        r=subprocess.run(cmd+['build','--request',str(path)],cwd=ROOT,capture_output=True,text=True,timeout=90)
        self.assertEqual(r.returncode,0,r.stderr+r.stdout);p=json.loads(r.stdout)['data']
        saved=self.root/'saved-context.json';saved.write_bytes(encoded(p))
        consume=cmd+['consume','--packet',str(saved),'--caller',CALLER,'--packet-hash',fingerprint(p)]
        r=subprocess.run(consume,cwd=ROOT,capture_output=True,text=True,timeout=90);self.assertEqual(r.returncode,0,r.stderr+r.stdout)
        ok(revoke(self.archive,purpose='retrieval'));r=subprocess.run(consume,cwd=ROOT,capture_output=True,text=True,timeout=90)
        self.assertEqual(r.returncode,1);self.assertEqual(json.loads(r.stdout)['status'],'TRAINING_RESTRICTED')

    def test_malformed_rehydration_selector_is_typed(self):
        p=self.built(self.start_context())
        for selector in ([],{'kind':[]},{'kind':'TASK_FIELD','source_id':[],'field_id':'x'},
                         {'kind':'TASK_FIELD','source_id':'source-1','field_id':'speed','extra':True}):
            with self.subTest(selector=selector):
                self.rejected('VALIDATION_FAILED',self.service.rehydrate(p,caller_id=CALLER,expected_packet_sha256=fingerprint(p),selector=selector))


class ContextToolTests(unittest.TestCase):
    def test_schemas_and_logic_regenerate_without_drift(self):
        paths=[*ROOT.glob('schemas/context_*.json'),ROOT/'docs/CONTEXT_RETRIEVAL_LOGIC.md',
               ROOT/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md',*ROOT.glob('docs/logic_flowcharts/context_*.dot')]
        before={p:p.read_bytes() for p in paths}
        for command in (['tools/generate_generation_schemas.py'],['tools/generate_subsystem_logic.py','--view','context']):
            r=subprocess.run([sys.executable,*command],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(before,{p:p.read_bytes() for p in paths})

    def test_three_read_only_helper_flows_and_research_not_promoted(self):
        a=load_atlas(ROOT/'spec/context_retrieval_flows.json')
        self.assertEqual({f['id'] for f in a['flows']},{'context_build','context_consume','context_rehydrate'})
        parent=next(f for f in load_atlas()['flows'] if f['id']=='context_manager')
        self.assertEqual(parent['status'],'research')
        for f in a['flows']:
            self.assertIn('BUDGET_EXHAUSTED',f['failure_codes']);self.assertIn('No external actions','\n'.join(f['invariants']))

    def test_cli_help_does_not_open_stores_or_train(self):
        r=subprocess.run([sys.executable,'-m','nss_base.context_cli','--help'],cwd=ROOT,capture_output=True,text=True,timeout=30)
        self.assertEqual(r.returncode,0,r.stderr);self.assertIn('rehydrate',r.stdout)

    def test_context_modules_have_no_sql_training_or_action_executor_imports(self):
        import ast
        forbidden={'sqlite3','torch','subprocess','requests'}
        for name in ('context_contracts','context_plan','context_service'):
            tree=ast.parse((ROOT/'nss_base'/(name+'.py')).read_text())
            imports={a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
            self.assertFalse(imports & forbidden)
            for node in ast.walk(tree):
                if isinstance(node,ast.Attribute):self.assertNotIn(node.attr,('_db','inspect_source','task_operation','capture','change','train'))
