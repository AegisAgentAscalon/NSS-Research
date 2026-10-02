# Current checkpoint — ContextRetrieval001 / v0.4.11

Implemented the software context service around existing catalogue task and reviewed
experience owners. It preserves mandatory state, selects bounded optional context,
rehydrates exact fields/source slices, rechecks permissions and rejects stale packets.
No new store, neural context mechanism, private ingestion or deployment permission.
Validation evidence is in docs/audits/contextretrieval001; current work order is in
NEXT_STEPS.md. Previous notes below are historical, not current implementation claims.

---

# Current checkpoint: 0.4.7 — QualificationEvidence002

Adds local claim-scoped reviewer decisions on exact NeuralProbe001 artifacts,
Core-only/endpoint prerequisites, fresh public source checks, deterministic numeric
rechecking, atomic event/receipt publication, transitive revocation and historical
inspection. No accepted evaluator/trainer module can self-promote. No generic
Aegis Runtime changes or real Nexus permissions. Independent means role-separated
local workflow; identities are unauthenticated attestations and checker is shared.

Read docs/audits/qualificationevidence002/AUDIT_REPORT.md and external release logs
for actual verification. The historical strict-reference MSE check is retained as
an explicit advisory; all accuracy/count groups match but exact MSE does not.

---

## Retained progress history (earlier claims are not current authority)

# Current checkpoint: MegaMind Alpha v0.4.6 — NeuralProbe001

Added an optional real PyTorch linear neural probe, data-gated training, frozen Core/A/B and new A2, matched joint control, data-only checkpoints, real activation-cache recovery and a separate numerical evidence journal. Approval remains simulated; no full NSS intelligence or native packed ternary result is claimed. See current README, packet, measured results and audit.

---

## Historical entries below; earlier capabilities/counts describe their release only

# Current checkpoint: MegaMind Alpha v0.4.5 — EvaluationRun001

Implemented local development evaluation plans/material/results, frozen thresholds,
pure repeatable integer checks, three explicit verdicts, current-use data gates,
immutable history and crash-safe report publication. No learned judging or release
permission. See docs/EVALUATION_RUN_001.md and the audited full-source handoff.

The record below is preserved historical progress, not a claim that all former
roadmap items are implemented in this branch.

---

# Current checkpoint — DatasetSnapshot001 / 0.4.4

Added fixed exact-revision training-data snapshots with human-attested selection,
public atomic archive batch checks, scoped permission/revocation rechecks on every
read, split/group/exact-duplicate checks, tokenizer byte identity, transactionally
published manifests/receipts, CLI, synthetic integrated demo and failure/crash tests.
Repaired missing/repointed revocation-index integrity in the archive owner.

This is still local software, not neural learning or authenticated release authority.
See [current audit](audits/datasetsnapshot001/AUDIT_REPORT.md) for the actual tests
and limits. The complete input was 0.4.3, not absent-source 0.6 notes. Next proposed
bounded piece is local EvaluationRun001 evidence plumbing. No model training yet.

---
## Historical progress below (earlier scope/counts are not current claims)

# Current: 0.4.3 — ExperienceArchive001 (2026-09-10)

Implemented the next bounded subsystem: local persistent experience, exact source
capture, separate interpretations/corrections, operator review, purpose decisions,
source revocation, event/revision integrity, and one-way StageHandoff intake.
No runtime checkpoint schema or neural component changed. See README, the new
contract and retained audit. Source lineage: reviewed 0.4.1 -> 0.4.2 -> this branch.
The release suite contains 210 tests (128 inherited, 82 new); exact command evidence
is retained and rerun from the delivered archive. These are software fixtures,
not neural learning/evaluation or authenticated human-review evidence.

---
## Historical progress (retained verbatim below)

# Current: Logic Atlas 001 correction review

Version 0.4.1-logicatlas001-corrected. Hardened schema-v2 atlas validation, corrected 25 design views, fixed recovery resume/load/history/input-binding behavior, added 14 regression tests (81 total), and regenerated Word v0.2, Markdown, DOT and PNG artifacts. No new neural subsystem or training. See `REVIEW_CORRECTIONS.md`, `TEST_AUDIT.md` and `NEXT_STEPS.md`. Earlier entries below are historical.

# Progress and handoff

## Logic Atlas 001 — version 0.4.0-logicatlas001

Completed a specification-only anti-spaghetti pass on top of the unchanged Recovery 001A/001B runtime.

Added:
- `spec/logic_atlas.json`: machine-readable source of truth for 25 implementation-level flows spanning the master spine, Core/package, tokenizer/context ABI, context selection, compute discipline, AR working loop, recurrent depth, ambiguity, overlay index/runtime/generation, memory, experience, knowledge, Builder, trainer, qualification, Generation Intent, Directional Guidance, DARP, multimodal ABI, external actions, recovery, Core upgrades, and Nexus governance.
- `nss_base/logic_atlas.py`: dependency-free structural validator and flow metrics.
- `tests/test_logic_atlas.py`: reachability, terminal typing, research-mechanism separation, Core-only, replay/action separation, QAP/transition qualification, claim-scoped qualification, complexity bounds, and negative validation tests.
- Generated human-readable pseudocode/Mermaid atlas plus compression guide, implementation packet template, and structural metrics.

This pass intentionally adds **no production runtime behavior** and makes no new neural claims. It exists so future coding passes can implement one subsystem at a time from a compact, testable logic specification rather than repeatedly re-reading the whole architecture.

## Recovery Experiment 001B — version 0.3.0-recovery001b

Completed one bounded follow-up after 001A, beginning with an independent audit of the uploaded 0.2.0 handoff.

Implemented:
- Durable `recovery_attempt` schema with PREPARED / STAGED / PUBLISHED / FAILED states.
- Content-addressed checkpoint storage plus a per-task current-checkpoint pointer.
- Recovery-attempt records binding source checkpoint hash, source/target ECIDs and profiles, portable input descriptor, and verified committed action keys.
- Durable target staging before publication.
- Atomic SQLite transaction that changes the task's current checkpoint and marks the attempt PUBLISHED together.
- Resume behavior for process crashes after prepare, after target computation, after durable staging, and after publication.
- Current-pointer compare-and-swap semantics: a stale attempt cannot overwrite a changed published source.
- Revalidation of staged target checkpoints before resumed publication.
- Authorization required on every unpublished resume path.
- Stronger replay-safe action verification: COMMITTED ledger receipt must be the expected deterministic receipt and must match the authoritative local mock-world receipt.
- Fail-closed behavior for missing/corrupt recovery evidence.
- Exact clean-A equivalence and source retention on failure.

Audit correction:
- The retained v0.1 in-memory runtime treated overlay order as irrelevant for `reuse` and sorted artifacts in configuration identity. That was inconsistent with ordered computation. Reuse now requires identical ordered overlays and the historical ECID now includes ordered artifacts.

Validation:
- 56 total unit tests pass (42 prior tests plus 14 001B/audit tests).
- Four 001B subprocess crash windows exit intentionally with code 73 and recover as specified.
- 001A demo remains passing.
- 001B demo returns SUCCESS, exact recovered-A/clean-A equality, current profile A, PUBLISHED attempt state, and one committed task mock effect.
- A clean extracted ZIP snapshot is re-tested before handoff.

Scope remains local deterministic simulation. No neural training, real model weights, device loading, actual Nexus authorization, signed qualification authority, concurrent runtime, real external tools, HSA/MSA, recurrent depth, DARP, or identity evaluation was implemented.

## Recovery Experiment 001A — version 0.2.0-recovery001a

Completed:
- Nine strict JSON Schema files plus semantic validators for manifest, artifacts, profiles, overlays, transitions, inputs, checkpoints, and action records.
- Actual SHA-256 of local Core/A/B/input fixture bytes; ECID binds the manifest and active profile.
- Integer Core+Overlay execution, stale-cache rejection, replay from portable inputs, and exact recovered-A/clean-A comparison.
- Directed transition fixtures with explicit reuse, invalidation, replay, and failure destinations; unconditional Core-only profile retained.
- Durable SQLite ledger with PENDING/COMMITTED/UNCERTAIN, globally scoped idempotency keys, separate mock receipts, explicit reconciliation, and four subprocess crash windows.
- Focused negative tests for corruption, incompatible state, dependency/exclusion violations, identity changes, action conflicts, missing evidence, and transition failure retention.

001A's limitation was that recovery returned the rebuilt target in memory; it did not durably stage/publish a target checkpoint. 001B addresses that narrow gap.

## Historical base pass

The original small foundation pass established qualified profiles, explicit directed transitions, Core-only fallback, configuration identity, stale-state invalidation, action disposition, editable Mermaid sources, and a dependency-free simulator. It remains historical/regression code only.


## 0.4.2 — StageHandoff001 reviewed-baseline branch (2026-09-10)
Reproduced the real 0.4.1 baseline (81 tests), added bounded TaskRecord/state
handoffs, stage sealing, exact-source completion, atomic record/config publication
and qualified Core-only returns. Added 47 test methods for a total of 128, including
static boundary regressions and the new demo. Full proof limits are in
STAGE_HANDOFF_001.md. Qualification/Nexus remain design/fixtures, not the later
notes-only 0.6.0 claims. No neural experiment or generic Runtime changes.
