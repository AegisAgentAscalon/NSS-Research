from __future__ import annotations
import os
for x in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):os.environ[x]='1'
import sys,json,tempfile,time,collections
from pathlib import Path
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from nss_bridge.runner import run_episode,independent_grade,fixtures
from nss_bridge.util import canonical,atomic_json,file_hash
R=Path(__file__).resolve().parents[1]
torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
torch.backends.mkldnn.enabled=False

def audit():
 start=time.perf_counter();lock=json.loads((R/'protocol/LOCK.json').read_text())
 for f in lock['files']:assert file_hash(R/f['path'])==f['sha256'],f['path']
 assert canonical(fixtures())==canonical(json.loads((R/'fixtures/EPISODES.json').read_text()))
 models={}
 for s in range(4101,4105):
  z=np.load(R/'models'/f'parent_{s}.npz',allow_pickle=False)
  cell=torch.nn.GRUCell(26,64,dtype=torch.float64);head=torch.nn.Linear(64,9,dtype=torch.float64)
  cell.load_state_dict({k.split('.',1)[1]:torch.tensor(z[k],dtype=torch.float64) for k in z.files if k.startswith('cell.')})
  head.load_state_dict({k.split('.',1)[1]:torch.tensor(z[k],dtype=torch.float64) for k in z.files if k.startswith('head.')})
  cell.eval();head.eval();models[s]=(cell,head)
 counts={'cases':0,'independent_recounts':0,'full_fresh_replays':0,'numerical_scalars':0,'outside':0,'argmax_differences':0,'recount_mismatches':0,'neural_event_labels_checked':0,'raw_response_judgments':0,'mismatched_acceptance':0,'effect_integrity':0};maxerr=0.;reas=collections.Counter();results=[]
 with torch.no_grad(),tempfile.TemporaryDirectory() as td:
  for p in sorted((R/'results/main/cases').glob('*/RESULT.json')):
   old=json.loads(p.read_text());counts['cases']+=1
   met=independent_grade(old);counts['independent_recounts']+=1
   assert not met['contract_errors'] and met['complete'];counts['effect_integrity']+=met['effects']
   new=run_episode(old['spec'],old['mode'],old['seed'],Path(td)/p.parent.name)
   assert canonical(old)==canonical(new),('FRESH_REPLAY',p.parent.name)
   counts['full_fresh_replays']+=1
   # Independent per-response check based on the exact public state AT SUBMISSION.
   # The inflight-revision and lost-reply cases are distinguished, never graded as normal initial replies.
   for r in old['records']:
    counts['raw_response_judgments']+=1;res=r['result'];reas[res['reason']]+=1
    if res['reason']=='SIMULATED_PERFORMED':
     proposal=json.loads(r['raw']);b=r['before'];todo=[i for i,v in enumerate(b['done']) if not v]
     assert todo and proposal['step']==todo[0]
     assert proposal['owner']==b['owner'] and proposal['task_id']==b['task_id'] and proposal['revision']==b['revision']
     if proposal['step']==7:assert b['approval']==b['revision']
    if res['reason']=='FINISHED':assert all(r['before']['done'])
   if old['seed'] is not None:
    cell,head=models[old['seed']];hs={};done={};cur={}
    for row in old['final']['neural']:
     k=row['key'];e=row['token']
     if k not in hs:hs[k]=torch.zeros(1,64,dtype=torch.float64);done[k]=set();cur[k]=0
     if e<8:done[k].add(e)
     elif e<16:done[k].discard(e-8)
     elif e==16:done[k].clear()
     elif e!=17:raise ValueError('BAD_EVENT')
     expected=min(set(range(8))-done[k]) if len(done[k])<8 else 8
     assert row['exact_next']==expected;cur[k]+=1;assert row['cursor']==cur[k];counts['neural_event_labels_checked']+=1
     x=torch.zeros(1,26,dtype=torch.float64);x[0,e]=1
     hs[k]=cell(x,hs[k]);out=head(hs[k]);a=np.r_[row['h'],row['logits']];b=np.r_[hs[k].numpy()[0],out.numpy()[0]]
     err=np.abs(a-b);tol=1e-9+1e-8*np.abs(b);counts['numerical_scalars']+=len(a);counts['outside']+=int((err>tol).sum());maxerr=max(maxerr,float(err.max()))
     counts['argmax_differences']+=int(int(out.argmax())!=row['prediction'])
   results.append({'case':p.parent.name,'sha256':file_hash(p),'grade':met})
 assert counts['outside']==counts['argmax_differences']==0
 total=sum(p.stat().st_size for p in R.rglob('*') if p.is_file())
 out={'counts':counts,'maximum_absolute_numeric_difference':maxerr,'tolerance':'1e-9+1e-8*abs(reference)','reason_counts':dict(reas),'seconds':time.perf_counter()-start,
      'all_source_locks_unchanged':len(lock['files']),'case_records':results,'optimizer_applications':0,
      'limits':{'bytes_before_doc_packaging':total,'64MiB_exceeded':total>64*1024**2,'note':'Final footprint and runner time/RSS checked retrospectively; protocol caps were NOT continuously enforced except request-round cap. Original source unchanged.'},
      'review':'All finite typed operations replayed independently. No natural-language generation or independent human semantic review; displayed prose is a deterministic rendering.'}
 return out
if __name__=='__main__':
 out=audit();atomic_json(R/'audit/AUDIT.json',out);print(json.dumps({k:v for k,v in out.items() if k!='case_records'},indent=2))
