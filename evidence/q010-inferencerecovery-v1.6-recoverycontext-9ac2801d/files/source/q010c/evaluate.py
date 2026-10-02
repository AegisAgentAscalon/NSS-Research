"""Columnar Q010 capture, preserving every declared case/stage, not a smaller test."""
from __future__ import annotations
from pathlib import Path
from typing import Any,Mapping
import argparse,copy,datetime,hashlib,json,os,time,resource,shutil
import numpy as np,torch
from q010r.conditions import condition_cells
from q010r.models import load_parent_reader,model_state_hash,AttentionPointerReader
from q010r import evaluation as ev
from q010c.protocol import ROOT,STAGING,SEEDS,ROLES,roster,sha,digest
from q010c.batch_core import *

def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def write_json(path:Path,v:Any):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('x') as f:json.dump(v,f,sort_keys=True,indent=2,allow_nan=False);f.write('\n')
def write_npz(path:Path,a:Mapping[str,np.ndarray])->dict:
 if path.exists():raise FileExistsError(path)
 for k,v in a.items():
  if not isinstance(v,np.ndarray) or v.dtype.hasobject:raise ValueError(('invalid array',k))
 with path.open('xb') as f:np.savez_compressed(f,**a);f.flush();os.fsync(f.fileno())
 return {'path':path.name,'bytes':path.stat().st_size,'sha256':sha(path),'array_digest':digest_arrays(a),'arrays':{k:{'shape':list(v.shape),'dtype':v.dtype.str} for k,v in sorted(a.items())}}

def capture_frame(state,symbols,cases,query,source_ids,readers,*,depth,feedback_mode)->dict[str,np.ndarray]:
 raw=arrays_of(state);out={'state__'+k:v for k,v in raw.items()};out['symbols']=np.asarray(symbols,np.int64);out['initial_query']=np.asarray(query,np.float32);out['initial_source_ids']=np.asarray(source_ids,np.int64)
 for reader_id,m in readers.items():
  trace=read_batch(state,out['symbols'],out['initial_query'],out['initial_source_ids'],m,depth=depth,feedback_mode=feedback_mode,reader_id=reader_id)
  out.update({f'{reader_id}__{k}':v for k,v in trace.items()})
 return out

def load_readers(seed:int, root:Path, *, roster_sha256:str)->tuple[dict,dict]:
 from q010c.train import load_payload,verify_completed_fit
 from q010c.roster import read_roster
 from q010c import execution_io as io
 from q010r import training
 if seed not in SEEDS:raise ValueError("unknown main paired seed")
 root=Path(root).resolve();locked=read_roster(root,roster_sha256)
 models={};identities={}
 for role in ('inherited','cap_only'):
  model,receipt=load_parent_reader(seed-400,cap=80. if role=='inherited' else 20000.)
  rid=f'inherited_{seed-400}' if role=='inherited' else role
  models[rid]=model;identities[rid]=io.portable_paths(receipt,{'PACKAGE':ROOT})
 for role,arm in (('ordinary','ordinary_continuation'),('near','close_identity_continuation'),('attention','task_adapted_attention')):
  row=next(x for x in locked['fits'] if x['seed']==seed and x['role']==role)
  fit=root/f'seed{seed}'/role
  if (io.verify_file(root,row['fit_config']) != fit/'FIT_CONFIG.json'
      or io.verify_file(root,row['completion']) != fit/'COMPLETE.json'):
   raise ValueError('roster artifact paths do not belong to the declared fit')
  config=io.read_json(fit/'FIT_CONFIG.json')
  complete=verify_completed_fit(fit,binding=io.digest(config))
  if (config.get('seed')!=seed or config.get('role')!=role or config.get('arm')!=arm
      or config.get('attempt_role')!='main' or complete.get('attempt_role')!='main'):
   raise ValueError('wrong seed, arm or fit/reproduction role')
  publication=io.contained(fit,complete['publication'])
  checkpoint=publication/'checkpoint_step_006000.pt'
  manifest=io.read_json(publication/'fit_manifest.json')
  payload=load_payload(checkpoint)
  identity=payload.get('identity',{});cfg=identity.get('config',{})
  if (payload.get('optimizer_step')!=6000 or len(payload.get('trace',[]))!=6000
      or payload.get('stream_state',{}).get('next_batch_index')!=6000
      or identity.get('paired_seed')!=seed or identity.get('arm')!=arm
      or cfg.get('fit_role')!='main' or cfg.get('study_phase')!='main_fits'
      or manifest.get('paired_seed')!=seed or manifest.get('arm')!=arm
      or manifest.get('status')!='complete' or manifest.get('completed_steps')!=6000
      or identity.get('protocol_sha256')!=locked['protocol_sha256']
      or complete.get('source_lock_sha256')!=locked['source_lock_sha256']
      or manifest.get('identity')!=identity):
   raise ValueError('checkpoint/config/seed/phase/manifest mismatch')
  model=AttentionPointerReader() if role=='attention' else load_parent_reader(seed-400,cap=20000.)[0]
  model.load_state_dict(payload['model_state'],strict=True);model.eval()
  strict=training._hash_tensor_map(model.state_dict());public=model_state_hash(model)
  if (strict!=row['strict_sha256'] or public!=row['public_sha256']
      or strict!=complete['final_strict_sha256'] or public!=manifest['final_weight_sha256']):
   raise ValueError('strict/public model fingerprint mismatch')
  models[role]=model
  identities[role]={'checkpoint':io.file_info(root,checkpoint),'paired_seed':seed,'arm':arm,
                    'strict_sha256':strict,'public_sha256':public,'steps':6000,
                    'roster_sha256':roster_sha256,
                    'fit_manifest':io.file_info(root,publication/'fit_manifest.json')}
 models['exact_owner']=None
 identities['exact_owner']={'kind':'privileged actual-owner traversal',
                            'source_sha256':sha(Path(__file__).with_name('batch_core.py'))}
 return models,identities

def capture_seed(seed:int,readers:Mapping[str,Any],identities:Mapping[str,Any],output:Path,*,split:str='heldout',selected_cells:list[str]|None=None,development_count:int|None=None)->dict:
 if output.exists():raise FileExistsError(output)
 output.mkdir(parents=True);t0=time.monotonic();chunks=[];chains=stages=0;noise_events=maintenance=livewrites=0
 cells=condition_cells();before={r:model_state_hash(m) for r,m in readers.items() if m is not None}
 write_json(output/'START.json',{'utc':utc(),'seed':seed,'split':split,'scope':('MAIN_CONDITION_GROUP' if selected_cells is not None else 'FULL_MATRIX') if split=='heldout' and development_count is None else 'DEVELOPMENT_SUBSET','readers':identities,'selected_cells':selected_cells,'development_count':development_count,'batching':'independent cases; all allowed stages','status':'STARTED'})
 life=None
 for cell in cells:
  if selected_cells is not None and cell.condition_id not in selected_cells:continue
  d=output/cell.condition_id;d.mkdir();ct=time.monotonic();count=0
  if cell.stratum=='lifecycle':
   if life is None:life=collect_lifecycle(seed,split='lifecycle' if split=='heldout' else 'development')
   frame=next(x for x in life.frames if x['condition_id']==cell.condition_id)
   state=state_from_arrays(frame['raw'],scope=frame['scope'],mode=frame['mode'],tick=frame['tick']);c=frame['case'];symbols=frame['symbols'][None];query=frame['query'].reshape(1,17);ids=np.array([frame['source_id']],np.int64)
   raw=capture_frame(state,symbols,[c],query,ids,readers,depth=1,feedback_mode='direct')
   meta={'condition_id':cell.condition_id,'seed':seed,'split':'lifecycle' if split=='heldout' else split,'checkpoint':None,'depth':1,'feedback_mode':'direct','cases':[case_meta(c)],'queries':[frame['recipe']],'episode_ids':[frame['episode_id']],'events':frame['events'],'operations':frame['operations'],'live_facts':[[list(x) for x in sorted(frame['facts'].items())]],'state_scope':frame['scope'],'state_mode':frame['mode'],'state_tick':frame['tick'],'readers':list(readers)}
   info=write_npz(d/'frame.npz',raw);write_json(d/'meta.json',meta);chunks.append({'condition':cell.condition_id,'file':str((d/'frame.npz').relative_to(output)),'meta':str((d/'meta.json').relative_to(output)),'meta_sha256':sha(d/'meta.json'),**info});chains+=len(readers);stages+=len(readers);count=1
  else:
   cases=prepare_cases(cell,seed,split=split)
   if development_count is not None:
    # Explicit development slice with both support strata, never used in main.
    n=development_count;cases=cases[:n//2]+cases[cell.episodes_per_seed//2:cell.episodes_per_seed//2+n-n//2]
   bs=BatchStore.initialize(cases,enabled=bool(cell.factors.get('state_enabled',True)));faults=bs.fault(cell,seed,split)
   checkpoints=list(cell.factors.get('evaluation_checkpoints',[]));dur=bool(checkpoints);depth=int(cell.factors.get('allowed_depth',min(int(cell.factors.get('path_length',3)),4)));feedback=str(cell.factors.get('feedback_mode','assisted'))
   if feedback=='direct':depth=1
   local_cp=checkpoints if checkpoints else [None];pending=0;event_seeds=[];event_digests=[]
   def snap(cp):
    nonlocal chains,stages,count
    q,ids,recipes=prepare_queries(cases,cell,seed,split=split,checkpoint=cp)
    raw=capture_frame(bs.state,bs.symbols,cases,q,ids,readers,depth=depth,feedback_mode=feedback)
    name='frame' if cp is None else f'cp{cp:04d}'
    raw['event_seed_prefix']=np.asarray(event_seeds,np.uint64).T.copy() if event_seeds else np.empty((len(cases),0),np.uint64)
    raw['event_digest_prefix']=np.array(event_digests,dtype='U64')
    meta={'condition_id':cell.condition_id,'seed':seed,'split':split,'checkpoint':cp,'depth':depth,'feedback_mode':feedback,'cases':[case_meta(c) for c in cases],'queries':recipes,'episode_ids':[f'{c.case_id}-cp{cp:04d}' if cp is not None else f'{cell.condition_id}-s{seed}-e{case_index(c):03d}' for i,c in enumerate(cases)],'faults':faults,'state_scope':bs.state.scope,'state_mode':bs.state.mode,'state_tick':bs.state.tick,'readers':list(readers),'event_count':0 if cp is None else cp}
    info=write_npz(d/f'{name}.npz',raw);write_json(d/f'{name}.json',meta);chunks.append({'condition':cell.condition_id,'file':str((d/f'{name}.npz').relative_to(output)),'meta':str((d/f'{name}.json').relative_to(output)),'meta_sha256':sha(d/f'{name}.json'),**info});chains+=len(cases)*len(readers);stages+=len(cases)*len(readers)*depth;count+=1
   if not checkpoints:snap(None)
   else:
    if checkpoints[0]==0:snap(0);pending=1
    for event in range(1,int(cell.factors.get('noise_events',0))+1):
     inject=bool(cell.factors.get('noise_injection_enabled',cell.factors.get('state_enabled',True)))
     if inject:
      seeds=bs.noise_event(cell,seed,event,split);noise_events+=len(cases)
     else:seeds=np.zeros(len(cases),np.uint64)
     event_seeds.append(seeds)
     cadence=cell.factors.get('maintenance_cadence')
     if bool(cell.factors.get('maintenance_enabled',False)) and cadence and event%int(cadence)==0:bs.maintain();maintenance+=len(cases)
     live=cell.factors.get('unrelated_live_write_every')
     if live and event%int(live)==0:bs.unrelated_write();livewrites+=len(cases)
     # Hash actual state after each event, including effects of maintenance/write.
     event_digests.append(digest_arrays(bs.raw()))
     if pending<len(checkpoints) and event==checkpoints[pending]:snap(event);pending+=1
    if pending!=len(checkpoints):raise AssertionError('missed durability checkpoint')
  if time.monotonic()-t0>3600:raise RuntimeError('predeclared evaluation wall cap')
  if resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024>1879048192:raise RuntimeError('predeclared process memory cap')
  if shutil.disk_usage(output).free<2147483648:raise RuntimeError('predeclared disk floor')
  print(json.dumps({'cell':cell.condition_id,'seed':seed,'frames':count,'seconds':time.monotonic()-ct,'chains_so_far':chains}),flush=True)
 after={r:model_state_hash(m) for r,m in readers.items() if m is not None}
 if before!=after:raise AssertionError('evaluation mutated weights')
 receipt={'status':'CAPTURED_NOT_YET_INDEPENDENTLY_VERIFIED','seed':seed,'split':split,'cells':len(set(x['condition'] for x in chunks)),'chunks':chunks,'chains':chains,'logical_stage_evaluations':stages,'actual_noise_events':noise_events,'maintenance_sweeps':maintenance,'qualified_unrelated_writes':livewrites,'seconds':time.monotonic()-t0,'peak_rss_bytes':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss*1024,'weights_before':before,'weights_after':after,'utc':utc()}
 write_json(output/'CAPTURE.json',receipt);return receipt

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--seed',type=int,required=True);p.add_argument('--fits',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--split',choices=['heldout'],default='heldout');p.add_argument('--roster-sha256',required=True);a=p.parse_args();torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True);r,i=load_readers(a.seed,a.fits,roster_sha256=a.roster_sha256);capture_seed(a.seed,r,i,a.output,split=a.split)
