"""Post-pilot same-weight hard-admission intervention. No training occurs."""
from pathlib import Path
import argparse
import json
import torch
from safetensors.torch import load_file
from .core import RecallModel, parameter_digest, digest_bytes
from .experiment import configure, evaluate, interventions

ROOT=Path(__file__).resolve().parents[1]


def run(evidence:Path, output:Path):
    configure()
    if output.exists():raise FileExistsError(output)
    before={'protocol_sha256':digest_bytes((ROOT/'spec/gate_diagnostic_registered.json').read_bytes()),
            'diagnostic_source_sha256':digest_bytes(Path(__file__).read_bytes()),
            'scope':'POST_PILOT_DIAGNOSTIC_NOT_CONFIRMATORY'}
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.with_suffix('.prerun.json').open('x') as f:json.dump(before,f,indent=2)
    results=[]
    for seed in range(201,206):
        path=evidence/f'gated_seed{seed}.safetensors'
        old=json.loads((evidence/f'gated_seed{seed}.json').read_text())
        model=RecallModel('hard_gated');model.load_state_dict(load_file(str(path)));model.eval()
        frozen=parameter_digest(model)
        if frozen!=old['training']['final_parameter_digest']:raise ValueError('Weight transfer was not exact')
        rows=evaluate(model,seed)
        for row in rows:row['kind']='soft_trained_hard_admission'
        data={'seed':seed,'source_checkpoint_sha256':digest_bytes(path.read_bytes()),
              'weights_digest':frozen,'parameter_updates':0,'algorithm_changed':True,
              'threshold':0.5,'evaluation':rows,'interventions':interventions(model,seed)}
        if frozen!=parameter_digest(model):raise ValueError('Weights changed')
        results.append(data)
    report={'manifest':before,'results':results,'all_weights_unchanged':True,
            'decision_boundary':'Diagnostic only; not production qualification or an accepted new core.'}
    with output.open('x') as f:json.dump(report,f,indent=2,allow_nan=False);f.write('\n')
    return report


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--evidence',type=Path,default=ROOT/'evidence/pilot')
    args=p.parse_args();r=run(args.evidence,args.output)
    for s in r['results']:
        selected=[x for x in s['evaluation'] if x['keep'] and x['depth']==4 and x['delay']==128 and x['condition']!='no_cue']
        print('seed',s['seed'],'128-delay recall',sum(x['correct'] for x in selected)/sum(x['n'] for x in selected))

if __name__=='__main__':main()
