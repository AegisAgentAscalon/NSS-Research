"""Research-only resumable query iteration; equivalent to locked reader forward.

Weights live in separately verified checkpoints. Working record arrays and query
state, scope and iteration index are persisted; no optimizer state exists here.
"""
from pathlib import Path
import json
import numpy as np
import torch
from torch.nn import functional as F
from . import common as c
from . import models
ABI='nbr006-query-v1'
class QueryRunner:
 def __init__(self,model,kind,keys,vals,present,q,scope='study'):
  self.model=model;self.kind=kind;self.keys=keys.clone();self.vals=vals.clone();self.present=present.clone();self.q=q.clone();self.scope=scope;self.round=0
  self.h=model.q_in(q) if kind in ['tied_attention','fixed_attention4'] else q.clone()
  self.code=q.clone();self.identity=c.weights_hash(model)
 @torch.no_grad()
 def advance(self,n=1):
  if n<0:raise ValueError('Negative rounds')
  for _ in range(n):
   if self.kind in ['untied_hop4','fixed_attention4'] and self.round>=4:
    self.round+=1;continue
   null=torch.zeros_like(self.q);null[:,-1]=1
   if self.kind in ['record_hop','gated_hop','untied_hop4']:
    matcher=self.model.blocks[self.round] if self.kind=='untied_hop4' else self.model.match
    w=matcher(self.h,self.keys,self.present).softmax(-1)
    read=torch.einsum('bn,bnd->bd',w,torch.cat([self.vals,null[:,None,:]],1))
    self.h=F.normalize(self.model.gru(read,self.h) if self.kind=='gated_hop' else read,dim=-1);self.code=self.h
   else:
    b=len(self.q);m=self.model
    k=m.k_in(torch.cat([self.keys,m.null_key[None,None,:].expand(b,1,-1)],1))
    v=m.v_in(torch.cat([self.vals,null[:,None,:]],1));mask=~torch.cat([self.present,torch.ones((b,1),dtype=torch.bool)],1)
    self.h=m.blocks[0 if self.kind=='tied_attention' else self.round](self.h,k,v,mask)
    self.code=F.normalize(m.out(self.h),dim=-1)
   self.round+=1
  return self.code
 def save(self,path):
  if c.weights_hash(self.model)!=self.identity:raise ValueError('Changed serving weights')
  path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
  np.savez_compressed(path,keys=self.keys.numpy(),vals=self.vals.numpy(),present=self.present.numpy(),q=self.q.numpy(),h=self.h.detach().numpy(),code=self.code.detach().numpy())
  c.dump(path.with_suffix('.json'),{'abi':ABI,'scope':self.scope,'kind':self.kind,'round':self.round,'weight_identity':self.identity,'array_sha256':c.sha(path)})
 @classmethod
 def load(cls,path,model,scope='study'):
  path=Path(path);meta=json.loads(path.with_suffix('.json').read_text())
  if meta['abi']!=ABI or meta['scope']!=scope or meta['weight_identity']!=c.weights_hash(model) or meta['array_sha256']!=c.sha(path):raise ValueError('Incompatible query snapshot')
  with np.load(path,allow_pickle=False) as d:
   obj=cls(model,meta['kind'],*[torch.from_numpy(d[k].copy()) for k in ['keys','vals','present','q']],scope=scope)
   obj.h=torch.from_numpy(d['h'].copy());obj.code=torch.from_numpy(d['code'].copy())
  obj.round=meta['round'];return obj
