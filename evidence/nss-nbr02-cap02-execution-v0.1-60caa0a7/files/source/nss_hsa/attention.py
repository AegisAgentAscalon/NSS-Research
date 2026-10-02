"""Attention execution. Packed HSA never constructs the full T x T graph.

One joint softmax per query over its complete allowed key set. Levels are NOT
normalized separately, and key duplication across routes is removed by the graph.
"""
from __future__ import annotations
import math
import torch
from torch.nn import functional as F
from .hierarchy import AttentionPlan, HierarchyError

def _check(q, k, v, plan):
    if q.ndim!=4 or q.shape!=k.shape or q.shape!=v.shape:
        raise HierarchyError('INVALID_QKV_SHAPES')
    if q.shape[0]!=plan.batch_size or q.shape[2]!=plan.positions:
        raise HierarchyError('PLAN_SHAPE_MISMATCH')
    if q.device!=plan.device or k.device!=q.device or v.device!=q.device:
        raise HierarchyError('PLAN_DEVICE_MISMATCH')
    if q.dtype!=k.dtype or q.dtype!=v.dtype or not q.is_floating_point():
        raise HierarchyError('INVALID_QKV_DTYPE')

def packed_attention(q: torch.Tensor, k: torch.Tensor, v: torch.Tensor, plan: AttentionPlan) -> torch.Tensor:
    """Gather K/V once per shared neighborhood, then run small batched SDPA tiles."""
    _check(q,k,v,plan)
    batch, heads, _, dim=q.shape;parts=[]
    bi=torch.arange(batch,device=q.device)[:,None,None,None]
    hi=torch.arange(heads,device=q.device)[None,:,None,None]
    for bucket in plan.buckets:
        m, rows, width=bucket.groups,bucket.queries,bucket.indices.shape[-1]
        qq=q[:,:,bucket.start:bucket.start+m*rows].reshape(batch,heads,m,rows,dim).permute(0,2,1,3,4).reshape(batch*m,heads,rows,dim)
        kk=k[bi,hi,bucket.indices[:,None],:].permute(0,2,1,3,4).reshape(batch*m,heads,width,dim)
        vv=v[bi,hi,bucket.indices[:,None],:].permute(0,2,1,3,4).reshape(batch*m,heads,width,dim)
        mask=bucket.valid.reshape(batch*m,1,1,width)
        aa=F.scaled_dot_product_attention(qq,kk,vv,attn_mask=mask,dropout_p=0.0,is_causal=False)
        parts.append(aa.reshape(batch,m,heads,rows,dim).permute(0,2,1,3,4).reshape(batch,heads,m*rows,dim))
    return torch.cat(parts,dim=2)

def graph_mask(plan: AttentionPlan) -> torch.Tensor:
    """Dense verification oracle only; never called on the packed execution path."""
    mask=torch.zeros((plan.batch_size,plan.positions,plan.positions),dtype=torch.bool,device=plan.device)
    for bi,spec in enumerate(plan.specs):
        for qi,keys in enumerate(spec.rows()):mask[bi,qi,list(keys)]=True
    return mask

def masked_reference(q,k,v,plan):
    _check(q,k,v,plan)
    scores=(q@k.transpose(-2,-1))/math.sqrt(q.shape[-1])
    return scores.masked_fill(~graph_mask(plan)[:,None],-torch.inf).softmax(-1)@v

def full_dense_attention(q,k,v,plan):
    _check(q,k,v,plan)
    return F.scaled_dot_product_attention(q,k,v,dropout_p=0.0)

BACKENDS={'packed':packed_attention,'masked_reference':masked_reference,'full_dense':full_dense_attention}
