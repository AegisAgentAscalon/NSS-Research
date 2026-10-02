from pathlib import Path
import subprocess,sys,os,json,time
import numpy as np
from nbr006 import common as c
root=c.ROOT;target=Path(sys.argv[1]);target.mkdir(parents=True,exist_ok=True);out=[]
env=dict(os.environ,OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
for seed in range(801,806):
 for kind in ['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4']:
  file=root/'results'/f'{kind}_{seed}.json'
  while not file.exists():time.sleep(2)
  d=json.loads(file.read_text());print('REPLAY',kind,seed,flush=True)
  cmd=[sys.executable,'-m','nbr006.eval','--kind',kind,'--seed',str(seed),'--checkpoint',str(root/'checkpoints'/f'{kind}_{seed}.safetensors'),'--binder',str(root/'checkpoints'/f'binder_{seed}.safetensors'),'--outdir',str(target)]
  with (target/(file.stem+'.log')).open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,check=True,cwd=root)
  with np.load(file.with_suffix('.npz'),allow_pickle=False) as a,np.load(target/file.with_suffix('.npz').name,allow_pickle=False) as b:
   assert set(a.files)==set(b.files)
   for key in a.files:np.testing.assert_array_equal(a[key],b[key])
   n_arrays=len(a.files)
  dd=json.loads((target/file.name).read_text());assert d['rows']==dd['rows'];assert d['model_weight_hash']==dd['model_weight_hash']
  out.append({'kind':kind,'seed':seed,'status':'PASS','arrays':n_arrays,'rows':len(d['rows'])})
c.dump(root/'evidence/FULL_REPLAY.json',{'status':'PASS','entries':out,'fresh_interpreters':len(out)})
