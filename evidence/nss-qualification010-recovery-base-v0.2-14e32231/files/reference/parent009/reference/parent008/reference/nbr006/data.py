"""Generated containment graphs. Ground-truth IDs are NEVER neural inputs.

Learned readers receive fresh random numeric identity codes, current record
vectors, record presence and query code. Terminal room self-records are supplied
facts. All ground-truth path traversal lives here/in the scorer, not in readers.
"""
import numpy as np
import torch
D=17

def normalize(x): return x / np.maximum(np.linalg.norm(x,axis=-1,keepdims=True),1e-8)

def batch(rng,b=64,n=16,max_h=4,hops=None,missing=None,query_noise=0.0):
 if n < max_h+3:raise ValueError('Not enough entities for path and two rooms')
 codes=np.zeros((b,n+1,D),dtype=np.float32)
 codes[:,:n,:16]=normalize(rng.standard_normal((b,n,16))).astype(np.float32)
 codes[:,n,-1]=1.0
 order=np.argsort(rng.random((b,n)),axis=1)
 parent=np.full((b,n+1),n,dtype=np.int64); rows=np.arange(b)
 for j in range(n):
  dest=order[:,j] if j<2 else order[rows,(rng.random(b)*j).astype(int)]
  if 2<=j<=max_h+1:dest=order[:,0] if j==2 else order[:,j-1]
  parent[rows,order[:,j]]=dest
 lengths=rng.integers(1,max_h+1,b) if hops is None else np.full(b,hops,dtype=np.int64)
 query=order[rows,lengths+1]
 absent=(rng.random(b)<.35) if missing is None else np.full(b,missing,dtype=bool)
 cutpos=2+(rng.random(b)*lengths).astype(int)
 parent[rows[absent],order[rows,cutpos][absent]]=n
 for j in range(max_h+2,n):
  mask=rng.random(b)<.12
  parent[rows[mask],order[mask,j]]=n
 parent[:,n]=n
 perm=np.argsort(rng.random((b,n)),axis=1)
 keys=codes[rows[:,None],perm]
 vals=codes[rows[:,None],parent[rows[:,None],perm]]
 present=parent[rows[:,None],perm]!=n
 keys=keys*present[...,None];vals=vals*present[...,None]
 q=codes[rows,query].copy()
 if query_noise:
  q[:,:16]+=rng.normal(0,query_noise,q[:,:16].shape).astype(np.float32);q=normalize(q).astype(np.float32)
 return {'codes':codes,'parent':parent,'order':order,'keys':keys,'vals':vals,'present':present,'query':query,'q':q,'length':lengths,'absent':absent,'rooms':order[:,:2],'slot_ids':perm}

def targets(p,steps=8):
 cur=p['query'].copy(); out=[];r=np.arange(len(cur))
 for _ in range(steps):
  cur=p['parent'][r,cur];out.append(cur.copy())
 return np.stack(out,axis=1)

def tensors(p):
 return tuple(torch.from_numpy(p[k]) for k in ['keys','vals','present','q','codes'])

def oracle_answer(p):
 n=p['parent'].shape[1]-1;ans=[]
 for row,start in enumerate(p['query']):
  node=int(start);seen=set()
  while node!=n and node not in seen:
   seen.add(node);nxt=int(p['parent'][row,node])
   if nxt==node:break
   node=nxt
  if node!=n and int(p['parent'][row,node])!=node:node=n
  ans.append(node)
 return np.array(ans,dtype=np.int64)

def check_problem(p):
 assert np.isfinite(p['codes']).all()
 assert np.array_equal(targets(p,p['parent'].shape[1]+1)[:,-1],oracle_answer(p))
 assert np.unique(p['slot_ids'],axis=1).shape==p['slot_ids'].shape
