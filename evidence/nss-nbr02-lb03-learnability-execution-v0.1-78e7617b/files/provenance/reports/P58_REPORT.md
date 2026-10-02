# NSS LB02-MASTER16 — Smaller working weights during two-bit training
## Research, results, resources and decision · Execution v0.1
**29 September 2026 | COMPLETE_BOUNDED_SAME_TASK_CONTINUATION / MASTER_ARRAY_SAVING / NO_NEW_TASK_OR_REPAIR_PHASE.**

## 1. ELI5 question and outcome
Can we halve the more precise working copies that learning keeps behind the two-bit inference weights, while continuing the same useful skill? Yes on this bounded continuation: both16-bit variants meet the new prospective working screen in all four inherited models. Nearest rounding finished with one wrong checklist answer in32,768, stochastic rounding with two, and the matched32-bit-master control with four. These tiny differences do not establish precision superiority.

The result concerns further practice of an ALREADY PREPARED model. It does not establish from-scratch16-bit-master learning, new-skill acquisition, preserved lifetime plasticity, all-two-bit training, an optimal rounding rule or a whole-NSS product. The original checklist and original eight cue associations never change. No new-cue-plus-repair schedule occurs.

## 2. Lineage and what changed
Four exact Q2_M8 step1024 preparation checkpoints from LB02-Q2-TRAIN were reused, including all4101–4104. The source ZIP, its original receipt hash, CRC, exact membership and580 declared payload hashes were verified. Only selected source/code/input/checkpoint files were copied; original archives were not merged or altered. These are the competent pre-correction checkpoints, not the later repaired models.

Each model contains18,249 learned coefficients:17,856 matrix values and393 biases. The GRUCell(26,64)+Linear(64,9) architecture is unchanged. All parameters remain eligible for updates; no adapters, HSA, DARP or language reader is added.

| Surface | M32 control | M16_NEAREST | M16_STOCHASTIC |
|---|---|---|---|
| Forward matrix values | Same four-level row-affine quantizer | Same | Same |
| Stored matrix masters | Float32 | IEEE float16 | IEEE float16 |
| Write rounding | Float32 result retained | Nearest-even | Adjacent-value stochastic |
| Biases and leaf gradients | Float32 | Float32 | Float32 |
| Stored moments | Inherited custom8-bit SQ8, FP32 scales | Same | Same |
| Training forward/backward | Float32 | Float32 | Float32 |
| Evaluation recurrent arithmetic | Float64 | Float64 | Float64 |

Both16-bit arms begin from the SAME nearest-even conversion. Thus their difference after training isolates the subsequent write-rounding choice, including its nonlinear trajectory consequences. M32 versus either16-bit branch includes the initial master cast. Initial conversion results are separately recorded, not hidden in final scores.

## 3. Actual implementation and memory boundary
The stored master is a NumPy float16 buffer for the three matrices and float32 for biases. A small C row scratch (at most64 floats) calculates the same two-bit affine quantization directly from that buffer. It emits transient float32 EFFECTIVE quantized matrices. Those tensors are autograd leaves; their gradients are passed to the stored masters using the inherited identity straight-through approximation. The quantizer derivative is not claimed exact.

There is NO persistent dense FP32 master shadow in the16-bit training implementation. Effective weights are nevertheless wide, and gradient/activation/autograd costs remain. Source checkpoint loading, audits and serialization can temporarily hold additional copies; the array reduction is not a whole-process peak reduction.

The custom C optimizer uses the inherited128-entry blockwise moment encoding: signed-linear first moment and unsigned square-root second moment with FP32 scales. It decodes/updates a block using local wide arithmetic and recompresses it. Updated masters are first rounded to FP32; FP16 nearest or stochastic storage follows. SR draws one SplitMix64 number for every matrix entry each update, including exactly representable results. The state is checkpointed per tensor. There is no saved full-precision per-weight residual.

One effective-weight set is shared by the A and B forwards in ALL three new implementations. The same-task precision comparison uses this common new execution arrangement; times are not directly comparable to the older duplicate-materialization trainer. Preflight checked exact identity-STE gradient parity and exact agreement of the new M32 update with the inherited C optimizer on a fixed arithmetic test.

## 4. Task, data and preparation
All eight items start unfinished. SET(i) makes i done until CLEAR(i) or RESET. CLEAR(i) reopens i. RESET reopens all. NOOP changes nothing. The answer is the smallest unfinished item;8 means DONE only when all are done. These public rules state persistence explicitly. The network sees event IDs/one-hot values, not target masks or expected labels. Original B labels remain0,1,0,1,0,1,0,1.

Each of12 branches takes256 updates using the same64 retained32×32-event A batches in stored order, repeated four times. Every update minimizes mean A cross-entropy plus mean B cross-entropy over all8 original cues. LR=.0003, source betas.9/.999, epsilon1e-8, no decay, global clip1.0. Moments and the optimizer counter continue from source step1024; final counter1280. This is not a fresh optimizer or novel acquisition phase.

Fresh development16, confirmation256 and stress16 histories were fixed before main work. Confirmation is64histories/family (mixed,idempotent,revision,reset),24prefix+32suffix; stress32prefix+128suffix. Exact full histories and32-event windows were checked against the available64 training batches/parent, three previous LB02 panels, and all new panels. No overlap rejection was needed. This is not an exclusion audit of every historical NSS corpus; familiar shorter sequences/rules recur.

Stages0 and256 are evaluated on all panels;64 is development-only. The fixed256 endpoint is primary; no favorable checkpoint or rounding seed is selected. The original source checkpoint had already been selected through prior preparation, so this is not independent random-initialization evidence.

## 5. Primary results — all candidates retained

| Master format | Correct/32,768 | Event accuracy | Whole/1,024 | False DONE | Original cue classes |
|---|---:|---:|---:|---:|---:|
| 32-bit matrix masters | 32,764/32,768 | 99.98779% | 1022/1,024 | 0 | 32/32 |
| 16-bit masters, nearest rounding | 32,767/32,768 | 99.99695% | 1023/1,024 | 0 | 32/32 |
| 16-bit masters, stochastic rounding | 32,766/32,768 | 99.99390% | 1022/1,024 | 1 | 32/32 |

All four parents remain included. The256 common histories are reused across modes and parents. The32,768 answers are event observations, not independent experiments. No confidence-interval/equivalence or overall architecture-superiority claim is made. All original B classes remain correct, with target probabilities near1; these are not calibrated real-world reliability estimates.

### Initial cast versus final continuation

| Format | Initial confirmation correct | Initial whole | Final correct | Final whole |
|---|---:|---:|---:|---:|
| 32-bit matrix masters | 32768/32,768 | 1024/1,024 | 32764/32,768 | 1022/1,024 |
| 16-bit masters, nearest rounding | 32767/32,768 | 1023/1,024 | 32767/32,768 | 1023/1,024 |
| 16-bit masters, stochastic rounding | 32767/32,768 | 1023/1,024 | 32766/32,768 | 1022/1,024 |

The FP32-master parent is perfect on this fresh finite panel before continuation. The initial FP16 cast introduces one observed error. Nearest-rounding continuation retains one error; ordinary FP32 continuation introduces four errors; stochastic continuation ends with two. This does not mean further practice is universally needed or that FP16 improves the model. The useful claim is preserved high working quality with smaller master storage.

### Parent-level final results

| Parent | M32 correct / whole / falseDONE | M16 nearest | M16 stochastic |
|---|---|---|---|
| 4101 | 8191/8192;255/256;0 | 8192/8192;256/256;0 | 8192/8192;256/256;0 |
| 4102 | 8192/8192;256/256;0 | 8192/8192;256/256;0 | 8192/8192;256/256;0 |
| 4103 | 8189/8192;255/256;0 | 8191/8192;255/256;0 | 8191/8192;255/256;0 |
| 4104 | 8192/8192;256/256;0 | 8192/8192;256/256;0 | 8191/8192;255/256;1 |

Every final arm scores8,192/8,192 events and64/64 whole continuations on the SEPARATE16-history longer suffix panel pooled over parents. That is a small fixed stress check, not an indefinite-horizon guarantee. The final development values and per-family counts remain in raw JSON.

## 6. Prospective working-point decision
A new parent-level screen requires >=98% event and>=90% whole accuracy, all8 B classes with minimum target probability>=.8, and losses no greater than0.1percentage point event accuracy or2points whole-history accuracy versus the matched M32 final; no more than one extra falseDONE is allowed. At least3/4 parents plus>=15% saving in counted master+gradient+moment arrays are required. Both16-bit arms meet this local screen in4/4 parents.

The one-extra-falseDONE allowance was fixed in THIS protocol before any confirmation result. It is not the earlier zero-new-error rule and does not retroactively pass older gates. The stochastic branch adds one falseDONE in parent4104; that remains explicitly reported, notwithstanding passing the new practical screen. There is no serving adoption or deployment.

## 7. Storage result — real arrays, not total RAM

| Counted array | M32 | Either M16 |
|---|---:|---:|
| Matrix working copies | 71,424 B | 35,712 B |
| Bias working copies | 1,572 B | 1,572 B |
| All master arrays | 72,996 B | 37,284 B |
| Float32 gradients | 72,996 B | 72,996 B |
| 8-bit optimizer notes and scales | 37,658 B | 37,658 B |
| **Subtotal** | **183,650 B** | **147,938 B** |

The targeted subtotal saves35,712bytes: **19.45%** beyond the previous mixed-precision M8 setup. Matrix masters alone halve; all master arrays decrease48.92% because biases remain FP32. Packed inference stays two-bit and its numerical payload remains8,001bytes. These are different representations serving different roles.

The same actual batch32 graph/backward memory probe also recorded72,996bytes of effective-weight tensors and2,276,520bytes of unique saved numerical tensor storage excluding effective weights. With48bytes of RNG and1,024bytes of optimizer scratch included, the accounted storage union is2,534,238bytes for M32 versus2,498,526bytes for M16—only about1.41% less for that broader union. It is a storage-union diagnostic, not simultaneous peak allocation or an isolated allocator measurement. Some saved tensors have different lifetimes; Python, input corpus, allocator retention and libraries are additional.

**The entire training process did not become19.4% smaller.** Observed process RSS is dominated by runtime/data/activations at this scale. This experiment demonstrates removal of one real array cost, not an OOM-bound workload rescue or a forecast of savings on a billion-parameter model.

## 8. The rounding tradeoff — quality retention is not full plasticity

| Mode | FP32-proposed changes rounded back to old stored value | Stored changes across updates | Final changed Q2 codes (all parents) |
|---|---:|---:|
| M32 | 0.00% | 18,377,862 | 567 |
| M16_NEAREST | 93.72% | 1,152,712 | 7 |
| M16_STOCHASTIC | 89.84% | 1,867,043 | 1083 |

The counters include biases as well as matrices; biases are never down-rounded to FP16. They measure each write attempt across repeated updates, not independent parameters. Nearest rounding discards many tiny proposed updates. Stochastic rounding lets more of them change a stored value, but does not guarantee better nonlinear learning and here produced one additional falseDONE.

Nearest rounding has few effective-code and scale changes because these already-prepared weights lie within quantization cells and many proposed movements are smaller than an FP16 step. All parameters remain eligible and receive gradients; not all useful behavior changes require code changes (scales and biases also matter). Still, maintaining an already-mastered skill is easier than proving that small updates can accumulate into a new capability. A frozen/unchanged reference would already score very highly. Do not promote this to preserved lifetime plasticity or successful low-bit learning from a weak initialization.

## 9. Time and execution cost

| Mode | Mean256-update training core | Mean complete branch |
|---|---:|---:|
| M32 | 2.2333s | 2.4321s |
| M16_NEAREST | 2.3827s | 2.5731s |
| M16_STOCHASTIC | 2.4808s | 2.6711s |

Observed nearest/stochastic training-core costs were about6.7%/11.1% above M32. These are sequential branches with rotated arm order, not a dedicated repeated/interleaved speed trial. No throughput or energy win is claimed. CPP kernel conversion overhead is paid, not hidden. A packed model is not automatically a faster model.

Actual main work: **3,072 optimizer applications**, plus **18 disposable preflight applications =3,090 total**. No new fits, repeated/discarded updates or unexpected caller interruptions. Final audit additionally builds/backpropagates12 memory-probe graphs, withZERO optimizer steps. Five C arithmetic-step comparisons and the stochastic-rounding microchecks are recorded as engineering work, not model-training applications. Main counted supervision:3,170,304 repeated target labels.

Recorded training cores total28.387s; evaluated trajectory cores total11.562s; final audit3.024s. These exclude development, imports, packaging, setup and other work, not a whole research or nighttime cost. Maximum recorded training RSS327,716,864bytes; audit RSS356,511,744bytes. No per-method energy/peak-allocator claim.

## 10. Test validity, complete answers and failures
All queries use the exact checklist rules in section4; dated English observations and hidden persistence rules are absent. Every raw array retains full public event tokens, labels, logits, prefix position and checkpoint hash. The primary score covers suffix events; allprefix information is still retained. Independent set-based labels agree with the original bitmask source. The checker does not alter predictions.

Four prospectively selected histories0,64,128,192 span the four families. The tests-and-answers document shows every event and all12 final answers for those four histories, not only positives. It is same-author finite-rule review, not third-party language review. Additional first-error cases are separately marked retrospective, and are not used for training.

One stochastic error: parent4104/history104, event27(one-based), redundant SET(6). Item2 remains unfinished but the model briefly answers DONE; the next event returns to answer2. One nearest-rounding error: parent4103/history3, event26, CLEAR(1); item0 was already unfinished so0remains the smallest unfinished item, but the model chooses1. These are unambiguous errors; narrow successful rates do not erase them.

## 11. Verification and execution boundaries
Preflight passed10groups covering4,608mask/event truth pairs,34,560quantizer comparisons,FP16 boundary cases, stochastic adjacency/frequency/RNG restart, inherited M8 optimizer compatibility, identity-STE gradient parity, actual-gradient training, packed export and checkpoint mutation/dtype rejection. It used18 model optimizer applications. No failed main numerical condition or source change occurred.

Fresh-process audit recounted all84raw evaluation arrays (264,192scored suffix answers;437,760events including prefixes), reproduced all84logit/end-state arrays and672Bobservations exactly, verified108checkpoints and3,072journal cursors/state hashes. It checked25original main source/input lock entries plus the separately frozen analysis source. The audit script has its own post-result lock. No audit optimizer update occurred.

Main evaluated A trajectories include 63,912,960 repeated scalar comparisons across Torch-vs-NumPy and packed-C-vs-Torch hidden/logit paths, allwithin1e-9+1e-8abs(reference); maximum absolute discrepancy3.3751e-14. This is evaluated-trajectory agreement, NOT exhaustive backward/optimizer numerical qualification. Fresh-process replay is internal repeatability, not independent external replication.

New source/config lock preceded fixture generation and maintraining; analysis code was locked after training but before confirmation scoring. Preflight used inherited training inputs, not fresh confirmation. Training resource checks were applied each update and storage checks at checkpoint writes. The evaluated-output writer did NOT enforce the promised storage guard at each evaluation write; final measured size was belowbothcaps. That is a monitoring coverage deviation, not a claim of continuously enforced end-to-end limits. Output/time/RSS limitations remain reported. No evidence threshold was altered to obtain favorable behavior.

## 12. Decision and next scope
Keep the prepared2-bit/Q2+M8 models and the new FP16-master variants as working bounded research references. Both satisfy this prospective same-task continuation/storage screen. Nearest rounding is simpler and has no main-panel falseDONE here, but it suppresses tiny updates; do not make it the permanent plasticity choice from this near-saturated task. Stochastic rounding is viable in this narrow comparison, not a quality/speed winner.

This stays in the useful-quantization milestone. Post-new-learning repair remains deferred. If further training-precision work is needed, the sharp next question is whether16-bit masters can accumulate useful changes during an earlier, not-yet-mastered portion of the SAME preparation task, with a matched M32 reference—not a new-association-plus-repair phase. Alternatively, memory profiling identifies saved activation storage as a larger cost on this smallbatch; any such intervention should be separate. No follow-up or restoration of other research is executed by this outcome.

Ternary remains the longer-term target, two-bit acceptable in the interim. This is a GRU fixture, not a BitNet reproduction, native two-bit arithmetic through forward/backward, language competence, or deployment of the bridge.

## 13. Sources, reproducibility and archive
- S1: preserved original LB02-Q2-TRAIN report, architecture and receipt under `provenance/`; exact four sourcepreparation checkpoints and64 training batches/parent under `inputs/`. The original580payload archive was byte-verified, not scientifically rerun.
- S2: `protocol/PROTOCOL.md`,CONFIG,MAIN_LOCK,FIXTURE_LOCK,ANALYSIS_LOCK,AUDIT_LOCK; allreported new decisions/results follow those declarations. Raw numerical evaluation under `results/`; perstep journals andevery32stepcheckpoint under `checkpoints/`.
- S3: Gupta et al., Deep Learning with Limited Numerical Precision, ICML2015/PMLR37:1737–1746, https://proceedings.mlr.press/v37/gupta15.html. Primary abstract read29September2026. It motivates the rounding control through16-bit fixed-point results; no paper model, code or data was copied, and this FP16/Q2experiment does not inherit its performance claims.
- `audit/FINAL_AUDIT.json`,MEMORY_PROFILES,PARAMETER_CHANGES andPREFLIGHT contain independent numerical/code checks andactual resource representations.
- `docs/TESTS_AND_ANSWERS.md` preserves the exact test contract andselected unedited answers. `source/verify_package.py` checks integrity without model loading. See README forread-only inference/audit and the no-overwrite training rule.

No old NSS outcome, threshold, archive or model file was rewritten. Checksum validation protects against accidental corruption, not an adversary replacing data and its checksum.
