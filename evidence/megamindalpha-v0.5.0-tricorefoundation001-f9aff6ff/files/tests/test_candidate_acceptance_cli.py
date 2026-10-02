import unittest
from contextlib import redirect_stdout,redirect_stderr
from io import StringIO
from copy import deepcopy
from candidate_acceptance_helpers import CandidateCase
from nss_base.neural_contracts import encoded,fingerprint
from nss_base.qualification_cli import main as qualify_cli
from nss_base.generation_cli import main as generation_cli
from nss_base.catalog_cli import main as catalog_cli
from nss_base.qualificationevidence002 import AT


class CandidateCLITests(CandidateCase):
    def call(self,fn,args):
        out=StringIO();err=StringIO()
        with redirect_stdout(out),redirect_stderr(err):status=fn(args)
        return status,out.getvalue(),err.getvalue()

    def test_candidate_proposal_cli_uses_new_source_format(self):
        f=self.root/'scope.json';f.write_bytes(encoded({'kind':'PROFILE','profile':'CORE'}))
        args=['--store',str(self.root/'qualification'),'propose','--candidate-config',str(self.root/'learner_owners.json'),
            '--run-id',self.plan['cycle_id'],'--seed','31','--precision','fp32','--claim',str(f),
            '--producer','fixture-builder','--request-id','cli-candidate','--at',AT]
        code,out,err=self.call(qualify_cli,args);self.assertEqual(code,0,err)
        self.assertIn('MegaMindAlpha.CandidateEvidence001',out)
        self.assertEqual(self.manager.inspect()['current'],self.parent)

    def test_mixed_cli_source_is_rejected(self):
        f=self.root/'scope.json';f.write_bytes(encoded({'kind':'PROFILE','profile':'CORE'}))
        args=['--store',str(self.root/'qualification'),'propose','--candidate-config',str(self.root/'learner_owners.json'),
            '--journal',str(self.root/'probe/journal'),'--data',str(self.root/'probe/data'),
            '--run-id',self.plan['cycle_id'],'--seed','31','--precision','fp32','--claim',str(f),
            '--producer','fixture-builder','--request-id','cli-candidate','--at',AT]
        code,_,err=self.call(qualify_cli,args);self.assertEqual(code,1);self.assertIn('VALIDATION_FAILED',err)

    def test_candidate_current_check_cli(self):
        path=self.root/'request.json';path.write_bytes(encoded(self.reqs[2]))
        sha=fingerprint(self.q.inspect(self.reqs[2]['request_id'])['certificate'])
        code,out,err=self.call(qualify_cli,['--store',str(self.root/'qualification'),'check','--request',str(path),
            '--certificate-sha256',sha,'--candidate-config',str(self.root/'learner_owners.json')])
        self.assertEqual(code,0,err);self.assertIn('evidence_satisfies_claim',out)

    def test_generation_cli_can_read_actual_new_profile(self):
        self.adopt();t=self.manager.pin_stage('cli-stage',profile='A2B',caller_id='local-runner',**self.ev)
        path=self.root/'ticket.json';path.write_bytes(encoded(t))
        code,out,err=self.call(generation_cli,['--store',str(self.root/'generations'),'read-stage','--ticket',str(path),
            '--caller','local-runner','--qualification',str(self.root/'qualification'),
            '--candidate-config',str(self.root/'learner_owners.json')])
        self.assertEqual(code,0,err);self.assertIn('A2B',out);self.assertIn('"runtime_execution_permit":false',out)

    def test_declared_profile_catalogue_uses_candidate_schema(self):
        from nss_base.catalog_controller import fixture_descriptor,CatalogController
        from nss_base.ledger import Ledger
        self.adopt();v=self.source.view(self.plan['cycle_id'],31,'fp32')
        d=fixture_descriptor(self.family,v[1]['artifacts'],catalog_id='cli-catalog',author_id='fixture-builder',
            declarations={p['id']:{'capabilities':[p['id']],'load_units':1,'step_units':1,'max_pairs':4}
                          for p in self.family['profiles']})
        path=self.root/'catalog.json';path.write_bytes(encoded(d))
        code,out,err=self.call(catalog_cli,['--store',str(self.root/'generations'),'register','--descriptor',str(path),
            '--reviewer','generation-reviewer','--qualification',str(self.root/'qualification'),
            '--candidate-config',str(self.root/'learner_owners.json'),'--ledger',str(self.root/'probe/mock_actions'),
            '--sources',str(self.root)])
        self.assertEqual(code,0,err);self.assertIn('catalog_sha256',out)

    def test_exported_schemas_validate_real_new_evidence(self):
        import importlib.util,json
        from pathlib import Path
        if importlib.util.find_spec('jsonschema') is None:self.skipTest('Optional JSON Schema validator absent')
        import jsonschema
        from referencing import Registry,Resource
        root=Path(__file__).resolve().parents[1]/'schemas'
        reg=Registry().with_resources((p.as_uri(),Resource.from_contents(json.loads(p.read_text()))) for p in root.glob('*.json'))
        examples=[('qualification_request',self.reqs[1]),('qualification_binding',self.family['binding']),
                  ('generation_manifest',self.family)]
        for name,value in examples:
            path=root/(name+'.schema.json');schema=json.loads(path.read_text());schema['$id']=path.as_uri()
            with self.subTest(name=name):jsonschema.Draft202012Validator(schema,registry=reg).validate(value)


class CandidateToolTests(unittest.TestCase):
    def test_source_adapter_has_no_authority_or_private_storage(self):
        import ast
        from pathlib import Path
        root=Path(__file__).resolve().parents[1]
        tree=ast.parse((root/'nss_base/qualification_candidate.py').read_text())
        forbidden={'sqlite3','subprocess','socket','requests','qualification_store','generation_store'}
        for n in ast.walk(tree):
            if isinstance(n,ast.Import):self.assertFalse({a.name.split('.')[0] for a in n.names}&forbidden)
            if isinstance(n,ast.ImportFrom):self.assertNotIn(n.module,forbidden)
            if isinstance(n,ast.Attribute):self.assertNotIn(n.attr,('_db','publish','issue','decide','stage'))

    def test_candidate_graphs_are_bounded_and_rejections_terminal(self):
        from pathlib import Path
        from nss_base.logic_atlas import load_atlas
        root=Path(__file__).resolve().parents[1]
        fs=load_atlas(root/'spec/candidate_acceptance_flows.json')['flows']
        self.assertEqual({f['id'] for f in fs},{'candidate_evidence','candidate_adoption','candidate_task_rollback'})
        f=next(f for f in fs if f['id']=='candidate_evidence')
        self.assertFalse(any(e['from']=='no' for e in f['transitions']))
        self.assertTrue(any(e['from']=='old' and e['to']=='hist' for e in f['transitions']))
        self.assertEqual(len(load_atlas(root/'spec/logic_atlas.json')['flows']),25)

    def test_candidate_schemas_and_logic_regenerate_without_drift(self):
        from pathlib import Path
        import subprocess,sys
        root=Path(__file__).resolve().parents[1]
        paths=[*root.glob('schemas/qualification_*.json'),*root.glob('schemas/generation_*.json'),
            *root.glob('schemas/catalog_*.json'),*root.glob('schemas/context_*.json'),
            root/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md',root/'docs/CANDIDATE_ACCEPTANCE_LOGIC.md',
            *root.glob('docs/logic_flowcharts/candidate_*.dot')]
        before={p:p.read_bytes() for p in paths}
        for args in [('tools/generate_qualification_schemas.py',),('tools/generate_generation_schemas.py',),
                     ('tools/generate_subsystem_logic.py','--view','candidate')]:
            run=subprocess.run([sys.executable,*args],cwd=root,capture_output=True,text=True,timeout=45)
            self.assertEqual(run.returncode,0,run.stderr)
        self.assertEqual(before,{p:p.read_bytes() for p in paths})

    def test_candidate_history_without_owner_evidence_is_rejected(self):
        from pathlib import Path
        import subprocess,sys,tempfile
        root=Path(__file__).resolve().parents[1]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'summary.json';p.write_text('{"status":"SUCCESS","scope":"CONNECTED_HUMAN_ASSISTED_LOCAL_CANDIDATE_ADOPTION_AND_ROLLBACK"}')
            run=subprocess.run([sys.executable,'tools/verify_connected_alpha.py','--summary',str(p)],
                cwd=root,capture_output=True,text=True,timeout=30)
            self.assertEqual(run.returncode,1)
