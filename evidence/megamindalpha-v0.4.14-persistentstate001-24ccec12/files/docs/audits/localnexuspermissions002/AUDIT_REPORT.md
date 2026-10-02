# LocalNexusPermissions002 — implementation and numerical-replay audit

**Release:** v0.4.8 on the reviewed-baseline branch.

**Status:** required CURRENT checks PASS; raw historical strict-MSE advisory retained.

**Not claimed:** production security, authenticated human identities, generic Runtime
execution permits, distributed exactly-once effects, or general neural NSS quality.

## Input and baseline
Input: MegaMindAlpha_v0.4.7_QualificationEvidence002.zip. SHA-256:
`951ffd532a9b6fe0d2ad59673250a5785ed6c5ba9726640b54b5b7adf5912900`.
The archive/manifest were verified before source modification. The unmodified
baseline passed **615 tests in 544.174 seconds**. Its historical strict numerical
check failed on small MSE differences; all accuracy/count observations agreed.
Raw baseline logs are retained under verification/.

## Numerical defect and bounded correction
The old record did not adequately bind CPU dispatch, compiled math-stack identity,
backend controls or a common saved-checkpoint scoring path. Controlled runs with
changed MKL compatibility settings produced different tiny rounding discrepancies,
with unchanged accuracy/counts. This proves sensitivity and incomplete metadata,
not the unrecorded exact cause of the original archived values.

New plans require schema v2, additional CPU/build/backend identity, deterministic
CPU float32/highest-matmul/no-autocast execution, and one shared scoring function
that reloads sealed checkpoints for both initial scores and replay. Caller RNG,
thread/dtype/precision settings are restored. Training tasks, architecture and
budgets were not changed. Exact comparisons are NOT replaced with tolerances.
Legacy plans stay inspectable but cannot authorize new CURRENT claims. Archived
reports and the original strict tool are untouched. Read
../../NUMERICAL_REPLAY_CONTRACT_V2.md for detailed scope.

## New permission subsystem
Exact accepted transition evidence is necessary but insufficient to execute.
A distinct declared local issuer grants one supported caller/task/transition/
state/action-receipt request for a bounded lifetime. Grants cannot delegate or
approve generation release. Live evidence/expiry/revocation are checked at issue,
consumption and dispatch admission. Grant consumption precedes computation.

After a crash, a consumed grant cannot dispatch again automatically. A local
reconciler reads the authoritative executor receipt: present and consistent means
record historical completion; confirmed absent means permanent abandonment. Missing
or corrupted journals fail closed rather than becoming assumed absence. A receipt
cannot complete a grant without a recorded dispatch. A committed retry cross-checks
its executor receipt and does not rerun computation or renew data permissions.

The executor performs only the existing bounded neural replay and records a local
experimental result. It cannot issue new external actions, change a production
checkpoint or mint a real Aegis Runtime permit. The old simulator flags retain
their meaning; the new coordinator crosses the fixed lab adapter boundary explicitly.

## Actual verification
- **730 unit tests passed** in the clean-extracted build: 615 inherited +115 new.
- The 115 methods comprise 16 numerical-contract and 99 permission tests, including
  **11 real process-crash scenarios**. The exact method index is TEST_INDEX.md.
- The earlier worktree run passed 729 tests before the final A->Core coverage method
  was added. The clean-extracted run includes and passes that additional case.
- All **nine demonstrations** passed.
- All **18 required gates** passed. There are19 raw gates total; the one non-required
  `reference_neural_evidence` gate retains the old strict-MSE disagreement.
- All25 parent logic graphs and14 subordinate graphs validate structurally. This is
  graph structure/coverage checking, NOT proof of termination or program correctness.
- Static import boundaries, compilation, deterministic schema/logic regeneration,
  and source-manifest verification passed.
- All6 fresh neural trials replayed exactly in separate processes without any
  tolerance fallback. The two fresh confirmation runs agree on all30 checkpoint
  hashes and all60 full metric dictionaries. This is local evidence, not universal
  cross-hardware reproducibility.
- The connected permission demo returns COMMITTED, refuses the wrong caller and
  revoked grant/prerequisite, preserves report bytes, records one executor result,
  and leaves the old committed mock external effect count at1.

The inherited unclosed-SQLite ResourceWarning remains visible in the unit log. It
also appeared before modification. No warning-free release claim is made.

## Audit fixes and plan deviations
Three inherited numerical modules changed: neural_backend.py, neural_records.py
and neuralprobe001.py. The protocol schemas are versioned, not silently migrated.
All **34 inherited test/helper files** remain unchanged, as do **36 inherited runtime
modules**. Seven new runtime modules add the local permission boundary.

A completion guard was strengthened to reject results lacking dispatch admission.
Early development tests mistakenly called two inherited helper APIs with incorrect
arguments; the new test fixtures were corrected to those existing public APIs, not
by weakening implementation checks. The final complete suites pass.

The release runner's per-command timeout increased from420 to1200 seconds because
the measured unmodified baseline already required544 seconds. This is a scheduling
bound, not a reduced assertion or a changed acceptance threshold.

One flowchart label was corrected after the full run: initial validation checks the
request/grant/caller, while real source-state checking follows consumption before
dispatch. No node/edge behavior or Python code changed. Final graph, regeneration,
manifest and source identity checks are rerun after documentation finalization.

## Trust and evidence boundaries
Operator IDs are trusted local declarations, not authenticated identities or proof
of distinct people. Hash chains catch accidental/partial changes, not a privileged
actor rewriting all history. No cross-store lease, hostile Python sandbox, native
device integration, multi-session scheduling or production deployment is supplied.
Live checks are point-in-time: revocation cannot undo already admitted computation.
The demo uses synthetic data/scripted choices; the permission owner itself does not
train. Explicit demo setup reuses the existing tiny neural training fixture.

The model is still a favorable512-parameter linear Core with two128-parameter
extensions. Ternary mode remains float32 storage/overlays/math with effective
{-1,0,+1} Core weights. No packed1.58-bit performance or modular superiority claim.

Fresh reports shipped here are inspection evidence, not portable permission grants.
Their source stores may be revoked or absent; recreate a deliberate fresh run for
new qualification. Neither a passing test nor a report grants deployment authority.

## Next bounded pass
OverlayGenerationManager001: specify generation-wide qualification and release
permission separately; stage/adopt/archive a whole exact family atomically with
explicit recovery. Existing replay grants cannot be stretched into release permits.
