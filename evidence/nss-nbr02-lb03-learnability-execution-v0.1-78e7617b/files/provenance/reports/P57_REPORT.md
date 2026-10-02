# NSS LB02-Q2-TRAIN — Two-bit weights and smaller learning state
## Research, results, cost and decision · Execution v0.1
**29 September 2026 | Complete logical comparison; useful Q2 preparation and optimizer-memory reduction; sustained learning working point remains open; actual-update ceiling exceeded during recorded operational recovery.**

## 1. ELI5: what we asked and what we found
Can the little checklist learner use four weight settings, still learn a changed association, and keep fewer working notes while learning? Ternary/BitNet-style 1.58-bit matrix symbols remain the owner's longer-term aim; two-bit matrix storage is an acceptable interim target. This is a GRU experiment, not a BitNet Transformer reproduction.

**Good news:** after the planned 1,024 preparation updates, the two-bit model with compressed optimizer notes answered 32,766/32,768 checklist events correctly (99.99390%) and completed 1,022/1,024 continuations without error. It then acquired the changed cue in all four parents. After the fixed balanced repair, all current cue classes remained correct and old checklist accuracy was 99.24622%.

**A real learning-memory saving:** the counted master+gradient+optimizer tensor payload fell from 291,984 to 183,650 bytes, a 37.10% reduction; optimizer arrays alone fell by 74.21%. It did not reduce all training state to two bits, reduce measured whole-process RAM by 37%, or increase training throughput. The compressed path was descriptively about 3.55% slower than the otherwise matched two-bit/full-moment path.

The remaining limitation is reliable complete work after a new correction. The compressed path made 11 false-DONE answers after repair and completed 952/1,024 continuations (92.97%). Only one of four parents met the full learning-endpoint rule. The comparison's complete logical endpoints exist, but two caller interruptions required 205–207 extra applications to recover the intended trajectories. The original actual-update cap was exceeded and remains a failed resource condition—not silently reclassified as a clean pass.

All reported data derive from `results/SUMMARY.json`, raw arrays and update journals. The report does not substitute external literature for model results.

## 2. What ran: three matched branches, no new parent fits
Four exact original SURFACE01 parents (4101–4104) were recovered as float32 arrays from the verified LB01-TERNARY source archive. Each contains GRUCell(26,64)+Linear(64,9): 18,249 learned coefficients, comprising 17,856 matrix entries and 393 biases. Every original coefficient can change during training.

| Branch | Matrices during forward computation | Stored optimizer notes |
|---|---|---|
| F32_M32 | Float32 | Float32 first and second moments |
| Q2_M32 | Four-level, per-row affine quantized | Same float32 moments |
| Q2_M8 | Identical four-level quantization | Blockwise 8-bit first/second-moment codes plus scales |

The direct F32/Q2 comparison tests weight representation under matched preparation. Q2_M32 versus Q2_M8 tests compressed optimizer state on the same weight representation. This is not a complete factorial: there is no float-forward/M8 arm. It makes no universal optimizer or quantizer claim.

No pretrained download, adapter, new architecture, live deployment, HSA, DARP or further language-reader experiment was introduced. The exact task scorer never edits predictions or supplies missing inference answers.

## 3. Task rules, tests and data separation
All eight checklist items start unfinished. SET(i) makes i done until CLEAR(i) or RESET; CLEAR(i) makes it unfinished; RESET makes all unfinished; NOOP changes nothing. After each event, answer the smallest unfinished index; 8 means DONE and is correct only when every item is done. These are explicit persistent state rules, not ambiguous English observations. The network receives the event code/one-hot input, not the label, mask, or natural-language explanation.

The second task is eight zero-state cue associations, initially 0,1,0,1,0,1,0,1. New learning flips cue 0 to 1 while keeping the other seven current. This is a corrected association, not a newly learned procedure or open-ended reasoning.

The main panel contains 256 new histories, balanced across mixed, idempotent, revision and reset families. Each has 24 prefix events and 32 scored suffix events. Development has 16 histories of the same length; separate stress has 16 histories, 32 prefix plus 128 suffix events. Primary REBUILD reads the whole history using the candidate's own weights. Secondary CARRY starts the suffix from the original float parent's prefix state; it is not selected instead when it scores better.

Primary 32,768 answers = 256 histories × 32 suffix events × four inherited parents; whole-continuation denominator is 1,024. These repeated events/paths are not independent replications. All four parents remain included. New histories and 32-event windows were excluded against the retained 64 replay batches per parent, prior LB01 panels and earlier new panels. Not all original training corpora were available; shorter familiar patterns and rules recur. This is known-rule generalization, not novel semantic learning.

Source/configuration were frozen before fixture generation and training; fixtures were frozen before training. Confirmation results did not select model endpoints. Stage-0 evaluation of the same confirmation panel is the predeclared conversion baseline, not an unseen-after-all-training-only protocol.

## 4. Preparation and correction schedule
Every branch receives the same 64 retained A batches, each 32 histories × 32 events, repeated 16 times for 1,024 joint A+original-B updates. The learning rate follows the fixed cosine schedule .003 to .0003. Checkpoints at 256 and 512 give development-only curves; 1,024 is the fixed primary preparation endpoint.

Then each branch starts fresh optimizer state for 64 B-only acquisition updates at .003, followed by another fresh optimizer for 32 A+current-B repair updates at .003. This corrects the earlier test's uninformative acquisition recipe, which failed even with float weights. The successful CYCLE-style separation of acquisition and balanced repair motivated the schedule; success is measured anew, not inherited by assertion.

All branches use betas .9/.999, epsilon 1e-8, no decay and global gradient clipping at 1. All parameters receive gradients. A custom common C Adam implementation gives FP32 stored moments with double local arithmetic; it is not bit-exact to every operation order of the historical Torch Adam implementation. The M32/M8 comparison uses the same declared equations apart from the compressed previous moments. No moment arrays carry across phase boundaries.

The same preparation schedule does not imply equal runtime. All gradients, effective-weight tensors, optimizer buffers and earlier expensive parent preparation remain costs. This study counts its continuation only; it does not train a two-bit model from scratch.

## 5. Preparation result: near-complete recovery under two-bit weights

| Condition | Correct / answers | Accuracy | Entire continuations | False DONE | Current cue classes |
|---|---|---|---|---|---|
| Float weights / FP32 moments | 32,763/32,768 | 99.98474% | 1023/1024 (99.90%) | 0 | 32/32 |
| Two-bit weights / FP32 moments | 32,765/32,768 | 99.99084% | 1022/1024 (99.80%) | 1 | 32/32 |
| Two-bit weights / 8-bit moments | 32,766/32,768 | 99.99390% | 1022/1024 (99.80%) | 1 | 32/32 |


At direct conversion before preparation, both Q2 branches had 22,215/32,768 correct answers (67.79%), 113/1,024 completely correct continuations and 49 false-DONE predictions. The unchanged float reference had 32,751/32,768 correct, 1,023/1,024 whole and no false DONE. After preparation, Q2_M8 has only two event errors, removing 10,551 of the 10,553 conversion errors in net count. This is a substantial recovery, not proof that quantization is universally better than float because its pooled error count happens to be smaller.

The two Q2 optimizer conditions produce different isolated residual errors. Both satisfy the prospectively required preparation working point in three of four parents; the fourth misses the zero-new-false-DONE requirement. F32 preparation meets it in all four. No extra fitting repairs the failed parent's observed example.

### Fixed development curve — more practice within this schedule

| Arm | Update 256 correct / 2,048 | Update 512 correct / 2,048 | Update 1,024 correct / 2,048 |
|---|---|---|---|
| Float weights / FP32 moments | 2048 | 2048 | 2048 |
| Two-bit weights / FP32 moments | 2038 | 2042 | 2048 |
| Two-bit weights / 8-bit moments | 2037 | 2047 | 2047 |


These are the same 16 development histories per parent. The 512 and 1,024 stages differ in training amount and position in the prescribed learning-rate schedule. This is not a randomized test of optimally spending extra compute, nor evidence that twice the training always helps. No best development checkpoint replaces the fixed endpoint. It also is not a clean comparison with the old ternary experiment, which used a different quantizer, schedule, panel and optimizer engine.

## 6. New learning and old-work repair
All 12 paths acquired all eight applicable cue classes at update 1,088; minimum correct-target probabilities exceeded .98 in each arm's worst parent. Unlike LB01's shared acquisition failure, the float control successfully learned here.

The intermediate checklist damage remains visible:

| Condition | Correct / answers | Accuracy | Entire continuations | False DONE | Current cue classes |
|---|---|---|---|---|---|
| Float weights / FP32 moments | 5,564/32,768 | 16.97998% | 0/1024 (0.00%) | 2 | 32/32 |
| Two-bit weights / FP32 moments | 18,960/32,768 | 57.86133% | 160/1024 (15.62%) | 32 | 32/32 |
| Two-bit weights / 8-bit moments | 17,265/32,768 | 52.68860% | 95/1024 (9.28%) | 37 | 32/32 |


Those are candidate-only measurements, not user-facing serving weights. This study does not automatically adopt them. No old-task rehearsal occurs in the 64 B-only steps, so substantial interference remains possible.

After the fixed 32 balanced-repair updates:

| Condition | Correct / answers | Accuracy | Entire continuations | False DONE | Current cue classes |
|---|---|---|---|---|---|
| Float weights / FP32 moments | 32,540/32,768 | 99.30420% | 941/1024 (91.89%) | 16 | 32/32 |
| Two-bit weights / FP32 moments | 32,607/32,768 | 99.50867% | 959/1024 (93.65%) | 19 | 32/32 |
| Two-bit weights / 8-bit moments | 32,521/32,768 | 99.24622% | 952/1024 (92.97%) | 11 | 32/32 |


Every path retained every corrected cue class, with its minimum target probability at least .97598 across all paths. These assigned scores are not calibrated reliability guarantees. The Q2_M8 repair reduced its post-acquisition checklist error count from 15,503 to 247. That is a large repair effect with residual risk, not lossless continual learning.

### Every parent: primary repaired result

| Parent | F32 correct / 8,192; whole; false DONE | Q2_M32 | Q2_M8 |
|---|---|---|---|
| 4101 | 8146; 240/256; 7 | 8172; 248/256; 1 | 8108; 236/256; 2 |
| 4102 | 8145; 235/256; 2 | 8139; 234/256; 7 | 8175; 246/256; 5 |
| 4103 | 8159; 233/256; 6 | 8145; 242/256; 5 | 8148; 240/256; 0 |
| 4104 | 8090; 233/256; 1 | 8151; 235/256; 6 | 8090; 230/256; 4 |


Compared with Q2_M32, compressed moments yield fewer correct events in two parents and more in two. Parent 4101 loses 4.69 percentage points of whole-history accuracy and adds one false DONE; the other three have fewer false-DONE events but do not all meet the absolute working-point requirements. A lower pooled false-DONE count (11 versus 19) cannot erase that parent regression.

## 7. Original decision criteria and the outcome
A working parent must achieve at least 98% event accuracy, 90% entirely correct continuations, no more than 1 point event loss versus its own unchanged float parent, no newly induced false DONE, and all applicable B classes with minimum target probability .8. Three of four parents are needed for the provisional cohort working point. These are engineering decisions, not significance tests or confidence intervals.

Preparation: F32 4/4, Q2_M32 3/4, Q2_M8 3/4. The preparation cohort criterion is met by both Q2 paths. Post-correction learning: F32 0/4, Q2_M32 0/4, Q2_M8 1/4. No arm meets the complete learning-cohort criterion; this is not a failure unique to low-bit weights or compressed moments.

The separately declared compressed-versus-M32 rule requires event loss <=1 point, whole-history loss <=2 points, no extra false DONE, and both paths at working quality. It is met in 2/4 paired parents after preparation and 0/4 after correction/repair. The numeric array reduction exceeds its separate 25% criterion. Memory reduction is thus measured, but quality-equivalent low-memory learning has not been fully qualified.

Strict failed criteria do not erase 99.99% prepared accuracy, the near-complete old-skill recovery, or successful acquisition/retention of the corrected associations. Conversely, those successes do not make the failed completion criteria or operational budget disappear.

## 8. Longer sequences and old-state carry
Separate 128-event suffix stress after preparation:

| Condition | Correct / answers | Accuracy | Entire continuations | False DONE | Current cue classes |
|---|---|---|---|---|---|
| Float weights / FP32 moments | 8,189/8,192 | 99.96338% | 63/64 (98.44%) | 0 | 32/32 |
| Two-bit weights / FP32 moments | 8,192/8,192 | 100.00000% | 64/64 (100.00%) | 0 | 32/32 |
| Two-bit weights / 8-bit moments | 8,192/8,192 | 100.00000% | 64/64 (100.00%) | 0 | 32/32 |


After correction/repair on that stress panel:

| Condition | Correct / answers | Accuracy | Entire continuations | False DONE | Current cue classes |
|---|---|---|---|---|---|
| Float weights / FP32 moments | 8,139/8,192 | 99.35303% | 52/64 (81.25%) | 9 | 32/32 |
| Two-bit weights / FP32 moments | 8,124/8,192 | 99.16992% | 49/64 (76.56%) | 7 | 32/32 |
| Two-bit weights / 8-bit moments | 8,156/8,192 | 99.56055% | 53/64 (82.81%) | 4 | 32/32 |


Only 16 underlying stress histories are present, repeated over four parents. Longer histories again distinguish high event accuracy from wholly correct work. Q2_M8 has 99.56% event accuracy but 53/64 (82.81%) entirely correct stress continuations after repair.

Secondary primary-panel CARRY after repair:

| Condition | Correct / answers | Accuracy | Entire continuations | False DONE | Current cue classes |
|---|---|---|---|---|---|
| Float weights / FP32 moments | 32,603/32,768 | 99.49646% | 958/1024 (93.55%) | 12 | 32/32 |
| Two-bit weights / FP32 moments | 32,657/32,768 | 99.66125% | 970/1024 (94.73%) | 8 | 32/32 |
| Two-bit weights / 8-bit moments | 32,554/32,768 | 99.34692% | 953/1024 (93.07%) | 8 | 32/32 |


This is continuity from the original float parent's state, not from each post-preparation accepted generation. It does not establish multi-night state migration, safe adoption or a complete NSS lifecycle. REBUILD remains primary.

## 9. What is actually low-bit?
The Q2 quantizer stores four row-specific affine values using codes 0..3. For each row, min/max include zero, scale=max((hi-lo)/3,1e-8), zero_point=clip(round_even(-lo/scale),0,3), and code=clip(round_even(w/scale)+zero_point,0,3). Effective coefficients are FP32-rounded (code-zero_point)*scale. An identity straight-through surrogate carries gradients to the FP32 master; quantizer derivatives are not claimed exact.

| Surface | Actual representation |
|---|---|
| Matrix codes in saved inference model | Four 2-bit codes per byte |
| Row scales and all biases | Float32 |
| Row zero points | uint8 |
| Masters and gradients during training | Float32 |
| Effective quantized training matrices and activations | Float32 tensors |
| M32 optimizer arrays | Float32 |
| M8 optimizer arrays | int8 linear first moment; uint8 square-root second moment; FP32 block scales |
| Inference hidden state, gates and accumulations | Float64 |
| C optimizer arithmetic | Double local arithmetic, FP32 updated moments/masters, then optional packing |

This is full-parameter quantization-aware learning with compressed optimizer state. It is not native two-bit arithmetic throughout forward/backward or a two-bit total learner. M8 uses one 128-element scratch pair, not persistent full decoded moment arrays. Before parameter update, the previous quantized moments are decoded; new moments are computed and used at higher precision, then compressed for the next step. The second moment's square-root representation is a custom choice. This is not the nonlinear bitsandbytes quantizer or a reproduction of the 8-bit Optimizers paper.

## 10. Real storage and learning-array accounting

| Numerical inference component | Bytes |
|---|---|
| Matrix codes (17,856 entries) | 4464 |
| 393 FP32 scales | 1572 |
| 393 uint8 zero points | 393 |
| 393 FP32 biases | 1572 |
| Total Q2 numerical payload | 8001 |
| Complete Q2 file including header/digest | 8703 |
| Original FP32 coefficients | 72996 |


The numeric model body is 9.12 times smaller (89.04% less) than the float32 coefficient array. It averages about 3.51 bits per original coefficient once scales/zero points/biases are included, rather than two bits for the whole model. The 393 biases are not quantized. During packed inference the C kernel directly reads codes, with no persistent expanded dense matrix; accumulation/nonlinear arithmetic remain float64. The Python demonstration still imports Torch, so its process does not occupy only 8,001 bytes.


| Learning arrays | Q2_M32 | Q2_M8 |
|---|---|---|
| Master weights | 72996 | 72996 |
| Gradients | 72996 | 72996 |
| Optimizer arrays including block scales | 145992 | 37658 |
| Sum of those arrays | 291984 | 183650 |
| Common C temporary block scratch (additional) | 1024 | 1024 |


Optimizer arrays save 108,334 bytes (74.21%). Masters+gradients+optimizer save 37.10%. The master+moment portion alone is persistent across steps; gradients are counted while present. This sum is not a measured total peak. Floating effective matrices (71,424 bytes per materialized set), quantization temporaries, activations, autograd bookkeeping, replay data, RNG and serialization copies remain. Because A and B have separate forwards, effective tensors may overlap in lifetime; one 71,424-byte figure is not the total temporary peak. M8 checkpoints are 125,035 bytes versus 230,467 for M32 here, including master weights, state, RNG and serialization overhead; checkpoint size is not live training RAM.

Peak logged main-process RSS across branches was 393,523,200 bytes, dominated by shared runtime/model/data allocations and not an isolated tensor-lifetime measurement. No 37% total-process or energy reduction is claimed.

## 11. Can we afford more training now?
Lower memory can enable a larger batch/model or prevent out-of-memory failure, but fixed-memory reduction does not itself shorten a step. More updates under a time/energy budget require higher throughput or other measured savings. This run has not demonstrated that.


| Arm | Mean retained training-core seconds / 1,120 updates | Mean preparation seconds |
|---|---|---|
| Float weights / FP32 moments | 10.0347 | 9.6859 |
| Two-bit weights / FP32 moments | 10.1107 | 9.7258 |
| Two-bit weights / 8-bit moments | 10.4694 | 10.0807 |


The compressed Q2 path is descriptively 3.55% slower than Q2 with wider optimizer arrays, and about 4.33% slower than float. These are per-step clocks from four sequentially executed parent comparisons with rotated arm order; not a separately interleaved, equal-quality, optimized-kernel benchmark. Discarded recovered work, preparation, import, checkpoint and audit costs are excluded from these retained-training-core means and accounted separately where available.

The dedicated inference timing uses the first eight development histories (56 events), one warmup and five interleaved repeats per backend/export, one CPU thread. It executes identical effective weights, inputs and initial state. Loading, decoding before timing, scoring and training are excluded.

| Parent / Q2 optimizer | Packed C ms | Decoded NumPy ms | Packed/decoded |
|---|---|---|---|
| 4101 / Q2_M32 | 7.463 | 2.952 | 2.53× |
| 4101 / Q2_M8 | 7.106 | 2.761 | 2.57× |
| 4102 / Q2_M32 | 7.210 | 2.732 | 2.64× |
| 4102 / Q2_M8 | 7.137 | 2.770 | 2.58× |
| 4103 / Q2_M32 | 7.080 | 2.717 | 2.61× |
| 4103 / Q2_M8 | 7.295 | 2.921 | 2.50× |
| 4104 / Q2_M32 | 7.243 | 2.833 | 2.56× |
| 4104 / Q2_M8 | 7.285 | 2.811 | 2.59× |


Direct scalar packed inference is approximately 2.50–2.64 times slower. This is a compact representation and executable reference, not an optimized BitNet/SIMD/GPU implementation. Avoiding expanded weights did not create a speed win in this implementation. It should not be extrapolated to optimized low-bit hardware or language models.

## 12. Tests, answers, and semantic review
Every raw evaluated output retains the input fixture, model/step/state binding, expected finite label, prediction and unedited scores. An independent set-of-completed-items interpreter checks the original bitmask labels. A wrong answer remains wrong even if a hypothetical external guard could block it; no inference guard corrected these arrays.

`docs/TESTS_AND_ANSWERS.md` contains all events and predictions for eight prospectively listed histories at preparation and repair endpoints, with each parent/arm shown. These chosen indices happen to cover the mixed/idempotent families, not all four; no all-family manual-review claim is made. Full automated finite-rule checks cover all arrays. Additional first-failure examples are explicitly retrospective and not prevalence estimates. Review is same-author inspection plus programmatic exact-rule checking, not an independent language critic.

One prepared Q2_M8 failure: parent 4101, history 52. All items were complete; CLEAR(3) reopened item 3 at event 28. Event 29 SET(5) was redundant. Item 3 remained unfinished, but the model said DONE. The evidence explicitly supports answer 3, so this is not a persistence ambiguity. A repaired-stage failure on history 17 similarly leaves item 2 pending through redundant events, yet returns DONE. Successful and failed histories both remain in the record.

## 13. Verification and operational exceptions
Six grouped preflight tests cover all 256 four-code packing patterns, quantizer edge cases and surrogate gradients, 4,608 exact state/event truth cases, M32/M8 arithmetic against a separate NumPy step, packed recurrence and corrupted-export rejection, and full-parameter gradients plus exact optimizer resumption. Final successful preflight uses 25 disposable updates. One failed pre-lock reference check and a separate diagnosis used nine each, making 43 total disposable applications.

That initial NumPy reference accidentally multiplied a gradient in float32 while the C contract used double local arithmetic. Correcting the reference before main lock resolved the scale mismatch; the C optimizer and tolerance were unchanged. Original failed code and diagnostic are retained.

All 264 saved output arrays, containing 1,019,904 repeated A observations, were independently recounted and replayed bit-exactly in fresh processes. All 72 checkpoint files and 48 packed exports verified. All 72 B stage probes also agreed with the reference and saved scores. Main recorded evaluation covers 166,323,200 hidden/logit scalar comparisons; zero violations, maximum absolute difference 9.969e-12 under 1e-9+1e-8*abs(reference). Fresh audit additionally includes B arithmetic: 166,365,248 comparisons, zero differing classes or tolerance failures. Counts are repeated numerical checks, not independent tasks; this is not exhaustive numerical admission of every training graph or future input.

The three new fixture files regenerate byte-for-byte. The original 19 source/input lock entries, four fixture lock entries, four separately versioned recovery-script/appendix entries and three post-result analysis/audit/benchmark entries remained unchanged. The selected source archive passed its original receipt hash, CRC and all 531 declared payload checks. No historical scores were regraded, and source archives were not merged.

### Two caller interruptions and the original work ceiling
A combined runner call stopped parent 4102/F32 after 37 journaled updates but only a durable step-0 checkpoint. Reexecution reproduced all 37 non-timing log rows exactly; at most one additional unjournaled update is unknown. Another call stopped parent 4103/Q2_M32 after journaled step 680 with a durable step-512 checkpoint. Resumption reproduced all 168 logged repeated updates exactly, again with at most one extra unjournaled update.

Thus 13,440 logical main updates required 13,645–13,647 actual main applications. Including 43 preflight applications, total actual work is **13,688–13,690**. **The original 13,440 actual-main cap was exceeded.** Separately versioned recovery appendices disclosed that before completing each interrupted branch. This remains an operational-budget exception, not a retrospective clean pass. No branch received additional logical training, a new optimizer recipe, target, selected seed or changed threshold. Unsaved inference and first-caller terminal time/RSS remain unknown. Final comparisons completed, but original cost compliance cannot be claimed.

Retained training-step clocks sum to 122.459 s; known discarded training clocks add 1.952 s, with up to two unlogged update durations unknown. Fresh model replay sums to 28.209 s. These exclude imports, development, verification preparation, reporting, packaging and other costs; they are not complete research wall time. Per-branch time/RSS limits were checked at updates and storage at stage writes, not enforced as an OS sandbox.

## 14. Decision and next question
**Retain two-bit matrices plus the compressed-moment optimizer as a promising bounded research candidate.** This pass demonstrates actual compact serving weights, near-complete preparation recovery, acquisition/retention of a changed association and smaller real optimizer arrays. It does not yet establish the declared complete low-bit learning/retention working point, universal optimizer equivalence, cheaper-per-step training, all-two-bit training or 1.58-bit BitNet equivalence.

The next proposed step is one retention-focused learning comparison using the successful acquisition control and both moment formats, before shrinking further. Remaining master/gradient/activation costs should then be addressed one at a time, with no hidden full-precision copies. Return to ternary as the longer-term target after or alongside a separately justified preparation question; do not rebrand this four-level affine GRU as BitNet. A from-start ternary path remains untested.

All non-low-bit research remains on hold. No new night, further tuning, extra fit, activation quantization, four-bit optimizer, smaller master, native low-bit training kernel or follow-up experiment was run after these outcomes. This is not an adopted NSS serving component.

## 15. Primary literature and attribution
[External 1] Dettmers et al., *8-bit Optimizers via Block-wise Quantization*, arXiv:2110.02861v2. The abstract establishes compressed optimizer statistics as a tested mechanism family. Our signed-linear/square-root custom SQ8 implementation is not the paper's complete method and does not inherit its performance claims.

[External 2] Microsoft's official `bitnet-b1.58-2B-4T-bf16` model card distinguishes wider training master weights from packed ternary inference, and notes that suitable execution is needed for efficiency. Our small GRU is not that architecture or pretrained model.

[External 3] Ma et al., *The Era of 1-bit LLMs*, arXiv:2402.17764v1, gives the ternary matrix-weight precedent. It does not demonstrate low-bit learning-state memory for this learner.

Exact URLs and limited source-read scope are recorded in `protocol/EXTERNAL_REFERENCES.json`. No external checkpoint, training corpus or algorithm implementation was downloaded for this pass. All measured results above come from the local retained experiment, not those papers.

## 16. Reproduction and evidence map
- `protocol/`: fixed recipe, environment, input/fixture locks and explicit recovery deviations.
- `inputs/`: exact four original parents and 64 replay batches per parent.
- `source/`: quantizer, packed C inference, common optimizer, trainer, preflight, analysis and audits.
- `fixtures/`: complete public event histories, labels, family identifiers and prefixes.
- `checkpoints/`: all 72 model/optimizer/RNG snapshots and complete logical update journals.
- `exports/`: 48 packed Q2 inference files.
- `results/`: all 264 raw arrays, 72 stage records, aggregate decisions, per-parent/family counts and timing samples.
- `failures/`: original pre-lock checker issue and both partial caller journals/recovery evidence.
- `audit/`: every saved-output recount/replay receipt, checkpoint/export identities and fixture regeneration.
- `docs/`: this report, exact test/answer views, architecture and Codex handoff.

Use `README.md` for the offline demo and verification. Original science drivers refuse to overwrite a completed branch; reproducing training requires a new output directory and explicit source/runtime binding. The shipped binary is Linux/x86-64; recompilation has a new binary identity and must be documented rather than pretending it matches the old hash. No universal hardware/native-Windows qualification.
