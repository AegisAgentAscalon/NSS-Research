"""Frozen source representation and an unchanged-size recurrent repair map.

There are four explicit addresses and eight supplied categorical prototypes.
A qualified WRITE installs the full code. EMPTY is code index8 (a zero vector).
This controls update qualification and encoding; it does not learn either.
"""
from pathlib import Path
import math
import torch
from torch import nn
from safetensors.torch import load_file
from .util import sha,digest_tensors
D=16;KEYS=4;UNKNOWN=8
MODES=('hold','historical','replay','contract','presence_historical','presence_contract','local_empty','nearest')

class Representation(nn.Module):
    def __init__(self,checkpoint):
        super().__init__()
        src=load_file(str(checkpoint),device='cpu')
        self.head=nn.Sequential(nn.LayerNorm(D),nn.Linear(D,32),nn.GELU(),nn.Linear(32,9))
        self.head.load_state_dict({k[5:]:v for k,v in src.items() if k.startswith('head.')},strict=True)
        value=src['value.weight'];scale=value.square().mean().sqrt()
        self.register_buffer('scale',scale)
        self.register_buffer('codes',torch.cat((value/scale,torch.zeros(1,D)),0))
        self.source_sha256=sha(checkpoint);self.requires_grad_(False);self.eval()
    def forward(self,z):return self.head(z*self.scale)
    def nearest(self,z):return (z.unsqueeze(-2)-self.codes).square().sum(-1).argmin(-1)

class Repair(nn.Module):
    """Identical 2,128-parameter architecture to StateRecovery003.
    Exact zero is guarded in ALL repair arms, including historical.
    No branch tests the oracle label or a near-zero radius during inference.
    """
    def __init__(self):
        super().__init__();self.net=nn.Sequential(nn.Linear(D,64),nn.Tanh(),nn.Linear(64,D))
    def forward(self,z):
        baseline=self.net(torch.zeros(D,dtype=z.dtype,device=z.device))
        result=.5*z+.5*(self.net(z)-baseline)
        return torch.where((z==0).all(-1,keepdim=True),torch.zeros_like(result),result)

class LocalEmpty(Repair):
    """A continuous local empty-region intervention, not a presence flag.
    F_local(z) = [1-exp(-||z||^2 / radius^2)] * F_parent(z).
    Parent network is frozen. Only one positive radius scalar is fitted.
    No threshold, record label, or persistent metadata enters this map.
    This uses the declared convention EMPTY=0 and known nonzero code scale;
    it is not a representation-independent solution.
    """
    def __init__(self):
        super().__init__()
        self.net.requires_grad_(False)
        self.raw_radius=nn.Parameter(torch.tensor(math.log(math.expm1(1.2-.05))))
    def radius(self):return nn.functional.softplus(self.raw_radius)+.05
    def forward(self,z):
        gain=-torch.expm1(-z.square().sum(-1,keepdim=True)/self.radius().square())
        return gain*super().forward(z)

def load_components(root,rep_seed,mode,learn_seed=None):
    root=Path(root)
    if mode not in MODES:raise ValueError('Unknown mode')
    rep=Representation(root/'reference'/f'soft_slots_wide_seed{rep_seed}.safetensors')
    repair=None
    if mode not in ('hold','nearest'):
        repair=LocalEmpty() if mode=='local_empty' else Repair()
        if mode in ('historical','presence_historical'):
            ck=root/'reference'/f'recurrent_rep{rep_seed}_seed{rep_seed+200}.safetensors'
        else:
            kind='local_empty' if mode=='local_empty' else ('contract' if mode in ('contract','presence_contract') else 'replay')
            ck=root/'evidence/main'/f'{kind}_rep{rep_seed}_seed{learn_seed or rep_seed+300}.safetensors'
        repair.load_state_dict(load_file(str(ck)),strict=True)
        repair.requires_grad_(False);repair.eval()
    return rep,repair

class Memory:
    """Dynamic writable state. No target, true value, or full event ledger is
    retained inside a neural arm. Protected existence flags are kept only by
    explicitly named presence controls; these flags never encode the value.
    """
    def __init__(self,rep,mode,repair=None,batch=64,scope='study'):
        if mode not in MODES:raise ValueError('Unknown mode')
        if mode not in ('hold','nearest') and repair is None:raise ValueError('Missing repair')
        if type(batch)!=int or not 1<=batch<=4096:raise ValueError('Invalid batch')
        if not isinstance(scope,str) or not scope or len(scope)>200:raise ValueError('Invalid scope')
        self.rep=rep;self.mode=mode;self.repair=repair;self.scope=scope
        self.z=torch.zeros(batch,KEYS,D)
        self.presence=torch.zeros(batch,KEYS,dtype=torch.bool) if mode.startswith('presence_') else None
        self.events=0;self.rounds=0
    def identity(self):
        return {'schema':'writable-empty004/state-v1','scope':self.scope,'mode':self.mode,
                'representation':self.rep.source_sha256,
                'repair':digest_tensors(self.repair.state_dict()) if self.repair is not None else None,
                'shape':list(self.z.shape)}
    @torch.no_grad()
    def event(self,op,key=None,value=None,score=1.,scope=None):
        """Supplied clean rule score>=0.5; scope must match. Rejected events are
        genuine no-ops, not tiny writes. Strength of the value code is not scaled
        by score. Clear/write changes content and presence within one call.
        No claim of production crash atomicity or learned admission is made.
        """
        if op not in ('write','clear','clear_all','noop'):raise ValueError('Invalid operation')
        if not isinstance(score,(float,int)) or isinstance(score,bool) or not math.isfinite(score) or not 0<=score<=1:raise ValueError('Invalid score')
        if op in ('write','clear') and (type(key)!=int or not 0<=key<KEYS):raise ValueError('Invalid key')
        if op=='write':
            if type(value)==int:value=torch.full((len(self.z),),value,dtype=torch.long)
            if not torch.is_tensor(value) or value.dtype!=torch.int64 or value.shape!=(len(self.z),) or not ((value>=0)&(value<8)).all():raise ValueError('Invalid value')
        self.events+=1
        if scope is not None and scope!=self.scope:return False
        if op=='write' and score>=.5:
            self.z[:,key]=self.rep.codes[value]
            if self.presence is not None:self.presence[:,key]=True
            return True
        if op=='clear':
            self.z[:,key].zero_()
            if self.presence is not None:self.presence[:,key]=False
            return True
        if op=='clear_all':
            self.z.zero_()
            if self.presence is not None:self.presence.zero_()
            return True
        return False
    @torch.no_grad()
    def maintain(self,noise=None):
        if noise is not None:
            if noise.shape!=self.z.shape or noise.dtype!=self.z.dtype or not torch.isfinite(noise).all():raise ValueError('Invalid noise')
            self.z=self.z+noise
        if self.mode=='nearest':self.z=self.rep.codes[self.rep.nearest(self.z)]
        elif self.mode!='hold':self.z=self.repair(self.z)
        if self.presence is not None:
            self.z=torch.where(self.presence[:,:,None],self.z,torch.zeros_like(self.z))
        if not torch.isfinite(self.z).all():raise RuntimeError('Nonfinite memory')
        self.rounds+=1
    @torch.no_grad()
    def read(self):return self.rep(self.z).argmax(-1)
    def raw_state_bytes(self):
        return self.z.numel()*self.z.element_size()+(self.presence.numel()*self.presence.element_size() if self.presence is not None else 0)
