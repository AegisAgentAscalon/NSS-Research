"""Experiment 001A: exact integer computation, stale-cache rejection, and replay."""
from copy import deepcopy
from dataclasses import dataclass

from .runtime import ContractError, fail
from .serialization import validate
from .task_records import validate_checkpoint, validate_handoff_binding


def execute(bundle, profile, inputs):
    validate(inputs, "inputs.schema.json")
    values = list(inputs["values"])
    for operation in bundle.operations(profile):
        values = [x * operation["multiply"] + operation["add"] for x in values]
    return values


def checkpoint(bundle, profile, task_id, input_artifact):
    validate(input_artifact, "artifact.schema.json")
    inputs = bundle.artifact(input_artifact, "inputs.schema.json")
    value = dict(schema_version=1, task_id=task_id, profile=profile,
        ecid=bundle.ecid(profile), input_artifact=deepcopy(input_artifact),
        cache=execute(bundle, profile, inputs), draft="unfinished segment")
    return validate_checkpoint(value)


def accept_cache(bundle, state, profile):
    validate_checkpoint(state)
    if state["profile"] != profile or state["ecid"] != bundle.ecid(profile):
        fail("INCOMPATIBLE_CONFIGURATION", "Stale cached state rejected")
    expected = execute(bundle, profile, bundle.artifact(state["input_artifact"], "inputs.schema.json"))
    if state["cache"] != expected:
        fail("VALIDATION_FAILED", "Cache content does not match portable inputs")
    return list(state["cache"])


@dataclass(frozen=True)
class RecoveryResult:
    status: str
    state: dict
    replayed: bool = False
    detail: str = ""


def recover(bundle, state, destination, ledger, *, authorized=False, load_ok=True, task_handoff=None):
    """Commit no new state unless checks and replay succeed; source is unchanged."""
    try:
        validate_checkpoint(state)
        accept_cache(bundle, state, state["profile"])
        edge = bundle.edge(state["profile"], destination)
        if not authorized:
            fail("AUTHORIZATION_DENIED", "Simulated authorization not supplied")
        # Both reuse and replay are blocked by unresolved effects for this task.
        ledger.ensure_replay_safe(state["task_id"])
        if not load_ok:
            fail("INTERNAL_FAILURE", "Simulated load failure: retain source configuration")
        if state['schema_version'] == 2:
            validate_handoff_binding(state, task_handoff)
        elif task_handoff is not None:
            fail('VALIDATION_FAILED', 'Legacy checkpoint cannot accept a task handoff')
        replay = edge["replay_required"]
        if replay:
            updated = checkpoint(bundle, destination, state["task_id"], state["input_artifact"])
            updated["draft"] = ""  # Never carry an abandoned output segment forward.
        else:
            updated = deepcopy(state)
            updated.update(profile=destination, ecid=bundle.ecid(destination))
        if task_handoff is not None:
            updated.update(schema_version=2, task_record=deepcopy(task_handoff['target_record']), draft='')
            validate_checkpoint(updated)
        return RecoveryResult("SUCCESS", updated, replay)
    except ContractError as e:
        return RecoveryResult(e.code, state, detail=str(e))
