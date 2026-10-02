"""Validated profiles and explicit configuration transitions, using immutable values."""
from dataclasses import dataclass, replace
from hashlib import sha256
import json

class ContractError(ValueError):
    def __init__(self, code, message):
        self.code = code
        super().__init__(message)

def fail(code, message):
    raise ContractError(code, message)

def digest(value):
    return sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

@dataclass(frozen=True)
class Overlay:
    id: str
    artifact_hash: str
    requires: tuple[str, ...] = ()
    excludes: tuple[str, ...] = ()

@dataclass(frozen=True)
class Profile:
    id: str
    overlays: tuple[str, ...]
    evidence_ref: str

@dataclass(frozen=True)
class Transition:
    source: str
    target: str
    mode: str  # reuse or replay; migration deliberately unsupported
    evidence_ref: str

@dataclass(frozen=True)
class Catalog:
    core_hash: str
    generation: str
    tokenizer: str
    context_abi: str
    overlay_abi: str
    runtime_version: str
    overlays: tuple[Overlay, ...]
    profiles: tuple[Profile, ...]
    transitions: tuple[Transition, ...]

    def __post_init__(self):
        required = (self.core_hash, self.generation, self.tokenizer,
                    self.context_abi, self.overlay_abi, self.runtime_version)
        if not all(required):
            fail("VALIDATION_FAILED", "Missing configuration identity")
        ov = {o.id: o for o in self.overlays}
        ps = {p.id: p for p in self.profiles}
        if len(ov) != len(self.overlays) or len(ps) != len(self.profiles):
            fail("VALIDATION_FAILED", "Duplicate overlay or profile ID")
        if not any(not p.overlays for p in self.profiles):
            fail("VALIDATION_FAILED", "Every generation requires a Core-only profile")
        for o in self.overlays:
            if not o.id or not o.artifact_hash or not set(o.requires + o.excludes) <= ov.keys():
                fail("VALIDATION_FAILED", "Invalid overlay metadata")
        for p in self.profiles:
            selected = set(p.overlays)
            if not p.id or not p.evidence_ref or len(selected) != len(p.overlays) or not selected <= ov.keys():
                fail("VALIDATION_FAILED", "Invalid profile metadata")
            for name in selected:
                if not set(ov[name].requires) <= selected or set(ov[name].excludes) & selected:
                    fail("INCOMPATIBLE_CONFIGURATION", "Dependency or exclusion violation")
        edges = set()
        for t in self.transitions:
            edge = (t.source, t.target)
            if edge in edges or t.source not in ps or t.target not in ps or not t.evidence_ref or t.mode not in ("reuse", "replay"):
                fail("VALIDATION_FAILED", "Invalid or duplicate transition")
            edges.add(edge)
            # Conservative base rule: changing active weights always requires replay.
            if t.mode == "reuse" and ps[t.source].overlays != ps[t.target].overlays:
                fail("INCOMPATIBLE_CONFIGURATION", "Changed active weights or execution order require replay")

    def profile(self, profile_id):
        for p in self.profiles:
            if p.id == profile_id:
                return p
        fail("INCOMPATIBLE_CONFIGURATION", "Unknown or unqualified profile")

    def ecid(self, profile_id):
        p = self.profile(profile_id)
        ov = {o.id: o for o in self.overlays}
        return digest({"schema": 1, "core": self.core_hash, "generation": self.generation,
            "profile": p.id, "ordered_artifacts": [(n, ov[n].artifact_hash) for n in p.overlays],
            "tokenizer": self.tokenizer, "context_abi": self.context_abi,
            "overlay_abi": self.overlay_abi, "runtime": self.runtime_version})

@dataclass(frozen=True)
class State:
    task_id: str
    profile: str
    ecid: str
    input_refs: tuple[str, ...]  # portable inputs, not old hidden-state checkpoints
    cache: tuple[str, ...] = ()
    draft: str = ""
    committed_action_ids: tuple[str, ...] = ()
    uncertain_action_ids: tuple[str, ...] = ()

@dataclass(frozen=True)
class Result:
    status: str
    state: State
    replay_required: bool = False
    detail: str = ""

def transition(catalog, state, target, *, authorized=False, load_ok=True):
    """Pure simulation. Failures return original state; no I/O or action execution."""
    try:
        if state.ecid != catalog.ecid(state.profile):
            fail("INCOMPATIBLE_CONFIGURATION", "State ECID does not match source")
        target_ecid = catalog.ecid(target)
        if not authorized:
            fail("AUTHORIZATION_DENIED", "Explicit simulated authorization required")
        edge = next((t for t in catalog.transitions if (t.source, t.target) == (state.profile, target)), None)
        if edge is None:
            fail("INCOMPATIBLE_CONFIGURATION", "No qualified directed transition")
        if edge.mode == "replay" and state.uncertain_action_ids:
            fail("RECOVERY_REQUIRED", "Reconcile uncertain actions before replay")
        if edge.mode == "replay" and not state.input_refs:
            fail("RECOVERY_REQUIRED", "Portable replay inputs unavailable")
        if not load_ok:
            fail("INTERNAL_FAILURE", "Simulated load failed; original state retained")
        changes = {"profile": target, "ecid": target_ecid}
        if edge.mode == "replay":
            changes.update(cache=(), draft="")
        return Result("SUCCESS", replace(state, **changes), edge.mode == "replay")
    except ContractError as e:
        return Result(e.code, state, detail=str(e))

def action_disposition(state, action_id):
    """Advisory only. Never executes an action or claims exactly-once delivery."""
    if action_id in state.uncertain_action_ids:
        return "RECONCILE"
    if action_id in state.committed_action_ids:
        return "SKIP_COMMITTED"
    return "REQUIRES_AUTHORIZED_EXECUTOR"
