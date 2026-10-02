"""Shared tools stay deterministic and contracts remain documentation, not authority."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from nss_base.logic_atlas import load_atlas
ROOT=Path(__file__).resolve().parents[1]


class CatalogToolingTests(unittest.TestCase):
    def test_helper_graphs_have_history_exits_and_no_deployment(self):
        a=load_atlas(ROOT/'spec/overlay_catalog_flows.json')
        self.assertEqual({f['id'] for f in a['flows']},{'catalog_select','catalog_task_handoff','catalog_task_completion'})
        for f in a['flows'][1:]:
            self.assertTrue(any(e['when']=='yes_history_only' and e['to']=='done' for e in f['transitions']))
            self.assertIn('HISTORY_ONLY','\n'.join(f['pseudocode']))

    def test_schemas_and_shared_renderer_regenerate_identically(self):
        paths=[*ROOT.glob('schemas/catalog_*.json'),ROOT/'docs/OVERLAY_CATALOG_LOGIC.md',
            ROOT/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md',*ROOT.glob('docs/logic_flowcharts/catalog_*.dot')]
        before={str(p):p.read_bytes() for p in paths}
        for script,args in [('tools/generate_subsystem_logic.py',['--view','catalog']),('tools/generate_generation_schemas.py',[])]:
            r=subprocess.run([sys.executable,script,*args],cwd=ROOT,capture_output=True,text=True,timeout=60)
            self.assertEqual(r.returncode,0,r.stderr)
        self.assertEqual(before,{str(p):p.read_bytes() for p in paths})

    def test_schema_export_has_explicit_action_and_cost_units(self):
        d=json.loads((ROOT/'schemas/catalog_descriptor.schema.json').read_text())
        self.assertEqual(d['properties']['claim_scope']['const'],'REVIEWED_ROUTING_FIXTURE_NOT_NEW_NEURAL_EVIDENCE')
        c=json.loads((ROOT/'schemas/catalog_command.schema.json').read_text())
        self.assertEqual({s['properties']['action']['const'] for s in c['oneOf']},{'START','MOVE','FINISH','CLOSE','CANCEL'})

    def test_cli_help_does_not_train_or_execute(self):
        p=subprocess.run([sys.executable,'-m','nss_base.catalog_cli','--help'],cwd=ROOT,capture_output=True,text=True,timeout=60)
        self.assertEqual(p.returncode,0,p.stderr);self.assertIn('catalog',p.stdout)
