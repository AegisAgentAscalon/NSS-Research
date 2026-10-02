# NSS CM-01 execution v0.2 — results

**Status: completed bounded, fixed-weight interface pilot.** No training, no optimizer updates, no changes to the fifteen Q010 main exports. This is the execution of **CM-01 from NSS_Context_Management_v0.1**, not the older differently numbered MicroContext draft and not the separate Q010-P1 768-case proposal.

## Executive finding

A grounded 56-byte reference workspace improved the primary near reader's held-out close-identity recall from **88/200 (44.0%) to 142/200 (71.0%)**, a **27.0 percentage-point** increase. Ordinary-known recall improved from **157/200 (78.5%) to 200/200 (100%)**. All five held-out families met the predeclared near-arm gain/control rule, versus the required four. The lowest family gain is exactly 4/40 = 10 percentage points, not a rounded sub-threshold result.

The main qualification is important: the improvement is concentrated in higher-noise queries. At sigma .01, near-arm close recall was 71/100 without the workspace and 70/100 with it. At sigma .2 it rose from 17/100 to 72/100. This supports **reference-assisted query reconstruction/denoising in this wrapper**, not a general solution to close-identity confusion.

The public exact-retrieval control returned the correct payload on **40/40 ordinary-known and 40/40 close-identity held-out records**. It outperformed the learned hybrid on close identities. Therefore the experiment does not establish that neural reading is necessary for exact stored-payload recall once a valid reference is available. Nor does it establish any advantage of token serialization: the structured and serialized interfaces agreed on all **7,680 main reader/case comparisons**.

## What “always resident” means here

The proposed architecture can maintain a fixed-size workspace available whenever a core performs a relevant operation. The controller reads and updates those symbols; the symbols are not autonomous processes. Residency, how frequently the model consults the workspace, and how frequently it rewrites it are separate choices. A resident workspace need not grow with history or be regenerated every recurrent step.

This pilot implements a limited version: a persistent reference packet populated from observable selection/correction events, retained across other events, and consulted at one learned read endpoint. A non-neural unit test confirms persistence through 32 unrelated registration events without rewriting the selected packet. **That is a software invariant, not a CM-02 continuity experiment or a learned recurrent-memory result.** No always-on learned internal token lane, model-managed storage writing, recurrent-state compression, long-horizon cognition, or 8/32/64 native-token budget was tested.

## Locked experiment and added information

The latest 512-record plan was used. The older planning handoff prohibited execution at the time it was written; the current user's explicit execution request authorizes this first bounded pilot. Conditional CM-02 through CM-05 and Q010-P1 were not automatically launched.

Eight fresh episode families were frozen: three development, five held out, with eight strata and eight labeled records per stratum. Each case uses a new path-length-one source graph with sixteen 17-dimensional catalogue codes and one learned reader stage. These families group disjoint episode/catalogue recipes; this is not one continuously evolving catalogue over 64 events. The five fixed model seeds are repeated evaluations, not independent new data families.

The source generator is the retained Q010 make_case implementation. The execution contract separately fixes public event semantics, revisions/deletions, corrections/conflicts, noise balancing, scope handling, and fault injection. Exact source reconstruction in the scorer reproduces keys, values, masks, catalogue, query and the source truth from saved seeds, without importing producer code. These execution completions are declared in protocol/PROTOCOL.json; they are not retroactive changes to Q010's 64-condition evaluation.

A streaming deterministic manager sees an observable registration/selection journal, current scope/task and retained workspace. Handles are allocated from a separate random stream, not derived from answer IDs. Its query output is only an original query, a canonical query previously observed in that journal, or explicit management abstention. It cannot open the protected truth ledger. The original learned rule, K/V/valid arrays and original catalogue-assisted output resolver remain unchanged.

The three interfaces are A: original numerical query; B: structured workspace; C: exactly the same fields serialized as UTF8_BYTE_V1. The string is **56 ASCII bytes/control symbols**, not 56 language-model tokens. Its fields are version, scope, handle, revision, binding-event reference and operation. At most two indexed lookups are made per management request. Missing/unresolved references fall back to the original query; observably invalid references cause management abstention; valid references can substitute a canonical query. The manager never substitutes an expected answer into the learned read.

A separate public exact-lookup control reads the observed payload under the same valid binding and otherwise returns UNKNOWN. It has no fuzzy fallback. A privileged exact-owner control uses the isolated source/ownership ledger to select the actual readable row; it is never pooled with nonprivileged outcomes.

## Held-out task results

Each learned-reader cell below contains **40 held-out episode records × five fixed model seeds = 200 reader/case evaluations**. B and C are identical. Percentages are exploratory descriptive outcomes, not calibrated probabilities or general NSS qualification.

| Role | Task stratum | A: original query | B/C: reference workspace | Change |
| --- | --- | ---: | ---: | ---: |
| near | Ordinary known | 157/200 (78.5%) | 200/200 (100.0%) | +21.5 pp |
| near | Close identity | 88/200 (44.0%) | 142/200 (71.0%) | +27.0 pp |
| ordinary | Ordinary known | 113/200 (56.5%) | 200/200 (100.0%) | +43.5 pp |
| ordinary | Close identity | 73/200 (36.5%) | 129/200 (64.5%) | +28.0 pp |
| attention | Ordinary known | 114/200 (57.0%) | 200/200 (100.0%) | +43.0 pp |
| attention | Close identity | 62/200 (31.0%) | 108/200 (54.0%) | +23.0 pp |

### Primary near arm: every held-out family

Each close-identity percentage is over eight records evaluated with five fixed seeds, not forty independent episodes.

| Family | Original close recall | Workspace close recall | Change | Workspace ordinary-known recall |
| --- | ---: | ---: | ---: | ---: |
| CMEVAL-01 | 32.5% | 55.0% | +22.5 pp | 100.0% |
| CMEVAL-02 | 40.0% | 70.0% | +30.0 pp | 100.0% |
| CMEVAL-03 | 37.5% | 82.5% | +45.0 pp | 100.0% |
| CMEVAL-04 | 55.0% | 82.5% | +27.5 pp | 100.0% |
| CMEVAL-05 | 55.0% | 65.0% | +10.0 pp | 100.0% |

The ordinary arm failed its exploratory gain rule in one family (CMEVAL-05: 47.5% to 45.0%, -2.5 points). The attention comparison met the gain/control rule in all five families but had lower pooled close recall. The primary arm was not switched after results. No gate, threshold, decoder or held-out selection was fitted.

### Noise-matched breakdown for the primary near arm

| Stratum | Query sigma | A | B/C |
| --- | ---: | ---: | ---: |
| bound_known | 0.01 | 100/100 (100.0%) | 100/100 (100.0%) |
| bound_known | 0.2 | 57/100 (57.0%) | 100/100 (100.0%) |
| bound_close | 0.01 | 71/100 (71.0%) | 70/100 (70.0%) |
| bound_close | 0.2 | 17/100 (17.0%) | 72/100 (72.0%) |
| unbound_known | 0.01 | 100/100 (100.0%) | 100/100 (100.0%) |
| unbound_known | 0.2 | 66/100 (66.0%) | 66/100 (66.0%) |
| unbound_absent | 0.01 | 0/100 (0.0%) | 0/100 (0.0%) |
| unbound_absent | 0.2 | 34/100 (34.0%) | 34/100 (34.0%) |

These strata contain different randomly drawn episodes at each noise scale, as frozen before execution. The within-case A/B comparison is paired. The pronounced high-noise gain is consistent with canonical-query reconstruction; the low-noise close-identity result does not support a blanket improvement.

## Negative cases and information limits

All negative outcomes remain in the evidence package. The table separates content correctness from management action. A safe refusal on a known record is still a recall failure.

| Primary near arm, held out | Task correct | Management abstentions | Accepted wrong bindings |
| --- | ---: | ---: | ---: |
| stale_revision: revision | 0/100 | 100 | 0 |
| stale_revision: deletion | 100/100 | 100 | 0 |
| cross_scope: foreign_scope_checkpoint | 0/200 | 200 | 0 |
| wrong_reference: detectable | 0/100 | 100 | 0 |
| wrong_reference: no_cue | 33/100 | 0 | 100 |
| correction_conflict: correction | 100/100 | 0 | 0 |
| correction_conflict: unresolved_conflict | 74/100 | 0 | 0 |

On observably invalid bindings, B/C abstained in all **500 held-out primary reader/case evaluations** (100 unique records × five seeds). Four hundred of those evaluations still required a known answer and therefore remain task-recall losses. The remaining one hundred correspond to deleted records and correctly returned UNKNOWN. The false-reference-acceptance rule passes without pretending that these refusals constitute successful recall.

The no-cue stratum contains a public binding consistent with the journal but inconsistent with the hidden intended identity. All **100 held-out primary evaluations** accepted that wrong binding. The learned reader nevertheless returned the expected content in 33/100; these incidental content successes do not validate the binding. The public exact lookup faithfully followed the wrong reference and was wrong on all 20 unique held-out no-cue records.

There are **64 main opposite-truth pairs** whose complete public history, workspace and numerical input are byte-identical. At sigma .01, the near reader answered all known cases correctly and classified none of their matched absent counterparts UNKNOWN. At sigma .2 it achieved 66/100 known correctness and 34/100 absent correctness. Pairing yields 50% balanced accuracy in both noise strata: deterministic processing cannot recover an origin distinction absent from the supplied information. No gate was optimized for these pairs. Thirty-two additional no-cue counterfactual descriptions reuse existing evidence and invoke no models.

The public exact control's 100% absent accuracy on unbound cases comes from returning UNKNOWN whenever it lacks a usable reference; its known accuracy on the same unbound interface is 0%. This is not identity recognition.

## Verification and measured work

The original planning archive passed its ten-file integrity check; the recovery context passed verification of 5,449 manifest-listed files. Its archive SHA-256 remains `9ac2801dc9a67ce3d7fbea5d4f79281b66176e961488fbffb6bf9c660056279e`.

Before any generated fixture or main cases, the execution source/configuration and **2,284 seed allocations** were frozen. The collision audit scanned 5,091 retained source/record files (298,234,599 bytes), including reserved proposals. No collisions were found. This audit cannot inspect missing historical RNG histories or all unmaterialized historical random draws; it does not claim to do so.

Thirteen non-neural contract test methods passed, including malformed/reserved encodings, exact serialization, query provenance, scope, stale/deleted records, conflicts, and persistence without rewrite. The eight-case numerical fixture passed independent scoring and fresh-process replay before main generation.

| Work item | Actual |
| --- | ---: |
| Main labeled records | 512 |
| Main distinct public inputs | 448 (64 deliberate opposite-label duplicates) |
| Main model exports evaluated | 15 |
| Main learned interface decision rows | 23,040 |
| Main non-neural control rows | 1,024 |
| Main producer model calls | 10,560 |
| Fixture producer model calls | 33 |
| Total model calls, including both exact replays | 21,186 / 30,816 cap |
| Physical model-forward batches, including replay | 492 |
| Exact replay array comparisons | 2,228 |
| Exact replay numeric elements | 1,570,385 |
| Incorrect main learned-interface rows retained | 10,571 |
| Incorrect fixture learned-interface rows retained | 33 |
| Incorrect non-neural control rows retained, main + fixture | 256 + 4 |
| New optimizer updates | 0 |

The separate scorer imports no producer/model/generator/manager modules. It reconstructs source inputs and live truth, independently replays management actions, checks the original pointer arithmetic with the pinned verifier, and decodes outputs independently. Fresh-process replay regenerates sources and model outputs; arrays, events, routing and metadata match exactly. Timing and Python allocator-dependent object-size observations are excluded from byte-equality requirements and explicitly retained as separate measurements. Replay is not new scientific sample size. This is internal implementation independence, not third-party replication or cross-device validation.

Producer processes have a guard against opening the protected truth ledger. Public-only envelope checks with changed hidden labels were performed on all 512 main and eight fixture records in both producer/replay executions. These are concrete isolation checks, not a formal information-flow proof.

The underflow amendment was not modified. The retained v1.6 fresh-main underflow fixture still fails the frozen verifier and passes the preserved amended verifier, whose final-probability bound adds 2^-126. The lost original v2 source and historical rejected raw row are still missing and are not claimed recovered.

### Resource accounting

Supervised stages through main replay/comparison took **55.64 seconds of measured stage wall time**, including seed scanning/imports. The conservative shared clock at that endpoint was **780.92 seconds**, including preparation between commands. The clock begins 150 seconds before the first recorded preflight receipt to account for the initial inspection. Both figures are below the two-hour study cap; they are not deployment-latency benchmarks.

Peak sampled supervisor-plus-worker process-tree RSS during these instrumented stages was **627,650,560 bytes** (598.6 MiB), below 4 GiB. Sampling was every 0.1 seconds; very brief peaks can be missed. The initial extraction/integrity commands preceded this instrumentation, so no continuously measured peak for that short prelude is claimed.

Each packet is 56 encoded bytes (26 bytes for a hypothetical packed representation of its semantic fields). Each case's public K/V/valid arrays occupy 2,192 bytes; the output resolver's catalogue/symbol arrays occupy another 1,232 bytes; each query is 68 bytes. The public journal's canonical JSON is 12,897–14,111 bytes per case, while the materialized directory is 13,374–14,367 bytes. The binding index is additional. Python object inventories, lookup bytes, event counts and rewrite counts are retained in `raw/main/capture_run/capture/costs.jsonl`; summing separate Python object inventories can double-count shared immutable objects and is not an exact allocation measurement.

Across the 512 main records, the controller processed 8,832 public events and logged 448 selection/correction/conflict workspace changes. The B interface used 544 total indexed lookups (0–2 per record), returning 246,683 serialized bytes. C uses the same retained information and is an encoding control. Archive/index construction, public control lookup and verification also cost work. A tiny control string is **not** the whole system memory budget, and no net memory-saving claim is made.

## Interpretation and next boundary

The adopted role change is compatible with this result: a compact context channel can preserve information needed to select a reliable recall operation. The clearest measured contribution here is grounded reference management and reconstruction of a less noisy query. When a valid exact reference already exists, the public archive control provides a stronger payload-recall route than these small learned readers. A future system could reserve learned processing for reference acquisition, ambiguous selection, integration and task-state evolution, while using exact lookup for exact references. That is an engineering interpretation, not a newly tested integrated architecture.

The right next conditional experiment is CM-02: compare continuity after delays, switches and corrections, including a workspace-plus-archive arm with task/recurrent state disabled. This would distinguish useful workspace/archive continuity from a necessary recurrent contribution. CM-03 can then compare residency/read frequency against refresh frequency. CM-05 remains the native learned-token/recurrent experiment and needs its own small-model training specification. None was run here; the fifteen saved Q010 exports remain frozen.

## Evidence and historical limitations

The package includes the complete new bounded study's public inputs, isolated truth ledger, model-output arrays, workspace transitions, lookup receipts, public controls, negative decisions, source and locks, fixture/main replay outputs, numeric verifier provenance and audit receipts. It does not duplicate the old model archive. The separately retained 48.7 MB recovery context remains the model/source dependency.

Historical Q010 limitations remain: full main optimizer/RNG checkpoints and raw main numeric training traces are absent; the compact recovery omits the bulk original main capture/replay; three old verifier errors remain historical failures; original training qualification is false. This study does not fill those gaps and does not change old Q010 thresholds or results.

**Bottom line:** CM-01 produced a positive, noise-dependent reference-management result with reproducible limits. It did not demonstrate autonomous always-on tokens, native recurrent-state control, learned workspace generation, or state compression.

## Delivery QA

After numerical completion, the complete study was copied to a different directory and its independent main scorer was run again, with no additional model inference. All eight main result files were byte-identical to the original outputs. This added 10,560 arithmetic-audit rows, not new model calls or scientific samples. The QA stage took 6.96 seconds; the conservative shared clock was 1,247.85 seconds at its completion, still within two hours. The post-execution report/packaging code does not alter the locked study source, labels or thresholds. The optional future REPLAY_STUDY.py driver was syntax/CLI checked, not executed for a third full model run.
