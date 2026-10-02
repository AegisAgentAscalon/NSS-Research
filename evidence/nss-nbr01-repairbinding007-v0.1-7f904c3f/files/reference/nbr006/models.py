"""Actual trainable readers; no integer-ID matching or graph traversal here.

The record-hop has a deliberately strong key/value inductive bias. All methods
are supplied encoded source/target fields and supervised intermediate targets.
These small variants are NOT reproductions of full MemN2N/Universal Transformer.
"""
import math
import torch
from torch import nn
from torch.nn import functional as F
from .data import D

class Matcher(nn.Module):
 def __init__(self):
  super().__init__();self.q=nn.Linear(D,24,bias=False);self.k=nn.Linear(D,24,bias=False)
  self.log_scale=nn.Parameter(torch.tensor(math.log(12.0)));self.threshold=nn.Parameter(torch.tensor(.4))
 def forward(self,q,keys,present):
  a=F.normalize(self.q(q),dim=-1);b=F.normalize(self.k(keys),dim=-1)
  sim=torch.einsum('bd,bnd->bn',a,b)
  logits=(sim-self.threshold)*self.log_scale.exp().clamp(max=80)
  logits=logits.masked_fill(~present,-1e4)
  return torch.cat([logits,torch.zeros_like(logits[:,:1])],-1)

class RecordHop(nn.Module):
 def __init__(self,gated=False):
  super().__init__();self.match=Matcher();self.gated=gated
  if gated:self.gru=nn.GRUCell(D,D)
 def forward(self,keys,vals,present,q,depth=4):
  empty=torch.zeros_like(q);empty[:,-1]=1
  values=torch.cat([vals,empty[:,None,:]],1);h=q;out=[]
  for _ in range(depth):
   w=self.match(h,keys,present).softmax(-1)
   read=torch.einsum('bn,bnd->bd',w,values)
   h=F.normalize(self.gru(read,h) if self.gated else read,dim=-1)
   out.append(h)
  return torch.stack(out,1)

class UntiedHop(nn.Module):
 """Four independently trained content-attention stages; no eight-stage fiction."""
 def __init__(self):
  super().__init__();self.blocks=nn.ModuleList([Matcher() for _ in range(4)])
 def forward(self,keys,vals,present,q,depth=4,cycle=False):
  empty=torch.zeros_like(q);empty[:,-1]=1
  values=torch.cat([vals,empty[:,None,:]],1);h=q;out=[]
  for j in range(depth if cycle else min(depth,4)):
   weights=self.blocks[j%4](h,keys,present).softmax(-1)
   h=F.normalize(torch.einsum('bn,bnd->bd',weights,values),dim=-1);out.append(h)
  while len(out)<depth:out.append(out[-1])
  return torch.stack(out,1)

class AttentionBlock(nn.Module):
 def __init__(self,width=32):
  super().__init__()
  self.att=nn.MultiheadAttention(width,2,dropout=0.,batch_first=True)
  self.norm1=nn.LayerNorm(width);self.norm2=nn.LayerNorm(width)
  self.ff=nn.Sequential(nn.Linear(width,width*2),nn.GELU(),nn.Linear(width*2,width))
 def forward(self,h,k,v,mask):
  a=self.att(h[:,None,:],k,v,key_padding_mask=mask,need_weights=False)[0][:,0,:]
  h=self.norm1(h+a);return self.norm2(h+self.ff(h))

class AttentionReader(nn.Module):
 def __init__(self,tied=True):
  super().__init__();self.tied=tied
  self.q_in=nn.Linear(D,32);self.k_in=nn.Linear(D,32);self.v_in=nn.Linear(D,32)
  self.out=nn.Linear(32,D);self.blocks=nn.ModuleList([AttentionBlock() for _ in range(1 if tied else 4)])
  self.null_key=nn.Parameter(torch.randn(D)*.1)
 def forward(self,keys,vals,present,q,depth=4):
  b=len(q);null=torch.zeros_like(q);null[:,-1]=1
  k=self.k_in(torch.cat([keys,self.null_key[None,None,:].expand(b,1,-1)],1))
  v=self.v_in(torch.cat([vals,null[:,None,:]],1))
  mask=~torch.cat([present,torch.ones((b,1),dtype=torch.bool,device=q.device)],1)
  h=self.q_in(q);out=[]
  actual=depth if self.tied else min(depth,4)
  for j in range(actual):
   h=self.blocks[0 if self.tied else j](h,k,v,mask)
   out.append(F.normalize(self.out(h),dim=-1))
  while len(out)<depth:out.append(out[-1])
  return torch.stack(out,1)

class AlignedAttentionReader(AttentionReader):
 """Explicit code-space bottleneck between standard cross-attention blocks.

 Every output is re-encoded with the SAME q_in used for the initial query.
 This is a development-selected interface variant, not a silent fix to old fits.
 """
 def forward(self,keys,vals,present,q,depth=4):
  b=len(q);null=torch.zeros_like(q);null[:,-1]=1
  k=self.k_in(torch.cat([keys,self.null_key[None,None,:].expand(b,1,-1)],1))
  v=self.v_in(torch.cat([vals,null[:,None,:]],1))
  mask=~torch.cat([present,torch.ones((b,1),dtype=torch.bool,device=q.device)],1)
  code=q;out=[];actual=depth if self.tied else min(depth,4)
  for j in range(actual):
   h=self.blocks[0 if self.tied else j](self.q_in(code),k,v,mask)
   code=F.normalize(self.out(h),dim=-1);out.append(code)
  while len(out)<depth:out.append(out[-1])
  return torch.stack(out,1)

class FlatGRU(nn.Module):
 def __init__(self):
  super().__init__();self.enc=nn.GRUCell(D*2+1,96);self.init=nn.Linear(96+D,96)
  self.refine=nn.GRUCell(D+96,96);self.out=nn.Linear(96,D)
 def forward(self,keys,vals,present,q,depth=4):
  h=torch.zeros((len(q),96),device=q.device)
  for j in range(keys.shape[1]):
   x=torch.cat([keys[:,j],vals[:,j],present[:,j,None].float()],-1)
   new=self.enc(x,h);h=torch.where(present[:,j,None],new,h)
  memory=h;z=torch.tanh(self.init(torch.cat([memory,q],-1)));out=[]
  for _ in range(depth):
   z=self.refine(torch.cat([memory,q],-1),z);out.append(F.normalize(self.out(z),dim=-1))
  return torch.stack(out,1)

def make(kind):
 if kind=='record_hop':return RecordHop()
 if kind=='gated_hop':return RecordHop(True)
 if kind=='untied_hop4':return UntiedHop()
 if kind=='tied_attention':return AttentionReader(True)
 if kind=='fixed_attention4':return AttentionReader(False)
 if kind=='tied_aligned':return AlignedAttentionReader(True)
 if kind=='fixed_aligned4':return AlignedAttentionReader(False)
 if kind=='flat_gru':return FlatGRU()
 if kind=='binder':return Matcher()
 raise ValueError(kind)

def logits(out,codes):return torch.einsum('btd,bnd->btn',out,codes)*18.0
