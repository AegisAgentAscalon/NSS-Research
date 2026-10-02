"""Registered lifecycle and information-loss diagnostics on actual checkpoints."""
from __future__ import annotations
import json,time,hashlib
from pathlib import Path
import torch
from .util import load_model,write_json,weights_digest,sha
from .data import evaluation_batch,exact_latest,KEYS,VALUES
from .evaluate import predict,metrics
from .state import Session


def run_checks(root,output):
    root,output=Path(root),Path(output);output.mkdir(parents=True,exist_ok=True)
    cal=json.loads((root/'evidence/results/CALIBRATIONS.json').read_text())['calibrations']
    lifecycle=[];ambiguity=[]; resets=[]
    for p in sorted((root/'evidence/main').glob('*.safetensors')):
        tr=json.loads(p.with_suffix('.json').read_text());kind=tr['kind'];seed=tr['seed'];curr=tr['curriculum']
        m=load_model(p,kind);before=weights_digest(m)
        variants=['native']
        if kind=='soft_slots':variants+=['hard_fixed','close_low','hard_calibrated']
        if kind=='tape_reader':variants+=['exact_tool']
        for variant in variants:
            threshold=cal[p.stem]['threshold'] if variant=='hard_calibrated' else .5
            mode={'native':'native','hard_fixed':'hard','close_low':'close_low','hard_calibrated':'hard','exact_tool':'native'}[variant]
            # End-to-end exact-tool evaluation already exists; snapshot test
            # applies to the full-tape reader, not a falsely claimed hidden ledger.
            if variant!='exact_tool':
                x,y,prot=evaluation_batch(seed,'retain',4096,1)
                session=Session(m,f'{p.stem}-{variant}',mode,threshold)
                session.observe(x[:,:1024]);prefix=session.state.clone();clock=session.events
                q1=session.predict().clone();q2=session.predict()
                if not torch.equal(q1,q2) or not torch.equal(prefix,session.state) or clock!=session.events:
                    raise RuntimeError('Query changes clock/state')
                path=output/'snapshots'/f'{p.stem}-{variant}'
                metadata=session.save(path)
                reloaded_model=load_model(p,kind)
                resumed=Session.restore(path,reloaded_model,session.scope,mode,threshold)
                if not torch.equal(session.state,resumed.state) or not torch.equal(session.predict(),resumed.predict()):
                    raise RuntimeError('Snapshot differs')
                session.observe(x[:,1024:]);resumed.observe(x[:,1024:])
                if not torch.equal(session.state,resumed.state) or not torch.equal(session.predict(),resumed.predict()):
                    raise RuntimeError('Resumed continuation differs')
                finalpred=session.predict().argmax(-1)
                scope_rejected=False
                try:Session.restore(path,reloaded_model,session.scope+'wrong',mode,threshold)
                except ValueError:scope_rejected=True
                if not scope_rejected:raise RuntimeError('Wrong scope accepted')
                session.reset('new-empty-scope');empty_pred=session.predict().argmax(-1)
                resets.append(dict(kind=kind,seed=seed,curriculum=curr,variant=variant,
                                   unknown_correct=int((empty_pred==8).sum()),n=4))
                # Fixed-query state-off removes information for every model.
                xo,yo,_=evaluation_batch(seed,'retain',16,128)
                erased=predict(m,xo[:,:0],variant,threshold)
                lifecycle.append(dict(kind=kind,seed=seed,curriculum=curr,variant=variant,
                    checkpoint_events=1024,continued_events=x.shape[1],exact_resume=True,
                    query_does_not_mutate=True,wrong_scope_rejected=True,
                    all_four_after_continue_correct=bool((finalpred==y).all()),
                    raw_prefix_state_bytes=prefix.numel()*prefix.element_size(),
                    serialized_prefix_bytes=sum(q.stat().st_size for q in path.iterdir()),
                    state_off_correct=int((erased==yo).sum()),state_off_answers=yo.numel(),
                    state_off_unknown_predictions=int((erased==8).sum())))
            # Censor the last event's intended score .49 or .51 to exactly .50.
            # Identical visible stream, incompatible correct final values.
            # This is an information-loss diagnostic, not a train-distribution task.
            g=torch.Generator().manual_seed(9_000_000+seed)
            n=128
            x=torch.zeros(n,5,3);x[:,:4,0]=torch.arange(4)
            x[:,:4,1]=torch.randint(VALUES,(n,4),generator=g);x[:,:4,2]=.85
            key=torch.randint(KEYS,(n,),generator=g);b=torch.arange(n)
            old=x[b,key,1].long();new=(old+torch.randint(1,VALUES,(n,),generator=g))%VALUES
            x[:,4,0]=key;x[:,4,1]=new;x[:,4,2]=.5
            pred=predict(m,x,variant,threshold)[b,key]
            correct=int((pred==old).sum()+(pred==new).sum());maximum=n
            if correct>maximum:raise RuntimeError('Information-limit violation')
            ambiguity.append(dict(kind=kind,seed=seed,curriculum=curr,variant=variant,
                pairs=n,answers=2*n,correct=correct,maximum_without_new_evidence=maximum,
                visible_data_sha256=hashlib.sha256(x.numpy().tobytes()).hexdigest(),
                hidden_intent_never_supplied=True))
        if before!=weights_digest(m):raise RuntimeError('Checks changed weights')
    result=dict(status='PASS',lifecycle=lifecycle,reset_predictions=resets,ambiguity=ambiguity,
        qualification='Research snapshots only; no model integrated into NSS; same chunk boundaries used for exact continuation. Alternative chunking is tolerance-tested in unit suite.',
        ambiguity_note='50% pairwise upper bound follows by construction from identical observations with two incompatible latent-intent labels. It is not a discovered neural limitation or evidence of test leakage.')
    write_json(output/'ADDITIONAL_CHECKS.json',result);return result


@torch.no_grad()
def noise_belief_control(x):
    """Distribution-informed filter, not matched-teaching learned competence.

    Initializes from the same observation-only ledger on the eight-event setup.
    Uses the stated suffix prior P(write)=.08, pre-noise uniform score ranges,
    and Gaussian sigma=.10. Hidden intended scores/targets never enter.
    """
    import math
    observed,_=exact_latest(x[:,:8])
    belief=torch.nn.functional.one_hot(observed,9).to(torch.float64)
    q=x[:,8:,2].to(torch.float64)
    sigma=.1
    def cdf(z):return .5*(1+torch.erf(z/math.sqrt(2)))
    def integral(z):return z*cdf(z)+torch.exp(-z*z/2)/math.sqrt(2*math.pi)
    def likelihood(lo,hi):
        d=(cdf((q-lo)/sigma)-cdf((q-hi)/sigma))/(hi-lo)
        low=sigma/(hi-lo)*(integral(torch.tensor(-lo/sigma,dtype=torch.float64))-integral(torch.tensor(-hi/sigma,dtype=torch.float64)))
        high=sigma/(hi-lo)*(integral(torch.tensor((hi-1)/sigma,dtype=torch.float64))-integral(torch.tensor((lo-1)/sigma,dtype=torch.float64)))
        return torch.where(q<=0,low,torch.where(q>=1,high,d)).clamp_min(1e-300)
    positive=.08*likelihood(.55,.75)
    negative=.92*likelihood(.25,.45)
    admitted_probability=positive/(positive+negative)
    b=torch.arange(len(x))
    for t in range(q.shape[1]):
        k=x[:,8+t,0].long();v=x[:,8+t,1].long();p=admitted_probability[:,t]
        old=belief[b,k]
        replacement=torch.nn.functional.one_hot(v,9).to(torch.float64)
        belief[b,k]=(1-p[:,None])*old+p[:,None]*replacement
    if not torch.isfinite(belief).all() or not torch.allclose(belief.sum(-1),torch.ones_like(belief[:,:,0]),atol=1e-10):
        raise RuntimeError('Invalid belief distribution')
    return belief.argmax(-1),belief


def run_noise_control(root,output):
    from .data import HORIZONS,digest
    rows=[]
    for seed in range(301,306):
        for horizon in HORIZONS:
            x,y,p=evaluation_batch(seed,'noisy_observation',horizon)
            t0=time.perf_counter();pred,belief=noise_belief_control(x);elapsed=time.perf_counter()-t0
            rows.append(dict(seed=seed,horizon=horizon,condition='noisy_observation',
                dataset_sha256=digest(x,y),eval_seconds=elapsed,**metrics(pred,y,p)))
    result=dict(status='RUN',rows=rows,extra_model_knowledge=dict(write_prior=.08,sigma=.1,negative_score_range=[.25,.45],positive_score_range=[.55,.75]),
        truth_labels_supplied_to_filter=False,training_steps=0,
        persistent_belief_bytes_per_stream=4*9*8,
        temporary_work='This batched reference materializes posterior probabilities across the supplied tape; total peak is not constant-memory.',
        limitation='Noise-distribution-informed reference, not a fair equal-knowledge win over learners trained on uncorrupted signals; not a production belief model.')
    write_json(Path(output)/'NOISE_BELIEF_CONTROL.json',result);return result
