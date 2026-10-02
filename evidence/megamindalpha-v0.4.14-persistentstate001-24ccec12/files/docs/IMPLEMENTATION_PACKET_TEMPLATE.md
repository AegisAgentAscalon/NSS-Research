# Subsystem implementation packet template

Use this template immediately before implementing any subsystem from `spec/logic_atlas.json`.

## 1. Identity
- Subsystem ID:
- Owner module/package:
- Atlas flow ID/version:
- Adjacent public contracts:

## 2. Typed boundary
- Input types + validation:
- Output/result types:
- Persistent state owned:
- State explicitly *not* owned:

## 3. State machine
- Start state:
- Decision table:
- Success terminal(s):
- Failure terminal(s):
- Retry/replay states:
- Atomic publication point, if any:

## 4. Dependencies
- Allowed imports/calls:
- Forbidden imports/calls:
- Events/requests emitted:

## 5. Preconditions / postconditions / invariants
Copy directly from the canonical contract/atlas, then specialize only where implementation requires more precision.

## 6. Failure and rollback
For each typed failure:
- stimulus,
- returned outcome,
- state retained,
- durable evidence written,
- replay/retry eligibility.

## 7. Tests before implementation
Write expected tests first:
- happy path,
- each decision branch,
- each typed failure,
- stale/corrupt state,
- rollback/source-retention,
- forbidden-edge regression,
- deterministic equivalence where applicable.

## 8. Compression pass
Only after tests pass:
- duplicate guards to factor,
- lookup tables to precompute,
- payloads to replace with immutable refs,
- redundant serialization/model passes to eliminate,
- branches that can be data-driven.

## 9. Definition of Done
- Atlas flow still matches implementation.
- Public API documented.
- All tests pass.
- No forbidden dependency edge.
- Failure paths retain last-known-good state.
- Version/provenance updated.
- Flowchart/pseudocode changed if code behavior changed.
