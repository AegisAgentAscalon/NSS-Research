"""Static guardrails; these do not replace behavioral tests or sandboxing."""
import ast
from pathlib import Path
import unittest
from nss_base.logic_atlas import load_atlas
ROOT=Path(__file__).resolve().parents[1]

class SpecBoundaryTests(unittest.TestCase):
    def test_parent_atlas_and_two_helper_flows_validate(self):
        self.assertEqual(len(load_atlas()['flows']),25)
        atlas=load_atlas(ROOT/'spec/dataset_snapshot_flows.json')
        self.assertEqual({f['id'] for f in atlas['flows']},{'dataset_snapshot_build','dataset_snapshot_read'})

    def test_only_store_owns_dataset_sql_and_no_archive_private_access(self):
        for name in ('dataset_contracts','dataset_store','dataset_cli','datasetsnapshot001'):
            tree=ast.parse((ROOT/'nss_base'/f'{name}.py').read_text())
            for n in ast.walk(tree):
                if isinstance(n,ast.Import) and any(a.name=='sqlite3' for a in n.names):self.assertEqual(name,'dataset_store')
                if isinstance(n,ast.Attribute) and isinstance(n.value,ast.Name) and n.value.id=='archive':
                    self.assertFalse(n.attr.startswith('_'),f'Private reach-through in {name}: {n.attr}')

    def test_schema_limits_match_runtime_contract(self):
        import json
        from nss_base.dataset_contracts import MAX_MEMBERS
        schema=json.loads((ROOT/'schemas/dataset_build.schema.json').read_text())
        self.assertEqual(schema['properties']['members']['maxItems'],MAX_MEMBERS)
        self.assertEqual(schema['properties']['purpose']['enum'],['training'])
        self.assertEqual(schema['properties']['members']['items']['properties']['split']['enum'],['train','validation'])

if __name__=='__main__':unittest.main()
