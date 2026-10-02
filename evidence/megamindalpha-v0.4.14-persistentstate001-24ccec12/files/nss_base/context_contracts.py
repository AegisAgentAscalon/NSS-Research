"""Bounded software context contracts, NOT a tokenizer or learned attention ABI.

Budget unit is canonical ASCII-escaped UTF-8 JSON bytes of the entire payload.
Hashes identify inputs; they do not authenticate permission or establish truth.
"""
from copy import deepcopy
from .experience_contracts import bounded_copy
from .neural_contracts import encoded, fingerprint
from .runtime import fail
from .serialization import validate

FORMAT = 'MegaMindAlpha.ContextRetrieval001'
POLICY = 'explicit_ids_lexical_reviewed_experience_v1'
UNIT = 'CANONICAL_JSON_UTF8_BYTES'
MAX_CONTEXT_BYTES = 131072
MAX_EVIDENCE_BYTES = 2097152
OUTCOMES = ('SUCCESS', 'VALIDATION_FAILED', 'INCOMPATIBLE_CONFIGURATION',
    'AUTHORIZATION_DENIED', 'INSUFFICIENT_EVIDENCE', 'NEEDS_CLARIFICATION',
    'CONSTRAINT_CONFLICT', 'BUDGET_EXHAUSTED', 'CONFLICT_REQUIRES_REVIEW',
    'TRAINING_RESTRICTED', 'RETENTION_RESTRICTED', 'RECOVERY_REQUIRED', 'INTERNAL_FAILURE')
OMISSIONS = ('NOT_SELECTED', 'IRRELEVANT', 'BUDGET_EXHAUSTED',
    'INSUFFICIENT_EVIDENCE', 'CONSTRAINT_CONFLICT', 'CONFLICT_REQUIRES_REVIEW',
    'TRAINING_RESTRICTED', 'RETENTION_RESTRICTED')
TASK_SPINE = ('task_id', 'revision', 'parent_hash', 'goal', 'original_request',
    'stage', 'constraints', 'clarifications', 'unresolved_questions', 'receipts')


def byte_count(value):
    return len(encoded(value))


def request(value):
    x = bounded_copy(value)
    validate(x, 'context_request_v2.schema.json' if x.get('schema_version') == 2 else 'context_request.schema.json')
    for key in ('required_fact_ids', 'optional_fact_ids', 'assumption_ids', 'result_ids'):
        if x[key] != sorted(set(x[key])):
            fail('VALIDATION_FAILED', 'Context selector IDs must be sorted and unique')
    if set(x['required_fact_ids']) & set(x['optional_fact_ids']):
        fail('VALIDATION_FAILED', 'A fact cannot be both required and optional')
    terms = x['query_terms']
    if terms != sorted(set(terms)) or any(not t.strip() or t != t.strip().casefold() for t in terms):
        fail('VALIDATION_FAILED', 'Query terms must be trimmed, casefolded, sorted and unique')
    refs = x['experiences']
    if len({c['reference']['experience_id'] for c in refs}) != len(refs):
        fail('VALIDATION_FAILED', 'Duplicate experience candidate')
    if refs != sorted(refs, key=lambda c: c['reference']['experience_id']):
        fail('VALIDATION_FAILED', 'Experience candidates must be in identifier order')
    for key, sortkey in [('source_fields', lambda c: (c['source_id'], c['field_id'])),
                         ('evidence_slices', lambda c: (c['experience_id'], c['source_id'], c['start_byte'], c['end_byte']))]:
        if x[key] != sorted(x[key], key=sortkey) or len({sortkey(c) for c in x[key]}) != len(x[key]):
            fail('VALIDATION_FAILED', 'Duplicate or unordered exact-source selector')
    ids = {c['reference']['experience_id'] for c in refs}
    for s in x['evidence_slices']:
        if s['experience_id'] not in ids or s['end_byte'] <= s['start_byte']:
            fail('VALIDATION_FAILED', 'Evidence slice needs a candidate and nonempty byte range')
    if (x['archive_binding'] is None) != (not refs):
        fail('VALIDATION_FAILED', 'Pin an archive owner exactly when using experience candidates')
    if x['archive_binding'] is not None:
        a = x['archive_binding']; body = {k: v for k, v in a.items() if k != 'sha256'}
        if fingerprint(body) != a['sha256']:
            fail('VALIDATION_FAILED', 'Archive location binding hash differs')
    return x


def packet(value):
    x = bounded_copy(value)
    validate(x, 'context_packet_v2.schema.json' if x.get('schema_version') == 2 else 'context_packet.schema.json'); request(x['request'])
    if x['request_sha256'] != fingerprint(x['request']):
        fail('VALIDATION_FAILED', 'Context request digest differs')
    if x['payload_sha256'] != fingerprint(x['payload']):
        fail('VALIDATION_FAILED', 'Context payload digest differs')
    actual = byte_count(x['payload'])
    if (x['usage']['context_bytes'] != actual or actual > x['request']['budget']['max_context_bytes']
            or x['usage']['evidence_bytes'] > x['request']['budget']['max_evidence_bytes']):
        fail('VALIDATION_FAILED', 'Context byte accounting differs or exceeds budget')
    if x['binding']['task_state_identity'] != x['request']['expected_task_state_identity']:
        fail('INCOMPATIBLE_CONFIGURATION', 'Context state identity differs')
    return x


def make_request(view, caller_id, *, max_context_bytes=16384,
                 max_evidence_bytes=MAX_EVIDENCE_BYTES):
    """Prepare a proposal from a live view, not a new task/permission authority."""
    extra = {'state_scope':deepcopy(view['record']['persistent_state']['scope'])} if view['record']['schema_version'] == 2 else {}
    return request({'schema_version': 2 if extra else 1, 'format': FORMAT, 'policy': POLICY, **extra,
        'caller_id': caller_id, 'ticket': deepcopy(view['ticket']),
        'expected_record_sha256': fingerprint(view['record']),
        'expected_task_state_identity': view['task_state_identity'],
        'archive_binding': None,
        'budget': {'unit': UNIT, 'max_context_bytes': max_context_bytes,
                   'max_evidence_bytes': max_evidence_bytes},
        'required_fact_ids': [], 'optional_fact_ids': [], 'assumption_ids': [], 'result_ids': [],
        'source_fields': [], 'query_terms': [], 'experiences': [], 'evidence_slices': []})


def seal(req, view, payload, omissions, evidence_bytes):
    out = {'schema_version': req['schema_version'], 'format': FORMAT, 'policy': POLICY,
        'request': deepcopy(req), 'request_sha256': fingerprint(req),
        'binding': {'task_state_identity': view['task_state_identity'],
                    'record_sha256': fingerprint(view['record']),
                    'profile_ecid': view['ticket']['profile_ecid']},
        'payload': payload, 'payload_sha256': fingerprint(payload),
        'omissions': sorted(omissions, key=lambda o: (o['kind'], o['id'], o['reason'])),
        'usage': {'unit': UNIT, 'context_bytes': byte_count(payload), 'evidence_bytes': evidence_bytes},
        'scope': 'POINT_IN_TIME_TRUSTED_LOCAL_READ_NOT_EXECUTION_OR_TRAINING_AUTHORITY',
        'runtime_execution_permit': False, 'training_authorized': False, 'learned_retrieval': False}
    return packet(out)
