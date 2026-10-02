"""Pure current-role reduction inside the existing Generations journal owner.

This is a new explicit store format, not an implicit upgrade of a legacy database.
No model callback, file read, external effect or permission renewal occurs on replay.
"""
from copy import deepcopy
from .foundation_contracts import (FORMAT, ROLES, PHASES, AUXILIARY, configuration,
    task_view, integer, choice, state_envelope, validate_state_envelope, validate_exchange)
from .generation_contracts import role, exact
from .neural_contracts import fields, fingerprint, encoded
from .qualification_contracts import identifier, digest_value, text
from .state_contracts import command
from .state_updates import apply_delta
from .task_records import validate_task_record
from .runtime import fail


def idle(s):
    if s['busy'] is not None:
        fail('RECOVERY_REQUIRED', 'A reserved tick remains; finish it or explicitly recover after worker exit')


def command_binding(c, m, s):
    command(c)
    if c.get('schema_version') != 3 or c['store_id'] != m['store_id']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Wrong current-role state proposal owner')
    if c['expected_configuration_sha256'] != s['current']['generation_sha256']:
        fail('INCOMPATIBLE_CONFIGURATION', 'State proposal targets another configuration')


def _complete(s, m, b):
    fields(b, ('operation_id', 'states', 'candidate_states', 'messages', 'receipts', 'output'))
    job = s['busy']
    if job is None or job['operation_id'] != b['operation_id']:
        fail('CONSTRAINT_CONFLICT', 'No matching reserved tick')
    t = task_view(s, m, job['task_id'], job['caller_id'], job['scope'])
    cfg = s['configurations'][t['configuration_sha256']]
    aux = AUXILIARY[job['phase']]
    expected_roles = ['PRIMARY'] + ([aux] if aux is not None else []) + ['PRIMARY']
    rs = b['receipts']
    if type(rs) is not list or [r.get('role') for r in rs] != expected_roles:
        fail('VALIDATION_FAILED', 'Each tick needs actual pre/post Primary calls and its phase-specific auxiliary')
    for i, r in enumerate(rs):
        fields(r, ('role', 'call_index', 'operation', 'input_sha256', 'result_sha256',
                   'weights_before', 'weights_after', 'elapsed_us'))
        c = cfg['components'][r['role']]
        if r['call_index'] != i or c is None:
            fail('VALIDATION_FAILED', 'Bad call order or component')
        expected_op = 'candidate_step' if job['phase'] == 'LEARN' and r['role'] == 'SECONDARY' else 'infer'
        if r['operation'] != expected_op: fail('VALIDATION_FAILED', 'Wrong phase operation')
        for key in ('input_sha256', 'result_sha256'): digest_value(r[key])
        if r['weights_before'] != c['weights_sha256'] or r['weights_after'] != c['weights_sha256']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Serving parameters changed or mismatched')
        integer(r['elapsed_us'], 0, 10**12)
        if r['elapsed_us'] > cfg['limits']['callback_budget_ms'] * 1000:
            fail('BUDGET_EXHAUSTED', 'Cooperative callback exceeded its measured duration limit')
    for lane, key in (('temporal', 'states'), ('candidate', 'candidate_states')):
        after = b[key]; before = t[key]
        touched = {'PRIMARY'} if lane == 'temporal' else set()
        if aux is not None:
            (touched if (lane == 'candidate') == (job['phase'] == 'LEARN') else set()).add(aux)
        expected_keys = set(before) | touched
        if type(after) is not dict or set(after) != expected_keys:
            fail('VALIDATION_FAILED', 'Missing or extra component state')
        for r, env in after.items():
            validate_state_envelope(env, role_name=r, config=cfg, task=t, lane=lane)
            if r not in touched:
                exact(env, before[r]); continue
            inc = 2 if r == 'PRIMARY' else 1
            rev = before.get(r, {}).get('state_revision', 0) + inc
            if env['state_revision'] != rev or env['parent_event_id'] != job['operation_id'] or env['experience_cutoff'] != job['experience_cutoff']:
                fail('INCOMPATIBLE_CONFIGURATION', 'State update has stale event/revision/cutoff')
    pairs = [('PRIMARY', aux), (aux, 'PRIMARY')] if aux is not None else []
    if type(b['messages']) is not list or [(v.get('sender_role'), v.get('receiver_role')) for v in b['messages']] != pairs:
        fail('VALIDATION_FAILED', 'Wrong communication path')
    for message in b['messages']:
        validate_exchange(message, config=cfg, task=t)
        if message['parent_event_id'] != job['operation_id'] or message['experience_cutoff'] != job['experience_cutoff']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Message event/cutoff differs')
        if not set(message['source_references']) <= set(job['source_references']):
            fail('INSUFFICIENT_EVIDENCE', 'Generated message invented a source reference')
    fields(b['output'], ('record_kind', 'payload', 'source_references'))
    if b['output']['record_kind'] != 'derived' or not set(b['output']['source_references']) <= set(job['source_references']):
        fail('AUTHORIZATION_DENIED', 'Final generated output is derived data, not new observed evidence')
    if len(encoded(b['output'])) > cfg['limits']['max_message_bytes']:
        fail('BUDGET_EXHAUSTED', 'Final output exceeds byte budget')
    t['states'] = deepcopy(b['states']); t['candidate_states'] = deepcopy(b['candidate_states'])
    t['ticks'] += 1; t['experience_cutoff'] = job['experience_cutoff']; t['phase'] = job['phase']
    result = {**deepcopy(job), **deepcopy(b), 'status': 'COMMITTED',
              'runtime_execution_permit': False, 'training_authorized': False}
    s['operations'][job['operation_id']] = result; s['busy'] = None


def reduce_foundation_events(m, events):
    initial = configuration(m['initial_configuration']); h = fingerprint(initial)
    s = {'format': FORMAT, 'configurations': {h: initial},
         'current': {'epoch': 1, 'generation_sha256': h}, 'tasks': {}, 'task_heads': {},
         'operations': {}, 'state_operations': {}, 'busy': None, 'switches': []}
    for event in events:
        k, b, at = event['kind'], event['body'], event['at']
        if k == 'F_ADMIT':
            fields(b, ('record', 'command')); c = b['command']; command_binding(c, m, s); idle(s)
            r = validate_task_record(b['record']); role(m, c['caller_id'], 'OPERATOR')
            if c['action'] != 'BIND_STATE' or r['schema_version'] != 1 or r['revision'] != 0 or r['receipts'] or r['stage']['sealed']:
                fail('NOT_SUPPORTED', 'Admit a new unsealed exact task; importing legacy live receipts requires a migration')
            if r['task_id'] != c['task_id'] or r['task_id'] in s['tasks']:
                fail('CONSTRAINT_CONFLICT', 'Task identity differs or was already admitted')
            r = apply_delta(r, c, m, at, configuration_sha256=s['current']['generation_sha256'])
            s['tasks'][r['task_id']] = {'record': r, 'scope': deepcopy(c['scope']), 'caller_id': c['caller_id'],
                'configuration_sha256': s['current']['generation_sha256'], 'closed': False,
                'states': {}, 'candidate_states': {}, 'ticks': 0, 'experience_cutoff': 0,
                'phase': 'PRIMARY_ONLY', 'history': [deepcopy(b['record']), deepcopy(r)]}
            s['task_heads'][r['task_id']] = fingerprint(r)
            if c['operation_id'] in s['state_operations']: fail('CONSTRAINT_CONFLICT', 'Repeated state event')
            s['state_operations'][c['operation_id']] = {'command': c, 'record_sha256': fingerprint(r)}
        elif k == 'F_UPDATE':
            fields(b, ('command',)); c = b['command']; command_binding(c, m, s); idle(s)
            t = task_view(s, m, c['task_id'], c['caller_id'], c['scope'])
            if c['action'] != 'UPDATE_STATE' or c['operation_id'] in s['state_operations']:
                fail('CONSTRAINT_CONFLICT', 'Repeated or wrong state operation')
            r = apply_delta(t['record'], c, m, at, configuration_sha256=t['configuration_sha256'])
            t['record'] = r; t['history'].append(deepcopy(r)); s['task_heads'][c['task_id']] = fingerprint(r)
            s['state_operations'][c['operation_id']] = {'command': c, 'record_sha256': fingerprint(r)}
        elif k == 'F_BEGIN':
            fields(b, ('operation_id', 'task_id', 'caller_id', 'scope', 'phase', 'experience_cutoff',
                       'expected_tick', 'record_sha256', 'context_sha256', 'source_references', 'input_sha256'))
            idle(s); identifier(b['operation_id']); choice(b['phase'], PHASES, 'phase')
            t = task_view(s, m, b['task_id'], b['caller_id'], b['scope'])
            cfg = s['configurations'][t['configuration_sha256']]; aux = AUXILIARY[b['phase']]
            if b['operation_id'] in s['operations']: fail('CONSTRAINT_CONFLICT', 'Tick IDs cannot be recycled')
            if t['ticks'] != integer(b['expected_tick']) or b['record_sha256'] != fingerprint(t['record']):
                fail('CONSTRAINT_CONFLICT', 'Stale task/tick revision')
            if t['ticks'] >= cfg['limits']['max_ticks']: fail('BUDGET_EXHAUSTED', 'Task tick budget exhausted')
            if integer(b['experience_cutoff']) < t['experience_cutoff']:
                fail('INCOMPATIBLE_CONFIGURATION', 'Experience cutoff moved backwards')
            for key in ('record_sha256', 'context_sha256', 'input_sha256'): digest_value(b[key])
            if type(b['source_references']) is not list or len(b['source_references']) > 256:
                fail('VALIDATION_FAILED', 'Bounded source digest list required')
            for ref in b['source_references']: digest_value(ref)
            if aux is not None and cfg['components'][aux] is None:
                fail('NOT_SUPPORTED', 'Requested auxiliary is unavailable; choose Primary-only explicitly')
            if b['phase'] == 'LEARN' and 'candidate_learning' not in cfg['components']['SECONDARY']['capabilities']:
                fail('NOT_SUPPORTED', 'No candidate-learning interface; inference is not training')
            s['busy'] = deepcopy(b)
        elif k == 'F_COMPLETE':
            _complete(s, m, b)
        elif k == 'F_INTERRUPT':
            fields(b, ('operation_id', 'caller_id', 'reason')); role(m, b['caller_id'], 'OPERATOR'); text(b['reason'])
            job = s['busy']
            if job is None or job['operation_id'] != b['operation_id'] or job['caller_id'] != b['caller_id']:
                fail('AUTHORIZATION_DENIED', 'Only the reserved worker caller may recover this tick')
            s['operations'][job['operation_id']] = {**deepcopy(job), 'status': 'INTERRUPTED',
                'reason': b['reason'], 'completed_computation_claimed': False, 'external_effects_replayed': False}
            s['busy'] = None
        elif k == 'F_CLOSE':
            fields(b, ('task_id', 'caller_id', 'scope')); idle(s)
            task_view(s, m, b['task_id'], b['caller_id'], b['scope'])['closed'] = True
        elif k == 'F_SWITCH_TEST_CONFIGURATION':
            fields(b, ('configuration', 'expected_current', 'caller_id', 'reviewer_id', 'issuer_id',
                       'test_evidence_sha256', 'qualification_scope'))
            idle(s)
            if any(not t['closed'] for t in s['tasks'].values()):
                fail('CONSTRAINT_CONFLICT', 'Close all managed tasks before a whole-configuration boundary')
            c = configuration(b['configuration']); digest_value(b['test_evidence_sha256'])
            for key, r in (('caller_id', 'OPERATOR'), ('reviewer_id', 'REVIEWER'), ('issuer_id', 'ISSUER')):
                role(m, b[key], r)
            role(m, c['producer_id'], 'PRODUCER')
            if b['qualification_scope'] != 'STRUCTURAL_TEST_ATTESTATION_NOT_MODEL_QUALIFICATION':
                fail('NOT_SUPPORTED', 'No production or neural qualification is provided by this path')
            if b['reviewer_id'] in (c['producer_id'], b['caller_id']) or b['issuer_id'] in (c['producer_id'], b['caller_id']):
                fail('AUTHORIZATION_DENIED', 'Producer/executor cannot review or issue its own configuration')
            exact(b['expected_current'], s['current'])
            for old in s['configurations'].values():
                if old['generation_id'] == c['generation_id'] and old != c:
                    fail('CONSTRAINT_CONFLICT', 'Generation names cannot be rebound')
                if old['primary_generation'] == c['primary_generation'] and old['components']['PRIMARY'] != c['components']['PRIMARY']:
                    fail('INCOMPATIBLE_CONFIGURATION', 'Primary weights/ABI are immutable within their generation')
            if {v['component_id'] for v in c['components'].values() if v} & {o['id'] for o in m['operators']}:
                fail('AUTHORIZATION_DENIED', 'Components may not acquire authority identities')
            h = fingerprint(c); s['configurations'][h] = c
            s['current'] = {'epoch': s['current']['epoch'] + 1, 'generation_sha256': h}
            s['switches'].append(deepcopy(b))
        else:
            fail('INCOMPATIBLE_CONFIGURATION', 'Legacy/unknown event cannot enter a current-role store')
    return s
