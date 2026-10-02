# NSS failure-first instrumentation — addendum v0.1

**Record:** ACP-NSS-OBS-001 / RLOG-FAILURE-FIRST-001  
**Date:** 25 September 2026  
**Status:** User direction recorded; concrete implementation and fixture plan proposed, not implemented or executed.

> User direction: “Assume everything breaks. Have the wiring in place so that we have every failure documented and why.”

## 1. Decision and scope

Make diagnosability a design requirement of NSS research, rather than an analysis step improvised after a disappointing score. Before running an experiment, declare how each important boundary can fail, what evidence would expose it, how the evidence survives an interruption, and which observation or controlled diagnostic could distinguish competing explanations.

The requirement is not a promise of perfect observability or automatic root-cause discovery. Within a declared capture envelope, account for every attempted operation and evaluated outcome. A missing record, an unacknowledged operation, an untested mechanism, and an unknowable target distinction must remain explicit. “Cause unresolved; here is the retained evidence and the next discriminating test” is a valid finding. A convincing story without evidence is not.

This addendum supplements the Architecture Ledger v0.1 and NBR02-DC01 proposal v0.1. It does not overwrite them, authorize experiments, alter scientific thresholds, increase budgets, or promote a proposed logger into an implemented architectural component. NBR-01 remains CLOSED_BOUNDED_RECOVERED_EVIDENCE. NBR-02 remains ACTIVE_PROTOCOL_PREPARATION. RET-MW01-FIT-001 remains PARKED_OPEN.

## 2. What the existing proposal already provides—and what this adds

NBR02-DC01 already proposes pre-update scoring, one pending receipt, immutable cue-time parameters/traces, independent derivatives, full adaptive replay, all-attempt accounting, and detailed retained arrays. These are proposed controls, not executed capabilities. [S1 §§3–5, 8–11]

Add an explicit connection among those records: a failure catalogue, first-observable-divergence report, separate observed-versus-inferred explanations, a ledger for the health of the recording system, and declared synthetic fault fixtures. Logging more numbers alone is not the objective; the records must answer a question about where expectations and execution first differ.

The rationale is visible in earlier evidence: TS03 could report correct bindings while reporting wrong derived work. That dissociation did not prove that its hidden state was correct or uniquely identify a decoder defect. [S4 §7, provided Codex analysis] The instrumentation must preserve that distinction rather than translate every output error into an invented internal diagnosis.

## 3. The end-to-end evidence chain

Use stable run, attempt, fit, condition, transaction, event, receipt, checkpoint and update identifiers. Give each accepted operation a monotonic sequence number and explicit parent links. Use wall time for operational timing, not as a substitute for causal order.

| Boundary | Required observation | What a mismatch can establish |
|---|---|---|
| Source/configuration → actual inputs | Source/environment identities, split, causal input bytes, generator decisions, isolated label timing, shape/dtype/finite checks | Source mismatch, generation/label disagreement, unsupported test coverage, or illegal information availability |
| Public input → prediction | Permitted prefix, pre-update parameters, state before/after, raw logits/probability, decoder rule, state reset and routing decisions | An incorrect raw prediction; independent arithmetic may further localize implementation errors |
| Prediction → pending learning record | Receipt/scope/version, cue-time graph evidence or eligibility arrays, ownership/copy policy, creation digest, required reset lifetime | Missing, aliased, mutated, stale or incorrectly associated learning evidence |
| Pending record → accepted feedback | Released receipt, public validation results, pending identity, completion status, rejection reason | Wrong-scope, duplicate, late, absent or misbound feedback; not the hidden truth of a plausible authenticated label |
| Accepted feedback → raw derivative | Cue-time prediction/target, all derivative inputs, G/L raw gradients, independent same-state reference | Formula, graph-connectivity, retention or arithmetic disagreement when supported by the reference |
| Raw derivative → changed parameters | Learning rate, clipping norm/factor, raw and clipped derivatives, pre-step/projection/post-step parameters, attempt and commit records | A correct derivative applied incorrectly, or an update that was never acknowledged |
| New parameters → adaptation/retention | Before-update predictions, fixed development panels, per-cue recovery and no-update comparisons, fresh-state inventory | Failure to learn/recover or loss of unchanged associations, without assuming its internal cause |
| Raw output → verdict | Independent decoded outputs and denominators, per-case errors, original gates, separate safety-filter outputs | Scoring/filter/report errors rather than an improved raw learner |
| Evidence → delivered archive | Artifact identities, required-member list, declared restoration, relocated re-score and receipts | Missing/corrupt/incorrectly packaged evidence, independently of model accuracy |

For future maintained-workspace experiments, add legal writer inputs, before/after slots, writer reason, revisions, consultation points, encoded embeddings, affected state banks, and raw heads to the same chain. This is proposed monitoring, not permission to feed the evaluator's correct progress into the model.

## 4. The failure record

Each record must identify the observed symptom, expected contract, actual evidence, earliest *observable* divergence, scope of checks performed, affected outputs, and immediate action. Earliest observed divergence is not necessarily the first internal cause. Later errors may share a parent failure without being removed from task denominators.

Keep three explanatory layers distinct:

- **Observation:** directly measured or independently recomputed facts, including a failed assertion and its values.
- **Localization/inference:** a bounded explanation supported by those facts, with viable alternatives and unobserved boundaries.
- **Mechanism claim:** supported by a separately documented intervention/reproduction that changes the suspected mechanism while checking relevant alternatives. An injected fixture proves detection of that injected fault, not the cause of every superficially similar scientific failure.

A record may have cause status NOT_ASSESSED, UNRESOLVED, HYPOTHESES_ONLY, TESTED_LOCAL_MECHANISM or EVIDENCE_UNAVAILABLE. Do not require a numerical confidence score without a justified calibration method. Do not force a root-cause label just to complete a report.

FAILURE_RECORD.schema.json supplies a proposed machine-readable envelope. It is a record schema, not an implemented logger. Known expected negatives, rejected malformed inputs, surprise errors before a reversal receipt, learned errors, infrastructure failures and missing observations remain separate categories.

## 5. NBR02-DC01: distinguish the candidate failure explanations

The current mathematical contract says that one pending prediction retains the correct cue-time weights and graph/trace until its receipt. Fillers are paid-for work but not ancestors of the earlier prediction. Therefore, for a fixed cue/outcome order, each arm's update trajectory is expected to be delay-invariant. [S1 §§2–5, 8]

The proposed instrumentation should establish, in order:

1. Was the causal cue and its scored prediction recorded before label release?
2. Did a legal receipt identify the actual pending transaction, and was the retained parameter version still applicable?
3. Did retained cue evidence remain unchanged over the intervening events?
4. Did the derivative match an independently reconstructed derivative at the **same pre-update weights and cue state**?
5. Did clipping, the optimizer step and projection reproduce their declared operations?
6. Did the resulting parameters match the logged committed checkpoint?
7. Did subsequent changed-cue and unchanged-cue behavior satisfy the separately declared learning criteria?

G and L trajectories can differ by floating-point effects. Comparing two gradients evaluated at slightly different weights is not sufficient to diagnose a derivative bug. Compare each against its own independent same-state reference first. G/L equivalence in real arithmetic is a design property, not an executed verification result. [S1 §4, §8]

A zero derivative, a saturated activation, a loss increase on a later example, or a projected update is not automatically an implementation error. Record the measurements; assess them against the specified equations and task. A numerically correct update may still be ineffective for the scientific objective.

**Hypothetical example, not a new result:** a delayed update is ineffective. The receipt identity and parameter version match, but an eligibility buffer's digest changes during filler processing even though it should be immutable. That establishes a retention-contract breach. A separately authorized cloned-buffer reproduction could test whether overwrite/aliasing caused the derivative discrepancy. Until that mechanism is tested, do not write “aliasing confirmed.” If gradients and steps are correct but behavior remains poor, the issue belongs to learning competence/retention, not automatically to the delay machinery.

A correct-ID but wrong authenticated target may not be distinguishable from a real environmental reversal using the allowed observations. Report that information limit; an isolated gold ledger must not secretly become a deployed detector. [S1 §5]

## 6. Different failures require different actions

| Failure class | Proposed action |
|---|---|
| Scientific miss under a valid admitted protocol | Keep raw errors and complete the authorized finite evaluation; do not retune or hide them |
| Immediate-feedback admission failure | Preserve all development evidence; do not generate held-out conditions or relabel it a delay failure |
| Engineering validity failure: causal leakage, illegal update, broken source identity, numerical/replay disagreement | Emit failure evidence and stop the affected run as incomplete under the protocol; do not continue on a reduced denominator |
| Budget/resource stop | Preserve partial artifacts and attempted/in-flight counts; no clock reset, sample deletion, or automatic extension |
| Observation system failure: logging gap, missing commit, broken archive, unknown terminal status | Mark the evidence boundary explicitly; stop when required evidence can no longer be preserved |
| Expected negative/control case | Retain and score under its declared purpose; an expected wrong model answer is not an engineering crash |

The original scientific and engineering gates remain those in the future accepted protocol. A new stricter observation stop, fault suite, or storage policy must be versioned before dispatch; this document does not silently change an ongoing run.

## 7. Assume the recorder can fail too

Before an operation that can mutate learning state, append and flush an intent record containing a reserved attempt ID, pre-state identity and operation identity. After completion, append an acknowledgment with post-state identity and artifact references. Pin the persistence policy before execution; memory buffers, a process-local printout, and a durable commit are not interchangeable.

An independent lightweight supervisor should track worker heartbeat, monotonic completed sequence, last durable checkpoint, logs/artifact size and resource headroom. Keep the worker's evidence sink separate from its input interface. A supervisor is not immune to host/storage failure, and hashing does not make deletion impossible.

After an interruption, classify an intent without a completion as **completion unknown**. Charge its attempt; never assume failure means no mutation occurred and automatically repeat it. Resume only from a documented safe completed boundary under an explicitly allowed recovery policy. Retained G audit inputs are not a portable serialized live autograd graph. [S1 §10]

Reserve a small preallocated emergency summary area or equivalent bounded fallback before main execution. Pin its size within—not above—the authorized output ceiling. If evidence durability cannot be established, state the last durable event and the uncertain interval. Simultaneous worker, supervisor and storage loss cannot be promised away; a missing evidence interval is itself a recorded limitation.

## 8. Test the detectors before trusting them

FAULT_MATRIX.md proposes deliberate synthetic faults covering identity, retention, derivatives, update application, observations and delivery. Freeze expected assertions and signatures before executing them. Keep injected failures separate from naturally occurring scientific misses and from historical results.

Prefer non-neural fixtures, small fixed arithmetic examples and copies of retained fixture records. Mutation of copied arithmetic inputs can test an auditor without secretly applying another learner update. A pure logging or packet test needs no model at all. A graph-retention, end-to-end optimizer or full replay test may genuinely need neural operations; count those operations and obtain the corresponding budget before running them.

Fault-test success requires the appropriate detector to identify the declared breach, retain evidence, and take the intended action. Include clean controls so “reject everything” cannot pass. Pin tolerated numerical perturbations and illegal mutations separately. Include a logger/manifest fault: a monitor that never tests its own evidence pathway is insufficient.

This is a proposed finite catalogue, not “every possible failure.” Mark untested paths as untested. No faults were injected in preparing this addendum.

## 9. Observability must not become a hidden advantage or an unlimited archive

The learner reads only legal public events and its declared state. The scorer may see released labels and protected truth, but its explanations and computed correct gradients never flow into the learner. Observers must not mutate tensors, consume scientific RNG streams, detach an intended gradient path, add a target-dependent branch, or maintain an undisclosed answer cache. Measurement changes that affect the learner require a new scientific design.

For this proposed tiny learner, retaining full required numeric update evidence is practical enough to budget explicitly; actual fit within the caps still needs preflight. More generally, choose required full evidence before a run and cap optional diagnostic detail, not denominators. Use lossless chunked arrays, reference repeated bytes and retain failure indices. A hash without its underlying required evidence is an identity check, not a replayable record.

Publish collection, independent analysis and learner-only cost components separately. Actual instrumentation overhead stays in the run's resource ledger. Sampling intervals and blind spots must be documented. A ring buffer alone does not preserve every historical failure unless its required windows were durably flushed before overwrite.

The current DC01 proposal schedules 8,636 update attempts within a proposed 9,000 ceiling, leaving 364 unallocated attempts. It also specifies cell/head/time/memory/evidence caps. [S1 §9] Those spare attempts are not blanket permission to spend them on this catalogue. Bind required checks to the existing counted fixture where semantics match; otherwise revise the ledger and proposal before authorization. No additional numerical work is authorized by the user proposing this design principle.

## 10. Preflight acceptance and final report contract

Before execution, the reviewed implementation should provide: a finite failure catalogue; identifiers and schema; mandatory artifact inventory; independent scoring/arithmetic plan; observer isolation policy; non-neural and any counted neural fault tests; resource/durability headroom; and safe incomplete-run semantics. There must be enough evidence to distinguish a bad answer from a bad updater and a bad updater from a bad log.

The final report should state:

- Every scientific gate, per-condition/fit denominators, raw failures and partial attempts.
- Every declared invariant and fault fixture: passed, failed, not reached or not tested.
- The earliest observed mismatch for each grouped incident, its downstream scope and linked evidence.
- What is known, what was only hypothesized, which causal diagnostics actually ran, and what remains unresolved.
- Evidence gaps, exact replay/rescore scope, instrumentation cost, and a bounded next test rather than a retrospective story.

An experiment can be scientifically negative and diagnostically valuable. It can also have verified byte replay while remaining mechanistically unexplained. Report both dimensions; neither converts a scientific failure into a pass.

## 11. Architecture and program linkage

**Proposed architecture change:** ACP-NSS-OBS-001, a cross-cutting failure-evidence contract, not another core or a replacement for the advisory Validator. Link the existing observation, recurrent-state, maintained-workspace, exact-evidence, eligibility, update/cursor, and execution/authority boundaries. The relevant existing registers include ST-09 (fast adaptation/eligibility), ST-10 (optimizer/gradients/cursor), ST-12 (runtime/authority metadata), and IF-01 (observation → context/state). [S2, INTERFACES_AND_STATE.md]

Observer authority is separate from learner authority. An arithmetic auditor that sees a released target is not an autonomous model validator and does not get to repair raw model output. Preserve Primary/Secondary/Tertiary/Validator roles and all historical evidence limits.

For Codex, the requested next step is to integrate this contract into its proposed design, list reused versus new checks, and cost it. Do not launch a side experiment, expand the scientific task, or reopen the parked workspace branch. This is instrumentation for a falsifiable study—not an additional uncontrolled learning intervention.

## Sources and evidence tier

- **S1:** NSS_NBR02_DC01_Proposal_v0.1/PROPOSAL.md and CHAT_PROMPT.md. Proposed design, not execution evidence.
- **S2:** NSS_Architecture_Ledger_v0.1/ARCHITECTURE.md and the ZIP member INTERFACES_AND_STATE.md. Existing design and evidence organization, not a current runtime audit.
- **S3:** NSS_NBR01_Bounded_Closeout_Decision_v0.1.md. Accepted bounded phase decision.
- **S4:** Supplied Codex analysis “TS03-CR01 v0.4: what the failed composition test changes,” paragraph 7. Interpretation of the compact handoff; raw numerical claims were not independently reproduced by that review.
- **S5:** Current user instruction, quoted at the start. New direction.

The wiring, schema, failure matrix and architectural record in this package are newly proposed here. Only document generation, schema/static checks and archive integrity checks were performed; no model, scientific generator, gradient engine, fault-injection harness or learner was executed. SOURCE_IDENTITIES.json records exact identities for the locally available sources used. Historical manifests/results were not freshly requalified.
