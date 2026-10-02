# NSS NBR02 SURFACE01 — Execution Report v0.1

**Date:** 27 September 2026  
**Disposition:** `STOP_BASELINE_COMPETENCE`  
**Main parent fits completed:** 4/4  
**Main correction/adaptation comparison:** NOT RUN  
**Main confirmation histories:** NOT GENERATED  
**Historical studies:** not loaded, modified, repaired, or requalified

## 1. Result and scope

SURFACE01 executed its fixed engineering preflight and all four planned parent fits. Three parents passed the prospective baseline screen. Parent 4103 produced six false-DONE answers within one admission history. Its event accuracy and whole-continuation accuracy were still above their thresholds; it failed specifically because the protocol permits zero false-DONE predictions.

The all-parent admission rule therefore stopped the entire main correction comparison. No seed was removed or replaced, no training was extended, no threshold was relaxed, and no confirmation histories were generated. The planned frozen-versus-adaptive transition and shared-versus-copied readout hypotheses remain unanswered by this execution.

The informative narrower observation is a **fixed-weight failure to preserve the correct answer through semantically idempotent events**. The exact checklist did not change during the six wrong answers. The model's output did change, and its assigned probability for the wrong DONE class increased substantially. This is a baseline behavioral failure, not evidence of correction-induced forgetting.

This report distinguishes frozen-protocol results from the explicitly labeled post-result analysis of retained arrays. The latter performed no new model forwards or optimizer applications. All reported counts are descriptive within this bounded synthetic task.

## 2. Executed instrument and task

The learner was a fresh `GRUCell(26,64) + Linear(64,9)` with **18,249 scalar parameters**. Each parent was initialized with its declared seed, 4101–4104. Inputs were individual one-hot SET, CLEAR, RESET, NOOP and B-cue events. A current bitmask, answer, or valid-action list was never supplied to the learner. No no-op filtering was used. Exact task routing, initial state and independent labels were provided by the harness; those are not learned capabilities.

Task A used eight completion flags, with output equal to the lowest unfinished item index or DONE. Indexing was 0–7; DONE was class 8. All training streams were 32 events. Each batch contained eight streams from each of four families: mixed edits, repeated/idempotent events, revisions, and resets. The TARGET_MASK_ROUNDS_V1 generator was specified in `protocol/EXECUTION_PROTOCOL.md` and source-locked before main fitting. Every parent saw all 256 exact checklist masks. New admission histories were not presented as new state-space semantics.

Task B originally mapped eight cues to their parity labels through the same unmasked nine-class head, each from zero state. Each parent received 2,000 Adam updates at learning rate 0.003, using the equally weighted A/B cross-entropy recipe and gradient clipping specified in the proposal. Main correction training would have changed one association per independent context, but this phase never began.

Admission used 256 histories per parent: 64 per family, half interrupted after eight events and half after 24. Thirty-two suffix events were scored for the main baseline gates; boundary answers were recorded separately. The histories were generated independently of training and checked for exact reuse, including 32-token windows. All four admission generators logged zero overlap rejections. Different parents had different training and admission RNG streams; the three passing parents were not separately tested on parent 4103's exact failing history.

## 3. Baseline admission

The unchanged family-level requirements were at least 99% event accuracy, at least 95% wholly correct 32-event continuations, and zero false DONE. All eight original B answers also had to be correct with assigned true-class probability at least 0.80.

| Parent seed | Correct A suffix events | Wholly correct continuations | False-DONE events | Original B | Admission |
|---|---:|---:|---:|---|---|
| 4101 | 8,192 / 8,192 | 256 / 256 | 0 | 8/8, minimum probability 0.99997211 | PASS |
| 4102 | 8,192 / 8,192 | 256 / 256 | 0 | 8/8, minimum probability 0.99997494 | PASS |
| 4103 | 8,186 / 8,192 | 255 / 256 | 6 | 8/8, minimum probability 0.99997555 | FAIL |
| 4104 | 8,192 / 8,192 | 256 / 256 | 0 | 8/8, minimum probability 0.99997537 | PASS |

All errors occurred in the idempotent family for parent 4103. That family had **2,042/2,048 correct events (99.7070%) and 63/64 wholly correct continuations (98.4375%)**. Both accuracy requirements passed. Only the zero-false-DONE requirement failed. Its other three families were perfect on this panel.

Pooling only for descriptive context, there were 32,762/32,768 correct suffix events (99.981689%) and 1,023/1,024 entirely correct continuations. These large denominators do not turn four independent parent fits into thousands of replications. The six incorrect events are one temporally connected failure within one history, not six independent failures.

**Gate source:** `evidence/outcome.json`; individual admissions in `evidence/admission_<seed>_summary.json`; compact counts in `analysis/parent_family_results.csv`. The retained-array audit independently recomputed every family count and found no differences.

## 4. The failure, event by event

Parent 4103, admission row 120, idempotent family, was interrupted after event eight. Its first error occurred nine suffix events later, at absolute event 17.

An earlier `CLEAR(5)` left item 5 incomplete while lower-index items still determined the answer. At event 16, completing item 0 made item 5 the next unfinished item, and the model correctly selected class 5. The following operations did not change the exact checklist:

`SET(1), NOOP, NOOP, SET(3), SET(3), SET(3)`

Items 1 and 3 were already complete. Throughout these six events the exact mask remained 223 (`11011111`, shown with bit 7 on the left): item 5 was still unfinished.

| Absolute event | Suffix event | Input | Correct answer | Model answer | Assigned probability of DONE |
|---|---:|---|---|---|---:|
| 16 | 8 | SET(0) | Item 5 | Item 5 | 25.2621% |
| 17 | 9 | SET(1), already complete | Item 5 | DONE | 47.8078% |
| 18 | 10 | NOOP | Item 5 | DONE | 93.5859% |
| 19 | 11 | NOOP | Item 5 | DONE | 95.2407% |
| 20 | 12 | SET(3), already complete | Item 5 | DONE | 95.5804% |
| 21 | 13 | SET(3), already complete | Item 5 | DONE | 98.2410% |
| 22 | 14 | SET(3), already complete | Item 5 | DONE | 99.4094% |
| 23 | 15 | SET(5), actual completion | DONE | DONE | 99.8736% |

These are softmax outputs, not validated probabilities of real-world correctness. No weight updates occurred during this rollout. The later correct DONE answer followed an actual completion event; it was not evidence that the model repaired its memory of an unfinished item.

### What the retained evidence rules out—and what it does not

The error occurred at absolute events **17–22**, within the 32-event training length. It cannot be dismissed as an error that appeared only after extrapolating beyond that length.

Retained-array inspection found **49,823 training-event exposures to mask 223** for parent 4103, including **1,389 idempotent SET(1) events with that same before/after mask**. Thus the exact symbolic state, and even the immediate symbolic transition at the first failure, were not wholly absent from training. These exposure counts are not independent examples of every relevant history and do not establish adequate learning of the required history-dependent representation.

The predeclared fitting diagnostic scored the final 4103 model on 160 actual training streams drawn from batches 1, 500, 1000, 1500 and 2000. It obtained **5,115/5,120 correct events and 159/160 wholly correct streams**, with zero false DONE. This sample shows some residual familiar-history fitting error; it is not the accuracy of the entire training corpus and does not establish one unique cause.

The supported localization is behavioral: maintaining the correct pending-item answer through idempotent operations failed under fixed parameters. Possible explanations include a weak history-dependent representation, training-objective limitations, optimization, or capacity. This run does not distinguish those explanations. Internal hidden coordinates need not remain constant during idempotent events; the required invariant is the task's meaning and correct answer, not numerical state equality.

**Failure evidence:** `failures/parent_4103_idempotent_first.npz` and its JSON receipt preserve the full original history, hidden trajectory, logits, targets, checkpoint hash and source-panel location. The CSV `analysis/failure_4103_events.csv` contains every event. Original batching is recorded for exact replay.

## 5. Instrumentation and numerical status

**All numerical admission checks passed.** The independently written NumPy float32 GRU reference was free-running over each complete prefix plus suffix, not repeatedly restarted from the canonical hidden trajectory. The envelope remained exactly `2e-6 + 2e-5 * abs(reference)`, with separate class-agreement checks.

Across parent A admission, **3,588,096 hidden/logit coordinates were compared, with zero out-of-envelope coordinates**. Maximum absolute discrepancy was 9.059906e-6; the maximum discrepancy normalized by its allowed envelope was 0.774906, below 1. The additional failed-parent training-history diagnostic also passed (maximum normalized discrepancy 0.862982). B checks passed as well. Larger absolute errors at large-magnitude coordinates are allowed by the predeclared relative term; no threshold was changed.

All eight deliberately injected faults were detected, and their eight corresponding clean controls passed: frozen-parameter mutation; copied-readout aliasing; wrong-task state receipt; truncated history; stale B targets; corrupt checkpoint bytes; a nonfinite tensor; and a wrong scorer label. These are bounded authored detector tests, not proof that all future defects will be caught. The independently implemented checklist oracles agreed over all 256 masks × 18 commands.

The three engineering probes each included an eight-update prefix, four uninterrupted further updates, and four repeated updates after checkpoint restoration in a fresh process. The resumed model, optimizer and Torch RNG values matched exactly in all three. The shared/copied B-graph fixture also produced identical gradients without additional optimizer applications.

A fresh process replayed **all four final-parent admission panels**, including the failure. All logits, full hidden trajectories and scored targets matched exactly. The independent checklist oracle matched all replayed histories. This is internal reproducibility, not third-party replication and not a rerun of all main training updates.

All **33 retained checkpoint files** passed model-tensor hash verification. Source and protocol hashes still matched their pre-main lock. Checkpoint byte hashes are in the final inventory. Original historical STATEBRIDGE numerical failures are unaffected by these new checks.

## 6. Work and resources

| Work item | Actual optimizer applications |
|---|---:|
| Four fixed parent fits | 8,000 |
| Engineering probes, including repeated resume work | 48 |
| Main B correction/adaptation | 0 |
| Post-stop fitting diagnostics and fresh inference replay | 0 |
| **Total actual** | **8,048** |
| Authorized maximum, not consumed | 10,096 |

The 48 engineering applications comprise 36 unique update positions plus 12 repeated resume applications. The engineering F/U probes did perform disposable B-style updates; **zero main B correction applications** does not mean no B-style engineering probe was executed.

Main parent fitting exposed 8,192,000 A event presentations plus 64,000 B cue presentations. The main process counted 8,310,336 canonical recurrent state-row evaluations, including fitting, admission and the fixed diagnosis; 54,304 reference state-row evaluations were separately counted. The fresh replay added 49,152 canonical and 49,152 reference state rows, with no backward pass. These counts are operation-accounting quantities, not independent observations or estimates of GPU FLOPs.

The measured executable main phase, including data generation, parent fitting, admission, diagnosis and its writes, took **83.317850 seconds**. Preflight took 7.738584 seconds; fresh replay took 0.345339 seconds. These are observed container timings, not forecasts or a measurement of assistant implementation/packaging time. Isolated main checker latency was not separately instrumented; combined phase timings and operation counts must not be represented as a complete component-level latency study.

Peak recorded process RSS was **367,435,776 bytes (350.414 MiB)**, below the 2 GiB process cap. A final parent's parameter tensors occupy **72,996 bytes** and its optimizer tensors **146,016 bytes**, including optimizer step counters. One 64-float task state uses 256 bytes; the readout tensors use 2,340 bytes. These small logical tensor counts are not total training memory. RSS includes framework/process allocations but is not simultaneous whole-system residency, user-device qualification or an energy measurement. Energy was not instrumented.

The preflight forecast budgeted 324,201,600 uncompressed evidence bytes, including a 32 MiB stop/failure reserve, against the 512 MiB delivery cap. Exact delivered sizes and hashes are in the accompanying delivery receipt. No unrelated archives were merged into this execution package.

## 7. Interpretation and next question

The fixed recipe learned the task to high measured accuracy, and three of four parents met all baseline requirements. It would be inaccurate to describe this as a broad failure to learn the checklist. It is equally inaccurate to promote the pooled accuracy into an admission pass: the declared false-completion reliability rule failed.

This result supports neither frozen nor adaptive recurrent weights for post-correction continuation because that comparison was not entered. It does not support any core count or successor architecture. Neither a state translator nor continuation rehearsal was tested. No architecture or learning-policy change is adopted.

The specific question earned by this stop is: **what keeps a pending item represented correctly while other items are resolved and later redundant events leave the task unchanged?** Any next protocol should distinguish that baseline semantic-stability problem from update-induced incompatibility. The exposed admission failure is now development evidence; it is not a reserved future confirmation case. New training, a replacement gate, or a follow-up diagnostic requires a new versioned dispatch rather than being silently appended here.

## 8. Review entry points

Start with this report, then `evidence/outcome.json` and `protocol/EXECUTION_LOCK.json`. The original proposal and completed execution specification are in `protocol/`. The frozen implementation is in `source/`. Main training inputs, labels, masks, RNG records and admission histories are in `fixtures/`; every parent checkpoint and all scheduled parent intermediates are in `checkpoints/`. The disposable probe artifacts are labeled separately.

`evidence/` contains numerical receipts, raw logits, retained hidden trajectories, B outputs, admission metrics, preflight and fresh replay. `failures/` contains the original failed admission record and reproducer. `analysis/` contains clearly labeled, zero-forward/zero-update retained-data analyses and independent array-rescoring/hash audits. `MANIFEST.json` and `MANIFEST.sha256` enumerate the delivered bytes. `CODEX_REVIEW.md` states the bounded review task and open question.

The PyTorch 2.10 GRUCell and numerical-accuracy documentation were consulted for implementation. They are not evidence that this study passed; the measurements and retained artifacts above are the evidence.
