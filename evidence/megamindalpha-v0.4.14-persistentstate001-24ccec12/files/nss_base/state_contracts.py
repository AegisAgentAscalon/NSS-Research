"""PersistentState001: strict, scoped proposal/data contracts, no I/O authority.

All new state deltas require declared human review in this first policy. Labels
and hashes are not authentication, calibrated confidence, or proof of truth.
"""
from copy import deepcopy
from .neural_contracts import encoded, fields, fingerprint
from .runtime import ContractError, fail
from .serialization import validate

FORMAT = 'MegaMindAlpha.PersistentState001'
POLICY = 'reviewed_symbolic_deltas_v1'
ACTIONS = ('BIND_STATE', 'UPDATE_STATE')
OPS = ('SET_GOAL', 'ADD_QUESTION', 'RESOLVE_QUESTION', 'DEFER_QUESTION',
       'ADD_NOTE', 'RETIRE_NOTE', 'EXPIRE_NOTE')
MAX_RECORD = 131072


def scope(value):
    validate(value, 'state_scope.schema.json')
    return value


def check_scope(record, supplied):
    """Legacy is never given invented attribution; v2 requires exact scope."""
    if record['schema_version'] == 1:
        if supplied is not None:
            fail('INCOMPATIBLE_CONFIGURATION', 'Legacy record has no admitted scope; bind it explicitly')
    elif supplied is None or scope(supplied) != record['persistent_state']['scope']:
        fail('AUTHORIZATION_DENIED', 'Agent/project/session scope differs or is absent')


def proposal_hash(c):
    return fingerprint({k: v for k, v in c.items() if k != 'review'})


def source_ref(value):
    if type(value) is not dict:
        fail('VALIDATION_FAILED', 'Typed source reference required')
    if value.get('kind') == 'TASK':
        fields(value, ('kind', 'source_id', 'field_id'))
    elif value.get('kind') == 'EXPERIENCE':
        fields(value, ('kind', 'reference'))
    else:
        fail('VALIDATION_FAILED', 'Unknown state evidence source')
    validate(value, 'state_source.schema.json')
    return value


def validate_state(record):
    state = record['persistent_state']
    for key in ('notes', 'annotations'):
        ids = [n['id'] for n in state[key]]
        if len(ids) != len(set(ids)):
            fail('VALIDATION_FAILED', 'Repeated state entry identity')
        for n in state[key]:
            for ref in n['source_refs']: source_ref(ref)
    if state['policy']['policy_id'] != POLICY:
        fail('INCOMPATIBLE_CONFIGURATION', 'Unknown persistent-state policy')
    if len(encoded(record)) > state['policy']['max_record_bytes']:
        fail('BUDGET_EXHAUSTED', 'Mandatory state exceeds admitted byte budget; do not truncate')
    for n in state['notes']:
        if n['expires_at'] is not None and (n['mandatory'] or n['identity_sensitive']):
            fail('VALIDATION_FAILED', 'Mandatory or identity-sensitive notes cannot expire implicitly')
    return record


def command(value):
    # encoded rejects non-finite numbers supplied as Python objects too.
    encoded(value)
    if type(value) is not dict or value.get('action') not in ACTIONS:
        fail('VALIDATION_FAILED', 'Unknown persistent-state command')
    validate(value, 'state_bind.schema.json' if value['action'] == 'BIND_STATE' else 'state_update.schema.json')
    targets = set()
    for op in value.get('deltas', []):
        name = op['op']
        extra = {'SET_GOAL': ('text',), 'ADD_QUESTION': ('id', 'text', 'blocking'),
                 'RESOLVE_QUESTION': ('id', 'answer'), 'DEFER_QUESTION': ('id', 'reason'),
                 'ADD_NOTE': ('note',), 'RETIRE_NOTE': ('id', 'reason'), 'EXPIRE_NOTE': ('id', 'reason')}
        fields(op, ('op', 'source_refs') + extra[name])
        for ref in op['source_refs']: source_ref(ref)
        key = 'goal' if name == 'SET_GOAL' else ('note:' + (op['note']['id'] if name == 'ADD_NOTE' else op['id'])
            if name in ('ADD_NOTE', 'RETIRE_NOTE', 'EXPIRE_NOTE') else 'question:' + op['id'])
        if key in targets: fail('CONSTRAINT_CONFLICT', 'One operation per state target per event')
        targets.add(key)
        if name not in ('RETIRE_NOTE', 'EXPIRE_NOTE') and not op['source_refs']:
            fail('INSUFFICIENT_EVIDENCE', 'New content requires source references')
    return deepcopy(value)


def review(c, manifest, at):
    # Pure role check shared with historical reducer; no current permission cache.
    r = c['review']
    if r is None:
        fail('NEEDS_CLARIFICATION', 'An exact human review is required before this state commit')
    if r['proposal_sha256'] != proposal_hash(c):
        fail('VALIDATION_FAILED', 'Review does not bind the exact proposal')
    operator = next((v for v in manifest['operators'] if v['id'] == r['reviewer_id']), None)
    if operator is None or 'REVIEWER' not in operator['roles']:
        fail('AUTHORIZATION_DENIED', 'Reviewer lacks the declared local review role')
    if r['reviewer_id'] in (c['caller_id'], c['proposer']['id']):
        fail('AUTHORIZATION_DENIED', 'Proposer/executor cannot review its own state change')
    if not r['reviewed_at'] <= at < r['expires_at'] or r['expires_at'] - r['reviewed_at'] > 3600:
        fail('AUTHORIZATION_DENIED', 'State review is expired, premature or exceeds one hour')


def revision_check(old, c, ecid):
    if c['expected_ecid'] != ecid:
        fail('INCOMPATIBLE_CONFIGURATION', 'State proposal targets a different ECID')
    if old['revision'] != c['expected_revision'] or fingerprint(old) != c['expected_record_sha256']:
        e = ContractError('CONSTRAINT_CONFLICT', 'Stale state revision; reread and re-propose')
        e.recovery = {'action': 'REREAD_AND_REPROPOSE', 'state_changed': False}
        raise e


def prepare(view, *, operation_id, proposer_id, proposer_version, state_scope,
            deltas=None, policy=None, archive_binding=None):
    """Construct a proposal only. Caller must obtain a separate review attestation."""
    c = {'schema_version': 2, 'operation_id': operation_id, 'caller_id': view['ticket']['caller_id'],
         'action': 'BIND_STATE' if policy is not None else 'UPDATE_STATE', 'source_ticket': deepcopy(view['ticket']),
         'scope': deepcopy(state_scope), 'expected_revision': view['record']['revision'],
         'expected_record_sha256': fingerprint(view['record']), 'expected_ecid': view['ticket']['profile_ecid'],
         'proposer': {'id': proposer_id, 'version': proposer_version}, 'review': None}
    if policy is not None: c.update(policy=deepcopy(policy), archive_binding=deepcopy(archive_binding))
    else: c['deltas'] = deepcopy(deltas)
    return command(c)


def attest(c, *, reviewer_id, reviewed_at, expires_at, reason):
    """Local declaration, NOT authentication. Only owner commit enforces validity."""
    out = deepcopy(c)
    out['review'] = {'kind': 'HUMAN_LOCAL_ATTESTATION', 'reviewer_id': reviewer_id,
        'proposal_sha256': proposal_hash(c), 'reviewed_at': reviewed_at, 'expires_at': expires_at,
        'decision': 'APPROVE', 'reason': reason}
    return command(out)
