from copy import deepcopy
import unittest

from nss_base.neural_contracts import fingerprint, encoded
from nss_base.qualification_contracts import (FORMAT,POLICY_HASH, authorize,binding,claim,decision,
    identifier,manifest,request,revocation,timestamp,verification)
from nss_base.qualificationevidence002 import OPERATORS,AT
from nss_base.runtime import ContractError
from nss_base.serialization import decode


def dummy_request():
    h='a'*64
    b={'run_id':'run','plan_sha256':h,'report_sha256':h,'trial_seed':101,'precision':'fp32',
       'checkpoint_hashes':{k:h for k in ('core','A','B','joint','A2')},
       'core_generation':'neural-probe-G1','tokenizer':'one_hot_16_pair_v1',
       'context_abi':'symbol-state-v1','overlay_abi':'two-linear-slots-v1',
       'profile_ecids':{k:h for k in ('CORE','A','B','AB')},'runtime_sha256':h,'code_sha256':h,
       'environment_sha256':h,'data_binding_sha256':h,'test_pairs_sha256':h,
       'transition_pairs_sha256':h,'protocol_sha256':h,'checker':'symbol_pair_accuracy_and_recovery_v1'}
    return {'schema_version':1,'request_id':'req','producer_id':'builder','at':AT,
        'claim':{'kind':'PROFILE','profile':'CORE'},'binding':b,'prerequisites':[],
        'policy_sha256':POLICY_HASH,'purpose':'LOCAL_DEVELOPMENT_QUALIFICATION'}


class PureQualificationContracts(unittest.TestCase):
    def bad(self, fn, value):
        with self.assertRaises(ContractError):fn(value)
    def test_valid_request_roundtrip(self):
        r=dummy_request();self.assertEqual(request(decode(encoded(r).decode())),r)
    def test_extra_request_field(self):
        r=dummy_request();r['deployment_authorized']=True;self.bad(request,r)
    def test_missing_request_field(self):
        r=dummy_request();del r['binding'];self.bad(request,r)
    def test_boolean_version(self):
        r=dummy_request();r['schema_version']=True;self.bad(request,r)
    def test_malformed_identifiers(self):
        for value in (None,[],{},True,'','../escape','x'*97):
            with self.subTest(value=value):self.bad(identifier,value)
    def test_bad_timestamp(self):
        for value in ('today','2026-02-30T01:00:00Z','2026-01-01',AT[:-1]+'+00:00'):
            with self.subTest(value=value):self.bad(timestamp,value)
    def test_unknown_policy(self):
        r=dummy_request();r['policy_sha256']='0'*64;self.bad(request,r)
    def test_deployment_purpose(self):
        r=dummy_request();r['purpose']='PRODUCTION';self.bad(request,r)
    def test_unknown_profile(self):
        self.bad(claim,{'kind':'PROFILE','profile':'A2'})
    def test_profile_union_is_not_a_claim(self):
        self.bad(claim,{'kind':'PROFILE','profile':['A','B']})
    def test_reverse_transition_is_not_qualified(self):
        self.bad(claim,{'kind':'TRANSITION','source':'A','destination':'AB','mode':'replay'})
    def test_reuse_mode_not_supported(self):
        self.bad(claim,{'kind':'TRANSITION','source':'AB','destination':'A','mode':'reuse'})
    def test_generic_model_claim_rejected(self):
        self.bad(claim,{'kind':'GENERAL_INTELLIGENCE','passed':True})
    def test_missing_core_prerequisite(self):
        r=dummy_request();r['claim']['profile']='A';self.bad(request,r)
    def test_duplicate_prerequisites(self):
        r=dummy_request();r['claim']={'kind':'TRANSITION','source':'AB','destination':'A','mode':'replay'}
        r['prerequisites']=['x','x','y'];self.bad(request,r)
    def test_self_dependency(self):
        r=dummy_request();r['claim']['profile']='A';r['prerequisites']=['req'];self.bad(request,r)
    def test_unknown_precision(self):
        r=dummy_request()['binding'];r['precision']='bf16';self.bad(binding,r)
    def test_missing_checkpoint(self):
        b=dummy_request()['binding'];del b['checkpoint_hashes']['core'];self.bad(binding,b)
    def test_missing_core_ecid(self):
        b=dummy_request()['binding'];del b['profile_ecids']['CORE'];self.bad(binding,b)
    def test_digest_malformed(self):
        b=dummy_request()['binding'];b['report_sha256']='invalid';self.bad(binding,b)
    def test_boolean_seed(self):
        b=dummy_request()['binding'];b['trial_seed']=True;self.bad(binding,b)
    def test_extra_binding_key(self):
        b=dummy_request()['binding'];b['custom_checker']='arbitrary';self.bad(binding,b)
    def test_core_generation_not_silently_upgraded(self):
        b=dummy_request()['binding'];b['core_generation']='G2';self.bad(binding,b)
    def test_duplicate_json_key(self):
        self.bad(decode,'{"schema_version":1,"schema_version":1}')
    def test_nonfinite_json(self):
        self.bad(decode,'{"x":NaN}')
    def test_oversized_request(self):
        r=dummy_request();r['request_id']='x'*(2*1024*1024+1);self.bad(request,r)
    def test_manifest_duplicate_operators(self):
        self.bad(manifest,{'schema_version':1,'format':FORMAT,'policy_sha256':POLICY_HASH,
                           'operators':[OPERATORS[0],OPERATORS[0]]})
    def test_manifest_unknown_role(self):
        ops=deepcopy(OPERATORS);ops[0]['roles']=['ADMIN'];self.bad(manifest,
            {'schema_version':1,'format':FORMAT,'policy_sha256':POLICY_HASH,'operators':ops})
    def test_manifest_requires_reviewer(self):
        self.bad(manifest,{'schema_version':1,'format':FORMAT,'policy_sha256':POLICY_HASH,
            'operators':[{'id':'one','roles':['PRODUCER']},{'id':'two','roles':['PRODUCER']}]})
    def test_role_separation_even_when_both_declared(self):
        m=manifest({'schema_version':1,'format':FORMAT,'policy_sha256':POLICY_HASH,'operators':OPERATORS})
        with self.assertRaises(ContractError):authorize(m,'fixture-both','REVIEWER','fixture-both')
    def test_runtime_policy_mutation_detected(self):
        from unittest.mock import patch
        from nss_base.qualification_contracts import POLICY
        with patch.dict(POLICY,minimum_accuracy=0.0):
            self.bad(request,dummy_request())
