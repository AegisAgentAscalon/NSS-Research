#!/usr/bin/env python3
"""Generate only the DatasetSnapshot001 and new public batch-use API schemas.
No external schema resolution. Existing archive schemas are inputs, not rewritten.
"""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]; S=ROOT/'schemas'
def obj(props):return {'type':'object','properties':props,'required':list(props),'additionalProperties':False}
def st(n=4096,m=1,p=None):
    s={'type':'string','minLength':m,'maxLength':n}
    if p:s['pattern']=p
    return s
def enum(*v):return {'type':'string','enum':list(v)}
def arr(s,n=32,m=1):return {'type':'array','items':s,'minItems':m,'maxItems':n}
def ref(name):return {'$ref':name+'.schema.json'}
ID=st(128,1,'[A-Za-z0-9_.:-]+');SHA=st(64,64,'[0-9a-f]{64}');TIME=st(20,20,r'[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
V={'type':'integer','enum':[1]}
EXACT=obj({'experience_id':ID,'revision':{'type':'integer','minimum':0,'maximum':511},'sha256':SHA})
MEMBER=obj({**EXACT['properties'],'split':enum('train','validation')})
TOKEN=obj({'id':ID,'version':st(128),'sha256':SHA})
REQ=obj({'schema_version':V,'snapshot_id':ID,'operation_id':ID,'actor':ref('experience_actor'),
    'at':TIME,'reason':st(),'purpose':enum('training'),'transform':enum('curated_text_v1','normalize_newlines_v1'),
    'tokenizer':TOKEN,'members':arr(MEMBER)})
rev=json.loads((S/'experience_revision.schema.json').read_text())['properties']
cap=json.loads((S/'experience_capture.schema.json').read_text())['properties']
VIEW=obj({'reference':EXACT,'purpose':enum('memory','retrieval','training','redistribution'),
    'statement':rev['statement'],'sources':rev['sources'],'observation':cap['observation'],
    'family_id':ID,'sensitivity':cap['sensitivity'],'updated_at':TIME,
    'review':rev['review'],'permission':rev['permissions']['properties']['training'],
    'source_revocation_status':enum('CLEAR'),'scope':enum('local-attestation-v1')})
ENTRY=obj({'split':enum('train','validation'),'view':VIEW,'text':st(8192),'text_sha256':SHA})
MAN=obj({'format':enum('MegaMindAlpha.DatasetSnapshot001'),'schema_version':V,
    'projection_version':enum('dataset-projection-v1'),'archive_binding':SHA,
    'request':REQ,'request_sha256':SHA,'members':arr(ENTRY)})
items={'experience_use_batch':obj({'references':arr(EXACT),'purpose':enum('memory','retrieval','training','redistribution')}),
       'experience_use_view':VIEW,'dataset_build':REQ,'dataset_manifest':MAN}
for name,schema in items.items():
    (S/(name+'.schema.json')).write_text(json.dumps({'$schema':'https://json-schema.org/draft/2020-12/schema',**schema},indent=2)+'\n')
print('Generated',len(items),'DatasetSnapshot/batch-use schemas.')
