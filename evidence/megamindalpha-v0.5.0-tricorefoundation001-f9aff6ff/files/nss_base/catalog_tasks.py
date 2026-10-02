"""Pure task-stage transitions in the existing generation journal.

No second pointer/database, numerical inference, or action execution. Current-use
source/ledger checks are performed at the owner's public transaction boundary.
"""
from copy import deepcopy
from .catalog_contracts import (command, descriptor, select_profile)
from .generation_contracts import exact, role
from .generation_views import qualified, quiescent, ticket_for
from .neural_contracts import fields, fingerprint
from .runtime import fail
from .task_records import validate_record_handoff, validate_task_record, finish_record
from .state_contracts import ACTIONS as STATE_ACTIONS, check_scope, revision_check
from .state_updates import apply_delta


def catalog_entry(s, key):
    if type(key) is not str or key not in s['catalogs']:
        fail('INSUFFICIENT_EVIDENCE', 'Unknown reviewed catalogue descriptor')
    return s['catalogs'][key]


def require_current(s, req):
    if req['expected_current'] != s['current']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Selection is stale; inspect current generation again')
    d = catalog_entry(s, req['catalog_sha256'])['descriptor']
    g = qualified(s, s['current']['generation_sha256'])['manifest']
    descriptor(d, g)
    return d, g


def source_task(s, ticket, caller, record_hash=None, scope=None):
    if type(ticket) is not dict or type(ticket.get('ticket_id')) is not str:
        fail('VALIDATION_FAILED', 'Exact managed-task ticket required')
    saved = s['tickets'].get(ticket['ticket_id'])
    if saved is None or 'work' not in saved:
        fail('INSUFFICIENT_EVIDENCE', 'Ticket does not own a portable task record')
    exact(ticket, saved['ticket'])
    if ticket['caller_id'] != caller: fail('AUTHORIZATION_DENIED', 'Wrong task holder')
    w = saved['work']; check_scope(w['record'], scope)
    if saved['closed'] or s['task_heads'].get(w['record']['task_id']) != ticket['ticket_id']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Task stage is closed or no longer its task head')
    if ticket['configuration'] != s['current']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Task ticket belongs to a different generation epoch')
    if record_hash is not None and record_hash != fingerprint(w['record']):
        fail('INCOMPATIBLE_CONFIGURATION', 'Task record changed; exact revision required')
    return saved


def followup_request(previous, req):
    """One source-compatibility rule for selection proposals and committed moves."""
    w = previous['work']; old = w['record']
    if not old['stage']['sealed']:
        fail('CONSTRAINT_CONFLICT', 'Finish current stage before selecting its successor')
    if req['task_id'] != old['task_id']:
        fail('CONSTRAINT_CONFLICT', 'Cross-task handoff rejected')
    if req['catalog_sha256'] != w['request']['catalog_sha256']:
        fail('INCOMPATIBLE_CONFIGURATION', 'A task pins one reviewed descriptor for its lifetime')
    exact(req['pairs'], w['request']['pairs'])
    if req['stage']['id'] in w['stage_ids']:
        fail('CONSTRAINT_CONFLICT', 'Task stage identities cannot repeat')


def receipt(c, ticket, record, phase):
    return {'schema_version': 1, 'operation_id': c['operation_id'], 'action': c['action'],
        'command_sha256': fingerprint(c), 'ticket': deepcopy(ticket), 'record_sha256': fingerprint(record),
        'phase': phase, 'status': 'SUCCESS', 'runtime_execution_permit': False,
        'production_deployment_authorized': False}


def reduce_catalog_event(m, s, event):
    """Replay semantics are verified independent of API planning on every read."""
    b = event['body']
    if event['kind'] == 'CATALOG_REGISTER':
        fields(b, ('descriptor', 'reviewer_id'))
        d = b['descriptor']
        if type(d) is not dict or 'generation_sha256' not in d:
            fail('VALIDATION_FAILED', 'Missing descriptor binding')
        g = qualified(s, d['generation_sha256'])['manifest']; d = descriptor(d, g)
        role(m, d['author_id'], 'PRODUCER'); role(m, b['reviewer_id'], 'REVIEWER')
        if d['author_id'] == b['reviewer_id']:
            fail('AUTHORIZATION_DENIED', 'Descriptor author cannot perform its own review')
        if any(v['descriptor']['catalog_id'] == d['catalog_id'] for v in s['catalogs'].values()):
            fail('CONSTRAINT_CONFLICT', 'Catalogue ID already binds an immutable descriptor')
        s['catalogs'][fingerprint(d)] = deepcopy(b)
        return
    fields(b, ('command', 'ticket', 'record', 'selection', 'inputs', 'receipt'))
    c = command(b['command']); role(m, c['caller_id'], 'OPERATOR')
    if c['operation_id'] in s['task_operations']:
        fail('CONSTRAINT_CONFLICT', 'Operation ID cannot be reused')
    action = c['action']; previous = None
    if action != 'START':
        previous = source_task(s, c['source_ticket'], c['caller_id'],
            None if action in STATE_ACTIONS else c['expected_record_sha256'],
            None if action == 'BIND_STATE' else c.get('scope'))
        if action in STATE_ACTIONS: revision_check(previous['work']['record'], c, previous['ticket']['profile_ecid'])
    if action in ('START', 'MOVE'):
        req = c['request']; d, g = require_current(s, req)
        profile = previous['ticket']['profile'] if previous else None
        exact(b['selection'], select_profile(d, g, req, profile))
        if c['ticket_id'] in s['tickets']: fail('CONSTRAINT_CONFLICT', 'Ticket IDs are never recycled')
        if action == 'START':
            quiescent(s)
            if req['task_id'] in s['task_heads']:
                fail('CONSTRAINT_CONFLICT', 'Task IDs cannot be restarted to bypass qualified transitions')
            if c['record']['stage']['required_facts']:
                # Initial mandatory content must be verified/furnished upstream;
                # this v1 interface starts with a self-contained portable record.
                for r in c['record']['stage']['required_facts']:
                    f = next((f for f in c['record']['facts'] if f['id'] == r['fact_id']), None)
                    if f is None or any(f[k] is None for k in r['fields']):
                        fail('NEEDS_CLARIFICATION', 'Initial required fact is missing')
            exact(b['record'], c['record'])
        else:
            w = previous['work']; old = w['record']
            followup_request(previous, req); exact(b['inputs'], w['inputs'])
            validate_record_handoff(old, b['record'], req['stage'])
            previous['closed'] = True; previous['work']['phase'] = 'HANDED_OFF'
        fields(b['inputs'], ('source_root', 'ledger_path', 'world_path'))
        for value in b['inputs'].values():
            if type(value) is not str or not 1 <= len(value) <= 4096:
                fail('VALIDATION_FAILED', 'Expected pinned local input-owner path')
        expected = ticket_for(s, m['store_id'], c['ticket_id'], b['selection']['profile'], c['caller_id'])
        exact(b['ticket'], expected)
        validate_task_record(b['record'])
        work = {'record': deepcopy(b['record']), 'request': deepcopy(req),
            'selection': deepcopy(b['selection']), 'inputs': deepcopy(b['inputs']), 'phase': 'RUNNING',
            'stage_ids': (previous['work']['stage_ids'] if previous else []) + [req['stage']['id']]}
        s['tickets'][c['ticket_id']] = {'ticket': expected, 'closed': False, 'work': work}
        s['task_heads'][req['task_id']] = c['ticket_id']; phase = 'RUNNING'
    else:
        exact(b['ticket'], previous['ticket']); exact(b['selection'], previous['work']['selection'])
        exact(b['inputs'], previous['work']['inputs']); old = previous['work']['record']
        if action in STATE_ACTIONS:
            expected = apply_delta(old, c, m, event['at']); phase = 'RUNNING'
        elif action == 'FINISH':
            expected = finish_record(old, previous['ticket']['profile_ecid'], c['results'], c['receipts'])
            phase = 'SEALED'
        elif action == 'CANCEL':
            expected = finish_record(old, previous['ticket']['profile_ecid'], [], c['receipts'], cancel=True)
            phase = 'CANCELLED'; previous['closed'] = True
        else:
            if not old['stage']['sealed']:
                fail('CONSTRAINT_CONFLICT', 'Close cannot discard unfinished work; explicitly cancel or finish')
            expected = old; phase = 'COMPLETED'; previous['closed'] = True
        exact(b['record'], expected); previous['work']['record'] = deepcopy(expected)
        previous['work']['phase'] = phase
        if action == 'CANCEL': previous['work']['cancellation_reason'] = c['reason']
    exact(b['receipt'], receipt(c, b['ticket'], b['record'], phase))
    s['task_operations'][c['operation_id']] = {'command': deepcopy(c), 'receipt': deepcopy(b['receipt'])}
