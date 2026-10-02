"""Fresh-interpreter result replay, fixed-source and checkpoint checks."""
from __future__ import annotations
import hashlib,json,time
from pathlib import Path
import torch
from .util import sha,write_json,load_model,weights_digest
from .models import MemoryModel
from .evaluate import evaluate_checkpoint,calibrate


def verify(root,output):
    root,output=Path(root),Path(output)
    output.mkdir(parents=True,exist_ok=True)
    reg=json.loads((root/'spec/REGISTRATION.json').read_text())
    for name,expected in reg['files'].items():
        if sha(root/name)!=expected:raise RuntimeError('Registered source changed: '+name)
    comparisons=[]; batches={};count=0
    mainpaths=sorted((root/'evidence/main').glob('*.safetensors'))
    if len(mainpaths)!=40:raise RuntimeError('Missing registered checkpoint')
    before={str(p.relative_to(root)):sha(p) for p in mainpaths}
    cal=json.loads((root/'evidence/results/CALIBRATIONS.json').read_text())['calibrations']
    for p in mainpaths:
        tr=json.loads(p.with_suffix('.json').read_text()); kind=tr['kind'];seed=tr['seed'];curr=tr['curriculum']
        if sha(p)!=tr['checkpoint_sha256']:raise RuntimeError('Checkpoint checksum')
        torch.manual_seed(seed);initial=MemoryModel(kind)
        if weights_digest(initial)!=tr['initial_parameter_digest']:raise RuntimeError('Initial identity')
        m=load_model(p,kind)
        if weights_digest(m)!=tr['final_parameter_digest']:raise RuntimeError('Final identity')
        changed=sum(int((v!=initial.state_dict()[k]).sum()) for k,v in m.state_dict().items())
        if changed!=tr['changed_parameter_elements'] or not changed:raise RuntimeError('Training change count')
        key=(seed,curr)
        if key in batches and batches[key]!=tr['train_batch_sha256']:raise RuntimeError('Unmatched batches')
        batches[key]=tr['train_batch_sha256']
        if kind=='soft_slots' and calibrate(m,seed)!=cal[p.stem]:raise RuntimeError('Calibration not reproduced')
        reference=json.loads((root/'evidence/results'/f'{p.stem}.eval.json').read_text())
        fresh=evaluate_checkpoint(root,p,tr,output/f'{p.stem}.eval.json',cal.get(p.stem))
        if len(reference['rows'])!=len(fresh['rows']):raise RuntimeError('Row count mismatch')
        for a,b in zip(reference['rows'],fresh['rows']):
            aa={k:v for k,v in a.items() if k!='eval_seconds'}
            bb={k:v for k,v in b.items() if k!='eval_seconds'}
            if aa!=bb:raise RuntimeError('Metric, dataset or prediction mismatch '+p.stem)
            count+=1
        comparisons.append(dict(checkpoint=p.name,rows_reproduced=len(fresh['rows']),
            exact_initial_identity=True,exact_final_identity=True,changed_elements=changed,
            calibration_reproduced=kind=='soft_slots'))
    after={str(p.relative_to(root)):sha(p) for p in mainpaths}
    if before!=after:raise RuntimeError('Replaying modified checkpoints')
    receipt=dict(status='PASS',checkpoints=len(comparisons),model_metric_cells_reproduced=count,
        registered_files=len(reg['files']),registered_files_unchanged=True,
        matched_training_stream_groups=len(batches),all_checkpoints_unchanged=True,
        comparisons=comparisons,note='Fresh checkpoint reload, regeneration of episodes and predictions; same published model implementation, not an independent model reimplementation.')
    write_json(output/'VERIFICATION.json',receipt)
    return receipt
