"""Fresh-interpreter continuation of80 actual model/state configurations."""
from pathlib import Path
import sys,argparse,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import torch
from nbr01_empty.models import *
from nbr01_empty.snapshot import save,restore
from nbr01_empty.util import setup,write_json,digest_tensors
setup()
def step(m,g,n):
 for _ in range(n):m.maintain(.15*torch.randn(m.z.shape,generator=g))
def finish(m,g):
 m.event('write',0,5,score=.5001);step(m,g,75);m.event('write',0,6);step(m,g,64)
 m.event('clear',0);step(m,g,32);m.event('write',0,1);step(m,g,64)
 return {'z':m.z,'rng':g.get_state(),'prediction':m.read(),**({'presence':m.presence} if m.presence is not None else {})}
p=argparse.ArgumentParser();p.add_argument('action',choices=('create','verify'));a=p.parse_args()
if a.action=='create':
 records=[]
 for seed in range(301,306):
  for mode in MODES:
   rep,repair=load_components(ROOT,seed,mode)
   for cut in ('before_first_write','after_clear'):
    m=Memory(rep,mode,repair,batch=4,scope='resume-test');g=torch.Generator().manual_seed(12_000_000+seed)
    m.event('write',1,2);m.event('write',2,3);step(m,g,25)
    if cut=='after_clear':m.event('write',0,4);step(m,g,64);m.event('clear',0);step(m,g,32)
    relative=f'evidence/snapshots/{mode}_rep{seed}_{cut}';save(m,g,ROOT/relative)
    final=finish(m,g);records.append(dict(seed=seed,mode=mode,cut=cut,path=relative,final_digest=digest_tensors(final),events=m.events,rounds=m.rounds,prediction=final['prediction'].tolist()))
 write_json(ROOT/'evidence/RESUME_EXPECTATIONS.json',{'records':records,'count':len(records)});print('created',len(records))
else:
 records=json.loads((ROOT/'evidence/RESUME_EXPECTATIONS.json').read_text())['records'];verified=[]
 for r in records:
  rep,repair=load_components(ROOT,r['seed'],r['mode']);m=Memory(rep,r['mode'],repair,batch=4,scope='resume-test');g=torch.Generator()
  restore(m,g,ROOT/r['path']);final=finish(m,g)
  if digest_tensors(final)!=r['final_digest'] or m.events!=r['events'] or m.rounds!=r['rounds']:raise RuntimeError('Resume mismatch '+r['path'])
  verified.append(r['path'])
 write_json(ROOT/'evidence/RESUME_VERIFICATION.json',{'status':'PASS','fresh_interpreter':True,'cases':len(verified),'verified':verified,'scope':'Research numerical state and RNG; not OS power-loss or production Runtime durability.'});print('verified',len(verified))
