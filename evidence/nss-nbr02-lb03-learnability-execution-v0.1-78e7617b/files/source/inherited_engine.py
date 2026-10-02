"""Actual M16 matrix storage, FP32 effective-weight leaves, SQ8 optimizer.
No persistent floating master duplication; quantizer uses one small row scratch.
This manually applies the inherited identity-STE gradient to stored masters.
"""
from __future__ import annotations
import os
for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):os.environ[k]='1'
import ctypes,hashlib,json,math,resource,time,platform,sys
from pathlib import Path
import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
ROOT=Path(__file__).resolve().parents[1]
torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.backends.mkldnn.enabled=False;torch.use_deterministic_algorithms(True)
MATS=('cell.weight_ih','cell.weight_hh','head.weight');BIASES=('cell.bias_ih','cell.bias_hh','head.bias');KEYS=MATS+BIASES
SHAPES={'cell.weight_ih':(192,26),'cell.weight_hh':(192,64),'head.weight':(9,64),'cell.bias_ih':(192,),'cell.bias_hh':(192,),'head.bias':(9,)}
P=ctypes.c_void_p;I=ctypes.c_int
LIB=ctypes.CDLL(str(ROOT/'bin/master16.so'))
LIB.round_array.argtypes=[I,P,P,I,P];LIB.round_array.restype=I
LIB.q2_effective.argtypes=[I,I,P,I,P,P,P,P];LIB.q2_effective.restype=I
LIB.adam_m8.argtypes=[I,P,P,I,I,P,P,P,P,I,ctypes.c_float,P,P,P];LIB.adam_m8.restype=I
OLD=ctypes.CDLL(str(ROOT/'bin/kernels.so'))
OLD.adam_step.argtypes=[I]+[P]*8+[I,I,ctypes.c_float];OLD.adam_step.restype=I
OLD.q2_rollout.argtypes=[I,I]+[P]*16;OLD.q2_rollout.restype=None
ptr=lambda a:P(a.ctypes.data) if a is not None else None

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False).encode()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,obj):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);q=p.with_suffix(p.suffix+'.tmp');q.write_bytes(canon(obj)+b'\n');q.replace(p)
def ahash(arr):
 h=hashlib.sha256()
 for k,a in sorted(arr.items()):
  a=np.ascontiguousarray(a);h.update(k.encode());h.update(str(a.dtype).encode());h.update(str(a.shape).encode());h.update(a.tobytes())
 return h.hexdigest()
def rss():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024

def q_numpy(a):
 a=np.asarray(a,np.float32);lo=np.minimum(a.min(1),np.float32(0));hi=np.maximum(a.max(1),np.float32(0));s=np.maximum(((hi.astype(np.float64)-lo)/3).astype(np.float32),np.float32(1e-8));z=np.clip(np.rint(-lo/s),0,3).astype(np.uint8);q=np.clip(np.rint(a/s[:,None])+z[:,None],0,3).astype(np.uint8);return q,s,z,(q.astype(np.int16)-z[:,None].astype(np.int16)).astype(np.float32)*s[:,None]
def quant(a):
 if a.dtype not in (np.float32,np.float16) or a.ndim!=2 or not a.flags.c_contiguous:raise ValueError('MASTER_ARRAY')
 q=np.empty(a.shape,np.uint8);s=np.empty(a.shape[0],np.float32);z=np.empty(a.shape[0],np.uint8);e=np.empty(a.shape,np.float32)
 if LIB.q2_effective(*a.shape,ptr(a),int(a.dtype==np.float16),ptr(e),ptr(q),ptr(s),ptr(z)):raise ValueError('QUANTIZATION')
 return q,s,z,e

def forward(w,t,h=None):
 t=torch.as_tensor(t,dtype=torch.long);dt=w[MATS[0]].dtype
 if t.ndim!=2 or (t<0).any() or (t>25).any():raise ValueError('TOKENS')
 x=F.one_hot(t,26).to(dt);h=torch.zeros((len(t),64),dtype=dt) if h is None else torch.as_tensor(h,dtype=dt).clone();hs=[];zs=[]
 for j in range(t.shape[1]):
  a=F.linear(x[:,j],w[MATS[0]],w[BIASES[0]]);b=F.linear(h,w[MATS[1]],w[BIASES[1]]);ar,az,an=a.chunk(3,-1);br,bz,bn=b.chunk(3,-1)
  r=torch.sigmoid(ar+br);zz=torch.sigmoid(az+bz);nn=torch.tanh(an+r*bn);h=(1-zz)*nn+zz*h;hs.append(h);zs.append(F.linear(h,w[MATS[2]],w[BIASES[2]]))
 return torch.stack(hs,1),torch.stack(zs,1)
def np_forward(w,t):
 w={k:np.asarray(a,np.float64) for k,a in w.items()};t=np.asarray(t);h=np.zeros((len(t),64));hs=[];zs=[]
 for j in range(t.shape[1]):
  a=w[MATS[0]][:,t[:,j]].T+w[BIASES[0]];b=h@w[MATS[1]].T+w[BIASES[1]];ar,az,an=np.split(a,3,-1);br,bz,bn=np.split(b,3,-1)
  r=1/(1+np.exp(-ar-br));z=1/(1+np.exp(-az-bz));n=np.tanh(an+r*bn);h=(1-z)*n+z*h;hs.append(h.copy());zs.append(h@w[MATS[2]].T+w[BIASES[2]])
 return np.stack(hs,1),np.stack(zs,1)
def comparison(a,b,atol=1e-9,rtol=1e-8):
 d=np.abs(a-b);tol=atol+rtol*np.abs(b);return dict(scalars=a.size,violations=int((d>tol).sum()),finite=bool(np.isfinite(a).all() and np.isfinite(b).all()),max_abs=float(d.max(initial=0)),max_ratio=float((d/tol).max(initial=0)))
def metrics(z,y):
 pred=z.argmax(-1);ok=pred==y;return dict(correct=int(ok.sum()),total=int(ok.size),whole=int(ok.all(1).sum()),histories=len(y),false_done=int(((pred==8)&(y!=8)).sum()))

class TrainState:
 def __init__(self,seed,mode):
  if mode not in ('M32','M16_NEAREST','M16_STOCHASTIC'):raise ValueError('MODE')
  d=torch.load(ROOT/f'inputs/parents/{seed}.pt',weights_only=True,map_location='cpu')
  assert d['step']==1024 and d['phase']=='prepare' and d['optimizer']['mode']=='m8'
  self.seed=seed;self.mode=mode;self.cursor=0;self.optstep=1024;self.master={k:np.ascontiguousarray(d['model'][k].numpy(),dtype=np.float16 if mode!='M32' and k in MATS else np.float32) for k in KEYS}
  self.mom={k:{n:v.numpy().copy() for n,v in d['optimizer']['arrays'][k].items()} for k in KEYS}
  self.rng={k:np.array([((seed*1000003+i*1009+773)&((1<<64)-1))],np.uint64) for i,k in enumerate(KEYS)}
  self.source_model_hash=d['model_hash'];self.source_file_sha=sha(ROOT/f'inputs/parents/{seed}.pt')
  self.step_stats=np.zeros(4,np.uint64);self.round_error=np.zeros(1,np.float64)
 def effective(self):return {k:quant(a)[3] if k in MATS else a.copy() for k,a in self.master.items()}
 def arrays(self):
  x={'w:'+k:v for k,v in self.master.items()}
  for k,s in self.mom.items():
   for n,v in s.items():x[f'o:{k}:{n}']=v
  for k,v in self.rng.items():x['r:'+k]=v
  return x
 def hash(self):return ahash(self.arrays())
 def save(self,path):
  meta=dict(schema='NSS_MASTER16_V1',seed=self.seed,mode=self.mode,cursor=self.cursor,optstep=self.optstep,hash=self.hash(),source=self.source_file_sha,source_model_hash=self.source_model_hash)
  a=self.arrays();a['meta']=np.frombuffer(canon(meta),np.uint8);path=Path(path);path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix('.tmp')
  with open(tmp,'wb') as f:np.savez_compressed(f,**a);f.flush();os.fsync(f.fileno())
  tmp.replace(path);return dict(path=str(path.relative_to(ROOT)),sha256=sha(path),state_hash=self.hash(),cursor=self.cursor)
 @classmethod
 def load(cls,path):
  with np.load(path,allow_pickle=False) as z:
   d=json.loads(z['meta'].tobytes());o=cls(d['seed'],d['mode']);o.cursor=d['cursor'];o.optstep=d['optstep']
   if d['schema']!='NSS_MASTER16_V1' or d['source']!=o.source_file_sha:raise ValueError('STATE_BINDING')
   for k in KEYS:
    a=z['w:'+k];old=o.master[k]
    if a.shape!=old.shape or a.dtype!=old.dtype or not np.isfinite(a).all():raise ValueError('MASTER_FORMAT')
    old[:]=a
    for n,v in o.mom[k].items():
     a=z[f'o:{k}:{n}']
     if a.shape!=v.shape or a.dtype!=v.dtype or not np.isfinite(a).all():raise ValueError('MOMENT_FORMAT')
     v[:]=a
    o.rng[k][:]=z['r:'+k]
   if o.hash()!=d['hash'] or o.optstep!=1024+o.cursor:raise ValueError('CHECKPOINT_INTEGRITY')
   return o
 def step(self,tokens,labels,lr=.0003,profile=False):
  start=time.perf_counter();ea=self.effective();w={k:torch.from_numpy(a).requires_grad_(True) for k,a in ea.items()}
  saved={};persistent_ptrs={a.ctypes.data for a in self.arrays().values()}
  def pack(x):
   st=x.untyped_storage();key=(st.data_ptr(),st.nbytes());saved[key]=(str(x.dtype),tuple(x.shape));return x
  ctx=torch.autograd.graph.saved_tensors_hooks(pack,lambda x:x) if profile else __import__('contextlib').nullcontext()
  with ctx:
   _,az=forward(w,tokens);_,bz=forward(w,np.arange(18,26)[:,None]);la=F.cross_entropy(az.reshape(-1,9),torch.as_tensor(labels,dtype=torch.long).reshape(-1));lb=F.cross_entropy(bz[:,0],torch.arange(8)%2);loss=la+lb
  if not torch.isfinite(loss):raise ValueError('LOSS')
  loss.backward();gn=torch.nn.utils.clip_grad_norm_(list(w.values()),1.,error_if_nonfinite=True)
  self.step_stats.fill(0);self.round_error.fill(0);self.optstep+=1
  for k in KEYS:
   g=w[k].grad
   if g is None or not g.is_contiguous() or not torch.isfinite(g).all():raise ValueError('GRADIENT')
   a=self.master[k];s=self.mom[k];ret=LIB.adam_m8(a.size,ptr(a),ptr(g.detach().numpy()),int(a.dtype==np.float16),int(self.mode=='M16_STOCHASTIC'),*[ptr(s[n]) for n in ('qm','qv','sm','sv')],self.optstep,np.float32(lr),ptr(self.rng[k]),ptr(self.step_stats),ptr(self.round_error))
   if ret:raise ValueError('UPDATE_NONFINITE')
  self.cursor+=1
  out=dict(cursor=self.cursor,optstep=self.optstep,loss=float(loss.detach()),A_loss=float(la.detach()),B_loss=float(lb.detach()),grad_norm=float(gn),statistics=self.step_stats.tolist(),round_error_squared=float(self.round_error[0]),state_hash=self.hash(),seconds=time.perf_counter()-start,rss=rss())
  if profile:
   effective_keys={(v.untyped_storage().data_ptr(),v.untyped_storage().nbytes()) for v in w.values()}
   out['memory_profile']=dict(master_bytes=sum(a.nbytes for a in self.master.values()),moment_bytes=sum(a.nbytes for s in self.mom.values() for a in s.values()),rng_bytes=sum(a.nbytes for a in self.rng.values()),effective_weight_bytes=sum(a.nbytes for a in ea.values()),gradient_bytes=sum(p.grad.numel()*p.grad.element_size() for p in w.values()),saved_tensor_unique_bytes=sum(k[1] for k in saved),saved_tensor_excluding_effective_bytes=sum(k[1] for k in saved if k not in effective_keys),saved_storage_count=len(saved),scope='Saved tensor storage union within one training graph, not total process peak; includes values whose lifetimes may differ. effective and saved sets may overlap. C scratch additional1024bytes and quantizer row256bytes; no full FP32 master shadow.')
  return out

def packed_roll(state,t):
 p={};s={};z={};w=state.effective()
 for k in MATS:
  q,s[k],z[k],e=quant(state.master[k]);v=q.ravel();pad=np.pad(v,(0,(-len(v))%4));p[k]=(pad.reshape(-1,4).astype(np.uint16)*[1,4,16,64]).sum(1).astype(np.uint8)
 t=np.ascontiguousarray(t,np.int64);h=np.zeros((len(t),64),np.float64);hs=np.empty((*t.shape,64));zs=np.empty((*t.shape,9));args=[t,h,*[p[k] for k in MATS],*[s[k] for k in MATS],*[z[k] for k in MATS],*[w[k] for k in BIASES],hs,zs];OLD.q2_rollout(len(t),t.shape[1],*[ptr(a) for a in args]);return hs,zs

def pack_export(state,path):
 arrays={};payload=0
 for k in MATS:
  q,s,z,e=quant(state.master[k]);v=q.ravel();a=np.pad(v,(0,(-len(v))%4));codes=(a.reshape(-1,4).astype(np.uint16)*[1,4,16,64]).sum(1).astype(np.uint8)
  for n,d in [('code',codes),('scale',s),('zero',z)]:arrays[k+':'+n]=d;payload+=d.nbytes
 for k in BIASES:arrays[k]=state.master[k];payload+=state.master[k].nbytes
 arrays['meta']=np.frombuffer(canon(dict(format='NSS_Q2_NPZ_V1',shapes=SHAPES,source=state.hash(),payload_bytes=payload)),np.uint8)
 np.savez(path,**arrays);return payload

def load_packed(path):
 with np.load(path,allow_pickle=False) as zf:
  d=json.loads(zf['meta'].tobytes())
  if d['format']!='NSS_Q2_NPZ_V1' or {k:tuple(v) for k,v in d['shapes'].items()}!=SHAPES:raise ValueError('PACKED_FORMAT')
  data={k:zf[k].copy() for k in zf.files if k!='meta'}
 for k in MATS:
  n=np.prod(SHAPES[k]);p=data[k+':code'];s=data[k+':scale'];z=data[k+':zero']
  if p.dtype!=np.uint8 or p.size!=(n+3)//4 or s.shape!=(SHAPES[k][0],) or s.dtype!=np.float32 or z.dtype!=np.uint8 or z.shape!=s.shape or (s<=0).any() or (z>3).any() or not np.isfinite(s).all():raise ValueError('PACKED_SHAPE_SCALE')
 for k in BIASES:
  if data[k].shape!=SHAPES[k] or data[k].dtype!=np.float32 or not np.isfinite(data[k]).all():raise ValueError('PACKED_BIAS')
 return data,d

def packed_file_roll(path,t):
 a,d=load_packed(path);t=np.ascontiguousarray(t,np.int64)
 if t.ndim!=2 or (t<0).any() or (t>25).any():raise ValueError('PACKED_INPUT')
 h=np.zeros((len(t),64),np.float64);hs=np.empty((*t.shape,64));zs=np.empty((*t.shape,9));args=[t,h,*[a[k+':code'] for k in MATS],*[a[k+':scale'] for k in MATS],*[a[k+':zero'] for k in MATS],*[a[k] for k in BIASES],hs,zs]
 OLD.q2_rollout(len(t),t.shape[1],*[ptr(v) for v in args]);return hs,zs
