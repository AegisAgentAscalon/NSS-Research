#!/usr/bin/env python3
"""Local research entry point. Never installs packages or downloads models.

All generated run outputs go outside this immutable source package by default.
This launcher does not promote a model, change the foundation, or start a daemon.
"""
from pathlib import Path
import argparse,datetime,hashlib,os,subprocess,sys,uuid
ROOT=Path(__file__).resolve().parent

def manifest():
 covered=set()
 for line in (ROOT/'MANIFEST.sha256').read_text().splitlines():
  digest,name=line.split('  ',1);p=(ROOT/name).resolve()
  if not p.is_relative_to(ROOT) or name in covered:raise ValueError('Unsafe/duplicate manifest path')
  if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:raise ValueError('Missing/changed: '+name)
  covered.add(name)
 actual={p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.suffix!='.pyc' and p.name!='MANIFEST.sha256'}
 if actual!=covered:raise ValueError('Unlisted or missing files: '+repr(actual^covered))
 print(f'PASS: {len(covered)} manifest-covered files',flush=True)

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('mode',choices=['checks','rescore','replay','train']);p.add_argument('--kind',default='record_hop',choices=['binder','record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4','exact_lookup']);p.add_argument('--seed',type=int,default=801);p.add_argument('--steps',type=int);p.add_argument('--output');a=p.parse_args()
 manifest()
 if a.steps is not None and a.steps<1:raise ValueError('Steps must be positive')
 try:import numpy,torch,safetensors
 except ImportError as e:print('Missing local dependency:',e,'\nNo packages were installed. See requirements.txt.',file=sys.stderr);return 2
 output=Path(a.output).resolve() if a.output else ROOT.parent/'NSS_Run_Output'/('BindingDepth006-'+datetime.datetime.now().strftime('%Y%m%d-%H%M%S')+'-'+uuid.uuid4().hex[:6])
 if output.is_relative_to(ROOT):raise ValueError('Choose an output directory outside the source package')
 output.mkdir(parents=True,exist_ok=False)
 env=dict(os.environ,OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',MKL_NUM_THREADS='1',PYTHONPATH=str(ROOT)+os.pathsep+os.environ.get('PYTHONPATH',''))
 if a.mode=='checks':cmd=[sys.executable,'-m','unittest','discover','-s','tests','-v']
 elif a.mode=='rescore':cmd=[sys.executable,'-m','nbr006.verify','--dir',str(ROOT/'results'),'--out',str(output/'RESCORE.json')]
 elif a.mode=='replay':
  if a.kind=='binder':raise ValueError('Binder is tested as part of a reader replay')
  if a.kind=='exact_lookup':cmd=[sys.executable,'-m','nbr006.exact_eval','--seed',str(a.seed),'--outdir',str(output)]
  else:cmd=[sys.executable,'-m','nbr006.eval','--kind',a.kind,'--seed',str(a.seed),'--checkpoint',str(ROOT/'checkpoints'/f'{a.kind}_{a.seed}.safetensors'),'--binder',str(ROOT/'checkpoints'/f'binder_{a.seed}.safetensors'),'--outdir',str(output)]
 elif a.mode=='train':
  if a.kind=='exact_lookup':raise ValueError('The exact control has no trainable parameters')
  cmd=[sys.executable,str(ROOT/'scripts/portable_train.py'),'--kind',a.kind,'--seed',str(a.seed),'--steps',str(a.steps or (1200 if a.kind=='binder' else 6000)),'--out',str(output/f'{a.kind}_{a.seed}.safetensors')]
 print('Output:',output,flush=True)
 with (output/'RUN.log').open('w') as f:result=subprocess.run(cmd,cwd=ROOT,env=env,stdout=f,stderr=subprocess.STDOUT)
 print((output/'RUN.log').read_text());print('Exit code:',result.returncode)
 if result.returncode==0 and a.mode=='replay':
  import numpy as np,json
  original=ROOT/'results'/f'{a.kind}_{a.seed}.npz';fresh=output/original.name
  with np.load(original,allow_pickle=False) as x,np.load(fresh,allow_pickle=False) as y:
   for key in x.files:np.testing.assert_array_equal(x[key],y[key])
  print('PASS: complete saved arrays match the packaged reference')
 manifest();return result.returncode
if __name__=='__main__':
 try:raise SystemExit(main())
 except (ValueError,FileExistsError,FileNotFoundError) as e:print('ERROR:',e,file=sys.stderr);raise SystemExit(2)
