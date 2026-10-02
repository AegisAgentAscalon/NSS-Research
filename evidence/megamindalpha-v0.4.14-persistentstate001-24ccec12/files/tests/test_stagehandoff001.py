"""StageHandoff001: typed working-state preservation, not neural performance tests."""
import copy
from contextlib import closing
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from nss_base.artifacts import Bundle
from nss_base.ledger import Ledger
from nss_base.publication import RecoveryStore, checkpoint_hash, database, durable_recover
from nss_base.recovery import checkpoint, accept_cache, execute
from nss_base.runtime import ContractError, digest
from nss_base.serialization import decode, read_json
from nss_base.task_records import validate_task_record, attach_task_record, validate_checkpoint
from nss_base.stage_handoff import handoff_stage, finish_stage, initialize_task

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / 'fixtures/stagehandoff001'

class StageHandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp = TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.fixture = self.root / 'fixture'; shutil.copytree(FIXTURE, self.fixture)
        self.bundle = Bundle(self.fixture / 'manifest.json')
        self.inputs = read_json(self.fixture / 'input_ref.json')
        self.ledger = Ledger(self.root / 'actions')
        self.store = RecoveryStore(self.root / 'recovery')
        self.record = read_json(self.fixture / 'task_record.json')
        self.source = attach_task_record(checkpoint(self.bundle, 'AB', 'stage-001', self.inputs), self.record)
        self.source_hash = self.store.publish_initial(self.source)
        self.request = {'schema_version':1, 'source_checkpoint_hash':self.source_hash,
            'next_stage':{'id':'solve','mode':'WORK','sealed':False,
                'objective':'Solve from the exact values and units.',
                'required_facts':[{'fact_id':'speed','fields':['value','unit']}],
                'requested_output':'Checked result with source references.'}}

    def call(self, destination='A', request=None, attempt='h1', **kw):
        return handoff_stage(self.bundle,self.store,self.ledger,task_id='stage-001',
            destination=destination,attempt_id=attempt,request=self.request if request is None else request,
            authorized=kw.pop('authorized', True),**kw)

    def assert_code(self, fn, code):
        with self.assertRaises(ContractError) as cm: fn()
        self.assertEqual(cm.exception.code,code)

    def reseed(self, record=None, profile='AB'):
        # A distinct local store, not an unsupported overwrite of published state.
        self.store = RecoveryStore(self.root / ('recovery'+str(len(list(self.root.iterdir())))))
        self.source = attach_task_record(checkpoint(self.bundle,profile,'stage-001',self.inputs),self.record if record is None else record)
        self.source_hash=self.store.publish_initial(self.source)
        self.request['source_checkpoint_hash']=self.source_hash

    def marker(self, key='action-1'):
        return {'schema_version':1,'key':key,'task_id':'stage-001',
            'payload':{'operation':'append_marker','value':'one external effect'},'status':'PENDING','receipt':None}

    def test_schema_roundtrip_does_not_mutate_caller(self):
        before=copy.deepcopy(self.record)
        validate_task_record(decode(json.dumps(self.record)))
        self.assertEqual(self.record,before)
        self.assertEqual(self.source['schema_version'],2)
        self.record['goal']='caller changed'
        self.assertNotEqual(self.record['goal'],self.source['task_record']['goal'])

    def test_reject_unknown_nested_fields_and_duplicates(self):
        r=copy.deepcopy(self.record);r['facts'][0]['confidence']=1
        self.assert_code(lambda:validate_task_record(r),'VALIDATION_FAILED')
        self.assert_code(lambda:decode('{"a":1,"a":2}'),'VALIDATION_FAILED')

    def test_reject_bool_revision_missing_and_wrong_types(self):
        for mutate in (lambda r:r.update(revision=True),lambda r:r.pop('goal'),lambda r:r.update(facts={}),lambda r:r.update(parent_hash='bad')):
            r=copy.deepcopy(self.record);mutate(r)
            self.assert_code(lambda:validate_task_record(r),'VALIDATION_FAILED')

    def test_record_bounds(self):
        for mutate in (lambda r:r.update(goal='a'*4097),lambda r:r.update(assumptions=[{'id':f'x{i}','text':'x','source_ids':[]} for i in range(129)])):
            r=copy.deepcopy(self.record);mutate(r)
            self.assert_code(lambda:validate_task_record(r),'VALIDATION_FAILED')

    def test_duplicate_ids_and_dangling_provenance(self):
        for mutate in (lambda r:r['facts'].append(copy.deepcopy(r['facts'][0])),lambda r:r['facts'][0].update(source_id='missing'),lambda r:r['clarifications'][0].update(question_id='missing')):
            r=copy.deepcopy(self.record);mutate(r)
            self.assert_code(lambda:validate_task_record(r),'VALIDATION_FAILED')

    def test_checkpoint_version_and_task_binding(self):
        for mutate in (lambda c:c.update(schema_version=1),lambda c:c['task_record'].update(task_id='other'),lambda c:c.pop('task_record')):
            c=copy.deepcopy(self.source);mutate(c)
            self.assert_code(lambda:validate_checkpoint(c),'VALIDATION_FAILED')

    def test_exact_unit_rehydration_and_preservation(self):
        r=self.call();self.assertEqual(r['status'],'SUCCESS',r)
        self.assertEqual(r['state']['task_record']['facts'][0]['unit'],'m/s')
        for key in ('goal','original_request','assumptions','unresolved_questions','clarifications','constraints','receipts','sources','checked_results'):
            self.assertEqual(self.source['task_record'][key],r['state']['task_record'][key])
        self.assertEqual(r['state']['task_record']['parent_hash'],digest(self.source['task_record']))
        self.assertEqual(r['state']['task_record']['revision'],1)
        self.assertEqual(self.store.current('stage-001')['profile'],'A')
        self.assertEqual(self.store.inspect_attempt('h1')['schema_version'],2)
        self.assertEqual(self.record['facts'][0]['unit'],None)

    def test_missing_source_reports_insufficient_evidence_and_retains_source(self):
        (self.fixture/'problem.json').unlink()
        r=self.call();self.assertEqual(r['status'],'INSUFFICIENT_EVIDENCE',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)
        self.assertIsNone(self.store.inspect_attempt('h1'))

    def test_source_tampering_is_not_accepted(self):
        (self.fixture/'problem.json').write_text('{}')
        r=self.call();self.assertEqual(r['status'],'INCOMPATIBLE_CONFIGURATION',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def test_contradictory_value_not_silently_corrected(self):
        rec=copy.deepcopy(self.record);rec['facts'][0]['value']='999';self.reseed(rec)
        r=self.call();self.assertEqual(r['status'],'CONSTRAINT_CONFLICT',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def test_source_without_required_unit_asks_instead_of_inventing(self):
        ev=read_json(self.fixture/'problem.json');ev['fields'][0]['unit']=None
        p=self.fixture/'problem.json';p.write_text(json.dumps(ev))
        from hashlib import sha256
        rec=copy.deepcopy(self.record);rec['sources'][0]['artifact']['sha256']=sha256(p.read_bytes()).hexdigest();self.reseed(rec)
        r=self.call();self.assertEqual(r['status'],'NEEDS_CLARIFICATION',r)
        self.assertEqual(self.store.current('stage-001')['task_record']['facts'][0]['unit'],None)

    def test_unknown_required_fact_and_unresolved_blocker(self):
        req=copy.deepcopy(self.request);req['next_stage']['required_facts'][0]['fact_id']='mass'
        self.assertEqual(self.call(request=req)['status'],'NEEDS_CLARIFICATION')
        rec=copy.deepcopy(self.record);rec['unresolved_questions'].append({'id':'unknown','text':'Which value?','blocking':True});self.reseed(rec)
        self.assertEqual(self.call(attempt='h2')['status'],'NEEDS_CLARIFICATION')

    def test_qualified_ab_a_and_unconditional_core_return(self):
        r=self.call();self.assertEqual(r['status'],'SUCCESS')
        sealed=finish_stage(self.bundle,self.store,self.ledger,task_id='stage-001',expected_checkpoint_hash=checkpoint_hash(r['state']),new_results=[],new_receipts=[],authorized=True)
        self.assertEqual(sealed['status'],'SUCCESS',sealed)
        req=copy.deepcopy(self.request);req['source_checkpoint_hash']=checkpoint_hash(sealed['state']);req['next_stage'].update(id='control',mode='CONTROL',required_facts=[])
        r2=self.call(destination='core',request=req,attempt='h2')
        self.assertEqual(r2['status'],'SUCCESS',r2)
        self.assertEqual(r2['state']['cache'],execute(self.bundle,'core',self.bundle.artifact(self.inputs,'inputs.schema.json')))
        self.assertEqual(r2['state']['draft'],'')

    def test_control_and_evaluation_require_core_only(self):
        for mode in ('CONTROL','EVALUATION'):
            req=copy.deepcopy(self.request);req['next_stage']['mode']=mode
            r=self.call(request=req);self.assertEqual(r['status'],'INCOMPATIBLE_CONFIGURATION',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def test_stale_cache_rejected_clean_a_equivalence(self):
        self.assert_code(lambda:accept_cache(self.bundle,self.source,'A'),'INCOMPATIBLE_CONFIGURATION')
        r=self.call();self.assertTrue(r['replayed']);self.assertEqual(r['state']['draft'],'')
        self.assertEqual(r['state']['cache'],execute(self.bundle,'A',self.bundle.artifact(self.inputs,'inputs.schema.json')))

    def test_unqualified_profile_union_reverse_and_missing_core(self):
        for target in ('B','AB_union','unknown'):
            self.assertEqual(self.call(destination=target)['status'],'INCOMPATIBLE_CONFIGURATION')
        self.assertEqual(self.call(destination='A+B')['status'],'VALIDATION_FAILED')
        self.reseed(profile='A')
        self.assertEqual(self.call(destination='AB')['status'],'INCOMPATIBLE_CONFIGURATION')
        m=read_json(self.fixture/'manifest.json');m['profiles']=[p for p in m['profiles'] if p['id']!='core'];(self.fixture/'manifest.json').write_text(json.dumps(m))
        self.assert_code(lambda:Bundle(self.fixture/'manifest.json'),'VALIDATION_FAILED')

    def test_unsealed_source_and_stale_request_fail(self):
        req=copy.deepcopy(self.request);req['source_checkpoint_hash']='0'*64
        self.assertEqual(self.call(request=req)['status'],'INCOMPATIBLE_CONFIGURATION')
        rec=copy.deepcopy(self.record);rec['stage']['sealed']=False;self.reseed(rec)
        self.assertEqual(self.call()['status'],'CONSTRAINT_CONFLICT')

    def test_request_validation_no_hidden_assumptions(self):
        for mutate in (lambda x:x.update(unexpected=True),lambda x:x['next_stage'].update(sealed=True),lambda x:x['next_stage'].update(id='interpret')):
            q=copy.deepcopy(self.request);mutate(q)
            self.assertIn(self.call(request=q)['status'],('VALIDATION_FAILED','CONSTRAINT_CONFLICT'))

    def test_noop_revalidates_authorization_artifacts_and_receipts(self):
        r=self.call(destination='AB',authorized=False);self.assertEqual(r['status'],'AUTHORIZATION_DENIED')
        act=self.marker();self.ledger.perform(act)
        self.assertEqual(self.call(destination='AB')['status'],'RECOVERY_REQUIRED')
        rec=copy.deepcopy(self.record);rec['receipts']=[{'key':act['key'],'kind':'mock_action','receipt':self.ledger.inspect(act['key'])['receipt']}];self.reseed(rec)
        r=self.call(destination='AB');self.assertEqual(r['status'],'SUCCESS',r);self.assertFalse(r['replayed'])
        self.assertEqual(r['state']['ecid'],self.source['ecid']);self.assertEqual(r['state']['draft'],'')

    def test_action_and_presented_output_are_never_reexecuted(self):
        rec=copy.deepcopy(self.record)
        for key,kind in [('action-1','mock_action'),('output-1','presented_output')]:
            act=self.marker(key);self.ledger.perform(act)
            rec['receipts'].append({'key':key,'kind':kind,'receipt':self.ledger.inspect(key)['receipt']})
        self.reseed(rec)
        with patch.object(self.ledger,'perform',side_effect=AssertionError('side effects forbidden')):
            r=self.call()
        self.assertEqual(r['status'],'SUCCESS',r);self.assertEqual(self.ledger.effect_count(),2)
        self.assertEqual(r['state']['task_record']['receipts'],rec['receipts'])

    def test_uncertain_and_forged_receipt_block_handoff(self):
        act=self.marker();self.ledger.perform(act)
        rec=copy.deepcopy(self.record);rec['receipts']=[{'key':act['key'],'kind':'mock_action','receipt':'f'*64}];self.reseed(rec)
        self.assertEqual(self.call()['status'],'VALIDATION_FAILED')
        with closing(sqlite3.connect(self.ledger.path)) as db, db:
            v=self.ledger.inspect(act['key']);v.update(status='UNCERTAIN',receipt=None)
            db.execute('UPDATE records SET body=? WHERE key=?',(json.dumps(v),act['key']))
        self.assertEqual(self.call()['status'],'RECOVERY_REQUIRED')

    def test_load_failure_and_denial_preserve_source(self):
        self.assertEqual(self.call(authorized=False)['status'],'AUTHORIZATION_DENIED')
        r=self.call(load_ok=False);self.assertEqual(r['status'],'INTERNAL_FAILURE',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def test_finished_stage_new_results_are_ecid_bound(self):
        r=self.call();key=checkpoint_hash(r['state'])
        result={'id':'result1','text':'Fixture arithmetic checked.','check_ref':'fixture:integer-equality','producer_ecid':r['state']['ecid'],'source_ids':['source-1']}
        f=finish_stage(self.bundle,self.store,self.ledger,task_id='stage-001',expected_checkpoint_hash=key,new_results=[result],new_receipts=[],authorized=True)
        self.assertEqual(f['status'],'SUCCESS',f);self.assertTrue(f['state']['task_record']['stage']['sealed'])
        self.assertEqual(f['state']['task_record']['checked_results'],[result])
        self.assertEqual(f['state']['task_record']['revision'],2)
        self.assertEqual(finish_stage(self.bundle,self.store,self.ledger,task_id='stage-001',expected_checkpoint_hash=key,new_results=[],new_receipts=[],authorized=True)['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_finish_rejects_wrong_ecid_and_denial(self):
        r=self.call();key=checkpoint_hash(r['state'])
        result={'id':'result1','text':'Unverified','check_ref':'fixture:check','producer_ecid':self.source['ecid'],'source_ids':['source-1']}
        self.assertEqual(finish_stage(self.bundle,self.store,self.ledger,task_id='stage-001',expected_checkpoint_hash=key,new_results=[result],new_receipts=[],authorized=True)['status'],'INCOMPATIBLE_CONFIGURATION')
        self.assertEqual(finish_stage(self.bundle,self.store,self.ledger,task_id='stage-001',expected_checkpoint_hash=key,new_results=[],new_receipts=[],authorized=False)['status'],'AUTHORIZATION_DENIED')
        self.assertEqual(self.store.current_hash('stage-001'),key)

    def test_historical_request_does_not_reactivate_old_profile(self):
        first=self.call();self.assertFalse(first['historical'])
        sealed=finish_stage(self.bundle,self.store,self.ledger,task_id='stage-001',expected_checkpoint_hash=checkpoint_hash(first['state']),new_results=[],new_receipts=[],authorized=True)
        req=copy.deepcopy(self.request);req['source_checkpoint_hash']=checkpoint_hash(sealed['state']);req['next_stage'].update(id='judge',mode='EVALUATION',required_facts=[])
        self.assertEqual(self.call(destination='core',request=req,attempt='h2')['status'],'SUCCESS')
        current=self.store.current_hash('stage-001')
        old=self.call(authorized=False);self.assertEqual(old['status'],'SUCCESS');self.assertTrue(old['historical'])
        self.assertEqual(old['state'],first['state']);self.assertEqual(self.store.current_hash('stage-001'),current)
        altered=copy.deepcopy(self.request);altered['next_stage']['objective']='different'
        self.assertEqual(self.call(request=altered)['status'],'CONSTRAINT_CONFLICT')

    def test_direct_recovery_cannot_drop_task_record(self):
        r=durable_recover(self.bundle,self.store,self.ledger,task_id='stage-001',destination='A',attempt_id='direct',authorized=True)
        self.assertEqual(r['status'],'VALIDATION_FAILED',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def test_initialize_is_core_only_and_idempotent_exact_record(self):
        store=RecoveryStore(self.root/'initial')
        r=initialize_task(self.bundle,store,self.ledger,record=self.record,input_artifact=self.inputs,authorized=True)
        self.assertEqual(r['status'],'SUCCESS',r);self.assertEqual(r['state']['profile'],'core')
        r2=initialize_task(self.bundle,store,self.ledger,record=self.record,input_artifact=self.inputs,authorized=True)
        self.assertEqual(r2['state'],r['state'])

    def test_warm_artifact_is_not_an_active_overlay(self):
        # Read/cache B bytes but compute under A: residency is not activation.
        b=self.bundle.document['overlays'][1]['artifact'];self.bundle.artifact(b)
        r=self.call();self.assertEqual(r['state']['cache'],[-11,7,19,73])
        self.assertEqual(self.bundle.catalog.profile(r['state']['profile']).overlays,('A',))

    def test_mutated_core_is_detected_before_publication(self):
        (self.fixture/'artifacts/core.json').write_text('{}')
        r=self.call();self.assertEqual(r['status'],'INCOMPATIBLE_CONFIGURATION',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def crash(self,point,request=None):
        req=self.request if request is None else request
        (self.root/'request.json').write_text(json.dumps(req))
        return subprocess.run([sys.executable,str(ROOT/'tests/stage_handoff_crash_worker.py'),str(self.root),point],cwd=ROOT,capture_output=True,text=True)

    def test_process_crash_windows(self):
        act=self.marker();receipt=self.ledger.perform(act)
        rec=copy.deepcopy(self.record);rec['receipts']=[{'key':act['key'],'kind':'mock_action','receipt':receipt}]
        self.source=attach_task_record(checkpoint(self.bundle,'AB','stage-001',self.inputs),rec)
        self.source_hash=checkpoint_hash(self.source);self.request['source_checkpoint_hash']=self.source_hash
        for point in ('after_prepare','after_compute','after_stage','after_publish'):
            with self.subTest(point=point):
                self.store=RecoveryStore(self.root/'recovery')
                # Reset this isolated test's store and request per crash window.
                shutil.rmtree(self.root/'recovery');self.store=RecoveryStore(self.root/'recovery');self.store.publish_initial(self.source)
                p=self.crash(point);self.assertEqual(p.returncode,73,p.stdout+p.stderr)
                self.store=RecoveryStore(self.root/'recovery');self.ledger=Ledger(self.root/'actions')
                before=self.store.current('stage-001')
                self.assertEqual(before['profile'],'A' if point=='after_publish' else 'AB')
                r=self.call();self.assertEqual(r['status'],'SUCCESS',r)
                self.assertEqual(r['state']['cache'],[-11,7,19,73])
                self.assertEqual(r['state']['task_record']['facts'][0]['unit'],'m/s')
                self.assertEqual(self.store.inspect_attempt('h1')['status'],'PUBLISHED')
                self.assertEqual(self.store.current_hash('stage-001'),checkpoint_hash(r['state']))
                self.assertEqual(self.ledger.effect_count(),1)
                self.assertEqual(r['state']['task_record']['receipts'],rec['receipts'])

    def test_resume_rechecks_authorization_and_request(self):
        self.assertEqual(self.crash('after_stage').returncode,73)
        self.assertEqual(self.call(authorized=False)['status'],'AUTHORIZATION_DENIED')
        req=copy.deepcopy(self.request);req['next_stage']['requested_output']='substituted'
        self.assertEqual(self.call(request=req)['status'],'CONSTRAINT_CONFLICT')
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)
        self.assertEqual(self.call()['status'],'SUCCESS')

    def test_resume_rechecks_source_and_action_evidence(self):
        self.assertEqual(self.crash('after_prepare').returncode,73)
        self.ledger.perform(self.marker())
        self.assertEqual(self.call()['status'],'RECOVERY_REQUIRED')
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def test_staged_task_record_substitution_is_rejected(self):
        self.assertEqual(self.crash('after_stage').returncode,73)
        attempt=self.store.inspect_attempt('h1')
        with database(self.store.path) as db:
            row=db.execute('SELECT body FROM checkpoints WHERE key=?',(attempt['staged_checkpoint_hash'],)).fetchone()
            v=decode(row[0]);v['task_record']['goal']='changed maliciously'
            key=checkpoint_hash(v)
            db.execute('INSERT INTO checkpoints(key,body) VALUES (?,?)',(key,json.dumps(v)))
            attempt['staged_checkpoint_hash']=key
            db.execute('UPDATE attempts SET body=? WHERE key=?',(json.dumps(attempt),'h1'))
        r=self.call();self.assertEqual(r['status'],'INCOMPATIBLE_CONFIGURATION',r)
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)

    def test_corrupt_record_and_missing_database_fail_closed(self):
        with database(self.store.path) as db:
            v=copy.deepcopy(self.source);v['task_record']['goal']='altered'
            db.execute('UPDATE checkpoints SET body=? WHERE key=?',(json.dumps(v),self.source_hash))
        r=self.call();self.assertEqual(r['status'],'VALIDATION_FAILED',r);self.assertIsNone(r['state'])
        self.store.path.unlink()
        r=self.call();self.assertEqual(r['status'],'RECOVERY_REQUIRED',r);self.assertIsNone(r['state'])

    def test_historical_target_substitution_fails_without_reactivation(self):
        first=self.call();self.assertEqual(first['status'],'SUCCESS')
        current=self.store.current_hash('stage-001')
        attempt=self.store.inspect_attempt('h1')
        with database(self.store.path) as db:
            v=copy.deepcopy(first['state']);v['task_record']['goal']='different history'
            h=checkpoint_hash(v)
            db.execute('INSERT INTO checkpoints(key,body) VALUES (?,?)',(h,json.dumps(v)))
            attempt.update(staged_checkpoint_hash=h,published_checkpoint_hash=h)
            db.execute('UPDATE attempts SET body=? WHERE key=?',(json.dumps(attempt),'h1'))
        r=self.call();self.assertEqual(r['status'],'INCOMPATIBLE_CONFIGURATION',r)
        self.assertEqual(self.store.current_hash('stage-001'),current)

    def test_explicit_dependent_b_profile_rejected(self):
        m=read_json(self.fixture/'manifest.json')
        m['profiles'].append({'id':'B','overlays':['B'],'evidence_ref':'fixture:not-enough'})
        (self.fixture/'manifest.json').write_text(json.dumps(m))
        self.assert_code(lambda:Bundle(self.fixture/'manifest.json'),'INCOMPATIBLE_CONFIGURATION')

    def test_staged_load_failure_retains_record_and_profile(self):
        self.assertEqual(self.crash('after_stage').returncode,73)
        r=self.call(load_ok=False);self.assertEqual(r['status'],'INTERNAL_FAILURE',r)
        self.assertEqual(self.store.current('stage-001'),self.source)
        self.assertEqual(self.store.inspect_attempt('h1')['status'],'FAILED')

    def test_missing_source_after_stage_does_not_publish(self):
        self.assertEqual(self.crash('after_stage').returncode,73)
        p=self.fixture/'problem.json';original=p.read_bytes();p.unlink()
        self.assertEqual(self.call()['status'],'INSUFFICIENT_EVIDENCE')
        self.assertEqual(self.store.current_hash('stage-001'),self.source_hash)
        p.write_bytes(original)
        self.assertEqual(self.call()['status'],'SUCCESS')

    def test_finish_can_append_a_new_verified_mock_receipt(self):
        r=self.call();a=self.marker('new-output');receipt=self.ledger.perform(a)
        f=finish_stage(self.bundle,self.store,self.ledger,task_id='stage-001',expected_checkpoint_hash=checkpoint_hash(r['state']),new_results=[],new_receipts=[{'key':a['key'],'kind':'presented_output','receipt':receipt}],authorized=True)
        self.assertEqual(f['status'],'SUCCESS',f)
        self.assertEqual(self.ledger.effect_count(),1)
        self.assertEqual(len(f['state']['task_record']['receipts']),1)

    def test_assumption_cannot_supply_required_fact(self):
        rec=copy.deepcopy(self.record);rec['facts']=[]
        rec['assumptions'].append({'id':'speed','text':'Probably 10 m/s','source_ids':['source-1']})
        self.reseed(rec)
        self.assertEqual(self.call()['status'],'NEEDS_CLARIFICATION')

    def test_source_path_escape_and_invalid_flags_rejected(self):
        rec=copy.deepcopy(self.record);rec['sources'][0]['artifact']['path']='../outside.json'
        self.assert_code(lambda:validate_task_record(rec),'VALIDATION_FAILED')
        self.assertEqual(self.call(authorized='yes')['status'],'VALIDATION_FAILED')
        self.assertEqual(self.call(load_ok=1)['status'],'VALIDATION_FAILED')

    def test_duplicate_source_fields_and_oversized_evidence(self):
        from hashlib import sha256
        ev=read_json(self.fixture/'problem.json');ev['fields'].append(copy.deepcopy(ev['fields'][0]))
        p=self.fixture/'problem.json';p.write_text(json.dumps(ev))
        rec=copy.deepcopy(self.record);rec['sources'][0]['artifact']['sha256']=sha256(p.read_bytes()).hexdigest();self.reseed(rec)
        self.assertEqual(self.call()['status'],'VALIDATION_FAILED')
        p.write_text(' '*262145)
        self.assertEqual(self.call(attempt='h2')['status'],'VALIDATION_FAILED')

    def test_record_size_limit_and_revision_parent_required(self):
        rec=copy.deepcopy(self.record)
        rec['assumptions']=[{'id':f'x{i}','text':'x'*4096,'source_ids':[]} for i in range(100)]
        self.assert_code(lambda:validate_task_record(rec),'VALIDATION_FAILED')
        rec=copy.deepcopy(self.record);rec['revision']=1
        self.assert_code(lambda:validate_task_record(rec),'VALIDATION_FAILED')

    def test_public_boundary_missing_current_has_no_fabricated_state(self):
        self.store=RecoveryStore(self.root/'empty')
        r=self.call();self.assertEqual(r['status'],'RECOVERY_REQUIRED');self.assertIsNone(r['state'])

if __name__=='__main__':unittest.main()
