from pathlib import Path
import sys,json,time,statistics,importlib.metadata
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from nbr01_recovery.evaluate import load_candidates
from nbr01_recovery.util import setup,write_json,environment
ROOT=Path(__file__).resolve().parents[1]

@torch.no_grad()
def main():
    setup();rep,models,cs=load_candidates(ROOT,ROOT/'evidence/main',303,503)
    y=torch.arange(256).remainder(9).reshape(64,4);rows=[]
    for name,c in cs.items():
        s=c.state(y);tim=[]
        for _ in range(20):s=c.step(s);c.predict(s)
        for trial in range(5):
            s=c.state(y);t=time.perf_counter()
            for _ in range(300):s=c.step(s);c.predict(s)
            tim.append((time.perf_counter()-t)/300)
        relevant='readout_repair' if name=='readout_repair' else 'fast_slow' if name.startswith('fast_slow') else 'recurrent' if name.startswith('recurrent') else None
        extra=sum(p.numel()*p.element_size() for p in models[relevant].parameters()) if relevant else 0
        rows.append(dict(mode=name,raw_activation_bytes_per_stream=c.active_state_bytes_per_stream(),
            protected_archive_bytes_per_stream=32 if name=='exact_archive' else 0,
            frozen_representation_tensor_bytes=sum(t.numel()*t.element_size() for t in rep.state_dict().values()),
            extra_parameter_bytes=extra,batch_streams=64,
            median_seconds_per_maintenance_plus_read_batch=statistics.median(tim),replicate_seconds=tim,
            note='Descriptive microbenchmark, not inference-token latency; hold overhead includes original readout. Exact control retains dummy neural buffer plus separateint64 archive in this harness.'))
    training=[json.loads(p.read_text()) for p in (ROOT/'evidence/main').glob('*.json') if not p.name.endswith('.prerun.json')]
    prior=[json.loads((ROOT/'reference'/f'soft_slots_wide_seed{s}.json').read_text()) for s in range(301,306)]
    out=dict(environment=environment(),packages={k:importlib.metadata.version(k) for k in ['torch','numpy','safetensors','psutil']},
        modes=rows,training_records=training,
        reused_preparation=dict(checkpoints=5,old_steps=sum(r['steps'] for r in prior),old_examples=sum(r['examples'] for r in prior),
           old_events=sum(r['observed_events'] for r in prior),old_loop_seconds=sum(r['train_wall_seconds'] for r in prior),note='Historical documented preparation, NOT rerun or included in new46s training loops'),
        measured_scope='Tensor bytes and descriptive CPU times; RSS sample peaks in training metadata. Exact per-op workspace peaks, target hardware latency and energy NOT_MEASURED. No low-bit or biological-efficiency claim.')
    write_json(ROOT/'evidence/RESOURCE_ACCOUNTING.json',out)
    print('Resource accounting written')
if __name__=='__main__':main()
