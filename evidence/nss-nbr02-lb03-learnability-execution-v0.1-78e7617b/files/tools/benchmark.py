"""Predeclared disposable actual-update benchmark, not main-trajectory retuning."""
from pathlib import Path
import sys,time,json,datetime
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
from candidate import *
OUT=R/'audit/BENCHMARK.json';LOG=R/'audit/BENCHMARK_UPDATES.jsonl'
if OUT.exists()or LOG.exists():raise RuntimeError('NO_BENCHMARK_OVERWRITE')
count=0;rows=[];rng=np.random.default_rng(C['benchmark_seed']);batch=load_batch(4101,0)
def episode(mode,regime,n,kind,rep):
 global count
 state=Candidate(4101,mode,regime);t,y=batch;times=[];start=time.perf_counter()
 for i in range(n):
  if count>=C['benchmark_update_cap']:raise RuntimeError('BENCHMARK_UPDATE_CAP')
  count+=1
  with LOG.open('a')as f:f.write(json.dumps(dict(application=count,event='intent',mode=mode,regime=regime,kind=kind,rep=rep,cursor=i+1))+'\n')
  row=state.step(t,y,lr_at(i));times.append(row['seconds'])
  with LOG.open('a')as f:f.write(json.dumps(dict(application=count,event='committed',mode=mode,regime=regime,kind=kind,rep=rep,record=row))+'\n')
 return dict(mode=mode,regime=regime,kind=kind,rep=rep,updates=n,per_step=times,step_core_total=sum(times),wall_seconds=time.perf_counter()-start,final_state_hash=state.hash())
for regime in C['regimes']:
 for mode in C['modes']:rows.append(episode(mode,regime,2,'warmup',-1))
 for rep in range(3):
  order=rng.permutation(C['modes']).tolist()
  for mode in order:rows.append(episode(mode,regime,5,'timed',rep))
summary=[]
for regime in C['regimes']:
 vals={m:[v for r in rows if r['kind']=='timed'and r['mode']==m and r['regime']==regime for v in r['per_step']] for m in C['modes']}
 base=float(np.median(vals['M32']))
 for mode,vs in vals.items():summary.append(dict(regime=regime,mode=mode,median_update_seconds=float(np.median(vs)),ratio_to_M32=float(np.median(vs))/base,samples=len(vs),runtime_gate=float(np.median(vs))/base<=C['gates']['training_time_ratio_max']))
write(OUT,dict(actual_model_updates=count,rows=rows,summary=summary,scope='Tiny-model CPU first-step overhead; three repeated five-update clones plus warmups. Parent4101 only. No end-to-end speedup, energy, larger-batch or device-limit rescue claim.'))
print(json.dumps(summary))
