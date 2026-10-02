"""Replay every case in a fresh interpreter and independently recompute scores.
This is internal reproducibility, not an external scientific replication.
"""
from pathlib import Path
import sys,json,tempfile,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import torch,numpy as np
from safetensors.torch import load_file
from nbr01_empty.evaluate import evaluate_one
from nbr01_empty.util import sha,write_json,digest_tensors
from nbr01_empty.models import MODES

def expected(row,n):
 b=np.arange(n)%8;y=np.full((n,4),8,dtype=np.int64);y[:,1]=b;y[:,2]=(b+3)%8
 case=row['case']
 if case=='global_clear':return np.full((n,4),8,dtype=np.int64)
 if case=='shock':
  g=torch.Generator().manual_seed(10_000_000+row['seed']+int(row['sigma']*100));return torch.randint(0,9,(256,4),generator=g).numpy()
 if case=='lifecycle':
  phase=row['phase']
  if phase in ('first_write','correction','rewritten'):y[:,0]=(b+{'first_write':1,'correction':2,'rewritten':4}[phase])%8
 elif case=='extended_first_write':y[:,0]=(b+2)%8
 elif case=='attenuated_write':y[:,0]=(b+1)%8
 elif case=='metadata_repaired_by_events':y[:,1]=(b+5)%8
 elif case not in ('extended_empty','metadata_fault'):raise ValueError(case)
 return y

start=time.perf_counter()
for file,h in json.loads((ROOT/'spec/REGISTRATION.json').read_text())['core_files'].items():
 if sha(ROOT/file)!=h:raise RuntimeError('Registered source changed: '+file)
trains=[]
for seed in range(301,306):
 group=[]
 for kind in ('replay','contract','local_empty'):
  stem=f'{kind}_rep{seed}_seed{seed+300}';r=json.loads((ROOT/'evidence/main'/f'{stem}.json').read_text());p=ROOT/'evidence/main'/f'{stem}.safetensors'
  assert sha(p)==r['checkpoint_sha256'];assert r['steps']==1800;assert r['changed_parameter_elements']>0
  weights=load_file(str(p));assert digest_tensors(weights)==r['final_digest']
  if kind=='local_empty':
   parent=load_file(str(ROOT/'reference'/f'recurrent_rep{seed}_seed{seed+200}.safetensors'))
   assert all(torch.equal(weights[k],v) for k,v in parent.items());assert r['trainable_parameters']==1
  group.append(r);trains.append(stem)
 assert len({r['training_data_digest'] for r in group})==1
 assert group[0]['initial_digest']==group[1]['initial_digest']
verified=[];total_rows=0;answers=0
with tempfile.TemporaryDirectory(prefix='nbr004-replay-') as d:
 for seed in range(301,306):
  for mode in MODES:
   stem=f'{mode}_rep{seed}';old=json.loads((ROOT/'evidence/results'/f'{stem}.json').read_text())
   arr=np.load(ROOT/'evidence/results'/f'{stem}.npz')
   for row in old['rows']:
    pred=arr[row['prediction_key']];target=arr[row['prediction_key']+'_target']
    assert np.array_equal(target,expected(row,len(target))),('Independent ledger mismatch',stem,row)
    assert pred.shape==target.shape and ((0<=pred)&(pred<=8)).all()
    for k,mask in [('known_accuracy',target<8),('unknown_accuracy',target==8)]:
     v=float((pred[mask]==target[mask]).mean()) if mask.any() else None
     assert v==row[k],(stem,k,row)
    assert float((pred[:,0]==target[:,0]).mean())==row['focus_accuracy']
    assert float((pred[:,1:]==target[:,1:]).mean())==row['neighbors_accuracy']
   new=evaluate_one(ROOT,Path(d),seed,mode)
   assert old['rows']==new['rows'],('Rows failed',stem)
   assert old['stability']==new['stability'],('Local dynamics failed',stem)
   assert old['result_array_digest']==new['result_array_digest']
   newarr=np.load(Path(d)/(stem+'.npz'))
   assert set(newarr.files)==set(arr.files)
   assert all(np.array_equal(arr[k],newarr[k]) for k in arr.files)
   total_rows+=len(old['rows']);answers+=old['answer_evaluations'];verified.append(stem)
write_json(ROOT/'evidence/INDEPENDENT_VERIFICATION.json',{'status':'PASS','fresh_interpreter':True,'registered_core_hashes_match':True,
 'trained_checkpoints':len(trains),'trained_checkpoint_names':trains,'paired_training_inputs_matched':True,
 'local_parent_networks_unchanged':True,'result_runs':len(verified),'metric_rows':total_rows,'saved_answer_evaluations':answers,
 'all_arrays_bitwise_identical':True,'independent_target_ledger_and_score_recalculation':True,
 'replayed_local_dynamics':True,'elapsed_seconds':time.perf_counter()-start,'verified':verified,
 'scope':'Internal fresh-process reproducibility; not external replication, new training seeds or production qualification.'})
print('ALL RESULTS VERIFIED',flush=True)
