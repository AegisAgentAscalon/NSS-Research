# NSS NBR02 SH01 — Execution report v0.1

**Date:** 27 September 2026, America/Detroit (execution timestamps use UTC, 28 September).
**Disposition:** WORKING FIRST PROTOTYPE; PARTIAL TRAINING COHORT; AVAILABLE FINALS FULLY EVALUATED.
**Overall efficiency advantage:** NOT ESTABLISHED. **No tri-core, DARP, prior GRU, or prior checkpoint was used.**

## 1. Main finding

A versioned JSON segment manager and a native hierarchical sparse attention reader now have
an executable shared interface. The completed HSA fits learned this small, explicit maintenance
rule substantially better than the equally trained dense fits. Persistent segment-packet reuse
reduced measured context-management cycle time without changing packets or reader decisions.
However, the native gather-based HSA implementation was 2.33–3.49 times slower than the
installed dense SDPA reader at the measured sizes. Its lower connection count is not a wall-time,
peak-memory, or complete-maintenance efficiency win.

Seven of eight scheduled 600-update fits completed. An external runner interruption left
8803/HSA incomplete, with a durable step-200 checkpoint. Three complete pairs (8801,8802,8804)
are the paired comparison; 8803/dense is reported but never used as an extra HSA comparator.
No seed replacement, shorter-checkpoint selection, threshold relaxation, or replay of uncertain
updates occurred. The interrupted run is retained, not relabeled complete.

## 2. What was built, and what remains supplied software

`source/store.py` implements an append-only versioned record store, scoped/time-cutoff lookup,
source digests, exact dependency-based packet assembly, budget refusal, cached version proofs,
source-change invalidation, serialized restart, and an idempotent action-receipt ledger.
`source/common.py` implements the typed-record compiler, shared trainable reader and native
sparse attention. `source/demo.py` loads a JSON packet and emits JSON maintenance dispositions
with model/source identifiers. It does not execute those dispositions.

Both managers use the SAME exact dependency index and evidence selection. The simple manager
rebuilds every packet; the persistent segmented manager can reuse a version-bound packet.
This is deliberately not a comparison with an incompetent retriever or a giant unrelated prompt.
It isolates persistence and reuse, not the complete value of semantic segmentation. Cache hits
still deserialize the packet, rebuild numerical features, and run the reader: no free KV cache
or free neural rereading is assumed. Source histories remain resident in this prototype; disk,
network and very large archive performance were not measured.

The hierarchy contains exact progress/receipt/constraint records, per-task metadata/query slots,
region metadata anchors and one global maintenance flag. Summary slots are not natural-language
summaries and do not contain precomputed desired dispositions. Regions summarize metadata only.
The manager and compiler supply identity, revisions, visibility, exact fields and dependency links;
the neural model learns the declared rule from those inputs. HSA edge selection is governed by
those explicit dependency IDs. It is NOT learned retrieval, learned top-k selection, language
understanding, automatic summarization or autonomous diagnosis.

The executable HSA graph provides dense local task interaction, direct connections to exact
prerequisite task records, own-region summary access, region anchors and a global anchor.
Native gather computes selected padded neighborhoods directly. No full T×T score tensor is
allocated on that path. A masked dense implementation exists only as a numerical reference.
The dense competitor uses `torch.nn.functional.scaled_dot_product_attention` from installed
PyTorch 2.10.0+cpu. Backend-specific dense memory allocation was not profiled, so logical
T² scores must not be reported as actual dense peak allocation.

The neural input has **37 engineered feature channels per record position**, compiled from JSON.
These positions are NOT language tokens. JSON is not compressed or tokenized by a language
model in this study. Neither a 25,000-language-token allowance nor an overnight cumulative
language-token budget has been tested.

## 3. Maintenance fixture and experimental design

Each world has eight tasks and two declared prerequisites per task. Evidence includes task
completion, receipts, unrelated local constraints and a global freeze flag. The requested
maintenance disposition is DEFER during a freeze; otherwise COMPLETE for an already completed
task, READY for a pending task with both prerequisites complete, or BLOCKED otherwise.
An independently written exact rule scored 2,048/2,048 on confirmation. The task is intentionally
algorithmic and does not require a neural model in production. This is a controlled mechanism
fixture, not a claim that HSA beats ordinary code for known bookkeeping.

Each reader has **18,500 trainable parameters**: width32, two 2-head attention/FFN
blocks, layer norms, and a four-class head. Dense/HSA initialization is paired within seed.
The same 9,600 training worlds in the same 600 batches of16 were used in every fit. All weights
train using the frozen AdamW settings in `PROTOCOL.md`. Final step600 is the only primary endpoint.
The functional reporting target was >=95% decision accuracy and >=90% macro recall per fit.
These are descriptive thresholds, not permission to suppress other measurements.

Confirmation:256 new eight-task worlds,2,048 task decisions/model. Stress:64 new sixteen-task
worlds,1,024 decisions/model, reported separately. The same worlds are reused across model seeds
and tasks within a world are dependent. Pooled decisions are not independent trials. Training,
development, confirmation and stress content fingerprints were disjoint; identical abstract
rules/labels naturally recur. Continuous random address codes are novel in held-out worlds;
this is not a new-rule or natural-language generalization test.

## 4. Fresh confirmation results

| Seed | Dense | HSA |
|---|---|---|
| 8801 | 1,854/2,048 (90.527%) | 2,048/2,048 (100.000%) |
| 8802 | 1,842/2,048 (89.941%) | 2,038/2,048 (99.512%) |
| 8803 | 1,855/2,048 (90.576%) | Unavailable: interrupted at saved step 200/600 |
| 8804 | 1,857/2,048 (90.674%) | 2,047/2,048 (99.951%) |

On the three complete pairs:

| Reader | Correct task decisions | Exact whole-world decisions | False COMPLETE |
|---|---:|---:|---:|
| Dense | 5,553/6,144 (90.381%) | 368/768 (47.917%) | 10 |
| HSA | 6,133/6,144 (99.821%) | 758/768 (98.698%) | 1 |

All three available HSA finals met the functional target; none of the four dense finals did.
This supports the usefulness of the provided hierarchy/dependency wiring for learning this
particular rule under the fixed training budget. It does not show an optimized dense model
cannot learn it, establish equal-quality inference efficiency, or complete the planned four-pair
cohort. Do not report 3/3 available as 4/4 planned or suppress 8803's interruption.

The main dense weakness is READY/BLOCKED discrimination, not the global freeze flag. For example,
8801/dense correctly recognized 52/210 READY cases and misclassified 158 as BLOCKED. HSA 8802's10
errors include eight BLOCKED→READY, one BLOCKED→COMPLETE, and one READY→BLOCKED. HSA 8804's one
error is COMPLETE→BLOCKED. Error records retain the actual progress, prerequisites, logits and
source-world fingerprint (`failures/learned_decision_examples.json`). This localizes affected
behavior; it does not identify a unique internal cause.

On sixteen-task stress, HSA accuracy was99.902%,99.219%,100% for8801,8802,8804 respectively;
pooled3,063/3,072 (99.707%). This is a modest length-transfer observation, not evidence for
thousands of language tokens. Dense stress results and all confusion matrices remain in the raw summary.

## 5. Four-configuration integration

The integrated fixture uses16 additional worlds with six jobs each: initial assembly, warm reuse,
a source revision, serialized restart, and continued reuse. The three complete pairs give:

| Configuration | Correct task decisions | Fully correct job outputs |
|---|---:|---:|
| simple + dense | 2,187/2,304 | 204/288 |
| segmented + dense | 2,187/2,304 | 204/288 |
| simple + hsa | 2,304/2,304 | 288/288 |
| segmented + hsa | 2,304/2,304 | 288/288 |

Both managers emitted byte-identical packet sequences for every available reader/seed and produced
identical predictions. Those equivalences include the changed dependency and restarted manager.
For each reader/seed, the persistent manager recorded 64 cache hits and 32 builds across 96 jobs;
the simple manager rebuilt 96 times. These repeated jobs are not96 independent worlds.

This establishes a working shared interface and reuse behavior in the fixture. It does NOT
establish superadditive architectural synergy, reduced neural token traffic, successful migration
of recurrent hidden state across weight updates, repeated nightly learning, or a complete NSS
maintenance cycle. No real unfinished user task or external action was executed.

## 6. Measured cost: gains and losses must be separated

### Full neural reader execution, fixed input and identical weights

One CPU thread, batch1, three warmups,15 alternating-order repetitions per mode. Includes
projection, two attention/FFN blocks and head. Weights from8801/dense are shared between modes
for the timing-only comparison; their HSA-mode accuracy is not a trained-model metric.

| Tasks | Record positions | Dense median ms | HSA median ms | HSA/dense | Fewer padded score cells |
|---:|---:|---:|---:|---|---:|
| 8 | 36 | 0.237 | 0.591 | 2.50× slower | 47.2% |
| 32 | 135 | 0.588 | 1.371 | 2.33× slower | 81.5% |
| 128 | 524 | 2.320 | 8.092 | 3.49× slower | 93.1% |

At 128 tasks, HSA uses 17,882 valid or 18,864 padded query-key cells per head/layer, versus 274,576
logical dense cells. **The 93.13% padded-cell reduction did not produce speedup.** The gather path
also materializes 4,829,184 bytes of selected K/V payload per layer at that size. This can outweigh
score-buffer savings; dense SDPA does not necessarily materialize the full logical score array.
No total peak-memory or energy advantage is claimed. A likely engineering contributor is gather
and temporary-buffer overhead, but this pass did not profile causal operator time or implement
an optimized block-sparse kernel. The code supports testing that next, not assuming it wins.

### Complete six-job context-management cycle

Includes initial store/index construction, six packet requests and JSON decodes, a source update,
and serialized checkpoint/restart. Excludes the neural reader and record-vector compilation.
Fifteen repetitions/condition, fixed simple-then-segmented order; small CPU measurements are
sensitive to ordering and noise. Raw timings are retained.

| Tasks | Simple median ms | Segmented median ms | Reduction | Source bytes decoded per cycle |
|---:|---:|---:|---:|---:|
| 8 | 1.417 | 0.970 | 31.6% | 18,841 → 6,537 |
| 32 | 5.653 | 3.677 | 35.0% | 74,979 → 25,253 |
| 128 | 20.079 | 14.009 | 30.2% | 300,429 → 100,401 |

The persistent manager built two packets rather than six. At 128 tasks its manager snapshot was
73,043 bytes versus167 bytes for the uncached manager, in addition to the common source store.
Both delivered 359,268 serialized packet bytes over the six jobs. **Source rereading fell; bytes
sent to the reader did not.** Caching spends retained memory to save rebuild/decode work.

The integration records also expose manager, compiler, reader and index timings separately.
Those one-pass timeline timings omit the serialized restart interval; use the lifecycle benchmark
above for restart-inclusive management cost. There is no combined energy metric, full-night cost,
or valid equal-quality dense/HSA latency comparison in this pass.

## 7. Failure-first checks and numerical verification

The first preflight crashed because restored test objects shared mutable nested objects with
the original. Injecting corruption into the supposed copy contaminated the source and another
fixture. The old store/preflight source and traceback are preserved in `failures/preflight_001/`.
Deep-copy isolation at store and manager snapshot boundaries fixed this before scientific locking.
Two explicit alias-isolation assertions were added; no confirmation data informed that fix.

The corrected suite passed **664/664 assertions**, including64 seeded lifecycle scenarios,
11 deliberate fault checks, numerical checks, optimizer smoke and native-shape inspection.
Assertions within repeated scenarios are not independent tests. Faults include wrong scope,
not-yet-visible records, mandatory-context overflow, missing source/dependency, corrupt source,
corrupt checkpoint/cache, duplicate revision, conflicting action receipt and stale packet.
Some fault checks detect differences rather than simulate every possible real-world corruption.

Across randomized 3/8/16/32-task layouts,32,640 attention-output scalars and97,920 gradient
scalars were compared between native gather and masked-dense paths: zero outside the predeclared
precision-specific envelopes. The float64 subset additionally used an independently indexed NumPy
softmax reference, with zero failures. Trained HSA finals were checked on the first eight
confirmation worlds per available seed (768 logits total), with zero tolerance breaches and no
argmax discrepancies. This trained numeric check is a subset, not every confirmation trajectory.
The previous studies' failed recurrent numerical gates were not changed or requalified.

Native tensor-shape tracing on the32-task attention path found no full T×T intermediate. This is
an implementation check at a sampled shape; source inspection explains the general gather layout.
Final-weight fresh-process replay reproduced all **21 saved development/confirmation/stress
logit files bit-exactly**. Independent scalar recounts agreed in21/21, and all **30 retained
checkpoint model hashes** matched. These are internal reproducibility checks, not third-party
replication or a complete independent model implementation.

## 8. Interruption, update accounting and evidence limits

The initial process was interrupted after five final fits and the 8803/HSA step200 checkpoint.
There is no surviving per-update journal for that process; losses held only in RAM were lost.
The last durable checkpoint establishes 3,200 main applications. Up to200 more may have occurred
before the next scheduled save; the exact count is unavailable. The interval is retained, not
replaced with a made-up exact count. Absence of the step400 save bounds the uncertainty under
the frozen schedule. No uncertain prefix was replayed.

Only the two not-yet-started 8804 fits were then completed, adding exactly 1,200 applications.
Total main work is therefore**4,400–4,600**, below the original 4,800 ceiling, plus**four disposable
preflight applications**. Seven finals completed; the eighth remains incomplete. The added driver
journals each update immediately. Operational source extensions are listed separately; all
original locked source/protocol/fixture hashes remained unchanged. No original schedule, labels,
learning rate, training batch order, or functional threshold was changed.

The first process's exact terminal time and peak RSS are unavailable. The continuation process
reported 10.465 seconds including fixture reload/training/evaluation and peak RSS617,877,504 bytes.
Post-execution integration/profiling/replay took 3.030 seconds with peak RSS 344,334,336 bytes.
These are separate process measurements, NOT total task wall time or a complete resource audit.
Preparation, implementation and packaging were not fully instrumented; first-process resource
compliance cannot be given a blanket pass. Evidence payload is well below the 128 MiB ceiling;
delivery records its final exact size. Storage forecasts did not stop this run.

## 9. Assessment and next engineering question

**Worth retaining:** the versioned context contract, exact evidence/provenance boundaries,
restart checks, fixed evidence across managers, native HSA forward/backward implementation,
and the trained typed-record feasibility signal. These are working components, not merely names.

**Not established:** a fully learned context manager, general retrieval/summarization, a stronger
maintenance output model, DARP, full-day/night repair, a 25,000-language-token budget, a superior
neural dense baseline, lower total memory, lower energy, native kernel efficiency, or an integrated
NSS architecture winner. Seven finals are not the scheduled eight.

The next justified engineering candidate is to keep this shared record contract while comparing
more efficient grouped/block execution with an optimized same-graph masked execution, then test
a stronger dense relational reader at an agreed quality level. That would separate useful graph
structure from the expense of this gather implementation. Per-segment encoding reuse would be a
separate version-bound cache proposal, not free reuse across changing weights. No such follow-on
run was executed or authorized automatically by these results.

**Bottom line:** the first components work together on this bounded fixture; the hierarchy helps
learning, packet reuse helps assembly, and the present sparse implementation loses on runtime.
The evidence argues for engineering the execution path—not calling the whole combination an
efficiency success because it uses fewer attention edges.

## Evidence map

- `PROTOCOL.md`, `SOURCE_LOCK.json`: prospectively defined mechanisms, settings and identity lock.
- `source/`: actual implementation; `complete_retained.py` is bounded operational continuation;
  `post_retained.py` excludes missing finals without replacing them.
- `fixtures/*.jsonl.gz`: raw typed-record worlds for train/dev/confirmation/stress/integration.
- `results/summary.json`, `pred_*.npz`: every evaluated final, class counts, raw logits and targets.
- `results/integration.json`, `integration_*`: packet equivalence, four-way outputs and costs.
- `results/benchmark.json`: all raw timing repetitions and allocation-accounting fields.
- `results/preflight.json`, `numerical_trained_*`, `audit.json`: math, lifecycle and replay checks.
- `results/interruption_receipt.json`, `main_outcome.json`: incomplete fit and bounded update count.
- `failures/`: retained preflight bug and first eight learned-error examples per completed fit.
- `checkpoints/`: all30 checkpoints, including the unfinished fit; no weights were selected post hoc.
- `examples/`: runnable JSON input/output example. Example is development, not confirmation.
- `MANIFEST.json` and external delivery receipt: file and archive integrity.

## Design provenance and external implementation references

The supplied `VargBot_MegaMind_Context_Architecture.txt` describes exact records, local detail,
compressed distant context, selected remote evidence, global anchors and bounded active packets.
It is preserved under `provenance/`. The exact graph, field encoding, rule and budgets here are
new implementation choices, not claims that the older source specifies this precise algorithm.
The user's latest direction makes maintenance efficiency the objective and does not require tri-core.
Longformer is an external precedent for combining local and global attention, not a reproduction
claim: https://arxiv.org/abs/2004.05150 . Official API guidance was checked for the installed version:
https://docs.pytorch.org/docs/2.10/generated/torch.nn.functional.scaled_dot_product_attention.html .
Only the relevant abstracts/API descriptions were consulted; no external model was downloaded.
