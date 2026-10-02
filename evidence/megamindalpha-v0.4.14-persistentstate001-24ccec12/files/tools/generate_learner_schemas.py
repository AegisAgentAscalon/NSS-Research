#!/usr/bin/env python3
"""Deterministic exchange schemas. Owner validators add policy and current-use checks.

These standard JSON Schemas contain finite numbers; they are not fed through the
legacy integer-only schema interpreter. Runtime uses the explicit owner validators.
"""
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nss_base.learner_contracts import FORMAT, RECIPE_ID, CRITERIA


def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
def c(v):return {'const':v}
def arr(x,lo,hi):return {'type':'array','items':x,'minItems':lo,'maxItems':hi}
ID={'type':'string','pattern':'^[A-Za-z0-9_.:-]{1,96}$'};SHA={'type':'string','pattern':'^[0-9a-f]{64}$'}
V={'type':'integer','const':1};TIME={'type':'integer','minimum':0,'maximum':253402300799}
TEXT={'type':'string','minLength':1,'maxLength':2000};NONE=c('NONE')
recipe=obj({'id':c(RECIPE_ID),'seed':{'type':'integer','minimum':0,'maximum':2**31-1},
    'steps':{'type':'integer','minimum':1,'maximum':1000},'learning_rate':{'type':'number','minimum':.00001,'maximum':.1}})
origin={'oneOf':[{'type':'null'},obj({'task_id':ID,'record_sha256':SHA,'context_packet_sha256':SHA})]}
plan=obj({'schema_version':V,'format':c(FORMAT),'cycle_id':ID,'producer_id':ID,'at':TIME,'reason':TEXT,
    'parent':{'$ref':'qualification_binding.schema.json'},
    'parent_core_certificate':obj({'request_id':ID,'certificate_sha256':SHA}),
    'archive_sha256':SHA,'snapshot_request':{'$ref':'dataset_build.schema.json'},'recipe':recipe,
    'budget':obj({'optimizer_updates':{'type':'integer','minimum':0,'maximum':1000},
        'evaluation_passes':{'type':'integer','minimum':0,'maximum':2},'training_attempts':{'type':'integer','const':1}}),
    'criteria':c(CRITERIA),'code_sha256':SHA,'environment_sha256':SHA,'origin':origin,'authority':NONE})
operators=obj({'schema_version':V,'format':c(FORMAT),'producer_ids':arr(ID,1,32),'approver_ids':arr(ID,1,32)})
for k in ('producer_ids','approver_ids'):operators['properties'][k]['uniqueItems']=True
snapshot=obj({'snapshot_id':ID,'sha256':SHA,'member_count':{'type':'integer','const':2}})
receipt=obj({'id':ID,'plan_sha256':SHA,'report_sha256':SHA,'verdict':{'enum':['PASS','FAIL','INCONCLUSIVE']},'authority':NONE})
numeric=obj({'schema_version':V,'kind':{'enum':['OVERLAY_TRAINING','OVERLAY_EVALUATION']},
    'learning_plan':plan,'snapshot':snapshot,'training_receipt':{'oneOf':[{'type':'null'},receipt]},'authority':NONE})
proposal=obj({'schema_version':V,'format':c(FORMAT),'cycle_id':ID,'learning_plan_sha256':SHA,
    'parent':{'$ref':'qualification_binding.schema.json'},'snapshot':snapshot,'training':receipt,'evaluation':receipt,
    'numerical_verdict':{'enum':['PASS','FAIL','INCONCLUSIVE']},
    'recommendation':{'enum':['INDEPENDENT_REVIEW_REQUIRED','NOT_RECOMMENDED']},
    'qualification_status':c('INSUFFICIENT_EVIDENCE'),
    'missing_claims':c(['PROFILE:A2','PROFILE:A2B','DIRECTED_TRANSITIONS_FOR_NEW_CANDIDATE']),
    'authority':NONE,'deployment_authorized':c(False),'runtime_execution_permit':c(False),
    'scope':c('Fixed A2 overlay recipe; no self-qualification or successor-Core authority')})
for name,x in [('plan',plan),('operators',operators),('numerical_plan',numeric),('proposal',proposal),
    ('approval',obj({'cycle_id':ID,'plan_sha256':SHA,'approver_id':ID,'expires_at':TIME}))]:
    (ROOT/f'schemas/learner_{name}.schema.json').write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**x},indent=2)+'\n')
print('Generated five bounded learner exchange schemas. Owner validators enforce policy, lineage, roles and recovery.')
