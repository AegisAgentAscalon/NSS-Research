from pathlib import Path
import json,hashlib,numpy as np,torch
B=Path('/mnt/data/_nss_pass61_work/reconciled');O=Path('/mnt/data/NSS_LB03_LEARNABILITY_v0.1/provenance');T=B/'NSS_NBR02_LB02_Q2_TRAIN_Execution_v0.1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ah(a):
 h=hashlib.sha256()
 for k,v in sorted(a.items()):
  if isinstance(v,torch.Tensor):v=v.cpu().numpy()
  v=np.ascontiguousarray(v);h.update(k.encode());h.update(str(v.dtype).encode());h.update(str(v.shape).encode());h.update(v.tobytes())
 return h.hexdigest()
rows=[]
for seed in range(4101,4105):
 ref=B/f'NSS_NBR02_BRIDGE01_Prototype_v0.1/models/parent_{seed}.npz'
 with np.load(ref,allow_pickle=False) as f:a={k:f[k] for k in f.files}
 for num,tag in [(56,'LB01_TERNARY'),(57,'LB02_Q2_TRAIN'),(59,'LB01_T3_TARGET')]:
  p=B/f'NSS_NBR02_{tag}_Execution_v0.1/inputs/parents/{seed}.npz'
  with np.load(p,allow_pickle=False) as f:b={k:f[k] for k in f.files}
  assert ah(a)==ah(b)
  rows.append(dict(parent=seed,from_pass=55,to_pass=num,from_file=str(ref.relative_to(B)),to_file=str(p.relative_to(B)),byte_equal=sha(ref)==sha(p),tensor_equal=True,model_hash=ah(a)))
 for mode,number,target in [('Q2_M8',58,f'NSS_NBR02_LB02_MASTER16_Execution_v0.1/inputs/parents/{seed}.pt'),('Q2_M32',59,f'NSS_NBR02_LB01_T3_TARGET_Execution_v0.1/inputs/parents/{seed}_Q2_M32_1024.pt')]:
  p=T/f'checkpoints/{seed}_{mode}/step1024.pt';q=B/target
  assert sha(p)==sha(q)
  d=torch.load(p,map_location='cpu',weights_only=True)
  assert ah(d['model'])==d['model_hash']
  rows.append(dict(parent=seed,from_pass=57,to_pass=number,from_file=str(p.relative_to(B)),to_file=target,byte_equal=True,model_hash=d['model_hash'],step=d['step'],phase=d['phase']))
 for step in (0,1024):
  p=T/f'checkpoints/{seed}_Q2_M8/step{step:04d}.pt';d=torch.load(p,map_location='cpu',weights_only=True)
  print(seed,step,list(d), {k:v for k,v in d.items() if k not in ('model','optimizer','torch_rng')},'optimizerkeys',list(d['optimizer']))
  assert ah(d['model'])==d['model_hash']
  if step==0:assert ah(a)==d['model_hash']
# Exact filename for pass59->60 exports: determine by content and list candidates.
p60=B/'NSS_LB01_Q2_PACK_v0.1/inputs/models'
for q in sorted(p60.glob('*.q2')):
 matches=[p for p in (B/'NSS_NBR02_LB01_T3_TARGET_Execution_v0.1/exports').glob('*') if p.is_file() and sha(p)==sha(q)]
 assert len(matches)==1,(q,matches)
 rows.append(dict(parent=int(q.stem),from_pass=59,to_pass=60,from_file=str(matches[0].relative_to(B)),to_file=str(q.relative_to(B)),byte_equal=True,sha256=sha(q)))
(O/'CHECKPOINT_LINEAGE.json').write_text(json.dumps(dict(checks=rows,no_model_execution=True,scope='Safe tensor loading and exact array/hash comparison; no forward calls'),indent=2))
print('LINEAGE checks',len(rows))
