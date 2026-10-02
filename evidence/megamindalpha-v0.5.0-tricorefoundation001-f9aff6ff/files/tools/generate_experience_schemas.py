#!/usr/bin/env python3
"""Regenerate the shipped v1 archive schemas; no network or third-party library.
Semantic rules (lineage, timestamps, exact evidence, permissions) remain in
experience_contracts.py and are tested separately.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
S=ROOT/'schemas'
def obj(props,required=None): return {'type':'object','properties':props,'required':list(props) if required is None else required,'additionalProperties':False}
def string(n=4096,minimum=1,pattern=None):
 d={'type':'string','minLength':minimum,'maxLength':n}
 if pattern:d['pattern']=pattern
 return d
def enum(*v): return {'type':'string','enum':list(v)}
def arr(s,n=32,m=0):return {'type':'array','items':s,'minItems':m,'maxItems':n}
def nullable(s):return {**s,'type':[s['type'],'null']}
def ref(n):return {'$ref':n+'.schema.json'}
ID=string(128,pattern='[A-Za-z0-9_.:-]+');SHA=string(64,64,'[0-9a-f]{64}'); TIME=string(20,20,r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
ACTOR=obj({'id':ID,'kind':enum('HUMAN','MODEL','SYSTEM','UNKNOWN'),'version':string(128)})
EXEC=obj({'task_id':ID,'stage_id':ID,'checkpoint_sha256':SHA,'ecid':SHA,'profile':ID,'core_generation':ID,'core_sha256':SHA,'task_record_sha256':SHA,'capture_request_sha256':nullable(SHA)})
OBS=obj({'kind':enum('TASK_STAGE','EXTERNAL_RECORD'),'execution':nullable(EXEC),'summary':string(4096),'outcome':enum('UNKNOWN','SUCCEEDED','FAILED','PARTIAL'),'check_refs':arr(string(256),64)})
SOURCEMETA={'id':ID,'kind':enum('USER_REPORT','TOOL_RESULT','MODEL_OUTPUT','SYNTHETIC','REFERENCE','TASK_SNAPSHOT','POLICY'),'author':ACTOR,'recorded_at':TIME,'media_type':enum('text/plain','application/json'),'sha256':SHA,'generator':nullable(ACTOR),'parent_source_ids':arr(ID,32),'rights_note':string(2048)}
EVID=obj({**SOURCEMETA,'content':string(262144,0)})
STATEMENT=obj({'text':string(8192),'uncertainty':enum('LOW','MEDIUM','HIGH','UNKNOWN'),'support_ids':arr(ID,32,1)})
CAP=obj({'schema_version':{'type':'integer','enum':[1]},'operation_id':ID,'experience_id':ID,'actor':ACTOR,'at':TIME,'observation':OBS,'family_id':ID,'sensitivity':enum('ORDINARY','PRIVATE','IDENTITY_SENSITIVE'),'evidence':arr(EVID,32,1),'statement':STATEMENT})
MUT=obj({'schema_version':{'type':'integer','enum':[1]},'operation_id':ID,'experience_id':ID,'expected_revision_hash':SHA,'actor':ACTOR,'at':TIME,'reason':string(4096),'action':enum('ANNOTATE','CORRECT','REVIEW','DISPUTE','RESOLVE','PERMISSION','WITHDRAW'),'payload':{'type':'object','properties':{},'required':[],'additionalProperties':False}})
# payload is validated against its action schema separately; do not feed this
# container schema to the sibling validator with an unrestricted arbitrary value.
MUT['properties']['payload']={'type':'object','properties':{},'required':[],'additionalProperties':False}
# Export one concrete schema per action, avoiding unsupported oneOf in the local validator.
payloads={
 'ANNOTATE':obj({'statement':STATEMENT,'evidence':arr(EVID,32)}),
 'CORRECT':obj({'statement':STATEMENT,'evidence':arr(EVID,32)}),
 'REVIEW':obj({'decision':enum('APPROVED','REJECTED')}),
 'DISPUTE':obj({'conflict_id':ID,'support_ids':arr(ID,32,1),'evidence':arr(EVID,32)}),
 'RESOLVE':obj({'conflict_id':ID,'support_ids':arr(ID,32,1),'evidence':arr(EVID,32)}),
 'PERMISSION':obj({'purpose':enum('memory','retrieval','training','redistribution'),'decision':enum('ALLOWED','DENIED','REVOKED'),'permission_ref':string(2048)}),
 'WITHDRAW':obj({})}
REVOKE=obj({'schema_version':{'type':'integer','enum':[1]},'operation_id':ID,'actor':ACTOR,'at':TIME,'reason':string(4096),'permission_ref':string(2048),'source_sha256':SHA,'purpose':enum('memory','retrieval','training','redistribution')})
SOURCE=obj(SOURCEMETA)
revstatement=obj({**STATEMENT['properties'],'kind':enum('INTERPRETATION','CORRECTION'),'author':ACTOR,'recorded_at':TIME,'supersedes':nullable(SHA)})
review=obj({'status':enum('PENDING_REVIEW','APPROVED','REJECTED','QUARANTINED','WITHDRAWN'),'reviewer':nullable(ACTOR),'at':nullable(TIME),'reason':string(4096,0)})
permission=obj({'status':enum('UNKNOWN','ALLOWED','DENIED','REVOKED'),'actor':nullable(ACTOR),'at':nullable(TIME),'reason':string(4096,0),'permission_ref':nullable(string(2048))})
conflict=obj({'id':ID,'status':enum('OPEN','RESOLVED'),'raised_by':ACTOR,'raised_at':TIME,'reason':string(4096),'support_ids':arr(ID,32,1),'resolution':nullable(obj({'actor':ACTOR,'at':TIME,'reason':string(4096),'support_ids':arr(ID,32,1)}))})
REV=obj({'schema_version':{'type':'integer','enum':[1]},'experience_id':ID,'revision':{'type':'integer','minimum':0,'maximum':511},'parent_hash':nullable(SHA),'capture_hash':SHA,'updated_at':TIME,'sources':arr(SOURCE,64,1),'statement':revstatement,'review':review,'conflicts':arr(conflict,64),'permissions':obj({p:permission for p in ('memory','retrieval','training','redistribution')})})

STAGE_FIELDS={k:CAP['properties'][k] for k in ('schema_version','operation_id','experience_id','actor','at','family_id','sensitivity','statement')}
STAGE_FIELDS.update(task_id=ID,expected_checkpoint_hash=SHA)
for k in ('summary','outcome','check_refs'): STAGE_FIELDS[k]=OBS['properties'][k]
STAGE=obj(STAGE_FIELDS)
items={'experience_actor':ACTOR,'experience_capture':CAP,'experience_source':SOURCE,'experience_source_revocation':REVOKE,'experience_revision':REV,'experience_stage_capture':STAGE}

for name,payload in payloads.items():
 spec={**MUT,'properties':{**MUT['properties'],'action':enum(name),'payload':payload}}
 items['experience_'+name.lower()]=spec
for name,spec in items.items():
 (S/(name+'.schema.json')).write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**spec},indent=2)+'\n')
print('schemas',len(items))
