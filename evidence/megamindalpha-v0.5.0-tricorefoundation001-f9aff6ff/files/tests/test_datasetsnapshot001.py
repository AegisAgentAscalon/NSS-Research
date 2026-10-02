"""Acceptance specifications written before DatasetSnapshot001 implementation."""
import copy
from contextlib import closing
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
from tempfile import TemporaryDirectory
import unittest

from nss_base.dataset_store import DatasetSnapshots
from nss_base.dataset_contracts import normalize_request, validate_manifest
from nss_base.experience_store import ExperienceArchive
from nss_base.runtime import ContractError, digest
from dataset_helpers import AT, HUMAN, MODEL, ok, approved, capture_request, change, revoke, tokenizer, build_request


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.archive = ExperienceArchive.create(self.root / 'archive')
        self.token_path, self.token = tokenizer(self.root)
        self.store = DatasetSnapshots.create(self.root / 'snapshots', archive=self.archive)

    def req(self, n=1, **kw):
        return build_request([approved(self.archive, f'exp{i}') for i in range(n)], self.token, **kw)

    def build(self, req, **kw):
        return self.store.build(req, archive=self.archive, tokenizer_path=self.token_path, **kw)

    def read(self, receipt, **kw):
        return self.store.read_for_use(receipt['snapshot_id'], expected_manifest_hash=receipt['sha256'],
            purpose='training', split=kw.pop('split', 'train'), archive=kw.pop('archive', self.archive),
            tokenizer_path=kw.pop('tokenizer_path', self.token_path), **kw)

    def test_build_is_fixed_and_source_linked(self):
        req = self.req(2); prior = copy.deepcopy(req)
        receipt = ok(self.build(req)); self.assertEqual(req, prior)
        manifest = ok(self.store.inspect(receipt['snapshot_id']))['manifest']
        self.assertEqual(digest(manifest), receipt['sha256'])
        self.assertEqual([m['view']['reference'] for m in manifest['members']],
                         [{k: v for k, v in m.items() if k != 'split'} for m in req['members']])
        self.assertEqual(manifest['members'][0]['view']['permission']['status'], 'ALLOWED')
        self.assertEqual(ok(self.read(receipt))['examples'][0]['text'], manifest['members'][0]['text'])
        self.assertEqual(ok(self.store.audit())['snapshots'], 1)

    def test_pending_record_not_training_data(self):
        ref = ok(self.archive.capture(capture_request()))['reference']
        self.assertEqual(self.build(build_request([ref], self.token))['status'], 'CONFLICT_REQUIRES_REVIEW')
        self.assertEqual(ok(self.store.audit())['snapshots'], 0)

    def test_approved_without_training_permission_is_blocked(self):
        ok(self.archive.capture(capture_request())); ref = ok(change(self.archive, 'exp1','REVIEW',{'decision':'APPROVED'}))['reference']
        self.assertEqual(self.build(build_request([ref], self.token))['status'], 'TRAINING_RESTRICTED')

    def test_retrieval_permission_is_not_training(self):
        ok(self.archive.capture(capture_request())); ok(change(self.archive,'exp1','REVIEW',{'decision':'APPROVED'}))
        ref = ok(change(self.archive,'exp1','PERMISSION',{'purpose':'retrieval','decision':'ALLOWED','permission_ref':'fixture:r'}))['reference']
        self.assertEqual(self.build(build_request([ref],self.token))['status'],'TRAINING_RESTRICTED')

    def test_no_silent_skipping_of_denied_member(self):
        req = self.req(2); ok(revoke(self.archive,'exp1'))
        self.assertEqual(self.build(req)['status'],'TRAINING_RESTRICTED')
        self.assertEqual(ok(self.store.audit())['snapshots'],0)

    def test_record_correction_preserves_snapshot_but_blocks_old_use(self):
        req = self.req(); receipt = ok(self.build(req)); old = ok(self.store.inspect('snapshot1'))
        ok(change(self.archive,'exp0','CORRECT',{'statement':{'text':'Corrected: speed is 12 m/s.','uncertainty':'LOW','support_ids':['source1']},'evidence':[]}))
        self.assertEqual(ok(self.store.inspect('snapshot1')),old)
        self.assertEqual(self.read(receipt)['status'],'CONSTRAINT_CONFLICT')
        ok(change(self.archive,'exp0','REVIEW',{'decision':'APPROVED'}))
        ref=ok(change(self.archive,'exp0','PERMISSION',{'purpose':'training','decision':'ALLOWED','permission_ref':'fixture:new'}))['reference']
        new=ok(self.build(build_request([ref],self.token,sid='snapshot2')))
        self.assertEqual(ok(self.read(new))['examples'][0]['text'],'Corrected: speed is 12 m/s.')
        self.assertEqual(ok(self.store.inspect('snapshot1')),old)

    def test_unrelated_archive_growth_does_not_mutate_or_block(self):
        receipt=ok(self.build(self.req())); old=ok(self.store.inspect('snapshot1'))
        approved(self.archive,'other')
        self.assertEqual(ok(self.store.inspect('snapshot1')),old);ok(self.read(receipt))

    def test_source_revocation_blocks_after_reopen(self):
        receipt=ok(self.build(self.req())); old=ok(self.store.inspect('snapshot1'))
        ok(revoke(self.archive,'exp0'))
        self.archive=ExperienceArchive(self.root/'archive'); self.store=DatasetSnapshots(self.root/'snapshots')
        self.assertEqual(self.read(receipt)['status'],'TRAINING_RESTRICTED')
        self.assertEqual(ok(self.store.inspect('snapshot1')),old)

    def test_revocation_of_validation_member_blocks_training_split_too(self):
        receipt=ok(self.build(self.req(2)));ok(revoke(self.archive,'exp1'))
        self.assertEqual(self.read(receipt)['status'],'TRAINING_RESTRICTED')

    def test_unrelated_purpose_revocation_does_not_block_training(self):
        receipt=ok(self.build(self.req()));ok(revoke(self.archive,'exp0',purpose='redistribution'))
        ok(self.read(receipt))

    def test_withdrawal_blocks_snapshot(self):
        receipt=ok(self.build(self.req()));ok(change(self.archive,'exp0','WITHDRAW',{}))
        self.assertNotEqual(self.read(receipt)['status'],'SUCCESS')

    def test_dispute_blocks_snapshot(self):
        receipt=ok(self.build(self.req()));ok(change(self.archive,'exp0','DISPUTE',{'conflict_id':'c','support_ids':['source1'],'evidence':[]}))
        self.assertNotEqual(self.read(receipt)['status'],'SUCCESS')

    def test_same_family_cannot_cross_splits(self):
        refs=[approved(self.archive,f'exp{i}',family='shared') for i in range(2)]
        self.assertEqual(self.build(build_request(refs,self.token))['status'],'CONSTRAINT_CONFLICT')

    def test_same_source_cannot_cross_splits_even_with_different_family(self):
        refs=[approved(self.archive,f'exp{i}',source='Same exact source bytes.') for i in range(2)]
        self.assertEqual(self.build(build_request(refs,self.token))['status'],'CONSTRAINT_CONFLICT')

    def test_shared_family_and_source_allowed_within_one_split(self):
        refs=[approved(self.archive,f'exp{i}',family='shared',source='Same source.') for i in range(2)]
        req=build_request(refs,self.token);req['members'][1]['split']='train'
        receipt=ok(self.build(req));self.assertEqual(len(ok(self.read(receipt))['examples']),2)

    def test_duplicate_projected_examples_rejected_not_silently_removed(self):
        refs=[approved(self.archive,f'exp{i}',text='Same curated example.') for i in range(2)]
        req=build_request(refs,self.token); req['members'][1]['split']='train'
        self.assertEqual(self.build(req)['status'],'CONSTRAINT_CONFLICT')

    def test_newline_projection_and_collision(self):
        a=approved(self.archive,'a',text='One\r\nTwo');b=approved(self.archive,'b',text='One\nTwo')
        req=build_request([a,b],self.token,transform='normalize_newlines_v1')
        self.assertEqual(self.build(req)['status'],'CONSTRAINT_CONFLICT')
        req=build_request([a],self.token,transform='normalize_newlines_v1',sid='newlines')
        receipt=ok(self.build(req));self.assertEqual(ok(self.read(receipt))['examples'][0]['text'],'One\nTwo')

    def test_exact_retry_after_revocation_is_historical_receipt_only(self):
        req=self.req();first=self.build(req);ok(revoke(self.archive,'exp0'))
        retry=self.build(req);self.assertTrue(retry['replayed']);self.assertTrue(retry['historical'])
        self.assertEqual(ok(first),ok(retry));self.assertNotIn('examples',retry['data'])
        self.assertEqual(self.read(first['data'])['status'],'TRAINING_RESTRICTED')
        self.assertEqual(ok(self.store.audit())['snapshots'],1)

    def test_same_operation_different_request_rejected(self):
        req=self.req();ok(self.build(req));req['reason']='Different request'
        self.assertEqual(self.build(req)['status'],'CONSTRAINT_CONFLICT')

    def test_same_snapshot_id_different_operation_rejected(self):
        req=self.req();ok(self.build(req));req['operation_id']='build:other'
        self.assertEqual(self.build(req)['status'],'CONSTRAINT_CONFLICT')

    def test_member_order_normalized_for_idempotency(self):
        req=self.req(2);first=ok(self.build(req));req['members'].reverse()
        retry=self.build(req);self.assertTrue(retry['replayed']);self.assertEqual(ok(retry),first)

    def test_consume_requires_exact_manifest_hash(self):
        receipt=ok(self.build(self.req()));receipt['sha256']='0'*64
        self.assertEqual(self.read(receipt)['status'],'CONSTRAINT_CONFLICT')

    def test_tokenizer_tamper_blocks_build_and_read(self):
        req=self.req();receipt=ok(self.build(req));self.token_path.write_text('changed')
        self.assertEqual(self.read(receipt)['status'],'VALIDATION_FAILED')
        req['snapshot_id']='snapshot2';req['operation_id']='build:2'
        self.assertEqual(self.build(req)['status'],'VALIDATION_FAILED')

    def test_different_archive_cannot_be_substituted(self):
        receipt=ok(self.build(self.req()));other=ExperienceArchive.create(self.root/'other-archive')
        approved(other,'exp0')
        self.assertEqual(self.read(receipt,archive=other)['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_missing_archive_not_recreated(self):
        receipt=ok(self.build(self.req()));self.archive.path.unlink()
        self.assertEqual(self.read(receipt)['status'],'RECOVERY_REQUIRED')
        self.assertFalse(self.archive.path.exists())

    def test_missing_tokenizer_is_typed(self):
        receipt=ok(self.build(self.req()));self.token_path.unlink()
        self.assertEqual(self.read(receipt)['status'],'INSUFFICIENT_EVIDENCE')

    def test_corrupt_manifest_blocks_read_and_audit(self):
        receipt=ok(self.build(self.req()))
        with closing(sqlite3.connect(self.store.path)) as db, db: db.execute("UPDATE snapshots SET body='{}'")
        self.assertEqual(self.read(receipt)['status'],'VALIDATION_FAILED')
        self.assertEqual(self.store.audit()['status'],'VALIDATION_FAILED')

    def test_missing_operation_receipt_blocks_read(self):
        receipt=ok(self.build(self.req()))
        with closing(sqlite3.connect(self.store.path)) as db, db: db.execute('DELETE FROM operations')
        self.assertEqual(self.read(receipt)['status'],'VALIDATION_FAILED')

    def test_missing_source_bytes_fail_closed(self):
        receipt=ok(self.build(self.req()))
        with closing(sqlite3.connect(self.archive.path)) as db, db: db.execute('DELETE FROM evidence')
        self.assertNotEqual(self.read(receipt)['status'],'SUCCESS')

    def test_admin_inspect_not_a_permission_grant(self):
        receipt=ok(self.build(self.req()));ok(revoke(self.archive,'exp0'))
        self.assertFalse(ok(self.store.inspect('snapshot1'))['use_authorized'])
        ok(self.store.audit());self.assertEqual(self.read(receipt)['status'],'TRAINING_RESTRICTED')

    def test_requested_split_not_present_returns_no_examples(self):
        receipt=ok(self.build(self.req()))
        self.assertEqual(self.read(receipt,split='validation')['status'],'INSUFFICIENT_EVIDENCE')

    def test_invalid_read_purpose_cannot_bypass_training_gate(self):
        receipt=ok(self.build(self.req()))
        for p in ['retrieval','redistribution','evaluation',None,[],{}]:
            with self.subTest(p=p):
                r=self.store.read_for_use('snapshot1',expected_manifest_hash=receipt['sha256'],purpose=p,split='train',archive=self.archive,tokenizer_path=self.token_path)
                self.assertEqual(r['status'],'VALIDATION_FAILED')

    def test_model_cannot_attest_selection(self):
        req=self.req();req['actor']=MODEL.copy()
        self.assertEqual(self.build(req)['status'],'AUTHORIZATION_DENIED')

    def test_malformed_requests_fail_typed_and_leave_no_snapshot(self):
        req=self.req()
        variants=[None,[],{},True]
        for key,value in [('members',[]),('purpose','retrieval'),('transform','exec:evil'),('schema_version',True),('at','2026-02-30T13:00:00Z')]:
            r=copy.deepcopy(req);r[key]=value;variants.append(r)
        r=copy.deepcopy(req);r['unknown']=True;variants.append(r)
        for r in variants:
            with self.subTest(request=r):self.assertEqual(self.build(r)['status'],'VALIDATION_FAILED')
        self.assertEqual(ok(self.store.audit())['snapshots'],0)

    def test_duplicate_members_and_boolean_revision_rejected(self):
        req=self.req();req['members'].append(copy.deepcopy(req['members'][0]))
        self.assertEqual(self.build(req)['status'],'VALIDATION_FAILED')
        req['members'].pop();req['members'][0]['revision']=True
        self.assertEqual(self.build(req)['status'],'VALIDATION_FAILED')

    def test_wrong_revision_and_wrong_hash_rejected(self):
        req=self.req();req['members'][0]['revision']+=1
        self.assertEqual(self.build(req)['status'],'CONSTRAINT_CONFLICT')
        req['members'][0]['revision']-=1;req['members'][0]['sha256']='f'*64
        self.assertEqual(self.build(req)['status'],'CONSTRAINT_CONFLICT')

    def test_at_least_one_train_member_required(self):
        req=self.req();req['members'][0]['split']='validation'
        self.assertEqual(self.build(req)['status'],'VALIDATION_FAILED')

    def test_request_cannot_predate_selected_review(self):
        req=self.req();req['at']='2020-01-01T00:00:00Z'
        self.assertEqual(self.build(req)['status'],'VALIDATION_FAILED')

    def test_too_many_members_rejected_before_archive_lookup(self):
        req=self.req();req['members']*=33
        self.assertEqual(self.build(req)['status'],'VALIDATION_FAILED')

    def test_nonempty_directory_and_unknown_store_rejected(self):
        with self.assertRaises(ContractError): DatasetSnapshots.create(self.root/'snapshots',archive=self.archive)
        with self.assertRaises(ContractError): DatasetSnapshots(self.root/'missing')
        self.assertFalse((self.root/'missing').exists())

    def test_list_and_operation_receipt(self):
        req=self.req();receipt=ok(self.build(req))
        self.assertEqual(ok(self.store.list_snapshots()),[receipt])
        self.assertEqual(ok(self.store.operation_receipt(req['operation_id'])),receipt)
        self.assertIsNone(ok(self.store.operation_receipt('missing')))

    def test_schema_manifest_roundtrip(self):
        receipt=ok(self.build(self.req()));m=ok(self.store.inspect('snapshot1'))['manifest']
        self.assertEqual(validate_manifest(json.loads(json.dumps(m))),m)
        m['members'][0]['text']='tampered'
        with self.assertRaises(ContractError):validate_manifest(m)


if __name__=='__main__':unittest.main()
