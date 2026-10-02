#!/usr/bin/env python3
"""EvaluationRun001 local schemas, using only the repository validator's keywords."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'schemas'
def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
def st(n=4096,m=1,p=None):
    v={'type':'string','minLength':m,'maxLength':n}
    if p:v['pattern']=p
    return v
def enum(*v):return {'type':'string','enum':list(v)}
def integer(lo,hi):return {'type':'integer','minimum':lo,'maximum':hi}
def arr(s,n=32,m=1):return {'type':'array','items':s,'minItems':m,'maxItems':n}
ID=st(128,1,'[A-Za-z0-9_.:-]+'); SHA=st(64,64,'[0-9a-f]{64}')
TIME=st(20,20,r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
V={'type':'integer','enum':[1]}; BOOL={'type':'boolean'}
REF=obj({'path':st(512),'sha256':SHA})
DATA=obj({'snapshot_id':ID,'sha256':SHA,'split':enum('validation')});DATA['type']=['object','null']
PLAN=obj({'schema_version':V,'run_id':ID,'actor':{'$ref':'experience_actor.schema.json'},'at':TIME,
    'reason':st(),'candidate':obj({'manifest':REF,'profile':ID,'expected_ecid':SHA}),
    'suite':REF,'implementation_sha256':SHA,'repeats':integer(1,5),'max_evaluations':integer(1,160),
    'development_snapshot':DATA})
VECTOR=arr(integer(-(10**150),10**150),64)
TEST=obj({'id':ID,'version':ID,'checker':enum('exact_integer_sequence_v1'),
          'fixture':REF,'expected':VECTOR,'mandatory':BOOL})
SUITE=obj({'schema_version':V,'id':ID,'version':ID,'purpose':enum('DEVELOPMENT_SYNTHETIC'),
    'evaluation_permission':obj({'actor':{'$ref':'experience_actor.schema.json'},'reference':st()}),
    'minimum_pass_basis_points':integer(0,10000),'tests':arr(TEST)})
FILE=obj({'path':st(512),'sha256':SHA,'role':enum('manifest','operation','suite','fixture'),
          'text':st(1024*1024)})
# Bounded inventory capacity, not a license to omit newly installed modules.
# v0.4.12 exceeds the earlier 128-entry envelope; all file hashes remain bound.
MAX_IMPLEMENTATION_FILES=256
CODE=obj({'version':enum('evaluation-integer-v1'), 'files':arr(obj({'path':st(512),'sha256':SHA}),MAX_IMPLEMENTATION_FILES),
    'environment':obj({'python':st(256),'implementation':st(128),'platform':st(1024),'machine':st(128,0)}),
    'sha256':SHA})
OBS=obj({'snapshot_id':ID,'sha256':SHA,'split':enum('validation'),
         'examples_sha256':SHA,'member_count':integer(1,32)})
OBS['type']=['object','null']
MATERIAL=obj({'schema_version':V,'format':enum('MegaMindAlpha.EvaluationMaterial001'),
    'files':arr(FILE,128),'implementation':CODE,'development_observation':OBS})
TRIAL=obj({'repeat':integer(1,5),'test_id':ID,'test_version':ID,'input_sha256':SHA,
    'expected_sha256':SHA,'observed':VECTOR,'observed_sha256':SHA,'passed':BOOL})
REPEAT=obj({'repeat':integer(1,5),'complete':BOOL,'sha256':SHA})
REPORT=obj({'schema_version':V,'format':enum('MegaMindAlpha.EvaluationRun001'),
    'run_id':ID,'plan_sha256':SHA,'material_sha256':SHA,'checker':enum('exact_integer_sequence_v1'),
    'scope':enum('DEVELOPMENT_SYNTHETIC_NOT_RELEASE_QUALIFICATION'),
    'authority':enum('NONE'),'expected_checks':integer(1,160),'completed_checks':integer(0,160),
    'verdict':enum('PASS','FAIL','INCONCLUSIVE'),'stop_reason':enum('COMPLETE','BUDGET_EXHAUSTED'),
    'reproducible':{'type':['boolean','null']},'trials':arr(TRIAL,160,0),'repeats':arr(REPEAT,5)})
for name,schema in {'evaluation_plan':PLAN,'evaluation_suite':SUITE,'evaluation_material':MATERIAL,'evaluation_report':REPORT}.items():
    (S/(name+'.schema.json')).write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**schema},indent=2)+'\n')
print('Generated 4 EvaluationRun001 schemas.')
