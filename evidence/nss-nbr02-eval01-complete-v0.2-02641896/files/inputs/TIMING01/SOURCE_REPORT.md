# NSS-NBR02-TIMING01 — fixed-work rehearsal placement
## Completed execution v0.1 / prospectively locked scientific protocol v0.1

**Disposition: COMPLETE. Engineering and baseline admission passed; the early and late branches both FAILED the full-trajectory scientific screen for G and L because old-answer confidence exceeded its limits.** The timing contrast itself is an executed, descriptive diagnostic: later rehearsal improved final old-answer probability quality in most contexts but left a worse interval before that repair. No held-out class answer was lost in any branch's old inventory on this sample. That distinction prevents confidence failures from being mislabeled class forgetting.

This was the selected REPLAY-TIMING candidate, not CONTINUATION-MIX, confidence-capped learning, dreaming, a paper reproduction, or a phase advance. The completed held-out run is new evidence; the earlier PROTECT01 and REHEARSE01 admission stops remain unchanged.

## 1. New protocol and data, fixed before results

The candidate note left admission thresholds and full-work ceilings unresolved. They were completed under the user's execution instruction and locked before any new model/stimulus. The inherited dense tanh learner has 674 float32 parameters (16 recurrent units, 23 input coordinates) and a binary head. G computes the exact three-transition derivative; L uses the same diagonal-local approximation as before, including replay examples. No exact-old hybrid or projection was added.

Eight fresh initial fits (G/L by four paired initializations) each received exactly 100 old-association teaching updates. Four development and eight held-out bases use the same f,p,f,f,p,f public-receipt grammar. Every base restarts from its method/fit's initial checkpoint: this is not a long-lived cumulative learner. All old labels come from received evidence; the fixed eight-record buffer contains the toy's entire old inventory. No unbuffered-skill protection is established.

B1 uses a norm-1 first changed-label correction. U, E and LATE use norm 2 at that receipt only. E applies one norm-1 mean-gradient batch on the eight old records immediately afterward; LATE applies the identical record list after the next valid same-cue/scope/same-label receipt. All later real updates use norm 1. The public worker detects these events from receipt history, not the evaluator's trial index or score. It rejects a second contradictory focal label before the promised follow-up; the separately tested absent-follow-up path leaves rehearsal unspent rather than applying it elsewhere.

All eight replay gradients are independently recomputed at the branch's own current weights, combined in the pinned ordered float64 mean, cast once to float32, clipped once, and applied once. Same records and example/application budgets do not imply the same realized update vector or size. Queries reset temporary state and never update weights.

E and LATE each spend one batch/eight example gradients. B1/U are cheaper. There is no new focal-repetition control in this timing-only study; historical F results are not treated as new observations.

### Prospective baseline competence

A qualifying fit needed 8/8 initial old labels, at least16/20 B1 mixed development answers, 4/4 focal acquisitions after first teaching, 4/4 reversal recoveries after the second corrective receipt, and 4/4 final focal answers. Each method needed3/4 qualifying fits; all four would be retained after group admission. All G and L fits passed. G mixed scores were16,16,17,17; L17,16,17,17.

The own-frozen K/H/net-gain statistics were still measured, not removed or weakened, but were not an admission requirement in this new question. They remain in A0.csv. This is a prospectively changed prerequisite, not a retrospective claim that older runs passed. New held-out labels were generated only after A0 and B1-only confidence calibration were locked. New thresholds: G loss0.006372255809107594 and probability-margin0.01239680384228814; L loss0.01 and margin0.02.

### Common scoring grid

Every branch is assessed at T3 before-extra, T3 after-extra, T4 before-extra, T4 after-extra, T5 post-real and T6 post-real. A branch without an operation at an aligned boundary reuses its prior actual readout, with source frame and reuse flag recorded. These six observations are not six independent tasks or equal intervals of elapsed time. The late branch never receives a postponed start to scoring.

A full-trajectory pass requires first-correction efficacy over B1, no lost U-correct focal answer, every pre-fork-correct old class retained, no additional B1 old error, and all base and pooled old-confidence guardrails at every common boundary. The E–LATE timing contrast is exploratory; no post-result significance test or new superiority threshold is introduced.

## 2. Immediate correction and retained classes

| Learner | B1 first correction | U | E after early batch | LATE before its later batch |
|---|---:|---:|---:|---:|
| G | 11/32 | 32/32 | 32/32 | 32/32 |
| L | 12/32 | 32/32 | 32/32 | 32/32 |

Each32 is eight held-out association bases by four fitted models, not32 independent families. E/LATE improved the first answer in every base on the fit-averaged contrast and in all four fits. Neither introduced a focal regression relative to U at any common boundary.

Every old class is correct in all four branches at all six held-out boundaries. For each branch/method, this is256 model/base/old-cue answers repeatedly measured six times (1536 observations). Therefore no branch demonstrates restoration of an already-wrong old class here. The confidence effects below concern correct but differently supported predictions, not newly discovered catastrophic forgetting.

The exact causal label table correctly answered all48 held-out post-receipt focal and384 old queries (432 occasions), and missed the predictable first-teaching/reversal surprises before feedback (32/48 pre-feedback successes). It remains an ordinary strong bookkeeping control, not a neural achievement or an oracle supplied future labels.

## 3. Timing changes where the old-confidence cost occurs

Mean old-answer log loss, lower is better:

| Learner / placement | Just after strong correction | After early batch | Next focal update, before late batch | After late batch | Final |
|---|---:|---:|---:|---:|---:|
| G early | .013224 | .010385 | .021778 | .021778 | .020179 |
| G late | .013224 | .013224 | .025315 | .013347 | .013545 |
| L early | .050585 | .015746 | .029835 | .029835 | .024700 |
| L late | .050585 | .050585 | .062770 | .015181 | .020211 |

Both rehearsal placements reduce mean old loss at their application in all32 contexts per method and preserve every focal class. The late branch has lower final mean old loss in G8/8 bases and30/32 model/base contexts, and L7/8 bases and29/32 contexts. Pooled late-minus-early final differences are −.0066335 G and −.0044888 L (about32.9% and18.2% lower than early means, descriptive).

But the late branch is worse during the interval in which it has not rehearsed, and after the next focal-only update before its batch. A final-only report would hide that. The extra old-record step spends some focal confidence in both placements; classes remain correct. The 6-boundary schedule does not measure damage continuously between operations.

## 4. No full-trajectory qualification

| Learner / branch | First-correction efficacy | Old classes, all boundaries | Old confidence, all boundaries | Failed base/boundary cells out of48 | Complete screen |
|---|---|---|---|---:|---|
| G early | PASS | PASS | FAIL | 21 | FAIL |
| G late | PASS | PASS | FAIL | 20 | FAIL |
| L early | PASS | PASS | FAIL | 17 | FAIL |
| L late | PASS | PASS | FAIL | 24 | FAIL |

The norm-2/no-rehearsal U reference violates confidence in30/48 G and41/48 L cells. These are eight bases crossed with six explicitly aligned boundaries, averaging four fits/eight old cues; repeated unchanged states count as distinct declared boundaries, not independent harmful events. Pooled boundary failures and every individual probability/margin remain available.

For L, later rehearsal lowers final mean loss yet increases the number of measured boundary violations from17 to24. For G, both schedules exceed the pooled confidence envelope immediately after the strong correction, even before their different maintenance choices can act. That initial excursion is intentionally not exempted. These are empirical guardrail failures, not universal proofs of unsafe behavior.

The minimum measured old correct-label probabilities across the grid are G .71955(E)/.69476(LATE), L .55110(E)/.64825(LATE). Model probabilities are not calibrated guarantees. No overall timing choice dominates every retention metric.

## 5. Why equal rehearsal work need not produce equal changes

All held-out replay batches were below the norm-1 clip ceiling. Mean raw norms: G early .05205 versus late .11535; L early .24736 versus late .30628. The late batch is calculated at weights after an additional focal update; identical records therefore supply different gradients. This is part of the timing intervention, not an uncharged extra rehearsal step or proof of a pure equal-step directional effect.

The full record includes source receipts, per-example raw gradients, reduction operands, effective norms, before/after parameters and all inventories. The original predicted cue is recorded before feedback; branch reconstructions do not masquerade as additional blind predictions. No outcome-directed weighting, retry, extra epoch, clipping change or post-score correction occurred.

## 6. Failure-first checks and complete evidence

The numerical audit independently reconstructs every update, derivative, batch reduction and input from the stored public recipe, using NumPy rather than producer/controller/model code. It verifies G exact and L own-rule fidelity separately; L is not expected to equal the exact gradient. It performs9,950,920 scalar comparisons per pass, maximum tolerance ratio .1112471 under2e−6+2e−5|reference|. This is an empirical numerical tolerance, not a formal error bound. Q010's old softmax amendment is unrelated.

Twelve non-neural contract methods passed. The fixed derivative and three-delay integration cases passed, including timing authority, no-op/missing/wrong follow-up semantics, batch reduction and public-buffer checks. Eight deliberately bad batch updates per pass were actually applied in isolated copies and detected. Seven post-capture checks combine those live faults with copied corruption/truncation/missing-commit tests. These are bounded detector tests, not exhaustive crash or information-flow proofs.

Full fresh-process adaptive replay reinitialized every model and repeated all fixtures, probes, initial learning, development, held-out receipt updates and replay batches. It matched41,508 numerical frames,130,206 arrays and29,022,292 elements plus plans, public messages/events, counters, admission and decisions. All13 final score/audit files and four earlier stage-audit files matched byte-for-byte. Delay fixtures are invariance checks on detached waiting, not independent causal-learning evidence.

The primary capture contains29,540 scored neural query/diagnostic rows and2,757 incorrect rows. Held-out contributes519 negatives across methods and frozen controls; all41 post-feedback learned focal misses there belong to B1's first corrections. Other held-out negatives are before-feedback predictions and frozen-control behavior. No negative is dropped; old-confidence failures have their own table even when the class is correct. Primary stats count26,360 explicit query frames; raw pre-feedback predictions add further score rows, so these two totals are not interchangeable.

All6,136 update attempts across capture and replay have durable commits; no unknown-completion natural update or failed scientific fit exists. No historical weights were loaded or modified. Forty initial checkpoint records per pass retain0/25/50/75/100 histories, plus branch/probe/fixture checkpoints, every update and SGD cursors (SGD has no momentum slots). Fresh adaptive replay is internal reproduction, not third-party replication.

## 7. Resource and delivery accounting

| Work, capture plus complete replay | Actual | Frozen cap |
|---|---:|---:|
| Parameter applications | 6,136 | 7,000 |
| Recurrent cells | 197,112 | 260,000 |
| Output heads | 63,464 | 80,000 |
| G reverse-mode calls | 4,700 | 6,000 |
| L example-gradient calculations | 4,700 | 6,000 |
| Replay-record fetches | 3,712 | 4,800 |

Every example in the old batches is charged, even when numerical arrays later compress or deduplicate. Eight initial fits and96 main method/fit/base contexts ran; the method-specific old graphs are not secretly exact for L. Exact controls, NumPy audits, encoding and logging have measured overhead beyond neural counts.

Primary and replay supervised numerical stages took75.91 and76.49seconds, including their internal scoring. The shared post-authorization clock through replay was521.19seconds, including implementation/preparation, below the two-hour limit. These are instrumented run times, not deployed method speed comparisons. Peak sampled process-tree RSS was840,425,472bytes and container current3,585,794,048bytes, below3GiB/3.5GiB limits respectively. Sampling interval .1seconds can miss short peaks; initial uninstrumented work and separate delivery QA are not claimed continuously covered.

**Storage qualification:** preflight empirical projections were62,276,783 delivery bytes and190,697,670 live encoded bytes. These were not worst-case proofs. Verbose duplicated logs exceeded that layout forecast during the second pass. After the first worker had closed its files, three sealed logs were losslessly gzipped, decoded and hash-verified before removing their redundant uncompressed copies. This kept actual retained output below256MiB during the live run; final observed pre-alias size247,912,993bytes. No running log was truncated or altered. This packaging adjustment and original/encoded hashes are in SEALED_CAPTURE_LOGS.json.

After genuine replay equality, byte-identical replay files were declared aliases. Numerical frames were reversibly encoded as exact headers plus byte lanes; restoration reproduces all73,267,305 original framed-record bytes (pinned zlib1.3.1), not newly evaluated model outputs. Original logs/arrays are all reconstructible. A full restoration intentionally materializes redundant copies and is not the compact retained representation used for the live cap. The delivery receipt reports exact compressed and logical sizes and fresh-restoration results.

OBS-DC01-COST-001 remains open: Python object accounting omits some backing/native allocations. Process/cgroup samples and full numerical traces do not justify overall G/L memory superiority. Codec compression is not learned-state compression.

## 8. Interpretation, roadmap and the supplied paper

Timing is useful but not a full-trajectory solution here. Later maintenance repairs a more disrupted state and improves the ending on most cases; it does not protect the interval while learning continues without that maintenance. The next design question may concern continued updates that reintroduce interference, not additional timing-only variations. No continuation mixture, confidence cap or extra rehearsal was run or authorized by this result.

NBR01 remains bounded-closed, NBR02 active. Existing REHEARSE/PROTECT admission stops and REV01 retention failures remain immutable. RET-MW01-FIT-001 is parked, RET-DREAM-MAINT-001 deferred, and FCR-0103-001 retains the planned01–03 foundation consolidation before04. The user's conditional early return to the skipped NBR01 question has not been dispatched; the exact ticket was not identified and this run did not pass full-trajectory qualification.

The screenshot's primary paper was verified as *Self-Play Pretraining with Zero Data*, arXiv:2609.30063v1 (24September2026). Its generator learns programs producing synthetic byte sequences, with a learner trained to predict their output. Record it under RET-TRAIN-SELFPLAY-001 for later curriculum-generation research. It is a proof-of-concept external lead, not evidence that NSS dreaming, online retention or zero-compute learning works. See program/TRAINING_PAPER_BACKLOG.md for source, narrow summary and proposed controls. Nothing from the paper enters this experiment's training or selection.

Parent Architecture Ledger unchanged. This run supplies AER-NBR02-TIMING01-001, with the observed timing trade-off and full-trajectory confidence failures, not production adoption of a maintenance schedule.
