import importlib.util
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('dependency_checker',ROOT/'tools/check_dependencies.py')
checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)

class BoundaryTests(unittest.TestCase):
    def test_current_import_graph(self):
        self.assertEqual(checker.check(ROOT),[])

    def test_forbidden_relative_and_absolute_imports_are_detected(self):
        for statement in ('from .stage_handoff import handoff_stage','from nss_base.publication import RecoveryStore'):
            with self.subTest(statement=statement), TemporaryDirectory() as tmp:
                root=Path(tmp)
                shutil.copytree(ROOT/'nss_base',root/'nss_base',ignore=shutil.ignore_patterns('__pycache__'))
                (root/'spec').mkdir();shutil.copy(ROOT/'spec/python_dependencies.json',root/'spec/python_dependencies.json')
                path=root/'nss_base/task_records.py';path.write_text(path.read_text()+'\n'+statement+'\n')
                errors=checker.check(root)
                self.assertTrue(any('forbidden' in e for e in errors),errors)
                self.assertTrue(any('Circular' in e for e in errors),errors)

    def test_stage_demo(self):
        from nss_base.stagehandoff001 import run
        with TemporaryDirectory() as tmp:
            report=run(tmp)
        self.assertEqual(report['status'],'SUCCESS')
        self.assertEqual(report['profile_sequence'],['core','AB','A','core'])
        self.assertEqual(report['unit_after'],'m/s')
        self.assertEqual(report['committed_mock_effects'],1)
        self.assertTrue(report['exact_match'])

if __name__=='__main__':unittest.main()
