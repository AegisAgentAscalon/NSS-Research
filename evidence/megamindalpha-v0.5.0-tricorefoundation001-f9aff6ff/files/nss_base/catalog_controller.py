"""Public deterministic controller; the generation manager owns all durable state.

This facade binds local dependencies once. It cannot issue qualification, release,
replay, or Aegis Runtime permits; no direct SQL, neural execution or effect callback.
"""
from copy import deepcopy
from .catalog_contracts import descriptor
from .generation_store import Generations
from .ledger import Ledger
from .neural_contracts import encoded, fingerprint
from .runtime import fail


class CatalogController:
    def __init__(self, generations, *, qualifications, source, ledger, evidence_root, archive=None):
        if type(generations) is not Generations or type(ledger) is not Ledger:
            fail('VALIDATION_FAILED', 'Installed generation and ledger owners required')
        self.generations = generations
        self.evidence = {'qualifications': qualifications, 'source': source}
        self.inputs = {'ledger': ledger, 'evidence_root': evidence_root}
        self.archive = archive  # Optional existing evidence owner, never a second state store.

    def register(self, value, *, reviewer_id):
        return self.generations.register_catalog(value, reviewer_id=reviewer_id, **self.evidence)

    def catalog(self, *, expected_current, catalog_sha256=None):
        return self.generations.describe_catalog(expected_current=expected_current,
            catalog_sha256=catalog_sha256, **self.evidence)

    def select(self, request, *, caller_id, source_ticket=None, expected_record_sha256=None, scope=None):
        return self.generations.select_stage(request, caller_id=caller_id,
            source_ticket=source_ticket, expected_record_sha256=expected_record_sha256, scope=scope, **self.evidence)

    def apply(self, command, *, fault_at=None):
        return self.generations.task_operation(command, fault_at=fault_at, archive=self.archive, **self.inputs, **self.evidence)

    def read(self, ticket, *, caller_id, expected_record_sha256, scope=None):
        return self.generations.read_task_stage(ticket, caller_id=caller_id,
            expected_record_sha256=expected_record_sha256, scope=scope, archive=self.archive, **self.inputs, **self.evidence)

    def inspect(self, task_id, *, caller_id=None, scope=None):
        return self.generations.inspect_task(task_id, caller_id=caller_id, scope=scope)

    def state_history(self, task_id, *, caller_id, scope):
        return self.generations.inspect_state_history(task_id, caller_id=caller_id, scope=scope)


def fixture_descriptor(g, artifacts, *, catalog_id, author_id, declarations):
    """Build (NOT review/authorize) declared capabilities/costs around exact bytes.

    Caller supplies every profile's labels, load/step units and max input pairs.
    The exact serialized document size is computed, not a memory measurement.
    """
    from .catalog_contracts import FORMAT, POLICY
    if type(declarations) is not dict or set(declarations) != {p['id'] for p in g['profiles']}:
        fail('VALIDATION_FAILED', 'Provide a declaration for each exact profile')
    profiles = []
    for p in sorted(g['profiles'], key=lambda v: v['id']):
        item = deepcopy(declarations[p['id']])
        if type(item) is not dict or set(item) != {'capabilities', 'load_units', 'step_units', 'max_pairs'}:
            fail('VALIDATION_FAILED', 'Invalid profile declaration')
        profiles.append({'id': p['id'], 'ecid': p['ecid'], **item,
            'sealed_document_bytes': sum(len(encoded(artifacts[k])) for k in ['core'] + p['members'])})
    return descriptor({'schema_version': 1, 'format': FORMAT, 'policy': POLICY,
        'catalog_id': catalog_id, 'generation_sha256': fingerprint(g), 'author_id': author_id,
        'claim_scope': 'REVIEWED_ROUTING_FIXTURE_NOT_NEW_NEURAL_EVIDENCE', 'profiles': profiles}, g)
