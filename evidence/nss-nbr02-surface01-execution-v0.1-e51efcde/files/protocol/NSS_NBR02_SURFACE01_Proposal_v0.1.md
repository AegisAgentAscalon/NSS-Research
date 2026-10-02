# NSS NBR02 SURFACE01 — Selective Update / Continuation Screen

**Version:** Proposal v0.1  
**Status:** REVIEW PROPOSAL — no scientific execution performed; not a frozen execution dispatch.  
**Question:** Can a small recurrent learner acquire a corrected association while preserving an unrelated unfinished computation, and which update surface causes any damage?

## 1. Scope and evidence basis

This proposes a new synthetic diagnostic. It does not preserve tri-core as a required architecture, compare core counts, reintroduce overlays, choose a production architecture, or reopen RET-MW01-FIT-001.

The source is the user-supplied `NSS_Research_and_Architecture_Chat_Handoff_v1.0.md`, especially its STATEBRIDGE01 report (line 132) and saved readout-by-recurrence comparison (lines 251–257). That source reports initially readable saved states followed by poor continuation. Its original whole-prefix numerical gate failed, so it is motivation, not qualified causal evidence.

The original STATEBRIDGE execution payload is not attached to this conversation. This study therefore uses fresh models and a newly specified task. It is not a reproduction of that study, does not restore its missing provenance, and cannot retroactively qualify it. All settings and thresholds below are proposed design choices, not settings recovered from the old experiment.

## 2. Main hypotheses

- **Output interference:** Updating the answer readout can damage A even when its state-transition machinery is unchanged.
- **Transition interference:** Updating the transition block can damage subsequent A computation even when A retains its original answer readout.
- **Restricted sufficiency:** For this association-correction task, a readout-only update may learn B adequately without requiring a transition update.

These are not mutually exclusive. Failure of B acquisition prevents a retention-only success claim. A null result is allowed: if ordinary full updating does not harm A under this recipe, the study has not demonstrated a need for protection.

## 3. Fresh test problem

### Task A: interrupted eight-item checklist

Maintain eight completion flags, initially all false. Events are `SET(i)`, `CLEAR(i)`, `RESET`, and `NOOP`. After each event, predict the smallest incomplete item (classes 0–7), or `DONE` (class 8) when all items are complete.

The network receives individual events only. It is not given the current bitmask, the answer, a valid-action list, a computed progress field, or an oracle correction. Deterministic code supplies explicit task identity and preserves task-local state. These are engineered conveniences, not learned routing.

Use 26-dimensional one-hot inputs: eight SET tokens, eight CLEAR tokens, RESET, NOOP, and eight B cue tokens. The shared output has nine logits. A labels come from an exact independent checklist oracle. Predictions do not feed back as future inputs: this is a controlled open-loop event-stream diagnostic, not an autonomous planning benchmark.

Fresh training episodes have 32 events. The generator must expose all nine answer classes, repeated operations, clearing previously completed items, reset, and no-op intervals; it must not rely on an easy majority `next item = 0` distribution. The exact generator distribution and source hash are a required implementation-freeze item, not something to choose after the main fits.

The confirmation panel contains 32 new histories per parent, balanced across four declared families: ordinary mixed edits; repeated/idempotent edits and no-ops; clears/revisions; and reset-containing histories. Half interrupt after 8 events and half after 24. Each has a 128-event suffix, with readings at the boundary and after every subsequent event. Report horizons 8, 32, and 128 separately. The first 32 continuation events form the main screen; 128 is a separately reported extrapolation stress test, not a way to average away shorter-horizon failure.

Histories are held out, not checklist states: the task has only 256 exact masks. Do not claim novelty merely because a new RNG seed was used. Deduplicate exact histories across training and confirmation, log any finite-state overlap, and retain all confirmation histories rather than filtering for parent success.

### Task B: a revised association

There are eight identifiable cue tokens. Initially, cue `c` has binary label `c mod 2`, using output classes 0 and 1 within the same unmasked nine-class head. Each B presentation begins from zero recurrent state, separate from saved A state.

Four independent correction contexts reverse cues 0, 3, 4, and 7 respectively. Each context starts from the same parent; changes do not accumulate across contexts. Only one label changes in each context. The other seven remain valid obligations.

Each adaptation batch includes all eight current cue-label records, once each. Thus old-B rehearsal is supplied equally to all adaptive conditions. A events, A targets, A hidden states, and A confirmation results are never included in the adaptation loss.

This is learning a finite factual association, not demonstrating general procedural skill or held-out cue generalization. The corrected cue is intentionally trained and tested; call that acquisition, not generalization. The B correction does not invalidate any A target.

## 4. Model and paired intervention

Proposed learner: `GRUCell(26,64)` plus `Linear(64,9)`, without dropout, normalization buffers, adapters, or other adaptive surfaces. This is a small diagnostic instrument, not a proposed final NSS backbone.

Let the original transition be F0 and original readout be H0. The transition block includes ALL GRU input weights, recurrent weights, and biases. Freezing only the hidden-to-hidden matrix would not satisfy the frozen-transition condition.

| Condition | B learning changes | A transition | A readout |
|---|---|---|---|
| F-SHARED | Readout only | F0 | Updated H |
| F-COPIED | B readout only | F0 | Original H0 |
| U-SHARED | Transition and readout | Updated F | Updated H |
| U-COPIED | Transition and B readout | Updated F | Original H0 |

Every condition begins with identical parent values. A copied readout is an exact, independently stored copy, never random initialization. There is no hidden normalization state, optimizer weight decay, input adapter, or output-to-state feedback that can change A in the fully protected control.

### Four comparisons, only two distinct learning paths

Since A supplies no adaptation loss and A predictions never affect B inputs, the shared-versus-copied distinction does not change the B training graph. For each parent and correction, train only:

1. F0 frozen, H trainable.
2. F and H trainable.

At each saved stage, evaluate each resulting state path through both its updated H and the original H0. This is equivalent to the four cells above under the declared conditions. Verify the equivalence with a development fixture; do not reuse this shortcut in a later protocol with A replay, coupled optimization, or output feedback.

The B trajectory is therefore identical within each shared/copied pair. This makes the readout contrast particularly clean and avoids counting duplicate training runs as replication.

**Interpretive constraint:** F-COPIED preserves A by construction. Its retention is an implementation invariant, not a learned preservation discovery. Its useful empirical question is whether B also learns and retains its seven other associations. Added readout storage and explicit task routing still count in costs.

### Controls

- **NO-UPDATE:** Original model and state; should retain its baseline A behavior but fail the revised B obligation.
- **Exact checklist oracle:** Validates labels and scorer behavior. It is a software reference, not neural evidence.
- **Reset-state ablation fixture:** Paired different prefixes with identical subsequent events must demonstrate that the task actually requires retained history. This is a harness sanity test, not a new fitted method.

## 5. Training and bounded workload

### Proposed fixed recipe

Four fresh parent seeds: 4101–4104. No seed replacement or checkpoint selection. One disposable engineering-probe seed: 4199, excluded from all results.

Each parent receives exactly 2,000 optimizer updates. Proposed parent batches contain 32 A streams of length 32 plus all eight reset-state B cues. Loss is the equally weighted mean of A cross-entropy and B cross-entropy. Only the final scheduled parent checkpoint is admitted; intermediate checkpoints are retained for diagnosis, not selection.

For parent fitting and B adaptation, use Adam with learning rate 0.003, betas (0.9, 0.999), epsilon 1e-8, no weight decay, and active-parameter global gradient-norm clipping at 1.0. Use the same scalar settings in both adaptation paths. Start a fresh optimizer at the parent-to-adaptation boundary; do not inherit unequal momentum histories. Record gradient norm, clipping scale, and actual parameter change by block. This is a fixed-recipe comparison, not equal-update-norm or optimally tuned performance.

Each parent produces four independent correction contexts and two learning paths per context, each with 64 B updates. Save/evaluate stages 0, 1, 2, 4, 8, 16, 32, and 64. Final acquisition is decided at stage 64, not the best observed stage. Intermediate results describe candidate-stage behavior; A is suspended, so do not mislabel them as actual user exposure.

### Optimizer application budget

- Parent fitting: 4 × 2,000 = 8,000.
- B adaptation: 4 parents × 4 corrections × 2 paths × 64 = 2,048.
- Fixed engineering cost/resume probes: one parent-style and two adaptation-style probes, 16 updates each = 48.
- **Total maximum: 10,096 optimizer applications.**

No extra fits, repairs, translator training, hyperparameter search, failed-seed replacements, or retry training are included. Inference, reference checking, backward work, serialization, and proof replay are separately metered; this update count is not a complete compute budget.

Proposed resource caps are 2 GiB process RSS and 512 MiB delivered evidence, including a predeclared reserve for stop/failure records. Runtime and numerical-array volume require a measured preflight estimate against the execution environment before dispatch freeze. If the planned workload cannot fit, stop and revise the proposal before main work, not the evidence after results. No completion-time claim is made.

## 6. Admission and outcomes

The following are proposed engineering thresholds, not population guarantees or inherited historical gates.

### Parent competence

Before any main B adaptation, require each parent to achieve, on a separate development/admission panel, at least 99% A event accuracy and 95% completely correct 32-event continuations in each family, zero false-DONE predictions, and all eight original B labels correct with true-label probability at least 0.80.

If any parent fails, record `STOP_BASELINE_COMPETENCE`; retain all seeds and diagnose the fixed recipe. Do not delete weak fits, increase training, or open confirmation to find a favorable subset. Main confirmation generation and access occur only after this admission and implementation freeze.

A confirmation-time parent failure remains visible and can invalidate a joint pass for that parent/context; it does not justify removing those histories. Report absolute performance and damage relative to the parent separately.

### Joint screen, evaluated per parent and correction context

At the final B stage, a condition passes this bounded screen only when all are true:

1. Corrected B label is correct with probability at least 0.80; every unchanged B cue is also correct with probability at least 0.80.
2. On A CARRY at horizon 32, event accuracy is at least 99% and wholly correct continuation rate at least 95%, separately in each family.
3. Relative to NO-UPDATE on exactly the same histories, A event accuracy drops by no more than one percentage point in any family, and there are zero newly introduced false-DONE predictions.
4. Numerical, state-isolation, provenance, and resource admission checks pass.

An all-context replication screen requires all four correction contexts to pass within a parent, and all four parents to meet that screen. Report every individual outcome even when the overall screen fails. Confidence/margin and loss changes remain mandatory diagnostics even when they do not cross a class-error threshold; class retention alone is not a general safety claim.

REBUILD is a separately scored remedy, not a substitute silently used to pass a failed CARRY condition. A condition can be classified as `CARRY_FAIL_REBUILD_PASS`; that is a useful result, not a CARRY pass. Long-horizon results at 128 must be reported against the matching parent reference even if the parent itself is imperfect there.

## 7. Continuation measurements

At every saved B stage, clone the original suspended A state; evaluation must not modify the learner or the canonical suspended state.

- **CARRY:** Apply the remaining event sequence to the original saved A state using the condition's transition and readout.
- **REBUILD:** Recompute the exact supported prefix from zero under that condition's transition, then apply the identical remaining sequence. Replay events only; never replay stale optimizer steps or overwrite the original evidence.

Read the interruption boundary without applying an extra query transition. Save subsequent per-event logits and targets. Measure boundary accuracy, event accuracy, whole-continuation correctness, first error position, false DONE, and true-label loss/margin change versus the parent. Show horizons 8, 32, 128 and per-family results separately.

Distinguish worst damage along a resumed continuation from worst damage across sampled update checkpoints. Checkpoints 3, 5–7, etc. are not observed for A, so do not claim an every-update trajectory guarantee. B can be logged at every adaptation update cheaply, but that does not fill gaps in A evaluation.

The independent replication unit is the parent fit (four), not the number of readouts. Correction contexts and prefixes are paired observations nested within a parent. Report per-seed tables and paired contrasts; do not manufacture large-sample certainty by treating every event as an independent experiment.

## 8. Failure-first and numerical verification

Pin actual software versions, device, thread count, dtype, batching, operation order, source hashes, task generation, and RNG streams before main execution. Proposed main arithmetic is CPU float32 with deterministic settings; log the actual environment rather than presuming a version from online documentation.

Three checks remain separate:

1. Exact preservation of parameter/state/fixture bytes that are supposed to be unchanged, including readout non-aliasing and checkpoint round trips.
2. Fresh-process deterministic replay on the same canonical implementation and execution shape.
3. An independently written GRU-equation reference, evaluated over complete prefixes and suffixes from the same stored weights and inputs, not just one-step or argmax checks.

Proposed reference envelope: `abs(actual - reference) <= 2e-6 + 2e-5 * abs(reference)` at every checked hidden coordinate and logit; discrete predictions must agree. A float64 reference can help locate float32 arithmetic differences but is not a replacement model or a post-result tolerance waiver. Check every scored main trajectory, not only favorable examples. Record the maximum discrepancy, exact offending coordinate/event, and full reproducer.

The same-implementation replay requirement is different from a claim that distinct floating-point implementations must be bit-identical. PyTorch documents that mathematically equivalent operations, batching, platforms, and versions can produce different floating-point results. The implementation freeze must resolve the checker specification prospectively. A numerical failure stops qualification; later supplementary agreement does not erase it.

Exercise clean controls plus injected faults before main work: accidental frozen-parameter mutation; aliased copied readout; wrong-task state; truncated rebuild history; stale B target; corrupted checkpoint; nonfinite tensor; and a deliberately wrong scorer target. Each expected fault must be detected. A failure record contains phase, parent/context/condition/stage, expected versus actual, input/weight/state hashes, minimal reproducible evidence, and stop disposition. Distinguish an observed symptom from a confirmed cause; `CAUSE_UNRESOLVED` is preferable to inventing an explanation.

## 9. Required evidence package

Retain the versioned protocol and source, environment lock, exact fixtures or lossless deterministic generators with draw records, parent and scheduled adaptation checkpoints, optimizer/RNG state sufficient to resume, per-event logits/targets, per-cue B outputs, metrics, update masks/norms, resource measurements, fault-test receipts, and a failure ledger. Archive parameter snapshots once where shared/copied evaluations use identical values; record that reuse explicitly.

Store full hidden-state trajectories for the fixed checker/failure fixtures and all failure reproducers. For other trajectories, saved inputs, starting states, weights, operation specification, and per-event logits must support reconstruction and rescoring without retraining. Preflight accounts for the actual record counts and shapes. Do not duplicate arrays to inflate a proof package, silently discard failures, or claim compression ratios before measurement.

Provide SHA-256 hashes and an inventory manifest; verify archive integrity. Label fresh-process replay as internal reproducibility, not independent third-party replication. Report total retained and peak memory, model/optimizer/state bytes, B learning cost, A rebuild cost, checker cost, and archive size. Parameter count alone does not settle efficiency.

## 10. Interpretation and bounded next decisions

- If F-SHARED damages A while F-COPIED preserves it, the readout change causes that contrast under an unchanged transition.
- If U-COPIED damages A while F-COPIED preserves it, a changed transition can disrupt continuation despite an original A readout. Compare CARRY/REBUILD to distinguish stale-state compatibility from changed computation that also fails on rebuilt history.
- If U-COPIED preserves A and learns B, this task does not require completely freezing the transition.
- If F-COPIED preserves A but fails B, isolation is insufficient under this recipe; it is not an acceptable learning solution. This does not prove that no readout-only optimizer or representation could learn B.
- If both update paths learn B and all conditions retain A, no interference advantage has been demonstrated on this task.
- If the parent cannot learn A, the experiment stops at baseline competence, not a claimed continual-learning failure.

A positive result can identify a useful update boundary for a finite association task. It cannot establish that a frozen backbone plus small modules can acquire genuinely new procedures, that a state translator works, that low-bit traces work, that lifelong learning is sustainable, or that any complete NSS architecture is selected.

The next mechanistic question should follow the result; continuation rehearsal or state translation is not automatically added to this run. A later skill-acquisition task must not be satisfied merely by memorizing revised cue labels.

## References and execution-freeze checklist

**Provided history:** `NSS_Research_and_Architecture_Chat_Handoff_v1.0.md`, STATEBRIDGE01 summary (line 132), prospective saved diagnostic (lines 251–257), evaluation/lifecycle boundaries (lines 220–237). Later conversation supersedes its requirement to preserve tri-core as the default architecture.

**External implementation reference:** PyTorch official GRUCell documentation and Numerical accuracy note, consulted for the cell equation and floating-point verification boundary. The web's current documentation version is not an environment lock.

Before this becomes an executable dispatch, freeze the exact A generator and family definitions; admission and confirmation fixtures/seed separation; model initialization and environment; optimizer implementation; reference checker and fault injections; record layouts; resource forecast and stop reserve; and the source/protocol hashes. No learning result has been generated while preparing this proposal.
