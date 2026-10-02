"""Descriptive CPU/state accounting; no claim of user-hardware suitability."""
import sys,time,json,statistics
from pathlib import Path
import torch
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_exist.models import *
from nbr01_exist.util import setup,write_json,environment
setup();rows=[]
with torch.no_grad():
 for mode in MODES:
    rep,old,new=load_components(ROOT,303,mode);m=Memory(rep,mode,old,new,64);m.event('write',0,2)
    for _ in range(20):m.maintain();m.read()
    timings=[]
    for _ in range(5):
        st=time.perf_counter()
        for k in range(200):m.maintain();m.read()
        timings.append((time.perf_counter()-st)/200)
    used_old=mode not in ('nearest','coupled17')
    rows.append(dict(mode=mode,raw_state_per_stream=m.raw_state_bytes()//64,
        serving_shared_representation_bytes=sum(v.numel()*v.element_size() for v in rep.state_dict().values()),
        serving_parent_bytes=sum(v.numel()*v.element_size() for v in old.state_dict().values()) if used_old else 0,
        serving_new_bytes=sum(v.numel()*v.element_size() for v in new.state_dict().values()) if new else 0,
        loader_parent_bytes_even_if_unused=sum(v.numel()*v.element_size() for v in old.state_dict().values()),
        median_maintenance_read_seconds=statistics.median(timings),all_timings=timings,batch=64))
train=[json.loads(p.read_text()) for p in (ROOT/'evidence/main').glob('*.json') if '.prerun.' not in p.name]
dev=[json.loads(p.read_text()) for p in (ROOT/'evidence/development').glob('*.json') if '.prerun.' not in p.name]
write_json(ROOT/'evidence/RESOURCE_ACCOUNTING.json',dict(status='MEASURED_WITH_LIMITS',environment=environment(),modes=rows,
    completed_main_training_cpu_seconds=sum(t['train_cpu_seconds'] for t in train),completed_main_training_job_wall_seconds_sum=sum(t['train_wall_seconds'] for t in train),
    development_training_cpu_seconds=sum(t['train_cpu_seconds'] for t in dev),development_steps=sum(t['steps'] for t in dev),
    max_sampled_single_training_process_rss_bytes=max(t['sampled_process_peak_rss_bytes'] for t in train),
    total_concurrent_phase_peak='NOT_MEASURED; workers overlapped. Single-process peaks are NOT a complete phase peak.',
    inherited_preparation='Parent content maps and representations were not trained here. Historical receipts remain in reference/.',
    exclusions='Raw state excludes framework objects, RNG, scope/revision metadata, checkpoints, output archives, gradients, optimizer state and temporary arithmetic. All use float32, not low-bit traces.',
    timing_limit='Descriptive sandbox CPU loop measurements, not equal-quality/compute comparison, target-device budget or energy measurement.'))
print('Resource rows',len(rows))
