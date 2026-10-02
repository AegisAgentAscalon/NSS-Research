"""SH01 record-feature adapter. No oracle targets enter the reader or topology."""
from __future__ import annotations
import numpy as np
import torch
from .hierarchy import Hierarchy,HierarchyError

def compile_features(world:dict, spec:Hierarchy|None=None)->torch.Tensor:
    spec=spec or Hierarchy.from_dependencies(world['deps'])
    if spec.dependencies!=tuple(tuple(d) for d in world['deps']):raise HierarchyError('FEATURE_TOPOLOGY_MISMATCH')
    n=spec.tasks;codes=np.asarray(world['codes'],dtype=np.float32)
    if codes.shape!=(n,8):raise HierarchyError('INVALID_ADDRESS_SHAPE')
    if any(len(d)!=2 for d in spec.dependencies):raise HierarchyError('SH01_ADAPTER_REQUIRES_TWO_DEPENDENCIES')
    for key in ['progress','receipts','constraints']:
        if len(world[key])!=n or any(v not in [0,1] for v in world[key]):raise HierarchyError('INVALID_BINARY_FIELD',key)
    nuisance=np.asarray(world['nuisance'],np.float32)
    if nuisance.shape!=(n,4) or world['freeze'] not in [0,1]:raise HierarchyError('INVALID_EVIDENCE_SHAPE')
    x=np.zeros((spec.positions,37),np.float32)
    for i in range(n):
        for role in range(4):
            pos=4*i+role;x[pos,role]=1;x[pos,6:14]=codes[i]
            if role==0:
                x[pos,14:22]=codes[world['deps'][i][0]];x[pos,22:30]=codes[world['deps'][i][1]]
            elif role==1:x[pos,30]=2*world['progress'][i]-1
            elif role==2:x[pos,31]=2*world['receipts'][i]-1
            else:x[pos,32]=2*world['constraints'][i]-1
            x[pos,33:37]=nuisance[i]
    for r in range(spec.regions):
        pos=4*n+r;x[pos,4]=1;x[pos,6:14]=codes[r*spec.region_width:min(n,(r+1)*spec.region_width)].mean(0)
    x[-1,5]=1;x[-1,32]=2*world['freeze']-1
    if not np.isfinite(x).all():raise HierarchyError('NONFINITE_FEATURE')
    return torch.from_numpy(x)

def prepare_worlds(worlds:list[dict]):
    specs=tuple(Hierarchy.from_dependencies(w['deps']) for w in worlds)
    return torch.stack([compile_features(w,s) for w,s in zip(worlds,specs)]),specs
