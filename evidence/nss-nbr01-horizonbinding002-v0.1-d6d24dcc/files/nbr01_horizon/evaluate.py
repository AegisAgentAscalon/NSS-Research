"""Registered evaluation and observation-only controls. No optimization here."""
from __future__ import annotations
import hashlib, json, time
from pathlib import Path
import torch
from .data import CONDITIONS, HORIZONS, evaluation_batch, exact_latest, digest
from .util import load_model, weights_digest, write_json, sha, source_identity


def calibrate(model, seed):
    """Extra explicitly labelled gate data, NOT held-out episode outcomes."""
    g = torch.Generator().manual_seed(5_000_000 + seed)
    x = torch.zeros(1, 2048, 3)
    x[0, :, 0] = torch.randint(4, (2048,), generator=g)
    x[0, :, 1] = torch.randint(8, (2048,), generator=g)
    x[0, :, 2] = torch.rand(2048, generator=g)
    labels = x[0, :, 2] >= .5
    with torch.no_grad():
        scores = model.gates(x)[0]
    max_negative, min_positive = float(scores[~labels].max()), float(scores[labels].min())
    separation = max_negative < min_positive
    if separation:
        threshold = (max_negative + min_positive) / 2
    else:
        unique = scores.unique().sort().values
        choices = torch.cat((torch.tensor([0.]), (unique[:-1]+unique[1:])/2, torch.tensor([1.])))
        errors = ((scores[:, None] >= choices[None, :]) != labels[:, None]).float().mean(0)
        threshold = float(choices[errors.argmin()])
    pred = scores >= threshold
    return dict(threshold=threshold, labelled_events=2048, separable=separation,
                false_admit=int((pred & ~labels).sum()), missed_write=int((~pred & labels).sum()),
                negatives=int((~labels).sum()), positives=int(labels.sum()),
                calibration_dataset_sha256=digest(x,labels), weight_updates=0,
                note='Additional gate labels supplied, unlike fixed0.5. No main episode targets used.')


def metrics(pred, y, protected):
    known, unknown = y < 8, y == 8
    same = pred == y
    b = torch.arange(len(y))
    return dict(n_streams=len(y), n_answers=y.numel(), correct=int(same.sum()),
                known=int(known.sum()), known_correct=int(same[known].sum()),
                unknown=int(unknown.sum()), unknown_correct=int(same[unknown].sum()),
                all_four_correct=int(same.all(1).sum()),
                protected_correct=int(same[b,protected].sum()),
                unknown_predictions=int((pred==8).sum()),
                prediction_sha256=hashlib.sha256(pred.contiguous().numpy().tobytes()).hexdigest())


@torch.no_grad()
def predict(model, x, variant, threshold=.5):
    if variant=='exact_tool':
        _, x = exact_latest(x)
    mode = {'native':'native','hard_fixed':'hard','close_low':'close_low',
            'hard_calibrated':'hard','exact_tool':'native'}[variant]
    pieces=[]
    batch_limit = 16 if model.kind=='tape_reader' else 128
    for s in range(0,len(x),batch_limit):
        logits = model.predict_chunked(x[s:s+batch_limit], mode=mode, threshold=threshold)
        if not torch.isfinite(logits).all(): raise RuntimeError('Nonfinite evaluation')
        pieces.append(logits.argmax(-1))
    return torch.cat(pieces)


def gate_diagnostics(model):
    q = torch.linspace(0,1,10001)
    x = torch.zeros(1,len(q),3); x[0,:,2]=q
    # gates() consumes q only and accepts this diagnostic grid without an
    # episode time-budget implication.
    with torch.no_grad(): s=model.gates(x)[0]
    return dict(q_points=10001, min=float(s.min()),max=float(s.max()),
        monotone_nondecreasing=bool((s[1:]>=s[:-1]).all()),
        q_first_fixed_admission=(float(q[(s>=.5).nonzero()[0]]) if (s>=.5).any() else None),
        gate_at_q0_49=float(s[4900]),gate_at_q0_50=float(s[5000]),gate_at_q0_51=float(s[5100]),
        q_sample=[float(v) for v in q[::100]],gate_sample=[float(v) for v in s[::100]])


@torch.no_grad()
def evaluate_checkpoint(root, path, training, output, calibration=None):
    kind,seed,curriculum = training['kind'],training['seed'],training['curriculum']
    model=load_model(path,kind); before=weights_digest(model)
    variants=['native']
    if kind=='soft_slots': variants += ['hard_fixed','close_low','hard_calibrated']
    if kind=='tape_reader': variants += ['exact_tool']
    if 'hard_calibrated' in variants and calibration is None:
        raise ValueError('Must fix calibration before main episode scoring')
    rows=[]; start=time.perf_counter()
    for condition in CONDITIONS:
        for horizon in HORIZONS:
            x,y,protected=evaluation_batch(seed,condition,horizon)
            data_sha=digest(x,y)
            for variant in variants:
                threshold=calibration['threshold'] if variant=='hard_calibrated' else .5
                t0=time.perf_counter(); pred=predict(model,x,variant,threshold); elapsed=time.perf_counter()-t0
                row=dict(kind=kind,seed=seed,curriculum=curriculum,variant=variant,
                         condition=condition,horizon=horizon,events=x.shape[1],
                         dataset_sha256=data_sha,threshold=threshold,eval_seconds=elapsed,
                         **metrics(pred,y,protected))
                rows.append(row)
    if before!=weights_digest(model): raise RuntimeError('Evaluation changed parameters')
    record=dict(study='NBR-01/HorizonBinding002',kind=kind,seed=seed,curriculum=curriculum,
                checkpoint_sha256=sha(path), weights_unchanged=True, rows=rows,
                eval_wall_seconds=time.perf_counter()-start,calibration=calibration,
                gate_diagnostics=gate_diagnostics(model) if kind in ('soft_slots','hard_slots') else None)
    write_json(output,record)
    print('EVALUATED',path.stem,len(rows),round(record['eval_wall_seconds'],2),flush=True)
    return record


def evaluate_all(root, output):
    root,output=Path(root),Path(output)
    output.mkdir(parents=True,exist_ok=True)
    paths=sorted((root/'evidence/main').glob('*.safetensors'))
    if len(paths)!=40: raise ValueError('Expected all40 registered checkpoint files')
    cpath=output/'CALIBRATIONS.json'
    if cpath.exists(): raise FileExistsError('Refuse to silently replace calibration')
    # All thresholds published before ANY main episode score is examined.
    cal={}
    for p in paths:
        if p.name.startswith('soft_slots_'):
            tr=json.loads(p.with_suffix('.json').read_text())
            cal[p.stem]=calibrate(load_model(p,'soft_slots'),tr['seed'])
    write_json(cpath,dict(time_unix=time.time(),source=source_identity(root),calibrations=cal,
                         main_episode_scores_seen=False,protocol_sha256=sha(root/'spec/protocol.json')))
    for p in paths:
        out=output/(p.stem+'.eval.json')
        if out.exists():raise FileExistsError(out)
        training=json.loads(p.with_suffix('.json').read_text())
        evaluate_checkpoint(root,p,training,out,cal.get(p.stem))
    exact=[]
    for seed in range(301,306):
        for condition in CONDITIONS:
            for horizon in HORIZONS:
                x,y,protected=evaluation_batch(seed,condition,horizon)
                t0=time.perf_counter(); pred,_=exact_latest(x); elapsed=time.perf_counter()-t0
                exact.append(dict(seed=seed,condition=condition,horizon=horizon,
                                  dataset_sha256=digest(x,y),eval_seconds=elapsed,
                                  **metrics(pred,y,protected)))
    write_json(output/'EXACT_CONTROL.json',dict(rows=exact,labels_never_supplied_to_control=True))
