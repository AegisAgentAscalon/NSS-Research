import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from permission_helpers import PermissionCase
from nss_base.neural_contracts import fingerprint
ROOT=Path(__file__).resolve().parents[1]

class PermissionCliPureTests(unittest.TestCase):
    def test_help_is_available(self):
        r=subprocess.run([sys.executable,'-m','nss_base.permission_cli','--help'],cwd=ROOT,capture_output=True,text=True)
        self.assertEqual(r.returncode,0);self.assertIn('reconcile',r.stdout)
    def test_missing_store_is_not_created_by_audit(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'missing'
            r=subprocess.run([sys.executable,'-m','nss_base.permission_cli','--store',str(p),'audit'],cwd=ROOT,capture_output=True,text=True)
            self.assertEqual(r.returncode,1);self.assertFalse(p.exists())
            self.assertEqual(json.loads(r.stderr)['status'],'RECOVERY_REQUIRED')

class PermissionCliIntegrationTests(PermissionCase):
    def cli(self,*args):
        r=subprocess.run([sys.executable,'-m','nss_base.permission_cli','--store',str(self.root/'permissions'),*map(str,args)],cwd=ROOT,capture_output=True,text=True,timeout=120)
        return r,json.loads(r.stdout if r.returncode==0 else r.stderr)
    def test_inspect_does_not_renew_permission(self):
        self.issue();r,o=self.cli('inspect','--request-id','permission-1')
        self.assertEqual(r.returncode,0);self.assertTrue(o['historical']);self.assertFalse(o['runtime_execution_permit'])
    def test_cli_denies_unknown_actor(self):
        self.clock-=10
        p=self.root/'operation.json';p.write_text(json.dumps(self.operation))
        r,o=self.cli('issue','--request',p,'--issuer','unknown','--qualifications',self.root/'q','--journal',self.root/'probe/journal','--data',self.root/'probe/data')
        self.assertEqual(r.returncode,1);self.assertEqual(o['status'],'AUTHORIZATION_DENIED')
    def test_cli_reconcile_abandons_without_executing(self):
        h=self.granted();self.begin(h);p=self.root/'operation.json';p.write_text(json.dumps(self.operation))
        r,o=self.cli('reconcile','--request',p,'--grant-sha256',h,'--actor','local-owner','--executor',self.root/'executor')
        self.assertEqual(r.returncode,0);self.assertEqual(o['status'],'ABANDONED')
        self.assertEqual(self.executor.audit()['committed_results'],0)
