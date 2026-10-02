"""State/depth and binding/lifecycle evaluation. No training code imported.

Every generated fact set and label is determined before a candidate sees it.
All comparisons share source facts; learned binding errors are NOT repaired by
an oracle before readout. State-off is an information-removal ablation.
"""
import argparse,time,json,copy
from pathlib import Path
import numpy as np
import torch
from safetensors.torch import load_file
from . import data,models,common as c
from .store import RecordStore
DEPTHS=[1,2,4,8]

def source_seed(seed,h,missing,extra=0):return 900000+seed*1000+h*10+int(missing)+extra

def install(p,matcher):
 b,n=p['parent'].shape[0],p['parent'].shape[1]-1
 state=RecordStore(b,n,matcher);r=np.arange(b)
 # Events arrive in random order independent of the graph's topology.
 for j in range(n):
  ids=p['slot_ids'][:,j];dest=p['parent'][r,ids];valid=dest!=n
  state.event(torch.from_numpy(p['codes'][r,ids]),torch.from_numpy(p['codes'][r,dest]),1,torch.from_numpy(valid))
 return state

def direct_binding_score(state,p):
 # Reads each supplied source via the learned selector, then decodes stored value.
 codes=torch.from_numpy(p['codes']);b,n=state.present.shape;r=torch.arange(b)
 out=[];exist=[]
 for j in range(n):
  sel=state.matcher(codes[:,j],state.keys,state.present).argmax(-1);found=sel<n
  read=state.vals[r,sel.clamp(max=n-1)]
  pred=torch.einsum('bd,bnd->bn',torch.nn.functional.normalize(read,dim=-1),codes).argmax(-1)
  pred=torch.where(found,pred,torch.full_like(pred,n))
  out.append(pred.numpy());exist.append(found.numpy())
 return np.stack(out,1),np.stack(exist,1)

def distract(state,p,rng,count,sigma=0.0):
 # All events update only the last topological background subject; no tested
 # path node or room is overwritten. Includes wrong-scope and denied writes.
 b,n=state.present.shape;r=np.arange(b);ids=p['order'][:,-1]
 src=torch.from_numpy(p['codes'][r,ids])
 for j in range(count):
  target=p['rooms'][:,j%2];val=torch.from_numpy(p['codes'][r,target])
  if j%7==0:
   state.event(src,val,1,scope='other')
  elif j%7==1:
   state.event(src,val,1,qualified=False)
  else:
   state.event(src,val,1)
   p['parent'][r,ids]=target
  if sigma:state.perturb(rng,sigma)


def metrics(pred,p,depth,kind):
 target=data.oracle_answer(p);n=p['parent'].shape[1]-1
 known=target!=n;unknown=~known;rooms=p['rooms']
 isroom=(pred[:,None]==rooms).any(-1);unresolved=(pred!=n)&~isroom
 hit=pred==target
 return {'answer_accuracy':float(hit.mean()),'known_accuracy':float(hit[known].mean()) if known.any() else None,'unknown_accuracy':float(hit[unknown].mean()) if unknown.any() else None,'unsupported_room_rate':float(isroom[unknown].mean()) if unknown.any() else None,'unresolved_rate':float(unresolved.mean()),'n':len(pred),'actual_query_rounds':min(depth,4) if kind in ('fixed_attention4','fixed_aligned4','untied_hop4') else depth}

@torch.no_grad()
def evaluate(kind,seed,checkpoint,binder_path,outdir,small=False):
 outpath=Path(outdir)/f'{kind}_{seed}.json'
 if outpath.exists() or outpath.with_suffix('.npz').exists():raise FileExistsError(outpath)
 model=models.make(kind);model.load_state_dict(load_file(str(checkpoint)));model.eval()
 matcher=models.make('binder');matcher.load_state_dict(load_file(str(binder_path)));matcher.eval()
 mh=c.weights_hash(model);bh=c.weights_hash(matcher);t=time.perf_counter();rows=[];arrays={};counts={'configs':0,'predictions':0};query_seconds=0.0;b=128 if not small else 32
 def record(name,p,k,v,e,q=None,cycle=False):
  nonlocal query_seconds
  rt=time.perf_counter()
  codes=torch.from_numpy(p['codes']);q=torch.from_numpy(p['q']) if q is None else q
  out=model(k,v,e,q,8,cycle=True) if cycle else model(k,v,e,q,8);pred=models.logits(out,codes).argmax(-1).numpy()
  query_seconds+=time.perf_counter()-rt
  key=f'c{counts["configs"]:04d}';counts['configs']+=1
  arrays[key+'_pred']=pred[:,[0,1,3,7]].astype(np.int16)
  arrays[key+'_parent']=p['parent'].astype(np.int16);arrays[key+'_query']=p['query'].astype(np.int16);arrays[key+'_rooms']=p['rooms'].astype(np.int16)
  for j,depth in enumerate(DEPTHS):
   r={'case':name,'key':key,'kind':kind,'seed':seed,'depth':depth};r.update(metrics(pred[:,depth-1],p,depth,'cycled_hop4' if cycle else kind));rows.append(r);counts['predictions']+=b
 # A: exact visible current facts; depths and path lengths held separately.
 for h in [1,2,4,6,8]:
  for missing in [False,True]:
   p=data.batch(np.random.default_rng(source_seed(seed,h,missing)),b,max_h=h,hops=h,missing=missing)
   k,v,e,q,book=data.tensors(p);record(f'visible/h{h}/missing{int(missing)}',p,k,v,e)
 # B/C: same problem held through unrelated valid/denied/out-of-scope events.
 for h in [1,4,8]:
  for missing in [False,True]:
   for horizon in [0,64,1024]:
    rng=np.random.default_rng(source_seed(seed,h,missing,100));p=data.batch(rng,b,max_h=h,hops=h,missing=missing)
    st=install(p,matcher);distract(st,p,rng,horizon)
    k,v,e=st.snapshot();record(f'stream/h{h}/missing{int(missing)}/delay{horizon}/on',p,k,v,e)
    record(f'stream/h{h}/missing{int(missing)}/delay{horizon}/off',p,torch.zeros_like(k),torch.zeros_like(v),torch.zeros_like(e))
 # Lifecycle: correction/clear/rewrite after 64 distractors at each stage.
 rng=np.random.default_rng(source_seed(seed,4,False,200));p=data.batch(rng,b,max_h=4,hops=4,missing=False)
 st=install(p,matcher);rr=np.arange(b);focus=p['order'][:,2];original=p['parent'][rr,focus].copy()
 phases=[('initial',None),('correction',p['rooms'][:,1]),('clear',np.full(b,16)),('rewrite',original)]
 for name,dest in phases:
  if dest is not None:
   val=torch.from_numpy(p['codes'][rr,dest]);src=torch.from_numpy(p['codes'][rr,focus]);op=-1 if name=='clear' else 1
   st.event(src,val,op);p['parent'][rr,focus]=dest
  distract(st,p,rng,64)
  record(f'lifecycle/{name}',p,*st.snapshot())
 # Exact empty reset, followed by fresh data in the same object.
 st.clear_all();p['parent'][:,:]=16;record('lifecycle/global_reset',p,*st.snapshot())
 fresh=data.batch(rng,b,max_h=4,hops=4,missing=False)
 newst=install(fresh,matcher);record('lifecycle/new_scope_fresh_records',fresh,*newst.snapshot())
 # Perturbations and interface shifts. No silent repair or gold reconstruction.
 for case,noise in [('query_noise05',.05),('query_noise20',.2)]:
  p=data.batch(np.random.default_rng(source_seed(seed,4,False,300)),b,max_h=4,hops=4,missing=False,query_noise=noise)
  record('stress/'+case,p,*data.tensors(p)[:3])
 for sigma in [.02,.08]:
  rng=np.random.default_rng(source_seed(seed,4,False,400));p=data.batch(rng,b,max_h=4,hops=4,missing=False)
  st=install(p,matcher);distract(st,p,rng,64,sigma)
  record(f'stress/chronic_noise{sigma}',p,*st.snapshot())
 # Larger record set: novel count with same 17-D identity geometry.
 for hh in [4,8]:
  for missing in [False,True]:
   p=data.batch(np.random.default_rng(source_seed(seed,hh,missing,500)),b,n=32,max_h=hh,hops=hh,missing=missing)
   record(f'stress/n32/h{hh}/missing'+str(int(missing)),p,*data.tensors(p)[:3])
 # Permutations and wrong associations are causal tests, not new training.
 p=data.batch(np.random.default_rng(source_seed(seed,4,False,600)),b,max_h=4,hops=4,missing=False)
 k,v,e,_,_=data.tensors(p);record('intervention/base',p,k,v,e)
 record('intervention/reverse_slots',p,k.flip(1),v.flip(1),e.flip(1))
 record('intervention/shuffle_values',p,k,v.roll(1,1),e)
 record('intervention/no_evidence',p,k*0,v*0,e&False)
 # Common orthogonal code rotation preserves identity/relationships, changes coordinates.
 rotation=np.linalg.qr(np.random.default_rng(89001).normal(size=(16,16)))[0].astype(np.float32)
 pp=copy.deepcopy(p)
 for name in ['codes','keys','vals','q']:pp[name][...,:16]=pp[name][...,:16]@rotation
 record('intervention/rotate_all_codes',pp,*data.tensors(pp)[:3])
 if kind=='untied_hop4':
  for hh in [1,4,8]:
   for missing in [False,True]:
    p=data.batch(np.random.default_rng(source_seed(seed,hh,missing)),b,max_h=hh,hops=hh,missing=missing)
    record(f'intervention/cycled4/h{hh}/missing{int(missing)}',p,*data.tensors(p)[:3],cycle=True)
 assert c.weights_hash(model)==mh and c.weights_hash(matcher)==bh
 outdir=Path(outdir);outdir.mkdir(parents=True,exist_ok=True);name=f'{kind}_{seed}'
 np.savez_compressed(outdir/(name+'.npz'),**arrays)
 result={'kind':kind,'seed':seed,'rows':rows,'counts':counts,'seconds':time.perf_counter()-t,'weights_unchanged':True,'model_weight_hash':mh,'binder_weight_hash':bh,'prediction_sha256':c.sha(outdir/(name+'.npz')),'batch_size':b,'query_compute_seconds':query_seconds}
 c.dump(outdir/(name+'.json'),result);return result

if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--kind',required=True);a.add_argument('--seed',type=int,required=True);a.add_argument('--checkpoint',required=True);a.add_argument('--binder',required=True);a.add_argument('--outdir',required=True);a.add_argument('--small',action='store_true');p=a.parse_args();c.setup(p.seed);r=evaluate(p.kind,p.seed,p.checkpoint,p.binder,p.outdir,p.small);print(r['counts'],r['seconds'])
