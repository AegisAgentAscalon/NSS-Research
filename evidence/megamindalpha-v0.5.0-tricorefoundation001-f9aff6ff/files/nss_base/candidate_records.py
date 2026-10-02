"""Candidate artifact and numerical-report owners using existing journal mechanics.

These sibling formats deliberately cannot be interpreted as NeuralProbe001 evidence
by a caller as independent qualification. Qualification uses the separate CandidateEvidence adapter. One store owns each report; the coordinator stores refs.
"""
from copy import deepcopy
from .learner_contracts import evaluation_verdict, metrics, numerical_plan
from .neural_contracts import encoded, fields, fingerprint
from .neural_records import ProbeRuns
from .runtime import fail


def training_plan(x):
    x = numerical_plan(x)
    if x['kind'] != 'OVERLAY_TRAINING': fail('INCOMPATIBLE_CONFIGURATION','Expected a training-owner plan')
    return x


def evaluation_plan(x):
    x = numerical_plan(x)
    if x['kind'] != 'OVERLAY_EVALUATION': fail('INCOMPATIBLE_CONFIGURATION','Expected an evaluation-owner plan')
    return x


def training_report(p, r):
    p = training_plan(p)
    fields(r, ('schema_version','plan_sha256','scope','verdict','authority','artifacts',
        'checkpoint_hashes','training','invariants'))
    encoded(r)
    if (type(r['schema_version']) is not int or r['schema_version'] != 1 or r['plan_sha256'] != fingerprint(p)
            or r['scope'] != 'ARTIFACT_TRAINING_COMPLETE_NOT_CAPABILITY_APPROVAL' or r['verdict'] != 'PASS' or r['authority'] != 'NONE'):
        fail('VALIDATION_FAILED','Invalid candidate training report')
    fields(r['artifacts'], ('core','A','B','A2')); fields(r['checkpoint_hashes'], ('core','A','B','A2'))
    if r['checkpoint_hashes'] != {k:fingerprint(v) for k,v in r['artifacts'].items()}:
        fail('VALIDATION_FAILED','Candidate artifact digest mismatch')
    parent = p['learning_plan']['parent']['checkpoint_hashes']
    if any(r['checkpoint_hashes'][k] != parent[k] for k in ('core','A','B')):
        fail('VALIDATION_FAILED','Parent Core or accepted overlays changed')
    # Structural data validation only. Actual loading and checking belong to the backend.
    for k, a in r['artifacts'].items():
        fields(a, ('schema_version','architecture','kind','metadata','tensors'))
        if a['kind'] != ('core' if k == 'core' else 'overlay'):
            fail('VALIDATION_FAILED','Artifact role substitution')
        if k == 'A2' and a['metadata'] != {'mode':'fp32','rank':4}:
            fail('VALIDATION_FAILED','Candidate violates fixed slot/rank contract')
    fields(r['training'], ('updates','first_loss','last_loss','seconds','blank_noop','weights_changed','train_input_tokens'))
    t = r['training']; steps = p['learning_plan']['recipe']['steps']
    if (type(t['updates']) is not int or t['updates'] != steps or t['train_input_tokens'] != steps*128*2
            or type(t['train_input_tokens']) is not int or t['blank_noop'] is not True or t['weights_changed'] is not True):
        fail('VALIDATION_FAILED','Invalid optimizer/update ownership evidence')
    for k in ('first_loss','last_loss','seconds'):
        if type(t[k]) not in (float,int) or t[k] < 0: fail('VALIDATION_FAILED','Invalid training observation')
    fields(r['invariants'], ('core_unchanged','accepted_overlays_unchanged','only_candidate_trained'))
    if any(v is not True for v in r['invariants'].values()): fail('VALIDATION_FAILED','Candidate violated an invariant')
    return deepcopy(r)


def evaluation_report(p, r):
    p = evaluation_plan(p)
    fields(r, ('schema_version','plan_sha256','scope','authority','verdict','repeats','checkpoint_hashes','test_pairs_sha256'))
    encoded(r)
    if (type(r['schema_version']) is not int or r['schema_version'] != 1 or r['plan_sha256'] != fingerprint(p)
        or r['scope'] != 'DEVELOPER_VISIBLE_SYNTHETIC_OVERLAY_EVALUATION' or r['authority'] != 'NONE'):
        fail('VALIDATION_FAILED','Invalid candidate evaluation report')
    from .neural_contracts import pairs
    if r['test_pairs_sha256'] != fingerprint(pairs('test')): fail('VALIDATION_FAILED','Evaluation fixture changed')
    fields(r['checkpoint_hashes'], ('core','A','B','A2'))
    from .qualification_contracts import digest_value
    for h in r['checkpoint_hashes'].values(): digest_value(h)
    if any(r['checkpoint_hashes'][k] != p['learning_plan']['parent']['checkpoint_hashes'][k] for k in ('core','A','B')):
        fail('VALIDATION_FAILED','Evaluation parent artifact substitution')
    if type(r['repeats']) is not list or len(r['repeats']) != 2:
        fail('VALIDATION_FAILED','Exactly two planned evaluation repeats required')
    for row in r['repeats']: metrics(row)
    if r['verdict'] != evaluation_verdict(r['repeats']):
        fail('VALIDATION_FAILED','Verdict differs from the frozen acceptance rules')
    return deepcopy(r)


class CandidateRuns(ProbeRuns):
    """Stores new-overlay artifacts; PASS means sealed artifacts, not qualification."""
    filename = 'candidate_runs.sqlite3'
    format = 'MegaMindAlpha.FrozenCoreOverlayCandidate001'
    validate_plan = staticmethod(training_plan)
    validate_report = staticmethod(training_report)


class CandidateEvaluations(ProbeRuns):
    """Stores exact numerical evaluations without deployment authority."""
    filename = 'candidate_evaluations.sqlite3'
    format = 'MegaMindAlpha.CandidateEvaluation001'
    validate_plan = staticmethod(evaluation_plan)
    validate_report = staticmethod(evaluation_report)
