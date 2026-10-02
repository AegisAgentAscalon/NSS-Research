"""Synthetic corruption and actual qualified-write events, with paired RNG.
No targets are passed to a candidate during recovery. Fault amplitudes are in
RMS-normalized source-embedding coordinates, not a physiological unit.
"""
import torch
from .models import UNKNOWN,D,KEYS

def labels(g,n,keys=KEYS):
    y=torch.arange(n*keys).remainder(9)
    return y[torch.randperm(len(y),generator=g)].reshape(n,keys)

def training_batch(rep,g,batch=128):
    # Inputs and all target-code/answer teaching are shared across trainable arms.
    old=torch.randint(0,9,(batch,),generator=g)
    new=torch.randint(0,8,(batch,),generator=g)
    write=torch.rand(batch,generator=g)<.35
    clear=torch.rand(batch,generator=g)<.10
    sigma=torch.tensor([0.,.1,.25,.5])[torch.randint(0,4,(batch,),generator=g)]
    n1=torch.randn(batch,D,generator=g)*sigma[:,None]
    n2=torch.randn(batch,D,generator=g)*sigma[:,None]
    common=torch.rand(batch,generator=g)<.25
    fastonly=torch.rand(batch,generator=g)<.25
    n2=torch.where(common[:,None],n1,n2)
    n2=torch.where(fastonly[:,None],torch.zeros_like(n2),n2)
    erase=torch.rand(batch,D,generator=g)<.20
    doerase=torch.rand(batch,generator=g)<.20
    oldcode=rep.codes[old]
    f=torch.where(doerase[:,None]&erase,torch.zeros_like(oldcode),oldcode)+n1
    s=oldcode+n2
    f=torch.where(clear[:,None],torch.zeros_like(f),f)
    s=torch.where(clear[:,None],torch.zeros_like(s),s)
    # Clear is an exact scope operation, not an observed UNKNOWN write.
    write=write&~clear
    target=torch.where(clear,UNKNOWN,torch.where(write,new,old))
    depth=(1,2,4)[int(torch.randint(0,3,(),generator=g))]
    return dict(f=f,s=s,new=new,write=write,target=target,depth=depth)

def fault(state,kind,level,g,codes,targets):
    a=[x.clone() for x in state]
    n1=torch.randn(a[0].shape,generator=g)
    n2=torch.randn(a[0].shape,generator=g)
    if kind=='clean':return tuple(a)
    if kind=='gaussian':
        return tuple(x+level*n for x,n in zip(a,(n1,n2)))
    if kind=='common_gaussian':return tuple(x+level*n1 for x in a)
    if kind=='fast_gaussian':
        a[0]=a[0]+level*n1;return tuple(a)
    if kind=='coordinate_erase':
        for i,x in enumerate(a):
            mask=torch.rand(x.shape,generator=g)<level
            a[i]=torch.where(mask,torch.zeros_like(x),x)
        return tuple(a)
    if kind=='toward_wrong':
        wrong=(targets+3).remainder(8)
        return tuple((1-level)*x+level*codes[wrong] for x in a)
    if kind=='erase_fast':a[0].zero_();return tuple(a)
    if kind=='erase_all':return tuple(torch.zeros_like(x) for x in a)
    raise ValueError('Unknown fault')

def fault_matrix():
    return [('clean',0.)]+[(k,s) for k,levels in (
        ('gaussian',[.25,.5,1.,1.5]),('common_gaussian',[.5,1.]),
        ('fast_gaussian',[.5,1.]),('coordinate_erase',[.25,.5,.75]),
        ('toward_wrong',[.25,.5,.75])) for s in levels]+[('erase_fast',1.),('erase_all',1.)]
