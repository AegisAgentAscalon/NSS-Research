"""Retained input/oracle/hash and durable attempt checks; no optimizer reproduction."""
from pathlib import Path
import hashlib,json,sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from reference import oracle
root=Path(__file__).resolve().parents[1];src=root/'primary'
def canon(o):return json.dumps(o,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def ah(a):
 d=hashlib.sha256()
 for k,v in sorted(a.items()):
  v=np.ascontiguousarray(v);d.update(canon([k,str(v.dtype),list(v.shape)]));d.update(v.tobytes())
 return d.hexdigest()
def read(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
intents={};commits={};tail='0'*64;counts={k:0 for k in ['updates','backwards','cells','heads']};seq=0
for line in (src/'audit/attempts.jsonl').read_text().splitlines():
 r=json.loads(line);seq+=1;given=r.pop('hash');assert r['seq']==seq and r['previous']==tail
 tail=hashlib.sha256(canon(r)).hexdigest();assert tail==given
 if r['kind']=='INTENT':
  intents[r['seq']]=r
  for k in counts:counts[k]+=r['cost'][k]
 elif r['kind']=='COMMIT':
  assert r['intent'] in intents and r['intent'] not in commits;commits[r['intent']]=r
assert len(intents)==len(commits)
for k,v in counts.items():assert v==json.loads((src/'audit/COUNTS.json').read_text())['counts'][k]
train_intents={r['op']:r for r in intents.values() if '/fit/' in r['op']};checked=0;prefix_targets=0
for folder in [src/'probe']+sorted((src/'train').iterdir()):
 name='cost_probe' if folder.name=='probe' else folder.name.removeprefix('fit');d=read(folder/'INPUTS.npz');prev=ah(read(folder/'initial.npz'))
 records=[json.loads(l) for l in (folder/'TRAINING.jsonl').read_text().splitlines()]
 for u,(n,r) in enumerate(zip(d['lengths'],records)):
  e=d['events'][u,:,:int(n)];bits,nxt=oracle(e);packed=np.sum(bits.astype(np.uint8)*(1<<np.arange(4,dtype=np.uint8)),axis=-1,dtype=np.uint8)
  inp=ah({'A':e,'packed':packed,'B':d['b_events'],'target_B':d['b_labels']});rec=train_intents[f'{name}/fit/{u}']
  assert inp==rec['inputs'] and prev==rec['pre'];commit=commits[rec['seq']]
  assert commit['post']==r['post'] and r['update']==u+1
  prev=r['post'];checked+=1;prefix_targets+=bits.shape[0]*bits.shape[1]
 assert prev==ah(read(folder/'terminal.npz'))
summary={'training_updates_hash_oracle_checked':checked,'A_prefix_targets_independently_rebuilt':prefix_targets,
 'durable_intents':len(intents),'durable_commits':len(commits),'unknown_completion_current_pass':0,'counts':counts,
 'initial_optimization_independently_recomputed':False,'full_learning_replay_checked_separately':True,
 'archived_initial_raw_gradients':'Hash/norm recorded every update; raw values not captured for all initial steps. Full Adam/RNG/cursor checkpoints every250 and exact second training retained.'}
(root/'audit/TRAINING_INPUT_AND_LEDGER_CHECK.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
