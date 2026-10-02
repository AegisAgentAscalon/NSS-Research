"""Reproducible build/CLI checks; no secret data, subprocess network or new backend."""
import ast
from copy import deepcopy
from pathlib import Path
import json
import subprocess
import sys
import time
import unittest
from learner_helpers import LearnerCase
from nss_base.boundedlearnercoordinator001 import plan_from_reviewed_data
from nss_base.learner_cli import initialize, paths
from nss_base.learner_coordinator import LearnerCoordinator
from nss_base.neural_contracts import encoded
from nss_base.runtime import ContractError
ROOT=Path(__file__).resolve().parents[1]


class LearnerCliTests(LearnerCase):
    def cli(self, *args):
        cfg=self.root/'owners.json';cfg.write_bytes(encoded(self.config))
        return subprocess.run([sys.executable,'-m','nss_base.learner_cli','--config',str(cfg),*args],
            cwd=ROOT,capture_output=True,text=True,timeout=120)

    def test_cli_explicit_cycle_never_deploys(self):
        self.co.clock=lambda:int(time.time());p=plan_from_reviewed_data(self.co,steps=180)
        path=self.root/'learning-plan.json';path.write_bytes(encoded(p))
        for command in [('prepare','--plan',str(path)),('approve','--cycle','learn-001','--actor','human-operator',
                         '--expires-at',str(int(time.time())+600)),('advance','--cycle','learn-001','--caller','learner-worker')]:
            r=self.cli(*command);self.assertEqual(r.returncode,0,r.stdout+r.stderr)
        result=json.loads(r.stdout);self.assertFalse(result['proposal']['deployment_authorized'])
        before=self.co.training.audit()
        r=self.cli('check-proposal','--cycle','learn-001');self.assertEqual(r.returncode,2,r.stderr)
        self.assertEqual(json.loads(r.stdout)['status'],'INSUFFICIENT_EVIDENCE')
        r=self.cli('advance','--cycle','learn-001','--caller','learner-worker');self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(before,self.co.training.audit())
        r=self.cli('withdraw','--cycle','learn-001','--actor','human-operator','--reason','operator withdrew')
        self.assertEqual(r.returncode,0,r.stderr)
        r=self.cli('check-proposal','--cycle','learn-001');self.assertEqual(r.returncode,1)
        self.assertEqual(json.loads(r.stderr)['status'],'AUTHORIZATION_DENIED')
        self.assertEqual(self.cli('inspect','--cycle','learn-001').returncode,0)

    def test_cli_denial_does_not_dispatch(self):
        self.ready();r=self.cli('advance','--cycle','learn-001','--caller','unknown')
        self.assertEqual(r.returncode,1,r.stdout);self.assertEqual(json.loads(r.stderr)['status'],'AUTHORIZATION_DENIED')
        self.assertEqual(self.co.training.audit()['attempts'],0)

    def test_cli_duplicate_json_is_typed(self):
        path=self.root/'duplicate.json';path.write_text('{"schema_version":1,"schema_version":2}')
        r=self.cli('prepare','--plan',str(path));self.assertEqual(r.returncode,1)
        self.assertEqual(json.loads(r.stderr)['status'],'VALIDATION_FAILED')

    def test_initialization_never_overwrites_owners(self):
        from nss_base.boundedlearnercoordinator001 import OPERATORS
        before=self.co.cycles.inspect()
        self.error('CONSTRAINT_CONFLICT',initialize,self.config,OPERATORS)
        self.assertEqual(before,self.co.cycles.inspect())
        cfg=deepcopy(self.config);cfg['cycles']=cfg['candidates']
        self.error('VALIDATION_FAILED',initialize,cfg,OPERATORS)
        cfg=deepcopy(self.config);cfg['cycles']=str(Path(cfg['candidates'])/'nested')
        self.error('VALIDATION_FAILED',initialize,cfg,OPERATORS)

    def test_config_shapes_and_owner_types_fail_closed(self):
        for x in ({},dict(self.config,archive=[]),dict(self.config,extra='x')):
            with self.subTest(x=x):self.error('VALIDATION_FAILED',paths,x)
        kw=dict(archive=self.co.archive,snapshots=self.co.snapshots,tokenizer_path=self.co.tokenizer_path,
            source=self.co.source,qualifications=self.co.qualifications,training=self.co.training,evaluations=self.co.evaluations)
        self.error('VALIDATION_FAILED',LearnerCoordinator,object(),**kw)
        self.error('VALIDATION_FAILED',LearnerCoordinator,self.co.cycles,clock='python:eval',**kw)


class LearnerToolTests(unittest.TestCase):
    def test_public_gate_rejects_malformed_ids_as_typed_errors(self):
        import tempfile
        from nss_base.learner_store import LearningCycles
        from nss_base.boundedlearnercoordinator001 import OPERATORS
        with tempfile.TemporaryDirectory() as d:
            journal=LearningCycles.create(Path(d)/'cycles',OPERATORS)
            for value in ([],{},False,None):
                with self.subTest(value=value), self.assertRaises(ContractError):
                    journal.gate(value,'learner-worker',at=2000000000)

    def test_full_installed_inventory_fits_bounded_evaluation_schema(self):
        from nss_base.evaluation_inputs import implementation_identity
        from nss_base.serialization import _validate
        schema=json.loads((ROOT/'schemas/evaluation_material.schema.json').read_text())['properties']['implementation']
        identity=implementation_identity()
        expected={p.relative_to(ROOT).as_posix() for p in [*ROOT.glob('nss_base/*.py'),*ROOT.glob('schemas/*.json'),ROOT/'VERSION']}
        self.assertEqual({f['path'] for f in identity['files']},expected)
        self.assertGreater(len(identity['files']),128)
        _validate(identity,schema,'$.implementation')
        self.assertEqual(schema['properties']['files']['maxItems'],256)
        too_large=deepcopy(identity);too_large['files']=[identity['files'][0]]*257
        with self.assertRaises(ContractError):_validate(too_large,schema,'$.implementation')

    def test_schemas_and_logic_regenerate_exactly(self):
        paths=[*ROOT.glob('schemas/learner_*.json'),ROOT/'docs/BOUNDED_LEARNER_LOGIC.md',
            ROOT/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md',*ROOT.glob('docs/logic_flowcharts/learner_*.dot')]
        self.assertEqual(len(list(ROOT.glob('schemas/learner_*.json'))),5)
        before={p:p.read_bytes() for p in paths}
        for args in [('tools/generate_learner_schemas.py',),('tools/generate_subsystem_logic.py','--view','learner')]:
            r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(before,{p:p.read_bytes() for p in paths})

    def test_helper_graphs_have_no_qualification_or_deployment_authority(self):
        from nss_base.logic_atlas import load_atlas
        helpers=load_atlas(ROOT/'spec/bounded_learner_flows.json')
        self.assertEqual({f['id'] for f in helpers['flows']},{'learner_admission','learner_cycle','learner_recipe'})
        parent=load_atlas(ROOT/'spec/logic_atlas.json');self.assertEqual(len(parent['flows']),25)
        for name,status in {'context_manager':'research','recurrent_depth':'research','directional_guidance':'research-policy','darp':'research'}.items():
            self.assertEqual(next(f for f in parent['flows'] if f['id']==name)['status'],status)
        raw=json.dumps(helpers)
        self.assertIn('INSUFFICIENT_EVIDENCE',raw);self.assertIn('RECOVERY_REQUIRED',raw)

    def test_orchestrator_has_no_private_storage_or_release_shortcut(self):
        tree=ast.parse((ROOT/'nss_base/learner_coordinator.py').read_text())
        bad={'sqlite3','subprocess','requests','socket'}
        imports={a.name.split('.')[0] for n in ast.walk(tree) if isinstance(n,ast.Import) for a in n.names}
        self.assertFalse(imports & bad)
        for n in ast.walk(tree):
            if isinstance(n,ast.Attribute):self.assertNotIn(n.attr,('_db','review','issue','adopt','release','publish','revoke'))
        store=(ROOT/'nss_base/learner_store.py').read_text()
        self.assertNotIn('import sqlite3',store)

    def test_cli_help_and_dependency_check(self):
        for args in [('-m','nss_base.learner_cli','--help'),('tools/check_dependencies.py',)]:
            r=subprocess.run([sys.executable,*args],cwd=ROOT,capture_output=True,text=True,timeout=30)
            self.assertEqual(r.returncode,0,r.stderr+r.stdout)

    def test_connected_verifier_rejects_missing_evidence(self):
        import tempfile
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'summary.json';p.write_text('{"status":"SUCCESS"}')
            r=subprocess.run([sys.executable,'tools/verify_connected_alpha.py','--summary',str(p)],cwd=ROOT,
                capture_output=True,text=True,timeout=30)
            self.assertEqual(r.returncode,1)
