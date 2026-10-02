"""Post-pilot isolation: close low gates OR fully open high gates, not both.

Threshold0.5 is inherited, not fitted on this probe. Fresh generated instances are
still exploratory diagnostics, not independent confirmatory architecture evidence.
"""
import argparse
import json
from pathlib import Path
import torch
from safetensors.torch import load_file
from .core import RecallModel, HIDDEN, validate_tokens, batch, parameter_digest, digest_bytes
from .experiment import configure

ROOT=Path(__file__).resolve().parents[1]

class AdmissionProbe(RecallModel):
    def __init__(self, policy):
        super().__init__('gated')
        if policy not in ('soft','close_low_only','open_high_only'):raise ValueError('Unknown intervention')
        self.policy=policy
    def encode(self, events, hidden=None):
        validate_tokens(events)
        embedded=self.embed(events)
        h=embedded.new_zeros((events.shape[0],HIDDEN)) if hidden is None else hidden.squeeze(0)
        for e in embedded.unbind(1):
            g=torch.sigmoid(self.gate(e))
            if self.policy=='close_low_only':g=torch.where(g<0.5,0.0,g)
            if self.policy=='open_high_only':g=torch.where(g>=0.5,1.0,g)
            h=(1-g)*h+g*torch.tanh(self.value(e))
        return h.unsqueeze(0)

@torch.no_grad()
def probe(output):
    configure()
    if output.exists():raise FileExistsError(output)
    output.parent.mkdir(parents=True,exist_ok=True)
    prereg={'phase':'POST_PILOT_CAUSAL_DIAGNOSTIC_NOT_CONFIRMATORY','source_sha256':digest_bytes(Path(__file__).read_bytes()),
            'threshold':0.5,'depth':4,'delay':128,'seeds':list(range(201,206)),
            'policies':['soft','close_low_only','open_high_only'],'parameter_updates':0,
            'question':'Separate residual low-gate writes from insufficient high-gate admission.'}
    with output.with_suffix('.prerun.json').open('x') as f:json.dump(prereg,f,indent=2)
    results=[]
    for seed in range(201,206):
        checkpoint=ROOT/'evidence/pilot'/f'gated_seed{seed}.safetensors'
        weights=load_file(str(checkpoint))
        for policy in prereg['policies']:
            m=AdmissionProbe(policy);m.load_state_dict(weights);m.eval();before=parameter_digest(m)
            for ci,condition in enumerate(('early_cue','overwrite','no_cue')):
                x,y=batch(torch.Generator().manual_seed(810000+seed*10+ci),256,128,condition)
                pred=m(x,4).argmax(1)
                results.append({'seed':seed,'policy':policy,'condition':condition,'n':len(y),
                                'correct':int((pred==y).sum()),'unknown_predictions':int((pred==8).sum()),
                                'observation_digest':digest_bytes(x.numpy().tobytes()),'weights_digest':before})
            if before!=parameter_digest(m):raise ValueError('Weights changed')
    with output.open('x') as f:json.dump({'registration':prereg,'results':results},f,indent=2);f.write('\n')
    for policy in prereg['policies']:
        cells=[r for r in results if r['policy']==policy and r['condition']!='no_cue']
        print(policy,sum(r['correct'] for r in cells)/sum(r['n'] for r in cells))

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--output',type=Path,required=True)
    probe(p.parse_args().output)
