# PersistentState001 — implementation contract / v0.4.14

## Scope and source
Implements Stage A / §23 of the **Fly-Inspired Persistent State & Adaptive Learning
Addendum v0.2 (12 September 2026)** using the v0.4.13 cumulative source checkpoint.
The original addendum and official architecture documents remain unchanged. This is
symbolic state S, not neural h, eligibility E, adaptive W, or production learning.

The source requires review for consequential and identity-sensitive updates. The initial
installed policy deliberately requires separate review for **all** new state deltas;
this avoids pretending a reliable automatic sensitivity classifier already exists.

## Ownership and public interfaces
`Generations` remains the only journal/current-head owner. Its CATALOG_TASK transaction
stores the exact command, reviewed receipt, next TaskRecord and task-head change together.
`CatalogController` is a facade. `state_contracts` validates schemas and local reviews;
`state_updates` is a pure reducer; `state_sources` delegates source access to the existing
`EvidenceReader` and ExperienceArchive public retrieval APIs. None owns another database.

- `state_contracts.prepare(view, operation_id=..., proposer_id=..., proposer_version=...,
  state_scope=..., policy=.../deltas=..., archive_binding=...)` creates an unapproved proposal.
- `state_contracts.attest(proposal, reviewer_id=..., reviewed_at=..., expires_at=..., reason=...)`
  creates a declaration. Only owner commit checks its role, exact contents and expiry.
- `CatalogController.apply(command)` validates and commits or raises a typed ContractError.
- `read(ticket, caller_id=..., expected_record_sha256=..., scope=...)` is checked current use.
- `inspect(task_id, caller_id=..., scope=...)` / `state_history(...)` are local historical
  inspection. They do not restore source permission or re-open a closed stage.

State admission and updates require OPERATOR caller, current running/unsealed stage,
exact revision + hash + producing profile ECID, and a different declared REVIEWER.
The reviewer must differ from both proposer and executor. Approval binds the full command
except the review envelope itself; validity is at most one hour. Labels are NOT authentication.

## Record and migration contract
Legacy TaskRecord v1 and its schema stay unchanged. A fresh legacy task can still run as
before. `BIND_STATE` records explicit agent/project/session attribution on a running task,
creating v2 at the next revision with the old hash as parent. No guessing attribution for
historical tasks. Already bound records cannot be rebound; closed tasks cannot be reopened.
A new session uses a new task admission and fresh source checks, not an old live ticket.
A process restart may resume the SAME still-valid session/task/configuration.

TaskRecord v2 contains `persistent_state` with `scope`, `policy`, optional exact archive
binding, latest committed state event, attributed notes and change annotations. The policy
pins a declared instruction-policy digest and canonical record-byte cap (1,024–131,072).
The digest is a reference, not proof of a verified instruction file or neural obedience.

Permitted state operations:

| Operation | Effect and restriction |
|---|---|
| SET_GOAL | Changes current goal, never the original request or protected constraints. |
| ADD_QUESTION | Adds an unresolved question with explicit blocking flag and exact sources. |
| RESOLVE_QUESTION | Records an answer that exactly matches one admitted user-source field. Not model self-clarification. |
| DEFER_QUESTION | Explicit reviewed reason makes the question nonblocking; no answer is invented. |
| ADD_NOTE | Adds a new attributed CLAIM/PROGRESS note; duplicate ID cannot overwrite it. |
| RETIRE_NOTE | Removes from current state with a reviewed reason; historical revision remains. |
| EXPIRE_NOTE | Same explicit removal, but only once its declared expiry has been reached. |

Each record admits at most 128 notes and 128 change annotations. A reviewed event
admits at most 256 distinct target operations, so clearing the full set of expired
notes is expressible without an intermediate state that still fails current-use
validation. Complete record/evidence byte budgets still apply. These are initial
implementation limits, not biological or model-capacity claims.

No JSON Patch or whole-record generated replacement. Scope, Core/QAP/ECID, sources,
rights, instruction-policy reference, budgets, model parameters and action receipts cannot
be edited through these operations. One target may be changed once per event; multiple
independent changes can commit as one bounded event. Exact earlier deltas remain in history.

Notes distinguish UNKNOWN, HYPOTHESIS, USER_STATED and TEST_VERIFIED. `confidence` is
null in S1: no calibrated numeric confidence is implemented. USER_STATED requires an
admitted user source; TEST_VERIFIED requires a declared tool-result source plus review.
Neither label is an automatic semantic proof. Author ID/version and reviewing identity
are preserved. Identity-sensitive notes require an exact approved identity-sensitive
archive record; subsequent challenge/supersession/permission withdrawal blocks current use.
Sensitivity flags rely on the proposer/reviewer; there is no automatic semantic classifier.

## Sources, permissions and data-channel boundary
TASK refs select exact fields of existing admitted, relative, hashed local fixtures.
They are not a general filesystem capability. EXPERIENCE refs pin an exact reviewed
record revision in the admitted archive and require current **retrieval** permission.
Training eligibility alone is insufficient. Wrong archive, missing/altered sources,
revocation, supersession or disputes fail current use. Shared readers enforce a bounded
2 MiB evidence-read allowance per validation pass; repeated guard checks are separate
passes, so this is not a total wall-clock/energy budget.

Checks occur on commit and every live scoped read; state sources are checked again
immediately before journal write. There is no cross-database lease: rights may change
after a point-in-time check or after bytes were exported. Explicit history inspection
retains original bytes and review lineage for the scoped local task holder but grants
no downstream retrieval/training/serving authorization. Secure erasure, encryption,
backup recall and learned unlearning are NOT implemented.

Context packet/request v2 carries `state_scope`; the current owner verifies the scope.
State appears under `payload.task.persistent_state` with authority label
`REVIEWED_WORKING_DATA_NOT_INSTRUCTION`. This is structural channel separation; actual
model-request channel mapping and neural prompt-injection resistance remain unimplemented.
Task source refs used only by state notes/annotations still join the mandatory source
list and can be exactly rehydrated under the same permissions/budget. For an archive
ref embedded in state, build a context request explicitly selecting that exact
experience before requesting a raw excerpt; this does not grant broad archive access.
The current authorized user input is not replaced by a saved summary.

## Questions, expiry and budgets
Unresolved questions may be saved and exposed in v2 context so the controller can ask
rather than guess. They still prevent a dependent MOVE while blocking and unresolved.
The legacy v1 context gate is unchanged. All accepted persistent-state fields are counted
as mandatory in the initial conservative context policy; optional removal is explicit,
not a claim of optimized semantic summarization.

Record and context limits use canonical JSON bytes, not tokenizer tokens. If mandatory
content does not fit, return BUDGET_EXHAUSTED without truncation/mutation. The context
owner supplies its existing budget/decomposition recovery choices. There is no automatic
summarizer or task decomposition algorithm.

An expired optional note blocks current use with RECOVERY_REQUIRED until a reviewed
EXPIRE_NOTE/RETIRE_NOTE removes it from current state. Mandatory and identity-sensitive
notes cannot receive automatic expiry. Retiring a now-ineligible note is allowed without
re-consuming its old source; remaining/new state must still satisfy current source checks.
FINISH/CLOSE/CANCEL may preserve already-performed work after rights withdrawal without
claiming fresh computation or retrieval permission.

## Atomicity, replay and typed outcomes
Event, new revision and current head share the existing SQLite transaction. Expected
hash/revision is checked inside that owner transaction. A mismatch returns
CONSTRAINT_CONFLICT plus REREAD_AND_REPROPOSE; it never uses last-writer-wins.
Same-event/same-command retries return the immutable receipt with `historical=true`,
even after expiry, source withdrawal or stage closure. A changed command under the same
ID fails. An uncommitted operation must pass current checks before a new commit.

Historical reducer replay uses the original event time and exact stored review; it does
not re-run tools or renew source rights. Live reads also verify journal and current
configuration. Incompatible state/tickets cannot be resumed under another ECID/scope.

Failure envelope uses existing codes: VALIDATION_FAILED, AUTHORIZATION_DENIED,
INCOMPATIBLE_CONFIGURATION, CONSTRAINT_CONFLICT, NEEDS_CLARIFICATION,
INSUFFICIENT_EVIDENCE, BUDGET_EXHAUSTED, RECOVERY_REQUIRED and propagated archive
review/retention codes. No missing evidence or timeout defaults to success.

External action receipts stay separate. State operations validate the existing ledger;
uncertain completion blocks state update until reconciliation. They do not perform an
external action and cannot undo or re-deliver one. One SQLite state commit is not a
transaction over the outside world.

## Verification and platform
Tests use inherited catalogue/context/experience fixtures and exact checkpoint artifacts.
The scripted demo demonstrates source-backed goal/question updates, no-review refusal,
restart, duplicate events, scope, current permission, identity challenge, retirement,
byte overflow, AB→A→CORE handoffs and closed history. The neural fixture may be trained
by existing setup, but no training is triggered by a symbolic state delta.

Fault injection uses real child-process exits before/after BIND and UPDATE commits and
an uncertain external-action window. These are process-crash tests, not sudden power
loss or storage-device failure tests. Single-worker trusted local baseline; no serving
concurrency/multiuser security claim. Linux execution is recorded; native Windows remains
an independent validation task. Full current checks and historical advisories are listed
in the release audit.

### Export compatibility

`catalog_command.schema.json` retains its five legacy v1 lifecycle arms byte-for-byte. `catalog_command_v2.schema.json` explicitly exports scoped MOVE/FINISH/CLOSE/CANCEL plus BIND_STATE/UPDATE_STATE; START remains v1 followed by explicit admission. Runtime dispatch selects the appropriate owned validator. The v2 catalogue is not a silent extension of the published v1 schema.
