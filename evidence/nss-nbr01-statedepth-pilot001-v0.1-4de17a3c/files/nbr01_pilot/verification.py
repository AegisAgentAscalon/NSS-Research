"""Read-only validation of packaged weights/results; never retrains or downloads."""
from __future__ import annotations
import argparse
import json
from pathlib import Path
import tempfile
import torch
from safetensors.torch import load_file
from .core import RecallModel, Session, parameter_digest, digest_bytes, batch, KINDS
from .experiment import configure, evaluate, interventions, lifecycle
from .controls import ExactState

ROOT=Path(__file__).resolve().parents[1]


def verify(evidence:Path, exhaustive:bool=False):
    configure()
    checks=[];results=[];fingerprints={}
    for seed in range(201,206):
        for kind in KINDS:
            path=evidence/f'{kind}_seed{seed}.json'
            result=json.loads(path.read_text());t=result['training']
            checkpoint=evidence/f'{kind}_seed{seed}.safetensors'
            if digest_bytes(checkpoint.read_bytes())!=t['checkpoint_sha256']:raise ValueError('Checkpoint checksum mismatch')
            torch.manual_seed(seed);model=RecallModel(kind)
            if parameter_digest(model)!=t['initial_parameter_digest']:raise ValueError('Initial parameters differ from seed')
            initial={k:v.clone() for k,v in model.state_dict().items()}
            model.load_state_dict(load_file(str(checkpoint)));model.eval()
            if parameter_digest(model)!=t['final_parameter_digest']:raise ValueError('Final parameters differ')
            changed=sum(int(torch.count_nonzero(v-initial[k])) for k,v in model.state_dict().items())
            if changed!=t['changed_parameter_elements'] or changed==0:raise ValueError('Wrong changed-parameter count')
            fingerprints.setdefault(seed,set()).add(t['train_batch_digest'])
            # Original tested core/experiment source must still match each recorded identity.
            for name in ('nbr01_pilot/core.py','nbr01_pilot/experiment.py'):
                if digest_bytes((ROOT/name).read_bytes())!=result['manifest']['source_sha256'][name]:
                    raise ValueError('Training/evaluation source changed since pilot')
            record={'kind':kind,'seed':seed,'weights_and_initial_seed_exact':True,
                    'changed_elements_recomputed':changed}
            with tempfile.TemporaryDirectory() as tmp:
                checked=lifecycle(model,seed,Path(tmp))
                if checked!=result['lifecycle']:raise ValueError('Lifecycle reproduction mismatch')
            record['lifecycle_reproduced']=True
            if exhaustive:
                new=evaluate(model,seed)
                if kind=='transformer':new+=evaluate(model,seed,memory_tool=True)
                expected=result['evaluation']
                keys=('kind','seed','delay','condition','keep','depth','n','correct','unknown_predictions','dataset_sha256')
                if [tuple(r[k] for k in keys) for r in new]!=[tuple(r[k] for k in keys) for r in expected]:
                    raise ValueError('Evaluation reproduction mismatch')
                if interventions(model,seed)!=result['interventions']:raise ValueError('Interventions differ')
                record['all_metric_cells_reproduced']=len(new)
            if parameter_digest(model)!=t['final_parameter_digest']:raise ValueError('Verification mutated parameters')
            checks.append(record);results.append(result)
    if any(len(h)!=1 for h in fingerprints.values()):raise ValueError('Teaching batches not matched')
    # Same observation sets per seed/condition/delay across models and memory tools.
    observations={}
    for result in results:
        for row in result['evaluation']:
            key=(row['seed'],row['condition'],row['delay'])
            observations.setdefault(key,set()).add(row['dataset_sha256'])
    if any(len(h)!=1 for h in observations.values()):raise ValueError('Evaluation information not matched')
    explicit=[]
    for seed in range(201,206):
        for delay in (0,4,16,64,128):
            for ci,condition in enumerate(('early_cue','overwrite','no_cue')):
                g=torch.Generator().manual_seed(300000+seed*100+delay*3+ci)
                x,y=batch(g,256,delay,condition)
                predictions=[]
                for tape in x.tolist():
                    s=ExactState()
                    for token in tape:s.observe(token)
                    predictions.append(s.query())
                correct=sum(int(a==b) for a,b in zip(predictions,y.tolist()))
                if correct!=len(y):raise ValueError('Independent estimator does not match environment')
                explicit.append({'seed':seed,'delay':delay,'condition':condition,'n':256,'correct':correct})
    return {'status':'PASS','fresh_process':True,'exhaustive_metric_replay':exhaustive,
            'model_checkpoints_verified':len(checks),'checks':checks,
            'training_batches_equal_per_seed':True,'evaluation_observations_equal':True,
            'explicit_estimator_episodes':sum(r['n'] for r in explicit),
            'explicit_estimator_results':explicit,
            'scope':'No retraining or production-generation qualification. Reproduces stored metrics on this software/backend.'}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--exhaustive',action='store_true')
    p.add_argument('--evidence',type=Path,default=ROOT/'evidence/pilot')
    p.add_argument('--output',type=Path)
    args=p.parse_args();result=verify(args.evidence,args.exhaustive)
    raw=json.dumps(result,indent=2)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        with args.output.open('x',encoding='utf-8') as f:f.write(raw)
    print(raw)

if __name__=='__main__':main()
