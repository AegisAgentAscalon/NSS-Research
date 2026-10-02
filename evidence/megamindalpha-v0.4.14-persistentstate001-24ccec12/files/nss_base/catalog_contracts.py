"""Exact reviewed fixture catalogue and deterministic stage-selection contracts.

Labels/cost units are operator declarations, NOT learned capability or hardware
measurements. Selection never grants execution, release, or neural qualification.
"""
from copy import deepcopy
from .generation_contracts import configuration, exact, generation
from .neural_contracts import encoded, fields, fingerprint, validate_pairs
from .qualification_contracts import digest_value, identifier, text
from .runtime import fail
from .task_records import validate_stage, validate_task_record
from .state_contracts import ACTIONS as STATE_ACTIONS, command as state_command, scope as state_scope

FORMAT = 'MegaMindAlpha.OverlayCatalogController001'
POLICY = 'exact_profile_declared_cost_v1'
OUTCOMES = ('SUCCESS', 'CAPABILITY_UNAVAILABLE', 'NEEDS_CLARIFICATION',
    'BUDGET_EXHAUSTED', 'INCOMPATIBLE_CONFIGURATION', 'CONSTRAINT_CONFLICT',
    'VALIDATION_FAILED', 'AUTHORIZATION_DENIED', 'INSUFFICIENT_EVIDENCE',
    'RECOVERY_REQUIRED', 'TRAINING_RESTRICTED')


def version(x):
    if type(x) is not int or x != 1:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported catalogue contract version')


def integer(x, low=0, high=10**9):
    if type(x) is not int or not low <= x <= high:
        fail('VALIDATION_FAILED', 'Expected bounded nonnegative integer')
    return x


def labels(x):
    if type(x) is not list or not 1 <= len(x) <= 32:
        fail('VALIDATION_FAILED', 'Expected a bounded nonempty capability list')
    for v in x: identifier(v)
    if x != sorted(set(x)):
        fail('VALIDATION_FAILED', 'Capability labels must be sorted and unique')
    return x


def descriptor(x, g):
    fields(x, ('schema_version', 'format', 'catalog_id', 'generation_sha256',
        'author_id', 'policy', 'claim_scope', 'profiles'))
    version(x['schema_version']); identifier(x['catalog_id']); identifier(x['author_id'])
    digest_value(x['generation_sha256']); g = generation(g); encoded(x)
    if (x['format'] != FORMAT or x['policy'] != POLICY or
            x['claim_scope'] != 'REVIEWED_ROUTING_FIXTURE_NOT_NEW_NEURAL_EVIDENCE'):
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown catalogue selection semantics')
    if x['generation_sha256'] != fingerprint(g):
        fail('INCOMPATIBLE_CONFIGURATION', 'Catalogue names a different exact generation')
    if type(x['profiles']) is not list:
        fail('VALIDATION_FAILED', 'Profiles must be an array')
    gp = {p['id']: p for p in g['profiles']}
    ids = []
    for p in x['profiles']:
        fields(p, ('id', 'ecid', 'capabilities', 'sealed_document_bytes',
            'load_units', 'step_units', 'max_pairs'))
        identifier(p['id']); digest_value(p['ecid']); labels(p['capabilities'])
        if p['id'] not in gp or p['ecid'] != gp[p['id']]['ecid']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Catalogue invents a profile or changes its ECID')
        integer(p['sealed_document_bytes'], 1); integer(p['load_units']); integer(p['step_units'], 1)
        integer(p['max_pairs'], 1, 256); ids.append(p['id'])
    if ids != sorted(gp):
        fail('INCOMPATIBLE_CONFIGURATION', 'Catalogue must describe every exact released profile once')
    return deepcopy(x)


def verify_document_sizes(d, g, artifacts):
    for p in d['profiles']:
        gp = next(a for a in g['profiles'] if a['id'] == p['id'])
        actual = sum(len(encoded(artifacts[k])) for k in ['core'] + gp['members'])
        if p['sealed_document_bytes'] != actual:
            fail('INCOMPATIBLE_CONFIGURATION', 'Declared serialized-artifact size differs from exact bytes')


def selection_request(x):
    fields(x, ('schema_version', 'catalog_sha256', 'expected_current', 'task_id',
        'stage', 'capabilities', 'pairs', 'budget'))
    version(x['schema_version']); digest_value(x['catalog_sha256']); configuration(x['expected_current'])
    identifier(x['task_id']); validate_stage(x['stage']); labels(x['capabilities']); validate_pairs(x['pairs'])
    if x['stage']['sealed']:
        fail('VALIDATION_FAILED', 'Selection requires an unsealed destination stage')
    fields(x['budget'], ('max_document_bytes', 'max_cost_units'))
    for v in x['budget'].values(): integer(v)
    encoded(x); return deepcopy(x)


def select_profile(d, g, req, source_profile=None):
    """One exact profile, no union. Costs are bounded declaration units, not joules."""
    descriptor(d, g); selection_request(req)
    if req['catalog_sha256'] != fingerprint(d) or req['expected_current']['generation_sha256'] != fingerprint(g):
        fail('INCOMPATIBLE_CONFIGURATION', 'Selection bindings differ from the reviewed catalogue')
    candidates = [p for p in d['profiles'] if set(req['capabilities']) <= set(p['capabilities'])]
    if req['stage']['mode'] in ('CONTROL', 'EVALUATION'):
        candidates = [p for p in candidates if p['id'] == 'CORE']
    if not candidates:
        fail('CAPABILITY_UNAVAILABLE', 'No ONE approved profile satisfies every requested label/mode')
    if source_profile is not None:
        edges = {(e['source'], e['destination']) for e in g['transitions']}
        candidates = [p for p in candidates if p['id'] == source_profile or (source_profile, p['id']) in edges]
        if not candidates:
            fail('INCOMPATIBLE_CONFIGURATION', 'No qualified directed transition to a suitable profile')
    options = []
    for p in candidates:
        cost = p['step_units'] * len(req['pairs']) + (0 if p['id'] == source_profile else p['load_units'])
        if (len(req['pairs']) <= p['max_pairs'] and
                p['sealed_document_bytes'] <= req['budget']['max_document_bytes'] and
                cost <= req['budget']['max_cost_units']):
            options.append((cost, p))
    if not options:
        fail('BUDGET_EXHAUSTED', 'No suitable qualified profile fits the explicit declared budget')
    cost = min(c for c, _ in options); best = [p for c, p in options if c == cost]
    stay = next((p for p in best if p['id'] == source_profile), None)
    if stay is None and len(best) != 1:
        fail('NEEDS_CLARIFICATION', 'Several equally priced approved profiles remain; no arbitrary choice')
    p = stay or best[0]
    return {'schema_version': 1, 'profile': p['id'], 'ecid': p['ecid'],
        'catalog_sha256': fingerprint(d), 'request_sha256': fingerprint(req),
        'configuration': deepcopy(req['expected_current']), 'declared_cost_units': cost,
        'sealed_document_bytes': p['sealed_document_bytes'],
        'source_profile': source_profile, 'state_policy': 'REBUILD_FROM_PORTABLE_INPUTS',
        'learned_routing': False, 'runtime_execution_permit': False}


def command(x):
    if type(x) is not dict or type(x.get('action')) is not str:
        fail('VALIDATION_FAILED', 'Typed catalogue-stage command required')
    if x['action'] in STATE_ACTIONS: return state_command(x)
    if type(x.get('schema_version')) is not int or x['schema_version'] not in (1, 2):
        fail('INCOMPATIBLE_CONFIGURATION', 'Unsupported task command version')
    common = ('schema_version', 'operation_id', 'caller_id', 'action')
    if x['schema_version'] == 2:
        common += ('scope',)
        state_scope(x.get('scope'))
        if x['action'] == 'START': fail('VALIDATION_FAILED', 'Start v1 then explicitly bind scope')
    kinds = {
        'START': ('request', 'ticket_id', 'record'),
        'MOVE': ('request', 'ticket_id', 'source_ticket', 'expected_record_sha256'),
        'FINISH': ('source_ticket', 'expected_record_sha256', 'results', 'receipts'),
        'CLOSE': ('source_ticket', 'expected_record_sha256'),
        'CANCEL': ('source_ticket', 'expected_record_sha256', 'receipts', 'reason'),
    }
    if x['action'] not in kinds: fail('VALIDATION_FAILED', 'Unsupported catalogue-stage action')
    fields(x, common + kinds[x['action']])
    identifier(x['operation_id']); identifier(x['caller_id']); encoded(x)
    if x['action'] in ('START', 'MOVE'):
        selection_request(x['request']); identifier(x['ticket_id'])
    if x['action'] == 'START':
        validate_task_record(x['record'])
        if x['record']['schema_version'] != 1:
            fail('VALIDATION_FAILED', 'Fresh admission uses v1; scope needs reviewed BIND_STATE')
        if x['record']['revision'] != 0 or x['record']['stage']['sealed']:
            fail('VALIDATION_FAILED', 'Fresh task requires revision-zero unsealed input')
        exact(x['record']['stage'], x['request']['stage'])
        if x['record']['task_id'] != x['request']['task_id']:
            fail('CONSTRAINT_CONFLICT', 'Request and initial record belong to different tasks')
    else:
        if type(x['source_ticket']) is not dict: fail('VALIDATION_FAILED', 'Exact source ticket required')
        digest_value(x['expected_record_sha256'])
    if 'results' in x and (type(x['results']) is not list or len(x['results']) > 128):
        fail('VALIDATION_FAILED', 'Results must be a bounded array')
    if 'receipts' in x and (type(x['receipts']) is not list or len(x['receipts']) > 128):
        fail('VALIDATION_FAILED', 'Receipts must be a bounded array')
    if 'reason' in x: text(x['reason'])
    return deepcopy(x)


def task_identity(ticket, record, pairs):
    return fingerprint({'contract': FORMAT, 'ticket': ticket, 'record_sha256': fingerprint(record),
                        'pairs_sha256': fingerprint(pairs)})


def require_state_identity(produced_identity, current_view):
    digest_value(produced_identity)
    if type(current_view) is not dict or not {'ticket', 'record', 'pairs', 'task_state_identity'} <= current_view.keys():
        fail('VALIDATION_FAILED', 'Expected a current task-stage view')
    validate_task_record(current_view['record']); validate_pairs(current_view['pairs'])
    expected = task_identity(current_view['ticket'], current_view['record'], current_view['pairs'])
    if current_view.get('task_state_identity') != expected or produced_identity != expected:
        fail('INCOMPATIBLE_CONFIGURATION', 'Stale configuration/stage/revision cache; rebuild from portable inputs')
    return True
