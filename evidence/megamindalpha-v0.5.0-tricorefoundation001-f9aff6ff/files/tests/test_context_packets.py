"""Inspect the byte budget and provenance, not purported neural memory quality."""
from copy import deepcopy
from unittest.mock import patch
from context_helpers import ContextCase, CALLER
from dataset_helpers import ok
from nss_base.context_contracts import byte_count, make_request
from nss_base.neural_contracts import encoded, fingerprint


class PacketTests(ContextCase):
    def test_mandatory_spine_retained_and_irrelevant_items_omitted(self):
        req=self.start_context(); before=self.ctl.inspect('catalog-task'); p=self.built(req)
        for key in ('goal','constraints','clarifications','unresolved_questions','receipts'):
            self.assertEqual(p['payload']['task'][key],before['work']['record'][key])
        self.assertEqual(p['payload']['facts'],[]); self.assertEqual(p['payload']['assumptions'],[])
        self.assertIn({'kind':'fact','id':'speed','reason':'NOT_SELECTED'},p['omissions'])
        self.assertEqual(before,self.ctl.inspect('catalog-task'))
        self.assertEqual(p['usage']['context_bytes'],byte_count(p['payload']))
        self.assertFalse(p['runtime_execution_permit']);self.assertFalse(p['training_authorized'])

    def test_required_fact_exactly_rehydrated_without_changing_task(self):
        req=self.start_context();req['required_fact_ids']=['speed'];p=self.built(req)
        f=p['payload']['facts'][0];self.assertEqual((f['value'],f['unit']),('10','m/s'))
        self.assertEqual(f['rehydrated_fields'],['unit']);self.assertIsNone(self.read()['record']['facts'][0]['unit'])
        self.assertEqual(ok(self.consume(p))['payload'],p['payload'])

    def test_stage_required_facts_cannot_be_omitted_by_empty_selectors(self):
        req=self.start_context(lambda r:r['stage']['required_facts'].append({'fact_id':'speed','fields':['value']}))
        self.assertEqual(self.built(req)['payload']['facts'][0]['id'],'speed')

    def test_unknown_required_fact_is_not_an_assumption(self):
        req=self.start_context();req['required_fact_ids']=['ideal']
        self.rejected('NEEDS_CLARIFICATION',self.service.build(req))

    def test_explicit_optional_ids_are_not_silently_misspelled(self):
        req=self.start_context()
        for key in ('optional_fact_ids','assumption_ids','result_ids'):
            with self.subTest(key=key):
                r=deepcopy(req);r[key]=['absent'];self.rejected('INSUFFICIENT_EVIDENCE',self.service.build(r))

    def test_exact_field_rehydration_and_source_binding(self):
        req=self.start_context();p=self.built(req)
        result=self.service.rehydrate(p,caller_id=CALLER,expected_packet_sha256=fingerprint(p),
            selector={'kind':'TASK_FIELD','source_id':'source-1','field_id':'speed'})
        expanded=ok(result);self.assertEqual(expanded['payload']['source_fields'][0]['field']['unit'],'m/s')
        self.assertEqual(p['payload']['source_fields'],[])
        self.assertEqual(expanded['request']['budget'],p['request']['budget'])

    def test_unknown_or_unselected_source_cannot_be_rehydrated(self):
        p=self.built(self.start_context())
        for selector in ({'kind':'TASK_FIELD','source_id':'missing','field_id':'speed'},
                         {'kind':'TASK_FIELD','source_id':'source-1','field_id':'missing'}):
            self.rejected('INSUFFICIENT_EVIDENCE',self.service.rehydrate(p,caller_id=CALLER,
                expected_packet_sha256=fingerprint(p),selector=selector))

    def test_unresolved_blocking_question_returns_no_packet(self):
        req=self.start_context(lambda r:r['unresolved_questions'].append({'id':'missing','text':'Which item?','blocking':True}))
        self.rejected('NEEDS_CLARIFICATION',self.service.build(req))

    def test_authoritative_clarification_prevents_repeat_question(self):
        def edit(r):r['unresolved_questions'][0]['blocking']=True
        req=self.start_context(edit);self.assertEqual(self.built(req)['payload']['task']['clarifications'][0]['id'],'clarify1')

    def test_mandatory_spine_overflow_has_recovery_and_preserves_state(self):
        req=self.start_context();old=self.ctl.inspect('catalog-task');req['budget']['max_context_bytes']=1
        r=self.rejected('BUDGET_EXHAUSTED',self.service.build(req))
        self.assertGreater(r['recovery']['mandatory_context_bytes'],1)
        self.assertFalse(r['recovery']['task_modified']);self.assertEqual(old,self.ctl.inspect('catalog-task'))

    def test_exact_context_boundary_and_optional_reduction(self):
        req=self.start_context();baseline=self.built(req);limit=baseline['usage']['context_bytes']
        req['budget']['max_context_bytes']=limit
        self.assertEqual(self.built(req)['usage']['context_bytes'],limit)
        req['optional_fact_ids']=['speed'];p=self.built(req)
        self.assertEqual(p['payload']['facts'],[])
        self.assertIn({'kind':'fact','id':'speed','reason':'BUDGET_EXHAUSTED'},p['omissions'])
        req['optional_fact_ids']=[];req['required_fact_ids']=['speed']
        self.rejected('BUDGET_EXHAUSTED',self.service.build(req))

    def test_one_byte_below_spine_fails(self):
        req=self.start_context();req['budget']['max_context_bytes']=self.built(req)['usage']['context_bytes']-1
        self.rejected('BUDGET_EXHAUSTED',self.service.build(req))

    def test_multilingual_bytes_count_the_actual_serialization_not_tokens(self):
        req=self.start_context(lambda r:r.update(goal='日本語 🧠'))
        p=self.built(req);self.assertEqual(p['usage']['context_bytes'],len(encoded(p['payload'])))
        self.assertEqual(p['usage']['unit'],'CANONICAL_JSON_UTF8_BYTES')
        self.assertNotIn('token_count',str(p));self.assertIn('日本語',p['payload']['task']['goal'])

    def test_evidence_budget_enforced_even_when_packet_budget_is_large(self):
        req=self.start_context();req['budget']['max_evidence_bytes']=0
        self.rejected('BUDGET_EXHAUSTED',self.service.build(req))

    def test_irrelevant_local_source_not_read_or_included(self):
        def edit(r):r['sources'].append({'id':'absent','kind':'document','artifact':{'path':'does-not-exist.json','sha256':'a'*64}})
        req=self.start_context(edit);p=self.built(req)
        self.assertEqual([s['id'] for s in p['payload']['sources']],['source-1'])
        self.assertIn({'kind':'source','id':'absent','reason':'NOT_SELECTED'},p['omissions'])

    def test_source_mismatch_and_missing_file_fail_closed(self):
        req=self.start_context();f=self.sources/'problem.json';old=f.read_bytes()
        f.write_bytes(old+b' ');self.rejected('INCOMPATIBLE_CONFIGURATION',self.service.build(req));f.write_bytes(old)
        f.unlink();self.rejected('INSUFFICIENT_EVIDENCE',self.service.build(req))

    def test_fact_conflicts_are_not_summarized_away(self):
        req=self.start_context(lambda r:r['facts'][0].update(value='999'));req['required_fact_ids']=['speed']
        self.rejected('CONSTRAINT_CONFLICT',self.service.build(req))

    def test_task_fact_remains_separate_from_assumption_and_checked_result(self):
        req=self.start_context();req['optional_fact_ids']=['speed'];req['assumption_ids']=['ideal']
        p=self.built(req);self.assertEqual(p['payload']['assumptions'][0]['id'],'ideal')
        self.assertEqual([f['id'] for f in p['payload']['facts']],['speed'])

    def test_packet_digest_does_not_replace_semantic_revalidation(self):
        p=self.built(self.start_context());bad=deepcopy(p);bad['payload']['task']['goal']='Substituted goal'
        bad['payload_sha256']=fingerprint(bad['payload']);bad['usage']['context_bytes']=byte_count(bad['payload'])
        self.rejected('INCOMPATIBLE_CONFIGURATION',self.consume(bad))

    def test_omission_tamper_fails_even_with_recomputed_outer_hash(self):
        p=self.built(self.start_context());p['omissions']=[]
        self.rejected('INCOMPATIBLE_CONFIGURATION',self.consume(p))

    def test_wrong_hash_and_wrong_caller_fail(self):
        p=self.built(self.start_context())
        self.rejected('VALIDATION_FAILED',self.service.consume(p,caller_id=CALLER,expected_packet_sha256='0'*64))
        self.rejected('AUTHORIZATION_DENIED',self.consume(p,'different-caller'))

    def test_sealed_task_revision_rejects_prior_packet(self):
        p=self.built(self.start_context());self.finished()
        self.rejected('INCOMPATIBLE_CONFIGURATION',self.consume(p))

    def test_closed_stage_rejects_prior_packet(self):
        p=self.built(self.start_context());self.ctl.apply(self.command('CANCEL'))
        self.rejected('INCOMPATIBLE_CONFIGURATION',self.consume(p))

    def test_generation_withdrawal_blocks_packet_use(self):
        p=self.built(self.start_context());self.manager.revoke(self.hashes[1],kind='QUALIFICATION',actor_id='generation-reviewer',reason='fixture')
        self.rejected('AUTHORIZATION_DENIED',self.consume(p))

    def test_checked_profile_return_works_and_old_packet_stays_stale(self):
        old=self.built(self.start_context());self.finished();self.ctl.apply(self.move_command())
        a=self.built(make_request(self.read(),CALLER));self.finished()
        self.ctl.apply(self.move_command('control','evaluate','EVALUATION'))
        core=self.built(make_request(self.read(),CALLER));self.assertEqual(core['request']['ticket']['profile'],'CORE')
        for p in (old,a):self.rejected('INCOMPATIBLE_CONFIGURATION',self.consume(p))

    def test_state_change_during_assembly_is_caught_before_output(self):
        req=self.start_context();original=self.service._view;count=0
        def reading(r):
            nonlocal count
            count+=1
            if count==2:self.finished()
            return original(r)
        with patch.object(self.service,'_view',side_effect=reading):
            self.rejected('INCOMPATIBLE_CONFIGURATION',self.service.build(req))
