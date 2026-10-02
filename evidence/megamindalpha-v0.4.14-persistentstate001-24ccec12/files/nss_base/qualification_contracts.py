"""Strict local claim contracts. Qualification is evidence, never an execution permit."""
from copy import deepcopy
from datetime import datetime
import re

from .neural_contracts import encoded, fields, fingerprint
from .runtime import fail

FORMAT = 'MegaMindAlpha.QualificationEvidence002'
AUTHORITY = 'TRUSTED_LOCAL_CLAIM_ONLY'
PROFILES = ('CORE', 'A', 'B', 'AB')
EDGES = (('AB', 'A'), ('A', 'CORE'))
CANDIDATE_FORMAT = 'MegaMindAlpha.CandidateEvidence001'
CANDIDATE_PROFILES = ('CORE', 'A2', 'A2B')
CANDIDATE_EDGES = (('A2B', 'A2'), ('A2', 'CORE'))
POLICY = {
    'id': 'neural_linear_claim_v1', 'version': 1,
    'minimum_accuracy': 0.95, 'minimum_ablation_gap': 0.10,
    'verification_repeats': 2,
    'profile_fixture': 'all_64_developer_visible_test_pairs',
    'transition_fixture': 'first_4_developer_visible_test_pairs',
    'recovery_atol_max': 0.000001, 'recovery_rtol_max': 0.000001,
    'scope': 'EXACT_NEURAL_LINEAR_DEVELOPMENT_CLAIM',
    'deployment_authorized': False,
}
POLICY_HASH = fingerprint(POLICY)


def identifier(value):
    if type(value) is not str or not re.fullmatch(r'[A-Za-z0-9_.:-]{1,96}', value):
        fail('VALIDATION_FAILED', 'Invalid local identifier')
    return value


def digest_value(value):
    if type(value) is not str or not re.fullmatch('[0-9a-f]{64}', value):
        fail('VALIDATION_FAILED', 'Expected SHA-256 identity')
    return value


def text(value, limit=2000):
    if type(value) is not str or not value.strip() or len(value) > limit:
        fail('VALIDATION_FAILED', 'Missing or oversized explanation')
    return value


def timestamp(value):
    if type(value) is not str or not re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value):
        fail('VALIDATION_FAILED', 'Expected UTC timestamp with second resolution')
    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        fail('VALIDATION_FAILED', 'Invalid calendar timestamp')
    return value


def _policy_intact():
    if fingerprint(POLICY) != POLICY_HASH:
        fail('INCOMPATIBLE_CONFIGURATION', 'Installed qualification policy was mutated')


def manifest(value):
    _policy_intact()
    fields(value, ('schema_version', 'format', 'operators', 'policy_sha256'))
    encoded(value)
    if type(value['schema_version']) is not int or value['schema_version'] != 1 or value['format'] != FORMAT:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported qualification store')
    if value['policy_sha256'] != POLICY_HASH:
        fail('INCOMPATIBLE_CONFIGURATION', 'Qualification policy differs')
    ops = value['operators']
    if type(ops) is not list or not 2 <= len(ops) <= 32:
        fail('VALIDATION_FAILED', 'Require bounded operator declarations')
    ids = []
    for op in ops:
        fields(op, ('id', 'roles'))
        ids.append(identifier(op['id']))
        roles = op['roles']
        if (type(roles) is not list or not roles or any(type(r) is not str or r not in ('PRODUCER', 'REVIEWER') for r in roles)
                or len(set(roles)) != len(roles)):
            fail('VALIDATION_FAILED', 'Invalid local role declaration')
    if len(set(ids)) != len(ids):
        fail('VALIDATION_FAILED', 'Duplicate operator')
    if not any('PRODUCER' in op['roles'] for op in ops) or not any('REVIEWER' in op['roles'] for op in ops):
        fail('VALIDATION_FAILED', 'Both local workflow roles are required')
    return deepcopy(value)


def authorize(m, actor, role, producer=None):
    identifier(actor)
    if producer is not None and actor == producer:
        fail('AUTHORIZATION_DENIED', 'Producer cannot review its own candidate')
    if not any(op['id'] == actor and role in op['roles'] for op in m['operators']):
        fail('AUTHORIZATION_DENIED', 'Local operator role is not declared')


def claim(value, *, source_format=None):
    if source_format not in (None, CANDIDATE_FORMAT):
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown claim evidence family')
    profiles = CANDIDATE_PROFILES if source_format == CANDIDATE_FORMAT else PROFILES
    edges = CANDIDATE_EDGES if source_format == CANDIDATE_FORMAT else EDGES
    if type(value) is not dict:
        fail('VALIDATION_FAILED', 'Claim must be a typed object')
    if value.get('kind') == 'PROFILE':
        fields(value, ('kind', 'profile'))
        if type(value['profile']) is not str or value['profile'] not in profiles:
            fail('INCOMPATIBLE_CONFIGURATION', 'Only explicit profiles of the selected evidence family are supported')
    elif value.get('kind') == 'TRANSITION':
        fields(value, ('kind', 'source', 'destination', 'mode'))
        if (type(value['source']) is not str or type(value['destination']) is not str
                or (value['source'], value['destination']) not in edges or value['mode'] != 'replay'):
            fail('INCOMPATIBLE_CONFIGURATION', 'Directed transition has no implemented checker')
    else:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown claim kind')
    return deepcopy(value)


def required_profiles(c, *, source_format=None):
    c = claim(c, source_format=source_format)
    if c['kind'] == 'PROFILE':
        return [] if c['profile'] == 'CORE' else ['CORE']
    return sorted(set(('CORE', c['source'], c['destination'])))


def binding(value):
    candidate = type(value) is dict and 'source_format' in value
    extra = ('source_format', 'candidate_lineage') if candidate else ()
    fields(value, ('run_id', 'plan_sha256', 'report_sha256', 'trial_seed', 'precision',
                   'checkpoint_hashes', 'core_generation', 'tokenizer', 'context_abi', 'overlay_abi',
                   'profile_ecids', 'runtime_sha256', 'code_sha256', 'environment_sha256',
                   'data_binding_sha256', 'test_pairs_sha256', 'transition_pairs_sha256',
                   'protocol_sha256', 'checker') + extra)
    encoded(value)
    identifier(value['run_id'])
    for k in ('plan_sha256', 'report_sha256', 'runtime_sha256', 'code_sha256', 'environment_sha256',
              'data_binding_sha256', 'test_pairs_sha256', 'transition_pairs_sha256', 'protocol_sha256'):
        digest_value(value[k])
    if type(value['trial_seed']) is not int or not 0 <= value['trial_seed'] < 2**31:
        fail('VALIDATION_FAILED', 'Invalid trial seed')
    if type(value['precision']) is not str or value['precision'] not in ('fp32', 'ternary_core_reference'):
        fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported precision')
    fields(value['checkpoint_hashes'], ('core', 'A', 'B', 'A2') if candidate else ('core', 'A', 'B', 'joint', 'A2'))
    fields(value['profile_ecids'], CANDIDATE_PROFILES if candidate else PROFILES)
    if candidate:
        if value['source_format'] != CANDIDATE_FORMAT:
            fail('INCOMPATIBLE_CONFIGURATION', 'Unknown qualification source format')
        candidate_lineage(value['candidate_lineage'])
    for h in [*value['checkpoint_hashes'].values(), *value['profile_ecids'].values()]:
        digest_value(h)
    for k, expected in {'core_generation': 'neural-probe-G1', 'tokenizer': 'one_hot_16_pair_v1',
                        'context_abi': 'symbol-state-v1', 'overlay_abi': 'two-linear-slots-v1',
                        'checker': 'candidate_A2_profile_and_recovery_v1' if candidate else 'symbol_pair_accuracy_and_recovery_v1'}.items():
        if value[k] != expected:
            fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported ' + k)
    return deepcopy(value)


def request(value):
    _policy_intact()
    fields(value, ('schema_version', 'request_id', 'producer_id', 'at', 'claim', 'binding',
                   'prerequisites', 'policy_sha256', 'purpose'))
    encoded(value)
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown request schema')
    identifier(value['request_id']); identifier(value['producer_id']); timestamp(value['at'])
    binding(value['binding']); claim_for_binding(value['claim'], value['binding'])
    if value['policy_sha256'] != POLICY_HASH or value['purpose'] != 'LOCAL_DEVELOPMENT_QUALIFICATION':
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown policy or request purpose')
    deps = value['prerequisites']
    if type(deps) is not list or len(deps) != len(required_profiles(value['claim'], source_format=value['binding'].get('source_format'))):
        fail('VALIDATION_FAILED', 'Explicit Core/endpoint prerequisites are required')
    for d in deps:
        identifier(d)
    if len(set(deps)) != len(deps) or value['request_id'] in deps:
        fail('VALIDATION_FAILED', 'Invalid prerequisite identity')
    return deepcopy(value)


def decision(value):
    fields(value, ('schema_version', 'operation_id', 'request_id', 'request_sha256',
                   'reviewer_id', 'at', 'recommendation', 'reason'))
    encoded(value)
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown decision schema')
    for k in ('operation_id', 'request_id', 'reviewer_id'):
        identifier(value[k])
    digest_value(value['request_sha256']); timestamp(value['at']); text(value['reason'])
    if type(value['recommendation']) is not str or value['recommendation'] not in ('ACCEPT', 'REJECT', 'INCONCLUSIVE'):
        fail('VALIDATION_FAILED', 'Unknown review recommendation')
    return deepcopy(value)


def revocation(value):
    fields(value, ('schema_version', 'operation_id', 'request_id', 'certificate_sha256',
                   'reviewer_id', 'at', 'reason'))
    encoded(value)
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown revocation schema')
    for k in ('operation_id', 'request_id', 'reviewer_id'):
        identifier(value[k])
    digest_value(value['certificate_sha256']); timestamp(value['at']); text(value['reason'])
    return deepcopy(value)


def verification(value):
    _policy_intact()
    fields(value, ('schema_version', 'request_sha256', 'binding_sha256', 'claim', 'policy_sha256',
                   'verdict', 'checks', 'repeats', 'checker_identity', 'limits', 'deployment_authorized'))
    encoded(value)
    if type(value['schema_version']) is not int or value['schema_version'] != 1 or value['deployment_authorized'] is not False:
        fail('VALIDATION_FAILED', 'Invalid verification authority')
    for k in ('request_sha256', 'binding_sha256'):
        digest_value(value[k])
    if value['policy_sha256'] != POLICY_HASH:
        fail('INCOMPATIBLE_CONFIGURATION', 'Verification policy differs')
    if type(value['verdict']) is not str or value['verdict'] not in ('PASS', 'FAIL', 'INCONCLUSIVE', 'NOT_RUN'):
        fail('VALIDATION_FAILED', 'Unknown verification verdict')
    if type(value['checks']) is not list or len(value['checks']) > 64:
        fail('VALIDATION_FAILED', 'Invalid bounded checks')
    for c in value['checks']:
        fields(c, ('id', 'passed', 'observed', 'requirement'))
        identifier(c['id']); text(c['requirement'])
        if type(c['passed']) is not bool:
            fail('VALIDATION_FAILED', 'Check outcome must be Boolean')
    if type(value['repeats']) is not list or len(value['repeats']) > POLICY['verification_repeats']:
        fail('VALIDATION_FAILED', 'Invalid repeat count')
    fields(value['checker_identity'], ('name', 'code_sha256', 'numerical_backend_sha256'))
    if value['checker_identity']['name'] not in ('qualification_neural_v1', 'qualification_candidate_v1'):
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown verifier')
    claim(value['claim'], source_format=CANDIDATE_FORMAT if value['checker_identity']['name']=='qualification_candidate_v1' else None)
    digest_value(value['checker_identity']['code_sha256']); digest_value(value['checker_identity']['numerical_backend_sha256'])
    if type(value['limits']) is not list or not value['limits'] or any(type(x) is not str or not x for x in value['limits']):
        fail('VALIDATION_FAILED', 'Verification scope limits are mandatory')
    if value['verdict'] == 'PASS' and (not value['checks'] or not all(c['passed'] for c in value['checks'])
            or len(value['repeats']) != POLICY['verification_repeats']
            or len({fingerprint(v) for v in value['repeats']}) != 1):
        fail('VALIDATION_FAILED', 'Passing claim requires complete repeatable checks')
    return deepcopy(value)


def candidate_lineage(x):
    fields(x, ('cycle_sha256', 'proposal_sha256', 'producer_id', 'training_receipt',
        'evaluation_receipt', 'snapshot', 'parent_binding_sha256', 'parent_core_certificate',
        'criteria_sha256', 'retention_pairs_sha256'))
    identifier(x['producer_id'])
    for k in ('cycle_sha256','proposal_sha256','parent_binding_sha256','criteria_sha256','retention_pairs_sha256'):
        digest_value(x[k])
    for k in ('training_receipt', 'evaluation_receipt'):
        r = x[k]; fields(r, ('id','plan_sha256','report_sha256','verdict','authority'))
        identifier(r['id']); digest_value(r['plan_sha256']); digest_value(r['report_sha256'])
        if r['verdict'] not in ('PASS','FAIL','INCONCLUSIVE') or r['authority'] != 'NONE':
            fail('VALIDATION_FAILED', 'Invalid exact numerical owner receipt')
    fields(x['snapshot'], ('snapshot_id','sha256','member_count'))
    identifier(x['snapshot']['snapshot_id']); digest_value(x['snapshot']['sha256'])
    if type(x['snapshot']['member_count']) is not int or x['snapshot']['member_count'] != 2:
        fail('VALIDATION_FAILED', 'Candidate recipe requires two exact dataset members')
    fields(x['parent_core_certificate'], ('request_id','certificate_sha256'))
    identifier(x['parent_core_certificate']['request_id']); digest_value(x['parent_core_certificate']['certificate_sha256'])


def claim_for_binding(c, b):
    """Original defaults stay strict; candidates select an explicit evidence format."""
    return claim(c, source_format=b.get('source_format'))


def checker_name(b):
    return 'qualification_candidate_v1' if b.get('source_format') == CANDIDATE_FORMAT else 'qualification_neural_v1'


def review_actor(req, actor):
    if actor == req['binding'].get('candidate_lineage', {}).get('producer_id'):
        fail('AUTHORIZATION_DENIED', 'Actual candidate producer cannot review its own output')
