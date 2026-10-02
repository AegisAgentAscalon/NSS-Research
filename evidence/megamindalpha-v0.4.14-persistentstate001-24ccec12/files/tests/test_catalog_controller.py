"""Observable selection/task contracts; share the real qualified generation fixture."""
from copy import deepcopy
from pathlib import Path
import shutil
from catalog_helpers import CatalogCase, CALLER
from nss_base.catalog_contracts import descriptor, selection_request, select_profile, require_state_identity
from nss_base.catalog_controller import fixture_descriptor, CatalogController
from nss_base.generation_store import Generations
from nss_base.neural_contracts import fingerprint
from nss_base.neural_data import ProbeData
from nss_base.ledger import Ledger
from nss_base.runtime import ContractError


class CatalogTests(CatalogCase):
    def test_known_capabilities_select_exact_profiles_without_mutation(self):
        before = self.manager.inspect()
        for cap, name in [('interpret','AB'),('solve','A'),('control','CORE')]:
            selected = self.ctl.select(self.req(cap), caller_id=CALLER)
            self.assertEqual(selected['profile'], name); self.assertFalse(selected['runtime_execution_permit'])
        self.assertEqual(before, self.manager.inspect())

    def test_live_catalogue_describes_all_exact_profiles(self):
        v=self.ctl.catalog(expected_current=self.manager.inspect()['current'])
        self.assertEqual(v['descriptor'],self.desc);self.assertFalse(v['runtime_execution_permit'])
        self.assertEqual(v['catalog_sha256'],self.catalog_hash)

    def test_multiple_reviewed_catalogues_require_exact_choice(self):
        d=deepcopy(self.desc);d['catalog_id']='catalog-two'
        self.ctl.register(d,reviewer_id='generation-reviewer')
        self.error('NEEDS_CLARIFICATION',self.ctl.catalog,expected_current=self.manager.inspect()['current'])
        self.assertEqual(self.ctl.catalog(expected_current=self.manager.inspect()['current'],catalog_sha256=self.catalog_hash)['descriptor'],self.desc)

    def test_every_requested_label_must_fit_one_profile_not_a_union(self):
        req = self.req(); req['capabilities'] = ['interpret','solve']
        self.error('CAPABILITY_UNAVAILABLE', self.ctl.select, req, caller_id=CALLER)

    def test_unknown_capability_is_not_approximated(self):
        self.error('CAPABILITY_UNAVAILABLE', self.ctl.select, self.req('unseen'), caller_id=CALLER)

    def test_unreleased_B_profile_cannot_be_advertised(self):
        d=deepcopy(self.desc); d['profiles'][0]['id']='B'
        self.error('INCOMPATIBLE_CONFIGURATION', descriptor,d,self.gs[1])

    def test_core_only_is_required_in_descriptor(self):
        d=deepcopy(self.desc);d['profiles']=[p for p in d['profiles'] if p['id']!='CORE']
        self.error('INCOMPATIBLE_CONFIGURATION',descriptor,d,self.gs[1])

    def test_control_and_evaluation_do_not_select_a_specialist(self):
        for mode in ('CONTROL','EVALUATION'):
            self.error('CAPABILITY_UNAVAILABLE',self.ctl.select,self.req('interpret',mode=mode),caller_id=CALLER)
            self.assertEqual(self.ctl.select(self.req('control',mode=mode),caller_id=CALLER)['profile'],'CORE')

    def test_ties_require_clarification_but_valid_current_tie_stays(self):
        d=deepcopy(self.desc)
        for p in d['profiles']:
            p['capabilities']=['shared'];p['load_units']=0;p['step_units']=1
        req=self.req('shared');req['catalog_sha256']=fingerprint(d)
        self.error('NEEDS_CLARIFICATION',select_profile,d,self.gs[1],req)
        self.assertEqual(select_profile(d,self.gs[1],req,'AB')['profile'],'AB')

    def test_switch_cost_favors_staying_when_cheaper(self):
        req=self.req('shared')
        picked=select_profile(self.desc,self.gs[1],req,'AB')
        self.assertEqual(picked['profile'],'A')  # 8+2 < 12+0
        d=deepcopy(self.desc);d['profiles'][0]['load_units']=100;req['catalog_sha256']=fingerprint(d)
        self.assertEqual(select_profile(d,self.gs[1],req,'AB')['profile'],'AB')

    def test_reverse_edge_cannot_be_inferred(self):
        self.started(cap='solve');self.finished()
        self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.apply,self.move_command('interpret'))
        self.assertEqual(self.ctl.inspect('catalog-task')['ticket']['profile'],'A')

    def test_multi_hop_is_not_silently_synthesized(self):
        self.started();self.finished()
        self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.apply,self.move_command('control',mode='CONTROL'))

    def test_stale_epoch_or_manifest_blocks_selection(self):
        for field,value in [('epoch',99),('generation_sha256',self.hashes[0])]:
            req=self.req();req['expected_current'][field]=value
            self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.select,req,caller_id=CALLER)

    def test_reviewed_descriptor_cannot_be_substituted_by_an_unregistered_hash(self):
        r=self.req();r['catalog_sha256']='0'*64
        self.error('INSUFFICIENT_EVIDENCE',self.ctl.select,r,caller_id=CALLER)

    def test_self_review_and_wrong_role_rejected(self):
        self.error('AUTHORIZATION_DENIED',self.ctl.register,self.desc,reviewer_id='fixture-builder')
        self.error('AUTHORIZATION_DENIED',self.ctl.select,self.req(),caller_id='release-owner')

    def test_descriptor_name_cannot_be_redefined(self):
        d=deepcopy(self.desc);d['profiles'][0]['load_units']+=1
        self.error('CONSTRAINT_CONFLICT',self.ctl.register,d,reviewer_id='generation-reviewer')
        self.assertTrue(self.ctl.register(self.desc,reviewer_id='generation-reviewer')['historical'])

    def test_declared_serialized_byte_cost_must_match_artifacts(self):
        d=deepcopy(self.desc);d['catalog_id']='wrong-size';d['profiles'][0]['sealed_document_bytes']+=1
        self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.register,d,reviewer_id='generation-reviewer')

    def test_live_child_withdrawal_blocks_selection_and_read(self):
        self.started();self.withdraw_child()
        self.error('AUTHORIZATION_DENIED',self.read)
        self.error('AUTHORIZATION_DENIED',self.ctl.select,self.req(task='fresh'),caller_id=CALLER)
        self.assertEqual(self.manager.inspect()['open_stages'],1)

    def test_source_permission_revocation_blocks_current_read(self):
        self.started();ProbeData(self.root/'probe/data').revoke_for_test()
        self.error('TRAINING_RESTRICTED',self.read)

    def test_finish_move_core_return_and_close_preserve_portable_work(self):
        c,r=self.started(task='neural-probe-replay');old=self.read('neural-probe-replay')
        self.finished('neural-probe-replay');move=self.move_command(task='neural-probe-replay')
        move['request']['stage']['required_facts']=[{'fact_id':'speed','fields':['value','unit']}]
        self.ctl.apply(move);new=self.read('neural-probe-replay')
        self.assertEqual(new['record']['facts'][0]['unit'],'m/s')
        for field in ('goal','sources','assumptions','clarifications','constraints','receipts','original_request','unresolved_questions'):
            self.assertEqual(new['record'][field],old['record'][field],field)
        self.error('INCOMPATIBLE_CONFIGURATION',require_state_identity,old['task_state_identity'],new)
        self.assertTrue(require_state_identity(new['task_state_identity'],new))
        self.finished('neural-probe-replay');self.ctl.apply(self.move_command('control','s3','EVALUATION',task='neural-probe-replay'))
        final=self.read('neural-probe-replay');self.assertEqual(set(final['artifacts']),{'core'})
        self.finished('neural-probe-replay');self.ctl.apply(self.command('CLOSE',task='neural-probe-replay'))
        self.assertEqual(self.manager.inspect()['open_stages'],0)
        self.assertTrue(self.ctl.apply(c)['historical']);self.assertEqual(self.ledger.effect_count(),1)

    def test_unfinished_source_blocks_move_and_plain_close(self):
        _,r=self.started()
        self.error('CONSTRAINT_CONFLICT',self.ctl.apply,self.move_command())
        self.error('CONSTRAINT_CONFLICT',self.ctl.apply,self.command('CLOSE'))
        self.error('CONSTRAINT_CONFLICT',self.manager.close_stage,r['ticket'],caller_id=CALLER)
        self.error('CONSTRAINT_CONFLICT',self.manager.read_stage,r['ticket'],caller_id=CALLER,**self.ev)

    def test_one_current_registered_stage_blocks_release_and_other_task(self):
        self.started();self.error('RECOVERY_REQUIRED',self.ctl.apply,self.start_command(task='other'))
        key,opts=self.issued(0,'update','UPDATE')
        self.error('RECOVERY_REQUIRED',self.manager.prepare,key,**opts)
        self.assertEqual(self.manager.inspect()['open_stages'],1)

    def test_same_profile_new_stage_still_invalidates_stage_cache(self):
        self.started();old=self.read();self.finished();self.ctl.apply(self.move_command('interpret'))
        new=self.read();self.assertEqual(old['ticket']['profile'],new['ticket']['profile'])
        self.error('INCOMPATIBLE_CONFIGURATION',require_state_identity,old['task_state_identity'],new)

    def test_old_record_revision_and_closed_ticket_rejected(self):
        _,r=self.started();self.finished()
        self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.read,r['ticket'],caller_id=CALLER,expected_record_sha256=r['record_sha256'])
        self.ctl.apply(self.move_command());self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.read,r['ticket'],caller_id=CALLER,expected_record_sha256=r['record_sha256'])

    def test_finished_stage_not_live_readable(self):
        self.started();self.finished();self.error('CONSTRAINT_CONFLICT',self.read)

    def test_same_task_cannot_restart_after_close_or_cancellation(self):
        self.started();self.ctl.apply(self.command('CANCEL'))
        c=self.start_command();c['operation_id']='restart';c['ticket_id']='restart'
        self.error('CONSTRAINT_CONFLICT',self.ctl.apply,c)

    def test_task_and_stage_identity_reuse_rejected(self):
        self.started();self.finished();c=self.move_command();c['request']['task_id']='other'
        self.error('CONSTRAINT_CONFLICT',self.ctl.apply,c)
        c=self.move_command();c['request']['stage']['id']='s1'
        self.error('CONSTRAINT_CONFLICT',self.ctl.apply,c)

    def test_pairs_may_not_change_during_handoff(self):
        self.started();self.finished();c=self.move_command();c['request']['pairs']=[[15,15]]
        self.error('VALIDATION_FAILED',self.ctl.apply,c)

    def test_task_pins_exact_descriptor_throughout_handoffs(self):
        self.started();self.finished();d=deepcopy(self.desc);d['catalog_id']='other'
        h=self.ctl.register(d,reviewer_id='generation-reviewer')['catalog_sha256'];c=self.move_command();c['request']['catalog_sha256']=h
        self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.apply,c)

    def test_missing_exact_source_preserves_source_stage(self):
        self.started();self.finished();c=self.move_command();c['request']['stage']['required_facts']=[{'fact_id':'missing','fields':['unit']}]
        before=self.ctl.inspect('catalog-task');self.error('NEEDS_CLARIFICATION',self.ctl.apply,c)
        self.assertEqual(before,self.ctl.inspect('catalog-task'))

    def test_blocking_question_stops_handoff(self):
        c=self.start_command();c['record']['unresolved_questions'].append({'id':'ask','text':'Unknown','blocking':True})
        self.ctl.apply(c);self.finished();self.error('NEEDS_CLARIFICATION',self.ctl.apply,self.move_command())

    def test_initial_required_fact_cannot_be_guessed(self):
        c=self.start_command();required=[{'fact_id':'speed','fields':['unit']}]
        c['request']['stage']['required_facts']=required;c['record']['stage']['required_facts']=required
        self.error('NEEDS_CLARIFICATION',self.ctl.apply,c)
        c['record']['facts'][0]['unit']='km/h';self.error('CONSTRAINT_CONFLICT',self.ctl.apply,c)

    def test_new_result_must_bind_selected_neural_ecid(self):
        self.started();c=self.command('FINISH',results=[{'id':'r','text':'test','check_ref':'check',
            'producer_ecid':'0'*64,'source_ids':[]}])
        self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.apply,c)

    def test_cancellation_preserves_unfinished_record_and_reason_after_revocation(self):
        self.started(task='neural-probe-replay');before=self.ctl.inspect('neural-probe-replay')
        self.withdraw_child();c=self.command('CANCEL',task='neural-probe-replay');r=self.ctl.apply(c)
        after=self.ctl.inspect('neural-probe-replay')
        self.assertEqual(r['phase'],'CANCELLED');self.assertTrue(after['closed'])
        self.assertFalse(after['work']['record']['stage']['sealed'])
        for key in ('facts','receipts','assumptions','constraints'):
            self.assertEqual(before['work']['record'][key],after['work']['record'][key])
        self.assertEqual(after['work']['cancellation_reason'],c['reason'])
        self.assertTrue(self.ctl.apply(c)['historical'])

    def test_pending_effect_blocks_cancel_until_explicit_reconciliation(self):
        self.started();a={'schema_version':1,'task_id':'catalog-task','key':'pending',
            'payload':{'operation':'append_marker','value':'test'},'status':'PENDING','receipt':None}
        # The owner records one real mock effect; omitting its receipt blocks closure.
        receipt=self.ledger.perform(a)
        self.error('RECOVERY_REQUIRED',self.ctl.apply,self.command('CANCEL'))
        c=self.command('CANCEL',receipts=[{'key':'pending','kind':'mock_action','receipt':receipt}])
        self.ctl.apply(c);self.assertEqual(self.ledger.effect_count(),2)
        self.assertTrue(self.ctl.apply(c)['historical']);self.assertEqual(self.ledger.effect_count(),2)

    def test_ledger_and_source_owner_substitution_blocked(self):
        self.started();c=self.command('FINISH');other=Ledger(self.root/'other-ledger')
        self.error('VALIDATION_FAILED',self.manager.task_operation,c,ledger=other,evidence_root=self.sources,**self.ev)
        self.error('VALIDATION_FAILED',self.manager.task_operation,c,ledger=self.ledger,evidence_root=self.root,**self.ev)

    def test_historical_retry_never_reopens_after_epoch_change(self):
        c,r=self.started();self.finished();self.ctl.apply(self.command('CLOSE'))
        self.adopted(0,'update','UPDATE');before=self.manager.inspect()
        self.assertTrue(self.ctl.apply(c)['historical']);self.assertEqual(before,self.manager.inspect())
        self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.read,r['ticket'],caller_id=CALLER,expected_record_sha256=r['record_sha256'])

    def test_retry_substitution_rejected(self):
        c,r=self.started();altered=deepcopy(c);altered['record']['goal']='different'
        self.error('VALIDATION_FAILED',self.ctl.apply,altered)

    def test_finish_after_withdrawal_records_work_but_does_not_restore_permission(self):
        self.started();self.withdraw_child();self.finished()
        self.error('AUTHORIZATION_DENIED',self.ctl.apply,self.move_command())
        self.ctl.apply(self.command('CLOSE'));self.assertTrue(self.ctl.inspect('catalog-task')['closed'])

    def test_bad_fault_hook_rejected_without_change(self):
        before=self.manager.inspect();self.error('VALIDATION_FAILED',self.ctl.apply,self.start_command(),fault_at='typo')
        self.assertEqual(before,self.manager.inspect())


# Exact failure stimuli share a test body, not separate copied fixture setup.
for name,field,value in [('negative_load','load_units',-1),('bool_cost','step_units',True),
                         ('float_cost','step_units',1.5),('no_pairs','max_pairs',0),('oversize_pairs','max_pairs',257)]:
    def test(self, field=field, value=value):
        d=deepcopy(self.desc);d['profiles'][0][field]=value
        self.error('VALIDATION_FAILED',descriptor,d,self.gs[1])
    setattr(CatalogTests,'test_invalid_descriptor_'+name,test)
for key in ('max_document_bytes','max_cost_units'):
    def test(self,key=key):
        req=self.req();req['budget'][key]=0
        self.error('BUDGET_EXHAUSTED',self.ctl.select,req,caller_id=CALLER)
    setattr(CatalogTests,'test_budget_'+key,test)


class CatalogSourceTests(CatalogCase):
    def test_missing_and_tampered_exact_sources_block_handoff(self):
        local=self.root/'handoff-sources';shutil.copytree(self.sources,local)
        self.sources=local;self.ctl=CatalogController(self.manager,ledger=self.ledger,evidence_root=local,**self.ev)
        self.started();self.finished();cmd=self.move_command()
        cmd['request']['stage']['required_facts']=[{'fact_id':'speed','fields':['unit']}]
        before=self.ctl.inspect('catalog-task');p=local/'problem.json';raw=p.read_bytes();p.unlink()
        self.error('INSUFFICIENT_EVIDENCE',self.ctl.apply,cmd)
        p.write_bytes(raw+b' ');self.error('INCOMPATIBLE_CONFIGURATION',self.ctl.apply,cmd)
        self.assertEqual(before,self.ctl.inspect('catalog-task'))
        p.write_bytes(raw);self.ctl.apply(cmd);self.assertEqual(self.read()['record']['facts'][0]['unit'],'m/s')

    def test_malformed_command_variants_fail_without_mutation(self):
        c=self.start_command();before=self.manager.inspect()
        cases=[{},None,{'action':'MAGIC'}]
        for key,value in [('schema_version',True),('ticket_id',''),('caller_id',[]),('extra','not allowed')]:
            x=deepcopy(c);x[key]=value;cases.append(x)
        for x in cases:
            with self.subTest(command=x):
                with self.assertRaises(ContractError):self.ctl.apply(x)
        self.assertEqual(before,self.manager.inspect())

    def test_malformed_view_does_not_raise_untyped_key_error(self):
        for v in (None, [], {}, {'record':{}}):
            self.error('VALIDATION_FAILED',require_state_identity,'0'*64,v)
