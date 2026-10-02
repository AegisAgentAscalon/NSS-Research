from pathlib import Path
import sys,json,hashlib,platform,datetime,subprocess,os
R=Path(__file__).resolve().parents[1];sys.path.insert(0,str(R/'source'))
import numpy as np
from task import stream,oracle,independent_oracle
C=json.loads((R/'protocol/CONFIG.json').read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def windows(row):return {np.asarray(row[i:i+32],np.uint8).tobytes() for i in range(len(row)-31)}
def build(dest):
 used=set();refs=[]
 for f in sorted((R/'inputs').rglob('*.npz')):
  with np.load(f,allow_pickle=False) as z:
   key=next((k for k in ['tokens','t','events','A_tokens'] if k in z.files),None)
   if key is None:continue
   t=z[key]
   if t.ndim<2:continue
   for row in t.reshape(-1,t.shape[-1]):used.update(windows(row))
   refs.append(dict(file=str(f.relative_to(R)),sha256=sha(f),token_key=key,rows=int(t.size//t.shape[-1])))
 receipt=dict(seed=C['fixture_seed'],exclusion_files=refs,initial_windows=len(used),panels={})
 for pi,panel in enumerate(['development','confirmation','stress']):
  rng=np.random.default_rng(C['fixture_seed']+pi*101);rows=[];fam=[];reject=0
  for family in range(4):
   for _ in range(C['fixture_counts'][panel]//4):
    for attempt in range(10000):
     t=stream(rng,C['length'][panel],family);ww=windows(t)
     if used.intersection(ww):reject+=1;continue
     used.update(ww);rows.append(t);fam.append(family);break
    else:raise RuntimeError('FIXTURE_COLLISION_STOP')
  ts=np.asarray(rows,np.uint8);y,m=oracle(ts);assert np.array_equal(y,independent_oracle(ts))
  out=dest/f'{panel}.npz';np.savez_compressed(out,tokens=ts,labels=y,masks=m,families=np.array(fam,np.uint8),prefix=np.array(C['prefix'][panel],np.int64))
  receipt['panels'][panel]=dict(path=str(out),histories=len(ts),sha256=sha(out),rejected_candidates=reject,counts=[fam.count(f)for f in range(4)])
 return receipt
if __name__=='__main__':
 target=R/'fixtures' if len(sys.argv)==1 else Path(sys.argv[1]);target.mkdir(parents=True,exist_ok=True)
 receipt=build(target);(target/'GENERATION.json').write_text(json.dumps(receipt,indent=2));print(json.dumps(receipt['panels']))
