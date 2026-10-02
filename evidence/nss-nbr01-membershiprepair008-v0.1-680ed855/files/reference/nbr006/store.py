"""Scoped bounded record state; fixed-weight learned content-based slot selector.

Ground-truth integer entity IDs never enter this class. Only numeric source and
value codes plus explicit write/clear/scope qualification are supplied. The
allocator, presence field and full-vector write are engineered infrastructure.
No optimizer is used and model parameters are never mutated by write operations.
"""
from pathlib import Path
import json
import numpy as np
import torch
from . import common as c
from .data import D
ABI='nbr006-record-v1'

class RecordStore:
 def __init__(self,batch,capacity,matcher,scope='study'):
  if batch<=0 or capacity<=0:raise ValueError('Positive dimensions required')
  self.keys=torch.zeros(batch,capacity,D);self.vals=torch.zeros_like(self.keys)
  self.present=torch.zeros(batch,capacity,dtype=torch.bool)
  self.matcher=matcher;self.scope=scope;self.events=0
  self.weight_identity=c.weights_hash(matcher)
 @property
 def bytes(self):return sum(x.numel()*x.element_size() for x in [self.keys,self.vals,self.present])
 def snapshot(self):return self.keys.clone(),self.vals.clone(),self.present.clone()
 def clear_all(self):self.keys.zero_();self.vals.zero_();self.present.zero_()
 @torch.no_grad()
 def event(self,src,val,operation,qualified=True,scope='study'):
  b,s,_=self.keys.shape;self.events+=1
  if src.shape!=(b,D) or val.shape!=(b,D):raise ValueError('Input shape mismatch')
  if not torch.isfinite(src).all() or not torch.isfinite(val).all():raise ValueError('Nonfinite event')
  op=torch.as_tensor(operation,dtype=torch.int64).expand(b)
  allowed=torch.as_tensor(qualified,dtype=torch.bool).expand(b)&(scope==self.scope)&(op!=0)
  if not ((op==0)|(op==1)|(op==-1)).all():raise ValueError('Unknown operation')
  # Returns selected physical slot, or capacity for not found. No IDs or oracle.
  selected=self.matcher(src,self.keys,self.present).argmax(-1)
  free=(~self.present).to(torch.int64).argmax(-1);has_free=(~self.present).any(-1)
  existing=selected<s
  targets=torch.where(existing,selected,free)
  canwrite=allowed&(op==1)&(existing|has_free)
  canclear=allowed&(op==-1)&existing
  r=torch.arange(b)
  fresh=canwrite&(~existing)
  self.keys[r[fresh],targets[fresh]]=src[fresh]
  self.vals[r[canwrite],targets[canwrite]]=val[canwrite]
  self.present[r[canwrite],targets[canwrite]]=True
  self.keys[r[canclear],targets[canclear]]=0
  self.vals[r[canclear],targets[canclear]]=0
  self.present[r[canclear],targets[canclear]]=False
  return {'selected':selected,'written':canwrite,'cleared':canclear,'capacity_rejected':allowed&(op==1)&~existing&~has_free}
 def perturb(self,rng,sigma,include_keys=True):
  if sigma<0:raise ValueError('Negative noise')
  if sigma:
   for x in ([self.keys,self.vals] if include_keys else [self.vals]):
    x.add_(torch.from_numpy(rng.normal(0,sigma,x.shape).astype(np.float32))*self.present[:,:,None])
 def save(self,path,rng):
  if c.weights_hash(self.matcher)!=self.weight_identity:raise ValueError('Changed matcher weights')
  path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
  np.savez_compressed(path,keys=self.keys.numpy(),vals=self.vals.numpy(),present=self.present.numpy())
  c.dump(path.with_suffix('.json'),{'abi':ABI,'scope':self.scope,'events':self.events,'shape':list(self.keys.shape),'weight_identity':self.weight_identity,'array_sha256':c.sha(path),'rng':rng.bit_generator.state})
 @classmethod
 def load(cls,path,matcher,scope='study'):
  path=Path(path);meta=json.loads(path.with_suffix('.json').read_text())
  if meta['abi']!=ABI or meta['scope']!=scope:raise ValueError('Incompatible scope/ABI')
  if meta['weight_identity']!=c.weights_hash(matcher):raise ValueError('Incompatible learned selector')
  if meta['array_sha256']!=c.sha(path):raise ValueError('Damaged snapshot')
  with np.load(path,allow_pickle=False) as a:
   k,v,e=a['keys'],a['vals'],a['present']
   if list(k.shape)!=meta['shape'] or k.ndim!=3 or k.shape[-1]!=D or v.shape!=k.shape or e.shape!=k.shape[:2]:raise ValueError('Invalid shapes')
   if k.dtype!=np.float32 or v.dtype!=np.float32 or e.dtype!=bool:raise ValueError('Invalid dtypes')
   if not np.isfinite(k).all() or not np.isfinite(v).all():raise ValueError('Nonfinite snapshot')
   obj=cls(k.shape[0],k.shape[1],matcher,scope);obj.keys.copy_(torch.from_numpy(k));obj.vals.copy_(torch.from_numpy(v));obj.present.copy_(torch.from_numpy(e))
  obj.events=meta['events'];rng=np.random.default_rng();rng.bit_generator.state=meta['rng'];return obj,rng
