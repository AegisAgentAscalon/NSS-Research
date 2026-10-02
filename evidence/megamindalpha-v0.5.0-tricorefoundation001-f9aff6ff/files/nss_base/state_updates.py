"""Pure symbolic state reduction. Generations is the only journal/head owner.

Historical replay checks structural semantics at the original event time; it
never renews external rights or replays external effects. Current source checks
belong to the public operation boundary in state_sources.
"""
from copy import deepcopy
from .neural_contracts import fingerprint
from .runtime import fail
from .state_contracts import check_scope, review, revision_check
from .task_records import validate_task_record


def apply_delta(old, c, manifest, at, *, configuration_sha256=None):
    validate_task_record(old)
    if c.get('schema_version') == 3:
        if configuration_sha256 is None:
            fail('INCOMPATIBLE_CONFIGURATION', 'Current-role update needs its exact configuration')
        revision_check(old, c, configuration_sha256)
    else:
        revision_check(old, c, c['source_ticket']['profile_ecid'])
    if old['stage']['sealed']:
        fail('CONSTRAINT_CONFLICT', 'Only a running unsealed stage accepts state deltas')
    review(c, manifest, at)
    out = deepcopy(old)
    if c['action'] == 'BIND_STATE':
        if old['schema_version'] != 1:
            fail('CONSTRAINT_CONFLICT', 'Scope is immutable; an admitted record cannot be rebound')
        out['schema_version'] = 2
        out['persistent_state'] = {'schema_version': 1, 'scope': deepcopy(c['scope']),
            'policy': deepcopy(c['policy']), 'archive_binding': deepcopy(c['archive_binding']),
            'last_event_id': c['operation_id'], 'authority': 'REVIEWED_WORKING_DATA_NOT_INSTRUCTION', 'notes': [], 'annotations': []}
    else:
        check_scope(old, c['scope'])
        if old['schema_version'] != 2: fail('INCOMPATIBLE_CONFIGURATION', 'Bind state before updating')
        state = out['persistent_state']
        for op in c['deltas']:
            name = op['op']; refs = deepcopy(op['source_refs'])
            meta = {'author': deepcopy(c['proposer']), 'reviewer_id': c['review']['reviewer_id'],
                    'event_id': c['operation_id'], 'source_refs': refs}
            if name == 'ADD_NOTE':
                n = deepcopy(op['note'])
                if any(p['id'] == n['id'] for p in state['notes']):
                    fail('CONSTRAINT_CONFLICT', 'Existing note needs explicit retirement, not overwrite')
                if n['expires_at'] is not None and n['expires_at'] <= at:
                    fail('VALIDATION_FAILED', 'New transient note must not already be expired')
                state['notes'].append({**n, **meta})
            elif name in ('RETIRE_NOTE', 'EXPIRE_NOTE'):
                n = next((n for n in state['notes'] if n['id'] == op['id']), None)
                if n is None: fail('INSUFFICIENT_EVIDENCE', 'Unknown note to retire')
                if name == 'EXPIRE_NOTE' and (n['expires_at'] is None or n['expires_at'] > at):
                    fail('CONSTRAINT_CONFLICT', 'Note has not reached its declared expiry')
                state['notes'].remove(n)  # Prior bytes remain in immutable journal revisions.
            else:
                target = 'goal' if name == 'SET_GOAL' else 'question:' + op['id']
                if name == 'SET_GOAL': out['goal'] = op['text']
                elif name == 'ADD_QUESTION':
                    if any(q['id'] == op['id'] for q in out['unresolved_questions']):
                        fail('CONSTRAINT_CONFLICT', 'Question ID already exists')
                    out['unresolved_questions'].append({k: op[k] for k in ('id', 'text', 'blocking')})
                else:
                    q = next((q for q in out['unresolved_questions'] if q['id'] == op['id']), None)
                    if q is None: fail('INSUFFICIENT_EVIDENCE', 'Question to resolve/defer is absent')
                    if any(v['question_id'] == q['id'] for v in out['clarifications']):
                        fail('CONSTRAINT_CONFLICT', 'Resolved question cannot be silently rewritten')
                    if name == 'RESOLVE_QUESTION':
                        task_refs = [r for r in refs if r['kind'] == 'TASK']
                        if len(task_refs) != 1: fail('VALIDATION_FAILED', 'Resolution needs one exact user source field')
                        sid = task_refs[0]['source_id']
                        if not any(s['id'] == sid and s['kind'] == 'user' for s in out['sources']):
                            fail('AUTHORIZATION_DENIED', 'Generated interpretation cannot forge user clarification')
                        out['clarifications'].append({'id': 'state:' + fingerprint({'event':c['operation_id'],'question':q['id']}), 'question_id': q['id'],
                                                      'answer': op['answer'], 'source_id': sid})
                    else: q['blocking'] = False  # Explicit deferral, not a fabricated answer.
                state['annotations'] = [a for a in state['annotations'] if a['id'] != target]
                state['annotations'].append({'id': target, 'change': name,
                    'reason': op.get('reason', 'Source-backed, explicitly reviewed update'), **meta})
        state['last_event_id'] = c['operation_id']
    out.update(revision=old['revision']+1, parent_hash=fingerprint(old))
    validate_task_record(out)
    return out
