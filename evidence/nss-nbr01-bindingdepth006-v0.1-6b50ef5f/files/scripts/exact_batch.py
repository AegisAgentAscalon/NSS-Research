from pathlib import Path
import subprocess,sys,os,time,json
import numpy as np
from nbr006 import common as c
root=c.ROOT;os.chdir(root);env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1');records=[]
for seed in range(801,806):
 while not (root/'checkpoints'/f'binder_{seed}.json').exists():time.sleep(2)
 for out in [root/'results',Path('/mnt/data/nss006_work/exact_replay')]:
  out.mkdir(parents=True,exist_ok=True)
  cmd=[sys.executable,'-m','nbr006.exact_eval','--seed',str(seed),'--outdir',str(out)]
  with (out/f'exact_lookup_{seed}.log').open('w') as f:subprocess.run(cmd,stdout=f,stderr=subprocess.STDOUT,env=env,check=True)
 with np.load(root/'results'/f'exact_lookup_{seed}.npz',allow_pickle=False) as a,np.load(Path('/mnt/data/nss006_work/exact_replay')/f'exact_lookup_{seed}.npz',allow_pickle=False) as b:
  for k in a.files:np.testing.assert_array_equal(a[k],b[k])
 records.append({'seed':seed,'status':'PASS'});print('EXACT_REPLAYED',seed,flush=True)
c.dump(root/'evidence/EXACT_REPLAY.json',{'status':'PASS','entries':records})
