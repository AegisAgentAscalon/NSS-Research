# StageHandoff001 — public contract and proof boundary

## Ownership
`task_records.py` owns portable-record validation and exact source completion.
`stage_handoff.py` owns the public stage operation boundary. `publication.py`
remains the single durable checkpoint/current-pointer/attempt owner.
No duplicate record database or current-profile pointer is introduced.

One current checkpoint exists per task. Calls are made by one execution runner;
there is no concurrent task scheduler, live GPU context or globally enforced
multi-worker activation rule in this experiment.

## Serialization
- `task_record.schema.json` v1: task ID, lineage, goal, original request, source
  descriptors/classes, facts, assumptions, unresolved questions, clarifications,
  labelled checked-results, user/policy constraints, mock receipts and stage.
- `task_stage.schema.json`: stage ID, mode WORK/CONTROL/EVALUATION, sealed flag,
  objective, required fact IDs/properties and requested output.
- `stage_handoff_request.schema.json` v1: EXACT source checkpoint SHA-256 and
  next-stage definition. New stages start unsealed and have a different ID from
  the immediate predecessor. Stage identity is checkpoint/revision scoped;
  stage labels are not globally unique across all time.
- `handoff_evidence.schema.json`: versioned explicit source fields. Only `value`
  and `unit` are supported. No natural-language extraction or general retrieval.
- Checkpoint schema v2 embeds `task_record`. Legacy v1 forbids it semantically.
- Attempt schema v2 binds `task_handoff={request,target_record}`. Legacy v1 does
  not accept that field. The existing source checkpoint hash binds the old record.

JSON schema shape validation PLUS `validate_task_record`, `validate_checkpoint`
and attempt/binding semantic validation are required. The JSON schemas alone do
not express every cross-field version or provenance rule. Unknown fields,
duplicate JSON keys, bool-as-int, dangling refs and duplicate IDs fail closed.
Maximum record size: 128 KiB serialized; at most 128 items per collection;
strings bounded by their schema; exact-source fixture files limited to 256 KiB.
These are functional input bounds, not hostile-input sandbox guarantees.
Canonical hashes use the existing sorted-key compact JSON `digest` function.

## Entry APIs

### initialize_task(bundle, store, ledger, *, record, input_artifact,
###                 authorized=False, core_profile="core")
Validate the supplied task record and verified mock receipts; require a declared
Core-only profile; execute the integer baseline and publish checkpoint v2.
Repeated identical initialization is idempotent. Different existing task state
is a conflict. Source content is admitted fixture data, not certified truth.

### handoff_stage(bundle, store, ledger, *, task_id, destination, attempt_id,
###               request, authorized=False, load_ok=True, crash_at=None)
Validate identifiers and exact source identity before interpreting the transition.
The source must be sealed. The destination must be one declared QAP, not a union
inferred from individually valid components, and its directed edge must exist.
CONTROL/EVALUATION require Core-only. All receipts must match the complete
verified local action set. Assumptions cannot fill required fact slots.

Resolve each required fact from its declared hashed local source field. Recheck
both existing value and unit for disagreement; only fill missing requested
properties, never overwrite an existing conflict. Unavailable sources return
INSUFFICIENT_EVIDENCE. Missing properties/blocking open questions return
NEEDS_CLARIFICATION. The record remains unchanged on these failures.

Bind the request and source-derived successor record in PREPARED. Use the existing
recovery operation to replay integer computation or apply a qualified same-input
reuse. Clear abandoned drafts. Publish record+profile+cache and PUBLISHED attempt
status in the same existing SQLite transaction. Revalidate on unpublished resume.

Fresh/retried operations revalidate simulated authorization; a PUBLISHED request
is a historical read, not activation. A retry with a changed request/target is a
conflict. `historical=True` means result.state is historical. Query
`store.current(task_id)` to inspect the active state.

### finish_stage(bundle, store, ledger, *, task_id, expected_checkpoint_hash,
###              new_results, new_receipts, authorized=False)
Seal an unsealed current stage through CAS. Append only new result/receipt entries;
retain all previous data and the exact stage definition. New result producer_ecid
must equal the current ECID. Record parent hash and revision advance. Receipts
must match actual mock-world evidence. A pending handoff blocks record revision.
This does not solve a task or independently certify a result: `check_ref` names
upstream fixture evidence and is not a released QualificationEvidence artifact.

## Result envelope
All coordinator methods return `status`, `state` (checkpoint or null), `attempt`
(record or null), `replayed` (boolean), `historical` (boolean), and `detail`.
SUCCESS does not mean a cognitive answer is correct; it means this software
operation met its local contract. Expected codes include VALIDATION_FAILED,
INCOMPATIBLE_CONFIGURATION, CONSTRAINT_CONFLICT, NEEDS_CLARIFICATION,
INSUFFICIENT_EVIDENCE, RECOVERY_REQUIRED, AUTHORIZATION_DENIED and INTERNAL_FAILURE.
Failure retains the current source when readable. Pre-prepare errors need not
create an attempt row. A transient pre-resume failure may leave an existing
PREPARED/STAGED attempt retryable. FAILED attempts require a new attempt ID.

## Invariants and forbidden calls
The accepted fixture artifacts remain unchanged. Profile changes preserve the
portable record and its provenance; only stage metadata/lineage and exact missing
fact properties change. CONTROL/EVALUATION never use an overlay profile.
Stage methods never call `Ledger.perform` or the private mock executor. Output
receipt labels refer to local marker effects, not a real UI delivery protocol.
TaskRecord claims/evaluator confidence never serve as authorization.
The public coordinator reads no database internals. Static Python imports are
checked by `tools/check_dependencies.py`; this is not whole-program verification.

## Failure / crash semantics
PREPARED, after-compute and STAGED crashes leave source profile AND source record
current. PUBLISHED observes both target checkpoint and committed attempt.
Resumption rechecks request, source hash, ECIDs, inputs, receipts, target load and
exact source-based record. Changed action sets or unknown receipts block it.
A qualified source->destination move does not imply the reverse. History cannot
reactivate itself. Missing/corrupt readable evidence returns typed failures at
new public coordinator endpoints. Privileged database rewriting, arbitrary
power loss, multiple live writers and remote side effects remain out of scope.

## Acceptance coverage (new lifecycle cases, not a blanket acceptance)
| Case | Software coverage | Remaining boundary |
|---|---|---|
| LT-01 | Core/A/AB fixtures; B dependency closure; unqualified unions denied; exact one-profile checkpoint; read-only B bytes do not activate it | No real hot/warm pager or concurrent scheduler |
| LT-02 | Source-backed value/unit completion; missing source/field and conflict outcomes; full portable sections retained | No learned language understanding or general semantic-preservation proof |
| LT-03 | AB->A clean integer equivalence; stale cache denied; crash windows; receipt preservation and no duplicate mock effects | No neural cache/latent migration or real outside-world guarantee |
| LT-14 | Mandatory Core-only; explicit directed edges; detect modified fixture Core bytes | No training-time immutability experiment or authenticated Core package |

Other lifecycle cases LT-04 through LT-13 remain unimplemented except incidental
mock output-receipt preservation. A stored checked result is not qualification.
The specification's claimed cognitive outcomes are still experimental targets.

## Next integration constraint
ECID identifies the configuration, not all state dependencies. Real neural
integration must also bind exact token/context/TaskRecord views to caches. This
integer simulator's cache depends only on numeric input artifacts and profile;
its same-profile reuse is not transferable evidence for a Transformer backend.
