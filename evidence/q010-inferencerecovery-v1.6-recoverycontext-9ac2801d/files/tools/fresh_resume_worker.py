"""Six actual interruption boundaries; prepare and restore in distinct interpreters.

Uses the supplied deterministic disposable test networks, not Q010 main weights.
All artifacts persist under an identified development directory. No optimizer calls.
"""
from pathlib import Path
import argparse,sys,json,hashlib,random,os
from unittest.mock import patch
import numpy as np
import torch
from q010c.protocol import ROOT,STAGING as S
A=S/'implementation_A'
sys.path.insert(0,str(A/'tests'))
from test_resumable_evaluation import ResumableEvaluationTests
from q010r.continuation import ContinuationIdentity,_encode
from q010r.resumable_evaluation import ResumableEvaluation
from q010r.conditions import condition_cells,make_seed_context,derive_seed_u64
from q010r.evaluation import capture_lifecycle_trace,make_condition_case,_maintenance_resolver_row

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(p,x):p.write_text(json.dumps(x,sort_keys=True,indent=2,allow_nan=False)+'\n')
def rig_at(root,kind,name):
 t=ResumableEvaluationTests(methodName='runTest');t.root=root;t.restore_count=0
 if kind=='lifecycle':
  cell=next(c for c in condition_cells() if c.stratum=='lifecycle')
  case=make_condition_case(cell,paired_seed=71,episode_index=0,arm='ordinary',split='lifecycle')
  rig=t.make_wrapper_rig(name,case,empty_lifecycle_store=True,model_id='resume_record_hop')
 else:rig=t.make_rig(name,reader_kind='attention' if kind=='attention' else 'record',noisy_start=kind=='maintenance')
 return t,rig

def noise_recipe(rig):
 context=make_seed_context(split='development',purpose='durability_noise_event',paired_seed=71,condition_id='m2k-resume-condition',episode_id=f"{rig['case'].case_id}-noise-0001",stage_index=None)
 seed=derive_seed_u64(**context)
 return {'schema':'q010r-durability-noise-v1','event_index':1,'rng_seed_context':context,'rng_seed_u64':seed,'sigma':.012,'fields':'both','injection_enabled':True,'live_write_event':None}

def start_boundary(t,rig,kind):
 s=rig['session']
 if kind=='transaction':s.prepare_transaction('correct',int(rig['case'].path_nodes[0]),int(rig['case'].path_nodes[2]),transaction_id='fresh-prepared-001')
 elif kind=='rng':
  r=noise_recipe(rig);s.begin_durability_event(1,rng=np.random.Generator(np.random.PCG64(r['rng_seed_u64'])),recipe=r)
 elif kind=='maintenance':
  s.begin_maintenance(1,'fresh-maintenance-001',policy='internal',fields='both')
  for _ in range(7):s.step_maintenance_row(_maintenance_resolver_row,value_restorer=_maintenance_resolver_row)
 elif kind in ('record','attention'):
  s.begin_query(rig['plan']);s.step_query(rig['plan'])
 elif kind=='lifecycle':
  original=ResumableEvaluation.commit_prepared_transaction;target=f"{rig['case'].case_id}-life-first-write"
  class Boundary(Exception):pass
  def stop(session,transaction_id):
   if transaction_id==target:raise Boundary('deliberate stop before first committed write')
   return original(session,transaction_id)
  with patch.object(ResumableEvaluation,'commit_prepared_transaction',new=stop):
   try:finish(t,rig,kind)
   except Boundary:pass
   else:raise AssertionError('requested real boundary not reached')
 else:raise ValueError(kind)

def finish(t,rig,kind):
 s=rig['session']
 if kind=='transaction':s.commit_prepared_transaction('fresh-prepared-001')
 elif kind=='rng':
  r=noise_recipe(rig)
  s.commit_durability_event(lambda st,op_id,rng:st.inject_noise(rng,.012,fields='both',operation_id=op_id,rng_seed_u64=r['rng_seed_u64'],rng_seed_context=r['rng_seed_context']),recipe=r)
 elif kind=='maintenance':
  while s.cursor['maintenance']['phase']=='rows':s.step_maintenance_row(_maintenance_resolver_row,value_restorer=_maintenance_resolver_row)
  s.commit_maintenance('fresh-maintenance-001',_maintenance_resolver_row,policy='internal',fields='both',value_restorer=_maintenance_resolver_row)
 elif kind in ('record','attention'):t._drain_query(rig)
 else:capture_lifecycle_trace(evidence=s.writer,readers=t.wrapper_readers(rig),paired_seed=71,arm='ordinary',split='lifecycle',continuation_session=s)

def snapshot(rig):
 s=rig['session'];st=s.store
 # Provenance branch paths are outside this numerical/evidence-prefix equality;
 # every actual evidence member is still hashed, with identical relative names.
 x={'arrays':st.actual_arrays(),'facts':sorted(st.facts.items()),'symbol_to_handle':sorted(st.symbol_to_handle.items()),'handle_to_symbol':sorted(st.handle_to_symbol.items()),'registered':sorted(st.registered_symbols),'source_events':st.source_events,'storage_ops':st.storage_ops,'sequences':[st._source_sequence,st._storage_sequence,st._fault_sequence,st._truth_revision],'prepared':{k:{'metadata':v.metadata(),'arrays':v.array_payload()} for k,v in st.prepared.items()},'rng':st.storage_rng.bit_generator.state,'cursor':s.cursor,'writer_rows':s.writer._all_stream_rows(),'evidence_members':{p.relative_to(s.writer.root).as_posix():sha(p) for p in sorted(s.writer.root.rglob('*')) if p.is_file()},'next_rng':{'python':random.random(),'numpy':np.random.random(3),'torch':torch.rand(3)}}
 return _encode(x)

def main():
 p=argparse.ArgumentParser();p.add_argument('phase',choices=['prepare','restore']);p.add_argument('kind',choices=['transaction','rng','maintenance','record','attention','lifecycle']);p.add_argument('--attempt',required=True);a=p.parse_args()
 torch.set_num_threads(1);torch.set_num_interop_threads(1);torch.use_deterministic_algorithms(True)
 root=S/'plan'/'runtime_tmp'/a.attempt/a.kind
 if a.phase=='prepare':
  root.mkdir(parents=True,exist_ok=False)
  t,ref=rig_at(root,a.kind,'reference');start_boundary(t,ref,a.kind);finish(t,ref,a.kind);write(root/'EXPECTED.json',snapshot(ref))
  t,part=rig_at(root,a.kind,'interrupted');start_boundary(t,part,a.kind)
  checkpoint=part['session'].last_checkpoint_path
  write(root/'INTERRUPTION.json',{'phase':'stopped_at_actual_boundary','kind':a.kind,'pid':os.getpid(),'checkpoint':str(checkpoint),'checkpoint_sha256':sha(checkpoint),'expected_sha256':sha(root/'EXPECTED.json'),'identity':part['session'].identity.as_dict(),'config':part['config'],'new_optimizer_updates':0})
 else:
  saved=json.loads((root/'INTERRUPTION.json').read_text());assert saved['pid']!=os.getpid();assert sha(saved['checkpoint'])==saved['checkpoint_sha256']
  t,rig=rig_at(root,a.kind,'restore-template')
  identity=ContinuationIdentity(**saved['identity'])
  resumed=ResumableEvaluation.restore(saved['checkpoint'],rig['store'],identity,resolved_config=saved['config'],reader_model=rig['model'],checkpoint_dir=root/'continued-checkpoints',checkpoint_prefix='restored',evidence_branch_root=root/'continued-evidence')
  rig.update(session=resumed,store=resumed.store,writer=resumed.writer);finish(t,rig,a.kind);actual=snapshot(rig);write(root/'ACTUAL.json',actual)
  expected=json.loads((root/'EXPECTED.json').read_text())
  if actual!=expected:
   write(root/'MISMATCH.json',{'differing_top_fields':[k for k in actual if actual[k]!=expected.get(k)]});raise AssertionError('fresh continuation disagrees')
  write(root/'PASS.json',{'status':'PASS','kind':a.kind,'prepare_pid':saved['pid'],'restore_pid':os.getpid(),'boundary':saved['checkpoint_sha256'],'actual_sha256':sha(root/'ACTUAL.json'),'expected_sha256':sha(root/'EXPECTED.json'),'new_optimizer_updates':0})
  print((root/'PASS.json').read_text())
if __name__=='__main__':main()
