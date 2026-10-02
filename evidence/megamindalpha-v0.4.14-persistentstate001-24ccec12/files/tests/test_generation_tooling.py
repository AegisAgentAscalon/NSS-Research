"""Regeneration, cleanup and shared-journal regressions without fabricated neural scores."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
from nss_base.logic_atlas import load_atlas
ROOT=Path(__file__).resolve().parents[1]


class GenerationToolingTests(unittest.TestCase):
    def test_helper_graphs_have_exact_scope_and_known_exits(self):
        a=load_atlas(ROOT/'spec/overlay_generation_flows.json')
        self.assertEqual({f['id'] for f in a['flows']},{'generation_family_qualify','generation_release','generation_managed_stage'})
        text='\n'.join('\n'.join(f['pseudocode']) for f in a['flows'])
        self.assertIn('HISTORY_WITHOUT_PUBLICATION',text);self.assertIn('no_open_managed_stage',text)

    def test_single_renderer_and_generation_schemas_regenerate_identically(self):
        paths=[*ROOT.glob('schemas/generation_*.json'),ROOT/'docs/OVERLAY_GENERATION_LOGIC.md',
               ROOT/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md',*ROOT.glob('docs/logic_flowcharts/generation_*.dot')]
        before={str(p):p.read_bytes() for p in paths}
        for command in (['tools/generate_subsystem_logic.py'],['tools/generate_generation_schemas.py']):
            p=subprocess.run([sys.executable,*command],cwd=ROOT,capture_output=True,text=True,timeout=30)
            self.assertEqual(p.returncode,0,p.stderr)
        self.assertEqual(before,{str(p):p.read_bytes() for p in paths})

    def test_old_one_off_converter_and_duplicate_renderers_are_removed(self):
        for name in ['update_review_doc.py',*[f'generate_{k}_logic_docs.py' for k in ('dataset','evaluation','neural','qualification','permission')]]:
            self.assertFalse((ROOT/'tools'/name).exists(),name)
        self.assertTrue((ROOT/'tools/logic_views.py').exists())

    def test_direct_atlas_validator_is_usable_outside_repo_cwd(self):
        p=subprocess.run([sys.executable,str(ROOT/'tools/validate_logic_atlas.py')],cwd=ROOT.parent,capture_output=True,text=True,timeout=30)
        self.assertEqual(p.returncode,0,p.stderr)

    def test_generation_grant_schema_cannot_be_replay_permission(self):
        s=json.loads((ROOT/'schemas/generation_release_grant.schema.json').read_text())
        self.assertFalse(s['properties']['runtime_execution_permit']['const'])
        self.assertTrue(s['properties']['catalog_publication_authorized']['const'])
        r=json.loads((ROOT/'schemas/generation_release_request.schema.json').read_text())
        self.assertEqual(r['properties']['operation']['const'],'PUBLISH_LOCAL_OVERLAY_GENERATION')
