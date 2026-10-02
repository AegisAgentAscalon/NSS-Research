"""Installed configuration-neutral view adapter; no task state or archive of its own."""
from pathlib import Path
from .runtime import fail


class FoundationContextSource:
    def __init__(self, generations, *, evidence_root):
        from .generation_store import Generations
        if type(generations) is not Generations:
            fail('VALIDATION_FAILED', 'Use the existing Generations owner')
        generations.foundation_snapshot()  # Reject legacy stores explicitly.
        self.generations = generations
        self.inputs = {'evidence_root': Path(evidence_root).resolve()}

    def read_context(self, req, *, archive=None):
        if req['schema_version'] != 3:
            fail('INCOMPATIBLE_CONFIGURATION', 'Current roles require context request v3')
        info = self.generations.foundation_snapshot()
        if req['store_id'] != info['store_id'] or req['expected_configuration_sha256'] != info['current']['generation_sha256']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Context owner/configuration differs')
        v = self.generations.foundation_read(req['task_id'], caller_id=req['caller_id'],
            owner_scope=req['state_scope'], evidence_root=self.inputs['evidence_root'], archive=archive,
            expected_record_sha256=req['expected_record_sha256'])
        if v['task_state_identity'] != req['expected_task_state_identity']:
            fail('INCOMPATIBLE_CONFIGURATION', 'Context is stale after state or execution progress')
        return v
