# StageHandoff001 implementation packet

## Scope and authority
Primary flow: `working_ar` in reviewed schema-v2 Logic Atlas. This is portable
working-state software; no learned AR controller is implemented. Adjacent
`overlay_runtime` / `checkpoint_recovery` remain the existing single-runner
integer simulator and are extended only to carry a bound task record.
The user authorized system-by-system construction following the v0.6 handoff.
Start from the actual reviewed 0.4.1 source. Later 0.6.0 notes are NOT source.
Qualification evidence and real Nexus authorization remain deferred. Booleans
and named fixture evidence are simulation inputs, not production permission.

## Owned boundary
`task_records.py`: TaskRecord schema semantics, exact source-backed completion,
readiness and immutable successor-record construction. No SQL, action execution,
neural code, training, or deployment authority.
`stage_handoff.py`: small coordinator using public RecoveryStore and recovery APIs.
`publication.py`: sole persistent checkpoint/current-pointer/attempt owner.
One checkpoint per task has ONE profile and ECID. There is no second current
pointer for records. TaskRecord is embedded in checkpoint schema v2, so record,
profile, cache and attempt publish in the same existing SQLite transaction.
Legacy checkpoint/attempt v1 retains original shape and behavior.

## Concrete types
TaskRecord: version, task_id, revision, parent_hash, goal, original_request,
sources, facts, assumptions, unresolved_questions, clarifications,
checked_results, constraints, receipts, stage.
Stage: id, mode WORK|CONTROL|EVALUATION, sealed flag, objective,
required_facts (fact_id + value/unit fields), requested_output.
HandoffRequest: version, exact source_checkpoint_hash, next_stage (unsealed).
Receipts bind mock-ledger key + kind + receipt digest. They are not permission.
Current ECID remains in the checkpoint, not repeated mutable active-state fields.
Result: status, readable state or None, replayed, detail, attempt, historical.

## Flow and gates
Validate exact request/source/task -> verify source checkpoint and sealed boundary
-> require a declared target profile and directed edge (including stays/Q0)
-> fresh simulated authorization and load readiness -> validate ALL task actions
and EXACT record receipts -> validate destination required facts; at most one
exact local source lookup per source ID per attempt -> reject missing/conflicting
facts or unresolved blocking questions -> build target TaskRecord revision
-> bind request+target record in PREPARED -> replay only integer computation
-> STAGED -> atomically publish checkpoint+record+PUBLISHED.
Resume revalidates authority, source inputs, target profile and handoff binding.
History reads return historical=True and do not reactivate an old profile.
Any failed unpublished transition leaves the source current. A transition request
is not allowed to silently mutate its target on retry.

## Task progression
Initialize one task from a Core-only fixture checkpoint and supplied record.
Finish a READY stage via a CAS-protected record-only checkpoint revision; append
explicit checked-result records, require their producer_ecid to match current.
Finishing does not certify the truth of results: check_ref is an upstream fixture
reference. No new facts/permissions/identity claims are invented. A later memory
curation pass owns correction policies. Existing record content stays intact.
An in-flight recovery blocks task revision. Core control/evaluation stages must
use a Core-only profile; no live candidate evaluation is claimed.

## Invariants
* Accepted Core/overlay artifact bytes never change.
* No arbitrary profile unions or implicit reverse transitions.
* Configuration changes reject old caches and clear unfinished drafts.
* Goals, assumptions, constraints, clarifications, unresolved issues, results and
  receipts survive handoff; only missing fact values/units may be filled from an
  exact hashed source, and existing values must agree.
* Never execute an action or redeliver output in a handoff; UNCERTAIN blocks it.
* Hashes are integrity identifiers, not authentication.
* Bounded records/requirements/source reads; no open-ended retry loop.

## Failure outcomes
VALIDATION_FAILED: shape/version/identity/hash/source conflict; retain source.
INCOMPATIBLE_CONFIGURATION: stale request, invalid profile/edge/core-only target.
CONSTRAINT_CONFLICT: stage/request reuse, evidence disagreement, already sealed.
NEEDS_CLARIFICATION: blocking issue or missing required source field; no guessing.
INSUFFICIENT_EVIDENCE: unavailable/hash-mismatched source data; retain source.
RECOVERY_REQUIRED: unresolved/mismatched action evidence or missing durable state.
AUTHORIZATION_DENIED / INTERNAL_FAILURE: simulation denial/load/storage failure.
Unknown physical storage failures are bounded at new public coordinator endpoints;
there is no power-loss, multi-runner, hostile-tamper or real exactly-once claim.

## Tests to write before implementation
Round-trip/unknown/duplicate fields; bool-as-int; dangling refs; duplicate IDs;
bounded strings/arrays; wrong record task; source mutation; source tampering;
missing unit retrieved exactly / source absent / contradictory values / missing
field / unresolved blocker; no assumptions promoted into facts; receipt omission,
substitution, UNCERTAIN and already-presented output; qualified core/A/AB including
B requires A, reject B/union; AB->A replay equivalence; A->Core-only control; reject
control under A; direct/implicit reverse denied; no-op/stay revalidates; exact
request retry/historical no-reactivation; changed inputs/receipt set fail resume;
PREPARED/compute/STAGED/PUBLISHED child-process crash windows; staged record
substitution/missing DB; stage finish CAS/history; tests prove imports stay bounded.

## Optimization and non-goals
Reuse Bundle, strict JSON validator, Ledger and RecoveryStore. Do not fork a
second state store or write a general workflow engine. Caching source reads is
per single validation call only. No neural training, curation automation, new
Nexus implementation, generic Aegis Runtime, background service, networking,
large dependencies, memory archive or broad Context Manager.

## Done gate
Full reviewed tests retained; new tests and demos pass from clean extraction;
25-flow atlas validates; generated Markdown reconciled; public API and failure
semantics documented; evidence and next steps packaged with a source manifest.
