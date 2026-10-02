"""New compatible GRU; no historical model loading and no labels in state inputs."""
from __future__ import annotations
import random,numpy as np,torch
from torch import nn
from common import CFG,seed,arrhash
NAMES=['cell.weight_ih','cell.weight_hh','cell.bias_ih','cell.bias_hh','head.weight','head.bias']
def setup():
    torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
    torch.set_default_dtype(torch.float32);torch.manual_seed(0);np.random.seed(0);random.seed(0)
    if torch.__version__!=CFG['torch'] or np.__version__!=CFG['numpy']:raise RuntimeError('NUMERIC_HOST_CHANGED')
class Net(nn.Module):
    def __init__(self):
        super().__init__();self.cell=nn.GRUCell(16,64);self.head=nn.Linear(64,9)
    def weights(self):return {k:self.state_dict()[k].detach().numpy().copy() for k in NAMES}
    def ident(self):return arrhash(self.weights())
    def roll(self,events,h=None):
        a=np.asarray(events);a=a[None,:] if a.ndim==1 else a
        t=torch.from_numpy(a.astype(np.int64));valid=t<16
        x=torch.nn.functional.one_hot(t.clamp(0,15),16).float()*valid[...,None]
        h=torch.zeros(len(a),64) if h is None else h
        hist=[]
        for i in range(a.shape[1]):
            proposed=self.cell(x[:,i],h);h=torch.where(valid[:,i,None],proposed,h);hist.append(h)
        states=torch.stack(hist,dim=1);return states,self.head(states)
    def flat(self):return torch.cat([p.detach().reshape(-1) for p in self.parameters()]).numpy().copy()
    def setflat(self,a):
        j=0
        with torch.no_grad():
            for p in self.parameters():n=p.numel();p.copy_(torch.from_numpy(a[j:j+n].reshape(tuple(p.shape)).copy()));j+=n
        assert j==16329

def init(name):
    m=Net();g=torch.Generator();g.manual_seed(seed('init/'+str(name)))
    with torch.no_grad():
        for p in m.parameters():p.uniform_(-.125,.125,generator=g)
    assert sum(p.numel() for p in m.parameters())==CFG['parameters']
    return m,g

def load(weights):
    m=Net();m.load_state_dict({k:torch.from_numpy(v.copy()) for k,v in weights.items()});return m

def a_loss(out,bits,nxt):
    return torch.nn.functional.binary_cross_entropy_with_logits(out[...,:4],torch.from_numpy(bits))+torch.nn.functional.cross_entropy(out[...,4:].reshape(-1,5),torch.from_numpy(nxt).reshape(-1))

def b_loss(out,target):return torch.nn.functional.binary_cross_entropy_with_logits(out[:,-1,0],torch.from_numpy(np.asarray(target,np.float32)))

def sgd(m,loss,lr):
    m.zero_grad(set_to_none=True);loss.backward()
    grad=torch.cat([p.grad.reshape(-1) for p in m.parameters()]);norm=torch.linalg.vector_norm(grad)
    if not torch.isfinite(norm):raise RuntimeError('NONFINITE_GRAD')
    factor=torch.clamp(torch.tensor(1.,dtype=torch.float32)/(norm+1e-6),max=1.)
    product=(grad*factor)*lr
    pre=m.flat();post=(torch.from_numpy(pre)-product.detach()).numpy().copy();m.setflat(post)
    return pre,grad.detach().numpy().copy(),post,np.array([float(loss.detach()),float(norm),float(factor),lr],np.float64),product.detach().numpy().copy()
