# LocalNexusPermissions002 — bounded operation permission contract

## Scope
A trusted-local operator may issue a short-lived, nondelegable, one-use grant for
one exactly qualified NeuralProbe001 replay: AB -> A or A -> CORE, with exactly
the four transition fixtures, one task ID, and the bound prior action receipts.
No profile/generation-wide permissions, native loading, arbitrary commands, external
actions, network identities, PKI or deployment manager are implemented here.
A host grant is NOT an Aegis Runtime execution permit.

The fixed replay executor rebuilds real small PyTorch activation state, stores one
local experimental result and returns a content-bound receipt. It does not mutate
the old runtime current-checkpoint pointer or perform new external effects.

## Owners and permitted edges
| Owner | Owns | Does not own |
|---|---|---|
| permission_contracts | Fixed local request/grant/receipt and role semantics | Runtime, qualification or source data |
| permission_journal / permission_store | Grant events, consumption, withdrawal, completion history | Qualification SQL or runtime-result SQL |
| permission_executor | Fixed replay and immutable result/receipt journal | Grants, arbitrary tools, production publication |
| permission_replay | Narrow coordination through public owner methods | Private state/SQL of neighbors |
| permission_cli | Explicit local operator commands | Authentication or unattended consent |

Qualifications.check_use and NeuralEvidence guard live scope and dependencies.
Ledger's public methods check that each old mock-effect receipt matches the mock
world. Owner imports are explicitly allowlisted and statically checked.

## Preconditions
A exact supported qualified transition and its Core/endpoint prerequisites exist.
Its data permissions, artifacts, numerical execution contract and installed code
still match. The request names the exact declared caller and task, exact source
state and action receipt set. The grant issuer has a distinct local identity from
the caller. The local role manifest is sealed on store creation. The existing action
ledger pair must be present; the CLI cannot silently create empty replay history.

## State machine
```
GRANTED --BEGIN (durable consumption)--> STARTED
STARTED --live recheck + DISPATCH--> DISPATCHED
DISPATCHED --executor result durable + completion receipt--> COMMITTED
STARTED / DISPATCHED --caught non-success--> UNCERTAIN
STARTED / DISPATCHED / UNCERTAIN --explicit reconcile, no result--> ABANDONED
DISPATCHED / UNCERTAIN --explicit reconcile, exact executor receipt--> COMMITTED
```
An accepted result requires a recorded dispatch. COMMITTED/ABANDONED are terminal;
neither may restore GRANTED. A separate REVOKE event permanently marks that grant
revoked. Exact re-issuance retries return history and never reset expiry or status.

## Live checks and failure outcomes
Issue and consumption check current qualification, transitive revocation, data,
code/environment and exact identity. A second check immediately before dispatch
rechecks the live grant and qualification. DISPATCH itself is admitted once.
Expiry is inclusive: now >= expires_at is denied. A backwards observed clock blocks
new authority. TTL is 1..900 seconds. Caller-supplied clock/extra fields are rejected.
Malformed requests fail before grant mutation; valid denied ISSUE/BEGIN/DISPATCH
attempts append sanitized reason-code audit events without raw content.

Expected errors include AUTHORIZATION_DENIED, INCOMPATIBLE_CONFIGURATION,
TRAINING_RESTRICTED, INSUFFICIENT_EVIDENCE, RECOVERY_REQUIRED, CONSTRAINT_CONFLICT,
BUDGET_EXHAUSTED and VALIDATION_FAILED. No successful record implicitly authorizes
production. Historical inspection returns historical=true.

## Crash and uncertainty policy
The grant is consumed BEFORE work. After a crash, a spent request may not execute
again automatically. The reconciler asks the replay-result owner for the exact
receipt. If it exists and is valid, record completion without new computation.
If the store is readable and the receipt is absent, abandon permanently. Missing
or corrupt stores cause RECOVERY_REQUIRED/validation failure, not assumed absence.
A later deliberate attempt needs a new request and fresh live authority.

A completion can be recorded after expiry/revocation because the work already
happened. This does not issue fresh authority. A repeated COMMITTED execution request
cross-checks the authoritative result receipt; it does not trust a status label.
SQLite transactions use synchronous=FULL and journal-head updates together. Tests
inject real process exits around issue, consume, dispatch, result, completion and
revocation publication. Power-loss proof, hostile coherent journal rewrites,
multi-process execution leases and distributed exactly-once effects are NOT claimed.

## Time of check and trust limitations
Live checks are point-in-time admission checks. They are not a distributed
cross-store lease: revocation/expiry does not roll back already admitted work.
The protocol is for one trusted-local execution worker; no claim of adversarial
Python isolation or direct-call prevention. A process permitted to modify code or
rewrite all SQLite history can defeat local attestations. Real authentication,
sealed authority, lock/lease coordination and backend-specific permits belong in
later reviewed work. Declared operator separation is not human identity proof.

## Data and numerical boundaries
No private records are ingested. The demo uses synthetic data and scripted local
role choices. The service itself does not train; explicit demo fixture preparation
reuses the existing opt-in tiny neural probe. Numerical schema-v2 is required for
new evidence use. Historical schema-v1 reports stay inspectable, not promotable.
No output is a production deployment authorization or a blanket neural guarantee.

## Entry points
```
python -m nss_base.localnexuspermissions002 --directory ../permissions-demo
python -m nss_base.permission_cli --help
```
CLI supports init, init-executor, prepare, issue, execute, reconcile, revoke,
inspect, history and audit. Expiring grants are consumed only through the narrow
coordinator. Schemas are in schemas/permission_*.schema.json; lifetime ordering,
identity separation, current evidence, action receipt matching and uniqueness need
the Python owner validators in addition to structural JSON Schema.
