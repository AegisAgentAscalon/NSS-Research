from pathlib import Path
import subprocess,sys,os,json,datetime
root=Path(__file__).resolve().parents[1];os.chdir(root)
KINDS=['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4']
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
for seed in range(801,806):
 for kind in ['binder']+KINDS:
  out=root/'checkpoints'/f'{kind}_{seed}.safetensors'
  if out.exists():raise FileExistsError(out)
  cmd=[sys.executable,'-m','nbr006.train','--kind',kind,'--seed',str(seed),'--steps',str(1200 if kind=='binder' else 6000),'--out',str(out)]
  print(datetime.datetime.now(datetime.timezone.utc).isoformat(),kind,seed,flush=True)
  with (root/'evidence'/f'TRAIN_{kind}_{seed}.log').open('w') as f:subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
print('MAIN_TRAINING_COMPLETE',flush=True)
