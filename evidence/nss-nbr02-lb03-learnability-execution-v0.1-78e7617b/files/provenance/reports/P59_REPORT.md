# NSS LB01-T3-TARGET — Can the useful two-bit model reach ternary?
## Model quantization: research, results, limits and decision
**Execution v0.1 | 29 September 2026 | COMPLETE_BOUNDED_COMPARISON / NO_TERNARY_WORKING_POINT / Q2_INTERIM_RETAINED**

## 1. ELI5: question, approach and outcome
Can the small checklist model keep its useful skill when the matrix weights have only three choices? We compared an immediate ternary switch, a gradual two-bit-to-ternary switch, and continued two-bit preparation. All four source models and twelve fixed-budget preparation paths completed. Every endpoint was fixed before confirmation scoring.

The immediate ternary path reached **32,283/32,768 answers (98.51990%)**, but only **863/1,024 wholly correct continuations (84.28%)**, with 65 false-DONE outputs. The gradual path reached **32,108/32,768 (97.98584%)**, 774/1,024 wholly correct (75.59%), with 211 false-DONE outputs. Neither met the declared ternary working point. The matched two-bit control remained at **32,764/32,768 (99.98779%)**, 1,023/1,024 wholly correct, with no false DONE on the primary panel.

This is model-weight quantization research. Preparation was used to obtain restricted weights; training acceleration, smaller masters/optimizers, new-cue learning, post-learning repair, HSA, DARP and deployment were not studied. Their prior results and current hold status remain unchanged. No fresh external literature or BitNet reproduction claim is made.

**Decision:** retain the useful Q2 working reference; preserve both genuine ternary candidates and their failures. This gradual-switch recipe does not earn adoption. Ternary remains a long-term candidate, but this pass does not reach its practical quality target. Moving to training-efficiency research still requires a separate user decision.

## 2. Exact model and source lineage
Four exact `Q2_M32` preparation checkpoints at step 1,024 from LB02-Q2-TRAIN, parents 4101–4104, initialize the three arms. All three arms within a parent begin with identical FP32 master tensors. Each receives fresh FP32 first/second moments, not inherited compressed optimizer notes. Source-parent hashes are checked before reuse. These are inherited learners, not four new randomized fits; ancestral preparation is an additional historical cost.

Model: GRUCell(26,64) plus Linear(64,9), 18,249 learned coefficients. All 17,856 matrix entries in the input, recurrent and output matrices are quantized. All 393 biases remain FP32. Scales are derived per row, not extra learned coefficients. The architecture and all original coefficients stay trainable during preparation.

Original full source archives were verified: LB02-Q2-TRAIN (580 declared payloads) and LB01-TERNARY (531). Their original receipt hashes, CRCs and exact member sets matched. Selected MASTER16 fixture members were independently compared with their manifest entries; its whole archive was not newly audited. Only selected inputs/source were copied into this delivery, not a merger of the historical archives. See `provenance/SOURCE_VERIFICATION.json`.

## 3. The controlled comparison
| Arm | Forward representation | Role |
|---|---|---|
| Q2_CONTROL | Four-level affine row quantization for all 1,024 updates | Matched useful-model reference |
| T3_DIRECT | Scaled -1/0/+1 from update 1 | Immediate conversion plus preparation |
| T3_RAMP | (1-alpha) Q2(W) + alpha T3(W); alpha=(step-1)/511, clipped to [0,1] | Gradual transition, ending genuinely ternary |

Step 1 of the ramp is Q2-only. Steps 2–511 use a mixture that can have more than three values: they are **not ternary**. Steps 512–1,024 are pure ternary, giving 513 pure-ternary updates, including the last 512. Only the fully ternary fixed endpoint counts toward the target. The two paths have equal total updates, not equal numbers of pure-ternary updates or equal quantizer computation. By the time the ramp reaches ternary, its common learning rate has already decayed. This is an intrinsic schedule difference, not proof that gradual quantization is universally inferior.

Q2 reuses the earlier per-row affine four-code rule. T3 uses `s=max(mean(abs(W)),1e-8)` with float64 reduction stored in FP32; `q=clip(round_even(W/s),-1,1)` and effective weights `s*q`. All forward effective weights are the exact hard quantizer output. The backward pass uses an identity straight-through surrogate. This derivative is a preparation approximation, not the mathematical derivative of rounding.

Both quantizers and the mixture use unchanged FP32 masters, gradients and M32 moments. Common custom C Adam uses beta .9/.999, epsilon 1e-8, zero decay, global clipping at 1, and double local update arithmetic with FP32 stored arrays. The fixed learning-rate schedule is cosine .003 to .0003. Each of the 64 retained A batches (32 histories of 32 events) is used 16 times, with the unchanged eight original cue targets also practiced at every update. No new cue or repair schedule is added.

## 4. Public task contract, fixtures and units
All eight checklist items begin unfinished. SET(i) completes item i until CLEAR(i) or RESET. CLEAR reopens i; RESET reopens all; NOOP changes nothing. The required response after an event is the smallest unfinished item, or code 8/DONE only when all are complete. The learner sees event codes and its own state, not target masks, labels, answers or checker feedback. These rules explicitly establish persistence, avoiding the earlier English temporal ambiguity. B cues remain the eight reset-state inputs with original alternating binary targets.

Development has 16 histories (24 prefix +32 scored events); confirmation has 256 of that length; separate stress has 64 histories (64 prefix +192 scored events). All panels contain equal mixed/idempotent/revision/reset families. Seeds and generators were frozen before training. Exact 32-event windows were excluded against accessible replay streams and prior copied LB01/LB02/MASTER16 panels, then between new panels. All original ancestral training data were not available; primitive events, task rules and shorter patterns recur. This is known-rule generalization, not new-procedure or language competence.

Primary REBUILD executes each full history from zero state under its own candidate. No CARRY/migration comparison is performed. Confirmation was first scored only after every final checkpoint was frozen. Curves at 256/512/768 use development only; no intermediate checkpoint replaces a disappointing final.

Primary counts are 256 histories x32 suffix events x4 inherited parents =32,768 answer observations and 1,024 continuations. Stress counts are 64 histories x192 suffix events x4 =49,152 answers and 256 continuations. Shared histories, stages, fields and arms are repeated measurements, not independent experiments. No population-significance or equivalence claim is made.

## 5. Main confirmation results
| Profile | Correct / events | Answer accuracy | Entire continuations | False DONE | Working parents |
|---|---|---|---|---|---|
| Original float parent | 32,743/32,768 | 99.92371% | 1020/1024 (99.61%) | 0 | 4/4 |
| Unchanged prepared Q2 | 32,764/32,768 | 99.98779% | 1022/1024 (99.80%) | 3 | 4/4 |
| Direct conversion, no new preparation | 7,261/32,768 | 22.15881% | 0/1024 (0.00%) | 0 | 0/4 |
| Q2 control, 1,024 updates | 32,764/32,768 | 99.98779% | 1023/1024 (99.90%) | 0 | 4/4 |
| Immediate ternary, 1,024 updates | 32,283/32,768 | 98.51990% | 863/1024 (84.28%) | 65 | 0/4 |
| Gradual transition, 1,024 updates | 32,108/32,768 | 97.98584% | 774/1024 (75.59%) | 211 | 0/4 |

All rows have 32/32 original cue classes correct. Minimum target probabilities satisfy .80; they are model scores, not calibrated reliability guarantees. The direct conversion control starts from the same prepared Q2 masters and has no new preparation. Its 25,507 errors fall to 485 after T3_DIRECT, a **98.10% net reduction**. That is substantial recovery under the restriction, but residual failures still prevent a useful whole-task ternary result.

The Q2-parent row's zero *new* false-DONE count is by self-reference; it has three actual false-DONE answers. It is not a new zero-error qualification. Q2_CONTROL has no primary false-DONE and meets the current working-point rule in four parents.

### Every parent — correct events; whole continuations; false DONE
| Parent | Q2 control | Immediate ternary | Gradual ternary |
|---|---|---|---|
| 4101 | 8192/8192; 256/256; 0 | 8053/8192; 208/256; 15 | 7978/8192; 180/256; 71 |
| 4102 | 8188/8192; 255/256; 0 | 8066/8192; 209/256; 13 | 8042/8192; 206/256; 45 |
| 4103 | 8192/8192; 256/256; 0 | 8094/8192; 223/256; 14 | 7988/8192; 175/256; 58 |
| 4104 | 8192/8192; 256/256; 0 | 8070/8192; 223/256; 23 | 8100/8192; 213/256; 37 |

Immediate ternary has more correct primary event answers than ramp in three parents; ramp has 30 more correct events in 4104, but fewer fully correct histories and more false-DONE there. Do not assemble a winner by choosing a different path for each seed.

### Family-level breakdown
| Profile | Family | Correct | Total | Whole /256 | False DONE |
|---|---|---|---|---|---|
| Q2 control, 1,024 updates | mixed | 8192 | 8192 | 256 | 0 |
| Q2 control, 1,024 updates | idempotent | 8188 | 8192 | 255 | 0 |
| Q2 control, 1,024 updates | revision | 8192 | 8192 | 256 | 0 |
| Q2 control, 1,024 updates | reset | 8192 | 8192 | 256 | 0 |
| Immediate ternary, 1,024 updates | mixed | 8080 | 8192 | 211 | 13 |
| Immediate ternary, 1,024 updates | idempotent | 8025 | 8192 | 213 | 27 |
| Immediate ternary, 1,024 updates | revision | 8096 | 8192 | 231 | 4 |
| Immediate ternary, 1,024 updates | reset | 8082 | 8192 | 208 | 21 |
| Gradual transition, 1,024 updates | mixed | 8015 | 8192 | 182 | 57 |
| Gradual transition, 1,024 updates | idempotent | 7973 | 8192 | 182 | 75 |
| Gradual transition, 1,024 updates | revision | 8135 | 8192 | 224 | 24 |
| Gradual transition, 1,024 updates | reset | 7985 | 8192 | 186 | 55 |

## 6. Longer histories expose the reliability cost
| Profile | Correct / events | Answer accuracy | Entire continuations | False DONE | Working parents |
|---|---|---|---|---|---|
| Original float parent | 49,146/49,152 | 99.98779% | 254/256 (99.22%) | 0 | 4/4 |
| Unchanged prepared Q2 | 49,120/49,152 | 99.93490% | 250/256 (97.66%) | 15 | 4/4 |
| Direct conversion, no new preparation | 10,310/49,152 | 20.97575% | 0/256 (0.00%) | 0 | 0/4 |
| Q2 control, 1,024 updates | 49,147/49,152 | 99.98983% | 253/256 (98.83%) | 2 | 2/4 |
| Immediate ternary, 1,024 updates | 48,401/49,152 | 98.47209% | 94/256 (36.72%) | 139 | 0/4 |
| Gradual transition, 1,024 updates | 47,936/49,152 | 97.52604% | 53/256 (20.70%) | 356 | 0/4 |

The two-bit control remains 99.98983% correct per event and 253/256 whole. Its two false-DONE errors are newly induced at positions where the Q2 parent was correct, so it passes the separate strict stress screen in only two of four parents. That limit stays explicit even though its aggregate long-history performance is strong. Neither ternary arm passes stress: immediate reaches only 94/256 whole histories and gradual 53/256. Near-98% individual accuracy cannot be equated with reliable completion of a long sequence.

## 7. Development curves and what they do not establish
Each entry is correct scored development answers out of 512, not an independent test set.
| Parent | Arm | 256 | 512 | 768 | 1024 |
|---|---|---|---|---|---|
| 4101 | Q2_CONTROL | 511 | 512 | 509 | 512 |
| 4101 | T3_DIRECT | 462 | 499 | 505 | 503 |
| 4101 | T3_RAMP | 512 | 488 | 494 | 499 |
| 4102 | Q2_CONTROL | 502 | 512 | 512 | 512 |
| 4102 | T3_DIRECT | 489 | 478 | 503 | 503 |
| 4102 | T3_RAMP | 512 | 483 | 500 | 486 |
| 4103 | Q2_CONTROL | 512 | 512 | 512 | 512 |
| 4103 | T3_DIRECT | 488 | 486 | 504 | 506 |
| 4103 | T3_RAMP | 496 | 490 | 501 | 500 |
| 4104 | Q2_CONTROL | 512 | 510 | 512 | 512 |
| 4104 | T3_DIRECT | 496 | 474 | 499 | 506 |
| 4104 | T3_RAMP | 507 | 479 | 502 | 505 |

The ramp's step256 weights are still a mixture (alpha=255/511). Those answers do not demonstrate ternary competence. Several ramps lose accuracy by the fully ternary stage; they may then improve during continued preparation, but none becomes an eligible ternary endpoint. These curves do not isolate the causal effect of abruptness: the schedule also changes exposure to pure ternary and learning-rate timing. No extra epochs, altered scales or selected stopping point were tested after observing this pattern.

The earlier LB01-TERNARY reported 96.48% on another panel, using another starting point and 512 preparation updates. The present 98.52% is not a clean causal improvement over that old percentage. The valid comparison is within this pass against the common prepared parent and matched Q2 continuation.

## 8. What is actually packed and what stays wide?
| Stored component | Q2 bytes | T3 bytes |
|---|---|---|
| Matrix codes (17,856) | 4,464 | 3,573 |
| Per-row FP32 scales | 1,572 | 1,572 |
| uint8 zero points | 393 | 0 |
| FP32 biases | 1,572 | 1,572 |
| Numerical model body | 8,001 | 6,717 |
| Complete endpoint file including header/hash | 8,703 | 7,604 |

Original FP32 coefficients occupy 72,996 bytes. Ternary numerical storage is **90.80% smaller** than that original coefficient body and **16.05% smaller** than Q2. Complete files differ in header length, so numerical bodies are the comparable representation count. The current ternary header yields 7,604 bytes, not the earlier archive's 7,556; the numerical body is unchanged.

Five trits per byte use 1.60081 actual code bits per matrix entry with padding. `log2(3)` describes the 1.58496-bit information capacity of a ternary symbol, not physical 1.58-bit memory cells. Including scales and wider biases, the body averages about 2.945 bits per original learned coefficient. This is not an all-1.58-bit model or a BitNet Transformer.

Direct packed C execution extracts codes without retaining a dense decoded weight matrix. FP32 scales and biases are promoted; recurrent state, gates and accumulation are FP64. The audit process also deliberately holds decoded NumPy/Torch references, outputs and fixture data, so process RSS is not the packed body size. There is no claim of integer-only execution, activation quantization, native GPU acceleration, or a faster kernel. No throughput benchmark was run in this pass.

Training master, gradient and M32-array storage remains 72,996+72,996+145,992=291,984 bytes before activations, effective weights, scratch, RNG and other overhead. Each floating effective matrix set adds 71,424 bytes; the mixture can create additional temporary sets. These are disclosed preparation costs, **not another training-memory experiment**. No smaller-master or optimizer-state intervention was made.

## 9. Test validity, raw answers and failure evidence
All exact event inputs and raw class scores are retained before scoring. The independent set-based interpreter checks the bitmask-derived target over every saved array, and preflight exhausts all 4,608 state/event combinations. Test validity follows from the explicit public finite state rules, not a hidden persistence assumption. A false completion remains a model error even if a future harness might reject it. No protection mask edits an output.

`docs/TESTS_AND_ANSWERS.md` renders the eight prospectively named confirmation histories for all six main profiles and all parents, including correct and incorrect responses. This is 192 history/profile records, 6,144 scored suffix observations. It is not a claim of independent human review of all raw arrays. The report's concrete examples received same-author inspection; remaining coverage is programmatic exact-rule checking, not a broad semantic critic.

Retrospective first-failure examples are stored separately in `results/EXAMPLES.json`, with their original NPZ locators:
- Parent4101/T3_DIRECT/history133: event29 SET(1) leaves items2 and4 pending. At event30 SET(2), item4 remains pending, but the model outputs DONE. At event31 redundant SET(3), it returns to4. The false-DONE claim at event30 remains a failure.
- Parent4101/T3_RAMP/history0: after event24 SET(4), items2 and7 remain pending. Event25 SET(2) leaves7 pending; the model outputs DONE and repeats it after NOOP. This is not an ambiguous assignment or missing-record test.

Repeated initial failures are illustrations, not estimates of prevalence. No fault-specific repair or additional scoring label was substituted after observation.

## 10. Decision criteria and interpretation
The prospectively fixed primary per-parent rule requires >=98% event accuracy, >=90% wholly correct continuations, <=1 percentage-point event loss relative to its own prepared Q2 parent, zero newly induced false-DONE at Q2-correct positions, and all eight original cue answers with minimum score .80. Three of four parents are needed for the cohort. Stress is scored separately with the same absolute quality thresholds and zero new false-DONE. These are engineering bands, not significance tests.

Neither ternary arm reaches the primary working point in any parent. The direct path's failure is not merely its crossing an arbitrary tiny tolerance: whole continuations drop to84.28%, and to36.72% on longer stress. The control remains useful. The no-learning conversion control's zero false-DONE is not a virtue when almost all sequences are wrong.

**Supported:** real packed ternary weights; exact-code execution; major recovery through fixed QAT; dependable bounded Q2 reference relative to these comparisons; preserved original cue associations. **Not supported:** useful ternary whole-task working point, advantage of this ramp, proof of all ternary models' limits, training-efficiency improvement, model growth/plasticity, post-update repair, full NSS companion qualification.

The tested Q2 and T3 codebooks differ in symmetry and row scaling, not only cardinality. A row-scale/codebook calibration comparison or ternary-from-start preparation would be distinct future hypotheses. Neither ran here. Do not automatically begin another sweep or select a revised schedule from confirmation. Two-bit remains the accepted interim direction; user approval is still needed to move research into efficient training.

## 11. Verification, reproducibility and resource accounting
All nine preflight groups passed, using 12 disposable optimizer applications. A pre-lock enumeration test incorrectly compared big-endian trit tuples with a little-endian packed order. The packing implementation was unchanged; the test ordering was corrected before any optimizer step and before main source lock. Original code and traceback remain in `failures/prelock_pattern_order/`. No main training/evaluation interruption, repeated tail, replacement seed, additional epoch or post-result model change occurred.

- **12,288 actual main +12 preflight =12,300 optimizer applications**, below the 12,336 total cap; 12 complete preparation paths.
- **168 raw arrays** independently recounted and replayed bit-for-bit in fresh processes:522,240 scored A answers,791,040 all-event predictions including prefixes,480 B answers.
- **52 packed exports** independently decoded and checked;72 continuation checkpoint files verified (60 distinct staged states plus12 latest aliases); four exact prepared source parents also verified.
- **12 final packed split/resume checks** reproduce the uninterrupted output. This is same-model inference restart, not state migration to different weights.
- **106,006,400 recorded evaluation numerical comparisons**, zero breaches of1e-9+1e-8*abs(reference), maximum absolute difference2.576e-13. These compare implementations using the same effective weights, not quantized predictions to unquantized output. They are not exhaustive verification of every backward graph or future input.
- Three fixture files regenerate byte-for-byte. Original37 main source/input entries,4 fixture entries,12 post-training endpoint/journal bindings and the separately frozen audit script remain unchanged. Audit, reporting and file-accounting code is labeled post-result.

| Arm | Mean training-core seconds /1024 | Maximum logged training RSS bytes |
|---|---|---|
| Q2_CONTROL | 9.761 | 329,105,408 |
| T3_DIRECT | 9.436 | 329,043,968 |
| T3_RAMP | 9.904 | 329,183,232 |

Total retained training-core time: **116.406s**. Full fresh-process model replay audit: **26.308s**. Maximum logged training RSS:329,183,232bytes; maximum audit RSS:407,932,928bytes. These include framework/data and are not per-format isolated model memory. They exclude source inspection, compilation/imports, development, packaging, documentation and other calls; they are not the whole research bill. Sequential noninterleaved preparation clocks are accounting, not an efficiency claim.

Resource enforcement is sampled rather than an OS sandbox. Training checks180s per-branch and2GiB RSS on update boundaries; the evidence guard is224MiB with pre/post declared writes. CONFIG also names a120s evaluation-profile bound, but the shared live guard uses180s; the strict120s figure was verified from all completed profile receipts (maximum 1.488s), not independently enforced at that value. B-array writing is covered by the enclosing profile storage checks rather than a per-allocation hard guard. These instrumentation limits do not alter a result, but prevent overstating resource enforcement.

## 12. Evidence map and reproduction
- `protocol/PROTOCOL.md`, `CONFIG.json`, original locks: prospective scope and criteria.
- `inputs/parents/`, `inputs/replay/`, `inputs/exclusions/`: exact selected ancestors and datasets; no full historical archive merger.
- `source/target.py`: fixed quantizers/transition schedule, parents, fixtures, effective weights and evaluation.
- `source/train_target.py`: bounded checkpointed preparation; `evaluate_target.py`: final and development-only profiles.
- `source/analyze_target.py`: pre-main frozen result calculations; `audit_target.py`: separately frozen post-result independent recount/replay; `finish_audit.py`: file/data accounting only.
- `source/core.py`, `legacy_core.py`, `kernels.c`, `ternary.c`, `task.py`: reused model/optimizer/packed kernels/task.
- `checkpoints/`: retained stage weights, optimizer/RNG state, all update journals and complete receipts.
- `exports/`: actual `.q2`/`.t3w` models. Intermediate ramp256 cannot be exported as ternary.
- `fixtures/` and `results/*.npz`: complete administered histories and unedited outputs/scores; JSONs bind checkpoint, fixture, source and scores.
- `audit/FINAL_AUDIT.json`, `REPLAY_*.json`, `PREFLIGHT.json`: check coverage and counts.
- `docs/TESTS_AND_ANSWERS.md`, `results/EXAMPLES.json`: prospective example sheets and separate retrospective first failures.

The full archive includes runnable code and all retained current evidence. The compact review package omits checkpoints, packed exports and large raw arrays and cannot independently reproduce neural execution. Checksums establish integrity, not external replication or authentication of an untrusted publisher.

**Final disposition:** retain Q2 as the working model-quantization reference; retain ternary candidates as useful but underqualified. Park this gradual-transition recipe. Do not promote training optimization or post-learning repair back into the current scope. No follow-on experiment or deployment is authorized by the results.
