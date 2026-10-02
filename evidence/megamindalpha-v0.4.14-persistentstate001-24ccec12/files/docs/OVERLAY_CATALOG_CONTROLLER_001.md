# OverlayCatalogController001 — deterministic approved-profile selection

## Scope
One cooperating local worker selects ONE exact profile per stage. It consumes
reviewed exact capability labels and declared cost/limit metadata from the current
qualified generation; it never synthesizes a union or an unqualified subset.
These labels are fixture mappings, not learned understanding or new numerical evidence.
`sealed_document_bytes` counts canonical JSON checkpoint-document bytes, NOT resident
RAM/VRAM, tensor memory, load latency or energy. Cost units are explicit declarations.

## Ownership and public interface
| Owner | Responsibility | Not owned |
|---|---|---|
| `catalog_contracts` | Strict descriptor/request/command checks and deterministic selection | Storage, qualification, learned routing |
| `CatalogController` | Small public facade bound to current source/ledger owners | Private SQL, neural execution, permissions |
| `catalog_tasks` | Pure managed-task reducer and task-state validation | External evidence I/O |
| `Generations` | ONE existing journal for release state, descriptors, task heads, tickets and operation receipts | Integer RecoveryStore, action ledger, serving processes |
| `task_records` | Shared portable fact/source/handoff/finish rules | Configuration or storage authority |
| `generation_views` | Shared pure generation-state queries | Additional store or mutable cache |

The static dependency allowlist is updated. New catalogue modules cannot import
private runtime/qualification SQL or invoke external effect execution. The generation
store uses its own existing transaction and public neighboring owner APIs.

A reviewed descriptor fixes its generation hash, profile ECIDs, all profile entries,
labels, input limits, declared costs, and exact serialized checkpoint sizes. A distinct
local reviewer registers it; IDs are immutable. Descriptor review is NOT neural
qualification, a release grant, a replay grant, or a real Runtime execution permit.

## Selection contract
1. Validate exact request schema, task/mode, pairs and finite resource bounds.
2. Recheck generation epoch/hash, descriptor binding and live source/child evidence.
3. Require one existing profile to cover ALL requested labels. Never combine entries.
4. CONTROL/EVALUATION can select only CORE.
5. For existing work require a finished exact source stage; profile changes need an
   explicit directed edge. Same-profile progression is a new stage with rebuilt state.
6. Filter by maximum input pairs and declared document/cost budget.
7. Rank `step_units * pair_count + load_units`; unchanged profile pays no load units.
   If tied, retain current if it is among the best. Other ties require clarification.
8. Return a selection proposal, not a reservation or execution permit. Admission
   rechecks the same conditions atomically rather than trusting a previous proposal.

Unknown labels return CAPABILITY_UNAVAILABLE; ties return NEEDS_CLARIFICATION;
resource limits return BUDGET_EXHAUSTED; impossible edges or stale identities return
INCOMPATIBLE_CONFIGURATION. Other owner failures preserve their original reason.
No speculative semantic matching, implicit fallback, global optimizer, or load thrashing
loop is implemented. Selection is bounded by four supported profiles.

## Task lifecycle
`START -> RUNNING -> FINISH/SEALED -> MOVE/RUNNING ... -> CLOSE/COMPLETED`.
Explicit `CANCEL` ends unfinished work while retaining its last record, receipts and
reason. A task ID and each stage/ticket ID are not recycled. Historical retries do not
reopen stages. Exactly one open registered stage blocks whole-generation publication.

A fresh task can begin in an approved WORK profile from portable initial inputs;
there is no preceding neural state to migrate. CONTROL/EVALUATION begins Core-only.
An existing task may NOT use close/reopen to invent CORE->AB, B-only, or a reverse edge.
The current numerical evidence supports AB->A and A->CORE; broader transitions need
new exact evidence rather than being inferred from valid destinations.

Every operation binds the exact previous record hash and local source/ledger owner
paths. MOVE preserves task identity and input pairs, requires the old stage sealed,
uses the existing exact-source rehydration rules, and preserves original request,
facts, assumptions, questions, clarifications, constraints, results and receipts.
Only explicitly required missing fact values/units may be filled, from hashed source
bytes. Missing, contradictory or ambiguous evidence stops before publication.

The old ticket closes, the new ticket opens, the task head moves, the portable record
advances and the completion receipt commit in ONE generation-journal transaction.
This is an integration with the shared TaskRecord contract, NOT a relabelling of the
integer StageHandoff001 cache or a claim that its RecoveryStore now holds neural state.

## State, caches and results
A live read returns only the selected Core/overlay checkpoint documents, input pairs,
exact record and a task-state identity binding generation epoch, ticket, profile ECID,
record revision and input pairs. Old identity is rejected after any stage or record
change. The experiment rebuilds actual small neural activations through this boundary.
There is no general native KV migration, device serving permit or hardware paging.

FINISH appends labelled results and verified action/output receipts. The result's
producer ECID must match the selected neural profile. A source/check label is provenance,
not an independent scientific judgment. Plain `read_stage/close_stage` cannot bypass
task-bound live-read and close rules for annotated tickets.

## Revocation, cancellation and recovery
START/MOVE/live reads always recheck current source/certificate eligibility through
owner APIs. FINISH/CLOSE/CANCEL may preserve already-performed work after revocation;
they admit no new neural execution and never renew authority. All action receipts are
verified by the authoritative local mock ledger. Missing or uncertain effects prevent
closure until the ledger owner explicitly reconciles them; this controller never runs,
retries, or undoes an effect. Presented-output receipts are retained similarly; arbitrary
live streams are not implemented.

Crashes before a transaction commit preserve the prior state; after commit, retrying
that exact operation returns its original receipt. One store owner means no extra
cross-database current-stage pointer to reconcile. Source eligibility and the action
ledger are still point-in-time checks in separate stores, NOT a multiwriter atomic lease.
Restart retains unfinished tasks and their barrier rather than automatically cancelling.

## Tests, limits and next work
See current audit/test map and the helper logic graphs. These are process-exit tests,
not power-loss certification or authentication. Declared roles remain trusted-local.
The bounded generation journal retains its existing capacity (2,000 events / 32 MiB).
Source-owner absolute paths are pinned; relocation requires explicit future migration.
Returned/exported bytes cannot be recalled by revocation. Unregistered foreign work
is outside the barrier. No new model quality, learned routing or energy gain is claimed.

Next: ContextRetrieval001. Build bounded selected task packets and exact-source
retrieval around these task records and the existing experience/knowledge owners,
without requiring native HSA/MSA, new neural architecture or a separate current pointer.

## Publication versus subsequent reads
A successful task transaction is durable. If a later live read fails because the
source or qualification was withdrawn, the published stage remains recorded and
pinned; the failure does not rewind its history. Use explicit completion/cancellation
or the next qualified recovery operation as appropriate. Historical retry lookup
occurs before current-ticket validation, but still requires the original exact
command and a declared operator role. It does not run a fresh read or reopen work.

## Version compatibility
Descriptor/command schemas are explicitly version 1 of the new controller format;
selection policy is pinned as `exact_profile_declared_cost_v1`. The existing journal
envelope and old generation event meanings are unchanged. New readers accept old
histories; the first named CATALOG_REGISTER/CATALOG_TASK extension event requires
the v0.4.10 reader. Older readers reject those unknown event kinds rather than ignore
or reinterpret them. Do not downgrade an extended live journal; retain the matching
runtime/source snapshot. No automatic reverse migration is implemented.
