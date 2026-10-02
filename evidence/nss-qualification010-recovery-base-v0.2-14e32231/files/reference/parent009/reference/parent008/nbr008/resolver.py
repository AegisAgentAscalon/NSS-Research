"""Pre-projection selective membership. Never receives origin, noise or truth.

The protected reference contains symbol codes, not relation facts. UNKNOWN is a
separate exact sentinel. Gate features are invariant to reference-row ordering.
"""
from dataclasses import dataclass
import torch
from torch import nn
from torch.nn import functional as F
D=17
ABI='nbr008-membership-v1'

class MatchHead(nn.Module):
    def __init__(self):
        super().__init__()
        self.net=nn.Sequential(nn.Linear(8,24),nn.Tanh(),nn.Linear(24,16),nn.Tanh(),nn.Linear(16,1))
    def forward(self,f):return self.net(f).squeeze(-1)

def features(x,book,active):
    """x B,M,17; book B,C,17; active B,C. No UNKNOWN row in book."""
    dot=torch.einsum('bmd,bcd->bmc',x,book)
    x2=x.square().sum(-1);b2=book.square().sum(-1)
    d=(x2[...,None]+b2[:,None,:]-2*dot).clamp_min(0)
    d=d.masked_fill(~active[:,None,:],1e6)
    vals,indices=d.topk(2,largest=False,dim=-1)
    norm=x2.sqrt();count=active.sum(-1)[:,None].expand_as(norm)
    picked=book[torch.arange(len(x))[:,None],indices[...,0]]
    sim=(x*picked).sum(-1)/(norm.clamp_min(1e-8)*picked.norm(dim=-1).clamp_min(1e-8))
    cos=(dot/(norm[...,None].clamp_min(1e-8)*b2.sqrt()[:,None,:].clamp_min(1e-8))).masked_fill(~active[:,None,:],-2)
    cs=cos.topk(2,dim=-1).values
    margin=torch.where(count>=2,vals[...,1]-vals[...,0],torch.ones_like(norm)*4)
    f=torch.stack([vals[...,0].clamp(max=8),margin.clamp(max=4),sim,cs[...,0]-cs[...,1],norm.clamp(max=4),x[...,-1].clamp(-2,2),count/16,cs[...,0]],-1)
    return f,indices[...,0]

@dataclass
class Decision:
    value:torch.Tensor
    accept:torch.Tensor
    index:torch.Tensor
    feat:torch.Tensor
    score:torch.Tensor
    status:torch.Tensor # 0=MATCH,1=NO_SUPPORTED_MATCH,2=UNKNOWN_SENTINEL

class Resolver:
    def __init__(self,method,params=None,head=None,restorer=None):
        self.method=method;self.params=params or {};self.head=head;self.restorer=restorer
        self.calls=0;self.items=0
    @property
    def selective(self):return self.method.startswith(('A_','B_','distance_','margin_')) or self.method=='reject_all'
    def __call__(self,x,book,active):
        if x.ndim!=3 or x.shape[-1]!=17 or book.ndim!=3 or book.shape[-1]!=17 or active.shape!=book.shape[:2]:raise ValueError('Invalid representation shapes')
        if book.shape[1]<2:raise ValueError('Allocated reference needs >=2 rows')
        if not torch.isfinite(x).all() or not torch.isfinite(book).all():raise ValueError('INVALID_REFERENCE or nonfinite input')
        self.calls+=1;self.items+=x.shape[0]*x.shape[1]
        f,idx=features(x,book,active)
        count=active.sum(-1)[:,None]
        # Preserve the parent ABI's explicit UNKNOWN competitor; small soft
        # null readouts must not be forced into a registered symbol.
        null_distance=x[...,:16].square().sum(-1)+(x[...,-1]-1).square()
        sentinel=null_distance<=f[...,0]
        erased=x.square().sum(-1)<1e-12
        accept=(count>0)&~sentinel&~erased
        score=-f[...,0]
        if self.method.startswith('A_'):
            accept &= (f[...,0]<=self.params['distance'])&(f[...,1]>=self.params['margin'])
        elif self.method.startswith('distance_'):accept &= f[...,0]<=self.params['distance']
        elif self.method.startswith('margin_'):accept &= f[...,1]>=self.params['margin']
        elif self.method.startswith('B_'):
            if self.head is None:raise ValueError('Missing head')
            score=self.head(f).sigmoid();accept &= score>=self.params['threshold']
        elif self.method=='reject_all':accept &= False
        elif self.method not in ('none','normalize','nearest','learned'):
            raise ValueError(self.method)
        if self.method in ('none','normalize'):
            val=x if self.method=='none' else F.normalize(x,dim=-1)
        elif self.method in ('learned','A_learned','B_learned'):
            if self.restorer is None:raise ValueError('Missing frozen restorer')
            sentinel_code=torch.zeros((len(x),1,17),dtype=x.dtype);sentinel_code[:,:,-1]=1
            full=torch.cat([book,sentinel_code],1)
            lg=self.restorer.logits(x,full)
            mask=torch.cat([active,torch.ones((len(x),1),dtype=torch.bool)],1)
            lg=lg.masked_fill(~mask[:,None,:],-1e6)
            val=F.normalize(torch.einsum('bmc,bcd->bmd',lg.softmax(-1),full),dim=-1)
        else:val=book[torch.arange(len(x))[:,None],idx]
        # Rejecting a stored field is NOT equivalent to clearing it: caller keeps raw.
        val=torch.where(accept[...,None],val,x)
        status=torch.where(sentinel,torch.full_like(idx,2),torch.where(accept,torch.zeros_like(idx),torch.ones_like(idx)))
        return Decision(val,accept,torch.where(accept,idx,torch.full_like(idx,-1)),f,score,status)
