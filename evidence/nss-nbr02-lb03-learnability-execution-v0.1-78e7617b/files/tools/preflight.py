from pathlib import Path
import sys,time,traceback,json,hashlib
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
from candidate import *
from task import oracle,independent_oracle
LOG=R/'audit/PREFLIGHT_UPDATES.jsonl';tests=[];updates=0

def check(name,fn):
 start=time.perf_counter();result=fn();tests.append(dict(name=name,status='PASS',seconds=time.perf_counter()-start,detail=result));write(R/'audit/PREFLIGHT_PARTIAL.json',dict(tests=tests,actual_updates=updates));print(name,'PASS',flush=True)
def step(s,t,y):
 global updates
 if updates>=C['preflight_update_cap']:raise RuntimeError('PREFLIGHT_CAP')
 updates+=1
 with LOG.open('a')as f:f.write(json.dumps(dict(application=updates,status='INTENT',seed=s.seed,mode=s.mode,regime=s.regime,cursor=s.cursor+1))+'\n');f.flush();os.fsync(f.fileno())
 row=s.step(t,y,.0003)
 with LOG.open('a')as f:f.write(json.dumps(dict(application=updates,status='COMMITTED',row=row))+'\n');f.flush();os.fsync(f.fileno())
 return row

def taskcheck():
 for mask in range(256):
  prefix=[j for j in range(8) if mask&(1<<j)]
  for e in range(18):
   t=np.array([prefix+[e]],np.uint8);a,_=oracle(t);assert np.array_equal(a,independent_oracle(t))
 return dict(state_event_pairs=4608)
def qcheck():
 rng=np.random.default_rng(16101);count=0
 for dt in (np.float32,np.float16):
  for cols in (1,26,64):
   a=np.asarray(rng.normal(0,.1,(32,cols)),dt);c=quant(a);n=q_numpy(a)
   for x,y in zip(c,n):assert np.array_equal(x,y),(dt,cols)
   count+=a.size
 for n in range(256):
  q=np.array([(n>>j)&3 for j in [0,2,4,6]],np.uint8);p=int((q.astype(np.uint16)*[1,4,16,64]).sum());assert p==n
 return dict(quantized_values=count,packed_patterns=256)
def roundcheck():
 rng=np.random.default_rng(16102);x=rng.uniform(-2,2,4096).astype(np.float32);out=np.empty(len(x),np.uint16);state=np.array([16102],np.uint64)
 assert LIB.round_array(len(x),ptr(x),ptr(out),0,ptr(state))==0
 assert np.array_equal(out.view(np.float16),x.astype(np.float16))
 a=np.full(20000,1+2**-12,np.float32);s0=state.copy();out=np.empty(len(a),np.uint16)
 assert LIB.round_array(len(a),ptr(a),ptr(out),1,ptr(state))==0
 h=out.view(np.float16);rate=float(np.mean(h>1));assert .235<rate<.265,rate
 replay=np.empty_like(out);assert LIB.round_array(len(a),ptr(a),ptr(replay),1,ptr(s0))==0;assert np.array_equal(out,replay)and np.array_equal(state,s0)
 return dict(nearest_values=len(x),stochastic_draws=len(a),upper_fraction=rate,expected=.25)
def optimizercheck():
 # Independent NumPy update for M32+M8. C does not use native Torch Adam.
 rng=np.random.default_rng(16103);n=257;w=rng.normal(0,.1,n).astype(np.float32);g=rng.normal(0,.01,n).astype(np.float32);qm=np.zeros(n,np.int8);qv=np.zeros(n,np.uint8);sm=np.zeros(3,np.float32);sv=np.zeros(3,np.float32)
 maxerr=0
 for st in range(1,6):
  wr=w.copy();qmr=qm.copy();qvr=qv.copy();smr=sm.copy();svr=sv.copy()
  for b,start in enumerate(range(0,n,128)):
   sl=slice(start,min(n,start+128));om=(qmr[sl].astype(np.float32)*smr[b]).astype(np.float32);vroot=(qvr[sl].astype(np.float32)*svr[b]).astype(np.float32);ov=(vroot*vroot).astype(np.float32)
   mm=(.9*om.astype(np.float64)+.1*g[sl].astype(np.float64)).astype(np.float32);vv=(.999*ov.astype(np.float64)+.001*g[sl].astype(np.float64)**2).astype(np.float32)
   x=(wr[sl].astype(np.float64)-float(np.float32(.001))*(mm.astype(np.float64)/(1-.9**st))/(np.sqrt(vv.astype(np.float64)/(1-.999**st))+1e-8)).astype(np.float32);wr[sl]=x
   mx=np.max(np.abs(mm));vx=np.max(vv);smr[b]=np.float32(mx/np.float32(127)) if mx else 0;svr[b]=np.float32(np.sqrt(float(vx))/255) if vx else 0
   qmr[sl]=np.clip(np.rint(mm.astype(np.float64)/float(smr[b])) if smr[b] else np.zeros_like(mm),-127,127).astype(np.int8)
   qvr[sl]=np.clip(np.rint(np.sqrt(vv.astype(np.float64))/float(svr[b])) if svr[b] else np.zeros_like(vv),0,255).astype(np.uint8)
  stats=np.zeros(4,np.uint64);err=np.zeros(1,np.float64);rs=np.array([16103],np.uint64)
  assert LIB.adam_m8(n,ptr(w),ptr(g),0,0,ptr(qm),ptr(qv),ptr(sm),ptr(sv),st,np.float32(.001),ptr(rs),ptr(stats),ptr(err))==0
  for a,b in [(w,wr),(sm,smr),(sv,svr)]:maxerr=max(maxerr,float(np.abs(a-b).max()));assert np.allclose(a,b,atol=1e-8,rtol=1e-6)
  assert np.array_equal(qm,qmr)and np.array_equal(qv,qvr)
 return dict(non_model_C_steps=5,values_per_step=n,max_abs=maxerr)
def gradientcheck():
 s=Candidate(4101,'M32','EARLY');a=s.effective();t,y=load_batch(4101,0);t=t[:2,:4];y=y[:2,:4]
 w={k:torch.from_numpy(v.copy()).requires_grad_(True)for k,v in a.items()};h,z=forward(w,t);l=F.cross_entropy(z.reshape(-1,9),torch.as_tensor(y,dtype=torch.long).reshape(-1));l.backward()
 cell=torch.nn.GRUCell(26,64);head=torch.nn.Linear(64,9)
 with torch.no_grad():
  for k,v in cell.named_parameters():v.copy_(torch.from_numpy(a['cell.'+k]))
  for k,v in head.named_parameters():v.copy_(torch.from_numpy(a['head.'+k]))
 hh=torch.zeros(2,64);zs=[]
 for j in range(4):hh=cell(F.one_hot(torch.as_tensor(t[:,j],dtype=torch.long),26).float(),hh);zs.append(head(hh))
 zz=torch.stack(zs,1);ll=F.cross_entropy(zz.reshape(-1,9),torch.as_tensor(y,dtype=torch.long).reshape(-1));ll.backward()
 native={'cell.'+k:v for k,v in cell.named_parameters()};native.update({'head.'+k:v for k,v in head.named_parameters()})
 mx=0
 for k in KEYS:
  aa=w[k].grad.numpy();bb=native[k].grad.numpy();mx=max(mx,float(np.abs(aa-bb).max()));assert np.allclose(aa,bb,atol=C['numerical']['fp32_grad_atol'],rtol=C['numerical']['fp32_grad_rtol'])
 # Sample actual FP32 vs FP64 fixed-effective-weight gradients, no discrete derivative claim.
 wd={k:torch.from_numpy(v.copy()).double().requires_grad_(True)for k,v in a.items()};_,zd=forward(wd,t);ld=F.cross_entropy(zd.reshape(-1,9),torch.as_tensor(y,dtype=torch.long).reshape(-1));ld.backward()
 for k in KEYS:assert np.allclose(w[k].grad.numpy(),wd[k].grad.numpy(),atol=C['numerical']['fp32_grad_atol'],rtol=C['numerical']['fp32_grad_rtol'])
 return dict(native_manual_gradient_scalars=18249,fp32_fp64_gradient_scalars=18249,max_abs_native=mx,forward_backward_only_optimizer_updates=0)
def modelcheck():
 allrows=[]
 for regime in C['regimes']:
  for mode in C['modes']:
   s=Candidate(4101,mode,regime);t,y=load_batch(4101,0);t=t[:4,:8];y=y[:4,:8]
   for j in range(2):step(s,t,y)
   file=R/f'audit/pref_{regime}_{mode}.npz';s.save(file);clone=Candidate.load(file);a=step(s,t,y);b=step(clone,t,y)
   assert s.hash()==clone.hash();assert {k:v for k,v in a.items()if k not in('seconds','peak_rss')}=={k:v for k,v in b.items()if k not in('seconds','peak_rss')}
   values=s.effective();ph,pz=packed_roll(s,t);nh,nz=np_forward(values,t)
   for aa,bb in ((ph,nh),(pz,nz)):
    c=comparison(aa,bb);assert c['finite'] and c['violations']==0
   allrows.append(dict(mode=mode,regime=regime,states_equal=True))
 return dict(cases=allrows,actual_model_updates=updates)
def corruptioncheck():
 p=R/'audit/pref_EARLY_M16_NEAREST.npz'
 with np.load(p,allow_pickle=False)as z:arrays={k:z[k].copy()for k in z.files}
 tests_=[]
 for defect in ['value','dtype','source','cursor']:
  aa={k:v.copy()for k,v in arrays.items()};meta=json.loads(aa['meta'].tobytes())
  if defect=='value':aa['w:head.bias'][0]+=1
  elif defect=='dtype':aa['w:head.weight']=aa['w:head.weight'].astype(np.float32)
  elif defect=='source':meta['source']='0'*64
  elif defect=='cursor':meta['optstep']+=1
  aa['meta']=np.frombuffer(canon(meta),np.uint8);q=R/f'audit/fault_{defect}.npz';np.savez_compressed(q,**aa)
  try:Candidate.load(q)
  except ValueError:tests_.append(defect)
  else:raise AssertionError('ACCEPTED_FAULT:'+defect)
 return dict(rejected=tests_)
try:
 check('explicit_task_rules',taskcheck);check('quantizer_and_packing',qcheck);check('rounding_and_RNG',roundcheck);check('optimizer_reference',optimizercheck);check('gradient_equations',gradientcheck);check('actual_updates_and_restart',modelcheck);check('corrupt_snapshot_rejection',corruptioncheck)
 write(R/'audit/PREFLIGHT.json',dict(status='PASS',groups=tests,actual_model_updates=updates,non_model_optimizer_reference_steps=5,no_main_results_examined=True))
except BaseException as e:
 write(R/'failures/PREFLIGHT_STOP.json',dict(exception=repr(e),traceback=traceback.format_exc(),actual_model_updates=updates,completed=tests));raise
