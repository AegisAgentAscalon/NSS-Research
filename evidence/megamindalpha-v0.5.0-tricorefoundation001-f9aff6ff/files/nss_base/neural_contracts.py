"""Pure contracts for a bounded, explicitly synthetic numerical experiment."""
from copy import deepcopy
from hashlib import sha256
import json
import math
from pathlib import Path

from .runtime import fail
from .serialization import decode

FORMAT = 'MegaMindAlpha.NeuralProbe001'
CHECKER = 'symbol_pair_accuracy_and_recovery_v1'
MAX_BYTES = 2 * 1024 * 1024
MODES = ('fp32', 'ternary_core_reference')
CODEC = {'schema_version': 1, 'id': 'one_hot_16_pair_v1', 'width': 16,
         'symbols': list(range(16)), 'sequence_length': 2, 'normalization': 'none'}


def encoded(obj):
    """Bounded canonical JSON; reject floats that cannot be represented finitely."""
    def check(x, depth=0):
        if depth > 20: fail('VALIDATION_FAILED', 'Excessive JSON nesting')
        if type(x) is dict:
            if any(type(k) is not str for k in x): fail('VALIDATION_FAILED', 'Non-text key')
            for v in x.values(): check(v, depth+1)
        elif type(x) is list:
            for v in x: check(v, depth+1)
        elif type(x) is float:
            if not math.isfinite(x): fail('VALIDATION_FAILED', 'Nonfinite number')
        elif type(x) not in (int, str, bool, type(None)):
            fail('VALIDATION_FAILED', 'Unsupported JSON value')
    try:
        check(obj)
        raw = json.dumps(obj, sort_keys=True, separators=(',', ':'), allow_nan=False).encode()
    except (TypeError, ValueError, RecursionError, UnicodeError) as exc:
        if hasattr(exc, 'code'): raise
        fail('VALIDATION_FAILED', 'Invalid JSON document')
    if len(raw) > MAX_BYTES: fail('BUDGET_EXHAUSTED', 'Numerical artifact exceeds byte bound')
    return raw


def fingerprint(obj):
    return sha256(encoded(obj)).hexdigest()


def fields(obj, expected):
    if type(obj) is not dict or set(obj) != set(expected):
        fail('VALIDATION_FAILED', 'Missing or extra contract fields')


def read_document(path):
    try:
        with Path(path).open('rb') as f: raw = f.read(MAX_BYTES+1)
        if len(raw) > MAX_BYTES: fail('BUDGET_EXHAUSTED', 'Input too large')
        value = decode(raw.decode('utf-8')); encoded(value)
        return value
    except (OSError, UnicodeError, RecursionError):
        fail('VALIDATION_FAILED', 'Unreadable JSON document')


def protocol(value):
    fields(value, ('schema_version','experiment','architecture','codec','width','rank',
        'core_steps','overlay_steps','learning_rate','seeds','precisions',
        'max_optimizer_steps','minimum_accuracy','minimum_ablation_gap',
        'recovery_atol','recovery_rtol','evaluation_exposure'))
    encoded(value)
    constants = {'schema_version': 1, 'experiment': 'NeuralProbe001',
        'architecture': 'two_linear_symbol_blocks_v1', 'codec': CODEC['id'], 'width': 16, 'rank': 4,
        'evaluation_exposure': 'DEVELOPER_VISIBLE_SYNTHETIC_HELDOUT_PAIRS'}
    for k,v in constants.items():
        if type(value[k]) is not type(v) or value[k] != v:
            fail('INCOMPATIBLE_CONFIGURATION', 'Unknown protocol '+k)
    for k,upper in [('core_steps',1000),('overlay_steps',1000),('max_optimizer_steps',100000)]:
        if type(value[k]) is not int or not 1<=value[k]<=upper:
            fail('VALIDATION_FAILED', 'Invalid optimizer budget')
    if (type(value['seeds']) is not list or not 1<=len(value['seeds'])<=5
            or any(type(s) is not int or not 0<=s<2**31 for s in value['seeds'])
            or len(set(value['seeds']))!=len(value['seeds'])):
        fail('VALIDATION_FAILED','Invalid/duplicate seeds')
    modes=value['precisions']
    if (type(modes) is not list or not modes or len(modes)>2
            or any(type(m) is not str or m not in MODES for m in modes) or len(set(modes))!=len(modes)):
        fail('VALIDATION_FAILED','Invalid/duplicate precision mode')
    for k,low,high in [('learning_rate',1e-5,.1),('minimum_accuracy',.5,1.),
                       ('minimum_ablation_gap',.01,1.),('recovery_atol',0.,1e-3),('recovery_rtol',0.,1e-3)]:
        v=value[k]
        if type(v) not in (float,int) or not math.isfinite(v) or not low<=v<=high:
            fail('VALIDATION_FAILED', 'Invalid numerical threshold '+k)
    return deepcopy(value)


def pairs(split):
    if split not in ('train','validation','test'): fail('VALIDATION_FAILED','Unknown split')
    return [[i,j] for i in range(16) for j in range(16)
            if (('test' if (i+j)%4==0 else 'validation' if (i+j)%4==1 else 'train') == split)]


def validate_pairs(value, expected_split=None):
    if type(value) is not list or not 1<=len(value)<=256:
        fail('VALIDATION_FAILED','Invalid pair count')
    for row in value:
        if type(row) is not list or len(row)!=2 or any(type(x) is not int or not 0<=x<16 for x in row):
            fail('VALIDATION_FAILED','Expected two symbols in [0,15]')
    if len({tuple(p) for p in value})!=len(value): fail('VALIDATION_FAILED','Duplicate pairs')
    if expected_split is not None and value!=pairs(expected_split):
        fail('CONSTRAINT_CONFLICT','Pairs differ from the declared fixed split')
    return deepcopy(value)


def mapping(name):
    a=list(range(16));b=list(range(16))
    for x,y in [(0,1),(2,3)]: a[x],a[y]=a[y],a[x]
    for x,y in [(1,2),(3,4)]: b[x],b[y]=b[y],b[x]
    a2=a.copy();a2[5],a2[6]=6,5
    maps={'CORE':list(range(16)),'A':a,'B':b,'AB':[b[x] for x in a],
          'A2':a2,'A2B':[b[x] for x in a2]}
    if type(name) is not str or name not in maps: fail('VALIDATION_FAILED','Unknown target mapping')
    return maps[name]


def required_updates(p):
    return len(p['seeds'])*len(p['precisions'])*(p['core_steps']+5*p['overlay_steps'])


def trial_verdict(p,metrics):
    names=('core','A','B','AB','joint','gen2','gen2_retained')
    if any(name not in metrics for name in names): fail('VALIDATION_FAILED','Missing numerical check')
    for m in metrics.values():
        fields(m,('pair_accuracy','token_accuracy','mse','pairs'))
        encoded(m)
        if type(m['pairs']) is not int or m['pairs']<1: fail('VALIDATION_FAILED','Invalid metric count')
        for k in ('pair_accuracy','token_accuracy'):
            if type(m[k]) not in (float,int) or not 0<=m[k]<=1: fail('VALIDATION_FAILED','Invalid accuracy')
        if type(m['mse']) not in (int,float) or m['mse']<0: fail('VALIDATION_FAILED','Invalid MSE')
    if not {'ablation_A','ablation_B','ablation_core'}<=metrics.keys():
        fail('VALIDATION_FAILED','Missing ablation')
    required=all(metrics[n]['pair_accuracy']>=p['minimum_accuracy'] for n in names)
    gap=metrics['AB']['pair_accuracy']-max(metrics[n]['pair_accuracy'] for n in ('ablation_A','ablation_B','ablation_core'))
    return 'PASS' if required and gap>=p['minimum_ablation_gap'] else 'FAIL'
