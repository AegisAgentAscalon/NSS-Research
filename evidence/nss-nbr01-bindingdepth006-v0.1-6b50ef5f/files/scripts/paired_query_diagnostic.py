"""Exploratory balance check after main inspection: known vs missing noisy queries.
No new fitting, calibration or main-score replacement. Models/cases declared in
source before this script's execution; diagnosis does not retroactively pass a gate.
"""
import json,numpy as np,torch
from safetensors.torch import load_file
from nbr006 import data,models,common as c
from nbr006.eval import metrics
c.setup(7);rows=[]
with torch.no_grad():
 for seed in range(801,806):
  for kind in ['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4']:
   m=models.make(kind);m.load_state_dict(load_file(str(c.ROOT/'checkpoints'/f'{kind}_{seed}.safetensors')));m.eval();identity=c.weights_hash(m)
   for noise in [.05,.2]:
    for missing in [False,True]:
     pp=data.batch(np.random.default_rng(410000+seed+int(missing)),512,max_h=4,hops=4,missing=missing,query_noise=noise)
     k,v,e,q,book=data.tensors(pp);out=m(k,v,e,q,8);pred=models.logits(out,book).argmax(-1).numpy()
     for depth in [4,8]:
      r={'kind':kind,'seed':seed,'noise':noise,'missing':missing,'depth':depth};r.update(metrics(pred[:,depth-1],pp,depth,kind));rows.append(r)
   assert c.weights_hash(m)==identity
c.dump(c.ROOT/'evidence/PAIRED_QUERY_DIAGNOSTIC.json',{'status':'EXPLORATORY_POST_MAIN_INSPECTION','rows':rows,'weights_unchanged':True,'not_in_main_counts':True,'purpose':'Main noisy-query rows were known-only; this supplements them without treating known-only recall as overall robustness.'})
print('Exploratory rows',len(rows))
