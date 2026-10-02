# NSS NBR02 SC02 — Incremental segmented maintenance, Execution v0.1

**Disposition: COMPLETE_BOUNDED_INCREMENTAL_ENGINEERING.** All 720 main conditions,20 timing cells,36 fresh-process episode replays and24 saved-workspace resumptions completed. No main class divergence, numerical-tolerance violation or duplicate receipt. Main caller interruption and inference-only completion are retained. The common engineering changes yield material measured speedups, especially under source changes and larger worlds. Scheduling has mixed incremental value. The additional intermediate-neural cache was slower than the otherwise identical P path in all 20 timed cells.

Receipts are timestamped28 September2026 UTC (local27 September in America/Detroit). No optimizer applications, new fits or weight changes in main execution. Existing8801/8802/8804 checkpoints;8803 remains incomplete. Exact SH02 three-level graph,37 features,18,500 parameters retained. No DARP, natural-language interface or full maintenance-night qualification.

## 1. User goal and experimental boundary

The owner asked to improve segmented context before moving on; even historical24 ms to below20 ms would be encouraging. That target was not treated as a requirement to manufacture a win. The historical32-task resume episode already runs at 13.144 ms under unchanged SC01 in the current runtime. P takes12.939 ms: a1.6% measured median reduction, too small for a strong isolated claim. Historical24.195 ms must NOT be directly contrasted with the new12.939 ms to claim the optimizer saved11 ms. All primary efficiency comparisons rerun old C/S and new F/P/I contemporaneously.

There is a stronger result on32-task source churn: old cache23.632 ms, SC01 segments20.939 ms, new P16.367 ms (30.7% faster than C,21.8% faster than S). On128-task churn, C52.360 ms,S49.490 ms,F26.532 ms,P28.925 ms. These are actual complete fixture-episode-core measurements, not forecasts. F beats P on that cell, so scheduling is not universally beneficial.

## 2. What changed; what did not

| Arm | Record/plan engineering | Work selection | First-block row cache |
|---|---|---|---|
| C | Unchanged SC01 publisher, compiler and signatures | Ordinary cache/request order | No |
| S | Unchanged SC01 publisher, compiler and signatures | SC01 event invalidation + greedy overlap | No |
| F | Exact vectorized initial/restart compilation; changed-row updates; graph-reusing plan construction; reuse exact signatures after full version-tuple checks | Conventional request order | No |
| P | Same F engineering | Event invalidation; compare ordinary and overlap packings by(group count, closure rows, first-block rows); ties favor ordinary | No |
| I | Same P engineering | Same P scheduler | Bounded, model-bound, per-neighborhood source-version validation |

All retain the same exact archive, query evidence, original two-layer semantics, result-cache capacity32 (4 in the declared eviction stress), and input caps. Generic improvements also go to the ordinary F reference. Results do not establish an advantage exclusive to the category "segmented context." No branch selects tasks from correctness labels.

Ordinary progress/receipt/constraint changes patch the matching encoded detail row; freeze patches the global row. Dependency changes validate and rebuild the topology/feature representation rather than attempting unsafe partial topology edits. Initial/restored feature construction is vectorized but compared byte-for-byte with the original compiler.

P's scheduling rule evaluates two inexpensive complete packings. It is not a global optimal scheduler or a calibrated runtime predictor. I keeps first-layer row outputs, not second-layer results or a trained memory. Each cache entry depends on all original keys of that first-layer query. Missing rows are recomputed with the unchanged neural modules. Numerical tensors are cloned per row to avoid retaining an entire batch through a view.

A fixed model identity is checked at binding; parameter mutation/replacement during use is rejected. Numeric/signature/source/plan caches are transient and cold after checkpoint restoration. Durable jobs/results are restored with original independent scope, model and source checks. There is no cross-weight activation migration.

## 3. Profile and development scope

Retained SC01 world seed 932101 was used for development, with cProfile at 32-task resume and128-task churn. It identified publication, plan construction and fingerprint/JSON work in addition to neural compute. Heavy diagnostic accounting was outside the original timed core and remains outside all timed cores: it was NOT removed to manufacture the headline saving. Profile overhead makes those diagnostic timings unsuitable as the final performance estimate.

Two development smoke passes and the34-case engineering suite preceded the main source lock. Earlier successful smoke output was replaced by the subsequent development pass; this is development, not multiple reserved confirmations. The pre-vectorization source is retained in development/. All failed historical SC01 tests remain historical; no new engineering test failed in the final SC02 suite. See scripts/profile_baseline.py and development/.

## 4. Fresh main results

48 fresh episodes:8/32/128 tasks x two new seeds942201/942202 x eight families(reuse,sweep,churn,revisions,resume,oversize,eviction,global). Each executed under three existing checkpoints and five arms:720 conditions. Original source generator retained; fresh world inputs were generated after source freeze and hashed. Eviction uses a4-result cache; global adds global changes and restart. These are repeated-context engineering checks, not720 independent learned models or61,620 independent task draws.

- **61,620 available answer observations**, **246,480 output-score scalar comparisons**.
- **0 changed classes**, **0 breaches** of unchanged float32 `abs(error)<=2e-5+2e-5*abs(full_reference)`.
- Maximum absolute error **4.053115845e-06**; largest fraction of permitted envelope **0.134160**.
- **0 duplicate(job,task,evidence-signature) receipts**.
- Maximum active rows36/126/383 under 40/128/384caps.
- Each arm answered12,324 times and was correct12,199 times (**98.9857%**); every arm preserved the same learned mistakes. No false COMPLETE in this panel. Correctness of the software execution is distinct from the underlying reader's imperfect task accuracy.
- Each arm explicitly deferred1,728 task-answer attempts in undersized controls. Total unresolved observations1,884per arm also include intentional interrupted-work positions; neither category is silently counted as completed work.

All source truth, answer statuses, class labels and evidence signatures matched between C and each other arm at 576 paired episode comparisons. Numerical closeness rather than identical floating values is the execution requirement. No tolerance was relaxed.

## 5. Actual maintenance timing — exposed reference workloads

Same CPU process per size, one thread, model 8801, seed 932101. One whole-episode warmup per arm/cell; then11 randomly interleaved repetitions, all retained. Times are median milliseconds. The order is seeded and recorded. New candidates were not tuned using reserved data.

| Tasks | Workload | C: old cache | S: SC01 | F: fast cache | P: planned segments | I: + neural cache |
|---:|---|---:|---:|---:|---:|---:|
| 8 | reuse | 2.888 | 2.084 | 2.406 | 2.395 | 2.730 |
| 8 | sweep | 2.972 | 2.119 | 2.511 | 2.313 | 2.706 |
| 8 | churn | 14.897 | 13.749 | 12.081 | 13.441 | 14.041 |
| 8 | resume | 6.712 | 6.029 | 7.222 | 6.998 | 7.241 |
| 32 | reuse | 6.799 | 4.883 | 4.716 | 4.291 | 5.836 |
| 32 | sweep | 10.104 | 8.437 | 7.868 | 8.326 | 9.449 |
| 32 | churn | 23.632 | 20.939 | 16.849 | 16.367 | 18.310 |
| 32 | resume | 14.863 | 13.144 | 13.757 | 12.939 | 14.959 |
| 128 | reuse | 15.350 | 13.181 | 9.279 | 8.909 | 11.116 |
| 128 | sweep | 47.335 | 47.788 | 35.073 | 37.414 | 44.213 |
| 128 | churn | 52.360 | 49.490 | 26.532 | 28.925 | 30.791 |
| 128 | resume | 36.427 | 33.819 | 27.451 | 26.884 | 30.763 |

P is faster than S in9/12cells, but slower in all three non-churn8-task cells. Its equal-cell geometric mean time ratio to S is0.88585(11.4% lower); this is a descriptive summary of this selected grid, not a deployment-weighted average or confidence bound. P versus F is almost tied in aggregate (ratio0.99581), despite individual wins and losses. Ordinary engineering deserves most of the credit.

## 6. Fresh timing workloads

New seed 942203 at 32/128 tasks; resume/churn/revisions/sweep. One prescribed warmup, then7 interleaved repetitions per arm/cell. Same frozen source, no post-timing tuning. These do not create fresh independently trained models.

| Tasks | Workload | C: old cache | S: SC01 | F: fast cache | P: planned segments | I: + neural cache |
|---:|---|---:|---:|---:|---:|---:|
| 32 | sweep | 11.260 | 9.877 | 9.821 | 10.790 | 11.887 |
| 32 | churn | 35.222 | 29.176 | 26.245 | 23.300 | 26.039 |
| 32 | resume | 15.631 | 13.833 | 13.702 | 14.155 | 15.519 |
| 32 | revisions | 16.575 | 12.780 | 12.890 | 11.316 | 14.745 |
| 128 | sweep | 44.408 | 47.505 | 36.612 | 37.274 | 44.849 |
| 128 | churn | 66.675 | 55.691 | 36.791 | 32.029 | 33.906 |
| 128 | resume | 39.149 | 31.443 | 29.029 | 27.864 | 30.965 |
| 128 | revisions | 39.921 | 26.599 | 25.844 | 21.770 | 26.691 |

P beats S in6/8 fresh timing cells and C in8/8. It beats F in5/8. Equal-cell P/S geometric time ratio0.84450 (15.6% lower), but fresh32-task resume is2.3% slower and sweep9.2% slower than S. Retain these losses. Exact individual samples, quartiles, min/max and order are in results/benchmark_*.json. There are940measured episode samples across100 arm/cell combinations, plus100 declared warmup episodes. Small differences should not be interpreted as established improvements from this limited CPU experiment.

## 7. Where the time went

The full-source-update ablation is especially clear in the retained128-task churn fixture. Median total source-publication time inside the episode falls from 12.782 ms(S) to0.298 ms(P); the job-processing phase also falls from 33.360 ms to25.923 ms. At 32 tasks, publication falls4.001 ms to0.232 ms. Component medians are separately calculated and need not sum exactly to the median whole episode. F gets the same publication improvement; this is not exclusively a segmentation benefit.

The128-task churn episode previously encoded1,008,176 bytes across initial publication and12 changes; F/P/I encode79,328 bytes (initial77,552 plus12 x148-byte changed rows). This is avoided rematerialization, NOT compressed evidence or reduced source truth. Its initial archive is still fully RAM-resident.

Across fresh main episodes, C/S/F/P/I issue987/945/987/942/942 sliced reader calls. Scheduling thus reduces only three calls from S in this aggregate and45 from request-order F; it does not eliminate the rest of the fixed-work cost.

## 8. The additional neural cache did not earn adoption

I reused28,800 of 61,344 first-layer output-row demands, reducing freshly computed first-layer rows to32,544(**46.95% fewer**). Encoder rows fell from 174,588(P) to113,412(I). Yet **I is slower than P in all 20 timing cells**. Its equal-cell geometric slowdown is about14.7% on the retained grid and15.0% on the fresh grid. Less neural work is not automatically less elapsed time.

The cache adds complete-neighborhood version checks, tensor copying/stacking, partial-stage planning and bookkeeping. Those are plausible contributors, not individually isolated causal attributions; this study did not profile every operator of I. Many reuse workloads already hit final-answer memoization, and restart intentionally drops intermediates, limiting their extra opportunity. Keep I code/results as a measured negative, not a recommended default.

## 9. Memory and measurement boundaries

I's peak retained first-layer tensor payload is49,152 bytes(48KiB); validity metadata serialized to JSON peaks55,717 bytes, and extra partial-plan tensors75,036 bytes. These are separate declared payload maxima; do not sum them as an observed simultaneous RSS peak. F/P/I also add a bounded exact-signature memo; its serialized representation peaks50,864 bytes. These metadata costs are real even where CPU time improves. Python object overhead is not captured by serialized payload sizes.

All methods can hold56,832 bytes of source-row cache at the largest cap, plus archive, activations, graph/plan metadata, result memo, jobs and receipts. I explicitly has an extra bounded numeric pool; it is NOT an equal-total-memory comparison. Largest recorded main-process RSS is333,176,832 bytes, including multiple model/reference/framework allocations, not an isolated per-policy peak.

Timing scope matches SC01: initial archive ingestion, workspace creation, model binding for new implementations, retrieval, validation, planning, neural work, changes, receipts and JSON checkpoint/archive reconstruction. Excludes process/model startup, full-reference scoring, expensive diagnostic payload accounting, publication to disk and actual filesystem durability. `whole_seconds` retains the wall call including diagnostic bookkeeping; it must not be equated to the timed core. This is an in-memory typed fixture, not the total cost of a whole maintenance night, real RAG I/O, language-token budget or training.

Main retained counts:4,803 sliced reader calls and2,160full-reference forwards. Main core time sum13.118s is not the research bill. Development/profiling,940timed episodes,warmups,post-run audits and publication are additional. The interrupted process's unsaved inference work is unknown; no exact all-process forward count is claimed. Optimizer applications remain exactly0.

## 10. Failure-first engineering and operational record

34 engineering checks passed: nine51-state publisher/restart comparisons; nine multi-change/eviction/resume neural-lifecycle tests;16other fault and boundary checks. Injected cases cover bad dependencies with rollback, wrong model/scope, malformed/corrupted snapshots, duplicate/invalid jobs, lost revision notifications, changed/replaced parameters, nonfinite evidence, invalidated intermediates/signatures, too-small budgets and snapshot isolation. Snapshot scope checks and checksums are not authentication against a malicious actor able to rewrite evidence and checksum together.

One90s caller timeout interrupted the command running32-task then128-task main evaluation.32 tasks completed;233/240128-task conditions were durable, the last being n128_s942202_revisions_m8804_F. A separately hashed operational driver executed only the missing7 conditions from the same fixed fixtures and checkpoints. All 233 existing output hashes stayed unchanged. The incomplete condition's unsaved inference count and first-process terminal RSS/time are unavailable. No source, gate, fixture, budget or learning change, and no repeated completed condition. See failures/main_caller_timeout.json and operational/complete_n128.py.

## 11. Post-result audit

Independent raw recount re-derived the deterministic task rule from each source fixture's event history, recomputed argmax/errors/tolerance checks in720 files and found no mismatch.576 policy-semantic comparisons matched. Fresh-process replay of 36 declared P/I episodes reproduced all saved observation and trace records bit-for-bit.24saved workspaces resumed to bit-exact final traces; intermediate caches were cold after restoration, as specified.23originally locked source/config/model files and48 fresh fixtures remain hash-identical. The original SC01 input manifest verified522payloads; original baseline code was copied unchanged.

These are internal consistency and repeatability checks, not independent third-party replication or a companion-identity study.

## 12. Assessment

Retain the incremental publisher, cached-graph planner and exact-signature reuse as working engineering improvements. Keep conventional F and scheduled P as alternatives; P has workload-specific extra value, not a universal right to replace ordinary grouping. Do not enable I by default on these measurements. Small jobs remain a documented weak point of the heavier machinery.

This pass demonstrated improvements larger than 2 ms in several relevant changing-record workloads, while accurately showing that the specific historical24 ms resumption case did not gain comparably in the current runtime. A useful bounded optimization result does not require every cell to improve or every idea to survive. Three hierarchy levels and all learned weights remain intact. Further timing/model research requires its own dispatch; no DARP or follow-on run is implied.
