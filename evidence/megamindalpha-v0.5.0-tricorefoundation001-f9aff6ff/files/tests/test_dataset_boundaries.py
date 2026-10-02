"""Additional adversarial cases. Integrity checks do not authenticate a local operator."""
from contextlib import closing
import copy
import json
from pathlib import Path
import sqlite3
import threading
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from nss_base.dataset_store import DatasetSnapshots
from nss_base.experience_store import ExperienceArchive
from nss_base.runtime import ContractError
from dataset_helpers import ok, approved, capture_request, change, revoke, tokenizer, build_request


class BoundaryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.archive=ExperienceArchive.create(self.root/'archive');self.token_path,self.tok=tokenizer(self.root)
        self.store=DatasetSnapshots.create(self.root/'snapshots',archive=self.archive)
        self.ref=approved(self.archive);self.req=build_request([self.ref],self.tok)

    def build(self,req=None):return self.store.build(req or self.req,archive=self.archive,tokenizer_path=self.token_path)
    def read(self,r):return self.store.read_for_use(r['snapshot_id'],expected_manifest_hash=r['sha256'],purpose='training',split='train',archive=self.archive,tokenizer_path=self.token_path)

    def test_missing_revocation_index_row_must_not_restore_permission(self):
        receipt=ok(self.build());ok(revoke(self.archive))
        with closing(sqlite3.connect(self.archive.path)) as db, db:db.execute('DELETE FROM revocations')
        self.assertNotEqual(self.read(receipt)['status'],'SUCCESS')
        self.assertNotEqual(self.archive.read_for_use('exp1',purpose='training',expected_revision_hash=self.ref['sha256'])['status'],'SUCCESS')

    def test_revocation_index_cannot_be_repointed_away_from_affected_source(self):
        receipt=ok(self.build());ok(revoke(self.archive))
        with closing(sqlite3.connect(self.archive.path)) as db, db:db.execute("UPDATE revocations SET source_sha256=?",('f'*64,))
        self.assertNotEqual(self.read(receipt)['status'],'SUCCESS')

    def test_corrupted_revocation_event_blocks_consumption(self):
        receipt=ok(self.build());ok(revoke(self.archive))
        with closing(sqlite3.connect(self.archive.path)) as db, db:db.execute("UPDATE operations SET body='{}' WHERE kind='REVOKE_SOURCE'")
        self.assertEqual(self.read(receipt)['status'],'VALIDATION_FAILED')

    def test_batch_reads_exact_revisions_without_admin_inspection(self):
        with patch.object(self.archive,'inspect',side_effect=AssertionError('admin bypass')), \
             patch.object(self.archive,'inspect_source',side_effect=AssertionError('raw bypass')), \
             patch.object(self.archive,'history',side_effect=AssertionError('history bypass')):
            receipt=ok(self.build());ok(self.read(receipt))

    def test_batch_checks_are_one_consistent_archive_transaction(self):
        second=approved(self.archive,'exp2'); original=self.archive._lineage
        attempted=threading.Event(); committed=threading.Event(); writer=[]
        calls=0
        def write():
            attempted.set(); writer.append(revoke(self.archive,'exp2'));committed.set()
        threads=[]
        def observe(db,id):
            nonlocal calls
            result=original(db,id);calls+=1
            if calls==1:
                t=threading.Thread(target=write);threads.append(t);t.start()
                self.assertTrue(attempted.wait(2))
                self.assertFalse(committed.wait(.08),'Writer should wait for batch read transaction')
            return result
        with patch.object(self.archive,'_lineage',side_effect=observe):
            result=self.archive.read_batch_for_use([self.ref,second],purpose='training')
        for t in threads:t.join(10);self.assertFalse(t.is_alive())
        ok(result);ok(writer[0])
        self.assertEqual(self.archive.read_batch_for_use([self.ref,second],purpose='training')['status'],'TRAINING_RESTRICTED')

    def test_revocation_between_observation_and_publication_yields_nonusable_snapshot(self):
        original=self.archive.read_batch_for_use
        def observe_then_revoke(*args,**kw):
            result=original(*args,**kw);ok(revoke(self.archive));return result
        with patch.object(self.archive,'read_batch_for_use',side_effect=observe_then_revoke):receipt=ok(self.build())
        # Publication is not a durable lease. The immutable historical observation
        # is permitted to exist, but current-use gating must refuse it.
        self.assertEqual(self.read(receipt)['status'],'TRAINING_RESTRICTED')
        self.assertFalse(ok(self.store.inspect('snapshot1'))['use_authorized'])

    def test_consumption_is_rechecked_every_time(self):
        receipt=ok(self.build());first=ok(self.read(receipt));ok(revoke(self.archive))
        self.assertEqual(self.read(receipt)['status'],'TRAINING_RESTRICTED')
        # Already returned Python values cannot be remotely recalled.
        self.assertEqual(len(first['examples']),1)

    def test_unknown_or_future_store_schema_fails_closed(self):
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute("UPDATE metadata SET value='999' WHERE key='schema_version'")
        with self.assertRaises(ContractError):DatasetSnapshots(self.root/'snapshots')

    def test_missing_snapshot_db_not_recreated_on_read(self):
        receipt=ok(self.build());self.store.path.unlink()
        self.assertEqual(self.read(receipt)['status'],'RECOVERY_REQUIRED');self.assertFalse(self.store.path.exists())

    def test_malformed_db_file_open_is_typed(self):
        self.store.path.write_bytes(b'not a sqlite database')
        with self.assertRaises(ContractError):DatasetSnapshots(self.root/'snapshots')

    def test_orphan_operation_detected_by_audit(self):
        ok(self.build())
        with closing(sqlite3.connect(self.store.path)) as db, db:
            db.execute("INSERT INTO operations SELECT 'orphan',request_sha256,body,'missing',result_sha256 FROM operations LIMIT 1")
        self.assertNotEqual(self.store.audit()['status'],'SUCCESS')

    def test_operation_identity_corruption_rejected(self):
        receipt=ok(self.build())
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute("UPDATE operations SET request_sha256=?",('0'*64,))
        self.assertEqual(self.read(receipt)['status'],'VALIDATION_FAILED')

    def test_bad_ids_types_and_splits_fail_typed(self):
        receipt=ok(self.build())
        for value in [None,[],{},True,'../escape']:
            with self.subTest(v=value):
                self.assertEqual(self.store.inspect(value)['status'],'VALIDATION_FAILED')
                self.assertEqual(self.store.operation_receipt(value)['status'],'VALIDATION_FAILED')
        for split in [None,[],{},True,'test','release','TRAIN']:
            with self.subTest(split=split):
                self.assertEqual(self.store.read_for_use('snapshot1',expected_manifest_hash=receipt['sha256'],purpose='training',split=split,archive=self.archive,tokenizer_path=self.token_path)['status'],'VALIDATION_FAILED')
        for limit in [True,0,1001,None,{}]:self.assertEqual(self.store.list_snapshots(limit=limit)['status'],'VALIDATION_FAILED')

    def test_batch_invalid_requests_fail_typed(self):
        for refs in [None,{},[True],[],[self.ref,self.ref],[{**self.ref,'revision':True}]]:
            self.assertEqual(self.archive.read_batch_for_use(refs,purpose='training')['status'],'VALIDATION_FAILED')
        for p in [None,[],{},'evaluation']:self.assertEqual(self.archive.read_batch_for_use([self.ref],purpose=p)['status'],'VALIDATION_FAILED')

    def test_deep_nonfinite_and_cyclic_request_rejected(self):
        cases=[]
        r=copy.deepcopy(self.req);r['reason']=float('nan');cases.append(r)
        r=copy.deepcopy(self.req);r['reason']=r;cases.append(r)
        r=copy.deepcopy(self.req);x={};r['reason']=x
        for _ in range(27):x['x']={};x=x['x']
        cases.append(r)
        for r in cases:self.assertEqual(self.store.build(r,archive=self.archive,tokenizer_path=self.token_path)['status'],'VALIDATION_FAILED')

    def test_oversized_input_rejected_without_publication(self):
        r=copy.deepcopy(self.req);r['reason']='x'*(4*1024*1024+1)
        self.assertEqual(self.store.build(r,archive=self.archive,tokenizer_path=self.token_path)['status'],'VALIDATION_FAILED')
        self.assertEqual(ok(self.store.audit())['snapshots'],0)

    def test_unrecognized_fault_point_is_not_accepted(self):
        self.assertEqual(self.store.build(self.req,archive=self.archive,tokenizer_path=self.token_path,fault_at='guess')['status'],'VALIDATION_FAILED')

    def test_request_does_not_allow_executable_transform_or_implicit_latest(self):
        for key,value in [('transform','python:eval'),('purpose','redistribution')]:
            r=copy.deepcopy(self.req);r[key]=value;self.assertEqual(self.build(r)['status'],'VALIDATION_FAILED')
        r=copy.deepcopy(self.req);del r['members'][0]['sha256'];self.assertEqual(self.build(r)['status'],'VALIDATION_FAILED')

    def test_whitespace_example_rejected(self):
        r=approved(self.archive,'white',text=' \n\t ')
        self.assertEqual(self.build(build_request([r],self.tok,sid='white'))['status'],'VALIDATION_FAILED')

    def test_shared_ancestor_source_cannot_leak_across_splits(self):
        # Different primary evidence does not hide a common included parent.
        def add_common(id):
            current=ok(self.archive.inspect(id));src=copy.deepcopy(capture_request('shared')['evidence'][0]);src['id']='common'
            src['kind']='REFERENCE'
            ok(change(self.archive,id,'ANNOTATE',{'statement':{'text':current['record']['statement']['text'],'uncertainty':'LOW','support_ids':['source1','common']},'evidence':[src]}))
            ok(change(self.archive,id,'REVIEW',{'decision':'APPROVED'}))
            return ok(change(self.archive,id,'PERMISSION',{'purpose':'training','decision':'ALLOWED','permission_ref':'fixture:t'}))['reference']
        approved(self.archive,'exp2');a=add_common('exp1');b=add_common('exp2')
        self.assertEqual(self.build(build_request([a,b],self.tok))['status'],'CONSTRAINT_CONFLICT')


    def test_sql_failure_rolls_back_manifest_and_preserves_prior_dataset(self):
        receipt=ok(self.build());req=copy.deepcopy(self.req)
        req.update(snapshot_id='snapshot2',operation_id='build:2')
        with closing(sqlite3.connect(self.store.path)) as db, db:
            db.execute("CREATE TRIGGER inject_failure BEFORE INSERT ON operations BEGIN SELECT RAISE(ABORT,'fixture'); END")
        self.assertEqual(self.build(req)['status'],'INTERNAL_FAILURE')
        self.assertEqual(ok(self.store.audit())['snapshots'],1);ok(self.read(receipt))
        with closing(sqlite3.connect(self.store.path)) as db, db:db.execute('DROP TRIGGER inject_failure')
        ok(self.build(req));self.assertEqual(ok(self.store.audit())['snapshots'],2)

    def test_returned_values_cannot_mutate_published_manifest(self):
        receipt=ok(self.build());first=ok(self.store.inspect('snapshot1'))
        first['manifest']['members'][0]['text']='caller mutation'
        self.assertNotEqual(ok(self.store.inspect('snapshot1'))['manifest']['members'][0]['text'],'caller mutation')
        sample=ok(self.read(receipt));sample['examples'][0]['text']='caller mutation'
        self.assertNotEqual(ok(self.read(receipt))['examples'][0]['text'],'caller mutation')

    def test_invalid_archive_and_path_objects_are_typed(self):
        self.assertEqual(self.store.build(self.req,archive=None,tokenizer_path=self.token_path)['status'],'VALIDATION_FAILED')
        self.assertEqual(self.store.build(self.req,archive=self.archive,tokenizer_path={})['status'],'VALIDATION_FAILED')
        with self.assertRaises(ContractError):DatasetSnapshots(None)

    def test_duplicate_stored_json_field_fails_closed(self):
        receipt=ok(self.build())
        with closing(sqlite3.connect(self.store.path)) as db, db:
            raw=db.execute('SELECT body FROM snapshots').fetchone()[0]
            db.execute('UPDATE snapshots SET body=?',(raw[:-1]+',"schema_version":1}',))
        self.assertEqual(self.read(receipt)['status'],'VALIDATION_FAILED')

    def test_changed_approval_or_unrelated_permission_requires_explicit_rebuild(self):
        receipt=ok(self.build())
        ok(change(self.archive,'exp1','PERMISSION',{'purpose':'retrieval','decision':'ALLOWED','permission_ref':'fixture:new'}))
        # Conservative exact-revision selection does not silently follow even a
        # benign head update. An explicit rebuild is required in this prototype.
        self.assertEqual(self.read(receipt)['status'],'CONSTRAINT_CONFLICT')

    def test_actual_tokenizer_byte_budget_enforced(self):
        with patch('nss_base.dataset_store.MAX_TOKENIZER_BYTES',1):
            self.assertEqual(self.build()['status'],'BUDGET_EXHAUSTED')

    def test_partial_archive_batch_is_rejected_before_publication(self):
        original=self.archive.read_batch_for_use
        def incomplete(*args,**kwargs):
            result=original(*args,**kwargs);result['data']['views']=[];return result
        with patch.object(self.archive,'read_batch_for_use',side_effect=incomplete):
            self.assertEqual(self.build()['status'],'VALIDATION_FAILED')
        self.assertEqual(ok(self.store.audit())['snapshots'],0)


if __name__=='__main__':unittest.main()
