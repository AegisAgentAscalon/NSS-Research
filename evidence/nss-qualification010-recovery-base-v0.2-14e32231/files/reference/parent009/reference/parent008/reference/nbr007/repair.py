"""Compatible restorers for the 17-dimensional identity ABI of BindingDepth006.

A dictionary contains identity symbols, never relations, presence or answers.
Its protection/access is explicit and shared by dictionary-based controls.
Masks enforce empty record maintenance, not learned qualification.
"""
import torch
from torch import nn
from torch.nn import functional as F
D=17
class DictionaryRepair(nn.Module):
    """Permutation-equivariant learned candidate scores + soft code retrieval.

    No canonical index is passed at inference. Normalizing nonzero mixtures is
    explicit scaffold. Training targets identify a clean symbol; no path labels.
    """
    def __init__(self):
        super().__init__()
        self.score=nn.Sequential(nn.Linear(5,32),nn.Tanh(),nn.Linear(32,1))
    def logits(self,x,book):
        # x: batch,items,17; book: batch,identities+UNKNOWN,17
        dot=torch.einsum('bmd,bnd->bmn',x,book)
        x2=x.square().sum(-1,keepdim=True).expand_as(dot)
        c2=book.square().sum(-1)[:,None,:].expand_as(dot)
        flags=book[:,:,-1][:,None,:].expand_as(dot)
        marker=x[:,:,-1,None].expand_as(dot)
        feat=torch.stack([dot,x2,c2,flags,marker],-1)
        return self.score(feat).squeeze(-1)
    def forward(self,x,book):
        p=self.logits(x,book).softmax(-1)
        return F.normalize(torch.einsum('bmn,bnd->bmd',p,book),dim=-1)
class IntrinsicRepair(nn.Module):
    """Unconditioned residual denoiser; no access to the episode dictionary."""
    def __init__(self):
        super().__init__()
        self.delta=nn.Sequential(nn.Linear(D,64),nn.Tanh(),nn.Linear(64,D))
        nn.init.zeros_(self.delta[-1].weight);nn.init.zeros_(self.delta[-1].bias)
    def forward(self,x,book=None):
        return F.normalize(x+self.delta(x),dim=-1)
def make(kind):
    if kind=='learned_dictionary':return DictionaryRepair()
    if kind=='intrinsic_mlp':return IntrinsicRepair()
    raise ValueError(kind)
def apply(kind,x,book,model=None):
    if kind=='none':return x
    if kind=='normalize':return F.normalize(x,dim=-1)
    if kind=='nearest':
        dist=(x.square().sum(-1,keepdim=True)+book.square().sum(-1)[:,None,:]-2*torch.einsum('bmd,bnd->bmn',x,book))
        idx=dist.argmin(-1)
        # A completely erased vector carries no symbol: explicitly abstain.
        idx=torch.where(x.square().sum(-1)<1e-12,torch.full_like(idx,book.shape[1]-1),idx)
        return book[torch.arange(len(x))[:,None],idx]
    if model is None:raise ValueError('Learned candidate requires a model')
    return model(x,book)
def maintain(keys,vals,present,book,kind,model=None,fields='both'):
    if fields not in ('keys','values','both','none'):raise ValueError(fields)
    if fields in ('keys','both'):
        keys=apply(kind,keys,book,model)*present[...,None]
    if fields in ('values','both'):
        vals=apply(kind,vals,book,model)*present[...,None]
    return keys,vals
