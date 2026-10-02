"""Current-use source checks for symbolic state, through existing evidence owners.

Local fixture paths are admitted with the task, not a general filesystem API.
Archive references use exact revisions and purpose='retrieval'. Point-in-time
checks are not a cross-database lease or a mechanism for recalling exported text.
"""
from .experience_store import ExperienceArchive
from .neural_contracts import fingerprint
from .runtime import fail
from .state_contracts import source_ref
from .context_plan import EvidenceReader, unwrap
from .context_contracts import MAX_EVIDENCE_BYTES



class StateEvidence:
    """Operation-local reads only. Never persists authority or writes sources."""
    def __init__(self, record, root, archive):
        self.record = record; self.root = root; self.archive = archive; self.cache = {}
        self.reader = EvidenceReader(root, archive, record, MAX_EVIDENCE_BYTES)
        state = record['persistent_state']; binding = state['archive_binding']
        if binding is not None:
            if type(archive) is not ExperienceArchive:
                fail('INSUFFICIENT_EVIDENCE', 'Pinned experience owner is unavailable')
            if unwrap(archive.binding()) != binding:
                fail('INCOMPATIBLE_CONFIGURATION', 'State pins a different experience archive')
        self.has_archive = binding is not None

    def read(self, ref):
        source_ref(ref); key = fingerprint(ref)
        if key in self.cache: return self.cache[key]
        if ref['kind'] == 'TASK':
            source = next((s for s in self.record['sources'] if s['id'] == ref['source_id']), None)
            if source is None: fail('INSUFFICIENT_EVIDENCE', 'State references a source not admitted by the task')
            field = self.reader.source(ref['source_id']).get(ref['field_id'])
            if field is None: fail('INSUFFICIENT_EVIDENCE', 'Exact state source field is unavailable')
            result = {'kind': 'TASK', 'source': source, 'field': field}
        else:
            if not self.has_archive: fail('INSUFFICIENT_EVIDENCE', 'No experience owner admitted for state')
            v = self.reader.experience(ref['reference'])
            result = {'kind': 'EXPERIENCE', 'view': v}
        self.cache[key] = result
        return result


def check_state_sources(record, *, root, archive, at):
    if record['schema_version'] == 1: return
    reader = StateEvidence(record, root, archive)
    state = record['persistent_state']
    # Every admitted source pointer remains resolvable, even on initial binding.
    # The shared reader enforces a bounded per-operation evidence byte budget.
    for src in record['sources']: reader.reader.source(src['id'])
    for item in state['annotations'] + state['notes']:
        if item.get('expires_at') is not None and item['expires_at'] <= at:
            fail('RECOVERY_REQUIRED', 'Optional state note expired; commit reviewed EXPIRE_NOTE before reuse')
        values = [reader.read(ref) for ref in item['source_refs']]
        if item.get('identity_sensitive') and not any(v['kind'] == 'EXPERIENCE' and
                v['view']['sensitivity'] == 'IDENTITY_SENSITIVE' for v in values):
            fail('CONFLICT_REQUIRES_REVIEW', 'Identity interpretation needs an approved identity-sensitive archive record')
        if item.get('status') == 'USER_STATED' and not any(v['kind'] == 'TASK' and
                v['source']['kind'] == 'user' for v in values):
            fail('VALIDATION_FAILED', 'USER_STATED label needs an admitted user source')
        if item.get('status') == 'TEST_VERIFIED' and not any(v['kind'] == 'TASK' and
                v['source']['kind'] == 'tool' for v in values):
            fail('VALIDATION_FAILED', 'TEST_VERIFIED label requires a declared tool-result source; human reviews its meaning')


def check_delta_sources(record, c, *, root, archive):
    reader = StateEvidence(record, root, archive)
    for op in c.get('deltas', []):
        values = [reader.read(r) for r in op['source_refs']]
        if op['op'] == 'RESOLVE_QUESTION':
            v = next(v for v in values if v['kind'] == 'TASK')
            if v['source']['kind'] != 'user' or v['field']['value'] != op['answer']:
                fail('CONSTRAINT_CONFLICT', 'Clarification must match exact admitted user-source text')
