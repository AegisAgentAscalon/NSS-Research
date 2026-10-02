"""Declared executable read control on the SAME supplied/learned-written records.

Keys use exact numeric bytes, not integer entity IDs or oracle-selected paths.
A corrupted query/key may fail byte lookup. No fuzzy-match rule is invented here.
The streaming writer remains the same frozen learned binder, so this is not an
independent protected exact archive. Visible input conditions are exact records.
"""
import argparse
from pathlib import Path
import numpy as np
import torch
from torch import nn
from . import models,common as c
from .eval import evaluate
class ExactReader(nn.Module):
 def __init__(self):super().__init__();self.register_buffer('version',torch.tensor(1,dtype=torch.int64))
 def forward(self,keys,vals,present,q,depth=4):
  key=keys.detach().numpy();val=vals.detach().numpy();live=present.numpy();qq=q.numpy()
  out=np.zeros((len(q),depth,q.shape[-1]),dtype=np.float32);null=np.zeros(q.shape[-1],dtype=np.float32);null[-1]=1
  for b in range(len(q)):
   table={key[b,j].tobytes():val[b,j].copy() for j in range(keys.shape[1]) if live[b,j]}
   current=qq[b].copy()
   for t in range(depth):
    current=table.get(current.tobytes(),null);out[b,t]=current
  return torch.from_numpy(out)

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seed',type=int,required=True);p.add_argument('--outdir',required=True);a=p.parse_args();c.setup(a.seed)
 original=models.make
 models.make=lambda kind:ExactReader() if kind=='exact_lookup' else original(kind)
 ckpt=c.ROOT/'spec/exact_control.safetensors'
 if not ckpt.exists():c.save_model(ckpt,ExactReader())
 r=evaluate('exact_lookup',a.seed,ckpt,c.ROOT/'checkpoints'/f'binder_{a.seed}.safetensors',a.outdir)
 print(r['counts'],r['seconds'])
