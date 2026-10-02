"""Isolated CPU component timing after other jobs finish; not deployment latency."""
from pathlib import Path
import sys,time,statistics,resource
import torch,numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr007 import ROOT,repair
from nbr007.evaluate import problem,load_models
from nbr006 import common as c,data
@torch.no_grad()
def run():
 c.setup(901);readers,b,fitted=load_models(901);p=problem(711,b=64);k,v,e,q,book=data.tensors(p)
 timings=[]
 for kind in ('none','normalize','intrinsic_mlp','learned_dictionary','nearest'):
  fn=lambda:repair.maintain(k,v,e,book,kind,fitted.get(kind),'both')
  for _ in range(5):fn()
  ts=[]
  for _ in range(31):
   t=time.perf_counter();fn();ts.append(time.perf_counter()-t)
  timings.append({'component':kind,'median_ms_per_batch64':statistics.median(ts)*1000,'raw_times':ts})
 for depth in (1,2,4,8):
  fn=lambda:readers['record_hop'](k,v,e,q,depth)
  for _ in range(5):fn()
  ts=[]
  for _ in range(31):
   t=time.perf_counter();fn();ts.append(time.perf_counter()-t)
  timings.append({'component':f'reader_depth{depth}','median_ms_per_batch64':statistics.median(ts)*1000,'raw_times':ts})
 raw={'records_per_stream':16,'float_dim':17,'content_buffers_bytes':16*2*17*4,'protected_presence_bytes':16,'identity_book_bytes':17*17*4,'query_bytes':17*4,'new_learned_parameter_bytes':{name:sum(x.numel()*x.element_size() for x in m.parameters()) for name,m in fitted.items()},'max_score_feature_array_bytes_per_stream':16*17*5*4,'max_hidden_score_array_bytes_per_stream':16*17*32*4}
 c.dump(ROOT/'evidence/RESOURCES.json',{'environment':c.env(),'timings':timings,'raw_accounting':raw,'process_peak_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'qualification':'One-thread CPU component timings, one seed; no end-to-end device, energy or optimized algorithm comparison. Temporary-array sizes are computed component sizes, not measured peak allocator memory.'})
 print([(r['component'],r['median_ms_per_batch64']) for r in timings])
if __name__=='__main__':run()
