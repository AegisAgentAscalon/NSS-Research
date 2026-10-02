"""CAP02: fixed-budget size-preparation diagnostic; see frozen PROTOCOL.md."""
from __future__ import annotations
import argparse,copy,gzip,hashlib,json,math,os,platform,resource,sys,time,traceback
from pathlib import Path
import numpy as np
import torch
from torch.nn import functional as F
from retained_common import worlds,compile_world,canonical,sha,write_json,model_hash,setup
from nss_hsa.reader import MaintenanceReader
from nss_hsa.hierarchy import Hierarchy,compile_plan,HierarchyError
from nss_hsa.records import prepare_worlds,compile_features
from cap01 import compare,StreamExecutor,full_reference
ROOT=Path(__file__).resolve().parents[1]
SEEDS=[8801,8802,8804];MODES=['dense','hsa'];ARMS=['S','M'];STEPS=96

def fsha(p):return sha(Path(p).read_bytes())
def now():
 from datetime import datetime,timezone
 return datetime.now(timezone.utc).isoformat()
def write_gzip(path,obj):
 raw=canonical(obj)
 with path.open('wb') as f:
  with gzip.GzipFile(filename='',mode='wb',fileobj=f,mtime=0) as z:z.write(raw)
def read_gzip(path):
 with gzip.open(path,'rt') as f:return json.load(f)
def identity(w):return sha(canonical({k:v for k,v in w.items() if k!='id'}))
def exact(w):
 # Independent scalar target rule; does not call retained_common.oracle.
 ans=[]
 for t,completed in enumerate(w['progress']):
  if w['freeze']:ans.append(0)
  elif completed:ans.append(1)
  elif all(w['progress'][d] for d in w['deps'][t]):ans.append(2)
  else:ans.append(3)
 return np.asarray(ans,dtype=np.int64)
def make_world(seed,n,freeze=None):
 w=worlds(seed,1,n)[0];rng=np.random.default_rng(seed+701);width=math.ceil(math.sqrt(n))
 for t in range(n):
  ids=[j for j in range(n) if j//width!=t//width]
  w['deps'][t]=[int(a) for a in rng.choice(ids,2,replace=False)]
 if freeze is not None:w['freeze']=int(freeze)
 targets=sorted(int(a) for a in rng.choice(n,8,replace=False))
 return {'world':w,'targets':targets,'n':n,'seed':seed,'identity':identity(w)}
def prep():
 start=time.perf_counter();train={'S':[],'M':[]}
 for step in range(STEPS):
  small=[make_world(1301001+step*100+j,8) for j in range(4)]
  n=[8,32,128][step%3]
  mixed=copy.deepcopy(small) if n==8 else [make_world(1501001+step*100+j,n) for j in range(4)]
  train['S'].append(small);train['M'].append(mixed)
 ev=[]
 for n in [8,32,128,512]:
  for frozen,count in [(0,8 if n==512 else 32),(1,2 if n==512 else 8)]:
   for j in range(count):
    r=make_world(2000000+n*1000+frozen*100+j,n,freeze=frozen)
    r.update({'id':f'n{n}_f{frozen}_{j:03d}','frozen':bool(frozen),'stratum':'stress' if n==512 else 'primary'})
    ev.append(r)
 trids={r['identity'] for a in train.values() for batch in a for r in batch};evids={r['identity'] for r in ev}
 assert len(evids)==len(ev) and not trids&evids
 write_gzip(ROOT/'fixtures/train.json.gz',train);write_gzip(ROOT/'fixtures/confirmation.json.gz',ev)
 hist=set();hist_count=0
 import zipfile
 with zipfile.ZipFile('/mnt/data/NSS_NBR02_SH01_Execution_v0.1.zip') as z:
  for name in z.namelist():
   if name.endswith('_identities.json'):
    d=json.loads(z.read(name));h=d.get('fingerprints',[]);hist.update(h);hist_count+=len(h)
 assert not (trids|evids)&hist
 write_json(ROOT/'results/PREPARATION.json',{'seconds':time.perf_counter()-start,'train_unique_worlds':len(trids),
   'confirmation_worlds':len(ev),'train_confirmation_overlap':len(trids&evids),'historical_fingerprints_checked':hist_count,
   'historical_exact_overlap':len((trids|evids)&hist),'sizes':[8,32,128,512],
   'confirmation_inputs_common_to_all_models':True,'training_label_positions_per_arm':STEPS*4*8})
 print('prepared',len(trids),'unique train worlds;',len(ev),'confirmation worlds',flush=True)
def new_model(seed,mode,arm='U'):
 p=ROOT/'parents'/f'{seed}_{mode}.pt' if arm=='U' else ROOT/'checkpoints'/f'{seed}_{mode}_{arm}_0096.pt'
 cp=torch.load(p,map_location='cpu',weights_only=False)
 m=MaintenanceReader();m.load_state_dict(cp['model']);return m

def batchify(records):
 ws=[r['world'] for r in records];x,spec=prepare_worlds(ws);plan=compile_plan(spec)
 y=torch.from_numpy(np.stack([exact(w) for w in ws]));ids=torch.tensor([r['targets'] for r in records],dtype=torch.int64)
 return x,plan,y,ids

def forward(m,x,plan,mode):return m(x,plan,'packed' if mode=='hsa' else 'full_dense')
def optimizer(m):return torch.optim.AdamW(m.parameters(),lr=.0005,betas=(.9,.999),eps=1e-8,weight_decay=.01,foreach=False,fused=False)
def do_update(m,opt,prepared,mode):
 x,p,y,ids=prepared;opt.zero_grad(set_to_none=True);out=forward(m,x,p,mode)
 chosen=out.gather(1,ids[:,:,None].expand(-1,-1,4));truth=y.gather(1,ids)
 loss=F.cross_entropy(chosen.reshape(-1,4),truth.reshape(-1));
 if not torch.isfinite(loss):raise RuntimeError('NONFINITE_LOSS')
 loss.backward();gn=torch.nn.utils.clip_grad_norm_(m.parameters(),1.,error_if_nonfinite=True);opt.step()
 if any(not torch.isfinite(a).all() for a in m.parameters()):raise RuntimeError('NONFINITE_PARAMETER')
 return {'loss':float(loss.detach()),'preclip_gradient_norm':float(gn),'correct_preupdate':int((chosen.argmax(-1)==truth).sum()),'labels':truth.numel(),'n':p.tasks}

def save_model(m,opt,seed,mode,arm,step,path=None):
 path=path or ROOT/'checkpoints'/f'{seed}_{mode}_{arm}_{step:04d}.pt'
 cp={'model':m.state_dict(),'optimizer':None if opt is None else opt.state_dict(),'seed':seed,'mode':mode,'arm':arm,
     'completed_updates':step,'model_hash':model_hash(m),'torch_rng':torch.get_rng_state(),
     'parent_file_sha256':fsha(ROOT/'parents'/f'{seed}_{mode}.pt')}
 tmp=path.with_suffix('.tmp');torch.save(cp,tmp);os.replace(tmp,path)
 return fsha(path)

def preflight():
 start=time.perf_counter();tests=[];apps=0;torch.manual_seed(2700001)
 def check(name,fn):
  t=time.perf_counter()
  try:
   value=fn();tests.append({'name':name,'pass':True,'detail':value,'seconds':time.perf_counter()-t})
  except Exception as e:
   tests.append({'name':name,'pass':False,'error':str(e),'trace':traceback.format_exc()})
   write_json(ROOT/'failures/PREFLIGHT.json',tests);raise
 def encoding(n):
  r=make_world(2800000+n,n);x=compile_features(r['world']).numpy();old,_,_=compile_world(r['world'])
  assert np.array_equal(x,old);return {'values':x.size}
 for n in [8,32,128,512]:check('exact_encoding_'+str(n),lambda n=n:encoding(n))
 def gradients(n):
  r=make_world(2810000+n,n);x,p,y,ids=batchify([r]);a=new_model(8801,'hsa');b=copy.deepcopy(a)
  oa=a(x,p,'packed');ob=b(x,p,'masked_reference');q=compare(oa.detach(),ob.detach());assert not q['violations']
  F.cross_entropy(oa.reshape(-1,4),y.reshape(-1)).backward();F.cross_entropy(ob.reshape(-1,4),y.reshape(-1)).backward()
  ag=np.concatenate([v.grad.numpy().ravel() for v in a.parameters()]);bg=np.concatenate([v.grad.numpy().ravel() for v in b.parameters()]);g=compare(ag,bg);assert not g['violations']
  return {'outputs':q,'gradients':g}
 for n in [8,32]:check('packed_masked_gradient_'+str(n),lambda n=n:gradients(n))
 def alllabels():
  from retained_common import oracle
  for n in [8,32,128,512]:
   for freeze in [0,1]:
    r=make_world(2820000+n+freeze,n,freeze);assert np.array_equal(exact(r['world']),oracle(r['world']))
  return {'worlds':8}
 check('independent_scorer',alllabels)
 def resume_updates():
  nonlocal apps
  r=make_world(2830000,8);prepared=batchify([r,r,r,r]);m=new_model(8801,'hsa');original=model_hash(new_model(8801,'hsa'));opt=optimizer(m)
  do_update(m,opt,prepared,'hsa');apps+=1
  cp=ROOT/'audit/preflight_resume.pt';save_model(m,opt,8801,'hsa','engineering',1,cp)
  do_update(m,opt,prepared,'hsa');apps+=1;expected=model_hash(m)
  d=torch.load(cp,weights_only=False);z=new_model(8801,'hsa');z.load_state_dict(d['model']);o=optimizer(z);o.load_state_dict(d['optimizer']);torch.set_rng_state(d['torch_rng'])
  do_update(z,o,prepared,'hsa');apps+=1;assert model_hash(z)==expected and model_hash(new_model(8801,'hsa'))==original
  cp.unlink();return {'applications':3,'parameter_replay_exact':True,'parent_unchanged':True}
 check('optimizer_resume_isolation',resume_updates)
 def baddep():
  r=make_world(2840000,8);r['world']['deps'][0]=[0,1]
  try:batchify([r])
  except HierarchyError:return {'detected':True}
  raise AssertionError('missed invalid dependency')
 check('fault_invalid_dependency',baddep)
 def nonfinite():
  r=make_world(2840001,8);r['world']['nuisance'][0][0]=float('nan')
  try:batchify([r])
  except HierarchyError:return {'detected':True}
  raise AssertionError('missed nonfinite')
 check('fault_nonfinite_input',nonfinite)
 def mutation():
  r=make_world(2840002,8);x,p,_,_=batchify([r]);p.buckets[0].indices[0,0,0]+=1
  try:p.validate_tensors()
  except HierarchyError:return {'detected':True}
  raise AssertionError('missed plan mutation')
 check('fault_plan_corruption',mutation)
 def counts():
  t=read_gzip(ROOT/'fixtures/train.json.gz');assert len(t['S'])==len(t['M'])==96
  for i in range(96):
   for a in ARMS:assert len(t[a][i])==4 and all(len(r['targets'])==8 for r in t[a][i])
   if i%3==0:assert t['S'][i]==t['M'][i]
  return {'applications':96,'labels_per_update':32,'identical_small_steps':32}
 check('paired_schedule_labels',counts)
 write_json(ROOT/'results/PREFLIGHT.json',{'status':'PASS','tests':tests,'optimizer_applications':apps,'seconds':time.perf_counter()-start})
 print('preflight',len(tests),'passed;',apps,'disposable updates',flush=True)

def lock():
 assert json.loads((ROOT/'results/PREFLIGHT.json').read_text())['status']=='PASS'
 paths=[ROOT/'PROTOCOL.md']+sorted((ROOT/'source').rglob('*.py'))+sorted((ROOT/'parents').glob('*'))+sorted((ROOT/'fixtures').glob('*'))
 write_json(ROOT/'SOURCE_FIXTURE_LOCK.json',{'utc':now(),'files':{str(p.relative_to(ROOT)):{'bytes':p.stat().st_size,'sha256':fsha(p)} for p in paths},
  'python':sys.version,'torch':torch.__version__,'numpy':np.__version__,'platform':platform.platform(),'threads':torch.get_num_threads(),'main_updates':1152})
 print('locked',len(paths),'source/input objects',flush=True)
def verify_lock():
 d=json.loads((ROOT/'SOURCE_FIXTURE_LOCK.json').read_text())
 for s,r in d['files'].items():
  if fsha(ROOT/s)!=r['sha256']:raise RuntimeError('SOURCE_LOCK_CHANGED:'+s)
 return len(d['files'])
def guard(start):
 prior=sum(json.loads(p.read_text())['seconds'] for pattern in ['TRAIN_PROCESS_*.json','EVAL_PROCESS_*.json','STREAM_*.json'] for p in (ROOT/'results').glob(pattern))
 if prior+time.perf_counter()-start>600:raise RuntimeError('RESOURCE_TIME_STOP')
 if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024>2*2**30:raise RuntimeError('RESOURCE_RSS_STOP')
 if sum(p.stat().st_size for p in ROOT.rglob('*') if p.is_file())>96*2**20:raise RuntimeError('RESOURCE_STORAGE_STOP')

def train(seed):
 verify_lock();start=time.perf_counter();data=read_gzip(ROOT/'fixtures/train.json.gz');prepared={a:[batchify(b) for b in data[a]] for a in ARMS};prep_s=time.perf_counter()-start
 for mode in MODES:
  for arm in ARMS:
   name=f'{seed}_{mode}_{arm}';outpath=ROOT/f'results/TRAIN_{name}.json'
   if outpath.exists():raise RuntimeError('DO_NOT_REPEAT_COMPLETED_BRANCH:'+name)
   m=new_model(seed,mode);m.train();opt=optimizer(m);initial=model_hash(m);torch.manual_seed(2900000+seed);done=0;t=time.perf_counter();status='RUNNING'
   save_model(m,None,seed,mode,arm,0)
   trace=ROOT/f'results/loss_{name}.jsonl'
   try:
    with trace.open('x') as f:
     for i,b in enumerate(prepared[arm],1):
      v=do_update(m,opt,b,mode);done=i;v.update({'step':i,'seed':seed,'mode':mode,'arm':arm});f.write(canonical(v).decode()+'\n');f.flush()
      if i%24==0:save_model(m,opt,seed,mode,arm,i);guard(start)
    status='COMPLETE'
   except Exception as e:
    write_json(ROOT/f'failures/TRAIN_{name}.json',{'error':str(e),'trace':traceback.format_exc(),'known_updates':done});status='TECHNICAL_STOP';raise
   finally:
    write_json(outpath,{'status':status,'seed':seed,'mode':mode,'arm':arm,'updates':done,'seconds':time.perf_counter()-t,
      'initial_hash':initial,'final_hash':model_hash(m),'labels':done*32,'source_worlds':done*4})
   print('trained',name,done,flush=True)
 write_json(ROOT/f'results/TRAIN_PROCESS_{seed}.json',{'seconds':time.perf_counter()-start,'precompile_seconds':prep_s,
  'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024})
 verify_lock()

def evaluate(seed):
 verify_lock()
 for s in SEEDS:
  for m in MODES:
   for a in ARMS:assert json.loads((ROOT/f'results/TRAIN_{s}_{m}_{a}.json').read_text())['status']=='COMPLETE'
 data=read_gzip(ROOT/'fixtures/confirmation.json.gz');start=time.perf_counter();prepared=[batchify([r]) for r in data]
 for mode in MODES:
  for arm in ['U','S','M']:
   m=new_model(seed,mode,arm);m.eval();rows=[];save={};t=time.perf_counter()
   with torch.inference_mode():
    for r,(x,plan,y,ids) in zip(data,prepared):
     logits=forward(m,x,plan,mode)[0].numpy().copy();all_y=y[0].numpy();sel=np.asarray(r['targets']);p=logits.argmax(-1)
     assert np.isfinite(logits).all()
     prefix=r['id'];save[prefix+'_logits']=logits;save[prefix+'_target']=all_y;save[prefix+'_selected']=sel
     rows.append({'id':prefix,'n':r['n'],'frozen':r['frozen'],'world_identity':r['identity'],
      'selected_correct':int((p[sel]==all_y[sel]).sum()),'selected_total':len(sel),'whole_selected_correct':bool(np.array_equal(p[sel],all_y[sel])),
      'all_correct':int((p==all_y).sum()),'all_total':len(all_y),'all_world_correct':bool(np.array_equal(p,all_y)),
      'false_complete':int(((p[sel]==1)&(all_y[sel]!=1)).sum()),'false_ready':int(((p[sel]==2)&(all_y[sel]!=2)).sum())})
   path=ROOT/f'results/PRED_{seed}_{mode}_{arm}.npz'
   if path.exists():raise RuntimeError('DO_NOT_REPLACE_EVALUATION')
   np.savez_compressed(path,**save)
   write_json(ROOT/f'results/EVAL_{seed}_{mode}_{arm}.json',{'seed':seed,'mode':mode,'arm':arm,'model_hash':model_hash(m),'seconds':time.perf_counter()-t,'worlds':rows})
   guard(start);print('evaluated',seed,mode,arm,len(rows),flush=True)
 write_json(ROOT/f'results/EVAL_PROCESS_{seed}.json',{'seconds':time.perf_counter()-start,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024})
 verify_lock()

def streaming(seed):
 from retained_common import Reader
 data=read_gzip(ROOT/'fixtures/confirmation.json.gz');results=[];start=time.perf_counter()
 for mode in MODES:
  cp=torch.load(ROOT/f'checkpoints/{seed}_{mode}_M_0096.pt',weights_only=False,map_location='cpu');m=Reader();m.load_state_dict(cp['model']);m.eval()
  for n in [32,128]:
   r=next(r for r in data if r['n']==n and not r['frozen']);ref=full_reference(m,r['world'],mode,r['targets'])
   spool=ROOT/f'audit/stream_{seed}_{mode}_n{n}';ex=StreamExecutor(m,r['world'],r['targets'],mode,'segmented',32,spool,scope='CAP02')
   ex.advance();assert ex.completed
   # Executor provides final scores from its saved numerical stage arrays.
   stage1=np.load(ex.h1_file);stage2=np.load(ex.h2_file)
   with torch.inference_mode():logits=m.head(m.norm(torch.from_numpy(stage2[list(ex.closure[2])].copy()))).numpy()
   checks={'stage1':compare(stage1[list(ex.closure[1])],ref['stage1'][list(ex.closure[1])]),
           'stage2':compare(stage2[list(ex.closure[2])],ref['stage2'][list(ex.closure[2])]),'logits':compare(logits,ref['logits'])}
   with np.load(ROOT/f'results/PRED_{seed}_{mode}_M.npz') as saved:
    prepared_logits=saved[r['id']+'_logits'][r['targets']]
   checks['resident_backend_logits']=compare(prepared_logits,ref['logits'])
   row={'seed':seed,'mode':mode,'n':n,'checks':checks,'class_disagreements':int((logits.argmax(-1)!=ref['logits'].argmax(-1)).sum()),
        'selected_positions_peak':ex.stats['peak_selected_positions'],'stats':dict(ex.stats),'cap':32}
   np.savez_compressed(ROOT/f'audit/STREAM_{seed}_{mode}_{n}.npz',stream_logits=logits,source_logits=ref['logits'],resident_logits=prepared_logits)
   results.append(row);guard(start)
   import shutil;shutil.rmtree(spool)
 write_json(ROOT/f'results/STREAM_{seed}.json',{'seconds':time.perf_counter()-start,'cases':results})
 print('stream checks',seed,len(results),sum(sum(v['violations'] for v in r['checks'].values()) for r in results),'violations',flush=True)

if __name__=='__main__':
 setup();p=argparse.ArgumentParser();p.add_argument('command',choices=['prep','preflight','lock','train','evaluate','stream']);p.add_argument('--seed',type=int);args=p.parse_args()
 try:
  {'prep':prep,'preflight':preflight,'lock':lock,'train':lambda:train(args.seed),'evaluate':lambda:evaluate(args.seed),'stream':lambda:streaming(args.seed)}[args.command]()
 except Exception as e:
  path=ROOT/f'failures/COMMAND_{args.command}_{args.seed}_{time.time_ns()}.json'
  write_json(path,{'command':args.command,'seed':args.seed,'utc':now(),'error':str(e),'trace':traceback.format_exc()});raise
