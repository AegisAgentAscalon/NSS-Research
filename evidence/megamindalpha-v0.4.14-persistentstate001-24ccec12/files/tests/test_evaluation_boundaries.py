"""Architecture/fixture/schema guardrails; not a sandbox or independent audit."""
import ast
import json
from pathlib import Path
import subprocess
import sys
import unittest
from nss_base.logic_atlas import load_atlas
from evaluation_helpers import EvaluationCase, ROOT, ok

class EvaluationBoundaryTests(unittest.TestCase):
    def test_all_parent_and_subordinate_flow_counts(self):
        self.assertEqual(len(load_atlas()['flows']),25)
        self.assertEqual(len(load_atlas(ROOT/'spec/dataset_snapshot_flows.json')['flows']),2)
        self.assertEqual({f['id'] for f in load_atlas(ROOT/'spec/evaluation_run_flows.json')['flows']},
            {'evaluation_prepare','evaluation_execute','evaluation_current_use'})

    def test_new_runtime_modules_obey_explicit_dependency_allowlist(self):
        p=subprocess.run([sys.executable,'tools/check_dependencies.py'],cwd=ROOT,capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)

    def test_only_evaluation_store_owns_sql_and_no_dynamic_execution(self):
        for path in (ROOT/'nss_base').glob('evaluation*.py'):
            tree=ast.parse(path.read_text())
            for node in ast.walk(tree):
                if isinstance(node,ast.Import) and any(a.name=='sqlite3' for a in node.names):self.assertEqual(path.stem,'evaluation_store')
                if isinstance(node,ast.Call) and isinstance(node.func,ast.Name):
                    self.assertNotIn(node.func.id,('eval','exec','__import__'))
                if isinstance(node,ast.Import):self.assertFalse(any(a.name in ('subprocess','pickle','requests') for a in node.names))

    def test_no_private_archive_or_snapshot_consumption_bypass(self):
        for path in (ROOT/'nss_base').glob('evaluation*.py'):
            if path.stem=='evaluationrun001':continue # Demo uses admin metadata only to construct explicit reviewed fixtures.
            for node in ast.walk(ast.parse(path.read_text())):
                if isinstance(node,ast.Attribute) and isinstance(node.value,ast.Name) and node.value.id in ('archive','snapshots'):
                    self.assertNotIn(node.attr,('inspect','inspect_source','history','path','_db','_stored'))
                    self.assertFalse(node.attr.startswith('_'))

    def test_schema_regeneration_is_byte_identical(self):
        paths=sorted((ROOT/'schemas').glob('evaluation_*.schema.json'));before=[p.read_bytes() for p in paths]
        p=subprocess.run([sys.executable,'tools/generate_evaluation_schemas.py'],cwd=ROOT,capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(before,[p.read_bytes() for p in paths])

    def test_logic_regeneration_is_byte_identical(self):
        paths=[ROOT/'docs/EVALUATION_RUN_LOGIC.md',ROOT/'docs/PSEUDOCODE_FLOWCHART_ATLAS.md',*sorted((ROOT/'docs/logic_flowcharts').glob('evaluation_*.dot'))]
        before=[p.read_bytes() for p in paths]
        p=subprocess.run([sys.executable,'tools/generate_subsystem_logic.py','--view','evaluation'],cwd=ROOT,capture_output=True,text=True,timeout=20)
        self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(before,[p.read_bytes() for p in paths])

    def test_budget_and_scope_schema_match_implemented_limits(self):
        suite=json.loads((ROOT/'schemas/evaluation_suite.schema.json').read_text())
        plan=json.loads((ROOT/'schemas/evaluation_plan.schema.json').read_text())
        self.assertEqual(suite['properties']['purpose']['enum'],['DEVELOPMENT_SYNTHETIC'])
        self.assertEqual(suite['properties']['tests']['maxItems'],32)
        self.assertEqual(plan['properties']['max_evaluations']['maximum'],160)
        self.assertEqual(plan['properties']['repeats']['maximum'],5)
