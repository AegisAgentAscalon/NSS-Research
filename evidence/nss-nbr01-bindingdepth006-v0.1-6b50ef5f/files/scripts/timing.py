"""Isolated CPU query-time measurements after training/replay jobs have ended."""
import time,json,statistics,resource
import numpy as np
import torch
from safetensors.torch import load_file
from nbr006 import common as c,data,models
from nbr006.exact_eval import ExactReader
c.setup(3);p=data.batch(np.random.default_rng(54321),128,max_h=4,hops=4,missing=None);k,v,e,q,book=data.tensors(p);rows=[]
with torch.no_grad():
 for kind in ['record_hop','gated_hop','untied_hop4','tied_attention','fixed_attention4','exact_lookup']:
  m=ExactReader() if kind=='exact_lookup' else models.make(kind)
  if kind!='exact_lookup':m.load_state_dict(load_file(str(c.ROOT/'checkpoints'/f'{kind}_801.safetensors')))
  m.eval()
  for depth in [1,2,4,8]:
   for _ in range(3):m(k,v,e,q,depth)
   times=[]
   for _ in range(30):
    t=time.perf_counter();m(k,v,e,q,depth);times.append(time.perf_counter()-t)
   rows.append({'kind':kind,'depth_allowance':depth,'actual_query_rounds':min(depth,4) if kind in ['untied_hop4','fixed_attention4'] else depth,'batch128_median_ms':statistics.median(times)*1000,'batch128_min_ms':min(times)*1000,'repetitions':len(times)})
c.dump(c.ROOT/'evidence/QUERY_TIMING.json',{'rows':rows,'env':c.env(),'rss_max_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'scope':'One checkpoint/architecture; batched CPU latency, not user-device latency or matched full pipeline cost. Exact control is Python byte-dictionary lookup, not optimized kernel.','record_state_bytes_per_stream':16*(2*17*4+1),'query_code_bytes':17*4,'identity_codebook_bytes_per_stream':17*17*4})
print('Measured',len(rows),'quality-cost settings')
