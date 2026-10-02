"""Pure contracts for a bounded LOCAL permission protocol, not authentication.

Only the two existing NeuralProbe001 replay transitions over the four qualified
fixture inputs are in scope. A host grant is NOT an Aegis Runtime execution permit.
"""
from copy import deepcopy
from .neural_contracts import encoded, fields, fingerprint, pairs
from .qualification_contracts import binding, claim, digest_value, identifier, text
from .runtime import fail

FORMAT = 'MegaMindAlpha.LocalNexusPermissions002'
OPERATION = 'NEURAL_PROBE_REPLAY'
AUTHORITY = 'TRUSTED_LOCAL_DEVELOPMENT_OPERATION_GRANT'
POLICY = {
    'version': 1, 'operation': OPERATION,
    'max_ttl_seconds': 900, 'max_uses': 1,
    'input_scope': 'EXACT_FIRST_FOUR_NEURAL_PROBE_TEST_PAIRS',
    'transitions': [['AB', 'A'], ['A', 'CORE']],
    'issuer_must_differ_from_caller': True,
    'delegation': False, 'deployment_authorized': False,
    'runtime_execution_permit': False,
}
POLICY_HASH = fingerprint(POLICY)
ROLES = ('ISSUER', 'EXECUTOR', 'RECONCILER')
MAX_EVENTS = 2000
MAX_HISTORY_BYTES = 16 * 1024 * 1024
ZERO = '0' * 64


def epoch(value):
    if type(value) is not int or not 0 <= value <= 253402300799:
        fail('VALIDATION_FAILED', 'Expected bounded whole UTC epoch seconds')
    return value


def intact():
    if fingerprint(POLICY) != POLICY_HASH:
        fail('INCOMPATIBLE_CONFIGURATION', 'Installed permission policy changed')


def manifest(value):
    intact()
    fields(value, ('schema_version', 'format', 'store_id', 'policy_sha256', 'operators'))
    encoded(value)
    if type(value['schema_version']) is not int or value['schema_version'] != 1 or value['format'] != FORMAT:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported permission store')
    identifier(value['store_id'])
    if value['policy_sha256'] != POLICY_HASH:
        fail('INCOMPATIBLE_CONFIGURATION', 'Permission policy differs')
    operators = value['operators']
    if type(operators) is not list or not 2 <= len(operators) <= 32:
        fail('VALIDATION_FAILED', 'Bounded local operator declarations required')
    ids = []
    for item in operators:
        fields(item, ('id', 'roles')); ids.append(identifier(item['id']))
        roles = item['roles']
        if (type(roles) is not list or not roles or len(roles) > len(ROLES)
                or any(type(r) is not str or r not in ROLES for r in roles)
                or len(set(roles)) != len(roles)):
            fail('VALIDATION_FAILED', 'Invalid permission role declaration')
    if len(set(ids)) != len(ids) or any(not any(r in o['roles'] for o in operators) for r in ROLES):
        fail('VALIDATION_FAILED', 'Duplicate identities or missing required permission role')
    return deepcopy(value)


def role(m, actor, expected):
    identifier(actor)
    if not any(o['id'] == actor and expected in o['roles'] for o in m['operators']):
        fail('AUTHORIZATION_DENIED', 'Required declared local role is absent')


def request(value):
    intact()
    fields(value, ('schema_version', 'request_id', 'caller_id', 'task_id', 'operation',
                  'policy_sha256', 'qualification_id', 'certificate_sha256', 'claim',
                  'binding', 'inputs', 'source_state_sha256', 'action_receipts'))
    encoded(value)
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown permission request format')
    for k in ('request_id', 'caller_id', 'task_id', 'qualification_id'):
        identifier(value[k])
    if value['operation'] != OPERATION or value['policy_sha256'] != POLICY_HASH:
        fail('INCOMPATIBLE_CONFIGURATION', 'Operation/policy outside the bounded permission scope')
    c = claim(value['claim']); binding(value['binding'])
    if (c['kind'] != 'TRANSITION' or [c['source'], c['destination']] not in POLICY['transitions']
            or 'source_format' in value['binding']):
        fail('INCOMPATIBLE_CONFIGURATION', 'A profile certificate is not a replay-transition claim')
    digest_value(value['certificate_sha256']); digest_value(value['source_state_sha256'])
    if value['inputs'] != pairs('test')[:4]:
        fail('INCOMPATIBLE_CONFIGURATION', 'Input scope is exactly the four qualified transition fixtures')
    # Equality alone accepts Python True == 1; validate exact symbol types as well.
    if any(type(v) is not int for pair in value['inputs'] for v in pair):
        fail('VALIDATION_FAILED', 'Symbols must be integers, not booleans')
    actions = value['action_receipts']
    if type(actions) is not list or len(actions) > 32:
        fail('VALIDATION_FAILED', 'Too many action receipts')
    keys = []
    for item in actions:
        fields(item, ('key', 'receipt')); keys.append(identifier(item['key'])); digest_value(item['receipt'])
    if keys != sorted(set(keys)):
        fail('VALIDATION_FAILED', 'Action receipt keys must be sorted and unique')
    return deepcopy(value)


def grant(value, req, m):
    req = request(req); m = manifest(m)
    fields(value, ('schema_version', 'store_id', 'request_id', 'request_sha256', 'caller_id',
                  'issuer_id', 'issued_at', 'expires_at', 'policy_sha256', 'max_uses',
                  'authority', 'deployment_authorized', 'runtime_execution_permit', 'delegable'))
    encoded(value)
    expected = {'schema_version': 1, 'store_id': m['store_id'], 'request_id': req['request_id'],
                'request_sha256': fingerprint(req), 'caller_id': req['caller_id'],
                'policy_sha256': POLICY_HASH, 'max_uses': 1, 'authority': AUTHORITY,
                'deployment_authorized': False, 'runtime_execution_permit': False, 'delegable': False}
    for k, v in expected.items():
        if type(value[k]) is not type(v) or value[k] != v:
            fail('VALIDATION_FAILED', 'Grant binding/authority differs: ' + k)
    role(m, value['issuer_id'], 'ISSUER'); role(m, value['caller_id'], 'EXECUTOR')
    if value['issuer_id'] == value['caller_id']:
        fail('AUTHORIZATION_DENIED', 'An executor cannot issue its own grant')
    epoch(value['issued_at']); epoch(value['expires_at'])
    if not 1 <= value['expires_at'] - value['issued_at'] <= POLICY['max_ttl_seconds']:
        fail('VALIDATION_FAILED', 'Invalid grant lifetime')
    return deepcopy(value)


def completion(value, req, grant_sha256):
    """Data-only runtime receipt; store additionally obtains it from the owner."""
    fields(value, ('schema_version', 'request_id', 'request_sha256', 'grant_sha256',
                  'executor_id', 'result_sha256', 'status', 'deployment_authorized'))
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown completion receipt')
    if (value['request_id'] != req['request_id'] or value['request_sha256'] != fingerprint(req)
            or value['grant_sha256'] != grant_sha256 or value['executor_id'] != 'bounded_neural_replay_v1'
            or value['status'] != 'COMMITTED' or value['deployment_authorized'] is not False):
        fail('VALIDATION_FAILED', 'Runtime receipt cannot be substituted')
    digest_value(value['result_sha256']); encoded(value)
    return deepcopy(value)
