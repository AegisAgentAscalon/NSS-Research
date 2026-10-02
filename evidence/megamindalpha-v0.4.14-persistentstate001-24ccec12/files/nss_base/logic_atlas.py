"""Machine-readable NSS pseudocode flow atlas validator and metrics.

This module validates the *specification graph*. It does not execute NSS subsystems
and does not prove any neural, governance, or side-effect behavior.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
from .serialization import read_json

from .runtime import ContractError, fail

SPEC_PATH = Path(__file__).resolve().parents[1] / "spec" / "logic_atlas.json"


@dataclass(frozen=True)
class FlowMetrics:
    nodes: int
    transitions: int
    decisions: int
    terminals: int
    cyclomatic_complexity: int


def load_atlas(path: str | Path = SPEC_PATH) -> dict:
    path = Path(path)
    try:
        data = read_json(path)
    except (OSError, json.JSONDecodeError) as exc:
        fail("VALIDATION_FAILED", f"Could not load logic atlas: {exc}")
    validate_atlas(data)
    return data


def _reachable(start: str, adjacency: dict[str, set[str]]) -> set[str]:
    seen: set[str] = set()
    stack = [start]
    while stack:
        current = stack.pop()
        if current in seen:
            continue
        seen.add(current)
        stack.extend(adjacency.get(current, ()))
    return seen


def _strings(value, label, *, empty=False):
    if not isinstance(value, list) or (not value and not empty) or not all(type(x) is str and x.strip() for x in value):
        fail("VALIDATION_FAILED", f"Invalid {label}")


def _identifier(value):
    return type(value) is str and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*", value) is not None


def validate_atlas(atlas: dict) -> None:
    fields = {"schema_version", "title", "purpose", "global_outcomes", "shared_primitives", "flows", "global_rules"}
    if type(atlas) is not dict or set(atlas) != fields or type(atlas["schema_version"]) is not int or atlas["schema_version"] != 2:
        fail("VALIDATION_FAILED", "Unsupported atlas shape/version")
    for name in ("title", "purpose"):
        if type(atlas[name]) is not str or not atlas[name].strip():
            fail("VALIDATION_FAILED", "Invalid atlas metadata")
    _strings(atlas["global_rules"], "global rules")
    outcomes = atlas["global_outcomes"]
    _strings(outcomes, "outcomes")
    if len(outcomes) != len(set(outcomes)) or "SUCCESS" not in outcomes:
        fail("VALIDATION_FAILED", "Invalid outcome registry")
    primitives = atlas["shared_primitives"]
    if type(primitives) is not dict or not primitives or not all(_identifier(k) and type(v) is str and v.strip() for k,v in primitives.items()):
        fail("VALIDATION_FAILED", "Invalid primitive registry")
    flows = atlas["flows"]
    if type(flows) is not list or not flows or not all(type(f) is dict for f in flows):
        fail("VALIDATION_FAILED", "Invalid flow collection")
    ids = [f.get("id") for f in flows]
    if not all(_identifier(x) for x in ids) or len(ids) != len(set(ids)):
        fail("VALIDATION_FAILED", "Duplicate or invalid flow id")
    for flow in flows:
        _validate_flow(flow, set(outcomes), set(primitives))


def _validate_flow(flow, outcomes, primitives):
    required = {"id", "title", "owner", "purpose", "status", "implementation", "inputs", "outputs",
                "nodes", "transitions", "terminals", "failure_codes", "forbidden_edges",
                "invariants", "pseudocode", "uses_primitives", "optimization_notes"}
    if set(flow) != required:
        fail("VALIDATION_FAILED", "Flow fields mismatch")
    for k in ("title", "owner", "purpose", "status"):
        if type(flow[k]) is not str or not flow[k].strip():
            fail("VALIDATION_FAILED", "Invalid flow metadata")
    if flow["implementation"] not in ("design-only", "partial-simulator"):
        fail("VALIDATION_FAILED", "Unknown implementation status")
    for key in ("inputs", "outputs", "failure_codes", "forbidden_edges", "invariants", "pseudocode", "uses_primitives", "optimization_notes"):
        _strings(flow[key], key, empty=key == "failure_codes")
    failures = set(flow["failure_codes"])
    if not failures <= outcomes or "SUCCESS" in failures:
        fail("VALIDATION_FAILED", "Unknown or successful failure code")
    if not set(flow["uses_primitives"]) <= primitives:
        fail("VALIDATION_FAILED", "Unknown primitive")
    # Literal registered outcomes in pseudocode must be declared by this flow.
    used = set(re.findall(r"\b[A-Z][A-Z_]+\b", "\n".join(flow["pseudocode"]))) & outcomes
    if not used <= failures | {"SUCCESS"}:
        fail("VALIDATION_FAILED", "Pseudocode uses undeclared outcome")
    nodes, edges, terminals = flow["nodes"], flow["transitions"], flow["terminals"]
    if type(nodes) is not list or not nodes or not all(type(n) is dict for n in nodes):
        fail("VALIDATION_FAILED", "Invalid nodes")
    kinds = {}
    for n in nodes:
        if set(n) != {"id", "label", "kind"} or not _identifier(n["id"]) or type(n["label"]) is not str or not n["label"].strip():
            fail("VALIDATION_FAILED", "Invalid node shape")
        if type(n["kind"]) is not str or n["kind"] not in {"start","process","decision","success","failure"} or n["id"] in kinds:
            fail("VALIDATION_FAILED", "Duplicate node or invalid kind")
        kinds[n["id"]] = n["kind"]
    starts = [n for n,k in kinds.items() if k == "start"]
    if len(starts) != 1:
        fail("VALIDATION_FAILED", "Exactly one start required")
    expected = {n for n,k in kinds.items() if k in ("success", "failure")}
    if type(terminals) is not dict or not terminals or set(terminals) != expected:
        fail("VALIDATION_FAILED", "Every terminal kind needs exactly one mapping")
    for node, codes in terminals.items():
        _strings(codes, "terminal outcome set")
        if len(set(codes)) != len(codes):
            fail("VALIDATION_FAILED", "Duplicate terminal outcome")
        if kinds[node] == "success" and codes != ["SUCCESS"]:
            fail("VALIDATION_FAILED", "Success terminal must return SUCCESS")
        if kinds[node] == "failure" and (not set(codes) <= failures or "SUCCESS" in codes):
            fail("VALIDATION_FAILED", "Failure terminal must preserve a declared non-success code")
    adjacency = {n:set() for n in kinds}
    reverse = {n:set() for n in kinds}
    conditions = {n:set() for n in kinds}
    if type(edges) is not list:
        fail("VALIDATION_FAILED", "Invalid transitions")
    for e in edges:
        if type(e) is not dict or set(e) != {"from", "to", "when"} or not all(type(e[k]) is str for k in e):
            fail("VALIDATION_FAILED", "Invalid edge shape")
        a,b,when = e["from"],e["to"],e["when"]
        if a not in kinds or b not in kinds or not when.strip() or a in terminals or when in conditions[a]:
            fail("VALIDATION_FAILED", "Invalid/duplicate edge or terminal exit")
        adjacency[a].add(b); reverse[b].add(a); conditions[a].add(when)
    if _reachable(starts[0], adjacency) != set(kinds):
        fail("VALIDATION_FAILED", "Unreachable graph nodes")
    can_exit = set()
    for terminal in terminals:
        can_exit |= _reachable(terminal, reverse)
    if can_exit != set(kinds):
        fail("VALIDATION_FAILED", "Closed cycle cannot reach any terminal")
    for node, kind in kinds.items():
        if node in terminals: continue
        if not conditions[node] or (kind == "decision" and len(conditions[node]) < 2):
            fail("VALIDATION_FAILED", "Missing node/decision exit")
        if len(conditions[node]) > 1 and "always" in conditions[node]:
            fail("VALIDATION_FAILED", "Unconditional edge conflicts with conditional exit")


def flow_metrics(flow: dict) -> FlowMetrics:
    nodes = len(flow["nodes"])
    edges = len(flow["transitions"])
    decisions = sum(1 for n in flow["nodes"] if n["kind"] == "decision")
    terminals = len(flow["terminals"])
    # Add one virtual exit and an edge from every terminal: E - N + T + 1.
    # Structural path count, not a complexity upper bound for implementations.
    cyclomatic = edges - nodes + terminals + 1
    return FlowMetrics(nodes, edges, decisions, terminals, cyclomatic)


def metrics_table(atlas: dict) -> list[tuple[str, FlowMetrics]]:
    validate_atlas(atlas)
    return [(flow["id"], flow_metrics(flow)) for flow in atlas["flows"]]


def get_flow(atlas: dict, flow_id: str) -> dict:
    for flow in atlas["flows"]:
        if flow["id"] == flow_id:
            return flow
    fail("VALIDATION_FAILED", f"Unknown logic flow {flow_id}")


def main() -> int:
    atlas = load_atlas()
    print(f"{atlas['title']} — {len(atlas['flows'])} flows")
    for flow_id, m in metrics_table(atlas):
        print(f"{flow_id:24s} nodes={m.nodes:2d} edges={m.transitions:2d} decisions={m.decisions:2d} terminals={m.terminals:2d} normalized_complexity={m.cyclomatic_complexity}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
