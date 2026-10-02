"""Fresh-interpreter numerical replay; not an independent scientific replication."""
from pathlib import Path
import argparse,json,subprocess,sys,time
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from nbr01_recovery.util import write_json,sha,digest_tensors,setup
ROOT=Path(__file__).resolve().parents[1]

def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(parents=True,exist_ok=True);records=[]
    setup()
    import torch
    from safetensors.torch import load_file
    from nbr01_recovery.train import make
    registered=json.loads((ROOT/'spec/REGISTRATION.json').read_text())
    for name,value in registered['source_sha256'].items():
        if sha(ROOT/name)!=value:raise RuntimeError(f'Registered source changed: {name}')
    if sha(ROOT/'spec/protocol.json')!=registered['protocol_sha256']:raise RuntimeError('Protocol changed')
    for meta in sorted((ROOT/'evidence/main').glob('*.json')):
        if meta.name.endswith('.prerun.json'):continue
        r=json.loads(meta.read_text());ckpt=meta.with_suffix('.safetensors')
        if sha(ckpt)!=r['checkpoint_sha256']:raise RuntimeError('Checkpoint changed')
        state=load_file(str(ckpt));torch.manual_seed(r['learn_seed']);m=make(r['kind'])
        init=m.state_dict()
        if digest_tensors(init)!=r['initial_digest'] or digest_tensors(state)!=r['final_digest']:raise RuntimeError('Identity mismatch')
        changed=sum(int((state[k]!=v).sum()) for k,v in init.items())
        if changed!=r['changed_parameter_elements']:raise RuntimeError('Changed count mismatch')
    for seed in range(301,306):
        cmd=[sys.executable,str(ROOT/'run.py'),'evaluate','--rep-seed',str(seed),'--seed',str(seed+200),
             '--models',str(ROOT/'evidence/main'),'--output',str(a.output)]
        t=time.perf_counter();r=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,timeout=180)
        (a.output/f'rep{seed}.log').write_text(r.stdout+r.stderr)
        if r.returncode:raise RuntimeError(r.stdout+r.stderr)
        name=f'rep{seed}_seed{seed+200}'
        original=json.loads((ROOT/'evidence/results'/f'{name}.json').read_text())
        replay=json.loads((a.output/f'{name}.json').read_text())
        if original['rows']!=replay['rows']:raise RuntimeError(f'Metric rows differ for{seed}')
        left=np.load(ROOT/'evidence/results'/f'{name}.predictions.npz',allow_pickle=False)
        right=np.load(a.output/f'{name}.predictions.npz',allow_pickle=False)
        if set(left.files)!=set(right.files):raise RuntimeError('Prediction keys differ')
        for k in left.files:
            if not np.array_equal(left[k],right[k]):raise RuntimeError('Prediction differs')
        records.append(dict(rep_seed=seed,cells=len(original['rows']),metric_rows_identical=True,
                            all_prediction_arrays_identical=True,seconds=time.perf_counter()-t))
    result=dict(status='PASS',source_registration_unchanged=True,checkpoints_verified=15,
                cells_replayed=sum(x['cells'] for x in records),pairs=records,
                meaning='Fresh interpreter replay of the same implementation, not independent external replication')
    write_json(a.output/'VERIFICATION.json',result);print(json.dumps(result,indent=2))
if __name__=='__main__':main()
