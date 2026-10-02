"""POST-HOC failure isolation: correct room answer can conceal record aliasing.

Uses the registered near-collision episodes, without any fitting or score repair.
The original main evaluation is preserved. Origin/old-slot IDs are scorer-only.
"""
from pathlib import Path
import sys
import numpy as np
import torch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr008.common import *
from nbr008.config import *
from nbr008.pipeline import *

@torch.no_grad()
def main():
 setup();rows=[];arrays={}
 for pair in range(1,6):
  mods=parents(pair);h,cfg=load_gate(1000+pair)
  for method in ('nearest','A_nearest','B_nearest'):
   r=resolver(method,mods,h,cfg);p=make_problem(560000000+pair,4,64,n=12);s=install(p,mods['binder'],r,True)
   rng=np.random.default_rng(560100000+pair);near=p['codes'][:,0].copy();near[:,:16]+=rng.normal(0,.01,(64,16)).astype(np.float32);near=data.normalize(near).astype(np.float32)
   old_keys=s.store.keys.clone();old_vals=s.store.vals.clone();old_presence=s.present.clone();oldq=torch.from_numpy(p['codes'][:,0])
   before=read(s,mods['record_hop'],r,oldq)['pred'][:,-1]
   reg=s.register(torch.from_numpy(near));assert reg['added'].all();p['codes'][:,12]=near
   dest=p['rooms'][:,1];receipt=s.event(torch.from_numpy(near),torch.from_numpy(p['codes'][np.arange(64),dest]),1,r,True)
   selected=receipt['selected'];written=receipt['written'];existing=written&(selected<16)
   modified_old=((s.store.vals-old_vals).abs().sum(-1)>1e-6)&old_presence
   keys_ids=torch.einsum('bsd,bnd->bsn',s.store.keys,s.book).argmax(-1)
   new_record=((keys_ids==12)&s.present).any(-1)
   after=read(s,mods['record_hop'],r,oldq)['pred'][:,-1]
   new_answer=read(s,mods['record_hop'],r,torch.from_numpy(near))['pred'][:,-1]
   key=f'p{pair}_{method}'
   vals={'write_accepted':written,'existing_slot_used':existing,'old_record_content_modified':modified_old.any(-1),'new_record_exists':new_record,'old_answer_changed':before!=after,'new_answer_correct':new_answer==torch.from_numpy(dest)}
   row={'pair':pair,'method':method,'n':64,**{k:int(v.sum()) for k,v in vals.items()}}
   for k,v in vals.items():arrays[key+'_'+k]=v.numpy()
   arrays[key+'_selected_slot']=selected.numpy();arrays[key+'_old_keys']=old_keys.numpy();arrays[key+'_old_values']=old_vals.numpy();arrays[key+'_after_values']=s.store.vals.numpy()
   rows.append(row)
 out=ROOT/'evidence/NEAR_COLLISION_DIAGNOSTIC.npz';np.savez_compressed(out,**arrays)
 info={'status':'RUN_POST_HOC','reason':'Main neural/exact traversal discrepancy on nearly identical registered sources','rows':rows,'array_sha256':sha(out),'no_training':True,'no_main_scores_replaced':True}
 dump(out.with_suffix('.json'),info);print(rows)
if __name__=='__main__':main()
