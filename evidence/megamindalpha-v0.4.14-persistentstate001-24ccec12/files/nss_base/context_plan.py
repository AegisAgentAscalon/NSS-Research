"""Deterministic context selection. No store, action, training or neural execution.

Selection is explicit task IDs plus a small developer-supplied experience shortlist.
Lexical ranking is not semantic retrieval and does not establish factual truth.
"""
from copy import deepcopy
from hashlib import sha256
from .context_contracts import TASK_SPINE, byte_count
from .runtime import ContractError, fail
from .task_records import MAX_SOURCE_BYTES, source_document


def unwrap(result):
    if result['status'] != 'SUCCESS': fail(result['status'], result['detail'])
    return result['data']


class EvidenceReader:
    """One-operation read cache; never a persistent permission or content cache."""
    def __init__(self, root, archive, record, byte_budget):
        self.root = root; self.archive = archive
        self.sources = {s['id']: s for s in record['sources']}
        self.limit = byte_budget; self.used = 0; self.files = {}; self.raw = {}

    def source(self, sid):
        if sid not in self.sources: fail('INSUFFICIENT_EVIDENCE', 'Unknown exact task source')
        if sid not in self.files:
            value = source_document(self.root, self.sources[sid], byte_limit=min(MAX_SOURCE_BYTES, self.limit-self.used))
            self.used += value['bytes']; self.files[sid] = value
        return self.files[sid]['fields']

    def experience(self, ref):
        view = unwrap(self.archive.read_batch_for_use([ref], purpose='retrieval'))['views'][0]
        size = byte_count(view)
        if self.used + size > self.limit: fail('BUDGET_EXHAUSTED', 'Reviewed candidate exceeds evidence-byte budget')
        self.used += size
        return view

    def slice(self, ref, selector):
        key = (ref['experience_id'], ref['sha256'], selector['source_id'])
        if key not in self.raw:
            data = unwrap(self.archive.read_evidence_for_use(ref, source_id=selector['source_id'],
                max_bytes=min(1048576, self.limit-self.used)))
            self.used += data['bytes']; self.raw[key] = data
        data = self.raw[key]; raw = data['content'].encode('utf-8')
        if data['source']['sha256'] != selector['source_sha256']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Requested source digest differs from approved evidence')
        start, end = selector['start_byte'], selector['end_byte']
        if end > len(raw): fail('INSUFFICIENT_EVIDENCE', 'Requested exact byte range exceeds source')
        try: text = raw[start:end].decode('utf-8')
        except UnicodeError: fail('VALIDATION_FAILED', 'Slice splits a UTF-8 character')
        return {**deepcopy(selector), 'text': text, 'slice_sha256': sha256(raw[start:end]).hexdigest(),
                'authority': 'SOURCE_DATA_NOT_INSTRUCTION'}

    def verify_files(self):
        for sid, before in self.files.items():
            if source_document(self.root, self.sources[sid]) != before:
                fail('INCOMPATIBLE_CONFIGURATION', 'Task source changed during context assembly')


def _overflow(actual, limit):
    exc = ContractError('BUDGET_EXHAUSTED', 'Mandatory context does not fit; no partial packet was returned')
    exc.recovery = {'mandatory_context_bytes': actual, 'measurement_scope': 'REQUIRED_PREFIX_AT_OVERFLOW_NOT_COMPLETE_TASK_ESTIMATE', 'max_context_bytes': limit,
        'choices': ['INCREASE_EXPLICIT_BYTE_BUDGET_WITHIN_LIMIT', 'DECOMPOSE_TASK_AT_AUTHORIZED_BOUNDARY'],
        'task_modified': False, 'content_summarized': False}
    raise exc


def assemble(req, view, reader):
    record = view['record']; limit = req['budget']['max_context_bytes']
    resolved = {c['question_id'] for c in record['clarifications']}
    if record['schema_version'] == 1 and any(q['blocking'] and q['id'] not in resolved for q in record['unresolved_questions']):
        fail('NEEDS_CLARIFICATION', 'A blocking question remains unresolved in the current TaskRecord')
    facts = {f['id']: f for f in record['facts']}
    requirements = {r['fact_id']: set(r['fields']) for r in record['stage']['required_facts']}
    for fid in req['required_fact_ids']: requirements.setdefault(fid, set()).add('value')
    maps = {'fact': facts, 'assumption': {a['id']: a for a in record['assumptions']},
            'result': {r['id']: r for r in record['checked_results']}}
    for kind, ids in [('fact', req['optional_fact_ids']), ('assumption', req['assumption_ids']), ('result', req['result_ids'])]:
        if not set(ids) <= maps[kind].keys(): fail('INSUFFICIENT_EVIDENCE', 'Selector names an unknown '+kind)
    if not requirements.keys() <= facts.keys(): fail('NEEDS_CLARIFICATION', 'Required fact absent; assumptions cannot fill it')
    payload = {'configuration': {'profile': view['ticket']['profile'], 'profile_ecid': view['ticket']['profile_ecid'],
        **deepcopy(view['ticket']['configuration'])},
        'task': {k: deepcopy(record[k]) for k in TASK_SPINE}, 'facts': [],
        'assumptions': [], 'checked_results': [], 'source_fields': [], 'sources': [],
        'experiences': [], 'evidence_slices': []}
    if record['schema_version'] == 2:
        # Explicit questions remain visible so a controller may ask instead of inventing an answer.
        # Exact evidence rights were checked by the scoped current-state owner.
        payload['task']['persistent_state'] = deepcopy(record['persistent_state'])
    omissions = []; included = {'fact': set(), 'assumption': set(), 'result': set(), 'experience': set()}

    def attach(target, ids):
        current = {s['id'] for s in target['sources']}
        for sid in sorted(set(ids)-current):
            reader.source(sid)  # verify the exact file, not merely a plausible reference
            target['sources'].append(deepcopy(reader.sources[sid]))
        target['sources'].sort(key=lambda s: s['id'])

    def add(key, item, source_ids, required, kind, id):
        nonlocal payload
        candidate = deepcopy(payload); attach(candidate, source_ids); candidate[key].append(item)
        size = byte_count(candidate)
        if size > limit:
            if required: _overflow(size, limit)
            omissions.append({'kind': kind, 'id': id, 'reason': 'BUDGET_EXHAUSTED'}); return False
        payload = candidate
        if kind in included: included[kind].add(id)
        return True

    spine_sources = [record['original_request']['source_id']] + [c['source_id'] for c in record['constraints']+record['clarifications']]
    if record['schema_version'] == 2:
        state = record['persistent_state']
        spine_sources += [ref['source_id'] for item in state['notes'] + state['annotations']
                          for ref in item['source_refs'] if ref['kind'] == 'TASK']
    attach(payload, spine_sources)
    if byte_count(payload) > limit: _overflow(byte_count(payload), limit)

    def resolved_fact(fid, needed):
        old = facts[fid]; exact = reader.source(old['source_id']).get(old['source_field'])
        if exact is None: fail('INSUFFICIENT_EVIDENCE', 'Exact source does not contain the fact field')
        for name in ('value', 'unit'):
            if old[name] is not None and old[name] != exact[name]:
                fail('CONSTRAINT_CONFLICT', 'Task fact contradicts its exact source field')
        if any(exact[k] is None for k in needed):
            fail('NEEDS_CLARIFICATION', 'Required value or unit is unknown in the exact source')
        out = deepcopy(old); out['rehydrated_fields'] = []
        for name in ('value', 'unit'):
            if old[name] is None and exact[name] is not None:
                out[name] = exact[name]; out['rehydrated_fields'].append(name)
        return out

    for fid in sorted(requirements):
        item = resolved_fact(fid, requirements[fid]); add('facts', item, [item['source_id']], True, 'fact', fid)
    for s in req['source_fields']:
        fields = reader.source(s['source_id'])
        if s['field_id'] not in fields: fail('INSUFFICIENT_EVIDENCE', 'Required source field is absent')
        add('source_fields', {'source_id': s['source_id'], 'field': deepcopy(fields[s['field_id']])},
            [s['source_id']], True, 'source', s['source_id'])

    # Explicitly requested evidence slices make their owning interpretation required.
    needed_experiences = {s['experience_id'] for s in req['evidence_slices']}
    ranked = []
    for c in sorted(req['experiences'], key=lambda c: (not (c['required'] or c['reference']['experience_id'] in needed_experiences),
                                                       -c['priority'], c['reference']['experience_id'])):
        ref = c['reference']; id = ref['experience_id']; required = c['required'] or id in needed_experiences
        try: ev = reader.experience(ref)
        except ContractError as e:
            if required or e.code not in ('TRAINING_RESTRICTED', 'RETENTION_RESTRICTED', 'CONFLICT_REQUIRES_REVIEW',
                                         'INSUFFICIENT_EVIDENCE', 'CONSTRAINT_CONFLICT', 'BUDGET_EXHAUSTED'):
                raise
            omissions.append({'kind': 'experience', 'id': id, 'reason': e.code}); continue
        score = sum(term in ev['statement']['text'].casefold() for term in req['query_terms'])
        if not required and req['query_terms'] and not score:
            omissions.append({'kind': 'experience', 'id': id, 'reason': 'IRRELEVANT'}); continue
        item = {k: deepcopy(ev[k]) for k in ('reference', 'statement', 'sources', 'review', 'permission', 'sensitivity')}
        item['authority'] = 'REVIEWED_INTERPRETATION_NOT_INSTRUCTION'
        if required: add('experiences', item, [], True, 'experience', id)
        else: ranked.append((-c['priority'], -score, id, item))
    refs = {c['reference']['experience_id']: c['reference'] for c in req['experiences']}
    for selector in req['evidence_slices']:
        add('evidence_slices', reader.slice(refs[selector['experience_id']], selector), [], True, 'source', selector['source_id'])

    for fid in req['optional_fact_ids']:
        if fid in included['fact']: continue  # a stage requirement takes precedence
        item = resolved_fact(fid, set()); add('facts', item, [item['source_id']], False, 'fact', fid)
    for kind, key, ids in [('assumption', 'assumptions', req['assumption_ids']), ('result', 'checked_results', req['result_ids'])]:
        for id in ids:
            item = deepcopy(maps[kind][id]); add(key, item, item['source_ids'], False, kind, id)
    for _, _, id, item in sorted(ranked): add('experiences', item, [], False, 'experience', id)
    for kind, key in [('fact','facts'),('assumption','assumptions'),('result','checked_results')]:
        omitted = {o['id'] for o in omissions if o['kind'] == kind}
        for item in record[key]:
            if item['id'] not in included[kind] and item['id'] not in omitted:
                omissions.append({'kind': kind, 'id': item['id'], 'reason': 'NOT_SELECTED'})
    selected_sources = {s['id'] for s in payload['sources']}
    for s in record['sources']:
        if s['id'] not in selected_sources: omissions.append({'kind':'source','id':s['id'],'reason':'NOT_SELECTED'})
    return payload, omissions
