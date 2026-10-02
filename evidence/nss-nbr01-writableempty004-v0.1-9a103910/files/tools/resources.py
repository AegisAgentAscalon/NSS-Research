from pathlib import Path
import sys,time,json,statistics
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
import torch
from nbr01_empty.models import *
from nbr01_empty.util import setup,write_json,environment
setup();out=[]
for mode in MODES:
 rep,repair=load_components(ROOT,301,mode);m=Memory(rep,mode,repair,64)
 m.event('write',1,3);m.event('write',2,4)
 with torch.no_grad():
  for _ in range(50):m.maintain();m.read()
  trials=[]
  for trial in range(5):
   t=time.perf_counter()
   for _ in range(200):m.maintain();m.read()
   trials.append((time.perf_counter()-t)/200)
 out.append(dict(mode=mode,raw_state_bytes_per_stream=m.raw_state_bytes()//64,
                 shared_representation_bytes=sum(v.numel()*v.element_size() for v in rep.state_dict().values()),
                 extra_repair_weight_bytes=sum(v.numel()*v.element_size() for v in repair.state_dict().values()) if repair else 0,
                 maintenance_and_read_seconds_median=statistics.median(trials),trials=trials,batch=64))
tr=[json.loads(p.read_text()) for p in (ROOT/'evidence/main').glob('*.json') if not p.name.endswith('.prerun.json')]
assert len(tr)==15
source=json.loads((ROOT/'reference/recurrent_rep301_seed501.json').read_text())
write_json(ROOT/'evidence/RESOURCE_ACCOUNTING.json',dict(environment=environment(),modes=out,
    main_optimizer_steps=sum(r['steps'] for r in tr),main_sequence_presentations=sum(r['sequence_presentations'] for r in tr),
    main_supervised_event_presentations=sum(r['supervised_event_presentations'] for r in tr),
    main_training_seconds=sum(r['train_wall_seconds'] for r in tr),
    sampled_training_process_peak_rss_bytes=max(r['sampled_process_peak_rss_bytes'] for r in tr),
    inherited='Five HorizonBinding002 reps plus five StateRecovery003 recurrent parents, supplied and unchanged; historical preparation not rerun and not free.',
    timing_scope='Descriptive CPU microbenchmark, not user-PC or end-to-end quality-matched latency; may share host CPU.',
    peak_temporary_allocation='NOT_MEASURED',energy='NOT_MEASURED',target_hardware='NOT_MEASURED',low_bit='NOT_RUN'))
print('resources recorded')
