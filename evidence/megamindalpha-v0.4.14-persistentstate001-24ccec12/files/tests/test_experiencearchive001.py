"""Defined before implementation: local archive contracts, not neural correctness."""
import copy
from contextlib import contextmanager
from hashlib import sha256
import json
from pathlib import Path
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from nss_base.runtime import ContractError, digest
from nss_base.serialization import decode
from nss_base.experience_store import ExperienceArchive

@contextmanager
def sql(path):
    db=sqlite3.connect(path)
    try:
        with db: yield db
    finally: db.close()

ROOT=Path(__file__).resolve().parents[1]
HUMAN={'id':'operator-1','kind':'HUMAN','version':'local-review-v1'}
MODEL={'id':'candidate-model','kind':'MODEL','version':'synthetic-v1'}
AT='2026-09-10T12:00:00Z'

def evidence(id='e1',content='Synthetic fixture: speed is 10 m/s.',kind='REFERENCE'):
    return {'id':id,'kind':kind,'author':HUMAN.copy(),'recorded_at':AT,
        'media_type':'text/plain','sha256':sha256(content.encode()).hexdigest(),
        'content':content,'generator':None,'parent_source_ids':[],
        'rights_note':'Self-authored synthetic software-test material. Not personal data.'}

def capture(id='exp1',operation_id=None):
    return {'schema_version':1,'operation_id':operation_id or 'capture:'+id,
        'experience_id':id,'actor':MODEL.copy(),'at':AT,
        'observation':{'kind':'EXTERNAL_RECORD','execution':None,
            'summary':'A synthetic model interpretation needs human review.',
            'outcome':'UNKNOWN','check_refs':[]},
        'family_id':'speed-fixture-family','sensitivity':'ORDINARY',
        'evidence':[evidence()],
        'statement':{'text':'The speed might be 10 km/h. This is an inference.',
            'uncertainty':'HIGH','support_ids':['e1']}}

class ArchiveTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name)/'archive'
        self.store=ExperienceArchive.create(self.root)
        self.seq=0

    def ok(self,result):
        self.assertEqual(result['status'],'SUCCESS',result)
        return result['data']

    def current(self,id='exp1'):
        return self.ok(self.store.inspect(id))

    def new(self,id='exp1'):
        return self.ok(self.store.capture(capture(id)))

    def cmd(self,action,payload=None,id='exp1',actor=None,expected=None,op=None):
        self.seq+=1
        return {'schema_version':1,'operation_id':op or f'edit:{self.seq}',
            'experience_id':id,'expected_revision_hash':expected or self.current(id)['reference']['sha256'],
            'actor':copy.deepcopy(actor or HUMAN),'at':AT,'reason':'Explicit fixture review decision.',
            'action':action,'payload':payload or {}}

    def change(self,action,payload=None,**kw):
        return self.store.change(self.cmd(action,payload,**kw))

    def approve(self,id='exp1'):
        return self.ok(self.change('REVIEW',{'decision':'APPROVED'},id=id))

    def permit(self,purpose='retrieval',decision='ALLOWED',id='exp1',actor=None):
        return self.change('PERMISSION',{'purpose':purpose,'decision':decision,
            'permission_ref':'fixture:owner-review-1'},id=id,actor=actor)

    def use(self,purpose='retrieval',id='exp1',expected=None):
        return self.store.read_for_use(id,purpose=purpose,
            expected_revision_hash=expected or self.current(id)['reference']['sha256'])

    def revoke(self,sha=None,purpose='retrieval',actor=None,op='revoke:1'):
        command={'schema_version':1,'operation_id':op,'actor':actor or HUMAN,
            'at':AT,'reason':'Source permission withdrawn by local reviewer.',
            'permission_ref':'fixture:revocation-1','source_sha256':sha or evidence()['sha256'],
            'purpose':purpose}
        return self.store.revoke_source(command)

    def test_submission_pending_and_unknown_purposes(self):
        data=self.new();state=data['record']
        self.assertEqual(state['review']['status'],'PENDING_REVIEW')
        self.assertTrue(all(v['status']=='UNKNOWN' for v in state['permissions'].values()))
        self.assertEqual(self.use()['status'],'CONFLICT_REQUIRES_REVIEW')
        self.assertEqual(state['statement']['author'],MODEL)
        self.assertEqual(state['statement']['kind'],'INTERPRETATION')

    def test_source_bytes_and_caller_data_remain_unchanged(self):
        req=capture();before=copy.deepcopy(req);self.ok(self.store.capture(req))
        req['statement']['text']='caller mutation'
        self.assertEqual(self.current()['record']['statement']['text'],before['statement']['text'])
        self.assertEqual(self.ok(self.store.inspect_source(evidence()['sha256']))['content'],evidence()['content'])

    def test_reopen_preserves_review_and_history(self):
        self.new();self.approve();self.ok(self.permit())
        before=self.current();self.store=ExperienceArchive(self.root)
        self.assertEqual(self.current(),before)
        self.assertEqual(len(self.ok(self.store.history('exp1'))),3)
        self.ok(self.use())

    def test_human_correction_keeps_raw_and_previous_interpretation(self):
        first=self.new();self.approve();self.ok(self.permit());self.ok(self.permit('training'))
        old=self.current()
        fixed=self.ok(self.change('CORRECT',{'statement':{
            'text':'The source says 10 m/s, not 10 km/h.','uncertainty':'LOW','support_ids':['e1']},'evidence':[]}))
        r=fixed['record'];self.assertEqual(r['statement']['kind'],'CORRECTION')
        self.assertEqual(r['statement']['supersedes'],digest(old['record']['statement']))
        self.assertEqual(r['review']['status'],'PENDING_REVIEW')
        self.assertEqual(r['permissions']['training']['status'],'UNKNOWN')
        historic=self.ok(self.store.inspect('exp1',revision_hash=first['reference']['sha256']))
        self.assertEqual(historic['record']['statement']['text'],first['record']['statement']['text'])
        self.assertEqual(self.ok(self.store.inspect_source(evidence()['sha256']))['content'],evidence()['content'])

    def test_later_correction_can_attach_new_evidence(self):
        self.new();src=evidence('correction-source','Checked correction: 10 m/s.')
        self.ok(self.change('CORRECT',{'statement':{'text':'Corrected based on a new check.','uncertainty':'LOW','support_ids':[src['id']]},'evidence':[src]}))
        self.assertEqual(len(self.current()['record']['sources']),2)
        self.assertEqual(self.ok(self.store.inspect_source(src['sha256']))['content'],src['content'])

    def test_approval_does_not_approve_training_or_retrieval(self):
        self.new();self.approve()
        self.assertEqual(self.use()['status'],'TRAINING_RESTRICTED')
        self.ok(self.permit('retrieval'));self.ok(self.use())
        for purpose in ('memory','training','redistribution'):
            self.assertEqual(self.use(purpose)['status'],'TRAINING_RESTRICTED')

    def test_permission_does_not_approve_unreviewed_claim(self):
        self.new();self.ok(self.permit('training'))
        self.assertEqual(self.use('training')['status'],'CONFLICT_REQUIRES_REVIEW')

    def test_denied_and_revoked_purposes_stay_restricted_after_correction(self):
        self.new();self.ok(self.permit('training','REVOKED'));self.ok(self.permit('redistribution','DENIED'))
        self.ok(self.change('CORRECT',{'statement':{'text':'New correction.','uncertainty':'LOW','support_ids':['e1']},'evidence':[]}))
        self.approve();self.assertEqual(self.use('training')['status'],'TRAINING_RESTRICTED')
        self.assertEqual(self.current()['record']['permissions']['redistribution']['status'],'DENIED')
        self.assertEqual(self.permit('training')['status'],'TRAINING_RESTRICTED')

    def test_model_cannot_make_consequential_review_changes(self):
        self.new()
        actions=[('REVIEW',{'decision':'APPROVED'}),('CORRECT',{'statement':{'text':'new','uncertainty':'LOW','support_ids':['e1']},'evidence':[]}),('PERMISSION',{'purpose':'training','decision':'ALLOWED','permission_ref':'fake'}),('WITHDRAW',{})]
        for action,payload in actions:
            with self.subTest(action=action):
                self.assertEqual(self.change(action,payload,actor=MODEL)['status'],'AUTHORIZATION_DENIED')
        self.assertEqual(self.revoke(actor=MODEL)['status'],'AUTHORIZATION_DENIED')

    def test_model_may_append_labelled_interpretation_but_not_approve(self):
        self.new();self.approve();self.ok(self.permit())
        self.ok(self.change('ANNOTATE',{'statement':{'text':'Proposed new interpretation.','uncertainty':'LOW','support_ids':['e1']},'evidence':[]},actor=MODEL))
        self.assertEqual(self.current()['record']['review']['status'],'PENDING_REVIEW')
        self.assertEqual(self.use()['status'],'CONFLICT_REQUIRES_REVIEW')

    def test_dispute_resolve_and_separate_review(self):
        self.new();self.approve();self.ok(self.permit())
        self.ok(self.change('DISPUTE',{'conflict_id':'c1','support_ids':['e1'],'evidence':[]}))
        self.assertEqual(self.current()['record']['review']['status'],'QUARANTINED')
        self.assertEqual(self.change('REVIEW',{'decision':'APPROVED'})['status'],'CONFLICT_REQUIRES_REVIEW')
        self.assertEqual(self.change('RESOLVE',{'conflict_id':'c1','support_ids':['e1'],'evidence':[]},actor=MODEL)['status'],'AUTHORIZATION_DENIED')
        self.ok(self.change('RESOLVE',{'conflict_id':'c1','support_ids':['e1'],'evidence':[]}))
        self.assertEqual(self.current()['record']['review']['status'],'PENDING_REVIEW')
        self.approve();self.ok(self.use())
        self.assertEqual(len(self.current()['record']['conflicts']),1)

    def test_annotation_cannot_erase_open_dispute(self):
        self.new();self.ok(self.change('DISPUTE',{'conflict_id':'c1','support_ids':['e1'],'evidence':[]}))
        self.ok(self.change('ANNOTATE',{'statement':{'text':'New wording','uncertainty':'LOW','support_ids':['e1']},'evidence':[]}))
        self.assertEqual(self.current()['record']['review']['status'],'QUARANTINED')

    def test_duplicate_or_unknown_conflicts_rejected(self):
        self.new();self.ok(self.change('DISPUTE',{'conflict_id':'c1','support_ids':['e1'],'evidence':[]}))
        self.assertEqual(self.change('DISPUTE',{'conflict_id':'c1','support_ids':['e1'],'evidence':[]})['status'],'CONSTRAINT_CONFLICT')
        self.assertEqual(self.change('RESOLVE',{'conflict_id':'missing','support_ids':['e1'],'evidence':[]})['status'],'VALIDATION_FAILED')

    def test_rejected_record_not_usable(self):
        self.new();self.ok(self.permit());self.ok(self.change('REVIEW',{'decision':'REJECTED'}))
        self.assertEqual(self.use()['status'],'CONFLICT_REQUIRES_REVIEW')

    def test_withdraw_blocks_use_and_new_edits_but_not_history_inspection(self):
        first=self.new();self.approve();self.ok(self.permit())
        self.ok(self.change('WITHDRAW'))
        self.assertEqual(self.use()['status'],'RETENTION_RESTRICTED')
        self.assertEqual(self.change('REVIEW',{'decision':'APPROVED'})['status'],'RETENTION_RESTRICTED')
        self.ok(self.store.inspect('exp1',revision_hash=first['reference']['sha256']))

    def test_source_revocation_blocks_all_linked_records_and_future_capture(self):
        for id in ('exp1','exp2'):
            self.new(id);self.approve(id);self.ok(self.permit(id=id))
        self.ok(self.revoke());self.store=ExperienceArchive(self.root)
        for id in ('exp1','exp2'):
            self.assertEqual(self.use(id=id)['status'],'TRAINING_RESTRICTED')
        self.new('exp3');self.approve('exp3')
        self.assertEqual(self.permit(id='exp3')['status'],'TRAINING_RESTRICTED')
        self.ok(self.permit('memory',id='exp1'));self.ok(self.use('memory'))

    def test_revocation_of_any_source_blocks_a_curated_view(self):
        self.new();e=evidence('new','additional evidence')
        self.ok(self.change('CORRECT',{'statement':{'text':'new claim','uncertainty':'LOW','support_ids':['e1']},'evidence':[e]}))
        self.approve();self.ok(self.permit());self.ok(self.revoke(sha=e['sha256']))
        self.assertEqual(self.use()['status'],'TRAINING_RESTRICTED')

    def test_historical_permission_cannot_be_used_as_current(self):
        self.new();self.approve();old=self.ok(self.permit())
        self.ok(self.permit(decision='REVOKED'))
        self.assertEqual(self.use(expected=old['reference']['sha256'])['status'],'CONSTRAINT_CONFLICT')
        self.assertEqual(self.use()['status'],'TRAINING_RESTRICTED')

    def test_exact_capture_retry_is_idempotent_after_review(self):
        first=self.new();self.approve()
        retry=self.store.capture(capture());self.ok(retry)
        self.assertTrue(retry['replayed']);self.assertTrue(retry['historical'])
        self.assertEqual(retry['data']['reference'],first['reference'])
        self.assertEqual(self.current()['record']['review']['status'],'APPROVED')

    def test_mutation_retry_does_not_regrant_old_permission(self):
        self.new();self.approve();cmd=self.cmd('PERMISSION',{'purpose':'training','decision':'ALLOWED','permission_ref':'p1'})
        self.ok(self.store.change(cmd));self.ok(self.permit('training','REVOKED'))
        retry=self.store.change(cmd);self.ok(retry);self.assertTrue(retry['historical'])
        self.assertEqual(self.use('training')['status'],'TRAINING_RESTRICTED')

    def test_changed_operation_id_reuse_and_stale_parent_rejected(self):
        self.new();cmd=self.cmd('REVIEW',{'decision':'APPROVED'})
        self.ok(self.store.change(cmd))
        modified=copy.deepcopy(cmd);modified['reason']='changed'
        self.assertEqual(self.store.change(modified)['status'],'CONSTRAINT_CONFLICT')
        modified['operation_id']='fresh-id'
        self.assertEqual(self.store.change(modified)['status'],'CONSTRAINT_CONFLICT')
        bad=capture();bad['observation']['summary']='different'
        self.assertEqual(self.store.capture(bad)['status'],'CONSTRAINT_CONFLICT')

    def test_global_operation_namespace_prevents_cross_kind_reuse(self):
        self.new();self.assertEqual(self.revoke(op='capture:exp1')['status'],'CONSTRAINT_CONFLICT')

    def test_duplicate_record_id_does_not_overwrite(self):
        original=self.new();req=capture(operation_id='different-op')
        self.assertEqual(self.store.capture(req)['status'],'CONSTRAINT_CONFLICT')
        self.assertEqual(self.current(),original)

    def test_source_revocation_replay_is_exact(self):
        self.new();first=self.revoke();self.ok(first);again=self.revoke();self.ok(again)
        self.assertTrue(again['replayed'])
        self.assertEqual(self.revoke(purpose='training')['status'],'CONSTRAINT_CONFLICT')

    def test_unknown_source_revocation_rejected(self):
        self.assertEqual(self.revoke(sha='a'*64)['status'],'INSUFFICIENT_EVIDENCE')

    def test_no_partly_added_evidence_after_invalid_correction(self):
        self.new();src=evidence('e2','must not persist on failed request')
        result=self.change('CORRECT',{'statement':{'text':'bad reference','uncertainty':'LOW','support_ids':['unknown']},'evidence':[src]})
        self.assertEqual(result['status'],'VALIDATION_FAILED')
        self.assertEqual(self.store.inspect_source(src['sha256'])['status'],'INSUFFICIENT_EVIDENCE')
        self.assertEqual(self.current()['record']['revision'],0)

    def test_cannot_substitute_evidence_using_existing_source_id(self):
        self.new();src=evidence(content='changed bytes')
        result=self.change('CORRECT',{'statement':{'text':'changed','uncertainty':'LOW','support_ids':['e1']},'evidence':[src]})
        self.assertEqual(result['status'],'CONSTRAINT_CONFLICT')

    def test_stale_or_wrong_record_inspection_hash_rejected(self):
        first=self.new();self.new('exp2')
        self.assertEqual(self.store.inspect('exp2',revision_hash=first['reference']['sha256'])['status'],'INSUFFICIENT_EVIDENCE')

    def test_list_is_bounded_and_cursor_validated(self):
        self.new('a');self.new('b');self.new('c')
        self.assertEqual([v['experience_id'] for v in self.ok(self.store.list_records(limit=2))],['a','b'])
        self.assertEqual([v['experience_id'] for v in self.ok(self.store.list_records(limit=2,after='b'))],['c'])
        for n in (0,-1,1001,True):
            self.assertEqual(self.store.list_records(limit=n)['status'],'VALIDATION_FAILED')

    def test_input_validation_rejects_malformed_shapes(self):
        mutations=[lambda r:r.update(extra=True),lambda r:r.update(schema_version=True),lambda r:r.update(evidence=[]),lambda r:r['statement'].update(confidence=100),lambda r:r['statement'].update(support_ids=['missing']),lambda r:r['evidence'].append(copy.deepcopy(r['evidence'][0])),lambda r:r['evidence'][0].update(sha256='a'*64),lambda r:r.update(at='2026-02-30T00:00:00Z'),lambda r:r['observation'].update(execution={}),lambda r:r['actor'].update(kind='ADMIN')]
        for mutate in mutations:
            with self.subTest(mutation=str(mutate)):
                r=capture();mutate(r);self.assertEqual(self.store.capture(r)['status'],'VALIDATION_FAILED')
        self.assertEqual(self.ok(self.store.list_records()),[])

    def test_invalid_unicode_nonfinite_and_deep_values_fail_typed(self):
        for mutate in (lambda r:r['statement'].update(text='\ud800'),lambda r:r['statement'].update(text=float('nan')),lambda r:r['statement'].update(text='x'*8193)):
            r=capture();mutate(r);self.assertEqual(self.store.capture(r)['status'],'VALIDATION_FAILED')
        r=capture();r['loop']=r
        self.assertEqual(self.store.capture(r)['status'],'VALIDATION_FAILED')

    def test_json_duplicate_fields_rejected(self):
        with self.assertRaises(ContractError):decode('{"operation_id":"one","operation_id":"two"}')

    def test_synthetic_requires_generator_and_named_parents(self):
        req=capture();req['evidence'].append(evidence('e2','synthetic paraphrase','SYNTHETIC'))
        self.assertEqual(self.store.capture(req)['status'],'VALIDATION_FAILED')
        req['evidence'][1].update(generator=MODEL.copy(),parent_source_ids=['e1'])
        self.ok(self.store.capture(req));self.assertEqual(self.current()['record']['sources'][1]['generator'],MODEL)

    def test_synthetic_lineage_cycles_and_dangling_parents_rejected(self):
        for parents in (['e1'],['absent']):
            req=capture();req['evidence'][0].update(kind='SYNTHETIC',generator=MODEL.copy(),parent_source_ids=parents)
            self.assertEqual(self.store.capture(req)['status'],'VALIDATION_FAILED')

    def test_timestamp_regression_rejected(self):
        self.new();cmd=self.cmd('REVIEW',{'decision':'APPROVED'});cmd['at']='2026-09-09T12:00:00Z'
        self.assertEqual(self.store.change(cmd)['status'],'VALIDATION_FAILED')

    def test_unknown_mutation_fields_actions_and_empty_reasons_fail(self):
        self.new()
        for mutate in (lambda c:c.update(action='DEPLOY'),lambda c:c.update(reason=''),lambda c:c['payload'].update(allowed=True),lambda c:c.update(expected_revision_hash='x')):
            c=self.cmd('REVIEW',{'decision':'APPROVED'});mutate(c)
            self.assertEqual(self.store.change(c)['status'],'VALIDATION_FAILED')

    def test_identity_sensitive_review_requires_human_without_inferred_authentication(self):
        req=capture();req['sensitivity']='IDENTITY_SENSITIVE';self.ok(self.store.capture(req))
        self.assertEqual(self.change('REVIEW',{'decision':'APPROVED'},actor=MODEL)['status'],'AUTHORIZATION_DENIED')
        self.approve();self.assertEqual(self.use('training')['status'],'TRAINING_RESTRICTED')

    def test_missing_database_is_not_recreated(self):
        self.new();self.store.path.unlink()
        self.assertEqual(self.store.inspect('exp1')['status'],'RECOVERY_REQUIRED')
        with self.assertRaises(ContractError):ExperienceArchive(self.root)
        self.assertFalse(self.store.path.exists())

    def test_unknown_existing_store_never_silently_initialized(self):
        another=Path(self.tmp.name)/'other';another.mkdir();(another/'note').write_text('do not replace')
        with self.assertRaises(ContractError):ExperienceArchive.create(another)
        self.assertFalse((another/'archive.sqlite3').exists())

    def test_unsupported_schema_fails_closed(self):
        with sql(self.store.path) as db:db.execute("UPDATE metadata SET value='99' WHERE key='schema_version'")
        self.assertEqual(self.store.audit()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_corrupt_evidence_is_detected(self):
        self.new()
        with sql(self.store.path) as db:db.execute('UPDATE evidence SET content=?',(b'changed',))
        self.assertEqual(self.store.inspect('exp1')['status'],'VALIDATION_FAILED')
        self.assertEqual(self.store.inspect_source(evidence()['sha256'])['status'],'VALIDATION_FAILED')

    def test_corrupt_revision_and_event_are_detected(self):
        self.new()
        with sql(self.store.path) as db:db.execute("UPDATE revisions SET body='{}'")
        self.assertEqual(self.store.inspect('exp1')['status'],'VALIDATION_FAILED')

    def test_well_formed_but_unearned_approval_is_rejected_by_replay_validation(self):
        self.new()
        with sql(self.store.path) as db:
            row=db.execute('SELECT body FROM revisions').fetchone();r=json.loads(row[0]);r['review'].update(status='APPROVED',reviewer=HUMAN,at=AT,reason='forged')
            h=digest(r);db.execute('UPDATE revisions SET body=?,sha256=?',(json.dumps(r),h));db.execute('UPDATE records SET head_sha256=?',(h,));db.execute('UPDATE operations SET result_sha256=?',(h,))
        self.assertEqual(self.store.inspect('exp1')['status'],'VALIDATION_FAILED')

    def test_substituted_current_pointer_and_missing_event_fail_closed(self):
        self.new();self.new('exp2');h=self.current('exp2')['reference']['sha256']
        with sql(self.store.path) as db:db.execute("UPDATE records SET head_sha256=? WHERE id='exp1'",(h,))
        self.assertEqual(self.store.inspect('exp1')['status'],'VALIDATION_FAILED')

    def test_deleted_operation_is_detected(self):
        self.new()
        with sql(self.store.path) as db:db.execute('DELETE FROM operations')
        self.assertEqual(self.store.inspect('exp1')['status'],'VALIDATION_FAILED')

    def test_audit_counts_and_source_deduplication(self):
        self.new();self.new('exp2');self.approve()
        report=self.ok(self.store.audit())
        self.assertEqual(report['records'],2);self.assertEqual(report['revisions'],3)
        self.assertEqual(report['evidence_blobs'],1)

    def test_storage_error_during_append_rolls_back(self):
        self.new();old=self.current()
        with patch('nss_base.experience_store._fault',side_effect=sqlite3.OperationalError('injected')):
            result=self.change('REVIEW',{'decision':'APPROVED'})
        self.assertEqual(result['status'],'INTERNAL_FAILURE')
        self.assertEqual(self.current(),old);self.ok(self.store.audit())

    def test_fault_points_are_not_accepted_in_untrusted_json(self):
        r=capture();r['crash_at']='after_commit'
        self.assertEqual(self.store.capture(r)['status'],'VALIDATION_FAILED')
