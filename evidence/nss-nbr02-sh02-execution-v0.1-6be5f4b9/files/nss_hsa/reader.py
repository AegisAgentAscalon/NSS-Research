"""Small typed-maintenance reader; parameter names/shapes are SH01-compatible."""
from __future__ import annotations
import torch
from torch import nn
from .attention import BACKENDS
from .hierarchy import AttentionPlan,HierarchyError

class Block(nn.Module):
    def __init__(self,d:int=32,heads:int=2):
        super().__init__();self.d=d;self.heads=heads
        self.norm1=nn.LayerNorm(d);self.qkv=nn.Linear(d,3*d);self.proj=nn.Linear(d,d)
        self.norm2=nn.LayerNorm(d);self.ff=nn.Sequential(nn.Linear(d,64),nn.GELU(),nn.Linear(64,d))
    def forward(self,x,plan,backend):
        b,t,d=x.shape;y=self.norm1(x)
        q,k,v=self.qkv(y).reshape(b,t,3,self.heads,d//self.heads).permute(2,0,3,1,4).unbind(0)
        a=BACKENDS[backend](q,k,v,plan)
        x=x+self.proj(a.transpose(1,2).reshape(b,t,d))
        return x+self.ff(self.norm2(x))

class MaintenanceReader(nn.Module):
    def __init__(self):
        super().__init__();self.enc=nn.Linear(37,32);self.blocks=nn.ModuleList([Block(),Block()])
        self.norm=nn.LayerNorm(32);self.head=nn.Linear(32,4)
    def forward(self,x:torch.Tensor,plan:AttentionPlan,backend:str='packed',*,checked:bool=False):
        if backend not in BACKENDS:raise HierarchyError('UNKNOWN_BACKEND',backend)
        if x.ndim!=3 or x.shape!=(plan.batch_size,plan.positions,37):raise HierarchyError('INVALID_FEATURE_SHAPE')
        if checked:
            plan.validate_tensors()
            if not torch.isfinite(x).all():raise HierarchyError('NONFINITE_FEATURE')
        z=self.enc(x)
        for block in self.blocks:z=block(z,plan,backend)
        return self.head(self.norm(z[:,0:plan.tasks*4:4]))
