from contextlib import closing
"""Synthetic local software-test helpers. No model or real human judgment."""
from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from nss_base.dataset_store import DatasetSnapshots
from nss_base.evaluation_store import EvaluationRuns
from nss_base.evaluationrun001 import plan_for, FIXTURE
from nss_base.experience_store import ExperienceArchive
from nss_base.runtime import digest
from dataset_helpers import ok, approved, tokenizer, build_request

ROOT=Path(__file__).resolve().parents[1]

class EvaluationCase(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.inputs=self.root/'inputs';shutil.copytree(FIXTURE,self.inputs)
        self.store=EvaluationRuns.create(self.root/'evaluations');self.plan=plan_for(self.inputs,'run-1')
        self.kw={'root':self.inputs}

    def execute(self,plan=None):return self.store.execute(plan or self.plan,**self.kw)
    def inspect(self):return ok(self.store.inspect(self.plan['run_id']))
    def report(self):return self.inspect()['report']
    def verify(self):
        r=self.inspect()['receipt'];return self.store.verify_current(r['run_id'],expected_report_sha256=r['report_sha256'],**self.kw)
    def rehash_suite(self):
        self.plan['suite']['sha256']=sha256((self.inputs/'suite.json').read_bytes()).hexdigest()
    def edit_suite(self,edit):
        path=self.inputs/'suite.json';s=json.loads(path.read_text());edit(s);path.write_text(json.dumps(s));self.rehash_suite()
    def add_dataset(self):
        self.archive=ExperienceArchive.create(self.root/'archive')
        refs=[approved(self.archive,'train'),approved(self.archive,'val')]
        self.token_path,self.token=tokenizer(self.root)
        self.snapshots=DatasetSnapshots.create(self.root/'snapshots',archive=self.archive)
        req=build_request(refs,self.token)
        ref=ok(self.snapshots.build(req,archive=self.archive,tokenizer_path=self.token_path))
        self.plan['development_snapshot']={k:ref[k] for k in ('snapshot_id','sha256')}
        self.plan['development_snapshot']['split']='validation'
        self.kw.update(snapshots=self.snapshots,archive=self.archive,tokenizer_path=self.token_path)
        return ref

    def tamper_report(self,edit,*,rehash=False,receipt=False):
        import sqlite3
        with closing(sqlite3.connect(self.store.path)) as db, db:
            row=db.execute('SELECT report FROM runs WHERE id=?',(self.plan['run_id'],)).fetchone()
            report=json.loads(row[0]);edit(report)
            if rehash:db.execute('UPDATE runs SET report=?,report_sha256=? WHERE id=?',(json.dumps(report),digest(report),self.plan['run_id']))
            else:db.execute('UPDATE runs SET report=? WHERE id=?',(json.dumps(report),self.plan['run_id']))
            if receipt:
                r=json.loads(db.execute('SELECT body FROM receipts WHERE run_id=?',(self.plan['run_id'],)).fetchone()[0])
                r['report_sha256']=digest(report);db.execute('UPDATE receipts SET body=? WHERE run_id=?',(json.dumps(r),self.plan['run_id']))
