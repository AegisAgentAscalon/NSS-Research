"""Portable working-state contracts for StageHandoff001 (no neural judgment).

Legacy records are embedded in checkpoint v2 bodies; managed v2 scoped records
are owned by Generations. Explicit review admits legacy v1 records. This module owns no
SQL store, action executor, training loop or release authority. Source completion
copies exact fields from allowlisted local, hashed fixture artifacts; it does
not infer or certify their truth.
"""
from copy import deepcopy
import json
from pathlib import Path

from .runtime import digest, fail
from .serialization import validate
from .state_contracts import validate_state

MAX_RECORD_BYTES = 131072
MAX_SOURCE_BYTES = 262144


def _unique(items, key, label):
    values = [x[key] for x in items]
    if len(values) != len(set(values)):
        fail('VALIDATION_FAILED', f'Duplicate {label}')


def validate_stage(stage):
    validate(stage, 'task_stage.schema.json')
    _unique(stage['required_facts'], 'fact_id', 'required fact')
    return stage


def validate_task_record(record):
    if type(record) is not dict or record.get('schema_version') not in (1, 2):
        fail('VALIDATION_FAILED', 'Unknown TaskRecord version')
    validate(record, 'task_record_v2.schema.json' if record['schema_version'] == 2 else 'task_record.schema.json')
    if record['schema_version'] == 2: validate_state(record)
    if record['schema_version'] == 1 and len(json.dumps(record, ensure_ascii=True).encode('utf-8')) > MAX_RECORD_BYTES:
        fail('VALIDATION_FAILED', 'TaskRecord exceeds bounded working-record budget')
    if (record['revision'] == 0) != (record['parent_hash'] is None):
        fail('VALIDATION_FAILED', 'Revision zero alone has no parent record hash')
    for key in ('sources','facts','assumptions','unresolved_questions','clarifications','checked_results','constraints'):
        _unique(record[key], 'id', key+' ID')
    _unique(record['receipts'], 'key', 'receipt key')
    _unique(record['clarifications'], 'question_id', 'resolved question')
    sources = {s['id']:s for s in record['sources']}
    questions = {q['id'] for q in record['unresolved_questions']}
    refs = [record['original_request']['source_id']]
    refs += [x['source_id'] for key in ('facts','clarifications','constraints') for x in record[key]]
    refs += [s for key in ('assumptions','checked_results') for x in record[key] for s in x['source_ids']]
    if not set(refs) <= sources.keys():
        fail('VALIDATION_FAILED', 'Dangling TaskRecord source reference')
    if any(c['question_id'] not in questions for c in record['clarifications']):
        fail('VALIDATION_FAILED', 'Clarification references unknown question')
    if any(c['origin'] != sources[c['source_id']]['kind'] for c in record['constraints']):
        fail('VALIDATION_FAILED', 'Constraint origin must match its source class')
    for s in record['sources']:
        path = Path(s['artifact']['path'])
        if path.is_absolute() or '..' in path.parts or '\\' in s['artifact']['path']:
            fail('VALIDATION_FAILED', 'Sources must name portable relative fixture paths')
    validate_stage(record['stage'])
    return record


def validate_checkpoint(state):
    """v1 is legacy; v2 requires a task-bound portable record. No silent upgrade."""
    validate(state, 'checkpoint.schema.json')
    has_record = 'task_record' in state
    if (state['schema_version'] == 2) != has_record:
        fail('VALIDATION_FAILED', 'Checkpoint version and TaskRecord presence disagree')
    if has_record:
        validate_task_record(state['task_record'])
        if state['task_record']['task_id'] != state['task_id']:
            fail('VALIDATION_FAILED', 'Checkpoint and TaskRecord belong to different tasks')
    return state


def attach_task_record(state, record):
    validate_checkpoint(state); validate_task_record(record)
    updated = deepcopy(state)
    updated.update(schema_version=2, task_record=deepcopy(record))
    validate_checkpoint(updated)
    return updated


def validate_request(request):
    validate(request, 'stage_handoff_request.schema.json')
    validate_stage(request['next_stage'])
    if request['next_stage']['sealed']:
        fail('VALIDATION_FAILED', 'A newly entered stage must be unsealed')
    return request


def validate_receipts(record, ledger):
    """Receipt completeness/integrity for the existing authoritative local mock."""
    keys = ledger.action_keys(record['task_id'])
    if keys != sorted(x['key'] for x in record['receipts']):
        fail('RECOVERY_REQUIRED', 'TaskRecord receipt set differs from verified task actions')
    for r in record['receipts']:
        a = ledger.inspect(r['key'])
        if a is None or a['task_id'] != record['task_id'] or a['receipt'] != r['receipt']:
            fail('VALIDATION_FAILED', 'TaskRecord receipt does not match mock action evidence')


def source_document(root, source, *, byte_limit=MAX_SOURCE_BYTES):
    """Read one admitted local fixture exactly; no network or archive permission.

    Archive-derived evidence must use the archive's purpose-aware public API.
    This helper is shared by stage handoffs and bounded context assembly.
    """
    from hashlib import sha256
    from .serialization import decode
    if type(byte_limit) is not int or not 0 <= byte_limit <= MAX_SOURCE_BYTES:
        fail('VALIDATION_FAILED', 'Invalid local source-read limit')
    if type(source) is not dict or 'artifact' not in source:
        fail('VALIDATION_FAILED', 'Expected a typed source artifact')
    validate(source['artifact'], 'artifact.schema.json')
    root = Path(root).resolve(); relative = Path(source['artifact']['path'])
    path = (root / relative).resolve()
    if relative.is_absolute() or '..' in relative.parts or '\\' in str(relative) or not path.is_relative_to(root):
        fail('VALIDATION_FAILED', 'Source escapes admitted artifact root')
    try:
        with path.open('rb') as f: raw = f.read(byte_limit + 1)
    except OSError:
        fail('INSUFFICIENT_EVIDENCE', 'Referenced exact source is unavailable; do not invent it')
    if len(raw) > byte_limit:
        fail('BUDGET_EXHAUSTED' if byte_limit < MAX_SOURCE_BYTES else 'VALIDATION_FAILED',
             'Source exceeds bounded fixture read budget')
    if sha256(raw).hexdigest() != source['artifact']['sha256']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Artifact bytes differ from manifest hash')
    try:
        evidence = validate(decode(raw.decode('utf-8')), 'handoff_evidence.schema.json')
    except UnicodeError:
        fail('VALIDATION_FAILED', 'Artifact is not UTF-8')
    _unique(evidence['fields'], 'id', 'source field')
    return {'fields': {f['id']: f for f in evidence['fields']}, 'bytes': len(raw)}


def source_fields(root, source):
    return source_document(root, source)['fields']


def advance_record(old, stage, *, evidence_root):
    """Portable handoff: no backend, cache, SQL, permission or ledger authority."""
    validate_task_record(old); validate_stage(stage)
    if not old['stage']['sealed'] or stage['sealed'] or stage['id'] == old['stage']['id']:
        fail('CONSTRAINT_CONFLICT', 'Handoff requires a sealed source and a new unsealed stage')
    resolved = {c['question_id'] for c in old['clarifications']}
    if any(q['blocking'] and q['id'] not in resolved for q in old['unresolved_questions']):
        fail('NEEDS_CLARIFICATION', 'Unresolved blocking question prevents stage handoff')
    target = deepcopy(old)
    facts = {f['id']: f for f in target['facts']}
    sources = {s['id']: s for s in old['sources']}
    read_cache = {}  # Only this exact operation; never a persistent permission cache.
    for req in stage['required_facts']:
        fact = facts.get(req['fact_id'])
        if fact is None:
            fail('NEEDS_CLARIFICATION', 'Required fact is absent; assumptions are not facts')
        sid = fact['source_id']
        if sid not in read_cache:
            read_cache[sid] = source_fields(evidence_root, sources[sid])
        original = read_cache[sid].get(fact['source_field'])
        if original is None:
            fail('NEEDS_CLARIFICATION', 'Exact source lacks the referenced field')
        for name in ('value', 'unit'):
            if fact[name] is not None and fact[name] != original[name]:
                fail('CONSTRAINT_CONFLICT', 'Existing fact disagrees with exact source')
        for name in req['fields']:
            if original[name] is None:
                fail('NEEDS_CLARIFICATION', 'Required source value/unit is unknown')
            fact[name] = original[name]
    target.update(revision=old['revision'] + 1, parent_hash=digest(old), stage=deepcopy(stage))
    validate_record_handoff(old, target, stage)
    return target


def validate_record_handoff(old, new, stage):
    """Check preservation without interpreting content or re-reading external sources."""
    validate_task_record(old); validate_task_record(new); validate_stage(stage)
    if not old['stage']['sealed'] or stage['sealed'] or old['stage']['id'] == stage['id']:
        fail('CONSTRAINT_CONFLICT', 'Invalid handoff boundary')
    if new['revision'] != old['revision'] + 1 or new['parent_hash'] != digest(old) or new['stage'] != stage:
        fail('INCOMPATIBLE_CONFIGURATION', 'Target record lineage or stage changed')
    for k in old:
        if k not in ('revision', 'parent_hash', 'stage', 'facts') and old[k] != new[k]:
            fail('INCOMPATIBLE_CONFIGURATION', 'Handoff discarded or modified portable task information')
    if len(old['facts']) != len(new['facts']):
        fail('INCOMPATIBLE_CONFIGURATION', 'Handoff cannot invent/remove facts')
    allowed = {r['fact_id']: r['fields'] for r in stage['required_facts']}
    for before, after in zip(old['facts'], new['facts']):
        for key in before:
            if before[key] == after[key]: continue
            if key not in ('value', 'unit') or before[key] is not None or key not in allowed.get(before['id'], []):
                fail('INCOMPATIBLE_CONFIGURATION', 'Only missing required fact properties may be filled')
    return new

def _validate_mode(bundle, profile, stage):
    selected = bundle.catalog.profile(profile)
    if stage['mode'] in ('CONTROL','EVALUATION') and selected.overlays:
        fail('INCOMPATIBLE_CONFIGURATION', 'Control/evaluation stages require Core-only state')


def prepare_handoff(bundle, source, destination, request, ledger):
    """Bounded plan: preserve the record, fill missing required facts from sources."""
    validate_checkpoint(source); validate_request(request)
    if source['schema_version'] != 2:
        fail('VALIDATION_FAILED', 'Stage handoff requires checkpoint v2')
    if request['source_checkpoint_hash'] != digest(source):
        fail('INCOMPATIBLE_CONFIGURATION', 'Handoff source checkpoint changed')
    old = source['task_record']; stage = request['next_stage']
    if not old['stage']['sealed'] or stage['id'] == old['stage']['id']:
        fail('CONSTRAINT_CONFLICT', 'Handoff requires a sealed source and a new stage ID')
    _validate_mode(bundle, source['profile'], old['stage'])
    _validate_mode(bundle, destination, stage)
    validate_receipts(old, ledger)
    target = advance_record(old, stage, evidence_root=bundle.root)
    binding = {'request':deepcopy(request),'target_record':target}
    validate_handoff_binding(source, binding)
    return binding


def validate_handoff_binding(source, binding):
    """Structural binding rechecked within publication; exact sources checked by planner."""
    validate_checkpoint(source)
    if source['schema_version'] != 2 or type(binding) is not dict or set(binding) != {'request','target_record'}:
        fail('VALIDATION_FAILED', 'Annotated checkpoint needs an exact handoff binding')
    request = validate_request(binding['request'])
    old, new = source['task_record'], validate_task_record(binding['target_record'])
    if request['source_checkpoint_hash'] != digest(source):
        fail('INCOMPATIBLE_CONFIGURATION', 'Handoff does not bind exact source')
    validate_record_handoff(old, new, request['next_stage'])
    return binding


def validate_target_record(source, binding, target):
    validate_checkpoint(target); validate_handoff_binding(source, binding)
    if target.get('task_record') != binding['target_record']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Staged record differs from bound handoff')


def finish_record(record, ecid, results, receipts, *, cancel=False):
    validate_task_record(record)
    if record['stage']['sealed'] and not cancel:
        fail('CONSTRAINT_CONFLICT', 'Stage already finished')
    if type(results) is not list or type(receipts) is not list:
        fail('VALIDATION_FAILED', 'New results/receipts must be arrays')
    out = deepcopy(record)
    out.update(revision=record['revision'] + 1, parent_hash=digest(record))
    if not cancel: out['stage']['sealed'] = True
    out['checked_results'].extend(deepcopy(results)); out['receipts'].extend(deepcopy(receipts))
    validate_task_record(out)
    if any(r['producer_ecid'] != ecid for r in results):
        fail('INCOMPATIBLE_CONFIGURATION', 'Result belongs to a different neural profile')
    return out


def sealed_revision(state, results, receipts):
    validate_checkpoint(state)
    if state['schema_version'] != 2:
        fail('VALIDATION_FAILED', 'Stage finish requires a TaskRecord')
    return finish_record(state['task_record'], state['ecid'], results, receipts)


def validate_sealed_revision(state, new):
    validate_checkpoint(state);validate_task_record(new)
    old=state['task_record']
    if old['stage']['sealed']:
        fail('CONSTRAINT_CONFLICT', 'Stage is already sealed')
    expected_stage=deepcopy(old['stage']);expected_stage['sealed']=True
    if new['revision']!=old['revision']+1 or new['parent_hash']!=digest(old) or new['stage']!=expected_stage:
        fail('INCOMPATIBLE_CONFIGURATION', 'Stage finish changed its lineage or boundary')
    for k in old:
        if k not in ('stage','revision','parent_hash','checked_results','receipts') and new[k]!=old[k]:
            fail('INCOMPATIBLE_CONFIGURATION', 'Stage finish changed existing portable state')
    for k in ('checked_results','receipts'):
        if new[k][:len(old[k])]!=old[k] or len(new[k])<len(old[k]):
            fail('INCOMPATIBLE_CONFIGURATION', 'Stage finish may append but not overwrite evidence')
    for result in new['checked_results'][len(old['checked_results']):]:
        if result['producer_ecid']!=state['ecid']:
            fail('INCOMPATIBLE_CONFIGURATION', 'New result belongs to a different execution configuration')
