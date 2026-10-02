"""No learning: exact comparison of already computed capture and adaptive replay."""
from pathlib import Path
import json,hashlib,sys,os
import numpy as np
ROOT=Path(__file__).resolve().parent.parent;sys.path.insert(0,str(ROOT/'source'))
from reference_numeric import records,canonical
p=ROOT/'raw/primary';q=ROOT/'raw/replay';narr=nelem=nframe=0
for (i,m,a),(j,mm,b) in __import__('itertools').zip_longest(records(p/'worker/records.bin'),records(q/'worker/records.bin')):
 assert i==j and canonical(m)==canonical(mm),'FRAME_METADATA';assert a.keys()==b.keys()
 nframe+=1
 for k in a:
  assert a[k].dtype==b[k].dtype and a[k].shape==b[k].shape and a[k].tobytes()==b[k].tobytes(),'ARRAY:'+k
  narr+=1;nelem+=a[k].size
matched=[]
for rel in ['private/PLAN.json','A0_AND_GUARDS_LOCK.json','EXACT.json','NOVELTY.json','COUNTERS.json','worker/events.jsonl','worker/SCHEMA_OBSERVED.json','public_messages.jsonl','public_responses.jsonl']:
 assert (p/rel).read_bytes()==(q/rel).read_bytes(),'NONNUMERIC:'+rel;matched.append(rel)
for a in (p/'final_audit').iterdir():
 if a.suffix=='.csv' or a.name=='DECISIONS.json':
  assert a.read_bytes()==(q/'final_audit'/a.name).read_bytes(),'SCORES:'+a.name;matched.append('final_audit/'+a.name)
pa=json.loads((p/'final_audit/AUDIT.json').read_text());qa=json.loads((q/'final_audit/AUDIT.json').read_text())
assert pa==qa,'INDEPENDENT_AUDIT_JSON'
cp=json.loads((p/'COUNTERS.json').read_text())['counts'];cq=json.loads((q/'COUNTERS.json').read_text())['counts'];assert cp==cq
caps=json.loads((ROOT/'protocol/WORK_LEDGER.json').read_text())['proposed_global_hard_caps'];mapping={'update_attempt':'updates','cell':'cells','head':'heads','backward':'reverse_calls','old_backward':'old_margin_reverse_calls','local':'L_focal_gradients','qp':'qp_calls','support':'support_candidates','svd':'svd_calls'}
actual={k:cp[k]+cq[k] for k in cp}
for k,cap in mapping.items():assert actual[k]<=caps[cap],k
result={'status':'PASS','full_adaptive_replay_of_completed_prefix':True,'heldout_generated':False,'frames':nframe,'arrays':narr,'elements':nelem,'byte_equal_files':matched,'all_attempt_counts':actual,'no_unknown_completion':actual['update_attempt']==actual['update_commit'],'engineering_scoring':pa['stats'],'not_independent_training_algorithm_or_external_replication':True}
(ROOT/'audit/REPLAY_COMPARISON.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
