# TIMING01: what the saved learning trajectories say
## ANA-NBR02-TIMING01-001 · retrospective analysis v0.1

**Disposition:** completed analysis of retained TIMING01 v0.1 evidence, not another learning experiment. The source study remains COMPLETE with both Early and Later full-trajectory confidence screens FAILED for both G and L. No model was instantiated or evaluated, no new derivative was computed, no optimizer was stepped, and no experimental stream or label was drawn. Saved weights, gradients, and logits were read as data. The source's formerly held-out observations are now exposed retrospective evidence, not fresh confirmation.

**Main finding:** later rehearsal improves the ending, but usually worsens the worst intermediate old-answer loss. Both rehearsal schedules improve old-answer quality when they act, while later focal updates systematically pull against it. The user's proposed small maintenance steps plus a larger later consolidation is therefore a useful new hypothesis, but the current records do not contain that combined intervention. Its result cannot be inferred by adding the old branches together.

**Important qualification:** all old class answers remain correct in this source's held-out grid, including the no-rehearsal strong-correction branch. The failures concern the declared confidence envelope. They are not evidence of class forgetting or loss of plasticity in this sample.

## 1. Evidence, reanalysis, and denominators

Source: `NSS_NBR02_TIMING01_Complete_v0.1.zip`, 37,195,996 bytes, SHA-256 `12a388b99a479384c601ef553b859624f29eb2c62f55a5bd7264a2308ae9256e`. The archive identity and CRC were checked. Its losslessly encoded records and aliases were restored in a separate working directory; all 168 logical manifest entries verified. The primary and already-retained replay record, message, response, and event-log files were compared bytewise by hash. That is verification of stored replay evidence, **not a fresh repetition of learning in this analysis**.

The independent extractor decoded 41,508 source frames, 130,206 array occurrences, and 29,022,292 elements, checking array descriptors and hashes. The self-contained analysis retains all scored rows, their logits, permitted labels and transactions, and selected main-update/batch arrays: 8,641 arrays with 5,498,056 elements. It does not duplicate all original training/checkpoint/fault evidence; keep the original complete study for that.

The new NumPy/standard-library analysis:

- Recomputed all 29,540 scored query classes, stable binary log losses, logit margins, and probability margins from captured logits. All classes agreed; maximum numeric difference was 8.88e-16.
- Reconstructed all 24,480 main development/held-out targets against the saved chronological released-receipt information, without generating any targets or replaying stochastic recipes.
- Reconstructed all 384 held-out method/branch/base/boundary confidence decisions. They agree with the original table.
- Rechecked all 192 development/held-out batch reductions and resulting float32 parameter-subtraction bytes using captured gradient operands, not fresh gradients.
- Verified identical immediate post-clip2 logits for E and LATE against U in all 192 corresponding development/held-out comparisons.

Most discussion below is the original **held-out** split analyzed retrospectively: eight bases × four fitted models = 32 paired model/base contexts per method; each has eight old records. The eight bases are the main association-case units. Fits, cues, repeated checkpoints, and replay are not independent new tasks. Development tables are supplied separately, never pooled into confirmation.

Sources and exact products: `inputs/`, `audit/EXTRACTION.json`, `tables/SUMMARY.json`, and `source/ANALYZE.py`. All 2,757 original negative query rows are retained, including pre-feedback surprises, frozen controls, and technical diagnostics. Correct classes with confidence failures have a separate failure table.

## 2. The shared initial failure precedes either scheduling decision

Every held-out base's first post-correction confidence check fails for both G and L under E and LATE. All eight base means fail in each case, before any rehearsal is applied. These are the same U/clip2 state, with identical old and focal logits.

| Method | Pooled old-loss increase over B1 immediately after clip2 | Allowed increase |
|---|---:|---:|
| G | 0.00953234 | 0.00637226 |
| L | 0.04667736 | 0.01000000 |

Therefore, **on these same prestates and inputs, adding any operation afterward cannot retroactively make the original all-boundary screen pass**. This is a temporal fact about an intervention, not a claim that no different model or initial correction could pass.

This matters for the user's micro/macro proposal. Such a schedule can improve recovery and maintenance after it acts. If the goal is literally no earlier confidence breach, the first correction must also be changed, or the system must implement a separately declared provisional/commit policy. Hiding that first readout, postponing only one branch's scoring, or relabeling later recovery as prevention would be misleading.

The source's strict criterion is preserved. A future protocol may separately specify an operational recovery criterion at the completion of each stage, while still publishing every pre-maintenance readout and strict-prevention failure. That is a new prospective question requiring authorization, not a waiver of TIMING01.

Evidence: `tables/SHARED_POST_CORRECTION.csv`, `BASE_BOUNDARY_GUARDS.csv`, `TRAJECTORY_AGGREGATES.csv`; inherited protocol/report in `inputs/`.

## 3. Better final answers and worse intermediate risk coexist

The previous report noted that late rehearsal had lower final old-answer loss in most cases. The reanalysis adds the **maximum mean old loss within each context** across the same six boundaries.

| Comparison: Later against Early | G | L |
|---|---:|---:|
| Lower final mean old loss | 30/32 contexts; 8/8 base means | 29/32; 7/8 bases |
| Lower peak mean old loss | 7/32 contexts; 1/8 base means | 1/32; 1/8 bases |
| Higher peak mean old loss | 25/32 contexts | 31/32 contexts |
| Lower six-boundary equally weighted mean loss | 18/32 contexts | 2/32 contexts |
| Lower final focal-answer loss | 0/32 contexts | 3/32 contexts |

All nonwinning counts in these paired loss comparisons are genuine worse values, not ties.

| Mean across contexts | G Early | G Later | L Early | L Later |
|---|---:|---:|---:|---:|
| Final mean old loss | .020179 | .013545 | .024700 | .020211 |
| Context peak mean old loss | .023244 | .025315 | .054971 | .062770 |
| Six-boundary mean old loss | .017601 | .015048 | .028703 | .035487 |
| Final focal loss | .007374 | .008821 | .006516 | .007534 |

The six-boundary mean is **not elapsed-time area under a curve**. Boundaries include intentional aligned reuses of unchanged states and are not equally spaced in time. It is one retrospective schedule-weighted description; the peak and final values answer different questions.

The final focal confidence cost is small, and every focal class remains correct. Nevertheless, later placement is not a free improvement of all outputs. For G, its final focal loss is worse in every context; for L, in 29/32.

Individual-tail risk also needs care. Late placement improves the single worst observed L old probability across the entire dataset (.648 versus .551 for Early), yet worsens the minimum old probability in 31/32 individual L contexts. One Early outlier can drive the global minimum while the typical context favors Early. Neither statistic should replace the other.

The evidence supports a timing-dependent trade-off, not universal schedule superiority, and no confidence interval treating 32 repeated contexts as IID cases is claimed.

Evidence: `PAIRED_CONTEXT_RISK.csv`, `RISK_COMPARISON_SUMMARY.csv`, `CONTEXT_RISK.csv`.

## 4. Both subsequent focal updates reliably pull against old knowledge

The recorded sequence has a strong correction at receipt3, a same-focal update at4, one protected-old-cue update at5, and another focal update at6. E rehearses after3; LATE rehearses after4.

| Method/branch | After clip2 | After early opportunity | After next focal update | After late opportunity | After old-cue update | Final focal update |
|---|---:|---:|---:|---:|---:|---:|
| G E | .013224 | .010385 | .021778 | .021778 | .018266 | .020179 |
| G LATE | .013224 | .013224 | .025315 | .013347 | .011635 | .013545 |
| L E | .050585 | .015746 | .029835 | .029835 | .021517 | .024700 |
| L LATE | .050585 | .050585 | .062770 | .015181 | .013588 | .020211 |

Both actual rehearsal steps reduce mean old loss in every one of the 32 contexts per method. Both later focal updates increase it in every context under both schedules. The focal class was already correct before those later receipts; ordinary cross-entropy nevertheless continued sharpening it.

The protected-old receipt at5 is less uniformly restorative than its mean suggests: it improves old mean loss in exactly 16/32 contexts and worsens it in 16/32 for each method/placement. It trains **one** old cue, not the whole eight-record buffer. It cannot be assumed to maintain every other old cue merely because the receipt is about old information.

These are before/after parameter-update effects in the captured short streams, not isolated idle-time memory decay. A correctly predicted cue may still benefit from confidence improvement, so the result does not prove that learning from correct examples is generally wasteful.

For the first changed-label transition, the focal before/after comparison uses the original recorded pre-feedback logits evaluated against the newly released label. Comparing its post-correction loss with the previous inventory under the old label would not be a valid same-target update effect; the analysis explicitly checks this.

Evidence: `UPDATE_TRANSITIONS.csv`, `OPERATION_EFFECTS.csv`, `TRAJECTORY_AGGREGATES.csv` and figures.

## 5. The interference pattern follows label groups across scopes

For each method and each rehearsal placement, there are 128 opposite-label old observations and 128 same-label old observations at that rehearsal (32 contexts × four records per label relation).

- At rehearsal: all 128 old records with a label opposite to the corrected focal label improve in loss; all 128 sharing the focal label worsen slightly.
- At each subsequent focal update: all 128 opposite-label records worsen, while all 128 same-label records improve.
- The pattern occurs in both scopes. No old class becomes wrong on this held-out grid.

The old-average improvement therefore does not mean that every memory improves. It reflects a beneficial redistribution of probability quality: the damaged opposite-label group recovers more than the strong same-label group gives up.

This is consistent with competing demands on shared parameters. It does not uniquely locate the cause in output bias, a particular layer, state representation, or the local derivative approximation. G and L were trained to different parameter states. A layer-specific cause or same-prestate cross-rule comparison would require a new intervention rather than a story inferred from correlations.

The per-parameter displacement shares and recorded-gradient effects are supplied as diagnostics. An exact G old-example gradient supports a first-order directional prediction at its recorded prestate. L's analogous quantity uses its approximate rule: its actual-minus-predicted difference mixes approximation error with nonlinear finite-step effects and must not be described as pure curvature.

Evidence: `LABEL_SCOPE_EFFECTS.csv`, `RECORD_CHANGES.csv`, `RECORDED_GRADIENT_LOCAL_EFFECT.csv`, `STEP_COMPONENTS.csv`.

## 6. A later batch is already a larger realized correction here

The same eight records do not yield the same gradient at different learned weights. In **all 32 paired contexts for each method**, the later batch's actual step norm is larger than the earlier one's.

| Batch diagnostic | G Early | G Later | L Early | L Later |
|---|---:|---:|---:|---:|
| Mean raw norm | .05205 | .11535 | .24736 | .30628 |
| Largest raw norm | .14288 | .48684 | .52201 | .53586 |
| Median Later/Early actual step ratio | — | 1.648 | — | 1.246 |

All 128 held-out batches are below clip1. Raising their clip ceiling alone would leave their updates unchanged. A meaningful small/large intervention must specify a learning-rate multiplier, number of applications, record count, or objective—not merely a higher inactive clip limit.

The mean cancellation ratios are about .705/.783 for G early/late and .822/.829 for L. These are not near-zero batch updates. Weak cancellation is not established as the bottleneck.

For G, the average exact-gradient dot-product prediction of old-loss change is -.003417 early and -.021857 late, versus actual changes -.002840 and -.011968. The finite-step improvement is smaller than that local approximation predicts, especially for the larger later steps. That warns against assuming linear additivity. It does not supply a trustworthy forecast for an unexecuted small-plus-large schedule.

An early microstep would change the prestate, hence the later macro gradient. We cannot add E's early benefit to LATE's late benefit, interpolate their weights, or multiply a saved gradient and claim a new experimental result. The user-requested hybrid is a new branch that needs fresh execution.

Evidence: `BATCH_DIAGNOSTICS.csv`, `PAIRED_BATCH_MAGNITUDES.csv`, `RECORDED_GRADIENT_LOCAL_EFFECT.csv`.

## 7. A moving relative reference can pass while absolute old loss rises

The frozen guard is relative to B1 at the **same** event boundary. B1's own old-answer probability quality changes as it learns.

For Early, the pooled confidence result changes from FAIL just after early rehearsal to PASS after the next focal update—even though absolute old loss rises:

| Method | E absolute old loss, before → after next focal update | E minus B1 old loss, before → after | Fixed allowance |
|---|---:|---:|---:|
| G | .010385 → .021778 | .006693 → .004614 | .006372 |
| L | .015746 → .029835 | .011838 → -.011153 | .010000 |

B1 itself weakens over that interval: G .003692→.017164; L .003908→.040987. So a relative pass does not establish absolute stability. This is correct implementation of the specified comparator, not a scorer error. All original failures remain failed.

The new tables report both comparison surfaces: deviation from the moving B1 and deviation from the common pre-fork old inventory. A future protocol should specify which operational question each metric answers, alongside classes, worst records, peak excursion, ending, and cost. It should not choose whichever comparator yields a pass after observing results.

Also, even pre-fork-relative confidence is a measurement choice, not a calibrated proof of real-world safety. We have no out-of-distribution class labels or reliability measurements establishing which small probability change is practically consequential outside the toy.

Evidence: `MOVING_BASELINE_DIAGNOSTIC.csv`, `CONTEXT_TRAJECTORIES.csv`, `BASE_BOUNDARY_GUARDS.csv`.

## 8. Implications for small maintenance plus larger consolidation

The user's suggestion directly targets the observed timing conflict: provide earlier relief and a later repair. It is coherent enough to test. The current data neither establish success nor determine an optimal allocation.

The proposed candidate must answer three distinct questions:

1. Does distributed work beat the same work postponed to one late consolidation window?
2. Does giving more weight to the late consolidation beat distributing that same nominal budget uniformly?
3. Does it preserve the new answer and withstand further learning after consolidation, rather than ending at its best-looking moment?

"Small" must not be confused with cheap. Computing the same eight old-example gradients and scaling the mean down still costs eight derivative calculations. The macro may have a larger coefficient yet a smaller actual norm if the earlier steps already repaired the old loss. Record both nominal and realized quantities.

`CANDIDATES.md` proposes a five-branch controlled design and keeps continued mixed updates as a distinct alternative. Nothing is dispatched by this analysis. The source's original strict full-trajectory failures and all earlier gates remain unchanged.

## 9. Verification scope, analysis incidents, and non-claims

`source/ANALYZE.py` imports no model, training, or original scoring code. It uses saved logits and arrays. Recomputing a mean of stored gradients is not creating a fresh gradient, and subtracting stored vectors to verify a recorded update is not applying an optimizer to a running model. Technical/fixture scores use their retained labels; full causal target checks here cover main development and held-out rows, not a complete reimplementation of every synthetic fault fixture.

Two analysis-only issues were corrected before release and retained in `audit/ANALYSIS_TOOLING_INCIDENTS.json`: a frozen-arm context filter initially used method rather than arm identity; and the initial first-correction focal difference used the previous old-label inventory rather than the captured same-target pre-feedback prediction. No source data, model output, or old scientific score was changed. All results were rebuilt after correction.

The analysis scripts and selected input arrays are self-contained for reanalysis. Fresh-extraction byte verification and a relocated reanalysis are recorded in the external delivery receipt. They are not a third-party replication, independent retraining, new model replay, or guarantee of cross-platform floating-point byte equality. Source memory-accounting limits remain open.

## 10. Research and architecture disposition

NBR01 remains bounded-closed; NBR02 remains active. This adds `ANA-NBR02-TIMING01-001` and a proposed two-timescale maintenance candidate, not a phase qualification. `RET-TIMING01-BALANCE-001` remains open. Workspace fitting is parked; dreaming and self-play pretraining remain deferred leads. The user's after NBR03 / before NBR04 foundation return and conditional earlier NBR01 revisit are preserved. The exact skipped NBR01 ticket still needs identification before any later dispatch.

The inherited G01–G22 register and program records are copied unchanged for context. The parent Architecture Ledger is not edited. No bounded rehearsal result is promoted to a production Tertiary schedule, autonomous memory writer, protection of unbuffered skills, or restored lifelong plasticity.

**Bottom line:** small ongoing maintenance plus a later larger consolidation is worth a controlled test, but not because we can already predict its success. The data identify exactly what it must improve: earlier confidence excursions, later update-induced interference, and stability after the final rehearsal—without surrendering the corrected answer or buying an undisclosed amount of extra training.
