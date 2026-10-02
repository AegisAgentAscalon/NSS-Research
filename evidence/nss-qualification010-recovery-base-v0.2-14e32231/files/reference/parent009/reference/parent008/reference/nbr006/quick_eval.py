import argparse,numpy as np,torch
from safetensors.torch import load_file
from . import models,data,common as c
p=argparse.ArgumentParser();p.add_argument('--kind',required=True);p.add_argument('--checkpoint',required=True);p.add_argument('--seed',type=int,default=8801);a=p.parse_args();c.setup(a.seed)
m=models.make(a.kind);m.load_state_dict(load_file(a.checkpoint));m.eval();r=[]
with torch.no_grad():
 for h in [1,2,4,6,8]:
  for missing in [False,True]:
   rng=np.random.default_rng(a.seed+10*h+int(missing));d=data.batch(rng,256,max_h=h,hops=h,missing=missing)
   k,v,e,q,book=data.tensors(d);out=m(k,v,e,q,8);pred=models.logits(out,book).argmax(-1).numpy();target=data.oracle_answer(d)
   scores=[float(np.mean(pred[:,j-1]==target)) for j in [1,2,4,8]]
   r.append({'hops':h,'missing':missing,'accuracy':scores})
print(r);c.dump(a.checkpoint.replace('.safetensors','.quick.json'),r)
