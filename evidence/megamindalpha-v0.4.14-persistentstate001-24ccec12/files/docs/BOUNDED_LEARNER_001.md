# BoundedLearnerCoordinator001 — implementation contract

> v0.4.13 integration note: this learner still owns no release authority. The separate
> CandidateAcceptance001 path now accepts its exact proposal format through existing
> qualification/generation owners. See CANDIDATE_ACCEPTANCE_001.md. Earlier statements
> about the former missing adapter describe v0.4.12, not the current connected demo.

This is human-assisted, trusted-local orchestration of one installed synthetic
recipe, NOT learned curation, a learned evaluator, autonomous model replacement,
production authentication, or an Aegis Runtime execution permit.

## Ownership and public boundary
- Existing ExperienceArchive owns evidence, revision/review and purpose rights.
- Existing DatasetSnapshots owns fixed membership and use checks.
- Existing NeuralEvidence owns access to the exact parent probe evidence.
- The numerical-run owner (shared ProbeRuns journal mechanics, versioned sibling
  formats) owns candidate checkpoints and evaluation reports/receipts.
- A small learner EventJournal owns ONLY plan, scoped local approval, dispatch
  markers, immutable references to owner receipts, cancellation and proposal.
  It never owns a second dataset, generation, task, permission or checkpoint head.
- The coordinator cannot import qualification/deployment mutators or perform tools.

## Input and preconditions
A LearningPlan pins a producer, reason, source-task/context references (provenance,
not authority), exact parent binding, archive identity, reviewed snapshot request,
installed recipe+seed+budget, numerical environment and installed code hash.
The caller supplies a plan explicitly; no automatic gap diagnosis is claimed.
An independently declared local operator approves that exact plan before dispatch,
with expiry. This training-only attestation cannot authorize deployment or reuse a
replay-specific permission. Unauthenticated local labels are not real identities.

Only synthetic one-hot symbol pairs under codec one_hot_16_pair_v1 are supported.
The recipe trains a NEW rank-4 A2 overlay against the EXACT frozen parent Core and
retains the parent's A and B for comparison. It does not train a replacement Core.
Train/validation go through current snapshot consumption; test combinations are
versioned developer-visible fixtures, not an independent protected benchmark.

## Flow and postconditions
prepare -> operator approval -> build exact snapshot -> claim one training attempt
-> train/atomically seal candidate -> claim evaluation -> evaluate twice with fixed
criteria -> seal exact report -> produce review-only release proposal.
The final proposal is NOT a qualification certificate. A2/A2B and transitions are
outside the current qualifier's supported claims, so eligibility remains
INSUFFICIENT_EVIDENCE even when numerical checks pass. FAIL reports produce a
NOT_RECOMMENDED proposal; no favorable score creates a deployment edge.

## Recovery and failure
Record dispatch BEFORE numerical work. Crash after a numerical receipt commits:
recover its exact receipt without retraining. Crash while dispatch is unresolved:
RECOVERY_REQUIRED; do NOT blindly repeat training/evaluation or replenish budget.
The operator can cancel/abandon and prepare a newly approved attempt. This is not
optimizer-checkpoint continuation. Pure dataset-build retries use the existing
idempotent owner. Cancel/revoke/expiry block later dispatch and are checked during
training at most every 25 updates (plus before/after each stage). Checks are points
in time, not cross-store leases. Completed artifacts and historical receipts remain
inspectable but confer no renewed right. Interruptions cannot recall used bytes.
Missing/stale/revoked data, changed code/environment/artifacts, conflicting IDs,
insufficient budget and evidence return typed non-success; old production stays put.

## Invariants and forbidden edges
- Only new candidate parameters may train. Parent Core, A, B and original report
  remain exact. Seed and total optimizer budget never silently change on resume.
- Coordinator never edits evidence, review permissions, tests or release policy.
- No evaluation callback/code name supplied by JSON. Only installed bounded recipe.
- No blind retry of ambiguous numerical work; no repeated committed mock action.
- No self-qualification; no candidate -> publication shortcut; no auto Core upgrade.
- Context reads/provenance hashes are NOT training approval or runtime permits.

## Tests required
Fixed-plan/mutation/role/budget validation; denied/expired/revoked/cancelled
admission; actual candidate training and exact Core preservation; explicit FAIL;
repeat/reload metrics; corruption/missing owner receipts; crash around dispatch,
owner publication and proposal; revoked data between phases; terminal history after
revocation; connected catalogue/context/archive/data/neural proposal acceptance.

## Resource accounting and current trust boundary
`optimizer_updates` is the maximum count for one claimed new-A2 training attempt.
`training_attempts` is exactly one; losing an unsealed numerical attempt does not
restore its claim. The plan must be explicitly abandoned and a separately approved
new plan used. `evaluation_passes` bounds each installed scoring/check operation
(two repeats), not the sum of all future verification work. A normal cycle scores
twice and re-verifies twice; parent qualification/source checks and a later explicit
current-use check incur additional work. These are bounded procedures, not a whole-
application wall-clock, energy, or hardware resource-enforcement guarantee. There is
no automatic retry/search loop for a better candidate.

The snapshot includes a pinned validation record for lineage and codec checking;
this fixed recipe trains only on the train record. Candidate scoring uses the installed
64-pair developer-visible test fixture and 49 retained-behavior pairs. Validation
text is not presented as an independently hidden test. Both training records and
test answers are synthetic, known to the implementation authors.

Permission checks occur at stage boundaries and at the backend's bounded optimizer
checkpoints; they are point-in-time checks, not an atomic cross-database lease. No
claim of multi-worker safety, authenticated human identity, recalling exported bytes,
learned curation/evaluation, or production Runtime execution is made. The operator
approval is local and distinct from qualification and deployment permission.

Optional `origin` fingerprints describe provenance supplied in the approved plan;
shape validation is not independent proof of a live source-task attestation. The
demo explicitly attaches the exact completed TaskRecord/context as reviewed archive
evidence. Arbitrary origin labels never grant training, qualification or release rights.

The required parent acceptance is its exact Core-only certificate. Pinned source
A/B checkpoint bytes are frozen comparison/continuation inputs, not newly granted
deployment rights. The demo separately prepares its accepted active parent family
through the existing qualifier/manager; the learner itself does not broaden that scope.
Candidate reports include small data-only parent checkpoint copies for standalone toy
verification. This is not a deduplicated production Neural Reserve storage claim.
