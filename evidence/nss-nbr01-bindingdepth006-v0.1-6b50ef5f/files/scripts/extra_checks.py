"""Registered binding audit, within-query equivalence, and staged resume checks."""
import argparse,os,json,copy
from pathlib import Path
import numpy as np
import torch
from safetensors.torch import load_file
from nbr006 import common as c,data,models
from nbr006.store import RecordStore
from nbr006.eval import install,distract,direct_binding_score
from nbr006.continuation import QueryRunner
ROOT=c.ROOT

def make_model(kind,seed):
 m=models.make(kind);m.load_state_dict(load_file(str(ROOT/'checkpoints'/f'{kind}_{seed}.safetensors')));m.eval();return m

@torch.no_grad()
def create(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=True);store_meta=[];query_meta=[];binding=[]
 for seed in range(801,806):
  m=make_model('binder',seed)
  for stage in ['initial','corrected','cleared','noisy']:
   rng=np.random.default_rng(880000+seed);p=data.batch(rng,32,max_h=4,hops=4,missing=False);s=install(p,m);rr=np.arange(32);focus=p['order'][:,2]
   if stage in ['corrected','cleared','noisy']:
    dst=p['rooms'][:,1];s.event(torch.from_numpy(p['codes'][rr,focus]),torch.from_numpy(p['codes'][rr,dst]),1);p['parent'][rr,focus]=dst
   if stage=='cleared':
    s.event(torch.from_numpy(p['codes'][rr,focus]),torch.zeros(32,17),-1);p['parent'][rr,focus]=16
   distract(s,p,rng,64,.02 if stage=='noisy' else 0)
   pred,exists=direct_binding_score(s,p);gt=p['parent'][:,:16]
   binding.append({'seed':seed,'stage':stage,'known':float((pred[gt!=16]==gt[gt!=16]).mean()),'missing':float((pred[gt==16]==16).mean()) if (gt==16).any() else None,'all_slots_correct':float((pred==gt).all(1).mean()),'existence_accuracy':float((exists==(gt!=16)).mean())})
   path=out/f'store_{seed}_{stage}.npz';s.save(path,rng)
   np.savez_compressed(out/f'input_{seed}_{stage}.npz',**p)
   distract(s,p,rng,17,.005)
   expected=out/f'expected_store_{seed}_{stage}.npz';np.savez_compressed(expected,keys=s.keys.numpy(),vals=s.vals.numpy(),present=s.present.numpy())
   store_meta.append({'seed':seed,'stage':stage,'path':path.name,'expected':expected.name,'inputs':f'input_{seed}_{stage}.npz'})
  for kind in ['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4']:
   reader=make_model(kind,seed);p=data.batch(np.random.default_rng(seed+66000),32,max_h=8,hops=8,missing=None);k,v,e,q,book=data.tensors(p)
   direct=reader(k,v,e,q,8)
   for split in [1,3,4,7]:
    qr=QueryRunner(reader,kind,k,v,e,q);qr.advance(split)
    if not torch.equal(qr.code,direct[:,split-1]):
     raise AssertionError(('step implementation differs',kind,seed,split,float((qr.code-direct[:,split-1]).abs().max())))
    path=out/f'query_{kind}_{seed}_{split}.npz';qr.save(path)
    expected=out/f'expected_query_{kind}_{seed}_{split}.npz';np.savez_compressed(expected,code=direct[:,7].numpy())
    query_meta.append({'kind':kind,'seed':seed,'split':split,'path':path.name,'expected':expected.name})
 c.dump(out/'INDEX.json',{'stores':store_meta,'queries':query_meta})
 c.dump(ROOT/'evidence/BINDING_AUDIT.json',{'entries':binding,'scope':'All slots including neighbours; protected presence; numeric content match; no natural-language qualification'})
 print('CREATED',len(store_meta),'store and',len(query_meta),'query continuation cases')

@torch.no_grad()
def verify(out):
 out=Path(out);idx=json.loads((out/'INDEX.json').read_text())
 for item in idx['stores']:
  m=make_model('binder',item['seed']);s,rng=RecordStore.load(out/item['path'],m)
  with np.load(out/item['inputs'],allow_pickle=False) as a:p={k:a[k] for k in a.files}
  distract(s,p,rng,17,.005)
  with np.load(out/item['expected'],allow_pickle=False) as a:
   for k in ['keys','vals','present']:np.testing.assert_array_equal(getattr(s,k).numpy(),a[k])
 for item in idx['queries']:
  m=make_model(item['kind'],item['seed']);qr=QueryRunner.load(out/item['path'],m);qr.advance(8-item['split'])
  with np.load(out/item['expected'],allow_pickle=False) as a:np.testing.assert_array_equal(qr.code.numpy(),a['code'])
 c.dump(out/'VERIFIED.json',{'status':'PASS','store_cases':len(idx['stores']),'query_cases':len(idx['queries']),'fresh_interpreter':True,'kind':'internal reproduction, not external replication'})
 print('PASS',len(idx['stores'])+len(idx['queries']),'continuations')

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['create','verify']);p.add_argument('--dir',required=True);a=p.parse_args();c.setup(1);create(a.dir) if a.mode=='create' else verify(a.dir)
