#!/usr/bin/env python3
"""Deterministic structural schemas; semantic/authority checks remain in the owners."""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.generation_contracts import FORMAT, OPERATION, POLICY, POLICY_HASH, ROLES


def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
def const(v):return {'const':v}
def array(v,low,high):return {'type':'array','items':v,'minItems':low,'maxItems':high,'uniqueItems':True}
ID={'type':'string','pattern':'^[A-Za-z0-9_.:-]{1,96}$'}
SHA={'type':'string','pattern':'^[0-9a-f]{64}$'}
V={'type':'integer','const':1};TIME={'type':'integer','minimum':0,'maximum':253402300799}
REF=obj({'id':ID,'sha256':SHA})
POINTER=obj({'epoch':{'type':'integer','minimum':0,'maximum':1000000},'generation_sha256':{'oneOf':[SHA,{'type':'null'}]}})
manifest=obj({'schema_version':V,'generation_id':ID,'producer_id':ID,'binding':{'$ref':'qualification_binding.schema.json'},
 'members':array(obj({'id':{'enum':['A','B','A2']},'sha256':SHA,'requires':array({'enum':['A','B','A2']},0,1)}),0,2),
 'profiles':array(obj({'id':{'enum':['CORE','A','B','AB','A2','A2B']},'members':array({'enum':['A','B','A2']},0,2),'ecid':SHA,'evidence':REF}),1,4),
 'transitions':array(obj({'source':{'enum':['AB','A','A2B','A2']},'destination':{'enum':['A','CORE','A2']},'mode':const('replay'),'state_policy':const('DISCARD_AND_REPLAY'),'evidence':REF}),0,2),
 'purpose':{'enum':['BOUNDED_NEURAL_PROBE_GENERATION','BOUNDED_CANDIDATE_OVERLAY_GENERATION']}})
request=obj({'schema_version':V,'release_id':ID,'operation':const(OPERATION),'caller_id':ID,'target_sha256':SHA,
 'generation_certificate_sha256':SHA,'expected_current':POINTER,'reason':{'type':'string','minLength':1,'maxLength':2000},'mode':{'enum':['BOOTSTRAP','UPDATE','ROLLBACK']}})
grant=obj({'schema_version':V,'store_id':ID,'request_sha256':SHA,'issuer_id':ID,'issued_at':TIME,'expires_at':TIME,
 'max_uses':{'type':'integer','const':1},'policy_sha256':const(POLICY_HASH),'authority':const(POLICY['scope']),
 'catalog_publication_authorized':const(True),'runtime_execution_permit':const(False),'production_deployment_authorized':const(False)})
store=obj({'schema_version':V,'format':const(FORMAT),'store_id':ID,'policy_sha256':const(POLICY_HASH),
 'operators':array(obj({'id':ID,'roles':array({'enum':list(ROLES)},1,4)}),3,32)})
ticket=obj({'schema_version':V,'store_id':ID,'ticket_id':ID,'caller_id':ID,'configuration':POINTER,
 'profile':{'enum':['CORE','A','B','AB','A2','A2B']},'profile_ecid':SHA,'state_reuse':const('EXACT_TICKET_ONLY')})
for name,s in [('manifest',manifest),('release_request',request),('release_grant',grant),('store',store),('ticket',ticket)]:
 (ROOT/f'schemas/generation_{name}.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**s},indent=2)+'\n')
p=ROOT/'fixtures/overlaygenerationmanager001';p.mkdir(parents=True,exist_ok=True)
(p/'policy.json').write_text(json.dumps(POLICY,indent=2)+'\n')
print('Generated five structural generation schemas. Owner validation adds exact evidence, closure, role, timing and current-state checks.')

# Catalogue/task schemas share the existing generation schema generator and owner.
# These are structural JSON Schema exports; owner code enforces current eligibility,
# exact descriptor membership, source/receipt lineage and directed transitions.
from nss_base.catalog_contracts import FORMAT as CATALOG_FORMAT, POLICY as CATALOG_POLICY
UINT={'type':'integer','minimum':0,'maximum':10**9}
CAPS=array(ID,1,32)
BUDGET=obj({'max_document_bytes':UINT,'max_cost_units':UINT})
STAGE={'$ref':'task_stage.schema.json'}
PAIR=array({'type':'integer','minimum':0,'maximum':15},2,2);PAIR.pop('uniqueItems')
PAIRS=array(PAIR,1,256)
catalog=obj({'schema_version':V,'format':const(CATALOG_FORMAT),'catalog_id':ID,'generation_sha256':SHA,
 'author_id':ID,'policy':const(CATALOG_POLICY),'claim_scope':const('REVIEWED_ROUTING_FIXTURE_NOT_NEW_NEURAL_EVIDENCE'),
 'profiles':array(obj({'id':{'enum':['CORE','A','B','AB','A2','A2B']},'ecid':SHA,'capabilities':CAPS,
 'sealed_document_bytes':{'type':'integer','minimum':1,'maximum':10**9},'load_units':UINT,
 'step_units':{'type':'integer','minimum':1,'maximum':10**9},'max_pairs':{'type':'integer','minimum':1,'maximum':256}}),1,4)})
selection=obj({'schema_version':V,'catalog_sha256':SHA,'expected_current':POINTER,'task_id':ID,
 'stage':STAGE,'capabilities':CAPS,'pairs':PAIRS,'budget':BUDGET})
common={'schema_version':V,'operation_id':ID,'caller_id':ID}
source={'source_ticket':{'$ref':'generation_ticket.schema.json'},'expected_record_sha256':SHA}
record_schema=json.loads((ROOT/'schemas/task_record.schema.json').read_text())['properties']
command={'oneOf':[
 obj({**common,'action':const('START'),'request':selection,'ticket_id':ID,'record':{'$ref':'task_record.schema.json'}}),
 obj({**common,'action':const('MOVE'),**source,'request':selection,'ticket_id':ID}),
 obj({**common,'action':const('FINISH'),**source,'results':record_schema['checked_results'],'receipts':record_schema['receipts']}),
 obj({**common,'action':const('CLOSE'),**source}),
 obj({**common,'action':const('CANCEL'),**source,'receipts':record_schema['receipts'],'reason':{'type':'string','minLength':1,'maxLength':2000}})]}
for name,value in [('descriptor',catalog),('selection_request',selection),('command',command)]:
 (ROOT/f'schemas/catalog_{name}.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**value},indent=2)+'\n')
print('Generated three structural catalogue/task schemas; no new schema-rendering script.')

# Context packets reuse existing TaskRecord, ticket and experience schemas. Byte
# budgets are software serialization limits, not tokenizer/attention guarantees.
from nss_base.context_contracts import FORMAT as CTX_FORMAT, POLICY as CTX_POLICY, UNIT, TASK_SPINE, OMISSIONS
C_ID={'type':'string','pattern':'[A-Za-z0-9_.:-]{1,128}','minLength':1,'maxLength':128}
C_SHA={'type':'string','pattern':'[0-9a-f]{64}'}
C_V={'type':'integer','enum':[1]}
def ce(v):return {'type':{str:'string',bool:'boolean',int:'integer'}[type(v)],'enum':[v]}
def ca(v,high=128):return {'type':'array','items':v,'minItems':0,'maxItems':high,'uniqueItems':True}
record=json.loads((ROOT/'schemas/task_record.schema.json').read_text())['properties']
rev=json.loads((ROOT/'schemas/experience_revision.schema.json').read_text())['properties']
ref=json.loads((ROOT/'schemas/experience_use_batch.schema.json').read_text())['properties']['references']['items']
archive=obj({'format':ce('MegaMindAlpha.ExperienceArchive001'),'schema_version':C_V,
 'locator':{'type':'string','minLength':1,'maxLength':4096},'sha256':C_SHA});archive['type']=['object','null']
field=json.loads((ROOT/'schemas/handoff_evidence.schema.json').read_text())['properties']['fields']['items']
selector=obj({'source_id':C_ID,'field_id':C_ID})
uint={'type':'integer','minimum':0,'maximum':1048576}
slice_selector=obj({'experience_id':C_ID,'source_id':C_ID,'source_sha256':C_SHA,'start_byte':uint,'end_byte':uint})
ctxreq=obj({'schema_version':C_V,'format':ce(CTX_FORMAT),'policy':ce(CTX_POLICY),'caller_id':ID,
 'ticket':{'$ref':'generation_ticket.schema.json'},'expected_record_sha256':C_SHA,'expected_task_state_identity':C_SHA,
 'archive_binding':archive,'budget':obj({'unit':ce(UNIT),
 'max_context_bytes':{'type':'integer','minimum':1,'maximum':131072},
 'max_evidence_bytes':{'type':'integer','minimum':0,'maximum':2097152}}),
 'required_fact_ids':ca(C_ID),'optional_fact_ids':ca(C_ID),'assumption_ids':ca(C_ID),'result_ids':ca(C_ID),
 'source_fields':ca(selector),'query_terms':ca({'type':'string','minLength':1,'maxLength':64},16),
 'experiences':ca(obj({'reference':ref,'required':{'type':'boolean'},
 'priority':{'type':'integer','minimum':0,'maximum':100}}),32),'evidence_slices':ca(slice_selector,32)})
# Use old schema validator-compatible type+enum syntax rather than const/oneOf.
ticket=json.loads((ROOT/'schemas/generation_ticket.schema.json').read_text())
def compat(s):
 if isinstance(s,dict):
  if 'oneOf' in s:
   arms=s.pop('oneOf'); s['type']=[v['type'] for v in arms]
   for v in arms:
    if v['type']!='null': s.update({k:val for k,val in v.items() if k!='type'})
  if 'const' in s:
   v=s.pop('const');s['enum']=[v]
   if 'type' not in s:s['type']={str:'string',bool:'boolean',int:'integer'}[type(v)]
  if 'enum' in s and 'type' not in s:
   s['type']={str:'string',bool:'boolean',int:'integer'}[type(s['enum'][0])]
  for v in s.values():compat(v)
 elif isinstance(s,list):
  for v in s:compat(v)
compat(ticket);ctxreq['properties']['ticket']=ticket
fact=obj({**record['facts']['items']['properties'],'rehydrated_fields':ca({'type':'string','enum':['value','unit']},2)})
permission=rev['permissions']['properties']['retrieval']
experience=obj({'reference':ref,'authority':ce('REVIEWED_INTERPRETATION_NOT_INSTRUCTION'),
 'statement':rev['statement'],'sources':rev['sources'],'review':rev['review'],
 'permission':permission,'sensitivity':{'type':'string','enum':['ORDINARY','IDENTITY_SENSITIVE','PRIVATE']}})
payload=obj({'configuration':obj({'profile':{'type':'string','enum':['CORE','A','B','AB','A2','A2B']},'profile_ecid':C_SHA,
 'epoch':{'type':'integer','minimum':1,'maximum':1000000},'generation_sha256':C_SHA}),
 'task':obj({k:record[k] for k in TASK_SPINE}), 'facts':ca(fact),
 'assumptions':record['assumptions'],'checked_results':record['checked_results'],
 'source_fields':ca(obj({'source_id':C_ID,'field':field})),
 'sources':record['sources'],'experiences':ca(experience,32),
 'evidence_slices':ca(obj({**slice_selector['properties'],'text':{'type':'string','minLength':1,'maxLength':1048576},
 'slice_sha256':C_SHA,'authority':ce('SOURCE_DATA_NOT_INSTRUCTION')}),32)})
ctxpacket=obj({'schema_version':C_V,'format':ce(CTX_FORMAT),'policy':ce(CTX_POLICY),
 'request':ctxreq,'request_sha256':C_SHA,'binding':obj({'task_state_identity':C_SHA,
 'record_sha256':C_SHA,'profile_ecid':C_SHA}), 'payload':payload,'payload_sha256':C_SHA,
 'omissions':ca(obj({'kind':{'type':'string','enum':['fact','assumption','result','experience','source']},
 'id':C_ID,'reason':{'type':'string','enum':list(OMISSIONS)}}),1024),
 'usage':obj({'unit':ce(UNIT),'context_bytes':{'type':'integer','minimum':0,'maximum':131072},
 'evidence_bytes':{'type':'integer','minimum':0,'maximum':2097152}}),
 'scope':ce('POINT_IN_TIME_TRUSTED_LOCAL_READ_NOT_EXECUTION_OR_TRAINING_AUTHORITY'),
 'runtime_execution_permit':ce(False),'training_authorized':ce(False),'learned_retrieval':ce(False)})
for name,s in [('request',ctxreq),('packet',ctxpacket)]:
 (ROOT/f'schemas/context_{name}.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**s},indent=2)+'\n')
print('Generated two context schemas using existing versioned source/task types.')

# PersistentState001 extends TaskRecord rather than introducing another store.
# Legacy schemas remain exact; owner validators choose the explicitly versioned form.
from copy import deepcopy
from nss_base.state_contracts import POLICY as STATE_POLICY
SCOPE=obj({k:ID for k in ('agent_id','project_id','session_id')})
AUTHOR=obj({'id':ID,'version':ID})
STATE_POLICY_SCHEMA=obj({'policy_id':ce(STATE_POLICY),'instruction_policy_sha256':C_SHA,
 'max_record_bytes':{'type':'integer','minimum':1024,'maximum':131072}})
SREF=obj({'kind':{'type':'string','enum':['TASK','EXPERIENCE']},'source_id':C_ID,'field_id':C_ID,'reference':ref})
SREF['required']=['kind']  # Discriminated cardinality is additionally checked by source_ref().
SREFS=ca(SREF,16)
BIND_ARCHIVE=deepcopy(archive)
REVIEW=obj({'kind':ce('HUMAN_LOCAL_ATTESTATION'),'reviewer_id':ID,'proposal_sha256':C_SHA,
 'reviewed_at':TIME,'expires_at':TIME,'decision':ce('APPROVE'),
 'reason':{'type':'string','minLength':1,'maxLength':2000}}); REVIEW['type']=['object','null']
NOTE=obj({'id':ID,'text':{'type':'string','minLength':1,'maxLength':4096},
 'kind':{'type':'string','enum':['CLAIM','PROGRESS']},
 'status':{'type':'string','enum':['UNKNOWN','HYPOTHESIS','USER_STATED','TEST_VERIFIED']},
 'confidence':{'type':'null'},'mandatory':{'type':'boolean'},'identity_sensitive':{'type':'boolean'},
 'expires_at':{'type':['integer','null'],'minimum':0,'maximum':253402300799}})
META={'author':AUTHOR,'reviewer_id':ID,'event_id':ID,'source_refs':SREFS}
ANN=obj({'id':{'type':'string','pattern':'[A-Za-z0-9_.:-]+','minLength':1,'maxLength':140},'change':{'type':'string','enum':['SET_GOAL','ADD_QUESTION','RESOLVE_QUESTION','DEFER_QUESTION']},
 'reason':{'type':'string','minLength':1,'maxLength':2000},**META})
STATE=obj({'schema_version':C_V,'scope':SCOPE,'policy':STATE_POLICY_SCHEMA,'archive_binding':BIND_ARCHIVE,
 'last_event_id':ID,'authority':ce('REVIEWED_WORKING_DATA_NOT_INSTRUCTION'),'notes':ca(obj({**NOTE['properties'],**META}),128),'annotations':ca(ANN,128)})
V2={'type':'integer','enum':[2]}
rec2=deepcopy(json.loads((ROOT/'schemas/task_record.schema.json').read_text()))
rec2['properties']['schema_version']=V2; rec2['properties']['persistent_state']=STATE
rec2['required'].append('persistent_state')
BASE_STATE={'schema_version':V2,'operation_id':ID,'caller_id':ID,'source_ticket':deepcopy(ticket),
 'scope':SCOPE,'expected_record_sha256':C_SHA,'expected_revision':{'type':'integer','minimum':0,'maximum':1000000},
 'expected_ecid':C_SHA,'proposer':AUTHOR,'review':REVIEW}
bind=obj({**BASE_STATE,'action':ce('BIND_STATE'),'policy':STATE_POLICY_SCHEMA,'archive_binding':BIND_ARCHIVE})
delta=obj({'op':{'type':'string','enum':['SET_GOAL','ADD_QUESTION','RESOLVE_QUESTION','DEFER_QUESTION','ADD_NOTE','RETIRE_NOTE','EXPIRE_NOTE']},
 'source_refs':SREFS,'id':C_ID,'text':{'type':'string','minLength':1,'maxLength':4096},'blocking':{'type':'boolean'},
 'answer':{'type':'string','minLength':1,'maxLength':4096},'reason':{'type':'string','minLength':1,'maxLength':2000},'note':NOTE})
delta['required']=['op','source_refs']
update=obj({**BASE_STATE,'action':ce('UPDATE_STATE'),'deltas':{'type':'array','items':delta,'minItems':1,'maxItems':256}})
for filename, schema in [('state_scope',SCOPE),('state_source',SREF),('task_record_v2',rec2),('state_bind',bind),('state_update',update)]:
 (ROOT/f'schemas/{filename}.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**schema},indent=2)+'\n')
# Export v2 catalogue commands for existing lifecycle operations as well; v1 START
# stays unchanged. A fresh legacy record is explicitly admitted via BIND_STATE.
scoped=[]
for arm in command['oneOf'][1:]:
 arm=deepcopy(arm);arm['properties']['schema_version']=V2;arm['properties']['scope']=SCOPE;arm['required'].append('scope');scoped.append(arm)
command2={'oneOf':scoped+[bind,update]}
(ROOT/'schemas/catalog_command_v2.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**command2},indent=2)+'\n')
ctxreq2=deepcopy(ctxreq);ctxreq2['properties']['schema_version']=V2
ctxreq2['properties']['state_scope']=SCOPE;ctxreq2['required'].append('state_scope')
ctxpacket2=deepcopy(ctxpacket);ctxpacket2['properties']['schema_version']=V2
ctxpacket2['properties']['request']=ctxreq2
ctxpacket2['properties']['payload']['properties']['task']['properties']['persistent_state']=STATE
ctxpacket2['properties']['payload']['properties']['task']['required'].append('persistent_state')
for name,value in [('request_v2',ctxreq2),('packet_v2',ctxpacket2)]:
 (ROOT/f'schemas/context_{name}.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**value},indent=2)+'\n')
print('Generated scoped state, reviewed-delta, legacy-compatible task and context v2 schemas.')
