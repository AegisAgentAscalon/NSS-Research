#!/usr/bin/env python3
"""Export structural JSON Schemas; pure Python contracts enforce semantic links."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.qualification_contracts import FORMAT, POLICY, POLICY_HASH, AUTHORITY, CANDIDATE_FORMAT

def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
def st(limit=2000):return {'type':'string','minLength':1,'maxLength':limit}
def const(v):return {'const':v}
def arr(s,n=32):return {'type':'array','items':s,'minItems':0,'maxItems':n,'uniqueItems':True}
def ref(n):return {'$ref':'qualification_'+n+'.schema.json'}
ID={**st(96),'pattern':'^[A-Za-z0-9_.:-]+$'};SHA={'type':'string','pattern':'^[0-9a-f]{64}$'}
AT={'type':'string','pattern':r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$'}
V={'type':'integer','const':1}
profile=obj({'kind':const('PROFILE'),'profile':{'enum':['CORE','A','B','AB','A2','A2B']}})
transitions=[obj({'kind':const('TRANSITION'),'source':const(a),'destination':const(b),'mode':const('replay')}) for a,b in [('AB','A'),('A','CORE'),('A2B','A2'),('A2','CORE')]]
claim={'oneOf':[profile,*transitions]}
b=obj({'run_id':ID,'plan_sha256':SHA,'report_sha256':SHA,'trial_seed':{'type':'integer','minimum':0,'maximum':2**31-1},
 'precision':{'enum':['fp32','ternary_core_reference']},'checkpoint_hashes':obj({k:SHA for k in ('core','A','B','joint','A2')}),
 'core_generation':const('neural-probe-G1'),'tokenizer':const('one_hot_16_pair_v1'),'context_abi':const('symbol-state-v1'),
 'overlay_abi':const('two-linear-slots-v1'),'profile_ecids':obj({k:SHA for k in ('CORE','A','B','AB')}),
 **{k:SHA for k in ('runtime_sha256','code_sha256','environment_sha256','data_binding_sha256','test_pairs_sha256','transition_pairs_sha256','protocol_sha256')},
 'checker':const('symbol_pair_accuracy_and_recovery_v1')})
# Distinct binding shapes retain the original probe schema unchanged.
receipt=obj({'id':ID,'plan_sha256':SHA,'report_sha256':SHA,'verdict':{'enum':['PASS','FAIL','INCONCLUSIVE']},'authority':const('NONE')})
lineage=obj({'cycle_sha256':SHA,'proposal_sha256':SHA,'producer_id':ID,'training_receipt':receipt,'evaluation_receipt':receipt,
 'snapshot':obj({'snapshot_id':ID,'sha256':SHA,'member_count':{'type':'integer','const':2}}),
 'parent_binding_sha256':SHA,'parent_core_certificate':obj({'request_id':ID,'certificate_sha256':SHA}),
 'criteria_sha256':SHA,'retention_pairs_sha256':SHA})
cb=obj({**b['properties'],'source_format':const(CANDIDATE_FORMAT),'candidate_lineage':lineage,
 'checkpoint_hashes':obj({k:SHA for k in ('core','A','B','A2')}),
 'profile_ecids':obj({k:SHA for k in ('CORE','A2','A2B')}),'checker':const('candidate_A2_profile_and_recovery_v1')})
b={'oneOf':[b,cb]}
r=obj({'schema_version':V,'request_id':ID,'producer_id':ID,'at':AT,'claim':ref('claim'),'binding':ref('binding'),
 'prerequisites':arr(ID,3),'policy_sha256':const(POLICY_HASH),'purpose':const('LOCAL_DEVELOPMENT_QUALIFICATION')})
d=obj({'schema_version':V,'operation_id':ID,'request_id':ID,'request_sha256':SHA,'reviewer_id':ID,'at':AT,
 'recommendation':{'enum':['ACCEPT','REJECT','INCONCLUSIVE']},'reason':st()})
rv=obj({'schema_version':V,'operation_id':ID,'request_id':ID,'certificate_sha256':SHA,'reviewer_id':ID,'at':AT,'reason':st()})
m=obj({'schema_version':V,'format':const(FORMAT),'operators':{**arr(obj({'id':ID,'roles':{**arr({'enum':['PRODUCER','REVIEWER']},2),'minItems':1}})), 'minItems':2},'policy_sha256':const(POLICY_HASH)})
c=obj({'schema_version':V,'evidence_id':ID,'request_sha256':SHA,'claim':ref('claim'),'binding':ref('binding'),
 'policy_sha256':const(POLICY_HASH),'verification_sha256':SHA,'producer_id':ID,'reviewer_id':ID,'issued_at':AT,
 'prerequisites':arr(obj({'id':ID,'sha256':SHA}),3),'scope':const(POLICY['scope']),'authority':const(AUTHORITY),
 'deployment_authorized':const(False)})
for name,value in {'claim':claim,'binding':b,'request':r,'decision':d,'revocation':rv,'manifest':m,'certificate':c}.items():
 (ROOT/'schemas'/('qualification_'+name+'.schema.json')).write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**value},indent=2)+'\n')
(ROOT/'fixtures/qualificationevidence002/policy.json').write_text(json.dumps(POLICY,indent=2)+'\n')
print('Generated seven structural qualification schemas and the exact frozen policy.')
