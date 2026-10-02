"""TriCoreFoundation001: strict current-role data; no serving or training authority.

The first implementation admits TEST_ADAPTERS_ONLY configurations. Real model
qualification and independent Forge/Runtime integration are deliberately unavailable.
Descriptors are data, never dynamic Python imports or permission credentials.
"""
from copy import deepcopy
from .neural_contracts import encoded, fields, fingerprint
from .qualification_contracts import identifier, digest_value, text
from .generation_contracts import role
from .runtime import fail
from .state_contracts import scope

FORMAT = 'NSS.TriCoreFoundation001'
ROLES = ('PRIMARY', 'SECONDARY', 'TERTIARY', 'VALIDATOR')
PHASES = ('PRIMARY_ONLY', 'TASK', 'LEARN', 'REFLECT', 'VERIFY')
AUXILIARY = {'PRIMARY_ONLY': None, 'TASK': 'SECONDARY', 'LEARN': 'SECONDARY',
             'REFLECT': 'TERTIARY', 'VERIFY': 'VALIDATOR'}
CAPABILITIES = ('structured', 'text', 'tokens', 'temporal_state', 'native_refinement',
                'candidate_learning', 'latent_reference')
POLICY = {'schema_version': 1, 'execution_scope': 'TEST_ADAPTERS_ONLY',
          'secondary_tertiary_exclusive': True, 'primary_calls_per_tick': 2,
          'validator_authority': 'ADVICE_ONLY', 'restore': 'EXACT_CONFIGURATION_AND_SCOPE',
          'runtime_execution_permit': False, 'training_authorized': False,
          'production_deployment_authorized': False}
POLICY_SHA256 = fingerprint(POLICY)
MAX_STATE_BYTES = 65536
MAX_MESSAGE_BYTES = 65536


def integer(value, low=0, high=1000000):
    if type(value) is not int or not low <= value <= high:
        fail('VALIDATION_FAILED', 'Integer outside declared bounds')
    return value


def choice(value, allowed, label):
    if type(value) is not str or value not in allowed:
        fail('VALIDATION_FAILED', 'Unsupported ' + label)
    return value


def component(value, expected_role, primary_generation):
    fields(value, ('role', 'component_id', 'revision', 'implementation', 'weights_sha256',
                   'primary_generation', 'interface_version', 'state_schema', 'codec_version',
                   'tokenizer_abi', 'serving_frozen', 'capabilities', 'evidence_class'))
    if value['role'] != expected_role or value['primary_generation'] != primary_generation:
        fail('INCOMPATIBLE_CONFIGURATION', 'Wrong component role or Primary generation')
    for key in ('component_id', 'revision', 'implementation', 'interface_version', 'state_schema', 'codec_version'):
        identifier(value[key])
    digest_value(value['weights_sha256'])
    if value['tokenizer_abi'] is not None: identifier(value['tokenizer_abi'])
    # Even adaptable roles serve fixed revisions; updates belong to candidate jobs.
    if value['serving_frozen'] is not True:
        fail('INCOMPATIBLE_CONFIGURATION', 'This serving revision must remain frozen')
    caps = value['capabilities']
    if type(caps) is not list or not caps or any(type(c) is not str for c in caps) or len(caps) != len(set(caps)):
        fail('VALIDATION_FAILED', 'Expected unique supported capabilities')
    for cap in caps: choice(cap, CAPABILITIES, 'capability')
    if 'structured' not in caps:
        fail('NOT_SUPPORTED', 'The initial inspectable interface requires structured data')
    if value['evidence_class'] != 'DETERMINISTIC_TEST_ADAPTER_NOT_NEURAL':
        fail('NOT_SUPPORTED', 'Real-model adapters require independent qualification and Runtime integration')
    return deepcopy(value)


def configuration(value):
    fields(value, ('schema_version', 'generation_id', 'primary_generation', 'producer_id',
                   'execution_scope', 'components', 'context_abi', 'exchange_abi', 'limits'))
    if type(value['schema_version']) is not int or value['schema_version'] != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown current-role configuration version')
    for key in ('generation_id', 'primary_generation', 'producer_id', 'context_abi', 'exchange_abi'):
        identifier(value[key])
    if value['execution_scope'] != POLICY['execution_scope']:
        fail('NOT_SUPPORTED', 'This release has no real-model deployment authority')
    fields(value['components'], ROLES)
    if value['components']['PRIMARY'] is None:
        fail('INCOMPATIBLE_CONFIGURATION', 'A usable Primary-only path is required')
    ids = []
    for r, c in value['components'].items():
        if c is not None:
            component(c, r, value['primary_generation']); ids.append(c['component_id'])
    if len(ids) != len(set(ids)):
        fail('INCOMPATIBLE_CONFIGURATION', 'Roles are distinct components, not relabelled shared auxiliaries')
    limits = value['limits']
    fields(limits, ('max_ticks', 'max_state_bytes', 'max_message_bytes', 'callback_budget_ms'))
    integer(limits['max_ticks'], 1, 1000)
    integer(limits['max_state_bytes'], 128, MAX_STATE_BYTES)
    integer(limits['max_message_bytes'], 128, MAX_MESSAGE_BYTES)
    integer(limits['callback_budget_ms'], 1, 60000)
    encoded(value)
    return deepcopy(value)


def store_manifest(value):
    fields(value, ('schema_version', 'format', 'store_id', 'policy_sha256', 'operators', 'initial_configuration'))
    if type(value['schema_version']) is not int or value['schema_version'] != 2 or value['format'] != FORMAT:
        fail('INCOMPATIBLE_CONFIGURATION', 'Not a current-role Generations store')
    identifier(value['store_id'])
    if value['policy_sha256'] != POLICY_SHA256:
        fail('INCOMPATIBLE_CONFIGURATION', 'Current-role policy differs')
    ops = value['operators']
    if type(ops) is not list or not 3 <= len(ops) <= 32:
        fail('VALIDATION_FAILED', 'Declare bounded independent local operators')
    names = []
    for op in ops:
        fields(op, ('id', 'roles')); identifier(op['id']); names.append(op['id'])
        rs = op['roles']
        if type(rs) is not list or not rs or any(type(r) is not str for r in rs) or len(rs) != len(set(rs)):
            fail('VALIDATION_FAILED', 'Invalid operator roles')
        for r in rs: choice(r, ('PRODUCER', 'REVIEWER', 'ISSUER', 'OPERATOR'), 'operator role')
    if len(names) != len(set(names)):
        fail('VALIDATION_FAILED', 'Repeated local operator')
    for r in ('PRODUCER', 'REVIEWER', 'ISSUER', 'OPERATOR'):
        if not any(r in op['roles'] for op in ops):
            fail('VALIDATION_FAILED', 'Missing independent lifecycle role')
    c = configuration(value['initial_configuration']); role(value, c['producer_id'], 'PRODUCER')
    if {c['component_id'] for c in c['components'].values() if c} & set(names):
        fail('AUTHORIZATION_DENIED', 'Neural component identities are not local authorities')
    return deepcopy(value)


def task_view(s, m, task_id, caller_id, owner_scope, *, live=True):
    identifier(task_id); role(m, caller_id, 'OPERATOR'); scope(owner_scope)
    if task_id not in s['tasks']:
        fail('INSUFFICIENT_EVIDENCE', 'Unknown current-role task')
    t = s['tasks'][task_id]
    if t['caller_id'] != caller_id or t['scope'] != owner_scope:
        fail('AUTHORIZATION_DENIED', 'Wrong caller or agent/project/session scope')
    if live:
        if t['closed']: fail('CONSTRAINT_CONFLICT', 'Task is closed')
        if t['configuration_sha256'] != s['current']['generation_sha256']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Task needs its exact original configuration or explicit migration')
    return t


def state_envelope(payload, *, role_name, config, task, event_id, cutoff, revision, lane='temporal'):
    choice(lane, ('temporal', 'candidate'), 'state lane')
    choice(role_name, ROLES, 'state owner'); identifier(event_id)
    comp = config['components'][role_name]
    if comp is None: fail('NOT_SUPPORTED', 'Missing state owner')
    if lane == 'candidate' and role_name != 'SECONDARY':
        fail('NOT_SUPPORTED', 'Initial candidate-job lane belongs to Secondary')
    raw = encoded(payload)
    if len(raw) > config['limits']['max_state_bytes']:
        fail('BUDGET_EXHAUSTED', 'Component state exceeds explicit byte budget')
    return {'schema_version': 1, 'owner_role': role_name, 'owner_component_revision': comp['revision'],
            'configuration_sha256': fingerprint(config), 'primary_generation': config['primary_generation'],
            'task_id': task['record']['task_id'], 'owner_scope': deepcopy(task['scope']),
            'state_schema': comp['state_schema'], 'codec_version': comp['codec_version'],
            'lane': lane, 'lifetime': 'TASK_EXACT_REVISION', 'state_revision': integer(revision, 1),
            'experience_cutoff': integer(cutoff), 'parent_event_id': event_id,
            'supported_restore_policy': POLICY['restore'], 'record_kind': 'derived',
            'payload': deepcopy(payload), 'payload_sha256': fingerprint(payload), 'payload_bytes': len(raw)}


def validate_state_envelope(value, *, role_name, config, task, lane='temporal'):
    fields(value, ('schema_version', 'owner_role', 'owner_component_revision', 'configuration_sha256',
                   'primary_generation', 'task_id', 'owner_scope', 'state_schema', 'codec_version', 'lane',
                   'lifetime', 'state_revision', 'experience_cutoff', 'parent_event_id',
                   'supported_restore_policy', 'record_kind', 'payload', 'payload_sha256', 'payload_bytes'))
    expected = state_envelope(value['payload'], role_name=role_name, config=config, task=task,
                              event_id=value['parent_event_id'], cutoff=value['experience_cutoff'],
                              revision=value['state_revision'], lane=lane)
    if encoded(value) != encoded(expected):
        fail('INCOMPATIBLE_CONFIGURATION', 'State scope, codec, generation or integrity differs')
    return deepcopy(value)


def exchange(payload, *, config, task, sender, receiver, event_id, message_id,
             cutoff, state_revision, record_kind, source_references=(), payload_format='structured'):
    choice(sender, ROLES, 'sender'); choice(receiver, ROLES, 'receiver')
    choice(record_kind, ('derived', 'hypothetical', 'proposed_action'), 'generated record kind')
    choice(payload_format, ('text', 'structured', 'tokens', 'latent_reference'), 'payload format')
    a, b = config['components'][sender], config['components'][receiver]
    if a is None or b is None: fail('NOT_SUPPORTED', 'Missing exchange endpoint')
    if payload_format not in a['capabilities'] or payload_format not in b['capabilities']:
        fail('NOT_SUPPORTED', 'Both endpoints must support the requested representation')
    if payload_format == 'tokens' and (a['tokenizer_abi'] is None or a['tokenizer_abi'] != b['tokenizer_abi']):
        fail('INCOMPATIBLE_CONFIGURATION', 'Token IDs require identical tokenizer/input ABI')
    if payload_format == 'latent_reference':
        fail('NOT_SUPPORTED', 'No trained latent alignment is qualified in this release')
    if payload_format == 'text' and type(payload) is not str:
        fail('VALIDATION_FAILED', 'Text payload required')
    if payload_format == 'tokens':
        if type(payload) is not list or len(payload) > 4096: fail('VALIDATION_FAILED', 'Bounded token array required')
        for item in payload: integer(item, 0, 2**31-1)
    if payload_format == 'structured' and type(payload) is not dict:
        fail('VALIDATION_FAILED', 'Structured payload required')
    if sender == 'TERTIARY' and record_kind != 'hypothetical':
        fail('AUTHORIZATION_DENIED', 'Initial Tertiary outputs remain hypothetical; checking is a separate event')
    if type(source_references) not in (list, tuple) or len(source_references) > 256:
        fail('VALIDATION_FAILED', 'Bounded exact-source reference list required')
    for ref in source_references: digest_value(ref)
    out = {'schema_version': 1, 'message_id': message_id, 'parent_event_id': event_id,
           'task_id': task['record']['task_id'], 'owner_scope': deepcopy(task['scope']),
           'sender_role': sender, 'receiver_role': receiver,
           'sender_component_revision': a['revision'], 'receiver_interface_version': b['interface_version'],
           'configuration_sha256': fingerprint(config), 'primary_generation': config['primary_generation'],
           'representation_schema': config['exchange_abi'], 'codec_version': a['codec_version'],
           'experience_cutoff': integer(cutoff), 'state_revision': integer(state_revision),
           'supported_restore_policy': POLICY['restore'], 'record_kind': record_kind,
           'payload_format': payload_format, 'payload': deepcopy(payload),
           'source_references': list(source_references), 'assumptions': [], 'uncertainty': None,
           'permission_scope': [], 'authority': 'DATA_NOT_PERMISSION_OR_RELEASE'}
    identifier(message_id); identifier(event_id)
    if len(encoded(out)) > config['limits']['max_message_bytes']:
        fail('BUDGET_EXHAUSTED', 'Exchange exceeds explicit byte budget')
    return out


def validate_exchange(value, *, config, task):
    if type(value) is not dict: fail('VALIDATION_FAILED', 'Exchange must be a document')
    required = ('payload', 'sender_role', 'receiver_role', 'parent_event_id', 'message_id',
                'experience_cutoff', 'state_revision', 'record_kind', 'source_references', 'payload_format')
    if not set(required) <= value.keys(): fail('VALIDATION_FAILED', 'Incomplete exchange')
    expected = exchange(value['payload'], config=config, task=task, sender=value['sender_role'],
                        receiver=value['receiver_role'], event_id=value['parent_event_id'],
                        message_id=value['message_id'], cutoff=value['experience_cutoff'],
                        state_revision=value['state_revision'], record_kind=value['record_kind'],
                        source_references=value['source_references'], payload_format=value['payload_format'])
    if encoded(value) != encoded(expected):
        fail('INCOMPATIBLE_CONFIGURATION', 'Exchange binding or authority differs')
    return deepcopy(value)
