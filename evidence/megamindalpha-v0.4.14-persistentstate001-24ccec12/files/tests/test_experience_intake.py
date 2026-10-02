"""Integration through public APIs: archive never mutates runtime or executes effects."""
from copy import deepcopy
from hashlib import sha256
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from nss_base.artifacts import Bundle
from nss_base.ledger import Ledger
from nss_base.publication import RecoveryStore, checkpoint_hash
from nss_base.recovery import checkpoint
from nss_base.runtime import digest
from nss_base.serialization import read_json
from nss_base.task_records import attach_task_record
from nss_base.stage_handoff import handoff_stage
from nss_base.experience_store import ExperienceArchive
from nss_base.experience_intake import capture_stage

ROOT=Path(__file__).resolve().parents[1]

class IntakeTests(unittest.TestCase):
    def setUp(self):
        self.tmp=TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);self.fixtures=self.root/'fixtures'
        shutil.copytree(ROOT/'fixtures/stagehandoff001',self.fixtures)
        self.bundle=Bundle(self.fixtures/'manifest.json')
        self.ledger=Ledger(self.root/'actions');self.runtime=RecoveryStore(self.root/'runtime')
        self.archive=ExperienceArchive.create(self.root/'archive')
        self.record=read_json(self.fixtures/'task_record.json')
        self.action={'schema_version':1,'task_id':'stage-001','key':'committed:one',
            'payload':{'operation':'append_marker','value':'one effect'},'status':'PENDING','receipt':None}
        receipt=self.ledger.perform(self.action)
        self.record['receipts']=[{'key':self.action['key'],'kind':'mock_action','receipt':receipt}]
        self.inputs=read_json(self.fixtures/'input_ref.json')
        self.state=attach_task_record(checkpoint(self.bundle,'AB','stage-001',self.inputs),self.record)
        self.hash=self.runtime.publish_initial(self.state)
        self.req={'schema_version':1,'operation_id':'capture:stage','experience_id':'exp-stage',
            'actor':{'id':'local-capture','kind':'SYSTEM','version':'001'},'at':'2026-09-10T12:00:00Z',
            'task_id':'stage-001','expected_checkpoint_hash':self.hash,
            'summary':'A sealed stage produced a provisional interpretation.', 'outcome':'UNKNOWN','check_refs':[],
            'statement':{'text':'Proposed interpretation, not a fact.','uncertainty':'HIGH','support_ids':['source-1']},
            'family_id':'stage-fixture-family','sensitivity':'ORDINARY'}

    def call(self,request=None):
        return capture_stage(self.archive,self.bundle,self.runtime,self.ledger,request=self.req if request is None else request)

    def test_capture_exact_portable_task_provenance_and_receipt_without_effect(self):
        result=self.call();self.assertEqual(result['status'],'SUCCESS',result)
        capture=result['data']['capture'];execution=capture['observation']['execution']
        self.assertEqual(execution['ecid'],self.state['ecid']);self.assertEqual(execution['checkpoint_sha256'],self.hash)
        self.assertEqual(execution['task_record_sha256'],digest(self.record))
        snapshot=next(s for s in capture['evidence'] if s['kind']=='TASK_SNAPSHOT')
        data=self.archive.inspect_source(snapshot['sha256'])['data']['content']
        self.assertEqual(sha256(data.encode()).hexdigest(),digest(self.record))
        self.assertIn(self.action['key'],data)
        self.assertNotIn('"cache"',data);self.assertNotIn('"draft"',data)
        self.assertEqual(self.runtime.current_hash('stage-001'),self.hash);self.assertEqual(self.ledger.effect_count(),1)

    def test_capture_source_is_locally_persistent_even_after_original_is_removed(self):
        result=self.call();self.assertEqual(result['status'],'SUCCESS',result)
        (self.fixtures/'problem.json').unlink()
        self.assertEqual(self.archive.inspect('exp-stage')['status'],'SUCCESS')
        self.assertEqual(self.call()['status'],'SUCCESS') # Exact committed retry reads history.

    def test_retry_after_runtime_moves_returns_prior_capture_without_reactivation(self):
        first=self.call();self.assertEqual(first['status'],'SUCCESS',first)
        request={'schema_version':1,'source_checkpoint_hash':self.hash,'next_stage':{
            'id':'later-stage','mode':'WORK','sealed':False,'objective':'Continue','required_facts':[], 'requested_output':'result'}}
        moved=handoff_stage(self.bundle,self.runtime,self.ledger,task_id='stage-001',destination='A',
            attempt_id='after-capture',request=request,authorized=True)
        self.assertEqual(moved['status'],'SUCCESS',moved)
        retry=self.call();self.assertEqual(retry['status'],'SUCCESS',retry);self.assertTrue(retry['replayed'])
        self.assertEqual(self.runtime.current('stage-001')['profile'],'A')
        self.assertEqual(len(self.archive.list_records()['data']),1)

    def test_substituted_capture_retry_rejected(self):
        self.call();bad=deepcopy(self.req);bad['summary']='different experience'
        self.assertEqual(self.call(bad)['status'],'CONSTRAINT_CONFLICT')

    def test_stale_checkpoint_is_not_captured(self):
        bad=deepcopy(self.req);bad['expected_checkpoint_hash']='a'*64
        self.assertEqual(self.call(bad)['status'],'CONSTRAINT_CONFLICT')
        self.assertEqual(self.archive.list_records()['data'],[])

    def test_unsealed_stage_requires_explicit_finish(self):
        r=deepcopy(self.record);r['stage']['sealed']=False
        self.runtime=RecoveryStore(self.root/'other-runtime')
        s=attach_task_record(checkpoint(self.bundle,'AB','stage-001',self.inputs),r)
        self.req['expected_checkpoint_hash']=self.runtime.publish_initial(s)
        self.assertEqual(self.call()['status'],'CONSTRAINT_CONFLICT')

    def test_modified_source_fails_without_runtime_or_archive_change(self):
        (self.fixtures/'problem.json').write_text('{}')
        self.assertEqual(self.call()['status'],'INCOMPATIBLE_CONFIGURATION')
        self.assertEqual(self.runtime.current_hash('stage-001'),self.hash)
        self.assertEqual(self.archive.list_records()['data'],[])

    def test_missing_source_is_explicitly_insufficient(self):
        (self.fixtures/'problem.json').unlink()
        self.assertEqual(self.call()['status'],'INSUFFICIENT_EVIDENCE')

    def test_receipt_mismatch_blocks_capture(self):
        r=deepcopy(self.record);r['receipts'][0]['receipt']='a'*64
        self.runtime=RecoveryStore(self.root/'other-runtime')
        s=attach_task_record(checkpoint(self.bundle,'AB','stage-001',self.inputs),r)
        self.req['expected_checkpoint_hash']=self.runtime.publish_initial(s)
        self.assertEqual(self.call()['status'],'VALIDATION_FAILED')
        self.assertEqual(self.ledger.effect_count(),1)

    def test_same_stage_different_submission_id_is_not_duplicate_experience(self):
        self.call();req=deepcopy(self.req);req.update(operation_id='new-operation',experience_id='new-record')
        self.assertEqual(self.call(req)['status'],'CONSTRAINT_CONFLICT')

    def test_source_symlink_cannot_escape_fixture_root(self):
        raw=(self.fixtures/'problem.json').read_bytes();outside=self.root/'outside.json';outside.write_bytes(raw)
        (self.fixtures/'problem.json').unlink();(self.fixtures/'problem.json').symlink_to(outside)
        self.assertEqual(self.call()['status'],'VALIDATION_FAILED')

    def test_archive_failure_does_not_break_task_or_repeat_action(self):
        self.archive.path.unlink();result=self.call()
        self.assertEqual(result['status'],'RECOVERY_REQUIRED')
        self.assertEqual(self.runtime.current_hash('stage-001'),self.hash)
        self.assertEqual(self.ledger.effect_count(),1)

    def test_imported_task_capture_cannot_substitute_stage_or_omit_snapshot(self):
        first=self.call();self.assertEqual(first['status'],'SUCCESS',first)
        original=deepcopy(first['data']['capture'])
        for src in original['evidence']:
            src['content']=self.archive.inspect_source(src['sha256'])['data']['content']
        for mode in ('stage','task_hash','missing_snapshot'):
            cmd=deepcopy(original);cmd.update(operation_id='substitute:'+mode,experience_id='other:'+mode)
            if mode=='stage':cmd['observation']['execution']['stage_id']='wrong-stage'
            elif mode=='task_hash':cmd['observation']['execution']['task_record_sha256']='a'*64
            else:cmd['evidence']=[x for x in cmd['evidence'] if x['kind']!='TASK_SNAPSHOT']
            result=self.archive.capture(cmd)
            self.assertEqual(result['status'],'VALIDATION_FAILED',result)

    def test_intake_never_guesses_original_source_author(self):
        result=self.call();self.assertEqual(result['status'],'SUCCESS',result)
        original=next(x for x in result['data']['capture']['evidence'] if x['id']=='source-1')
        self.assertEqual(original['author']['kind'],'UNKNOWN')
        self.assertIn('unverified',original['rights_note'])
