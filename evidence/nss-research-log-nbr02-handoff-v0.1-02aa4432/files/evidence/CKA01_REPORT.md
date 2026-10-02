# NSS CKA01 — checkpoint learning and generalization audit
## Completed diagnostic, execution v0.2 / protocol v0.1

**Finding:** the observed curves do not support “we trained the previous models too long” as the main explanation for the recent poor results. TS01 improved and then saturated on its original checklist benchmark, without late deterioration on the sampled same-recipe examples. TS03 has some late deterioration on the chronological stress tests, but also fails to master the sampled familiar training episodes. The practical concern is incomplete task fitting plus weak chronological transfer, not simply damage caused by excessive training.

This is an exploratory, post-result checkpoint audit. It does not replace historical terminal checkpoints, change failed qualification gates, or prove that more updates alone will solve TS03. No new fit, optimizer update or backward call occurred. Q010 and TS02 were not numerically evaluated in this bounded audit.

## 1. What was evaluated

| Cohort | Original fits | Saved checkpoints per fit | Snapshots evaluated |
|---|---:|---|---:|
| TS01 | 5 | 0,250,500,750,1000,1250,1500,1750,2000 | 45 |
| TS03 C0/C1 x R/Rplus/RW | 24 | 0,200,400,600,800 | 120 |
| Total | **29** | Every retained checkpoint in these cohorts | **165** |

Each checkpoint of the same fit saw the identical fixed panel: 64 actual early-training episodes, 64 newly seeded examples from the unchanged training recipe, and all original main evaluation sequences. The actual training sample was fixed before inference: TS01 items0–7 of updates0–7; TS03 all eight curriculum slots of updates0–7. These are small, deliberately transparent early-training samples, not estimates of accuracy on all historical training episodes. All sampled training episodes preceded the first nonzero stored checkpoint.

The original development and held-out partitions remain separate in the output. The original held-out data are now **known retrospective stress tests**, not fresh confirmation data. The fixed newly seeded recipe panel is a different source of diagnostic evidence. It has no outcome-based sampling or rejection.

The numerical pass used single-episode deterministic float32 CPU inference with the original architecture, native workspace integration, public event semantics, supplied routing, and readout. States were initialized anew for every episode. Only CARRY was evaluated; there was no new state-removal or readout intervention. Labels are used only in scoring, not passed to the learned transition.

There were 25,440 checkpoint/episode evaluations and 44,160 scored active-task queries, including repeated models/checkpoints on the same streams. They are not independent research tasks or evidence for a population-level confidence interval.

## 2. TS01: a solved narrow benchmark, not a model ruined by continued training

| Saved update | Original held-out joint successes | Accuracy | Newly seeded same-recipe endpoint successes |
|---|---:|---:|---:|
| 250 | 363/600 | 60.50% | 195/320 |
| 500 | 549/600 | 91.50% | 287/320 |
| 750 | 598/600 | 99.67% | 311/320 |
| 1000 | 600/600 | 100% | 319/320 |
| 1250 | 600/600 | 100% | 320/320 |
| 1500 | 600/600 | 100% | 320/320 |
| 1750 | 600/600 | 100% | 320/320 |
| 2000 | 600/600 | 100% | 320/320 |

The 600 denominator repeats 120 original query occasions over five fits; the 320 recipe endpoints comprise 64 separately drawn examples for each fit. All five fits first reach 120/120 original held-out successes together at the stored step1000 checkpoint. The fresh recipe endpoint panel becomes uniformly correct at step1250. Aggregate loss on the fixed recipe examples continues falling, from0.138454 at step1000 to0.056169 at step2000. The actual early-training panel also improves rather than deteriorates.

This supports **saturation of the measured task**, not an observed overtraining-induced loss of competence. It does not establish arbitrary-horizon generalization or broader instruction following. The task and source templates are still small and closely related, and routing remains supplied by code. A 100% original score leaves no accuracy headroom for a new management intervention on that exact benchmark; it remains valuable as a regression and cost reference.

## 3. TS03: imperfect learning even on familiar material

### C1 workspace model, original chronological stress queries

| Saved update | Joint successes | Accuracy |
|---|---:|---:|
| 200 | 83/320 | 25.94% |
| 400 | 132/320 | 41.25% |
| 600 | 143/320 | 44.69% |
| 800 | 139/320 | 43.44% |

There is a real late drop of **4/320 readouts (1.25 points)** from step600 to800. Two fits are unchanged, one loses one correct readout, and one loses three. This is a local stress-performance deterioration; it is not a return from 90% competence to43%. In fact, no individual TS03 fit at any retained checkpoint exceeds **39/80 (48.75%)** on the original held-out stress queries. Selecting a hindsight peak therefore cannot uncover a previously qualified model.

The broader grid is not uniformly worsening. From600 to800, original stress joint accuracy changes by +2.19points for C0-R, +6.88 for C1-R, +0.94 for C0-RW, −1.25 for C1-RW, −3.75 for C0-Rplus, and−1.56 for C1-Rplus. These are descriptive, paired fixed-panel results, not significance tests. All curves and individual fits remain in the package.

### The sampled practice examples are not mastered

At step800, C1-RW correctly answers the final active-task question on **51/256 actual early-training episodes (19.92%)**, and **65/256 newly seeded same-recipe episodes (25.39%)**. The retained-training cases really were seen by the respective original fit; they are not newly invented hard cases labelled as training.

These endpoint percentages must not be compared directly with the43.44% historical stress score as a difficulty ranking. The practice panel asks at the episode endpoint; the original stress denominator mixes its five predeclared checkpoints, including easy initial readouts. Episode lengths, event distributions and repeated semantic examples also differ.

The matched all-event/both-bank diagnostic gives a fuller picture:

| C1-RW update | Training sample: joint correct per bank/event | Fresh recipe: joint correct per bank/event | Mean training-sample objective | Mean fresh-recipe objective |
|---|---:|---:|---:|---:|
| 200 | 44.15% | 43.77% | 0.748093 | 0.754839 |
| 400 | 54.54% | 55.89% | 0.539293 | 0.531800 |
| 600 | 59.89% | 61.00% | 0.460610 | 0.444445 |
| 800 | 63.86% | 67.25% | 0.409811 | 0.388344 |

These objective values use the original loss terms on the fixed audit panel, weighted by bank/event count. They are not the historical varying-batch training curve and cannot be compared numerically with TS01's different objective. Event/bank observations are correlated. Early, unchanged and easier outputs may be correct while later consequential updates remain wrong.

The displayed learning curve uses this matched all-event definition, not the original query-only headline percentage:

![TS03 C1-RW fixed-panel learning curves](analysis/TS03_C1_RW_learning_curve.png)

The same-recipe sample does not show the characteristic broad pattern of improving training performance paired with worsening same-recipe performance. Both improve through the retained endpoint. Instead, the audit documents **substantial residual task error even on sampled familiar material**, alongside a stress-transfer gap and some late stress deterioration. The milestone, action and binding loss components all continue improving for C1-RW; declining loss is nevertheless not reliable exact task execution.

This shifts the interpretation away from the earlier untested suggestion that the models might already be excellent at familiar exercises and only fail unfamiliar ones. That explanation is insufficient for the sampled TS03 endpoints. Incomplete fitting, optimization difficulty, objective weighting, curriculum/order coverage and representation/readout interactions remain possible contributors. The audit does not identify one of them as the cause, and does not establish the counterfactual benefit of another200 updates.

## 4. Fresh identifiers are not necessarily fresh semantic examples

The audit compared normalized streams against **all retained training streams of the relevant fit/curriculum**, not merely the64 sampled training episodes. No duplicate was discarded.

For TS01, all320 fresh recipe streams are absent from the corresponding fit's training set after normalization. For each TS03 curriculum, **88/256 freshly drawn streams overlap semantically with that fit's training**, while168 do not. Much of the short recipe has limited semantic variety. Architecture comparisons reuse these same data; there are not three times as many independent fresh examples.

C1-RW's final endpoint score on the168 nonoverlapping recipe draws is **36/168 (21.43%)**. The nonoverlapping44-event subgroup improves from3/128 at step200 to28/128 at step800. The absence of a large familiar-to-fresh performance collapse therefore is not solely an artifact of counting repeated short examples. Full overlap/length-separated curves are provided. Exact nonoverlap still does not imply broad distributional independence.

## 5. Interpretation and next decision

The evidence supports three separate statements:

1. TS01 is saturated on its original accuracy benchmark, without observed late damage on these fixed panels. Preserve it; do not discard it as “overtrained.”
2. TS03 has late stress declines in some configurations, but no earlier high-performing hidden checkpoint. This is not a rescue by retrospective early stopping.
3. TS03 also lacks dependable task execution on the sampled original training examples. A fitting/sequence-learning diagnostic is at least as important as investigating specialization. More training, less training and architectural changes are all hypotheses, not fixes proved by this audit.

The next proposed test should establish whether the learned system can reliably fit a predeclared set of elementary transitions and their short compositions, then preserve that panel while varying **one** factor. Fitting budget or objective diagnostics should be distinguished from altered chronology or longer sequences. It should not introduce a new token writer, new readout, new state topology and new curriculum simultaneously. This is a planning recommendation only; no new training is authorized here.

The maintained management-token concept remains a bounded explicit information-management channel supporting richer recurrent state and exact evidence. This audit neither adopts a new native interface nor disqualifies all such designs. It also does not accept the proposed NBR-01 closeout or initiate NBR-02. The original closeout/G01–G22 context is reproduced without alteration in the accompanying document.

## 6. Verification and cost

Both historical ZIP identities and complete restored manifests were verified before loading trusted checkpoints. Every checkpoint was hash-verified; only its model tensors were extracted into portable data-only NPZ snapshots. Old optimizer/RNG state was not resumed, restored as a learning state, or modified. Newly constructed inference modules merely load existing weights; they are not new fits.

The capture and a fresh-process exact replay each evaluated all165 snapshots. Totals across both passes are **1,255,758 GRU transition attempts/completions** and **4,037,760 bank-head vectors**, with **zero optimizer/backward calls**. A separate numerical audit reconstructs every sequence in float64 NumPy without importing the model/producer. It checks1,720 input records/56,768 recorded prefixes through the independently implemented historical oracles, all13,181,760 categorical output coordinates, and12,445,440 state/logit/loss scalar comparisons. Those repeated coordinates are not independent observations.

The full-prefix engineering tolerance is the separately declared `1e-5 + 1e-4*abs(reference)`, not the prior single-step bound or Q010's underflow amendment. Maximum observed ratio was0.057254 of that tolerance. Fresh float32 replay matched **990 arrays /25,678,410 elements** exactly, plus all deterministic receipt/index records. All736 original terminal model/sequence pairs also reproduced the archived full-event logits and queried states **bit-for-bit** in each pass. That is a strong check that the new audit did not accidentally change the original inference behavior.

All44,160 query rows are retained, including **27,570 all-head-negative rows**, and the complete all-event predictions/losses and query logits/state. This diagnostic does not retain all intermediate hidden states or every nonquery logit; the independent full-prefix calculation reconstructs and checks the retained numerical evidence. Full original optimizer checkpoints remain in the historical archives, not duplicated here. Data-only weight copies make numerical audit reproduction portable.

The first independent scorer stopped during input verification because a NumPy unsigned task-slot expression represented no-op routing as255 instead of−1. The fixed input/producer already used signed−1. The signed conversion was repaired in a separate scorer v0.2, all672 TS01 input records passed the regression, and the original failure/source were retained. No input, weight, prediction, inference source, target, or scientific decision changed; no neural run was repeated for this repair. A non-scientific plotting-permission failure and the unavailable interactive-shell transport are also documented.

This is internal independent implementation and same-runtime replay, not independent optimization reproduction or third-party validation. Snapshot spacing can miss transient behavior between checkpoints. Only two study cohorts were covered. The historical missing Q010 evidence and previous failed study screens remain unchanged.

## 7. Package use

`VERIFY_AUDIT.py` verifies the delivered files. `RESCORE.py --output /new/folder` independently reconstructs and re-scores the retained audit with NumPy, using exact vendored oracle sources; it does not run a Torch model. `REPLAY.py --output /new/folder` is an optional **new** costed Torch replay using the data-only weight snapshots. Its interface was syntax-checked; it was not executed as a third neural replay for delivery. Preparing new procedural panels from scratch uses the historical source archives identified in the dependency file.

The final delivery receipt records fresh-extraction and relocated re-scoring. No restoration or giant historical archive is needed merely to read the report or re-score this audit.
