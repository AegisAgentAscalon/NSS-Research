"""Post-result diagnostic; preserves the failed original whole-prefix tolerance gate."""
from pathlib import Path
import sys,json,csv
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'source'))
from reference import KEYS,from_flat,forward,oracle
root=Path(__file__).resolve().parents[1];src=root/'primary';out=root/'analysis/numerical_localization';out.mkdir(parents=True,exist_ok=True)
def read(p):
 with np.load(p,allow_pickle=False) as z:return {k:z[k] for k in z.files}
local_n=0;localmax=0.;localbad=0;chain_n=0;chainbad=0;chainmaxabs=0.;rows=[];classes=[]
def c_local(a,b):
 global local_n,localmax,localbad
 diff=np.abs(np.asarray(a,float)-b);q=diff/(2e-6+2e-5*np.abs(b));local_n+=q.size;localmax=max(localmax,float(q.max(initial=0)));localbad+=int((q>1).sum())
def m_joint(o,t,n):return bool(np.array_equal(o[:4]>0,t.astype(bool)) and np.argmax(o[4:])==n)
for ctx in sorted((src/'contexts').iterdir()):
 meta=json.loads((ctx/'CONTEXT.json').read_text());pub=read(ctx/'PUBLIC.npz');ev=pub['events'];ls=pub['lengths'];su=pub['suffix'];h0=pub['initial_h']
 old=read(ctx/'weights_0.npz');w0=from_flat(np.concatenate([old[k].ravel() for k in KEYS]))
 for stage in range(3):
  wn=read(ctx/f'weights_{stage}.npz');w=from_flat(np.concatenate([wn[k].ravel() for k in KEYS]));r=read(ctx/f'A_stage_{stage}.npz')
  rebuilt64=np.zeros((32,64))
  for n in sorted(set(map(int,ls))):
   ii=np.flatnonzero(ls==n);observed=r['prefix_states'][ii,:n];obs_z=r['prefix_logits'][ii,:n]
   hs,zz,_=forward(w,ev[ii,:n]);rebuilt64[ii]=hs[:,-1]
   dif=np.abs(obs_z-zz);q=dif/(2e-6+2e-5*np.abs(zz));chain_n+=q.size;chainbad+=int((q>1).sum());chainmaxabs=max(chainmaxabs,float(dif.max(initial=0)))
   if (q>1).any():
    loc=np.unravel_index(np.argmax(q),q.shape)
    rows.append({'context':ctx.name,'stage':stage,'length':n,'tensor':'logits','bad_scalars':int((q>1).sum()),'max_ratio':float(q.max()),'max_abs_diff':float(dif.max()),'worst_observed':float(obs_z[loc]),'worst_reference':float(zz[loc])})
   for t in range(n):
    prev=np.zeros((len(ii),64)) if t==0 else observed[:,t-1]
    h,z,_=forward(w,ev[ii,t:t+1],prev);c_local(observed[:,t],h[:,0]);c_local(obs_z[:,t],z[:,0])
  for mode in ['CARRY','REBUILD','RESET','PINNED']:
   mw=w0 if mode=='PINNED' else w
   given={'CARRY':h0,'REBUILD':rebuilt64,'RESET':np.zeros_like(h0),'PINNED':h0}[mode]
   hs,zz,_=forward(mw,np.tile(su,(32,1)),given)
   zs=np.concatenate([(given@mw['head.weight'].T+mw['head.bias'])[:,None],zz],axis=1)
   obs=r[mode+'_logits'];st=r[mode+'_states']
   c_local(obs[:,0],st[:,0].astype(float)@mw['head.weight'].T+mw['head.bias'])
   for t in range(8):
    h,z,_=forward(mw,np.tile(su[t:t+1],(32,1)),st[:,t]);c_local(st[:,t+1],h[:,0]);c_local(obs[:,t+1],z[:,0])
   for i in range(32):
    b,n=oracle(np.r_[ev[i,:ls[i]],su]);truth=b[0,int(ls[i])-1:];nxt=n[0,int(ls[i])-1:]
    for p in [0,1,2,4,8]:
     cls_diff=not(np.array_equal(obs[i,p,:4]>0,zs[i,p,:4]>0) and np.argmax(obs[i,p,4:])==np.argmax(zs[i,p,4:]))
     classes.append({'split':meta['split'],'context':ctx.name,'stage':stage,'mode':mode,'history':i,'position':p,'class_vector_diff':int(cls_diff),'torch_joint':int(m_joint(obs[i,p],truth[p],nxt[p])),'float64_joint':int(m_joint(zs[i,p],truth[p],nxt[p])),'max_abs_logit_diff':float(np.max(np.abs(obs[i,p]-zs[i,p])))})
summary={'kind':'Exploratory numerical localization, not replacement of frozen qualification',
 'original_whole_prefix_tolerance_gate':'FAILED_UNCHANGED','one_step_scalar_comparisons':local_n,'one_step_out_of_tolerance':localbad,'one_step_max_ratio':localmax,
 'whole_prefix_logit_scalars':chain_n,'whole_prefix_logit_out_of_tolerance_scalars':chainbad,'whole_prefix_max_abs_logit_difference':chainmaxabs,
 'semantic_rows':len(classes),'class_vector_differences':sum(x['class_vector_diff'] for x in classes),
 'joint_correctness_differences':sum(x['torch_joint']!=x['float64_joint'] for x in classes),
 'maximum_query_logit_difference':max(x['max_abs_logit_diff'] for x in classes),
 'interpretation':'Recorded-step arithmetic versus original chained float64 recursion are different checks. Single-step consistency and endpoint agreement do not retroactively pass the original chained numeric gate.'}
for name,rs in [('LONG_PREFIX_EXCEEDANCES.csv',rows),('SEMANTIC_COMPARISON.csv',classes)]:
 with open(out/name,'w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(rs[0]) if rs else ['none']);w.writeheader();w.writerows(rs)
(out/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n');print(json.dumps(summary),flush=True)
