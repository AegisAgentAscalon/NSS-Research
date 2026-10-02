import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from nss_base.experience_store import ExperienceArchive
from test_experiencearchive001 import capture,evidence,HUMAN,AT

ROOT=Path(__file__).resolve().parents[1]

class CrashTests(unittest.TestCase):
    def crash(self,path,kind,req,point):
        file=path.parent/'request.json';file.write_text(json.dumps(req))
        child=subprocess.run([sys.executable,str(ROOT/'tests/experience_crash_worker.py'),str(path),kind,str(file),point],capture_output=True,text=True,timeout=10)
        self.assertEqual(child.returncode,74,(child.returncode,child.stdout,child.stderr))

    def test_capture_process_crash_windows_are_atomic_and_retryable(self):
        for point in ('after_blobs','after_revision','after_head','before_commit','after_commit'):
            with self.subTest(point=point),TemporaryDirectory() as temp:
                path=Path(temp)/'archive';ExperienceArchive.create(path)
                self.crash(path,'capture',capture(),point)
                store=ExperienceArchive(path);report=store.audit();self.assertEqual(report['status'],'SUCCESS',report)
                expected=1 if point=='after_commit' else 0
                self.assertEqual(report['data']['records'],expected)
                self.assertEqual(report['data']['revisions'],expected)
                self.assertEqual(report['data']['evidence_blobs'],expected)
                result=store.capture(capture());self.assertEqual(result['status'],'SUCCESS',result)
                self.assertEqual(result['replayed'],point=='after_commit')
                self.assertEqual(store.audit()['data']['records'],1)

    def test_review_process_crash_windows_leave_old_or_complete_new_revision(self):
        for point in ('after_blobs','after_revision','after_head','before_commit','after_commit'):
            with self.subTest(point=point),TemporaryDirectory() as temp:
                path=Path(temp)/'archive';s=ExperienceArchive.create(path);head=s.capture(capture())['data']['reference']['sha256']
                req={'schema_version':1,'operation_id':'review:1','experience_id':'exp1','expected_revision_hash':head,
                    'actor':HUMAN,'at':AT,'reason':'Human fixture approval.','action':'REVIEW','payload':{'decision':'APPROVED'}}
                self.crash(path,'change',req,point);s=ExperienceArchive(path)
                expected=1 if point=='after_commit' else 0
                current=s.inspect('exp1');self.assertEqual(current['status'],'SUCCESS',current)
                self.assertEqual(current['data']['record']['revision'],expected)
                result=s.change(req);self.assertEqual(result['status'],'SUCCESS',result)
                self.assertEqual(s.inspect('exp1')['data']['record']['revision'],1)
                self.assertEqual(s.audit()['status'],'SUCCESS')

    def test_source_revocation_crash_is_atomic(self):
        for point in ('after_revision','before_commit','after_commit'):
            with self.subTest(point=point),TemporaryDirectory() as temp:
                path=Path(temp)/'archive';s=ExperienceArchive.create(path);s.capture(capture())
                req={'schema_version':1,'operation_id':'source-revoke:1','actor':HUMAN,'at':AT,
                    'reason':'Permission removed.','permission_ref':'fixture:owner','source_sha256':evidence()['sha256'],'purpose':'training'}
                self.crash(path,'revoke',req,point);s=ExperienceArchive(path)
                self.assertEqual(s.audit()['data']['source_revocations'],int(point=='after_commit'))
                self.assertEqual(s.revoke_source(req)['status'],'SUCCESS')
                self.assertEqual(s.audit()['data']['source_revocations'],1)
