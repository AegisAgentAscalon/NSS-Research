import argparse,time,json,resource
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from . import common as c
from . import data,models

def fit(kind,seed,steps,path,development=False,batchsize=64):
 c.setup(seed);rng=np.random.default_rng(seed+100000);model=models.make(kind)
 optimizer=torch.optim.AdamW(model.parameters(),lr=.002,weight_decay=1e-4)
 start=c.utc();t=time.perf_counter();initial=c.weights_hash(model);history=[]
 for step in range(steps):
  optimizer.zero_grad(set_to_none=True)
  if kind=='binder':
   p=data.batch(rng,batchsize,max_h=4)
   keys,vals,present,q,codes=data.tensors(p)
   j=rng.integers(0,keys.shape[1],batchsize);new=rng.random(batchsize)<.4
   q=keys[torch.arange(batchsize),torch.from_numpy(j)].clone()
   target=j.copy();absent=~p['present'][np.arange(batchsize),j];new|=absent
   q[new]=torch.from_numpy(data.normalize(rng.normal(size=(new.sum(),data.D))).astype(np.float32))
   target[new]=keys.shape[1]
   q[:,:16]+=.015*torch.randn_like(q[:,:16]);q=F.normalize(q,dim=-1)
   pred=model(q,keys,present);loss=F.cross_entropy(pred,torch.from_numpy(target))
  else:
   p=data.batch(rng,batchsize,max_h=4)
   keys,vals,present,q,codes=data.tensors(p)
   depth=[1,2,4][step%3];out=model(keys,vals,present,q,depth)
   target=torch.from_numpy(data.targets(p,depth));pred=models.logits(out,codes)
   loss=F.cross_entropy(pred.flatten(0,1),target.flatten())
   correctvec=codes[torch.arange(batchsize)[:,None],target]
   loss=loss+.25*(out-correctvec).square().sum(-1).mean()
  if not torch.isfinite(loss):raise RuntimeError('nonfinite training loss')
  loss.backward();torch.nn.utils.clip_grad_norm_(model.parameters(),1.0);optimizer.step()
  if step==0 or (step+1)%100==0 or step==steps-1:
   r={'step':step+1,'loss':float(loss.detach()),'seconds':time.perf_counter()-t};history.append(r)
   print(kind,seed,r,flush=True)
 path=Path(path);c.save_model(path,model)
 result={'kind':kind,'seed':seed,'steps':steps,'batch':batchsize,'development':development,'start_utc':start,'end_utc':c.utc(),'training_seconds':time.perf_counter()-t,'parameters':sum(p.numel() for p in model.parameters()),'initial_weight_hash':initial,'final_weight_hash':c.weights_hash(model),'checkpoint_sha256':c.sha(path),'changed':initial!=c.weights_hash(model),'history':history,'rss_max_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'env':c.env(),'recipe':{'lr':.002,'optimizer':'AdamW','weight_decay':1e-4,'training_depths':[1,2,4],'max_chain':4,'intermediate_targets':True,'data_seed':seed+100000}}
 c.dump(path.with_suffix('.json'),result);return result

def main():
 p=argparse.ArgumentParser();p.add_argument('--kind',required=True);p.add_argument('--seed',type=int,required=True);p.add_argument('--steps',type=int,default=1200);p.add_argument('--out',required=True);p.add_argument('--development',action='store_true');a=p.parse_args();fit(a.kind,a.seed,a.steps,a.out,a.development)
if __name__=='__main__':main()
