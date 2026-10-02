"""Installed bounded neural recipe and evaluator, not arbitrary plugin execution.

Storage and permissions are provided by their public owners. Imported only for
opt-in neural use. Never trains the parent Core, A, or B; only a new A2 candidate.
"""
from copy import deepcopy
import torch
from torch.nn import functional as F
from .candidate_records import training_plan, training_report, evaluation_plan, evaluation_report
from .learner_contracts import evaluation_verdict
from .local_journal import fault
from .neural_backend import (Overlay, assert_frozen, checkpoint, deterministic_cpu,
    encode_pairs, fit, freeze, load_checkpoint, metric, targets)
from .neural_contracts import encoded, fingerprint, pairs, validate_pairs
from .runtime import ContractError, fail


def existing(store, run_id, plan):
    try: r = store.inspect(run_id)
    except ContractError as e:
        if e.code == 'INSUFFICIENT_EVIDENCE': return None
        raise
    if r['plan'] != plan: fail('CONSTRAINT_CONFLICT','Numerical run belongs to another immutable plan')
    return r


def train_candidate(store, run_id, plan, *, artifacts, train_pairs, gate, crash_at=None):
    """One attempt. PREPARED retry is ambiguous, never an implicit training restart."""
    p = training_plan(plan); old = existing(store, run_id, p)
    if old is not None:
        if old['status'] == 'FINALIZED': return old
        fail('RECOVERY_REQUIRED','Training dispatch has no committed candidate; explicitly abandon, not retrain')
    gate(); store.prepare(run_id, p); fault(crash_at,'after_training_prepared')
    cfg = p['learning_plan']['recipe']; parent = p['learning_plan']['parent']['checkpoint_hashes']
    train_pairs = validate_pairs(train_pairs, 'train')
    if set(artifacts) != {'core','A','B'}: fail('VALIDATION_FAILED','Exact three parent artifacts required')
    with deterministic_cpu(cfg['seed']):
        mods = {k:load_checkpoint(v,parent[k]) for k,v in artifacts.items()}
        core = mods['core']; x = encode_pairs(train_pairs); candidate = Overlay(4)
        initial = fingerprint(checkpoint(candidate))
        with torch.no_grad(): noop = torch.equal(core(x), core(x,a=candidate))
        if not noop: fail('VALIDATION_FAILED','Fresh overlay must be a no-op')
        wanted = targets(train_pairs, 'A2')
        log = fit(candidate.parameters(), lambda:F.mse_loss(core(x,a=candidate),wanted),
            cfg['steps'], cfg['learning_rate'], gate)
        freeze(candidate)
        for k,m in mods.items(): assert_frozen(m,parent[k])
        ck = {**deepcopy(artifacts), 'A2':checkpoint(candidate)}
        log.update(blank_noop=noop, weights_changed=initial!=fingerprint(ck['A2']),
                   train_input_tokens=cfg['steps']*len(train_pairs)*2)
    r = training_report(p, {'schema_version':1,'plan_sha256':fingerprint(p),
        'scope':'ARTIFACT_TRAINING_COMPLETE_NOT_CAPABILITY_APPROVAL','verdict':'PASS','authority':'NONE',
        'artifacts':ck,'checkpoint_hashes':{k:fingerprint(v) for k,v in ck.items()},'training':log,
        'invariants':{'core_unchanged':True,'accepted_overlays_unchanged':True,'only_candidate_trained':True}})
    fault(crash_at,'after_training_computed'); gate()
    out = store.finalize(run_id,r); fault(crash_at,'after_training_sealed'); return out


def scores(artifacts, hashes, seed):
    """Fresh checkpoint reload and no-grad scoring for first execution and verification."""
    with deterministic_cpu(seed):
        mods = {k:load_checkpoint(v,hashes[k]) for k,v in artifacts.items()}
        c=mods['core']; test=pairs('test'); x=encode_pairs(test)
        retained=[v for v in test if all(i not in (5,6) for i in v)]
        with torch.no_grad():
            return {'core':metric(c(x),test,'CORE'),
                'A2':metric(c(x,a=mods['A2']),test,'A2'),
                'A2B':metric(c(x,a=mods['A2'],b=mods['B']),test,'A2B'),
                'retained_AB':metric(c(encode_pairs(retained),a=mods['A2'],b=mods['B']),retained,'AB'),
                'parent_on_updated':metric(c(x,a=mods['A'],b=mods['B']),test,'A2B')}


def training_inputs(eplan, training):
    if (training['status'] != 'FINALIZED' or training['receipt'] != eplan['training_receipt']
            or training['plan'] != {**eplan, 'kind':'OVERLAY_TRAINING', 'training_receipt':None}):
        fail('CONSTRAINT_CONFLICT','Evaluation requires the exact completed training-owner receipt')
    return training_report(training['plan'],training['report'])


def evaluate_candidate(store, run_id, plan, *, training, gate, crash_at=None):
    p=evaluation_plan(plan); old=existing(store,run_id,p)
    if old is not None:
        if old['status']=='FINALIZED': return old
        fail('RECOVERY_REQUIRED','Unfinished evaluation requires explicit abandonment, not unbounded retries')
    t=training_inputs(p,training); gate(); store.prepare(run_id,p); fault(crash_at,'after_evaluation_prepared')
    repeats=[]
    for _ in range(p['learning_plan']['criteria']['repeats']):
        gate(); repeats.append(scores(t['artifacts'],t['checkpoint_hashes'],p['learning_plan']['recipe']['seed']))
    r=evaluation_report(p, {'schema_version':1,'plan_sha256':fingerprint(p),
        'scope':'DEVELOPER_VISIBLE_SYNTHETIC_OVERLAY_EVALUATION','authority':'NONE',
        'verdict':evaluation_verdict(repeats),'repeats':repeats,'checkpoint_hashes':t['checkpoint_hashes'],
        'test_pairs_sha256':fingerprint(pairs('test'))})
    fault(crash_at,'after_evaluation_computed'); gate()
    out=store.finalize(run_id,r); fault(crash_at,'after_evaluation_sealed'); return out


def verify_candidate(evaluation, training, *, gate):
    """Current evidence verification, never a qualification or learned judgment."""
    if evaluation['status']!='FINALIZED': fail('INSUFFICIENT_EVIDENCE','Incomplete evaluation')
    p=evaluation_plan(evaluation['plan']);r=evaluation_report(p,evaluation['report']);t=training_inputs(p,training)
    if r['checkpoint_hashes']!=t['checkpoint_hashes']: fail('VALIDATION_FAILED','Evaluation changed candidate hashes')
    for recorded in r['repeats']:
        gate()
        if scores(t['artifacts'],t['checkpoint_hashes'],p['learning_plan']['recipe']['seed'])!=recorded:
            fail('VALIDATION_FAILED','Exact numerical replay differs; never relax thresholds on retry')
    gate(); return {'status':'SUCCESS','verdict':r['verdict'],'recomputed_repeats':len(r['repeats']),'authority':'NONE'}
