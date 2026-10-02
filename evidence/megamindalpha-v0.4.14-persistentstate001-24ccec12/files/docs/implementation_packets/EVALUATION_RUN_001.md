# EvaluationRun001 — implementation packet

Scope: one local result/evidence owner on top of the reviewed-baseline 0.4.4
DatasetSnapshot checkpoint. Input archive SHA-256 is recorded in the audit. The
293 inherited tests passed before editing. No presumed missing 0.6 implementation.

## Ownership / public boundary
- evaluation_contracts: strict bounded plan/suite/material/report validation and
  versioned deterministic integer checker. No filesystem, SQL or runtime mutation.
- evaluation_inputs: verify/capture exact local candidate, suite, fixtures, code and
  environment identity; optionally read a development dataset through the PUBLIC
  snapshot consumption API. Never inspect archive SQL or admin history to consume.
- evaluation_store: owns only evaluation SQLite plans, prepared material, finalized
  reports and completion receipts. No active configuration or release pointer.
- evaluation_cli / evaluationrun001: explicit operator interface / synthetic demo.

Plan pins the candidate manifest bytes, profile + expected ECID, independent
self-authored synthetic test suite bytes, repeat count, check budget, exact local
implementation identity and optional development snapshot. Suite pins individual
fixture bytes, named/versioned tests, expected integer results, mandatory flags
and an integer pass threshold. Inputs/artifacts are data, never executable code.

PREPARE: strict plan -> validate exact artifact bytes/profile/dependencies ->
explicit suite-purpose attestation -> exact fixtures -> current optional snapshot
read -> capture immutable material -> commit PREPARED. Exact retry of a finalized
plan returns HISTORY, not renewed current-use authority. Different plan under same
run ID conflicts. Missing/corrupt stores never silently recreate/repair themselves.

EXECUTE: reopen/validate PREPARED -> repeat current-input and permission gates ->
run allowlisted PURE integer checks within frozen budget -> recheck current inputs
and optional snapshot before finalization -> atomically publish report + receipt.
No external actions can run here. A process crash before publication leaves
PREPARED, with no score/approval; retry may repeat pure computation only. Crash
after publication returns the same historical result. A paused/resumed run must
match original candidate, fixtures, code and data selection; it may not substitute
new inputs and keep the old ID.

PASS: all scheduled checks ran, mandatory cases pass, frozen overall threshold
passes, repeats reproduce. FAIL: complete run violates acceptance. INCONCLUSIVE:
check budget cannot complete planned matrix (never silently drop missing trials).
Contract/storage/access failure is separate from the evaluation verdict. Never
accept externally supplied scores. Recompute report integrity from retained
non-executable material during inspection/audit; this is not an independent judge.

## Data boundary
Suite is DEVELOPMENT_SYNTHETIC, not a protected release benchmark. Optional snapshot
read is explicitly training-purpose DEVELOPMENT data/lineage observation; its text
is not input to the arithmetic checker and does not become hidden test evidence.
Only hashes/counts/refs of those examples are retained, not their text. Each repeat
and final publication rechecks through DatasetSnapshots.read_for_use. No use lease,
cross-store atomicity, export recall, whole-store rollback prevention or training
claim. Historical results persist after revocation, with no authority to reuse data.

## Tests / hard gate
Exact and changed artifact/fixture/code identities; wrong profile/ECID; unknown test
or code execution request; malformed/duplicate/nonfinite input; frozen thresholds;
mandatory failure, optional threshold, incomplete budget; repeat equality; altered
scores/digests/rows; PREPARED versus FINALIZED; retry conflict and recovery; actual
child-process crash points; revocation/review change before resume/consume; complete
connected stage->archive->snapshot->evaluation demonstration preserving checkpoint
and mock-action count; invalid DB/schema/receipts fail closed; pure/store dependency
ownership; generated schemas/graphs reproducible. Every inherited assertion stays.

No neural evaluator, model training, benchmarking claims, real Nexus authorization,
qualified release signer, private data, networking, Runtime clone, concurrency or
security-isolation guarantees. Performance measurements/learned judges need separate
checker contracts. End-to-end demo may be rerun only in an empty fresh directory.
