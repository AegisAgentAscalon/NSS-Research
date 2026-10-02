from copy import deepcopy
import unittest
from learner_helpers import LearnerCase, CLOCK
from nss_base.boundedlearnercoordinator001 import OPERATORS
from nss_base.learner_contracts import learning_plan, manifest, numerical_input, metrics
from nss_base.neural_contracts import fingerprint
from nss_base.runtime import ContractError


class LearningContractTests(LearnerCase):
    def test_bad_plan_shapes_are_typed(self):
        for x in [None,[],False,{},'plan',dict(self.plan,extra=1)]:
            with self.subTest(value=type(x).__name__):self.error('VALIDATION_FAILED',learning_plan,x)

    def test_pinned_fields_cannot_drift(self):
        cases=[('code_sha256','0'*64),('environment_sha256','0'*64),('authority','DEPLOY'),('format','other'),('schema_version',True)]
        for key,value in cases:
            with self.subTest(field=key):self.error('INCOMPATIBLE_CONFIGURATION',learning_plan,dict(self.plan,**{key:value}))

    def test_recipe_is_not_a_supplied_program(self):
        for value in [{'id':'exec-python','seed':1,'steps':2,'learning_rate':.03},
            dict(self.plan['recipe'],callback='os.system')]:
            with self.subTest(value=value):
                with self.assertRaises(ContractError):learning_plan(dict(self.plan,recipe=value))

    def test_bad_training_numbers_fail(self):
        for key,vals in [('seed',[True,-1,2**31,'1']),('steps',[True,0,1001,'2']),('learning_rate',[True,0,float('nan'),float('inf'),.9])]:
            for value in vals:
                with self.subTest(field=key,value=value):
                    with self.assertRaises(ContractError):learning_plan(dict(self.plan,recipe=dict(self.plan['recipe'],**{key:value})))

    def test_budgets_bounded_and_single_attempt(self):
        for key,value in [('optimizer_updates',-1),('optimizer_updates',1001),('evaluation_passes',3),('training_attempts',2),('training_attempts',True)]:
            with self.subTest(field=key):self.error('VALIDATION_FAILED',learning_plan,dict(self.plan,budget=dict(self.plan['budget'],**{key:value})))

    def test_criteria_cannot_be_lowered(self):
        x=deepcopy(self.plan);x['criteria']['minimum_accuracy']=.1
        self.error('INCOMPATIBLE_CONFIGURATION',learning_plan,x)

    def test_origin_refs_are_typed_not_a_permit(self):
        x=deepcopy(self.plan);x['origin']={'task_id':'t','record_sha256':'0'*64,'context_packet_sha256':'1'*64}
        self.assertEqual(learning_plan(x)['authority'],'NONE')
        x['origin']['runtime_execution_permit']=True
        self.error('VALIDATION_FAILED',learning_plan,x)

    def test_data_split_and_codec_are_not_arbitrary(self):
        x=deepcopy(self.plan);x['snapshot_request']['members'][1]['split']='train'
        self.error('VALIDATION_FAILED',learning_plan,x)
        x=deepcopy(self.plan);x['snapshot_request']['tokenizer']['id']='different'
        self.error('INCOMPATIBLE_CONFIGURATION',learning_plan,x)

    def test_archive_and_certificate_ids_are_validated(self):
        for key,val in [('archive_sha256',[]),('parent_core_certificate',{})]:
            with self.subTest(field=key):self.error('VALIDATION_FAILED',learning_plan,dict(self.plan,**{key:val}))

    def test_operator_overlap_is_rejected(self):
        x=deepcopy(OPERATORS);x['approver_ids']=['learner-worker']
        self.error('AUTHORIZATION_DENIED',manifest,x)

    def test_operator_manifest_malformed_values(self):
        for v in [None,{},[],True]:
            with self.subTest(value=v):self.error('VALIDATION_FAILED',manifest,v)
        for vals in [['b','a'],[],['a','a'],[[]]]:
            with self.subTest(vals=vals):
                with self.assertRaises(ContractError):manifest(dict(OPERATORS,producer_ids=vals))

    def test_exact_cycle_id_cannot_rebind(self):
        self.co.prepare(self.plan);x=deepcopy(self.plan);x['recipe']['seed']+=1
        self.error('CONSTRAINT_CONFLICT',self.co.prepare,x)

    def test_bound_numerical_plan_rejects_other_snapshot(self):
        self.error('CONSTRAINT_CONFLICT',numerical_input,self.plan,{'snapshot_id':'other','sha256':'a'*64,'member_count':2})

    def test_bad_fault_hooks_are_rejected_before_work(self):
        for hook in ['wrong',[],False]:
            with self.subTest(hook=hook):self.error('VALIDATION_FAILED',self.co.prepare,self.plan,crash_at=hook)
        self.assertEqual(self.co.cycles.inspect()['cycles'],[])

    def test_invalid_clock_is_typed(self):
        for v in [True,-1,float('nan'),'today']:
            self.co.clock=lambda:v
            with self.subTest(value=v):self.error('VALIDATION_FAILED',self.co.prepare,self.plan)
