#!/usr/bin/env python3
"""Deterministic structural schemas; owner contracts enforce cross-field semantics."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.permission_contracts import FORMAT,POLICY,POLICY_HASH,AUTHORITY,OPERATION
from nss_base.neural_contracts import pairs

def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
def const(v):return {'const':v}
ID={'type':'string','pattern':'^[A-Za-z0-9_.:-]{1,96}$'}
SHA={'type':'string','pattern':'^[0-9a-f]{64}$'}
V={'type':'integer','const':1};EPOCH={'type':'integer','minimum':0,'maximum':253402300799}
claim={'oneOf':[obj({'kind':const('TRANSITION'),'source':const(a),'destination':const(b),'mode':const('replay')}) for a,b in [('AB','A'),('A','CORE')]]}
request=obj({'schema_version':V,'request_id':ID,'caller_id':ID,'task_id':ID,'operation':const(OPERATION),
 'policy_sha256':const(POLICY_HASH),'qualification_id':ID,'certificate_sha256':SHA,'claim':claim,
 'binding':{'$ref':'qualification_binding.schema.json'},'inputs':{'const':pairs('test')[:4], 'type':'array','items':{'type':'array','items':{'type':'integer'}}},
 'source_state_sha256':SHA,'action_receipts':{'type':'array','items':obj({'key':ID,'receipt':SHA}),'maxItems':32,'uniqueItems':True}})
grant=obj({'schema_version':V,'store_id':ID,'request_id':ID,'request_sha256':SHA,'caller_id':ID,'issuer_id':ID,
 'issued_at':EPOCH,'expires_at':EPOCH,'policy_sha256':const(POLICY_HASH),'max_uses':{'type':'integer','const':1},
 'authority':const(AUTHORITY),'deployment_authorized':const(False),'runtime_execution_permit':const(False),'delegable':const(False)})
manifest=obj({'schema_version':V,'format':const(FORMAT),'store_id':ID,'policy_sha256':const(POLICY_HASH),
 'operators':{'type':'array','minItems':2,'maxItems':32,'items':obj({'id':ID,'roles':{'type':'array','minItems':1,'maxItems':3,'uniqueItems':True,'items':{'enum':['ISSUER','EXECUTOR','RECONCILER']}}})}})
receipt=obj({'schema_version':V,'request_id':ID,'request_sha256':SHA,'grant_sha256':SHA,'executor_id':const('bounded_neural_replay_v1'),
 'result_sha256':SHA,'status':const('COMMITTED'),'deployment_authorized':const(False)})
for name,schema in [('request',request),('grant',grant),('manifest',manifest),('receipt',receipt)]:
 (ROOT/'schemas'/('permission_'+name+'.schema.json')).write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**schema},indent=2)+'\n')
p=ROOT/'fixtures/localnexuspermissions002';p.mkdir(parents=True,exist_ok=True)
(p/'policy.json').write_text(json.dumps(POLICY,indent=2)+'\n')
print('Generated four permission schemas; sorted keys, lifetimes, identity inequality, grant/current evidence and receipts also require owner semantic validation.')
