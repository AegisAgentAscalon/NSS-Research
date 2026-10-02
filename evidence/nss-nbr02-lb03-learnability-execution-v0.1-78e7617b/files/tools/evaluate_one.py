from pathlib import Path
import sys,json,time
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'));sys.path.insert(0,str(R/'tools'))
from candidate import *
from task import oracle,independent_oracle
from run_one import verify_lock,evidence_size

def evaluate(seed,mode,regime):
 verify_lock()
 for ss in C['parents']:
  for mm in C['modes']:
   for rr in C['regimes']:
    f=R/f'checkpoints/{ss}_{rr}_{mm}'
    if not (f/'COMPLETE.json').exists() and not (f/'STOP.json').exists():raise RuntimeError('ALL_ENDPOINTS_MUST_BE_FROZEN')
 if not (R/'protocol/ENDPOINT_LOCK.json').exists():raise RuntimeError('ENDPOINT_LOCK_REQUIRED')
 for q in json.loads((R/'protocol/ENDPOINT_LOCK.json').read_text())['files']:
  if sha(R/q['path'])!=q['sha256']:raise RuntimeError('ENDPOINT_MUTATED')
 records=[];numeric=[];start=time.perf_counter();out=R/'results'/f'{seed}_{regime}_{mode}';out.mkdir(exist_ok=True)
 if (out/'COMPLETE.json').exists():raise RuntimeError('NO_RESULT_OVERWRITE')
 for step in C['dev_steps']:
  cp=R/f'checkpoints/{seed}_{regime}_{mode}/step{step:04d}.npz';s=Candidate.load(cp);w=s.effective();packed=out/f'step{step:04d}.q2.npz';body=pack_export(s,packed)
  panels=['development']+(['confirmation','stress'] if step in C['confirmation_steps'] else [])
  for panel in panels:
   f=R/f'fixtures/{panel}.npz'
   with np.load(f,allow_pickle=False)as z:ts=z['tokens'].copy();ys=z['labels'].copy();fam=z['families'].copy();prefix=int(z['prefix'])
   assert np.array_equal(ys,independent_oracle(ts))
   with torch.no_grad():
    ww={k:torch.from_numpy(v).double()for k,v in w.items()};th,tz=forward(ww,ts);th=th.numpy();tz=tz.numpy()
   nh,nz=np_forward(w,ts);ph,pz=packed_file_roll(packed,ts)
   nc=[]
   for name,a,b in [('torch_numpy_h',th,nh),('torch_numpy_z',tz,nz),('packed_torch_h',ph,th),('packed_torch_z',pz,tz)]:
    x=comparison(a,b);x['comparison']=name;nc.append(x)
    if not x['finite']or x['violations']or (name.endswith('_z')and not np.array_equal(a.argmax(-1),b.argmax(-1))):
     np.savez_compressed(R/f'failures/numeric_{seed}_{regime}_{mode}_{step}_{panel}.npz',a=a,b=b,tokens=ts)
     raise RuntimeError('NUMERICAL_GATE')
   pred=pz.argmax(-1).astype(np.uint8);sm=metrics(pz[:,prefix:],ys[:,prefix:]);whole=(pred[:,prefix:]==ys[:,prefix:]).all(1);bad=np.argwhere(pred[:,prefix:]!=ys[:,prefix:])
   file=out/f'step{step:04d}_{panel}.npz';meta=dict(seed=seed,mode=mode,regime=regime,step=step,prefix=prefix,checkpoint_sha=sha(cp),state_hash=s.hash(),fixture_sha=sha(f),packed_sha=sha(packed),precision='FP64 evaluated arithmetic; Q2 effective values originate FP32')
   if evidence_size()+pz.nbytes+150000>C['evidence_bytes']:raise RuntimeError('EVIDENCE_CAP_EVAL')
   np.savez_compressed(file,tokens=ts,labels=ys,predictions=pred,logits=pz,final_hidden=ph[:,-1],families=fam,meta=np.frombuffer(canon(meta),np.uint8))
   row=dict(**meta,panel=panel,file=str(file.relative_to(R)),sha256=sha(file),**sm,first_errors=[dict(history=int(h),event=int(e+prefix),input=int(ts[h,e+prefix]),expected=int(ys[h,e+prefix]),predicted=int(pred[h,e+prefix]))for h,e in bad[:12]])
   row['families']={str(k):metrics(pz[fam==k,prefix:],ys[fam==k,prefix:])for k in range(4)}
   records.append(row);numeric.append(dict(step=step,panel=panel,checks=nc))
  bt=np.arange(18,26)[:,None];bh,bz=packed_file_roll(packed,bt);refh,refz=np_forward(w,bt);n=comparison(bz,refz)
  if not n['finite']or n['violations']:raise RuntimeError('B_NUMERIC')
  labels=np.array(C['old_B']if regime=='EARLY'else C['new_B'],np.uint8);scores=bz[:,0];prob=np.exp(scores-scores.max(1,keepdims=True));prob/=prob.sum(1,keepdims=True)
  bf=out/f'step{step:04d}_B.npz';np.savez_compressed(bf,tokens=bt,labels=labels,predictions=scores.argmax(-1).astype(np.uint8),logits=scores,probabilities=prob,target_probabilities=prob[np.arange(8),labels],final_hidden=bh[:,-1])
  numeric.append(dict(step=step,panel='B',checks=[n]));records.append(dict(seed=seed,mode=mode,regime=regime,step=step,panel='B',file=str(bf.relative_to(R)),sha256=sha(bf),correct=int((scores.argmax(1)==labels).sum()),total=8,min_probability=float(prob[np.arange(8),labels].min()),changed_correct=int((scores.argmax(1)[[2,5]]==labels[[2,5]]).sum()),unchanged_correct=int((scores.argmax(1)[[0,1,3,4,6,7]]==labels[[0,1,3,4,6,7]]).sum()),packed_numerical_bytes=body))
 write(out/'COMPLETE.json',dict(records=records,numerical=numeric,seconds=time.perf_counter()-start,peak_rss=rss()))
 print(seed,regime,mode,'evaluated',len(records),'outputs',flush=True)
if __name__=='__main__':evaluate(int(sys.argv[1]),sys.argv[2],sys.argv[3])
