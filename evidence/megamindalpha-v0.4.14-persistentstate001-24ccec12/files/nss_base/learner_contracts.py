"""Bounded learning-plan and outcome contracts; no runtime or release authority."""
from copy import deepcopy
from .dataset_contracts import normalize_request
from .local_journal import epoch
from .neural_contracts import CODEC, encoded, fields, fingerprint, pairs
from .qualification_contracts import binding, digest_value, identifier, text
from .runtime import fail

FORMAT = 'MegaMindAlpha.BoundedLearnerCoordinator001'
RECIPE_ID = 'frozen_core_A2_replacement_v1'
CRITERIA = {'minimum_accuracy': .95, 'minimum_retained_accuracy': .95, 'minimum_gain': .01,
            'repeats': 2, 'suite': 'A2B_with_parent_and_retention_v1'}
PHASES = ('SNAPSHOT', 'TRAIN', 'EVALUATE')
OUTCOMES = ('SUCCESS', 'AUTHORIZATION_DENIED', 'BUDGET_EXHAUSTED', 'CAPABILITY_UNAVAILABLE',
    'CONSTRAINT_CONFLICT', 'INCOMPATIBLE_CONFIGURATION', 'INSUFFICIENT_EVIDENCE',
    'RECOVERY_REQUIRED', 'TRAINING_RESTRICTED', 'VALIDATION_FAILED', 'CONFLICT_REQUIRES_REVIEW',
    'RETENTION_RESTRICTED', 'INTERNAL_FAILURE')


def integer(x, low, high):
    if type(x) is not int or not low <= x <= high:
        fail('VALIDATION_FAILED', 'Invalid bounded learning integer')
    return x


def recipe(x):
    fields(x, ('id', 'seed', 'steps', 'learning_rate'))
    if x['id'] != RECIPE_ID: fail('INCOMPATIBLE_CONFIGURATION', 'Only the installed A2 recipe is supported')
    integer(x['seed'], 0, 2**31-1); integer(x['steps'], 1, 1000)
    if type(x['learning_rate']) not in (float, int) or not 1e-5 <= x['learning_rate'] <= .1:
        fail('VALIDATION_FAILED', 'Invalid learning rate')
    return deepcopy(x)


def manifest(x):
    fields(x, ('schema_version', 'format', 'producer_ids', 'approver_ids'))
    if type(x['schema_version']) is not int or x['schema_version'] != 1 or x['format'] != FORMAT:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown local learner journal')
    for role in ('producer_ids', 'approver_ids'):
        if type(x[role]) is not list or not 1 <= len(x[role]) <= 32:
            fail('VALIDATION_FAILED', 'Explicit bounded operator lists required')
        for v in x[role]: identifier(v)
        if x[role] != sorted(set(x[role])): fail('VALIDATION_FAILED', 'Operator IDs must be unique/sorted')
    if set(x['producer_ids']) & set(x['approver_ids']):
        fail('AUTHORIZATION_DENIED', 'Producer and approver local roles must be distinct')
    return deepcopy(x)


def learning_plan(x):
    fields(x, ('schema_version', 'format', 'cycle_id', 'producer_id', 'at', 'reason',
        'parent', 'parent_core_certificate', 'archive_sha256', 'snapshot_request', 'recipe', 'budget', 'criteria',
        'code_sha256', 'environment_sha256', 'origin', 'authority'))
    encoded(x)
    if type(x['schema_version']) is not int or x['schema_version'] != 1 or x['format'] != FORMAT or x['authority'] != 'NONE':
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown plan version/authority')
    for k in ('cycle_id', 'producer_id'): identifier(x[k])
    epoch(x['at']); text(x['reason']); binding(x['parent']); recipe(x['recipe'])
    fields(x['parent_core_certificate'], ('request_id', 'certificate_sha256'))
    identifier(x['parent_core_certificate']['request_id']); digest_value(x['parent_core_certificate']['certificate_sha256'])
    for k in ('archive_sha256', 'code_sha256', 'environment_sha256'): digest_value(x[k])
    if x['code_sha256'] != x['parent']['code_sha256'] or x['environment_sha256'] != x['parent']['environment_sha256']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Parent evidence and planned execution differ')
    r = normalize_request(x['snapshot_request'])
    if r != x['snapshot_request'] or r['purpose'] != 'training' or r['transform'] != 'curated_text_v1':
        fail('VALIDATION_FAILED', 'Canonical reviewed training snapshot required')
    if r['tokenizer'] != {'id': CODEC['id'], 'version': '1', 'sha256': fingerprint(CODEC)}:
        fail('INCOMPATIBLE_CONFIGURATION', 'Only the fixed symbol codec is supported')
    if len(r['members']) != 2 or sorted(m['split'] for m in r['members']) != ['train', 'validation']:
        fail('VALIDATION_FAILED', 'Recipe requires one reviewed record for each development split')
    fields(x['budget'], ('optimizer_updates', 'evaluation_passes', 'training_attempts'))
    integer(x['budget']['optimizer_updates'], 0, 1000); integer(x['budget']['evaluation_passes'], 0, 2)
    if type(x['budget']['training_attempts']) is not int or x['budget']['training_attempts'] != 1:
        fail('VALIDATION_FAILED', 'Exactly one claimed training attempt per approved plan')
    if encoded(x['criteria']) != encoded(CRITERIA):
        fail('INCOMPATIBLE_CONFIGURATION', 'Acceptance criteria are fixed installed policy, not learner-editable')
    if x['origin'] is not None:
        fields(x['origin'], ('task_id', 'record_sha256', 'context_packet_sha256'))
        identifier(x['origin']['task_id'])
        for k in ('record_sha256', 'context_packet_sha256'): digest_value(x['origin'][k])
    return deepcopy(x)


def snapshot_ref(x):
    fields(x, ('snapshot_id', 'sha256', 'member_count'))
    identifier(x['snapshot_id']); digest_value(x['sha256']); integer(x['member_count'], 2, 2)
    return deepcopy(x)


def numerical_plan(x):
    fields(x, ('schema_version', 'kind', 'learning_plan', 'snapshot', 'training_receipt', 'authority'))
    if type(x['schema_version']) is not int or x['schema_version'] != 1 or x['authority'] != 'NONE':
        fail('VALIDATION_FAILED', 'Invalid numerical owner plan')
    p = learning_plan(x['learning_plan']); s = snapshot_ref(x['snapshot'])
    if s['snapshot_id'] != p['snapshot_request']['snapshot_id']:
        fail('CONSTRAINT_CONFLICT', 'Candidate snapshot differs from the approved plan')
    if x['kind'] == 'OVERLAY_TRAINING':
        if x['training_receipt'] is not None: fail('VALIDATION_FAILED', 'Training cannot import an evaluation receipt')
    elif x['kind'] == 'OVERLAY_EVALUATION':
        run_receipt(x['training_receipt'])
        expected = {**x, 'kind': 'OVERLAY_TRAINING', 'training_receipt': None}
        if x['training_receipt']['plan_sha256'] != fingerprint(expected):
            fail('CONSTRAINT_CONFLICT', 'Evaluation refers to another training plan')
    else: fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported numerical plan kind')
    return deepcopy(x)


def run_receipt(x):
    fields(x, ('id', 'plan_sha256', 'report_sha256', 'verdict', 'authority'))
    identifier(x['id']); digest_value(x['plan_sha256']); digest_value(x['report_sha256'])
    if x['verdict'] not in ('PASS', 'FAIL', 'INCONCLUSIVE') or x['authority'] != 'NONE':
        fail('VALIDATION_FAILED', 'Invalid numerical evidence receipt')
    return deepcopy(x)


def operation_id(p, phase):
    if phase not in PHASES: fail('VALIDATION_FAILED', 'Unknown learning phase')
    return phase.lower() + ':' + fingerprint(p)[:48]


def numerical_input(p, s, receipt=None):
    return numerical_plan({'schema_version': 1, 'kind': 'OVERLAY_EVALUATION' if receipt else 'OVERLAY_TRAINING',
        'learning_plan': p, 'snapshot': s, 'training_receipt': receipt, 'authority': 'NONE'})


def evaluation_verdict(rows):
    if len(rows) != CRITERIA['repeats'] or rows[0] != rows[1]: return 'INCONCLUSIVE'
    m = rows[0]
    return 'PASS' if (all(m[k]['pair_accuracy'] >= CRITERIA['minimum_accuracy'] for k in ('core','A2','A2B'))
        and m['retained_AB']['pair_accuracy'] >= CRITERIA['minimum_retained_accuracy']
        and m['A2B']['pair_accuracy'] - m['parent_on_updated']['pair_accuracy'] >= CRITERIA['minimum_gain']) else 'FAIL'


def metrics(x):
    fields(x, ('core', 'A2', 'A2B', 'retained_AB', 'parent_on_updated'))
    for k, v in x.items():
        fields(v, ('pair_accuracy', 'token_accuracy', 'mse', 'pairs'))
        expected = len([r for r in pairs('test') if all(i not in (5,6) for i in r)]) if k == 'retained_AB' else len(pairs('test'))
        integer(v['pairs'], expected, expected)
        for n in ('pair_accuracy','token_accuracy'):
            if type(v[n]) not in (int,float) or not 0 <= v[n] <= 1: fail('VALIDATION_FAILED','Invalid accuracy')
        if type(v['mse']) not in (int,float) or v['mse'] < 0: fail('VALIDATION_FAILED','Invalid MSE')
    encoded(x); return deepcopy(x)


OWNER_KEYS=('cycles','archive','snapshots','tokenizer','qualifications','parent_journal','parent_data','candidates','evaluations')


def owner_paths(config):
    from pathlib import Path
    fields(config,OWNER_KEYS)
    if any(type(v) is not str or not 1<=len(v)<=4096 for v in config.values()):
        fail('VALIDATION_FAILED','Explicit local owner paths required')
    return {k:Path(v).resolve() for k,v in config.items()}

