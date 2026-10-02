# DatasetSnapshot001 — implementation self-audit

**Checkpoint:** 0.4.4-megamind-alpha-datasetsnapshot001 (reviewed-baseline branch)

**Verdict:** PASS for the bounded local software tests below. This is not an
independent Astra audit, an authenticated permission system, a learned evaluator,
a training run, a neural compatibility result, or a production-security review.
One inherited test-fixture ResourceWarning remains disclosed below.

## Input baseline and evidence discipline
Complete input: `MegaMindAlpha_v0.4.3_ExperienceArchive001.zip`.
SHA-256: `be86703852ca3a72373ed7d2c96f71b91999cb6e21eed9e2f159a9e6e98de74a`.

Verified the supplied sidecar, ZIP integrity and original 209-file manifest.
Reproduced 210 tests, four prior demos, 25-flow validation, static imports and
compilation before modifying inherited behavior. The initial foreground baseline
attempt was interrupted by the tool timeout; the retained complete rerun passed.

The implementation packet and initial 42 acceptance methods preceded primary
implementation. Their expected missing-module failure is retained. Twenty later
adversarial methods reproduced two revocation-index defects before repair; their
failing and corrected logs are retained. CLI/crash/integration tests preceded
those components. Further edge/ownership/schema checks brought the new total to 83.

## Implemented system and precise connection
- Four new runtime modules: bounded contracts/projection; one snapshot store owner;
  operator CLI; synthetic connected demonstration.
- Four new schemas: exact archive batch requests, permission-checked views,
  snapshot build request and manifest. Existing source/record DB schema stays v1.
- ExperienceArchive adds `binding` and atomic `read_batch_for_use` public methods.
  Snapshot code has no private SQL/history/raw-inspection consumption bypass.
- Snapshot manifest and operation receipt publish in one SQLite transaction.
  The archive's eligibility observation is separate. No cross-store lease or
  exactly-once training claim is made.
- Only approved current exact revisions with explicit training permission can be
  selected. Every later read rechecks all members and source revocations.
- Corrections require explicit new snapshots; old content stays unchanged.
- Family/shared-source split controls and exact-text duplicate rejection apply.
  These are not semantic deduplication or independent-holdout proof.
- Tokenizer bytes are checked, not executed. Text projections are fixed and simple,
  not learned distillation or instruction-target generation.

## Actual validation before packaging
| Gate | Result |
|---|---|
| Full suite | **293 tests passed** (210 inherited + 83 new methods) |
| New publication crash scenarios | **6**, covering 4 distinct termination points plus revocation/retry cases |
| Recovery 001A and 001B | PASS |
| StageHandoff001 | PASS; core -> AB -> A -> core, clean-A comparison, one mock effect |
| ExperienceArchive001 | PASS; source/correction history and scoped use decisions retained |
| DatasetSnapshot001 | PASS; fixed snapshot, explicit correction/rebuild, later revocation blocks |
| Parent Logic Atlas | All **25** graphs structurally valid |
| Snapshot helpers | **2** additional subordinate graphs structurally valid |
| Import boundaries and compilation | PASS |
| New schema regeneration | Four files byte-identical |
| Affected text/helper DOT regeneration | Byte-identical |
| Changed parent flows | Only `experience` and `builder` |
| Inherited source/test preservation | All 14 inherited test files unchanged; 18 of 19 inherited runtime modules unchanged |

The one modified inherited source is `experience_store.py`: the two public batch/
binding methods plus the revocation-integrity repair. Existing public behavior is
retained except that damaged revocation state now fails closed in more cases.
Historical Word/reference artifacts and the reviewed compression guide are intact.
Exact change inventory and individual test methods are listed beside this report.

The two new build/read helper diagrams were rendered and visually inspected.
The affected existing builder/archive diagrams were regenerated from the JSON.
No official DOCX regeneration or accessibility audit is claimed.

## Connected behavior observed
The demo first runs the existing stage/archive pipeline, then creates a snapshot
from two explicitly permitted synthetic record revisions (train + validation).
It reads the train example, corrects the source-linked interpretation, and verifies
that the old snapshot remains byte-identical but read returns CONSTRAINT_CONFLICT.
After review and renewed permission it explicitly builds dataset-v2. A subsequent
source-training revocation makes that read return TRAINING_RESTRICTED after reopen.
An exact retry returns the historical receipt only. Snapshot audit reports 2
manifests and 2 publication operations. The runtime checkpoint remains unchanged
and the prior mock action count stays exactly **1**.

## Self-audit findings and repair
**R-01: missing revocation index row.** The inherited selected-source lookup could
miss a recorded revocation when its index row had been deleted. A retained test
reproduced an unexpected SUCCESS after withdrawal. The owner now checks that the
revocation event set and index set agree before granting use.

**R-02: repointed index row.** A corrupt row pointed away from the selected source
could similarly hide revocation. The owner now verifies all local revocation source/
purpose/operation bindings before filtering. A second retained regression failed
before repair and passes afterward. This deliberately scans the local revocation
ledger once per batch; large-scale performance optimization is deferred.

**R-03: mutable approval race.** Tests revoke a source after the coherent archive
observation but before snapshot publication. A historical manifest may still be
published, but it is unusable at the next current-use gate. This behavior is now
explicitly documented rather than claiming an unimplemented cross-database lease.

**R-04: resource warnings.** Initial new corruption tests used SQLite context
managers without explicit closing; those new tests were fixed. A separate warning
already present in the baseline was traced with tracemalloc to the unchanged
`tests/test_stagehandoff001.py:201` test fixture. It leaves a test connection to be
closed by garbage collection. The 47-test targeted diagnostic and full suites pass;
this non-blocking inherited fixture cleanup is retained as an open housekeeping
item rather than editing inherited tests or claiming a warning-free release.

## Limits and open work
- HUMAN/reviewer/permission fields are local attestations, not authenticated identity
  or proof of lawful rights. Same-path malicious whole-store replacement/rollback
  is outside this prototype; hashes do not supply independent trust anchors.
- Archive binding is local/path-based. Portable identities and relocation migration
  need separate design; silent substitution is rejected.
- Snapshot rows are immutable history, not perpetual permission. Returned/exported
  bytes cannot be recalled; no training loop exists to interrupt mid-batch.
- Any selected head change invalidates use conservatively, even benign metadata or
  unrelated-purpose changes. No automatic refresh/exclusion is permitted.
- No secure erasure, backup purge, trained-weight unlearning or legal compliance
  certification. Admin inspection remains separate from downstream use approval.
- No automatic curation, factual verification, neural weights, learned evaluation,
  Hugging Face/network access, private conversation ingestion or Runtime adaptation.
- Development-validation data are not an independent release holdout. No global
  family, semantic duplicate or evaluation-exposure ledger has been implemented.
- Budgets are deliberately small: 32 records, 4 MiB manifest, 32 MiB tokenizer
  identity artifact, plus inherited archive bounds. No large-scale throughput claim.
- Python 3.13.5 / SQLite 3.46.1 / Linux is the tested environment; Python 3.10+ is
  the intended API floor, not a verified cross-platform matrix.

## Acceptance mapping and release integrity
LT-04 snapshot immutability, consumption checks and revision/revocation semantics
are now demonstrated locally. LT-05 explicit reviewed selection and curation
separation are locally demonstrated. LT-06 trusted authority, the learned evaluator
and actual training remain OPEN. The next proposed piece is local EvaluationRun001
result/evidence plumbing, not another architecture-wide redesign.

The final archive is extracted to a fresh directory and all gates rerun there.
Its byte-specific checksum/results are delivered in the adjacent release verification
file, outside the archive, avoiding a self-referential manifest. No pre-release
command log is substituted for the final extracted-ZIP check.
