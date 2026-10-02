# NSS NBR02 — REHEARSE01 retained-data analysis
## Analysis v0.1 / source execution v0.2, scientific protocol v0.1

**Status: completed retrospective analysis; the source remains STOPPED_AT_A0.** No held-out data were generated. No network was instantiated or evaluated, no derivative was newly calculated from a network, no parameter update was applied to a learner, and no new random stimulus was drawn. Gradient comparisons use the vectors already captured in the source run. Recomputing arithmetic from recorded values is not a new learning trajectory.

## Executive finding

The data distinguish three issues that should not be merged into “the experiment failed.” First, the ordinary B1 learners acquire all four development associations and recover all four reversals after the second corrective receipt in every fit; the admission failures concern first-correction speed relative to a frozen control. Second, old-record rehearsal improves mean old-answer loss in every one of the 16 model/base contexts per method without breaking the corrected focal class. Third, the next focal-only update worsens mean old-answer loss in every context again. One rehearsal operation is useful but does not protect later updates.

The preserved gradients and individual old-answer changes reveal a consistent competition between increasing confidence in the new focal label and retaining confidence in old records carrying the opposite label. This is a bounded observation on a binary-association toy, not proof of an unavoidable stability/plasticity law or of a unique internal fault.

## 1. Source and verification scope

Primary dependency: `NSS_NBR02_REHEARSE01_Development_Stop_v0.2.zip`, 25,131,512 bytes, SHA-256 `7cfe40a31d34ae5371340c600850bbbe0587316e11f6e4f98320f62dba37aca3`.

The source archive passed CRC and its recorded archive identity. A separate extraction was restored using its lossless byte-restoration helper. All **164 source manifest entries** matched. The original uploaded archive was not modified.

A new reader, independent of the producer and historical scorer, traversed all **19,428 primary frames, 61,150 arrays and 14,577,108 elements**, checking frame and array hashes. It matched all **13,220 score rows** to their retained logits and independently recomputed class, log loss, logit margin and probability margin; the maximum observed difference was zero. This is retained-byte and scoring verification, **not another model or adaptive replay**. The replay target in the source delivery is a verified alias of historically recomputed evidence; restoring it now is not a fresh replay.

The analysis uses all **8,160 development query/diagnostic rows**, all **64 development replay batches**, and the fixed eight-fit A0 records. It retains all **271 development-negative rows**, not just the eight old-class error observations. The full original 13,220-row score table is included as input so its 2,046 total incorrect rows remain available and phase-labelled.

Selected saved vectors are copied into a data-only NPZ: **1,088 arrays / 992,256 elements**, with source frame IDs, dtypes, shapes and hashes. These are archived batch operands and update endpoints, not new checkpoints or newly evaluated gradients. The self-contained `ANALYZE.py` rebuilds 14 CSV tables and `SUMMARY.json`. No Torch, model runtime, generator, optimizer or original scorer is imported.

All findings below are **post-result development analyses**. Four bases crossed with four fits yield 16 contexts per method; repeated old cues, checkpoints, common branches and replay are not independent new tasks. The development data also calibrated the confidence envelopes, so descriptive application of those envelopes is not confirmation.

## 2. Admission decomposes into first-correction lag and frozen prior alignment

### 2.1 The reference learners do learn these associations

Reconstructing every focal history from saved logits gives:

| B1 focal readout, across four bases × four fits | G | L |
|---|---:|---:|
| After first teaching receipt | 16/16 | 16/16 |
| After the intervening protected-old receipt | 16/16 | 16/16 |
| After the first changed-label receipt, trial 3 | 4/16 | 5/16 |
| After the second changed-label receipt, trial 4 | 16/16 | 16/16 |
| After the later protected-old receipt | 16/16 | 16/16 |
| Final focal answer | 16/16 | 16/16 |

Thus the fixed-K B1 errors occur exclusively at trial 3, not because the model never acquires the task or cannot recover after a second correction. This does not satisfy or waive the existing first-correction-sensitive gain gate. It narrows the operational meaning of the failed prerequisite. [Tables: `FOCAL_HISTORY.csv`, `ADMISSION_DECOMPOSITION.csv`.]

### 2.2 The gate is attainable, but it mixes learning speed with a frozen model's label alignment

Let **n** be the number of the four bases on which the frozen model already predicts the eventual changed label, and **k** the number of successful B1 first corrections. In these observed data, B1 is perfect at trials 4 and 6 and the frozen answer never changes. Consequently:

- `B1_K = 8 + k`;
- `N_K = 3n`;
- `H = 12 - 3n`;
- the frozen rule `2(B1_K - N_K) >= H` is equivalent to `k >= 1.5n - 2` for H>0.

This is a descriptive algebraic simplification for these recorded histories, **not a proposed replacement gate** and not a general formula when later B1 answers are wrong.

| Method/fit | Frozen changed-label matches n /4 | B1 first corrections k /4 | B1_K /12 | N_K /12 | Net gain/H | Original decision |
|---|---:|---:|---:|---:|---:|---|
| G0 | 3 | 2 | 10 | 9 | 1/3 | Fail |
| G1 | 2 | 0 | 8 | 6 | 2/6 | Fail |
| G2 | 2 | 2 | 10 | 6 | 4/6 | Pass |
| G3 | 0 | 0 | 8 | 0 | 8/12 | Pass |
| L0 | 3 | 3 | 11 | 9 | 2/3 | Pass |
| L1 | 1 | 1 | 9 | 3 | 6/9 | Pass |
| L2 | 2 | 1 | 9 | 6 | 3/6 | Pass |
| L3 | 0 | 0 | 8 | 0 | 8/12 | Pass |

G0 has faster first correction than G3 but fails where G3 passes. This is not a scorer defect: the statistic was deliberately defined as *relative* net recovery, not pure first-correction speed. In G0, two frozen-error readouts are corrected, but one frozen-correct readout becomes wrong, leaving net gain one. G1 corrects four frozen errors and introduces two errors on frozen-correct readouts, leaving net gain two.

The frozen model receives no focal parameter learning; its pre-existing prediction can happen to match the reversed label. The relevant distinction is that an initially coincidentally correct output is not evidence of learning from the changed receipt. Keep the control strong, but do not equate this gain statistic with a complete diagnosis of baseline competence.

**Prospective implication:** separate evidence of elementary acquisition/two-receipt recovery from the first-correction-speed requirement that the intervention is intended to improve. Retain frozen-relative results as their own surface. Any new contract needs fresh prospective validation; these findings do not reopen held-out dispatch, select seeds, or turn A0 into a pass.

## 3. Rehearsal's benefit is consistent at the context level, not driven by one average

In all **16/16 G** and **16/16 L** contexts, the old-record R batch reduces mean loss on the eight old associations relative to the identical pre-extra state. All 32 focal answers remain correct. Mean old loss improves:

| Method | Before R | After R | Reduction in the pooled mean |
|---|---:|---:|---:|
| G | 0.022229 | 0.013178 | 40.72% |
| L | 0.049394 | 0.016503 | 66.59% |

The percentage is the reduction of these pooled means, not the average individual percentage improvement. R also beats extra focal practice F on mean old loss in every context immediately afterward. At the final checkpoint it remains better than both F and U in **15/16 contexts per method**, not all contexts.

The new answer's confidence is not preserved exactly: focal mean loss increases from **0.068150 to 0.087837 for G**, and **0.037131 to 0.054975 for L**, while its class remains correct. Rehearsal therefore improves old quality by spending some of the corrected answer's confidence margin. No claim is made that every old record benefits or that R dominates on every metric.

R maintains all **512/512 repeated old-class observations per method** over the four recovery checkpoints. No old class was wrong immediately before R, so this does not demonstrate resurrection of a forgotten class. It demonstrates confidence improvement followed by better retention under this schedule. [Tables: `PAIRED_RETENTION.csv`, `TRAJECTORY_MEANS.csv`, `OLD_CLASS_ERRORS.csv`.]

## 4. The next ordinary focal update reintroduces interference

After R, all focal answers are already correct. Nonetheless, the next lawful focal-only receipt causes mean old loss to rise in **all 16/16 contexts per method**.

| R branch | After strong correction | After old rehearsal | After next focal update | Final |
|---|---:|---:|---:|---:|
| G mean old loss | 0.022229 | 0.013178 | 0.050170 | 0.030882 |
| L mean old loss | 0.049394 | 0.016503 | 0.040991 | 0.031669 |

This is not idle-time memory decay. A recorded parameter update intervenes, its focal target is already class-correct, and its cross-entropy loss remains nonzero. The observation is consistent with continued sharpening of that answer interfering with old answers. It does not prove that changing the objective, skipping correct-example updates, or adding rehearsal would solve the problem; those have not been tested.

The later protected-old receipt improves some of this damage, but it targets **one old cue**, not the full old buffer. The experiment resets each base to its initial checkpoint; these are short independent histories, not a long-running continual learner.

![Old confidence along the recorded R trajectories](figures/old_confidence_trajectory.png)

### 4.1 Confidence violations are of two different kinds

The original descriptive count is independently reproduced: R exceeds its development-calibrated envelope in **2/16 G** and **5/16 L** base/checkpoint cells.

- **Immediately after R:** G has one failing base; L has four. G base1's excess over the loss limit is approximately 0.0000730 nats, and over the probability-margin limit approximately 0.000302. Some L first-stage excesses are similarly small; none is silently waived.
- **After the next focal receipt:** both methods fail at base2. Mean R-minus-B1 old loss is **0.025150 for G** against allowance **0.009116**, and **0.025470 for L** against **0.010000**. These are not merely tiny threshold crossings.
- **At the last two checkpoints:** all R base-level confidence cells are inside the declared diagnostic envelope. That later improvement cannot erase the earlier excursions.

The larger base2/receipt4 excursions are concentrated in fit3. Its per-fit mean excess over B1 is **0.103768 G** and **0.142698 L**; other fits partly offset those values. All fits remain in the results. A group average can hide a fragile individual configuration; removing that fit would not be a valid repair.

The weakest R old-answer probability in the measured tail is **0.610701 for G** and **0.543105 for L**. The latter is correct but close to the binary class boundary; perfect class counts are not equivalent to large safety margins. These probabilities are model outputs, not calibrated guarantees. [Tables: `CONFIDENCE_CELLS.csv`, `CONFIDENCE_CONTRIBUTORS.csv`, `TRAJECTORY_MEANS.csv`.]

## 5. Which old answers improve? A strong binary-label pattern

The old set is balanced: four records have the new focal label and four have the other label. Each group therefore contributes 64 model/base/cue observations per method at a given transition.

Immediately after R:

| Old records relative to the newly corrected focal label | G | L |
|---|---|---|
| Opposite label | Loss decreases in **64/64** | Loss decreases in **64/64** |
| Same label | Loss increases in **64/64** | Loss increases in **64/64** |

At the next focal update, the pattern reverses exactly: all 64 opposite-label old records lose probability quality, and all 64 same-label records gain it, for each method. This holds in both same-scope and other-scope subgroups in these data.

For G, opposite-label old mean loss goes **0.041745 → 0.023138** during R; same-label old loss goes **0.002712 → 0.003217**. For L, the corresponding changes are **0.097356 → 0.030960** and **0.001431 → 0.002046**. Averaging both groups is useful, but masks these opposite directions.

**Interpretation:** the old and new objectives are competing through shared learned parameters in this binary task. Rehearsal is not an isolated restoration of every record. It improves the more damaged opposite-label group while modestly reducing already-high confidence in the same-label group and focal answer. We have not isolated a particular recurrent layer, output bias, or single parameter as the cause. [Tables: `OLD_PER_RECORD_CHANGES.csv`, `LABEL_RELATION_SUMMARY.csv`.]

## 6. Saved gradients support competition, not an arithmetic malfunction

All 64 recorded batch reductions were checked independently: eight raw float32 gradients at one prestate; ordered float64 sum/divide; one float32 mean cast; the recorded clipping factor/product; and exact resulting parameter bytes. Every F/R pair has identical batch-entry parameter bytes. No new derivative or counterfactual update was evaluated.

### 6.1 Rehearsal is not being throttled by its clip limit

Every R batch has raw norm below 1 and clipping factor exactly 1:

- G norm range **0.029240–0.314154**, mean **0.096161**;
- L norm range **0.089909–0.617132**, mean **0.222218**.

Their mean cancellation ratios are approximately **0.7407** and **0.8074**. They are not zero-gradient batches.

Consequently, merely raising the R-batch clipping ceiling from 1 to 2 would leave the clipping factor unchanged for **these saved inputs**. This is an arithmetic observation, not a newly run alternative. A larger learning rate, different weighting, extra application or different timing would be a new intervention with risks to the focal answer.

### 6.2 The new and old corrections point against each other

At the common post-clip2 state, the dot-product cosine between the saved focal mean gradient and old mean gradient is negative in **all 32 contexts**. Mean cosine is **−0.452806 for G** and **−0.564193 for L**.

For G, these are recorded exact-gradient estimates at the same parameter state: the local derivative predicts that the R direction will lower mean old loss but raise focal loss, and the observed signs agree. For L, these are directions produced by its approximate rule; they must not be relabelled exact derivatives of the true loss.

Component norms indicate that the change is distributed: roughly 74.0% of R's squared step norm is in G's encoder/recurrent parameters and 82.5% in L's; the rest is in the readout. Those percentages do not measure causal contribution to errors. No layer or weight block was removed or replaced.

This supports a concrete, local competition explanation. It does **not** prove no joint solution exists, that a larger model is needed, or that replay cannot solve the task. [Tables: `SAVED_GRADIENT_GEOMETRY.csv`, `GRADIENT_BLOCK_ACCOUNTING.csv`, `BATCH_MAGNITUDES.csv`.]

## 7. Extra focal practice advances the next focal step, exactly

In every one of the **32 method/fit/base contexts**, F's post-extra stored parameter vector is bit-identical to U's vector after the next actual focal receipt at trial4. All nine query-logit pairs also match.

This follows the specific schedule: same focal input and released label, no intervening update on U, reset temporary state, and F's eight identical gradients averaged into one step. It demonstrates no new independent observation: F brings forward the learning computation that U subsequently performs after another environmental receipt.

This is a useful control interpretation, not a reason to drop F. Its extra work is deliberately matched to R. The source and current audit continue to charge every repeated gradient calculation.

**Signed-zero detail:** the fixed float64 accumulator starts at +0. F's mean is numerically identical to one raw gradient, but 27 of 32 F mean vectors change signs on a total of 3,040 exactly-zero components (−0 to +0). The prescribed reducer and resulting update bytes still match exactly. F-post and U-next parameter equality also holds. This does not explain any task error. A provisional analysis assertion had demanded an unnecessarily stronger raw-to-mean byte identity; it was replaced by value equality plus explicit signed-zero accounting, not by relaxing the defined batch contract. [Table: `F_EXTRA_TIMING_EQUIVALENCE.csv`; audit incident log.]

## 8. What to test next — proposal, not execution

The data support treating **rehearsal scheduling** as a next discriminator, rather than increasing the clipping limit of an already-unclipped R step. A clean timing-only diagnostic could move the same one eight-record batch from after the first changed-label receipt to after the next focal receipt, with all endpoints and intervening harm still scored. It would not automatically solve the immediate-recovery requirement; it would isolate placement at fixed replay examples/applications. The existing cases are now known regression material, not its confirmation set.

A fuller intervention that rehearses repeatedly would require a separately matched budget and controls for the extra steps. We should not silently add updates until the confidence envelope passes. A joint weighting or other loss policy is another possible mechanism, but changing timing, objective and dose together would make attribution difficult.

Independently, the prerequisite should be reviewed prospectively: does it establish the ability to acquire/recover associations, or require the slow reference to perform the rapid reversal that the candidate is intended to improve? Preserve the strong frozen control and raw first-receipt errors; do not weaken them just to admit the run.

**Bottom line:** this is a credible, bounded rehearsal signal with an observed limit: one refresher improves old confidence, but subsequent focal-only learning reintroduces the competing pressure. It is not a qualified held-out pass, prevention of all transient damage, restored plasticity, or a working dream phase.

## 9. Program status and limitations

NBR-01 stays closed at its accepted recovered-evidence scope. NBR-02 remains active. REHEARSE01's original A0 is unchanged and held-out qualification is NOT_ASSESSED. `RET-REHEARSE01-A0-001` and `RET-REHEARSE01-RECOVERY-001` gain this analysis as supporting evidence, not resolution. `RET-MW01-FIT-001` remains parked, `RET-DREAM-MAINT-001` deferred, and `OBS-DC01-COST-001` open. FCR-0103-001 remains the planned 01–03 foundation return before NBR-04.

The user's conditional near-term return to the skipped NBR-01 question is preserved. This audit neither earns the qualifying rehearsal pass nor dispatches that return; the exact skipped question ID still needs confirmation before a later experiment. No architecture master, historical result, unused experiment budget, or original training qualification has been changed.

This analysis did not replicate the historical fitting or re-evaluate the model on new inputs. It checked saved evidence, rebuilt descriptive tables, and derived additional arithmetic diagnostics. Internal analysis reproducibility is not third-party replication. No IID confidence interval or new scientific-success criterion is asserted.
