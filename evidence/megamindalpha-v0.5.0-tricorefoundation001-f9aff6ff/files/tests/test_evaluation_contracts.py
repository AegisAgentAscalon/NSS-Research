from copy import deepcopy
from hashlib import sha256
import json
from pathlib import Path
from unittest.mock import patch

from nss_base.evaluation_contracts import make_report, normalize_plan, normalize_suite, validate_material, validate_report
from nss_base.evaluation_inputs import capture_inputs
from nss_base.runtime import ContractError, digest
from nss_base.serialization import decode
from evaluation_helpers import EvaluationCase, ok

class EvaluationContractTests(EvaluationCase):
    def test_complete_pass_and_exact_trial_matrix(self):
        ref=ok(self.execute());r=self.report()
        self.assertEqual(ref['verdict'],'PASS');self.assertEqual(r['completed_checks'],6)
        self.assertEqual(r['trials'][0]['observed'],[-11,7,19,73]);self.assertTrue(r['reproducible'])
        self.assertEqual(r['repeats'][0]['sha256'],r['repeats'][1]['sha256'])

    def test_mandatory_failure_beats_zero_average_threshold(self):
        self.edit_suite(lambda s:(s.update(minimum_pass_basis_points=0),s['tests'][0].update(expected=[0])))
        self.assertEqual(ok(self.execute())['verdict'],'FAIL')

    def test_optional_failure_allowed_only_by_frozen_threshold(self):
        self.edit_suite(lambda s:(s.update(minimum_pass_basis_points=6666),s['tests'][2].update(expected=[0])))
        self.assertEqual(ok(self.execute())['verdict'],'PASS')

    def test_optional_failure_can_fail_overall_threshold(self):
        self.edit_suite(lambda s:s['tests'][2].update(expected=[0]))
        self.assertEqual(ok(self.execute())['verdict'],'FAIL')

    def test_incomplete_budget_is_not_pass_or_silent_subset(self):
        self.plan['max_evaluations']=1;r=ok(self.execute());report=self.report()
        self.assertEqual(r['verdict'],'INCONCLUSIVE');self.assertEqual(report['completed_checks'],1)
        self.assertEqual(report['expected_checks'],6);self.assertEqual(report['stop_reason'],'BUDGET_EXHAUSTED')
        self.assertIsNone(report['reproducible'])

    def test_budget_exhaustion_after_full_first_repeat_is_inconclusive(self):
        self.plan['max_evaluations']=3;ok(self.execute());r=self.report()
        self.assertEqual(r['verdict'],'INCONCLUSIVE');self.assertTrue(r['repeats'][0]['complete']);self.assertFalse(r['repeats'][1]['complete'])

    def test_one_repeat_makes_no_repeatability_claim(self):
        self.plan['repeats']=1;ok(self.execute());self.assertIsNone(self.report()['reproducible'])

    def test_zero_negative_boolean_and_oversized_budgets_rejected(self):
        for value in (0,-1,True,161,'1'):
            with self.subTest(value=value):
                p=deepcopy(self.plan);p['max_evaluations']=value
                self.assertEqual(self.execute(p)['status'],'VALIDATION_FAILED')

    def test_unknown_plan_fields_never_get_ignored(self):
        self.plan['approve_deployment']=True;self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_invalid_timestamp_is_not_accepted(self):
        self.plan['at']='2026-02-30T10:00:00Z';self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_plan_requires_local_human_attestation_not_model_claim(self):
        self.plan['actor']['kind']='MODEL';self.assertEqual(self.execute()['status'],'AUTHORIZATION_DENIED')

    def test_suite_requires_explicit_evaluation_use_attestation(self):
        self.edit_suite(lambda s:s['evaluation_permission']['actor'].update(kind='MODEL'))
        self.assertEqual(self.execute()['status'],'AUTHORIZATION_DENIED')

    def test_development_suite_cannot_be_relabelled_hidden_release(self):
        self.edit_suite(lambda s:s.update(purpose='PROTECTED_RELEASE'))
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_duplicate_test_ids_rejected(self):
        self.edit_suite(lambda s:s['tests'][1].update(id=s['tests'][0]['id']))
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_zero_mandatory_tests_rejected(self):
        self.edit_suite(lambda s:[t.update(mandatory=False) for t in s['tests']])
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_unknown_checker_and_executable_field_rejected(self):
        self.edit_suite(lambda s:s['tests'][0].update(checker='run_python'))
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')
        self.edit_suite(lambda s:s['tests'][0].update(checker='exact_integer_sequence_v1',command='rm'))
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_unknown_profile_and_incorrect_ecid_rejected(self):
        self.plan['candidate']['profile']='B'
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')
        self.plan['candidate']['profile']='A';self.plan['candidate']['expected_ecid']='0'*64
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_altered_candidate_bytes_rejected(self):
        (self.inputs/'candidate/artifacts/A.json').write_text('{"schema_version":1,"multiply":7,"add":9}')
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_altered_manifest_bytes_even_whitespace_rejected(self):
        p=self.inputs/'candidate/manifest.json';p.write_text(p.read_text()+' ')
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_altered_suite_bytes_rejected(self):
        p=self.inputs/'suite.json';p.write_text(p.read_text()+' ')
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_altered_fixture_bytes_rejected(self):
        p=self.inputs/'case_1.json';p.write_text(p.read_text()+' ')
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_missing_fixture_rejected(self):
        (self.inputs/'case_1.json').unlink();self.assertEqual(self.execute()['status'],'INSUFFICIENT_EVIDENCE')

    def test_path_traversal_absolute_and_noncanonical_rejected(self):
        for name in ('../suite.json','/tmp/suite.json','a//suite.json','./suite.json','a\\suite.json','file:foo'):
            with self.subTest(name=name):
                p=deepcopy(self.plan);p['suite']['path']=name
                self.assertEqual(self.execute(p)['status'],'VALIDATION_FAILED')

    def test_symlink_escape_rejected(self):
        external=self.root/'outside.json';external.write_bytes((self.inputs/'case_1.json').read_bytes())
        (self.inputs/'case_1.json').unlink();(self.inputs/'case_1.json').symlink_to(external)
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_duplicate_json_key_in_suite_rejected(self):
        path=self.inputs/'suite.json';path.write_text(path.read_text().rstrip()[:-1]+',"schema_version":1}')
        self.rehash_suite();self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_nonfinite_cyclic_deep_and_wrong_type_inputs_rejected(self):
        bad=deepcopy(self.plan);bad['repeats']=float('nan')
        cyclic={};cyclic['loop']=cyclic
        deep=0
        for i in range(26):deep=[deep]
        for p in (bad,cyclic,deep,[],None):
            with self.subTest(kind=type(p).__name__):
                self.assertEqual(self.store.execute(p,root=self.inputs)['status'],'VALIDATION_FAILED')

    def test_file_byte_budget_enforced(self):
        (self.inputs/'case_1.json').write_bytes(b' '*(1024*1024+1))
        self.assertEqual(self.execute()['status'],'BUDGET_EXHAUSTED')

    def test_input_vector_budget_enforced(self):
        p=self.inputs/'case_1.json';p.write_text(json.dumps({'schema_version':1,'values':[1]*65}))
        self.edit_suite(lambda s:s['tests'][0]['fixture'].update(sha256=sha256(p.read_bytes()).hexdigest()))
        self.assertEqual(self.execute()['status'],'BUDGET_EXHAUSTED')

    def test_implementation_identity_mismatch_rejected(self):
        self.plan['implementation_sha256']='f'*64
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_material_raw_bytes_and_roles_are_revalidated(self):
        m=capture_inputs(self.plan,self.inputs)
        for edit in (lambda x:x['files'][0].update(text='{}'),lambda x:x['files'][0].update(role='suite'),lambda x:x['files'].append(x['files'][0])):
            with self.subTest(edit=str(edit)):
                b=deepcopy(m);edit(b)
                with self.assertRaises(ContractError):validate_material(self.plan,b)

    def test_material_code_digest_cannot_be_relabelled(self):
        m=capture_inputs(self.plan,self.inputs);m['implementation']['environment']['python']='forged'
        with self.assertRaises(ContractError):validate_material(self.plan,m)

    def test_trial_omission_reordering_or_fabrication_is_rejected(self):
        m=capture_inputs(self.plan,self.inputs);r=make_report(self.plan,m)
        for rows in (r['trials'][:-1],list(reversed(r['trials'])),[dict(t,passed=True,observed=[0]) for t in r['trials']]):
            with self.subTest(rows=len(rows)):
                with self.assertRaises(ContractError):make_report(self.plan,m,rows)

    def test_report_digest_outcome_scope_and_counts_are_derived(self):
        m=capture_inputs(self.plan,self.inputs);r=make_report(self.plan,m)
        for key,value in [('verdict','FAIL'),('authority','DEPLOY'),('completed_checks',5),('scope','RELEASE'),('plan_sha256','0'*64)]:
            with self.subTest(key=key):
                b=deepcopy(r);b[key]=value
                with self.assertRaises(ContractError):validate_report(self.plan,m,b)

    def test_duplicate_fixture_cases_do_not_artificially_reweight_score(self):
        self.edit_suite(lambda s:s['tests'][1].update(fixture=deepcopy(s['tests'][0]['fixture'])))
        self.assertEqual(self.execute()['status'],'CONSTRAINT_CONFLICT')

    def test_process_identity_requires_restart_after_source_change(self):
        from nss_base.evaluation_inputs import implementation_identity
        changed=implementation_identity();changed['environment']['python']='changed'
        with patch('nss_base.evaluation_inputs._measure_identity',return_value=changed):
            with self.assertRaises(ContractError) as exc:implementation_identity()
        self.assertEqual(exc.exception.code,'INCOMPATIBLE_CONFIGURATION')

    def test_maximum_candidate_operation_count_is_bounded_before_reading(self):
        path=self.inputs/'candidate/manifest.json';d=json.loads(path.read_text())
        d['overlays']=[dict(d['overlays'][0],id='O'+str(i)) for i in range(16)]
        path.write_text(json.dumps(d));self.plan['candidate']['manifest']['sha256']=sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.execute()['status'],'BUDGET_EXHAUSTED')

    def test_core_only_profile_can_be_evaluated_without_overlays(self):
        from nss_base.evaluationrun001 import plan_for
        self.plan=plan_for(self.inputs,'core-only',profile='core')
        def core_expected(s):
            for t in s['tests']:
                x=json.loads((self.inputs/t['fixture']['path']).read_text())['values']
                t['expected']=[2*v+1 for v in x]
        self.edit_suite(core_expected)
        self.assertEqual(ok(self.execute())['verdict'],'PASS')

    def test_missing_core_only_candidate_profile_is_rejected(self):
        path=self.inputs/'candidate/manifest.json';d=json.loads(path.read_text())
        d['profiles']=[p for p in d['profiles'] if p['id']!='core'];d['transitions']=[]
        path.write_text(json.dumps(d));self.plan['candidate']['manifest']['sha256']=sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')

    def test_unqualified_union_and_missing_dependency_are_rejected(self):
        path=self.inputs/'candidate/manifest.json';d=json.loads(path.read_text())
        next(p for p in d['profiles'] if p['id']=='AB')['overlays']=['B']
        path.write_text(json.dumps(d));self.plan['candidate']['manifest']['sha256']=sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_candidate_execution_order_is_not_treated_as_a_set(self):
        path=self.inputs/'candidate/manifest.json';d=json.loads(path.read_text())
        next(p for p in d['profiles'] if p['id']=='AB')['overlays']=['B','A']
        path.write_text(json.dumps(d));self.plan['candidate']['manifest']['sha256']=sha256(path.read_bytes()).hexdigest()
        self.assertEqual(self.execute()['status'],'INCOMPATIBLE_CONFIGURATION')

    def test_caller_supplied_score_is_not_a_supported_input(self):
        self.plan['observed_score']=10000
        self.assertEqual(self.execute()['status'],'VALIDATION_FAILED')
