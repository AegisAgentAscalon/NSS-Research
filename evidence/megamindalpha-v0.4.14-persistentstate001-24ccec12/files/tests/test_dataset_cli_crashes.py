"""CLI, process-death and connected pipeline acceptance tests."""
import copy
import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from nss_base.dataset_store import DatasetSnapshots
from nss_base.experience_store import ExperienceArchive
from dataset_helpers import ok, approved, revoke, tokenizer, build_request

ROOT=Path(__file__).resolve().parents[1]


class CLITests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.archive=ExperienceArchive.create(self.root/'archive');self.ref=approved(self.archive)
        self.token_path,self.token=tokenizer(self.root)
        self.req=build_request([self.ref],self.token);self.request=self.root/'request.json'
        self.request.write_text(json.dumps(self.req))

    def cli(self,*args,expect=0):
        p=subprocess.run([sys.executable,'-m','nss_base.dataset_cli','--store',str(self.root/'snapshots'),
            '--archive',str(self.root/'archive'),*map(str,args)],cwd=ROOT,text=True,capture_output=True,timeout=20)
        self.assertEqual(p.returncode,expect,p.stdout+p.stderr)
        return json.loads(p.stdout)

    def test_cli_build_inspect_read_and_revocation(self):
        self.cli('init');receipt=ok(self.cli('build',self.request,'--tokenizer',self.token_path))
        self.assertFalse(ok(self.cli('inspect','snapshot1'))['use_authorized'])
        ok(self.cli('read','snapshot1','--expected',receipt['sha256'],'--tokenizer',self.token_path,'--split','train'))
        ok(revoke(self.archive))
        r=self.cli('read','snapshot1','--expected',receipt['sha256'],'--tokenizer',self.token_path,'--split','train',expect=2)
        self.assertEqual(r['status'],'TRAINING_RESTRICTED')
        self.cli('audit');self.cli('receipt','build:snapshot1');self.cli('list')

    def test_cli_prepare_is_not_build_or_approval(self):
        req=self.cli('prepare-build','--snapshot-id','manual','--operation-id','build:manual',
            '--reviewer','operator','--reason','Selected explicitly.', '--tokenizer',self.token_path,
            '--tokenizer-id','fixture','--tokenizer-version','1','--train','exp1')
        self.assertEqual(req['members'][0]['sha256'],self.ref['sha256'])
        self.assertFalse((self.root/'snapshots').exists())
        self.assertEqual(ok(self.archive.inspect('exp1'))['reference'],self.ref)

    def test_cli_preparation_can_use_unapproved_ref_but_build_blocks(self):
        from dataset_helpers import capture_request
        ok(self.archive.capture(capture_request('pending')))
        req=self.cli('prepare-build','--snapshot-id','manual','--operation-id','build:manual',
            '--reviewer','operator','--reason','Needs approval.', '--tokenizer',self.token_path,
            '--tokenizer-id','fixture','--tokenizer-version','1','--train','pending')
        self.request.write_text(json.dumps(req));self.cli('init')
        self.assertEqual(self.cli('build',self.request,'--tokenizer',self.token_path,expect=2)['status'],'CONFLICT_REQUIRES_REVIEW')

    def test_cli_never_initializes_on_inspect(self):
        r=self.cli('inspect','snapshot1',expect=2);self.assertEqual(r['status'],'RECOVERY_REQUIRED')
        self.assertFalse((self.root/'snapshots').exists())

    def test_cli_duplicate_json_keys_rejected(self):
        self.cli('init');raw=json.dumps(self.req);self.request.write_text(raw[:-1]+',"purpose":"training"}')
        self.assertEqual(self.cli('build',self.request,'--tokenizer',self.token_path,expect=2)['status'],'VALIDATION_FAILED')

    def test_cli_oversized_deep_nonfinite_requests_rejected(self):
        self.cli('init')
        for raw in ['{'+'"a":'*0, '['*1500+'0'+']'*1500, '{"x":NaN}', 'x'*(4*1024*1024+1)]:
            self.request.write_text(raw)
            self.assertEqual(self.cli('build',self.request,'--tokenizer',self.token_path,expect=2)['status'],'VALIDATION_FAILED')

    def test_cli_wrong_tokenizer_returns_nonzero_not_success(self):
        self.cli('init');self.token_path.write_text('different')
        self.assertEqual(self.cli('build',self.request,'--tokenizer',self.token_path,expect=2)['status'],'VALIDATION_FAILED')


class CrashTests(unittest.TestCase):
    def test_real_process_death_before_and_after_publication(self):
        for point in ('after_manifest','after_operation','before_commit','after_commit'):
            with self.subTest(point=point), TemporaryDirectory() as directory:
                root=Path(directory);archive=ExperienceArchive.create(root/'archive');ref=approved(archive)
                token_path,tok=tokenizer(root);store=DatasetSnapshots.create(root/'snapshots',archive=archive)
                request=build_request([ref],tok);(root/'request.json').write_text(json.dumps(request))
                p=subprocess.run([sys.executable,str(ROOT/'tests/dataset_crash_worker.py'),str(root),point],cwd=ROOT,capture_output=True,text=True,timeout=20)
                self.assertEqual(p.returncode,76,p.stdout+p.stderr)
                store=DatasetSnapshots(root/'snapshots');counts=ok(store.audit())
                expected=1 if point=='after_commit' else 0
                self.assertEqual(counts['snapshots'],expected);self.assertEqual(counts['operations'],expected)
                result=store.build(request,archive=archive,tokenizer_path=token_path)
                receipt=ok(result);self.assertEqual(result['replayed'],point=='after_commit')
                self.assertEqual(ok(store.audit())['snapshots'],1)
                ok(store.read_for_use('snapshot1',expected_manifest_hash=receipt['sha256'],purpose='training',split='train',archive=archive,tokenizer_path=token_path))
                substituted=copy.deepcopy(request);substituted['reason']='Changed after crash.'
                self.assertEqual(store.build(substituted,archive=archive,tokenizer_path=token_path)['status'],'CONSTRAINT_CONFLICT')

    def test_crash_replay_rechecks_revocation_before_new_publication(self):
        with TemporaryDirectory() as directory:
            root=Path(directory);archive=ExperienceArchive.create(root/'archive');ref=approved(archive)
            token_path,tok=tokenizer(root);store=DatasetSnapshots.create(root/'snapshots',archive=archive)
            request=build_request([ref],tok);(root/'request.json').write_text(json.dumps(request))
            p=subprocess.run([sys.executable,str(ROOT/'tests/dataset_crash_worker.py'),str(root),'after_manifest'],cwd=ROOT,capture_output=True,text=True,timeout=20)
            self.assertEqual(p.returncode,76,p.stdout+p.stderr);ok(revoke(archive))
            self.assertEqual(store.build(request,archive=archive,tokenizer_path=token_path)['status'],'TRAINING_RESTRICTED')
            self.assertEqual(ok(store.audit())['snapshots'],0)

    def test_committed_crash_retry_does_not_regrant_use(self):
        with TemporaryDirectory() as directory:
            root=Path(directory);archive=ExperienceArchive.create(root/'archive');ref=approved(archive)
            token_path,tok=tokenizer(root);store=DatasetSnapshots.create(root/'snapshots',archive=archive)
            request=build_request([ref],tok);(root/'request.json').write_text(json.dumps(request))
            p=subprocess.run([sys.executable,str(ROOT/'tests/dataset_crash_worker.py'),str(root),'after_commit'],cwd=ROOT,capture_output=True,text=True,timeout=20)
            self.assertEqual(p.returncode,76,p.stdout+p.stderr);ok(revoke(archive))
            result=store.build(request,archive=archive,tokenizer_path=token_path);ref=ok(result)
            self.assertTrue(result['historical'])
            self.assertEqual(store.read_for_use('snapshot1',expected_manifest_hash=ref['sha256'],purpose='training',split='train',archive=archive,tokenizer_path=token_path)['status'],'TRAINING_RESTRICTED')


class IntegrationTests(unittest.TestCase):
    def test_complete_synthetic_pipeline_and_revocation(self):
        from nss_base.datasetsnapshot001 import run
        with TemporaryDirectory() as directory:
            r=run(directory)
            self.assertEqual(r['status'],'SUCCESS');self.assertEqual(r['committed_mock_effects'],1)
            self.assertTrue(r['runtime_checkpoint_unchanged']);self.assertTrue(r['old_manifest_unchanged'])
            self.assertEqual(r['read_old_after_correction'],'CONSTRAINT_CONFLICT')
            self.assertEqual(r['read_rebuilt_after_revocation'],'TRAINING_RESTRICTED')
            self.assertEqual(r['snapshot_audit']['snapshots'],2)


if __name__=='__main__':unittest.main()
