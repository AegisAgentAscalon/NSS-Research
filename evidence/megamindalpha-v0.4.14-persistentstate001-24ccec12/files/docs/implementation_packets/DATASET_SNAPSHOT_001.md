# DatasetSnapshot001 — bounded implementation packet

Input: complete 0.4.3 ExperienceArchive001 ZIP, checksum verified; 210 baseline
unit tests reproduced before implementation. Scope authorized by continuation
of the next subsystem in NEXT_STEPS. Target: 0.4.4 reviewed-baseline branch.

## Owned boundary
- dataset_contracts: strict bounded requests, deterministic text projection,
  grouping/split checks, normalized manifest/replay validation. No I/O or training.
- dataset_store: one local snapshot SQLite owner; manifests + operation receipts
  publish together. Does not own archive revisions or the runtime checkpoint.
- dataset_cli: explicit local init/build/inspect/list/audit/read commands.
- datasetsnapshot001: synthetic connected demonstration, no private data.
- The archive owner adds a narrow public batch-use method. All selected current
  revisions, review decisions and source-purpose revocations are checked under
  ONE archive transaction. Snapshot code must never inspect archive SQL/private
  fields or use administrative history reads as a consumption bypass.

## Inputs / outputs
BuildRequest: schema_version, operation_id, snapshot_id, actor, at, reason,
training purpose, allowlisted transform, pinned tokenizer identity/hash,
explicit nonempty member list of exact (experience_id, revision, sha256, split).
Only train and validation splits in this pass. Protected release/held-out access
and exposure tracking remain deferred. At least one training member is required.
No automatic selection, semantic distillation, network, external source ingestion,
executable transform, tokenizer execution, learned evaluator or training job.

Published manifest: exact request/digest, archive binding, schema/projection policy,
ordered selected references, original approved statement/source metadata and
review/permission observations, deterministic text and hash per example. Membership
is immutable; identical example texts are rejected, not silently deduplicated.
Declared families and any shared exact source bytes cannot cross split boundaries.
A split is not proof of independence against hidden semantic/near-duplicate links.

## Logic and permissions
BUILD: validate and normalize -> local archive binding + tokenizer bytes -> exact
retry lookup -> atomic current archive batch-use check -> project + split checks ->
transactionally publish manifest and operation receipt. Failure publishes neither.
A historical retry returns only the original receipt, NEVER current use authority.
INSPECT/AUDIT: administrative structural checks, never current permission grants.
READ: verify exact manifest and expected tokenizer -> recheck ALL selected exact
current archive revisions + current training permissions + source revocations ->
rederive and compare all pinned views/text -> return requested split's examples.
Any blocked member blocks the entire snapshot. No silent partial dataset or head
refresh. The operator must explicitly build a new snapshot with changed membership.

## Isolation and identity
The archive transaction is the point-in-time eligibility observation. Publication
in the snapshot store is separate: there is NO cross-database transaction guarantee
or durable authorization lease. Every subsequent read rechecks the archive; a
consumer must call it again at future batch/epoch boundaries. Returned/exported
bytes cannot be recalled, and no running trainer is present in this slice.
Local archive identity is explicitly location-bound and checked on use. Moving
or replacing a store is not silently supported; clone rollback/hostile disk edits
are not cryptographically prevented. Authorship/HUMAN labels are local attestations.

## Tests to write before implementation
- Build from pending or retrieval-only records fails; exact approved training works.
- Unknown/malformed/duplicate inputs, wrong types, hashes, timestamps, revisions,
  transforms, purpose and tokenizer bytes fail with typed outcomes before writes.
- All-or-nothing selection: one stale/revoked/missing member rejects the build/read.
- Group/source/text leakage across splits is rejected; deterministic member order.
- Approved correction leaves original manifest unchanged but blocks its use;
  explicit fresh snapshot uses corrected exact revision; unrelated records do not
  change an existing snapshot or its eligibility.
- Revocation after snapshot build survives reopen and blocks read; administrative
  inspection and exact operation retry do not regrant permission.
- Missing/corrupt archive, source, manifest, operations and store metadata fail
  closed. No auto-repair, auto-selection, silent subset skipping or stale cache.
- Different archive locator and changed tokenizer cannot be substituted.
- Crash before/after manifest and receipt publication; reopen + exact retry yields
  no partial row or duplicate snapshot. Use real child-process death.
- Capture a sealed StageHandoff outcome -> archive review/permission -> snapshot ->
  read; runtime checkpoint/action count stay unchanged.
- Every inherited test, demo, 25-flow validator, import checker, compile and manifest
  pass. Final delivered ZIP extracted clean and independently rerun.

## Constraints and definition of done
No adjacent refactor. Necessary public archive extension is documented/tested;
old public behavior and all old test files remain intact. Strict schema files and
example requests, CLI, audit, pseudocode and bounded flowchart extension included.
LT-04 and LT-05 local storage/selection behaviors are tested, not full learning.
LT-06 authenticated authorization, evaluation exposure, neural training, Runtime
integration, secure erasure/unlearning and large-scale streaming remain OPEN.
