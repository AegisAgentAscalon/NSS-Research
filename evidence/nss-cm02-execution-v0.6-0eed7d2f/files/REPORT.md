# NSS CM-02 — reference continuity and freshness
## Completed study, execution v0.6 / reviewed scientific protocol v0.2

**Bottom line:** the small reference workspace maintained its specified bindings through the tested chronological changes, but an ordinary index did exactly the same job. Both improved held-out learned-read accuracy over discarding selection history. Ordinary exact retrieval was stronger still, and following an observed revision recovered current answers that the deliberately conservative pinned-reference policy refused.

This is a completed **deterministic information-management study**, not a demonstration of native recurrent memory, learned token interpretation, compression, or integrated NSS cores. All fifteen Q010 exports are unchanged; the five near readers participated, with **zero training and zero optimizer updates**.

## 1. What actually ran

The approved design used 32 chronological sequences: three development and five held-out families, four sequence templates per family. Every sequence had a new sixteen-record catalogue, two task contexts, a public prelude of sixteen registrations and one activation, then events 0–64. Queries followed events 0, 8, 16, 32, 48 and 64.

That gives **192 main query occasions**, including **120 held out**. Five frozen near-reader seeds (1201–1205) repeat measurements of each occasion; they do not create more independent episodes. These are tiny numerical readers (818 parameters / 3,272 tensor bytes each), not general language models. Their numerical interface and original catalogue-assisted decoder remain unchanged.

- **W, workspace:** two 56-byte ASCII reference strings, one per task; no hidden shadow selection table. The symbols use UTF8_BYTE_V1, not a language-model tokenizer.
- **I, conventional index:** a two-entry task dictionary holding the same six semantic fields as immutable tuples.
- **O, no retained selection:** original numerical query and current store; it deliberately discards the selection history. This is an information ablation, not an equal-information competitor.

W and I share the same revision-pinned validation rules. They observe each committed event; task switching preserves both entries; explicit selections/corrections update the addressed entry; conflicts mark it unresolved. Record revisions/deletion update the archive but do not silently refresh a selected entry. Queries do not rewrite state.

The two packet strings occupy 112 encoded bytes, but the journal, record store, historical bindings, task metadata, physical-row index, numerical arrays, reader and transient parsing all still count. There is no native persistent learned hidden state to disable in these readers.

## 2. Primary held-out results

| Interface | Correct readouts | Accuracy |
|---|---:|---:|
| O: no retained selection | 307 / 600 | 51.17% |
| W: compact workspace | 391 / 600 | 65.17% |
| I: ordinary maintained index | 391 / 600 | 65.17% |

**W–O = +14 percentage points; W–I = exactly zero.** Each denominator is 120 held-out query occasions × five saved readers, spread across 20 sequences and five families. The family, not each model/checkpoint observation, is the held-out grouping unit. No IID confidence interval over these repeated observations is claimed.

W and I matched on all **192 main routes**, current-context choices and all **960 paired model/query decisions**. The independently reconstructed pinned-prefix scan also matched at every query. There were zero observable invalid-reference acceptances and all 192 chronological whole-map checks passed.

| Held-out family | W / I accuracy | O accuracy | W–O difference |
|---|---:|---:|---:|
| CM02EVAL-01 | 58.33% | 45.83% | +12.50 pp |
| CM02EVAL-02 | 64.17% | 63.33% | +0.83 pp |
| CM02EVAL-03 | 73.33% | 48.33% | +25.00 pp |
| CM02EVAL-04 | 63.33% | 48.33% | +15.00 pp |
| CM02EVAL-05 | 66.67% | 50.00% | +16.67 pp |

The direction is positive in all five families, but CM-02 had no new recall-gain threshold. These are descriptive results, not a newly fitted gate or general NSS qualification.

### Noise and event conditions matter

| Incoming query noise | O | W / I | Difference |
|---|---:|---:|---:|
| sigma 0.01 | 222/300 = 74.00% | 202/300 = 67.33% | −6.67 pp |
| sigma 0.2 | 85/300 = 28.33% | 189/300 = 63.00% | +34.67 pp |

Thus the positive pooled result is **not** a blanket benefit. The small-noise pool is worse with the pinned manager; the high-noise pool improves substantially. Event/policy conditions are mixed within these pools, so this is not a clean factorial causal estimate of noise alone. Per-template/checkpoint/noise/seed tables preserve the breakdown.

For unchanged-target delay/switch sequences, W/I achieved 104/150 (69.33%) versus O's 78/150 (52%). The correct task reference survived, but learned reading remained imperfect. At D:64, W/I still recalled only 14/25 answers; exact retrieval got all five unique endpoint answers. **Reference continuity is not proof of flawless neural recall.**

## 3. Exact retrieval and the freshness-policy result

Four non-neural controls use the same public observations:

| Exact retrieval policy | Held-out correct occasions |
|---|---:|
| X_W: validated pinned workspace | 100/120 = 83.33% |
| X_I: validated pinned ordinary index | 100/120 = 83.33% |
| X_S: reconstruct observed prefix, same pinned policy | 100/120 = 83.33% |
| X_latest: follow a valid observed revision chain | 105/120 = 87.50% |

These controls run once per occasion, not five times per reader. Their numerical percentages can be compared descriptively on the shared occasions, but their denominators must not be inflated by repeating deterministic decisions.

At **F:16**, the selected entity had an observed newer revision and a current answer still existed. W/I intentionally treated the old revision-pinned reference as stale and abstained: **0/25 learned readouts**, or five unique known-answer occasions lost. X_W/I/S likewise returned UNKNOWN on 0/5 current answers. **X_latest retrieved all 5/5 current answers** by following the public revision chain. O happened to recover 16/25 through its unchanged noisy numerical query.

At **F:48**, the target had actually been deleted. W/I correctly returned UNKNOWN on **25/25** readouts, versus O's **2/25**. All exact controls returned UNKNOWN on **5/5** unique deleted-target occasions.

This is not evidence that X_latest is a smarter neural reader. It is a different, explicitly declared retrieval contract: *the continuing entity's current content* rather than *only the originally selected revision*. It retains and pays for an additional revision index. W/I were not silently upgraded to this policy after seeing results.

## 4. Failures and information limits remain visible

Every incorrect outcome is retained, including expected conservative refusals and no-cue failures.

| Selected held-out situation | W / I content correct | Management interpretation |
|---|---:|---|
| Revised known record, F:16 | 0/25 | Correctly detects stale reference; loses known current answer |
| Deleted record, F:48 | 25/25 | Correct UNKNOWN |
| Unresolved conflict, C:32 | 12/25 | Does not invent a selection; falls back to original query |
| Publicly consistent wrong intent, N:16 and N:32 | 10/50 | Accepts wrong intended binding in all 50 readouts |

The no-cue group has ten unique held-out occasions. The wrong reference is consistent with the observed journal, so rejecting it as observably invalid would require information the manager did not receive. Exact retrieval faithfully followed it and was wrong on all **10/10** main-intent occasions. The learned reader's incidental 10/50 content successes do not validate that binding.

Alternate hidden-intent labels on identical inputs were scored without new forwards. Across the held-out paired labels, W/I achieved 40% balanced correctness, O 39%, and exact controls 50%. A deterministic answer cannot satisfy both distinct correct labels; it may satisfy neither. Do not round the learned result to 50% or claim origin recognition.

Completed main evidence contains **1,165 incorrect learned-interface rows** and **120 incorrect exact-control rows**. The completed fixture adds **14** and **15**, respectively. Representation duplicates, repeated reader seeds, counterfactual labels and replay are not independent new scientific samples. Partial attempts are preserved separately and are not silently pooled into these completed-run denominators.

## 5. Costs: a very small representation trade-off, not compression

Whole unique Python object graphs were counted once per arm, including controller state, query and one reader. Shared objects/tensor storage are not summed repeatedly. These are object-inventory measurements, not OS allocation traces or a claim about optimized deployment memory.

At the held-out query checkpoints, for the seed-1201 representative model:

| Metric | W | I |
|---|---:|---:|
| Mean resident object-graph observation | 117,407.72 bytes | 117,440.47 bytes |
| Maximum resident object-graph observation | 183,508 bytes | 183,532 bytes |
| Maximum route-time transient controller graph | 169,155 bytes | 168,945 bytes |
| Semantic task fields rewritten per family | 884 bytes | 884 bytes |
| Selection-object shell bytes reallocated per family | 3,298 bytes | 2,992 bytes |
| Packet encodes / decodes per family | 34 / 50 | 0 / 0 |
| Event-plus-query indexed reads per family | 560 | 560 |

W's peak resident graph was **24 bytes smaller in each of five held-out families**, satisfying the proposal's narrow “named integer metric lower in at least four families” rule. Its mean resident observation was 32.75 bytes smaller. That is a Python representation result, not a meaningful overall memory-compression result.

There are opposing costs: larger parsing-transient graphs, 306 more selection-object shell bytes allocated per family, 1,904 ASCII packet bytes rewritten, 50 decodes, and 1,500 more logical returned bytes per family. Logical traffic uses the declared 56-byte string / 26-byte packed semantic-field accounting plus canonical record encodings; it is **not measured network traffic or the actual size of a Python tuple on a wire**. Canonical full metadata serialization was also slightly larger in every held-out W family. Do not treat summed byte observations across checkpoints as simultaneously resident memory.

The ordinary index therefore performs the same information-management work without string encoding/decoding. The workspace is a viable interface representation; this run supplies **no overall efficiency win over the index**.

The prefix-scan control paid for 5,520 event visits over the 120 held-out query occasions, plus reconstruction allocations and lookups. Its cost must not be used as though an ordinary index necessarily rescans history. Exact-control raw cost tables include all extra retrieval work; X_W/I incremental exact fetch costs must be added to their already charged manager costs, while X_S includes reconstruction and X_latest includes its own policy validation. The additional revision index's construction appears under L in EVENT_WORK.csv.

All models' identical input requirements were charged symmetrically. W/I shared physical forwards through the experimental audit cache; the cache grew to **9,145,833 object-graph bytes** in the main producer and is not free deployed memory. Model-input cache hits are not a speed advantage of whichever arm ran second. Query order rotated W/I/O. Timings include instrumented bookkeeping, are fully retained, and are descriptive only.

## 6. Verification and the execution history

**This was not a flawless first execution.** The final scientific results retain the following history:

| Execution version | Outcome | Attempted forwards |
|---|---|---:|
| v0.3 | Fixture capture succeeded; scorer crashed while indexing an absent O-arm reference. No main inputs generated. | 45 |
| v0.4 | Scorer-only repair; full fixture and exact replay passed. Main capture was interrupted by the assistant's tool-command timeout before scoring. | 1,175 |
| v0.5 | Identical scientific implementation; full fixture/replay passed again. Tool interruption recurred despite a longer requested command timeout. No main score. | 1,175 |
| v0.6 | Supervised process launched separately and polled in this turn; complete main capture, independent score and fresh replay passed. | 3,600 |
| **All attempts, including interruptions** | **Within the unchanged 6,000-call hard cap** | **5,995** |

Two interrupted in-flight attempts lack an acknowledged completion (5,993 acknowledged vs 5,995 attempted). They remain charged, and their partial arrays/logs are retained without inventing missing terminal receipts.

The v0.3 bug fix short-circuited hidden-binding inspection for routes with no reference, with a new regression test. All nineteen non-neural contract methods pass. The later versions changed only administrative lock/counter records and execution transport. Source/seed/event/policy/threshold bytes remained identical; all regenerated public and protected main stimulus bytes match the interrupted versions. No completed main results existed before the restart, no cases were selected or dropped, and no held-out tuning occurred.

**Explicit recovery exception:** v0.6 carries the already completed v0.5 fixture, including its original source lock, independent scores and fresh replay. Scientific source-byte identity was checked and that fixture was independently re-scored again. It does not claim another v0.6 fixture forward run. This preserved the finite call budget rather than resetting it. Both interrupted main versions remain marked incomplete.

Main exact fresh-process replay matched **14,400 arrays / 187,200 numeric elements**, all 1,800 numerical output containers, event/query metadata and all **16 independently scored files**. The carried fixture matched **360 arrays / 4,680 elements**, 45 numerical outputs and 16 score files. Timing and supervisor resources are explicitly excluded from bitwise comparison; all observed deterministic memory/cost fields matched.

The independent scorer does not import the producer, generator, controller, model or capture modules. It reconstructs catalogue generation, event histories, current truth and bindings separately, verifies numerical pointer arithmetic with the preserved amendment and applies the independent original decoder. This is internal implementation independence, not third-party replication or cross-device validation.

The worker received one public committed event at a time and the current numerical query. File guards blocked protected/future raw files and protocol/producer/scorer access. Main capture and replay each checked 384 altered-hidden/future envelope projections. Toy prefix tests and independent chronology reconstruction supplement this separation; these are concrete checks, not a formal information-flow security proof.

## 7. Numerical and historical boundaries

All fifteen exported weights passed final byte-hash checks; main workers checked participating weights before/after inference. Optimizer construction and gradient/backpropagation calls were guarded against. There were no optimizer updates.

The frozen verifier and separately reconstructed v1.6 underflow amendment are preserved. The final probability-error allowance remains **2^-126**. The retained v1.6 regenerated underflow fixture still fails the frozen verifier and passes the amendment on unchanged inputs. It is not the missing original rejected row, and the reconstructed implementation is not relabelled as the missing original v2 source.

Historical Q010 limitations remain: unavailable full optimizer/RNG checkpoints and raw main training traces; compact recovery omits older bulk main capture/replay; archived old verifier failures remain failures. This study does not restore training history, requalify original training, revise Q010 thresholds or prove the full NSS architecture. Frozen Primary, Secondary, Tertiary and advisory Validator roles were not implemented or replaced by this deterministic manager; Forge/Runtime was not integrated.

## 8. Resource accounting and reproducibility

The same conservative clock began at 19:59:30 UTC on 24 September 2026 and includes implementation, all attempts and restart preparation. Main replay/comparison completed at **1,726.40 seconds**, below the two-hour cap. The largest completed-stage sampled process-tree RSS was **597,893,120 bytes**; maximum sampled container memory **1,920,397,312 bytes**, below 3 GiB and 3.5 GiB abort limits. Sampling was every 0.05 seconds. Very short peaks can be missed; the initial extraction was not continuously instrumented and the two interrupted supervisors emitted no final resource receipts. Do not substitute summed successful-stage times for the full shared clock. Delivery QA is recorded separately.

The host was CPU-only Python 3.13.5 / NumPy 2.3.5 / PyTorch 2.10.0+cpu, with four CPU equivalents of quota and a 4 GiB container hard memory limit. Actual timings are not deployment forecasts.

All new public inputs, isolated labels, model outputs, control results, costs, negative outcomes, replay and interrupted evidence are included. Old model/archive payloads are not duplicated. The 48.7 MB **Q010_InferenceRecovery_v1.6_RecoveryContext.zip** remains the numerical source/model dependency; CM-01's archive is needed to repeat the prior-data novelty audit, not for scoring the retained CM-02 arrays.

`VERIFY_STUDY.py` checks delivery bytes and optionally dependency hashes. `RESCORE.py` re-scores completed evidence without model forwards. `REPLAY_STUDY.py` starts an explicitly separate reproduction in a new directory; its CLI/syntax were checked but it was not used for a third neural run in this delivery. Do not reset the archived 5,995-attempt ledger or overwrite delivered evidence.

## 9. Research interpretation

The bounded engineering layer behaves as specified: task references persist through switches; corrections apply to the addressed task; stale revisions and deletion are distinguished; no-cue intent errors remain unresolved. The compact string adds no recall advantage over the same information in a normal index.

The useful next architectural question is therefore **not** how to make a bookmark beat a dictionary. It is whether a real learned recurrent state can use a small management workspace to preserve and update task progress with less total state or repeated processing. That requires a separately specified native state transition, training protocol, observations and matched-resource controls. CM-02 does not launch or train that experiment.

In plain terms: **the bookmark survives the changing library, but an ordinary library index works just as well. Asking for the newest edition requires a different retrieval policy than refusing an old edition. Neither mechanism knows that a perfectly plausible bookmark points to the wrong book unless it has evidence of the mistake.**

## 10. Delivery quality checks

A relocated candidate copy passed byte-integrity verification, all 29 frozen local source/protocol checks and 164 numerical dependency checks. Its main and carried fixture were independently re-scored: **all 32 result files matched byte-for-byte**, with **zero additional model forwards**. The total attempted-call ledger remained 5,995. The shared clock through this QA was 2145.57 seconds, below two hours. The final ZIP integrity and exact delivery identity are in the separately supplied delivery receipt.
