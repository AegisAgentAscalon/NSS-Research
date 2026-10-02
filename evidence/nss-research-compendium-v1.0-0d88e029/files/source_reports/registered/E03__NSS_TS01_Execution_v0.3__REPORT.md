# NSS TS01 — learned task-progress state
## Completed execution v0.3 / approved scientific protocol v0.2

**Result: the predeclared bounded feasibility screen passed.** All five newly trained models attained **120/120 held-out joint successes** with carried state. The state-erasure control attained **40/120 per model**. Exact programmed streaming and prefix replay were also perfect on their respective held-out observations. The maintained management-token workspace was **not** an arm of this experiment; it is explicitly carried forward in `MAINTAINED_MANAGEMENT_TOKENS.md` and `CHAT_PROMPT.md`.

Unlike CM-01/CM-02, TS01 tests a real learned recurrent transition. It is nevertheless an intentionally tiny, supervised finite-state task, not a compression result, a general reasoning benchmark, or integrated NSS qualification. All fifteen historical Q010 exports remained unchanged and received **zero loads, zero forwards and zero optimizer updates** in TS01.

## 1. What the task required

Each of two tasks has four independent completion flags. The public event stream can complete a flag, revoke it, reset one task, activate a task for querying, or explicitly distract. A query asks for the active task's four flags plus its first incomplete milestone, or DONE. The answers are derived from the chronological updates; there is no prewritten answer payload to retrieve.

The learned transition is a shared float32 GRUCell(9,64) and Linear(64,9) head: **14,985 trainable parameters / 59,940 parameter bytes**, with two 64-float task banks, **512 bytes of recurrent state**. All six parameter tensors were initialized from the prescribed independent generators. The public RESET event enters the learned GRU; the carried bank is not externally cleared to make the target easy.

Important supplied capabilities remain explicit: ordinary code maps task IDs to banks, chooses the addressed bank, preserves the other bank, and filters labeled distractors/no-ops. Queries do not update state. Thus TS01 tests learned checklist updates and decoding **inside supplied task routing**, not learned attention to relevance or autonomous storage management.

## 2. Actual data and training

Five separate fits each completed 2,000 Adam updates with batch size 16: **10,000 optimizer and backward updates; 160,000 training episodes; 4,000,000 training events**. Episode lengths alternate between 17 and 33 events; full backpropagation covers each episode. Both banks' four bit logits and next-action head are supervised after every event. Gold states never enter the learned transition as inputs.

Only the terminal step-2000 checkpoint of each fit was admitted to scientific evaluation. All five terminal hashes were frozen before any concrete main development/held-out streams were generated. No development tuning, model selection, retries, extra fit, parameter sweep or changed criterion occurred.

| New fit | Mean first 100 batch losses | Mean last 100 batch losses | Parameters changed from initialization |
|---|---:|---:|---:|
| 01 | 1.992898 | 0.063673 | 14,985 / 14,985 |
| 02 | 1.966765 | 0.064830 | 14,985 / 14,985 |
| 03 | 2.037984 | 0.065917 | 14,985 / 14,985 |
| 04 | 2.053146 | 0.070999 | 14,985 / 14,985 |
| 05 | 2.022202 | 0.065960 | 14,985 / 14,985 |

These losses come from different batches under the fixed recipe; they are descriptive training curves, not fixed-corpus before/after evaluations.

Main evaluation contains **32 sequences** in three development and five held-out families: four templates per family, 65 events each after a charged registration/activation prelude. Queries follow events 0, 8, 16, 32, 48 and 64. This yields **192 main query occasions / 120 held out**. Five trained models repeat those same occasions; they do not create 600 independent episodes. The held-out units are five procedurally generated families containing 20 sequences.

The separate fixture used four sequences and one untrained initialized model. Its expected poor task accuracy was not a scientific failure: its job was validating interfaces, exact labels, numerical calculations, logging and fresh replay before training.

## 3. Primary results

Joint success requires both the entire four-bit checklist and the independent next-action head to be correct. The next head was not repaired from predicted bits.

| Held-out arm | Correct joint answers | Accuracy |
|---|---:|---:|
| CARRY: maintain learned state | **600/600** | **100%** |
| ZERO_EVERY_EVENT: clear both banks before every event | **200/600** | **33.33%** |
| PREFIX_REPLAY: rebuild the learned state from the observed prefix at every query | **600/600** | **100%** |
| EXACT_STREAM: ordinary packed progress tracker | **120/120** | **100%** |

EXACT_STREAM runs once per unique occasion, not five identical times. The state-removal arm is an information ablation, not an equal-resource efficiency competitor. Its performance reduction supports useful dependence on retained state, not superiority over another equally informed system.

### Every trained fit

| Fit | CARRY | ZERO_EVERY_EVENT | PREFIX_REPLAY |
|---|---:|---:|---:|
| 01 | 120/120 | 40/120 | 120/120 |
| 02 | 120/120 | 40/120 | 120/120 |
| 03 | 120/120 | 40/120 | 120/120 |
| 04 | 120/120 | 40/120 | 120/120 |
| 05 | 120/120 | 40/120 | 120/120 |

The proposal required at least 114/120 joint successes in at least four fits. **All five passed with 120/120.** CARRY and PREFIX_REPLAY also answered all **960 main** readouts correctly, including development; EXACT_STREAM was correct on all 192 main occasions.

### Every held-out family

| Family | CARRY | ZERO_EVERY_EVENT | Paired difference |
|---|---:|---:|---:|
| TS01EVAL-01 | 120/120 | 45/120 | 62.50 pp |
| TS01EVAL-02 | 120/120 | 50/120 | 58.33 pp |
| TS01EVAL-03 | 120/120 | 45/120 | 62.50 pp |
| TS01EVAL-04 | 120/120 | 30/120 | 75.00 pp |
| TS01EVAL-05 | 120/120 | 30/120 | 75.00 pp |

Each family row contains 24 query occasions repeated over five fits. All five family differences are strictly positive, as required.

## 4. Corrections, reset and negative evidence

At the forced V:16, V:32 and V:48 revocation checkpoints, CARRY made **0 wrong-DONE assertions in 75 held-out assessments**. The definition counts either an incorrect DONE next-action or an incorrect all-complete bit vector. There was no validator or refusal mechanism hiding an error.

The auxiliary held-out diagnostic inspected both banks after every event: **13,000 bank/event observations for CARRY**, all with correct bits and next action. Its missed-revocation, reset-carryover, inconsistent-head, wrong-DONE and stale-inactive-output counts were zero. These auxiliary states are strongly related observations, not 13,000 independent tests. Unaddressed-bank preservation itself is a supplied software invariant, not learned competence.

All **655 incorrect main query rows** remain in the package; they belong to ZERO_EVERY_EVENT (400 held out, 255 development). Its held-out next-action accuracy alone was 60%, bit-level accuracy 62.92%, and joint accuracy 33.33%—the easier partial metrics do not replace joint correctness. The untrained fixture retains **63 incorrect learned-interface rows** (21 per arm). Exact controls have no task errors. Full auxiliary errors and all correct rows remain available, including state-removal inactive-bank errors; replay and representation duplicates are not new samples.

Passing this narrow safety check does not establish general safe completion behavior beyond the sampled templates, event types and horizons.

## 5. What recurrence bought, and what it did not

Within one model's 32-sequence main evaluation, CARRY used **1,612 actual GRU transition examples**. PREFIX_REPLAY used **4,303**, with bit-identical endpoint states and logits. Thus replay required about **2.67 times as many recurrent transitions** under the six-query schedule. Both arms also pay for their retained event archive; replay scans observed prefixes rather than using a hidden state cache.

This is a computation-versus-retained-state comparison against this specified replay schedule, **not a wall-clock speedup claim or a victory over ordinary code**. CARRY/ZERO additionally read both heads after every event for auxiliary verification, whereas PREFIX_REPLAY reads both heads at query endpoints. Those extra diagnostic heads and all trace storage are charged, not disguised as deployed memory savings.

The exact programmed tracker maintains the same progress in **eight bits / one packed byte**, plus task IDs, active-task metadata, archive and software-object costs. The learned state alone is 512 bytes, plus 59,940 weight bytes. A native Python integer has object overhead; the one-byte figure is the exact sufficient progress representation, not a one-byte Python process. Consequently TS01 does **not** demonstrate storage compression or total efficiency over EXACT_STREAM.

Per-query component object inventories and logical wire/storage counts are retained, as are exact-control update timings and whole-stage time/resource samples. They are not complete native allocator traces or optimized deployment benchmarks. Native operator buffers and execution-frame overhead are only reflected in process RSS. The comparison does not claim an overall efficiency PASS. Any archive-free subtotal is explicitly hypothetical and removes the unnecessary archive symmetrically from CARRY and EXACT_STREAM, never from replay.

## 6. Data identity and duplicate audit

The 164 direct seed allocations and **160,000 derived episode seeds** passed the prescribed within-study collision checks. The prior direct-seed audit remains scoped to its available historical text; missing historical RNG draws are not retrospectively audited.

All 160,000 training wire episodes are unique when their full public identifiers/payloads are included. Removing IDs and ignored distractor payloads leaves **159,988 distinct normalized streams: 12 duplicate excess episodes**, all retained. All 36 main-plus-fixture normalized streams are distinct. None of their 17/33-event normalized prefixes matches a complete retained training stream. These checks do not imply broad distributional independence: the training and test templates are closely related, and testing 65 events after training on 17/33 is a bounded length check, not arbitrary-horizon generalization.

An independent audit regenerated **every training episode** from the frozen PCG64/digest recipe, reconstructed all **4,000,000 prefix targets**, verified every batch input hash, and checked checkpoint state against the recorded parameter hashes. It did not rerun optimization.

## 7. Numerical and replay verification

The independent NumPy scorer imports no producer, generator, model or controller logic. It reconstructs truth with Boolean lists, checks the separate packed-state exact control, independently decodes the saved logits, and reconstructs each saved one-step GRU/head operation in float64.

The unchanged engineering tolerance is `abs(observed-reference) <= 2e-6 + 2e-5*abs(reference)`. This is an empirical acceptance tolerance, not a proved rounding-error bound. In the main capture it checked **6,617,600 scalar comparisons**; the maximum tolerance ratio was **0.166669**, with no near-zero bit logits or near-tied next-action winners under the declared proximity checks. Same-runtime exact replay is a distinct stronger equality check on the actual float32 implementation.

Main fresh-process replay matched **2,144 arrays / 12,888,000 numerical elements** and all **11 independently scored files**. The untrained fixture independently matched **60 arrays / 322,616 elements** and its 11 score files. Recorded deterministic costs, episode/query metadata and inference receipts also match. Measured timings are not required to be equal.

The streaming worker receives only the next committed public event and its own context. It is denied file access to labels, protocol/seed records, training data and future public-input files. Hidden-label/future-suffix projection tests and exact prefix replay check causality; these are concrete engineering checks, not a formal information-flow proof. Internal independently implemented scoring and fresh replay are not third-party replication or cross-device validation.

## 8. Complete new training history and work ledger

Each fit retains full model/Adam/RNG/data-cursor checkpoints at updates **0,250,...,2000**: **45 complete checkpoints total**. They include Python, NumPy and Torch runtime RNG states, the dedicated initialization generator, and all sixteen most-recent independent episode-generator states. Every event, seed, batch loss, finite gradient norm, attempted/completed update, input hash and post-update parameter hash is retained. Checkpoint 2000 matches its final exported weights.

This is intentionally better retained history for the **new** fits. It is not a claim that the five training runs have been independently reproduced. Training activation/autograd graphs are not retained; evaluation before/after states and logits are complete.

| Charged work | Actual or conservative reservation | Hard cap |
|---|---:|---:|
| Cell-example reservations | **4,099,712** | 4,200,000 |
| Cell examples actually dispatched | **4,077,168** | Included above |
| Head-vector evaluations/reservations | **8,089,216** | 8,200,000 |
| Backward attempts/completions | **10,000** | 10,000 |
| Optimizer attempts/completions | **10,000** | 10,000 |

Training computes and charges masked no-op cell examples; evaluation skips no-op cells while reserving their conservative ceiling. Independent NumPy audits, data regeneration and exact-control operations are additional measured work within the same clock, not neural sample counts.

All 17 supervised stages completed on their first attempt. There were no failed fits, reruns or in-flight unacknowledged model calls. Ten non-neural contract methods passed before the numerical fixture. The shared clock through main scoring/replay/comparison was **1083.51 seconds**, including post-authorization implementation and preparation, below two hours. The sampled process-tree peak was **611,901,440 bytes**, and the sampled container peak **1,453,477,888 bytes**, below the 3 GiB and 3.5 GiB limits. Sampling was every 0.1 seconds; brief peaks and the initial uninstrumented preflight are not claimed fully covered. Delivery QA is separately receipted against the same starting clock.

## 9. Required next-step context for Codex

The user's maintained management-token concept remains central: a **bounded resident workspace that supports information management**, alongside recurrent task state and exact evidence storage. It may keep goals, constraints, task/scope identity, references, revisions and unresolved questions explicit without turning the entire task history into an expanding transcript. Residency, reading and rewriting are separate decisions.

TS01 supplies a successful small recurrent-state baseline for a later matched intervention. **It did not test the maintained workspace.** One-hot event inputs are not an always-resident organizer, and supplied task-bank routing is not learned token-based management.

A follow-up must specify how workspace contents arise from legitimate observations, how they condition recurrent updates, when they change, and how their costs are charged. Retain recurrent-only, extra-capacity, same-information structured, workspace-only/state-removal, exact-stream and replay controls as appropriate. Selective updates, stable/scratch entries, invalidating stale derived conclusions and reducing learned-state capacity remain hypotheses. Do not feed a gold progress ledger into the workspace and call it learned management. Do not automatically launch that follow-up or train a larger model.

## 10. Historical boundaries and delivery

All historical Q010 export hashes were checked before and after this work without loading their models. CM-02's closed **5,995-attempt** ledger and its interrupted attempts remain historical, not part of the new TS01 budget. Historical missing full Q010 optimizer/RNG/training traces, compact-archive omissions, old verifier failures and missing original underflow evidence remain unchanged.

Q010's reconstructed final-softmax underflow amendment **+2^-126** is neither altered nor applied to the new GRU checker. No original training history is fabricated. The NSS Primary/Secondary/Tertiary/Validator roles remain architectural background; no core replacement or Forge/Runtime integration occurred.

The study package contains the complete **new** evidence and source. Old archives/models are not duplicated and are not numerical dependencies of TS01 re-scoring. Lossless delivery deduplication may share byte-identical files and reconstruct redundant hash-count tables from retained per-episode identity rows; every restored byte is checked against its original manifest hash. This is packaging, not new evidence generation. Follow README/RESTORE_EVIDENCE/VERIFY_STUDY instructions after extraction.

### Delivery-only correction

The first candidate ZIP passed its listed-file hashes but relocation scoring detected that its packaging filter had omitted the two nested raw-input manifest files. The original study source, arrays, checkpoints and scores were intact. The packager was corrected to retain nested manifests, and the delivery verifier was strengthened to check required episode inputs in addition to hashes. The failed packaging receipt/log is retained in `audit/`. No neural calls, optimizer updates, case changes, or scientific score changes resulted. The final archive's fresh-extraction/restoration/rescoring result is recorded in the separately linked delivery receipt; the first candidate is not the delivered study.
