"""Learned, noise-exposed existence separate from frozen content recurrence.
Four supplied addresses and eight finite value codes. Qualification and write
encoding are exact controlled inputs, not a learned natural-language decision.
No target labels or protected flags are stored in the neural candidates.
"""
from pathlib import Path
import math
import torch
from torch import nn
from safetensors.torch import load_file
from .util import sha,digest_tensors
D=16;KEYS=4;UNKNOWN=8
MODES=('historical','protected','nearest','split1','split4','coupled17','fixed1','fixed4','hold1')
KINDS=('split1','split4','coupled17')

class Representation(nn.Module):
    def __init__(self,checkpoint):
        super().__init__();src=load_file(str(checkpoint),device='cpu')
        self.head=nn.Sequential(nn.LayerNorm(D),nn.Linear(D,32),nn.GELU(),nn.Linear(32,9))
        self.head.load_state_dict({k[5:]:v for k,v in src.items() if k.startswith('head.')},strict=True)
        scale=src['value.weight'].square().mean().sqrt()
        self.register_buffer('scale',scale)
        self.register_buffer('codes',torch.cat((src['value.weight']/scale,torch.zeros(1,D)),0))
        self.source_sha256=sha(checkpoint);self.requires_grad_(False);self.eval()
    def forward(self,z):return self.head(z*self.scale)
    def nearest(self,z):return (z.unsqueeze(-2)-self.codes).square().sum(-1).argmin(-1)

class Repair(nn.Module):
    """Inherited StateRecovery003 map, unchanged and frozen in split arms."""
    def __init__(self):
        super().__init__();self.net=nn.Sequential(nn.Linear(D,64),nn.Tanh(),nn.Linear(64,D))
    def forward(self,z):
        out=.5*z+.5*(self.net(z)-self.net(torch.zeros(D,dtype=z.dtype,device=z.device)))
        return torch.where((z==0).all(-1,keepdim=True),torch.zeros_like(out),out)

class Presence(nn.Module):
    """Learned continuous maintenance. No sign threshold inside this map.
    A sign readout is a declared interface rule, not a protected state variable.
    With width4 the four coordinates are redundant presence code coordinates;
    this extra state and its supervised encoding are accounted for explicitly.
    """
    def __init__(self,width):
        super().__init__()
        if width not in (1,4):raise ValueError('Presence width')
        self.width=width
        self.net=nn.Sequential(nn.Linear(width,16),nn.Tanh(),nn.Linear(16,width))
    def forward(self,p):return .1*p+.9*self.net(p)

class Coupled(nn.Module):
    """Equal-state-budget dense challenger to split1: 17 floats per record.
    Jointly refits content/existence, initialized from the 16-D repair parent.
    """
    def __init__(self,parent=None):
        super().__init__();self.net=nn.Sequential(nn.Linear(17,64),nn.Tanh(),nn.Linear(64,17))
        if parent is not None:
            with torch.no_grad():
                self.net[0].weight[:,:D].copy_(parent.net[0].weight)
                self.net[0].bias.copy_(parent.net[0].bias)
                self.net[0].weight[:,D:].mul_(.05)
                self.net[2].weight[:D].copy_(parent.net[2].weight)
                self.net[2].bias[:D].copy_(parent.net[2].bias)
                self.net[2].weight[D:].mul_(.05);self.net[2].bias[D:].zero_()
    def forward(self,z):return .5*z+.5*(self.net(z)-self.net(torch.zeros(17,dtype=z.dtype,device=z.device)))

def load_components(root,rep_seed,mode,learn_seed=None,checkpoint_dir=None):
    root=Path(root)
    if mode not in MODES:raise ValueError('Unknown mode')
    rep=Representation(root/'reference'/f'soft_slots_wide_seed{rep_seed}.safetensors')
    old=Repair();parent=root/'reference'/f'recurrent_rep{rep_seed}_seed{441 if rep_seed==141 else rep_seed+200}.safetensors'
    old.load_state_dict(load_file(str(parent)),strict=True);old.requires_grad_(False);old.eval()
    new=None
    if mode in KINDS:
        new=Coupled() if mode=='coupled17' else Presence(1 if mode=='split1' else 4)
        directory=Path(checkpoint_dir) if checkpoint_dir is not None else root/'evidence/main'
        ck=directory/f'{mode}_rep{rep_seed}_seed{learn_seed or rep_seed+400}.safetensors'
        new.load_state_dict(load_file(str(ck)),strict=True);new.requires_grad_(False);new.eval()
    return rep,old,new

class Memory:
    def __init__(self,rep,mode,old=None,new=None,batch=64,scope='study'):
        if mode not in MODES:raise ValueError('Unknown mode')
        if old is None and mode!='nearest':raise ValueError('Missing content model')
        if mode in KINDS and new is None:raise ValueError('Missing learned model')
        if type(batch)!=int or not 1<=batch<=4096:raise ValueError('Invalid batch')
        if not isinstance(scope,str) or not scope or len(scope)>200:raise ValueError('Invalid scope')
        self.rep=rep;self.mode=mode;self.old=old;self.new=new;self.scope=scope
        self.z=torch.zeros(batch,KEYS,D)
        self.width=4 if mode in ('split4','fixed4') else (1 if mode in ('split1','coupled17','fixed1','hold1') else 0)
        self.p=-torch.ones(batch,KEYS,self.width) if self.width else None
        self.flag=torch.zeros(batch,KEYS,dtype=torch.bool) if mode=='protected' else None
        self.events=0;self.rounds=0
    def identity(self):
        return dict(schema='existence-content005/state-v1',scope=self.scope,mode=self.mode,shape=list(self.z.shape),presence_width=self.width,
            representation=self.rep.source_sha256,old=digest_tensors(self.old.state_dict()) if self.old else None,
            learned=digest_tensors(self.new.state_dict()) if self.new else None,
            semantics='codes0-7; absent=-1 presence-code; present=+1; read mean(p)>0; exact writes/reset; old states incompatible')
    @torch.no_grad()
    def event(self,op,key=None,value=None,score=1.,scope=None):
        if op not in ('write','clear','clear_all','noop'):raise ValueError('Invalid operation')
        if not isinstance(score,(int,float)) or isinstance(score,bool) or not math.isfinite(score) or not 0<=score<=1:raise ValueError('Invalid score')
        if op in ('write','clear') and (type(key)!=int or not 0<=key<KEYS):raise ValueError('Invalid address')
        if op=='write':
            if type(value)==int:value=torch.full((len(self.z),),value,dtype=torch.long)
            if not torch.is_tensor(value) or value.dtype!=torch.long or value.shape!=(len(self.z),) or not ((value>=0)&(value<8)).all():raise ValueError('Invalid value')
        self.events+=1
        if scope is not None and scope!=self.scope:return False
        if op=='write' and score>=.5:
            self.z[:,key]=self.rep.codes[value]
            if self.p is not None:self.p[:,key]=1.
            if self.flag is not None:self.flag[:,key]=True
            return True
        if op in ('clear','clear_all'):
            s=(slice(None),key) if op=='clear' else (slice(None),slice(None))
            self.z[s]=0.
            if self.p is not None:self.p[s]=-1.
            if self.flag is not None:self.flag[s]=False
            return True
        return False
    @torch.no_grad()
    def maintain(self,content_noise=None,presence_noise=None,guard=True):
        # Validate both buffers before mutating either state.
        for a,b in ((content_noise,self.z),(presence_noise,self.p)):
            if a is not None and (b is None or a.shape!=b.shape or a.dtype!=b.dtype or not torch.isfinite(a).all()):raise ValueError('Invalid noise')
        z=self.z if content_noise is None else self.z+content_noise
        p=self.p if presence_noise is None else self.p+presence_noise
        if self.mode=='coupled17':
            both=self.new(torch.cat((z,p),-1));z,p=both[...,:D],both[...,D:]
        else:
            z=self.rep.codes[self.rep.nearest(z)] if self.mode=='nearest' else self.old(z)
            if self.mode in ('split1','split4'):p=self.new(p)
            elif self.mode in ('fixed1','fixed4'):
                p=torch.where(p.mean(-1,keepdim=True)>0,torch.ones_like(p),-torch.ones_like(p))
        # Identical inferred-status guard for all explicit neural existence arms.
        # This is not protected: an incorrect neural sign can erase a real value.
        # The guard is removed only in named interventions, not primary scoring.
        if guard:
            live=self.flag if self.flag is not None else (p.mean(-1)>0 if p is not None else None)
            if live is not None:z=torch.where(live[...,None],z,torch.zeros_like(z))
        if not torch.isfinite(z).all() or (p is not None and not torch.isfinite(p).all()):raise RuntimeError('Nonfinite state')
        self.z,self.p=z,p;self.rounds+=1
    @torch.no_grad()
    def read(self):
        answers=self.rep(self.z).argmax(-1)
        live=self.flag if self.flag is not None else (self.p.mean(-1)>0 if self.p is not None else None)
        return answers if live is None else torch.where(live,answers,torch.full_like(answers,UNKNOWN))
    @torch.no_grad()
    def existence(self):
        if self.flag is not None:return self.flag.clone()
        if self.p is not None:return self.p.mean(-1)>0
        return self.read()<UNKNOWN
    @torch.no_grad()
    def read_status(self):
        # 0=empty, 1=present/readable, 2=present but reader cannot recover value.
        live=self.existence();answer=self.read()
        return torch.where(live,torch.where(answer<UNKNOWN,1,2),0)
    def raw_state_bytes(self):return sum(x.numel()*x.element_size() for x in (self.z,self.p,self.flag) if x is not None)
