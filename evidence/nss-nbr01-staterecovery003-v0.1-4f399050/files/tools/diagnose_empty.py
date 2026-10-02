"""POST-HOC diagnostics of recurrent corruption of UNKNOWN, not a main score fix."""
from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import torch
from nbr01_recovery.util import setup,write_json,digest_tensors
from nbr01_recovery.evaluate import load_candidates,iterate
from nbr01_recovery.data import labels
ROOT=Path(__file__).resolve().parents[1]

@torch.no_grad()
def jacobian_fd(model,point,eps):
    eye=torch.eye(point.numel())*eps
    # Rows index input-coordinate perturbations; transpose to output-by-input.
    return ((model(point+eye)-model(point-eye))/(2*eps)).T

@torch.no_grad()
def run():
    setup();out=[];guard=[]
    for repseed in range(301,306):
        seed=repseed+200;rep,models,cs=load_candidates(ROOT,ROOT/'evidence/main',repseed,seed)
        model=models['recurrent'];before=digest_tensors(model.state_dict())
        points=list(iterate(cs['recurrent'],(rep.codes.clone(),),(4096,)))[-1][1][0]
        for eps in (1e-3,1e-4):
            spectral=[]
            for pt in points:
                j=jacobian_fd(model,pt,eps)
                spectral.append(float(torch.linalg.eigvals(j).abs().max()))
            out.append(dict(rep_seed=repseed,epsilon=eps,spectral_radius_per_class=spectral,
                unknown_radius=spectral[8],known_max_radius=max(spectral[:8]),
                exact_zero_fixed=bool(torch.equal(model(torch.zeros(16)),torch.zeros(16))),
                scope='Finite-difference local linearization around settled states; not a global convergence proof'))
        # Build an independent existence ledger from visible synthetic setup writes.
        y=labels(torch.Generator().manual_seed(10_000_000+seed),64)
        events=[(b,k,int(y[b,k])) for b in range(len(y)) for k in range(4) if int(y[b,k])<8]
        presence=torch.zeros_like(y,dtype=torch.bool)
        for b,k,value in events:presence[b,k]=True
        for mode in ('absent','correct_presence','inverted_presence'):
            z=rep.codes[y].clone();ng=torch.Generator().manual_seed(11_000_000+seed)
            mask=presence if mode!='inverted_presence' else ~presence
            for t in range(1024):
                z=z+.15*torch.randn(z.shape,generator=ng)
                z=model(z)
                if mode!='absent':z=torch.where(mask[...,None],z,torch.zeros_like(z))
            pred=rep(z).argmax(-1);known=y!=8
            guard.append(dict(rep_seed=repseed,mode=mode,known_n=int(known.sum()),
                 known_correct=int(((pred==y)&known).sum()),unknown_n=int((~known).sum()),
                 unknown_correct=int(((pred==y)&~known).sum()),
                 protected_presence_bytes_per_stream=4 if mode!='absent' else 0,
                 evidence='Presence derived only from setup WRITE observations; protected metadata is extra intact state. No per-query labels supplied.',
                 fault='Gaussian.15 damages neural coordinates, NOT presence metadata. Inversion is a separate deliberate bad-metadata control.'))
        if digest_tensors(model.state_dict())!=before:raise RuntimeError('Weights changed')
    result=dict(status='RUN_POST_HOC',local_stability=out,presence_interventions=guard,
        warnings=['Post-hoc after main UNKNOWN failures; main results unchanged',
        'Presence clamp is an exact metadata intervention, not learned neural improvement',
        'Cannot recover which value was erased or certify a known record is correct',
        'No claim about mammalian/fly physiology or general language epistemic uncertainty'])
    write_json(ROOT/'evidence/EMPTY_STATE_DIAGNOSTIC.json',result)
    print(json.dumps(result,indent=2))
if __name__=='__main__':run()
