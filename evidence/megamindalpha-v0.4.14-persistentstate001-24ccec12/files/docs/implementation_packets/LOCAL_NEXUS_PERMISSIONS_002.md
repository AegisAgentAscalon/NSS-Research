# LocalNexusPermissions002 implementation packet

**Status:** trusted-local development implementation; no production authority.

## Required public contracts
`prepare_request`: exact qualified transition + caller/task + existing action ledger
-> bound PermissionRequest or typed error.
`Permissions.issue`: request + issuer + TTL + qualification/source owners -> immutable
grant/history or denial.
`Permissions.begin` / `check_dispatch`: exact caller/request/grant and current owners
-> durable one-use STARTED / DISPATCHED or typed non-success.
`execute_once`: routes the bound request through grant checks, fixed replay, owner
result receipt and completion. No arbitrary caller callback accepted.
`Permissions.finish(reconcile=True)`: declared reconciler + exact executor owner ->
COMMITTED historical receipt, ABANDONED, or hold/error. Does not rerun computation.
`revoke`, `inspect`, `audit`, `history`: owner-governed events or read-only observations.

## Invariants and failure rules
See docs/LOCAL_NEXUS_PERMISSIONS_002.md and machine-readable subordinate flows.
No reset of consumed authority, scope widening, implicit renewal, new external
side effect, direct deployment, neighboring SQL or universal exactness claim.

## Qualification and integration
Must preserve all inherited tests and seven earlier subsystems, current numerical
strictness, exact QAP/directed transition semantics, stale-state rejection and old
mock action count. Live evidence withdrawal must block issue/consumption/dispatch.
Completed history is inspectable without becoming current permission.

## Mandatory test stimuli
- Substitute caller, task, operation, state digest, evidence, precision, inputs or grant.
- Expire/revoke before consume and after consume/before dispatch.
- Remove prerequisite/source eligibility between those stages.
- Attempt consume/dispatch twice or reuse the request ID with changed fields.
- Crash at every commit boundary; reopen stores and explicitly reconcile spent work.
- Remove/corrupt a COMMITTED executor receipt; retry must fail closed.
- Reconcile absent result: permanently abandon, never silently repeat.
- Change numerical backend fingerprint: deny reuse; perturb fresh MSE by 1e-12: fail.

## Implementation order
1. Confirm baseline and reproduce legacy MSE issue.
2. Add new numerical execution contract without editing historical evidence.
3. Pure request/grant schema + local append-only permission owner.
4. Fixed replay-result owner + narrow coordinator + local CLI.
5. Regression, negative, subprocess replay and process-crash tests.
6. Reconcile Nexus parent and three helper graphs. Update provenance/coverage docs.
7. Fresh archive extraction and all release checks. Preserve visible historical advisory.

## Deferred
Overlay Generation Manager and family-wide qualification need separate scope.
No existing transition claim can be reinterpreted as release approval.
