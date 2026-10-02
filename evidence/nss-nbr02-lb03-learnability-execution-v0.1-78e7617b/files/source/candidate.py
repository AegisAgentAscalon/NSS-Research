"""Pass 61: test low-precision *learning*, not merely preservation.
All model values can change. Q2 forward matrices, FP32 math and identity STE.
Persistent FP16 masters have no persistent FP32 shadow. No repair phase.
"""
from inherited_engine import *
import contextlib
C=json.loads((ROOT/'protocol/CONFIG.json').read_text())

class Candidate:
 def __init__(self,seed:int,mode:str,regime:str):
  if seed not in C['parents'] or mode not in C['modes'] or regime not in C['regimes']:raise ValueError('BAD_BINDING')
  self.seed=seed;self.mode=mode;self.regime=regime;self.cursor=0;self.optstep=0
  stage=0 if regime=='EARLY' else 1024
  path=ROOT/f'inputs/parents/{seed}_s{stage:04d}.pt'
  d=torch.load(path,weights_only=True,map_location='cpu')
  if d['seed']!=seed or d['step']!=stage or d['phase']!='prepare' or d['arm']!='Q2_M8':raise ValueError('PARENT_BINDING')
  self.source_file_sha=sha(path);self.source_model_hash=d['model_hash']
  raw={k:d['model'][k].numpy().copy() for k in KEYS}
  if ahash(raw)!=self.source_model_hash:raise ValueError('PARENT_HASH')
  self.master={k:np.ascontiguousarray(a,dtype=np.float16 if mode!='M32' and k in MATS else np.float32) for k,a in raw.items()}
  # Identical fresh optimizer states across all modes and both regimes.
  self.mom={k:dict(qm=np.zeros(a.size,np.int8),qv=np.zeros(a.size,np.uint8),sm=np.zeros((a.size+127)//128,np.float32),sv=np.zeros((a.size+127)//128,np.float32)) for k,a in self.master.items()}
  self.rng={k:np.array([C['round_seed_base']+seed*1000003+i*1009+(0 if regime=='EARLY' else 333333)],np.uint64) for i,k in enumerate(KEYS)}
  self.step_stats=np.zeros(4,np.uint64);self.round_error=np.zeros(1,np.float64)
  self.last_gradient_hash=None
 def effective(self):return {k:quant(a)[3] if k in MATS else a.copy() for k,a in self.master.items()}
 def arrays(self):
  a={'w:'+k:v for k,v in self.master.items()}
  for k,s in self.mom.items():
   for n,v in s.items():a[f'o:{k}:{n}']=v
  for k,v in self.rng.items():a['r:'+k]=v
  return a
 def hash(self):return ahash(self.arrays())
 def save(self,path):
  path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
  meta=dict(schema='NSS_LB03_STATE_V1',seed=self.seed,mode=self.mode,regime=self.regime,cursor=self.cursor,optstep=self.optstep,hash=self.hash(),source=self.source_file_sha,source_model_hash=self.source_model_hash,config_sha=sha(ROOT/'protocol/CONFIG.json'))
  a=self.arrays();a['meta']=np.frombuffer(canon(meta),np.uint8);tmp=path.with_suffix('.tmp')
  with tmp.open('wb') as f:np.savez_compressed(f,**a);f.flush();os.fsync(f.fileno())
  tmp.replace(path);return dict(path=str(path.relative_to(ROOT)),sha256=sha(path),state_hash=self.hash(),cursor=self.cursor)
 @classmethod
 def load(cls,path):
  with np.load(path,allow_pickle=False) as z:
   d=json.loads(z['meta'].tobytes());o=cls(d['seed'],d['mode'],d['regime'])
   if d['schema']!='NSS_LB03_STATE_V1' or d['config_sha']!=sha(ROOT/'protocol/CONFIG.json') or d['source']!=o.source_file_sha:raise ValueError('STATE_SOURCE_OR_CONFIG')
   if set(z.files)!=set(o.arrays())|{'meta'}:raise ValueError('STATE_MEMBERSHIP')
   for k,old in o.arrays().items():
    a=z[k]
    if a.shape!=old.shape or a.dtype!=old.dtype or not np.isfinite(a).all():raise ValueError('STATE_FORMAT:'+k)
    old[:]=a
   o.cursor=d['cursor'];o.optstep=d['optstep']
   if o.cursor!=o.optstep or o.cursor<0 or o.cursor>C['updates_per_branch']:raise ValueError('STATE_CURSOR')
   if o.hash()!=d['hash']:raise ValueError('STATE_DIGEST')
   return o
 def loss_and_grads(self,tokens,labels,profile=False):
  ea=self.effective();w={k:torch.from_numpy(a).requires_grad_(True) for k,a in ea.items()};saved={};saved_view_count=0
  def save_tensor(x):
   nonlocal saved_view_count
   st=x.untyped_storage();saved[(st.data_ptr(),st.nbytes())]=(str(x.dtype),tuple(x.shape));saved_view_count+=1;return x
  ctx=torch.autograd.graph.saved_tensors_hooks(save_tensor,lambda x:x) if profile else contextlib.nullcontext()
  yb=torch.as_tensor(C['old_B'] if self.regime=='EARLY' else C['new_B'],dtype=torch.long)
  with ctx:
   _,az=forward(w,tokens);_,bz=forward(w,np.arange(18,26)[:,None])
   la=F.cross_entropy(az.reshape(-1,9),torch.as_tensor(labels,dtype=torch.long).reshape(-1));lb=F.cross_entropy(bz[:,0],yb);loss=la+lb
  if not torch.isfinite(loss):raise ValueError('NONFINITE_LOSS')
  loss.backward();gn=torch.nn.utils.clip_grad_norm_(list(w.values()),C['clip_norm'],error_if_nonfinite=True)
  gradients={}
  for k in KEYS:
   if w[k].grad is None or not torch.isfinite(w[k].grad).all():raise ValueError('GRADIENT:'+k)
   gradients[k]=w[k].grad.detach().numpy() # FP32 leaf gradients, no silent half gradients
  metrics=dict(loss=float(loss.detach()),A_loss=float(la.detach()),B_loss=float(lb.detach()),grad_norm=float(gn),gradient_hash=ahash(gradients),A_targets=int(np.size(labels)),B_targets=8)
  if profile:
   effkeys={(v.untyped_storage().data_ptr(),v.untyped_storage().nbytes()) for v in w.values()}
   subtotal=sum(a.nbytes for a in self.master.values())+sum(a.nbytes for a in gradients.values())+sum(a.nbytes for m in self.mom.values() for a in m.values())
   metrics['memory_profile']=dict(master_bytes=sum(a.nbytes for a in self.master.values()),gradient_bytes=sum(a.nbytes for a in gradients.values()),moment_bytes=sum(a.nbytes for m in self.mom.values() for a in m.values()),learning_array_subtotal=subtotal,effective_weights=sum(a.nbytes for a in ea.values()),saved_unique_storage=sum(n for _,n in saved),saved_excluding_effective=sum(n for (ptr_,n) in saved if (ptr_,n) not in effkeys),saved_views=saved_view_count,rng_bytes=sum(a.nbytes for a in self.rng.values()),optimizer_scratch_bytes=1024,quantizer_row_scratch_bytes=256,scope='Union of distinct storages saved during one graph; not simultaneous peak, process RSS or activations-only. Wide transients, corpus, Python/compiler/runtime are additional.')
  return gradients,metrics,w
 def step(self,tokens,labels,lr:float,profile=False):
  start=time.perf_counter();grads,info,leaves=self.loss_and_grads(tokens,labels,profile=profile)
  self.optstep+=1;self.step_stats.fill(0);self.round_error.fill(0)
  for k in KEYS:
   a=self.master[k];g=grads[k];s=self.mom[k]
   ret=LIB.adam_m8(a.size,ptr(a),ptr(g),int(a.dtype==np.float16),int(self.mode=='M16_STOCHASTIC'),*[ptr(s[n]) for n in ('qm','qv','sm','sv')],self.optstep,np.float32(lr),ptr(self.rng[k]),ptr(self.step_stats),ptr(self.round_error))
   if ret:raise ValueError('UPDATE_NONFINITE:'+k)
  self.cursor+=1
  info.update(cursor=self.cursor,optstep=self.optstep,lr=float(lr),statistics=self.step_stats.tolist(),round_error_squared=float(self.round_error[0]),state_hash=self.hash(),seconds=time.perf_counter()-start,peak_rss=rss())
  return info

def lr_at(index):
 if not 0<=index<C['updates_per_branch']:raise ValueError('STEP_RANGE')
 f=.5*(1+math.cos(math.pi*index/(C['updates_per_branch']-1)))
 return C['lr_end']+(C['lr_start']-C['lr_end'])*f

def load_batch(seed,index):
 with np.load(ROOT/f'inputs/replay/{seed}.npz',allow_pickle=False) as z:return z['tokens'][index%64].copy(),z['labels'][index%64].copy()

if __name__=='__main__':
 print('Library only. Use tools/run_one.py after protocol freeze.')
