# Layered review and two-timescale maintenance
## ACP-NSS-LAYERED-MAINT-001 / DEC-NBR02-SCOPE-002 · v0.1 · 25 September 2026

**Status: proposed architecture elaboration during USER_DIRECTED_EXPERIMENTAL_HOLD.** This document records and develops the user's ideas. It does not select production thresholds, implement a reviewer, perform numerical analysis, authorize learning, or overturn any historical result. It supplements DEC-NBR02-SCOPE-001; the parent's experiment pause remains in force.

## 1. The user direction being captured

The user proposes a somewhat permissive filter so useful adaptations are not unnecessarily rejected; small periodic repairs plus a larger, less frequent repair; and review that limits both harmful accepted changes and beneficial changes incorrectly blocked. The subsequent clarification proposes applying this at multiple levels associated with NBR-01 and NBR-02, using maintained tokens for review coordination and the Tertiary core for a deeper review and correction of recorded changes since the previous dream.

**Working interpretation:** a shared change-journal and review interface, with layer-specific evidence and repair operations, followed by periodic broader consolidation. This is not one universal filter equation or a claim that identical mechanisms solve state drift and weight interference. NBR numbers name research tracks, not additional physical cores or literal neural layers.

## 2. What can be shared, and what must remain different

| Domain | Changing object | Typical review question | Candidate corrective operation |
|---|---|---|---|
| State/evidence continuity, associated with NBR-01 | Selected reference, task state, goal, evidence revision, workspace | Is the current work still tied to the intended task and current lawful evidence? Which conclusions are stale? | Resolve references, mark uncertainty, invalidate dependent results, recompute work from preserved evidence, or use a declared state reset/rebuild. |
| Parameter learning/retention, associated with NBR-02 | Permitted adaptive parameters and learning records | Did the candidate acquire the new behavior, and what happened to protected old behavior? | A budgeted rehearsal/update intervention on an isolated candidate, additional evidence review, or nonadoption. |
| Cross-revision compatibility | Existing recurrent state interpreted by changed parameters | Does this unfinished state remain meaningful under this exact parameter/schema revision? | Qualified migration, replay/rebuild, or explicit reset. Equal tensor dimensions are not enough. |

Shared infrastructure can record before/after revisions, scope, source receipts, anticipated affected capabilities, observed changes, uncertainty, and review disposition. It cannot replace the distinct correctness checks in the table. Refreshing a metadata field does not repair a learned parameter change; a rehearsal batch does not establish that a task reference is correct.

The source studies do not establish the third row: the recent NBR-02 query paths use fresh temporary state. Do not retrospectively diagnose state/weight incompatibility in experiments that excluded it. [S01 §§2,5; S04 §§11,15]

## 3. The bounded token workspace is a review interface, not a reviewer

The maintained token lane can keep the live review organized without retaining a full transcript. It could carry the active task/scope, current change identifier, evidence-version reference, candidate-versus-accepted status, unresolved issue reference, and the last fully accounted review cutoff.

Readable example, **not a selected grammar or a token-count claim**:

```text
task=plan_A
change=chg_314
kind=parameter_candidate
evidence=batch_27@r4
status=pending_review
risk_record=audit_314
last_dream_cutoff=evt_260
```

A model/controller interprets the fields, retrieves evidence, performs permitted checks, and writes supported status changes. Tokens themselves neither perform review nor authorize execution. A generated `safe` or `verified` label is a claim to check, not independent evidence. Store extensive scores, dependencies, incident records, and the change history in the exact archive/larger Working Space, referenced by the bounded workspace.

Residency, consultation, rewrite cadence, review cadence, and repair cadence are separate choices. A small resident packet need not be rewritten each recurrent iteration, and consulting it need not trigger training. Native learned review using that lane remains untested; earlier deterministic packets and native metadata-conditioning studies do not constitute an implemented autonomous review system. [S04 §§6,7,12,13; S03, "Maintained management workspace as a phase organizer"]

## 4. Accept bounded disruption without creating an unlimited ratchet

Leniency should be tied to what changed, its severity, confidence in the evidence, the affected scope, and a repair/availability deadline. It should not mean an unconditional larger allowance for every operation.

**Separate hard integrity requirements from performance trade-offs.** Invalid source authority, a lost update-completion record, an unsupported parameter-version combination, or a hypothetical label promoted to fact must not be excused as a small accuracy cost. Behavioral variation on a declared noncritical panel may receive a prospective tolerance; severe or out-of-scope regressions require a different disposition. These categories and their operational thresholds remain to be specified.

A change can improve its focal task and damage another task. Therefore, “correct adaptation” must not mean merely “the new answer is right.” Assess new benefit and old impact separately before giving an overall disposition. Legitimate revised facts are not immutable old targets: preserve the historical event while testing current behavior against its current evidence context.

Proposed review dispositions are **accept within declared limits**, **defer for evidence or bounded repair**, and **reject for a stated violation**. A provisional status is not an implicit permission to serve intermediate candidate weights. Any permitted user-visible bounded degradation must be stated at the accepted-revision boundary, independently of the larger internal candidate tolerance. Rejected or deferred changes remain reviewable; no indefinite silent deferral.

Use a stable qualification anchor over a declared epoch, plus a rolling parent comparison and current per-capability evidence. Do not reset cumulative impact to zero merely because another small change was accepted. The TIMING01 analysis showed why a moving comparator can report improvement relative to its reference while the candidate's absolute old loss rises. [S02 §7]

“Disruption budget” is a policy metaphor until its metrics are fixed. Track current deviation, worst affected records, peak excursions, duration and recurrence of unresolved deficits, and feedback-to-adoption delay. Do not blindly add repeated readings of the same deficit as if they were independent damage. Do not permit gains on easy items to conceal loss on a required capability. Update baseline references only through an explicit requalification and lawful target-version policy, not a convenient dream/reset label.

## 5. Fast review and micro-maintenance

While Secondary performs task work or its permitted learning, with Primary participating, a lightweight review could inspect the selected change and its declared dependencies. The compact workspace would carry the context and pending-review reference.

For state/evidence changes, the repair may be a reference check or recomputation with **zero parameter training**. For a weight-change candidate, repair may require a small lawful rehearsal operation. These must not be called the same operation or charged as if both were cheap.

Periodic small maintenance could prevent individually tolerable disruptions from accumulating. A separate early escalation can be proposed for a widening deficit, evidence conflict, impending deadline, or missing telemetry; exact triggers must be fixed before a test. Small and large parameter steps are not necessarily small and large compute costs. The same eight gradients cost eight gradients even when their mean is scaled down. [S02 §6]

No schedule is known to be necessary or sufficient. The already measured early/late rehearsal trade-off motivates the user's two-timescale design but does not establish that combining them works. A fast review also must examine new-answer retention after maintenance; rehearsal that restores yesterday's answers by undoing today's correction is not success.

## 6. Tertiary's deeper review since the last dream

The proposed deep-review interval is a versioned journal range, not an ever-growing prompt:

1. At a safe handoff, freeze an end cutoff and checkpoint the outgoing task component. Secondary and its learning are paused under the existing schedule; Primary remains frozen and participating.
2. Tertiary opens the interval after the previous **fully accounted** dream cutoff through the new cutoff, plus any older unresolved tickets and required dependency records. Later events belong to a later interval rather than moving the current review target.
3. Account for every retained change identifier in the interval. Review state changes, weight transactions, accepted/rejected/deferred proposals, failed updates and unknown-completion incidents. The journal should expose gaps, not infer their contents.
4. Triage and retrieve details under a declared budget. Examine cumulative regressions, repeated repairs of the same capability, relationships among updates, stale derived work, and rejected adaptations that may deserve reconsideration.
5. Produce evidence-linked repair proposals, immediate permitted metadata/state corrections, or a rehearsal/consolidation manifest. Distinguish supported findings from possible explanations and untested counterfactuals.
6. Apply any parameter maintenance through its separately authorized candidate-training path. The first conservative schedule pauses Tertiary before that training phase; no concurrent Secondary learning or new write authority is inferred.
7. Qualify the candidate and compatible state, record the actual disposition, and resume. Mark individual changes as reviewed, deferred, unresolved, superseded, or outside retained coverage. Advance the accounted-through cursor only over a contiguous fully accounted range; a reviewable unresolved ticket need not disappear before its existence can be accounted for. `Reviewed` and `resolved` are different fields.

**“All recorded changes” means full interval accounting, not a promise of unlimited deep recomputation of every parameter event.** Logging and review budgets are explicit. The record must show shallow versus detailed review, missing telemetry, and the remaining backlog. Tertiary cannot diagnose evidence that was never retained. If interrupted, preserve the interval, cursor, partial findings, and remaining work; do not label the dream completed.

Raw tensor differences are not semantic explanations. Retain task/receipt provenance, public targets and revisions, parent/candidate identities, attempt/commit state, outcome evidence, and pointers to relevant snapshots or selected numerical traces. The eventual storage contract must decide what is captured at every step versus checkpointed; neither every byte forever nor silent data loss is an acceptable assumption.

Do not apply an archived gradient directly to unrelated current weights. Recompute eligible training examples at the candidate's specified version, or use a separately specified valid update scheme. Pending credit traces also bind to their cue-time parameter version and must be drained, cancelled/reconstructed, or migrated under an explicit rule. A global weight rollback can erase useful later adaptations; selective recovery is not assumed to be a simple undo of one parameter delta. [S03, "Proposed end-to-end lifecycle" and "Failure-first record requirements"; S04 §§11,15]

## 7. What the review must guard against in both directions

The user asks for few harmful approvals and few correct changes mistakenly stopped. That is a two-sided target, not simply a stricter or looser threshold.

Record accepted harmful changes, rejected/deferred changes that later satisfy the defined joint old/new criteria, correct accepted changes, and appropriate rejections. Mixed-benefit/mixed-harm and unresolved cases remain explicit. False rejection cannot be inferred merely from the proposer insisting it was right; assessing it needs separate lawful evaluation evidence and a predeclared notion of an acceptable candidate. A held-out research scorer may classify errors retrospectively but may not feed private labels into the operational reviewer.

For consequential or ambiguous cases, review may require source re-reading, independent calculations, controlled reproduction, or additional actual feedback. A second verbal opinion on the same unsupported summary does not establish independent verification. Review can reconsider prior deferrals but cannot grant itself new authority, unlimited training, or access to withheld targets.

Measure both raw candidate behavior and actually served behavior. Include new-correction availability, refusal/deferral duration, residual old impact, false-accept/false-reject counts where identifiable, and all reviewer/repair/storage costs. Reject-all and accept-all are useful reference policies; neither should be mistaken for a competent learner. Continued availability via exact retrieval is a separate system result, not evidence that neural parameters learned the correction. [S01 §§4–7]

## 8. NSS role and phase boundaries

Primary participates in active phases and remains frozen within its accepted generation. Secondary task/post-task learning and Tertiary reflection retain mutual exclusion. The neural Validator supplies fallible evidence advice, not a release veto or training permission. Authorized qualification/runtime rules own adoption. No new core, neural overlay, or always-running background service is introduced by this design.

Tertiary may correct permitted review records and produce grounded state-repair or learning proposals. Weight changes follow the separately authorized candidate path; Primary changes require a qualified new generation. Keep observation replay, independently verified synthetic exercises, and unverified hypotheses in distinct provenance lanes. Repetition cannot turn an imagined result into an observed fact. Preserve current valid corrections during rehearsal. [S03; S04 §§12–15]

The maintained token lane, exact archive, broader Working Space and recurrent state remain distinct. Their total cost includes model residency, candidate copies, old records, review indexes, native training state, temporary buffers and latency. The current cost-accounting limitation is not repaired by this document.

## 9. A narrower next question; no experiment selected

The architecture-level question is:

> Can layered, evidence-grounded review with bounded disruption allowances and costed micro/macro maintenance admit useful changes promptly, limit accumulating old-capability regressions, and correctly escalate unresolved changes across state and parameter boundaries?

This is too broad for a single causal experiment. Before numerical work, settle the protected capabilities, candidate/served boundaries, cumulative budget, repair deadlines, authority, review data, and single primary outcome.

Then specify one layer and one contrast. For example, hold candidate-training and maintenance schedules identical while testing the contribution of a review policy to accepted harm and acceptable-change rejection; or hold review fixed while comparing maintenance schedules. These are planning options, not executed or authorized studies. A model-based reviewer needs a same-information, costed deterministic/algorithmic review baseline. Learned Tertiary value needs a selector/reviewer control beyond the mere benefit of scheduled replay. A joint state/weight continuity claim needs an actually specified migration interface, not a scratch-reset toy.

The proposed shared journal can eventually support both layers, but it must not make one layer's success evidence that the other works. Cumulative plasticity requires a longitudinal task-acquisition endpoint; neither safer adoption nor old-record repair supplies it automatically.

## 10. Current status and unresolved choices

Experimental dispatch remains **PAUSED**. This addendum records the user's design direction and proposed elaboration only. It does not adopt a five-field packet, a review model, a cadence, a confidence threshold, a new optimizer, a journal storage format or a serving policy.

NBR-01 remains `CLOSED_BOUNDED_RECOVERED_EVIDENCE`. NBR-02 remains active with no new execution authorization. `RET-MW01-FIT-001` stays parked; the exact near-term skipped NBR-01 question has not been identified for dispatch. `RET-DREAM-MAINT-001` is elaborated but still deferred/unimplemented. Existing failed/stopped screens, `RET-TIMING01-BALANCE-001`, `OBS-DC01-COST-001`, and the foundation return `FCR-0103-001` remain unchanged. No parent ledger or prior archive is overwritten.

Required owner-facing decisions: permitted bounded harm and protected severe cases; per-update and cumulative reference; micro/macro cadence unit; candidate-only versus served tolerance; reviewer authority/information; repair and adoption deadlines; evidence retention/coverage; and one testable comparison. Detailed numerical design and renewed run authorization follow those decisions, not this conceptual discussion.

## Source map and evidence tier

- **S01:** `NSS_NBR02_Decision_Review_v0.1/DECISION_REVIEW.md` and `NEXT_QUESTION_CONTRACT.md` — experimental hold, separate learner/adoption questions, no-learning and hidden-evidence safeguards.
- **S02:** `NSS_NBR02_TIMING01_Analysis_v0.1/REPORT.md` — reported retained-data findings and measurement limitations. This addendum did not repeat the analysis.
- **S03:** `NSS_NBR02_REV01_Execution_v0.4/DREAM_MAINTENANCE.md` — deferred Tertiary link and evidence/scheduling/qualification boundaries. References use the source heading names; no execution result is inferred from this concept note.
- **S04:** `NSS_Architecture_Ledger_v0.1/ARCHITECTURE.md` — retained roles, state/workspace split, candidate qualification and migration. Some experiment-status labels are historical; the later reports and current hold supersede their temporal status only.
- **U01/U02:** the two user messages requesting lenient bounded-disruption review with micro/macro repair, and proposing a shared review system across NBR-01/NBR-02 with deeper Tertiary review of the interval since its last dream.

Source file hashes are in `SOURCE_IDENTITIES.json`. Only document reading/writing and byte-integrity checks were performed. No scientific claim here is independently replicated by those checks.
