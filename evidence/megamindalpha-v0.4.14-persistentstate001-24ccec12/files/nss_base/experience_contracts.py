"""ExperienceArchive001: pure, bounded record/review semantics.

Actors and permissions are local operator attestations, not authentication or a
legal determination. Hashes bind bytes/lineage, not truth. No training consumer.
"""
from copy import deepcopy
from datetime import datetime
from hashlib import sha256
import json
import re

from .runtime import digest, fail
from .serialization import decode, validate
from .task_records import validate_task_record

PURPOSES = ('memory', 'retrieval', 'training', 'redistribution')
ACTIONS = ('ANNOTATE', 'CORRECT', 'REVIEW', 'DISPUTE', 'RESOLVE', 'PERMISSION', 'WITHDRAW')
MAX_COMMAND_BYTES = 4 * 1024 * 1024
MAX_SOURCE_BYTES = 1024 * 1024
MAX_REVISIONS = 512


def identifier(value):
    if type(value) is not str or re.fullmatch(r'[A-Za-z0-9_.:-]{1,128}', value) is None:
        fail('VALIDATION_FAILED', 'Invalid identifier')
    return value


def hash_id(value):
    if type(value) is not str or re.fullmatch('[0-9a-f]{64}', value) is None:
        fail('VALIDATION_FAILED', 'Invalid SHA-256 reference')
    return value


def purpose(value):
    if type(value) is not str or value not in PURPOSES:
        fail('VALIDATION_FAILED', 'Unknown use purpose')
    return value


def bounded_copy(value):
    """Reject cyclic, non-finite, deeply nested, non-JSON and oversized inputs."""
    def check(x, depth=0):
        if depth > 24:
            fail('VALIDATION_FAILED', 'JSON nesting exceeds record contract')
        if type(x) is dict:
            if any(type(k) is not str for k in x):
                fail('VALIDATION_FAILED', 'JSON object keys must be strings')
            for child in x.values(): check(child, depth + 1)
        elif type(x) is list:
            for child in x: check(child, depth + 1)
        elif type(x) not in (str, int, bool, type(None)):
            fail('VALIDATION_FAILED', 'Unsupported JSON value type')
    try:
        check(value)
        encoded = json.dumps(value, ensure_ascii=False, allow_nan=False).encode('utf-8')
        if len(encoded) > MAX_COMMAND_BYTES:
            fail('VALIDATION_FAILED', 'Command exceeds bounded archive budget')
        return deepcopy(value)
    except (UnicodeError, RecursionError, TypeError, ValueError) as exc:
        # Preserve deliberate typed contract failures.
        if hasattr(exc, 'code'): raise
        fail('VALIDATION_FAILED', 'Invalid or oversized JSON input')


def timestamp(value):
    if type(value) is not str or re.fullmatch(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z', value) is None:
        fail('VALIDATION_FAILED', 'Timestamp must be UTC YYYY-MM-DDTHH:MM:SSZ')
    try:
        datetime.strptime(value, '%Y-%m-%dT%H:%M:%SZ')
    except ValueError:
        fail('VALIDATION_FAILED', 'Invalid calendar timestamp')
    return value


def human(actor):
    if actor['kind'] != 'HUMAN':
        fail('AUTHORIZATION_DENIED', 'This operation requires a local HUMAN review attestation')


def source_metadata(sources):
    """Check explicit source labels and an acyclic, record-local derivation graph."""
    by_id = {}
    for source in sources:
        validate(source, 'experience_source.schema.json')
        timestamp(source['recorded_at'])
        sid = source['id']
        if sid in by_id: fail('VALIDATION_FAILED', 'Duplicate source ID')
        by_id[sid] = source
        parents = source['parent_source_ids']
        if len(parents) != len(set(parents)):
            fail('VALIDATION_FAILED', 'Duplicate source parent')
        if source['kind'] == 'SYNTHETIC':
            if not parents or source['generator'] is None or source['generator']['kind'] not in ('MODEL', 'SYSTEM'):
                fail('VALIDATION_FAILED', 'Synthetic evidence needs generator/version and source parents')
    visiting, visited = set(), set()
    def visit(sid):
        if sid not in by_id: fail('VALIDATION_FAILED', 'Dangling source parent')
        if sid in visiting: fail('VALIDATION_FAILED', 'Cyclic source lineage')
        if sid in visited: return
        visiting.add(sid)
        for parent in by_id[sid]['parent_source_ids']: visit(parent)
        visiting.remove(sid); visited.add(sid)
    for sid in by_id: visit(sid)
    return sources


def _extract_evidence(command):
    """Normalize evidence to refs; raw UTF-8 bytes are stored once in the blob table."""
    location = command if 'evidence' in command else command.get('payload', {})
    blobs, refs, seen = {}, [], set()
    for item in location.get('evidence', []):
        if item['id'] in seen: fail('VALIDATION_FAILED', 'Duplicate submitted source ID')
        seen.add(item['id'])
        content = item.pop('content').encode('utf-8')
        if len(content) > MAX_SOURCE_BYTES or sha256(content).hexdigest() != item['sha256']:
            fail('VALIDATION_FAILED', 'Evidence bytes and declared digest disagree or exceed limit')
        if item['sha256'] in blobs and blobs[item['sha256']] != content:
            fail('VALIDATION_FAILED', 'Evidence hash collision')
        blobs[item['sha256']] = content
        refs.append(item)
    if 'evidence' in location: location['evidence'] = refs
    return command, blobs


def _task_snapshot(command):
    """Check the portable snapshot binding, not authenticity of claimed execution."""
    execution=command['observation']['execution']
    if execution is None: return
    snapshots=[s for s in command['evidence'] if s['kind']=='TASK_SNAPSHOT']
    if len(snapshots)!=1:
        fail('VALIDATION_FAILED','A task-stage observation needs exactly one portable task snapshot')
    source=snapshots[0]
    try:
        record=validate_task_record(decode(source['content']))
    except (RecursionError,UnicodeError):
        fail('VALIDATION_FAILED','Malformed portable task snapshot')
    if (digest(record)!=execution['task_record_sha256'] or source['sha256']!=digest(record)
            or record['task_id']!=execution['task_id'] or record['stage']['id']!=execution['stage_id']
            or not record['stage']['sealed']):
        fail('VALIDATION_FAILED','Task snapshot identity, hash, stage, or sealing does not match capture')
    sources={s['id']:s for s in command['evidence']}
    for original in record['sources']:
        captured=sources.get(original['id'])
        if captured is None or captured['sha256']!=original['artifact']['sha256']:
            fail('VALIDATION_FAILED','Task source reference is not preserved by capture')


def normalize(command, kind):
    command = bounded_copy(command)
    if kind == 'CAPTURE':
        validate(command, 'experience_capture.schema.json')
        obs = command['observation']
        if (obs['kind'] == 'TASK_STAGE') != (obs['execution'] is not None):
            fail('VALIDATION_FAILED', 'Observation kind and execution context disagree')
        _task_snapshot(command)
    elif kind == 'CHANGE':
        if type(command) is not dict or command.get('action') not in ACTIONS:
            fail('VALIDATION_FAILED', 'Unknown archive mutation')
        validate(command, 'experience_' + command['action'].lower() + '.schema.json')
    elif kind == 'REVOKE_SOURCE':
        validate(command, 'experience_source_revocation.schema.json')
    else:
        fail('VALIDATION_FAILED', 'Unknown archive operation kind')
    timestamp(command['at'])
    return _extract_evidence(command)


def _support(ids, sources):
    if not ids or len(ids) != len(set(ids)) or not set(ids) <= {s['id'] for s in sources}:
        fail('VALIDATION_FAILED', 'Missing, duplicate, or dangling supporting source references')


def _review(status='PENDING_REVIEW', command=None):
    return {'status': status, 'reviewer': deepcopy(command['actor']) if command else None,
            'at': command['at'] if command else None, 'reason': command['reason'] if command else ''}


def _statement(command, prior=None):
    raw = command['statement'] if 'statement' in command else command['payload']['statement']
    return {**deepcopy(raw), 'kind': 'CORRECTION' if command.get('action') == 'CORRECT' else 'INTERPRETATION',
            'author': deepcopy(command['actor']), 'recorded_at': command['at'],
            'supersedes': digest(prior['statement']) if prior else None}


def validate_revision(state):
    validate(state, 'experience_revision.schema.json')
    timestamp(state['updated_at']); timestamp(state['statement']['recorded_at'])
    if (state['revision'] == 0) != (state['parent_hash'] is None):
        fail('VALIDATION_FAILED', 'Broken archive revision lineage')
    source_metadata(state['sources']); _support(state['statement']['support_ids'], state['sources'])
    seen = set()
    for conflict in state['conflicts']:
        if conflict['id'] in seen: fail('VALIDATION_FAILED', 'Duplicate conflict ID')
        seen.add(conflict['id']); _support(conflict['support_ids'], state['sources'])
        timestamp(conflict['raised_at'])
        if (conflict['status'] == 'RESOLVED') != (conflict['resolution'] is not None):
            fail('VALIDATION_FAILED', 'Conflict status and resolution disagree')
        if conflict['resolution']:
            human(conflict['resolution']['actor']); timestamp(conflict['resolution']['at'])
            _support(conflict['resolution']['support_ids'], state['sources'])
    status = state['review']['status']
    if any(c['status'] == 'OPEN' for c in state['conflicts']) and status not in ('QUARANTINED','WITHDRAWN'):
        fail('VALIDATION_FAILED', 'Open conflicts cannot become approved facts')
    if status in ('APPROVED','REJECTED','WITHDRAWN'):
        if state['review']['reviewer'] is None: fail('VALIDATION_FAILED', 'Missing reviewer attribution')
        human(state['review']['reviewer']); timestamp(state['review']['at'])
    for permission in state['permissions'].values():
        if permission['status'] != 'UNKNOWN':
            if permission['actor'] is None or permission['permission_ref'] is None:
                fail('VALIDATION_FAILED', 'Permission decision needs attribution and reference')
            human(permission['actor']); timestamp(permission['at'])
    return state


def initial_revision(command):
    source_metadata(command['evidence']); _support(command['statement']['support_ids'], command['evidence'])
    state = {'schema_version': 1, 'experience_id': command['experience_id'], 'revision': 0,
        'parent_hash': None, 'capture_hash': digest(command), 'updated_at': command['at'],
        'sources': deepcopy(command['evidence']), 'statement': _statement(command),
        'review': _review(), 'conflicts': [], 'permissions': {p: {
            'status': 'UNKNOWN','actor':None,'at':None,'reason':'','permission_ref':None} for p in PURPOSES}}
    return validate_revision(state)


def next_revision(prior, command):
    """Deterministic reducer: every decision remains visible and replay-verifiable."""
    validate_revision(prior)
    if command['experience_id'] != prior['experience_id'] or command['expected_revision_hash'] != digest(prior):
        fail('CONSTRAINT_CONFLICT', 'Mutation requires the exact current experience revision')
    if prior['revision'] + 1 >= MAX_REVISIONS:
        fail('BUDGET_EXHAUSTED', 'Per-record revision budget reached; explicit migration required')
    if command['at'] < prior['updated_at']:
        fail('VALIDATION_FAILED', 'Review timestamp precedes current revision')
    if prior['review']['status'] == 'WITHDRAWN':
        fail('RETENTION_RESTRICTED', 'Withdrawn records remain inspection-only in this version')
    action, payload = command['action'], command['payload']
    if action != 'ANNOTATE' and action != 'DISPUTE': human(command['actor'])
    state = deepcopy(prior)
    state.update(revision=prior['revision']+1, parent_hash=digest(prior), updated_at=command['at'])
    existing = {s['id']: s for s in state['sources']}
    for new in payload.get('evidence', []):
        if new['id'] in existing:
            if existing[new['id']] != new: fail('CONSTRAINT_CONFLICT', 'Source ID already binds different evidence')
        else:
            state['sources'].append(deepcopy(new)); existing[new['id']] = new
    source_metadata(state['sources'])
    open_conflicts = any(c['status'] == 'OPEN' for c in state['conflicts'])
    if action in ('ANNOTATE', 'CORRECT'):
        state['statement'] = _statement(command, prior)
        _support(state['statement']['support_ids'], state['sources'])
        state['review'] = _review('QUARANTINED' if open_conflicts else 'PENDING_REVIEW')
        for p in state['permissions'].values():
            if p['status'] == 'ALLOWED':
                p.update(status='UNKNOWN', actor=None, at=None,
                         reason='Changed interpretation requires fresh purpose permission.', permission_ref=None)
    elif action == 'REVIEW':
        if open_conflicts: fail('CONFLICT_REQUIRES_REVIEW', 'Resolve open disputes before approving or rejecting')
        state['review'] = _review(payload['decision'], command)
    elif action == 'DISPUTE':
        if any(c['id'] == payload['conflict_id'] for c in state['conflicts']):
            fail('CONSTRAINT_CONFLICT', 'Conflict ID already exists')
        _support(payload['support_ids'], state['sources'])
        state['conflicts'].append({'id':payload['conflict_id'],'status':'OPEN',
            'raised_by':deepcopy(command['actor']),'raised_at':command['at'],
            'reason':command['reason'],'support_ids':deepcopy(payload['support_ids']),'resolution':None})
        state['review'] = _review('QUARANTINED', command)
    elif action == 'RESOLVE':
        conflict = next((c for c in state['conflicts'] if c['id'] == payload['conflict_id']), None)
        if conflict is None: fail('VALIDATION_FAILED', 'Unknown conflict')
        if conflict['status'] != 'OPEN': fail('CONSTRAINT_CONFLICT', 'Conflict is already resolved')
        _support(payload['support_ids'], state['sources'])
        conflict['status']='RESOLVED'
        conflict['resolution']={'actor':deepcopy(command['actor']),'at':command['at'],
            'reason':command['reason'],'support_ids':deepcopy(payload['support_ids'])}
        state['review']=_review('QUARANTINED' if any(c['status']=='OPEN' for c in state['conflicts']) else 'PENDING_REVIEW')
    elif action == 'PERMISSION':
        p = state['permissions'][payload['purpose']]
        if p['status']=='REVOKED' and payload['decision']!='REVOKED':
            fail('TRAINING_RESTRICTED','Revoked record permission has no regrant operation in schema v1')
        p.update(status=payload['decision'],actor=deepcopy(command['actor']),at=command['at'],
                 reason=command['reason'],permission_ref=payload['permission_ref'])
    elif action == 'WITHDRAW':
        state['review'] = _review('WITHDRAWN', command)
    return validate_revision(state)


def check_use(state, requested_purpose, revoked):
    purpose(requested_purpose); validate_revision(state)
    if state['review']['status']=='WITHDRAWN': fail('RETENTION_RESTRICTED','Record is withdrawn; inspection is not downstream permission')
    if state['review']['status']!='APPROVED': fail('CONFLICT_REQUIRES_REVIEW','An explicit accepted review is required')
    if state['permissions'][requested_purpose]['status']!='ALLOWED' or revoked:
        fail('TRAINING_RESTRICTED','Requested purpose lacks current permission or a source was revoked')
