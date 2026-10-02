from pathlib import Path
import json,statistics,collections,math,hashlib
R=Path(__file__).resolve().parents[1]
rs=[json.loads(p.read_text())for p in sorted((R/'results/episodes').glob('*.json'))]
ben=[]
for p in sorted((R/'results').glob('benchmark_*_n*.json')):
 if 'progress'not in p.name:ben+=json.loads(p.read_text())['rows']
groups=collections.defaultdict(dict)
for r in ben:groups[(r['scope'],r['n'],r['family'])][r['variant']]=r
summary={'status':'COMPLETE_BOUNDED_INCREMENTAL_ENGINEERING','main_conditions':len(rs),'unique_fixtures':len({r['episode']for r in rs}),
         'answers':sum(r['answers']for r in rs),'numeric_scalars':sum(r['numeric_scalars']for r in rs),
         'numeric_violations':sum(r['numeric_violations']for r in rs),'changed_classes':sum(r['changed_classes']for r in rs),
         'duplicates':sum(r['duplicate_receipts']for r in rs),'max_abs':max(r['max_abs']for r in rs),
         'max_normalized':max(r['max_normalized']for r in rs),'optimizer_applications':0,'model_fits':0,
         'main_reference_forwards':sum(r['reference_forward_calls']for r in rs),
         'main_sliced_forwards':sum(r['stats'].get('reader_calls',0)for r in rs),
         'main_core_seconds':sum(r['core_seconds']for r in rs),
         'record_caps':{'8':40,'32':128,'128':384},'max_active_rows':{str(n):max(r['stats'].get('peak_active_rows',0)for r in rs if r['n']==n)for n in [8,32,128]},
         'timed_episode_samples':sum(r['repetitions']for r in ben),'benchmark_cells':len(groups),
         'max_recorded_main_process_rss':max(r['runtime']['peak_rss_bytes']for r in rs),
         'branch_counts':{},'timing_comparisons':[]}
for v in 'CSFPI':
 a=[r for r in rs if r['policy']==v]
 summary['branch_counts'][v]={'answers':sum(r['answers']for r in a),'correct':sum(r['correct']for r in a),'false_complete':sum(r['false_complete']for r in a),
 'deferred_attempts':sum(r['stats'].get('budget_deferrals',0)for r in a),'unresolved_observations':sum(r['unresolved_positions']for r in a),
 'reader_calls':sum(r['stats'].get('reader_calls',0)for r in a),'reader_input_rows':sum(r['stats'].get('reader_input_rows',0)for r in a),
 'first_block_computed':sum(r['stats'].get('first_block_computed_rows',0)for r in a),'intermediate_hits':sum(r['stats'].get('intermediate_hits',0)for r in a),
 'ingest_encoded_bytes':sum(r['ingest_encoded_bytes']for r in a),
 'max_payloads':{k:max(r['accounting_peak_payload'].get(k,0)for r in a)for k in a[0]['accounting_peak_payload']}}
for scope in ['retained','fresh']:
 d=[v for k,v in groups.items()if k[0]==scope]
 for c,base in [('P','S'),('P','C'),('F','C'),('P','F'),('I','P')]:
  ratios=[v[c]['median_ms']/v[base]['median_ms']for v in d]
  summary['timing_comparisons'].append({'scope':scope,'candidate':c,'base':base,'wins':sum(x<1 for x in ratios),'cells':len(d),'equal_cell_geomean_time_ratio':math.exp(statistics.mean(map(math.log,ratios)))})
(R/'results/SUMMARY.json').write_text(json.dumps(summary,indent=2))

def table(scope):
 s='| Tasks | Workload | C: old cache | S: SC01 | F: fast cache | P: planned segments | I: + neural cache |\n|---:|---|---:|---:|---:|---:|---:|\n'
 for key,b in sorted(groups.items(),key=lambda kv:(kv[0][1],['reuse','sweep','churn','resume','revisions'].index(kv[0][2]))):
  if key[0]!=scope:continue
  s+=f'| {key[1]} | {key[2]} | '+' | '.join(f'{b[v]["median_ms"]:.3f}'for v in 'CSFPI')+' |\n'
 return s
report=f'''# NSS NBR02 SC02 — Incremental segmented maintenance, Execution v0.1

**Disposition: COMPLETE_BOUNDED_INCREMENTAL_ENGINEERING.** All720 main conditions,20 timing cells,36 fresh-process episode replays and24 saved-workspace resumptions completed. No main class divergence, numerical-tolerance violation or duplicate receipt. Main caller interruption and inference-only completion are retained. The common engineering changes yield material measured speedups, especially under source changes and larger worlds. Scheduling has mixed incremental value. The additional intermediate-neural cache was slower than the otherwise identical P path in all20 timed cells.

Receipts are timestamped28 September2026 UTC (local27 September in America/Detroit). No optimizer applications, new fits or weight changes in main execution. Existing8801/8802/8804 checkpoints;8803 remains incomplete. Exact SH02 three-level graph,37features,18,500parameters retained. No DARP, natural-language interface or full maintenance-night qualification.

## 1. User goal and experimental boundary

The owner asked to improve segmented context before moving on; even historical24ms to below20ms would be encouraging. That target was not treated as a requirement to manufacture a win. The historical32-task resume episode already runs at13.144ms under unchanged SC01 in the current runtime. P takes12.939ms: a1.6% measured median reduction, too small for a strong isolated claim. Historical24.195ms must NOT be directly contrasted with the new12.939ms to claim the optimizer saved11ms. All primary efficiency comparisons rerun old C/S and new F/P/I contemporaneously.

There is a stronger result on32-task source churn: old cache23.632ms, SC01 segments20.939ms, new P16.367ms (30.7% faster than C,21.8% faster than S). On128-task churn, C52.360ms,S49.490ms,F26.532ms,P28.925ms. These are actual complete fixture-episode-core measurements, not forecasts. F beats P on that cell, so scheduling is not universally beneficial.

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

Retained SC01 world seed932101 was used for development, with cProfile at32-task resume and128-task churn. It identified publication, plan construction and fingerprint/JSON work in addition to neural compute. Heavy diagnostic accounting was outside the original timed core and remains outside all timed cores: it was NOT removed to manufacture the headline saving. Profile overhead makes those diagnostic timings unsuitable as the final performance estimate.

Two development smoke passes and the34-case engineering suite preceded the main source lock. Earlier successful smoke output was replaced by the subsequent development pass; this is development, not multiple reserved confirmations. The pre-vectorization source is retained in development/. All failed historical SC01 tests remain historical; no new engineering test failed in the final SC02 suite. See scripts/profile_baseline.py and development/.

## 4. Fresh main results

48 fresh episodes:8/32/128tasks x two new seeds942201/942202 x eight families(reuse,sweep,churn,revisions,resume,oversize,eviction,global). Each executed under three existing checkpoints and five arms:720conditions. Original source generator retained; fresh world inputs were generated after source freeze and hashed. Eviction uses a4-result cache; global adds global changes and restart. These are repeated-context engineering checks, not720 independent learned models or61,620 independent task draws.

- **{summary['answers']:,} available answer observations**, **{summary['numeric_scalars']:,} output-score scalar comparisons**.
- **0 changed classes**, **0 breaches** of unchanged float32 `abs(error)<=2e-5+2e-5*abs(full_reference)`.
- Maximum absolute error **{summary['max_abs']:.10g}**; largest fraction of permitted envelope **{summary['max_normalized']:.6f}**.
- **0 duplicate(job,task,evidence-signature) receipts**.
- Maximum active rows36/126/383 under40/128/384caps.
- Each arm answered12,324 times and was correct12,199 times (**{12199/12324*100:.4f}%**); every arm preserved the same learned mistakes. No false COMPLETE in this panel. Correctness of the software execution is distinct from the underlying reader's imperfect task accuracy.
- Each arm explicitly deferred1,728task-answer attempts in undersized controls. Total unresolved observations1,884per arm also include intentional interrupted-work positions; neither category is silently counted as completed work.

All source truth, answer statuses, class labels and evidence signatures matched between C and each other arm at576 paired episode comparisons. Numerical closeness rather than identical floating values is the execution requirement. No tolerance was relaxed.

## 5. Actual maintenance timing — exposed reference workloads

Same CPU process per size, one thread, model8801, seed932101. One whole-episode warmup per arm/cell; then11 randomly interleaved repetitions, all retained. Times are median milliseconds. The order is seeded and recorded. New candidates were not tuned using reserved data.

{table('retained')}
P is faster than S in9/12cells, but slower in all three non-churn8-task cells. Its equal-cell geometric mean time ratio to S is0.88585(11.4% lower); this is a descriptive summary of this selected grid, not a deployment-weighted average or confidence bound. P versus F is almost tied in aggregate (ratio0.99581), despite individual wins and losses. Ordinary engineering deserves most of the credit.

## 6. Fresh timing workloads

New seed942203 at32/128tasks; resume/churn/revisions/sweep. One prescribed warmup, then7interleaved repetitions per arm/cell. Same frozen source, no post-timing tuning. These do not create fresh independently trained models.

{table('fresh')}
P beats S in6/8fresh timing cells and C in8/8. It beats F in5/8. Equal-cell P/S geometric time ratio0.84450 (15.6% lower), but fresh32-task resume is2.3% slower and sweep9.2% slower than S. Retain these losses. Exact individual samples, quartiles, min/max and order are in results/benchmark_*.json. There are940measured episode samples across100arm/cell combinations, plus100declared warmup episodes. Small differences should not be interpreted as established improvements from this limited CPU experiment.

## 7. Where the time went

The full-source-update ablation is especially clear in the retained128-task churn fixture. Median total source-publication time inside the episode falls from12.782ms(S) to0.298ms(P); the job-processing phase also falls from33.360ms to25.923ms. At32tasks, publication falls4.001ms to0.232ms. Component medians are separately calculated and need not sum exactly to the median whole episode. F gets the same publication improvement; this is not exclusively a segmentation benefit.

The128-task churn episode previously encoded1,008,176bytes across initial publication and12changes; F/P/I encode79,328bytes (initial77,552 plus12 x148-byte changed rows). This is avoided rematerialization, NOT compressed evidence or reduced source truth. Its initial archive is still fully RAM-resident.

Across fresh main episodes, C/S/F/P/I issue987/945/987/942/942sliced reader calls. Scheduling thus reduces only three calls from S in this aggregate and45 from request-order F; it does not eliminate the rest of the fixed-work cost.

## 8. The additional neural cache did not earn adoption

I reused28,800 of61,344first-layer output-row demands, reducing freshly computed first-layer rows to32,544(**46.95% fewer**). Encoder rows fell from174,588(P) to113,412(I). Yet **I is slower than P in all20timing cells**. Its equal-cell geometric slowdown is about14.7% on the retained grid and15.0% on the fresh grid. Less neural work is not automatically less elapsed time.

The cache adds complete-neighborhood version checks, tensor copying/stacking, partial-stage planning and bookkeeping. Those are plausible contributors, not individually isolated causal attributions; this study did not profile every operator of I. Many reuse workloads already hit final-answer memoization, and restart intentionally drops intermediates, limiting their extra opportunity. Keep I code/results as a measured negative, not a recommended default.

## 9. Memory and measurement boundaries

I's peak retained first-layer tensor payload is49,152bytes(48KiB); validity metadata serialized to JSON peaks55,717bytes, and extra partial-plan tensors75,036bytes. These are separate declared payload maxima; do not sum them as an observed simultaneous RSS peak. F/P/I also add a bounded exact-signature memo; its serialized representation peaks50,864bytes. These metadata costs are real even where CPU time improves. Python object overhead is not captured by serialized payload sizes.

All methods can hold56,832bytes of source-row cache at the largest cap, plus archive, activations, graph/plan metadata, result memo, jobs and receipts. I explicitly has an extra bounded numeric pool; it is NOT an equal-total-memory comparison. Largest recorded main-process RSS is{summary['max_recorded_main_process_rss']:,}bytes, including multiple model/reference/framework allocations, not an isolated per-policy peak.

Timing scope matches SC01: initial archive ingestion, workspace creation, model binding for new implementations, retrieval, validation, planning, neural work, changes, receipts and JSON checkpoint/archive reconstruction. Excludes process/model startup, full-reference scoring, expensive diagnostic payload accounting, publication to disk and actual filesystem durability. `whole_seconds` retains the wall call including diagnostic bookkeeping; it must not be equated to the timed core. This is an in-memory typed fixture, not the total cost of a whole maintenance night, real RAG I/O, language-token budget or training.

Main retained counts:4,803sliced reader calls and2,160full-reference forwards. Main core time sum{summary['main_core_seconds']:.3f}s is not the research bill. Development/profiling,940timed episodes,warmups,post-run audits and publication are additional. The interrupted process's unsaved inference work is unknown; no exact all-process forward count is claimed. Optimizer applications remain exactly0.

## 10. Failure-first engineering and operational record

34engineering checks passed: nine51-state publisher/restart comparisons; nine multi-change/eviction/resume neural-lifecycle tests;16other fault and boundary checks. Injected cases cover bad dependencies with rollback, wrong model/scope, malformed/corrupted snapshots, duplicate/invalid jobs, lost revision notifications, changed/replaced parameters, nonfinite evidence, invalidated intermediates/signatures, too-small budgets and snapshot isolation. Snapshot scope checks and checksums are not authentication against a malicious actor able to rewrite evidence and checksum together.

One90s caller timeout interrupted the command running32-task then128-task main evaluation.32tasks completed;233/240128-task conditions were durable, the last being n128_s942202_revisions_m8804_F. A separately hashed operational driver executed only the missing7conditions from the same fixed fixtures and checkpoints. All233existing output hashes stayed unchanged. The incomplete condition's unsaved inference count and first-process terminal RSS/time are unavailable. No source, gate, fixture, budget or learning change, and no repeated completed condition. See failures/main_caller_timeout.json and operational/complete_n128.py.

## 11. Post-result audit

Independent raw recount re-derived the deterministic task rule from each source fixture's event history, recomputed argmax/errors/tolerance checks in720files and found no mismatch.576policy-semantic comparisons matched. Fresh-process replay of36declared P/I episodes reproduced all saved observation and trace records bit-for-bit.24saved workspaces resumed to bit-exact final traces; intermediate caches were cold after restoration, as specified.23originally locked source/config/model files and48fresh fixtures remain hash-identical. The original SC01 input manifest verified522payloads; original baseline code was copied unchanged.

These are internal consistency and repeatability checks, not independent third-party replication or a companion-identity study.

## 12. Assessment

Retain the incremental publisher, cached-graph planner and exact-signature reuse as working engineering improvements. Keep conventional F and scheduled P as alternatives; P has workload-specific extra value, not a universal right to replace ordinary grouping. Do not enable I by default on these measurements. Small jobs remain a documented weak point of the heavier machinery.

This pass demonstrated improvements larger than2ms in several relevant changing-record workloads, while accurately showing that the specific historical24ms resumption case did not gain comparably in the current runtime. A useful bounded optimization result does not require every cell to improve or every idea to survive. Three hierarchy levels and all learned weights remain intact. Further timing/model research requires its own dispatch; no DARP or follow-on run is implied.
'''
(R/'REPORT.md').write_text(report)
Path('/mnt/data/NSS_NBR02_SC02_Report_v0.1.md').write_text(report)
(R/'OUTCOME.json').write_text(json.dumps(summary,indent=2))
print('report generated',len(report),'chars')
