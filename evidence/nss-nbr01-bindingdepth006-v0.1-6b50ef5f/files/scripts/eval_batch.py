from pathlib import Path
import subprocess,sys,os,time
root=Path(__file__).resolve().parents[1];os.chdir(root)
KINDS=['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4']
env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1')
for seed in range(801,806):
 for kind in KINDS:
  ready=root/'checkpoints'/f'{kind}_{seed}.json'
  while not ready.exists():time.sleep(2)
  cmd=[sys.executable,'-m','nbr006.eval','--kind',kind,'--seed',str(seed),'--checkpoint',str(ready.with_suffix('.safetensors')),'--binder',str(root/'checkpoints'/f'binder_{seed}.safetensors'),'--outdir',str(root/'results')]
  with (root/'evidence'/f'EVAL_{kind}_{seed}.log').open('w') as f:subprocess.run(cmd,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)
  print('EVALUATED',kind,seed,flush=True)
print('MAIN_EVALUATION_COMPLETE',flush=True)
