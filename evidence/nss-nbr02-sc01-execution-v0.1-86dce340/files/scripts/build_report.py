from support import *
import shutil

def main():
    s=json.loads((ROOT/'results/SUMMARY.json').read_text());a=json.loads((ROOT/'results/audit.json').read_text())
    q=[]
    for n in [8,32,128]:
        g=next(x for x in s['groups']if x['n']==n and x['policy']=='index')
        q.append(f"| {n} | {g['correct']:,} / {g['answers']:,} | {100*g['correct']/g['answers']:.4f}% | {g['false_complete']} | 0 |")
    timing='\n'.join(f"| {d['n']} | {d['family']} | {d['index_ms']:.3f} | {d['cache_ms']:.3f} | {d['segment_ms']:.3f} | {d['segment_vs_cache_saving_percent']:+.2f}% |"for d in s['timing_contrasts'])
    counts='\n'.join(f"| {g['n']} | {g['policy']} | {g['reader_calls']:,} | {g['reader_rows']:,} | {g['archive_rows']:,} | {g['memo_hits']:,} |"for g in s['groups'])
    footprint='\n'.join(f"| {c['n']} | {c['full_positions']} | {c['min_single']}–{c['max_single']} | Yes |"for c in s['closure'])
    report=f'''# NSS NBR02 SC01 — Segmented Maintenance Workspace report v0.1

**Disposition: COMPLETE_BOUNDED_COMPONENT.** Exact graph-compatible segmented context and its lifecycle work on the specified synthetic maintenance episodes. All324 main condition executions completed. No main numerical failure, class divergence, or duplicate version-bound receipt was found. Efficiency beyond a strong conventional cache is modest and workload-dependent, not a universal architecture win.

**Time basis:** execution receipts record UTC28 September2026; this is the evening of27 September in America/Detroit. **Training:**0 optimizer applications,0 new fits,0 downloads. Same SH02 three-level hierarchy,37-feature representation,18,500 learned parameters, and existing8801/8802/8804 checkpoints. The incomplete8803 fit remains untouched.

## 1. What was implemented

`source/sc01.py` contains an exact versioned typed-record archive, a backward-closure segment planner, an executor of the unchanged two-block SH02 computation on that closure, bounded evidence/result caches, persistent unfinished-job records, advisory action receipts, source-revision invalidation, and JSON checkpoint/resumption. A complete required closure is loaded or the request is explicitly deferred; the model never receives an arbitrarily truncated neighborhood.

The original HSA package is copied unchanged. The new slice executor uses its frozen neural modules and original global row identities. The output query's entire two-layer dependency closure is computed, with one original joint softmax per query. No learned weights, graph edges, regional definitions, original encoded features, or model-depth rules were changed.

This is program-managed context for a small typed reader. It is not a language model writing its own notes, native25,000-token context, learned semantic segmentation, an autonomous repair planner, or a complete overnight learning-and-adoption cycle. Exact bookkeeping is software, not a neural achievement.

## 2. Comparators and fair information access

| Method | Transient reuse | Validation / work order |
|---|---|---|
| INDEX | No source-row or neural-result memoization | Exact retrieval, request order, greedy groups fitting the row cap. |
| CACHE | Bounded LRU of source rows AND per-task neural results | Recompute the complete dependency-version fingerprint on each result lookup; request-order grouping. |
| SEGMENT | Same source/result capacities | Explicit revision events mark affected results invalid; group pending work by incremental dependency overlap. Restart independently revalidates fingerprints. |

All three have the same durable job/receipt interface and bounded topology-plan cache. They can all preserve completed work across interruption. The cache baseline is not denied result reuse or resumption simply to make segmentation look necessary. The candidate combines scheduling and invalidation; this experiment does not separately identify their causal contributions or claim those techniques are unavailable to ordinary caching software.

Cached neural errors remain neural errors. Results are tied to the source archive, topology, full relevant source-version set, task and model identity. Unknown revision-event gaps, incompatible model/scope, malformed checkpoints and invalid graph dependencies raise explicit errors. Checksums detect accidental corruption, not a malicious party replacing both data and checksum.

## 3. Fixed workload and main outcomes

36 fresh episodes =3 sizes×2 fixture seeds×6 families(reuse, sweep, churn, revisions, resume, deliberately undersized). Each ran under3 existing models×3 policies, giving324 executions. Repeated worlds/tasks/policies and cached answers are not independent experimental replications.

The active input caps were40/128/384 typed record rows at8/32/128 tasks. Deliberately insufficient controls used16/32/128 rows. The32-entry result cache was identical for CACHE and SEGMENT. Each normal episode makes12 requests of up to8 tasks; resume adds an interrupted task set, intervening changed evidence, and later continuation.

- **{s['answers']:,} available answer observations:** zero changed class decisions versus the full same-weight SH02 reader.
- **{s['numeric_scalars']:,} output-score scalar comparisons:** zero breaches of the unchanged float32 envelope `2e-5 + 2e-5*abs(reference)`.
- Maximum absolute difference **{s['max_abs']:.9g}**; maximum fraction of allowed envelope **{s['max_normalized']:.6f}**.
- **{s['completed_request_occasions']:,} full request occasions** completed, and54 intentional partial occasions preserved progress for resumption.
- **{s['deferred_request_occasions']:,} undersized request occasions**, containing **{s['budget_deferrals']:,} task-answer attempts**, explicitly deferred. These are expected control outcomes, not completed maintenance successes or independent tasks.
- **0 duplicate(job,task,evidence-signature) advisory receipts**; changed evidence may legitimately produce a new superseding receipt.
- Maximum actual input rows36/126/383, respectively; no active-input cap breach.

These are exact information-management/equivalence outcomes, not100% underlying task accuracy. The unchanged learned reader still makes some mistakes:

| Tasks | Correct / observed answers, one policy | Accuracy | False COMPLETE | Class differences among policies |
|---|---|---|---|---|
{chr(10).join(q)}

Counts combine the three existing models and repeat occasions within two initial-world seeds. CACHE/SEGMENT have exactly the same counts. This table must not be compared as an independent new training result against SH01's different panel. The32/128-task conditions are small transfer/cost diagnostics, not qualified general scaling. Per-model class distributions/confusions are in `results/SUMMARY.json`.

## 4. The important context boundary

Every task query reads every regional anchor. On the next layer those anchors depend on all regional task-query metadata. Consequently the exact two-layer closure for even one task still includes all task query/identity rows, plus other necessary local/prerequisite evidence. This follows from the retained graph and was checked over the initial episode layouts:

| Tasks | Full input rows | Single-task exact closure range | All task-query metadata required? |
|---|---|---|---|
{footprint}

Ranges use the two initial layouts per size, not all possible graphs. The result does NOT mean every full task record must remain loaded: detailed state can still be paged selectively. It does mean that arbitrary tiny segments would change the model unless their original supporting information is provided another way. No information was dropped to make a budget pass.

The cap is **not total memory**. A separate raw evidence cache can hold up to that many rows as well; activations, numerical working buffers, plans, dependency metadata, provenance, result memoization, durable history, and the RAM-backed archive are additional. The full archive is resident in this prototype. No disk, compressed archive, network RAG, or end-to-end25,000-language-token claim is made.

## 5. Actual work saved

Main counts below include both fixture seeds and all three retained models. Input rows and reads are separate: a row can be served from cache yet still be processed again by the reader.

| Tasks | Policy | Sliced reader calls | Reader input rows | Archive rows fetched | Reused result observations |
|---|---|---|---|---|---|
{counts}

Most saving comes from conventional result/evidence reuse. At8 tasks, CACHE and SEGMENT do exactly the same number of reader calls and process the same rows; any timing difference there is management overhead, not reduced neural computation. SEGMENT sometimes packs work better, but its greedy ordering is not optimal. In the128-task timing fixture it actually uses3 calls rather than CACHE's2 in reuse,14 rather than13 in churn, and5 rather than4 in resume. This is a recorded negative, not hidden behind a favorable aggregate. At32 tasks the segmented method fetched slightly more archive rows overall despite processing fewer reader rows.

## 6. CPU/in-memory maintenance timing

One thread, existing model8801 only, seed932101. One prescribed whole-episode warmup, then9 randomly interleaved samples per method/condition. Values are medians in milliseconds **for the complete episode core**, not one neural forward. The timed core includes initial archive feature ingestion, retrieval, grouping, cache validation/invalidation, actual reader computation, receipt updates, source changes, and JSON checkpoint/store reconstruction. Full reference scoring, diagnostic payload accounting, result publication, process/model startup and explicit between-sample garbage collection are outside the core. Actual file-system durability and cold storage latency are not measured.

| Tasks | Workload | INDEX ms | CACHE ms | SEGMENT ms | SEGMENT saving vs CACHE |
|---|---|---|---|---|---|
{timing}

SEGMENT has a lower recorded median in11/12 cells; observed savings in those cells range0.84–25.24%. It is7.31% slower in32-task resume. The0.84% difference is too small to treat as a robust advantage from these runs. This is one CPU environment, one timing model, and one initial timing seed per size, not a general performance law or statistical superiority claim. Full raw timing repetitions and observed whole-call time are retained in `benchmark_n*.json`.

The smallest sweep necessarily repeats the same8 tasks; at32 tasks all32 outputs fit the memo capacity. Only the128-task sweep provides96 distinct requested task IDs with little result reuse. Do not describe every sweep row as a no-reuse workload.

## 7. Resource accounting and costs outside the active packet

Main runs performed **{s['main_sliced_reader_calls']:,} sliced forwards** plus **{s['main_reference_reader_calls']:,} full reference forwards**. Main measured maintenance-core time summed to{s['main_core_seconds']:.3f}s across324 conditions; this excludes preparation, auditing, formal benchmarking, documentation, and package construction. It is not the total research bill. Peak observed main-process RSS was{s['peak_main_process_rss_bytes']:,}bytes, including framework/model/archive allocations; it is not a per-policy isolated peak.

For the128-task resume timing workload, each archive contains77,552 encoded-row bytes plus33,367 canonical raw-world JSON bytes. CACHE/SEGMENT can additionally retain56,832 raw-row cache bytes. Their result-memo payload is about20.6KB; graph/closure indexes, plan tensors and progress receipts add further costs. Source ingestion recompiles the entire encoded world on publication and its cost is included. Payload fields are exact for their declared representations, not measurements of Python object overhead or total peak tensors. Memory counters must not be added naively because maxima need not occur simultaneously.

No optimizer was instantiated or stepped for this study. Backward/gradient learning was not performed. Unknown discarded timing work from two tool interruptions prevents an exact all-process inference-attempt total; known main counts above remain complete.

## 8. Failure-first checks and retained operational incidents

Engineering passed34 explicit cases, including10 injected faults, plus12 end-to-end engineering episodes. Checks cover exact closures, float32/float64 agreement, invalid/missing dependencies, nonfinite values, corrupt/mis-scoped/wrong-model checkpoints, repeated receipts, lost revision events, dependency changes, and snapshot isolation.

**Pre-lock verifier bug:** JSON reconstruction turned float32-computed scores into float64 containers. The first comparator selected the stricter float64 envelope from that storage dtype, yielding four failed assertions. The source, failures and receipt are retained under`failures/prelock_verifier_precision/`. The comparator was corrected before main lock to choose the unchanged tolerance from reference computation precision. This was not a post-result tolerance relaxation. All engineering checks were then rerun and passed.

**Timing interruptions:** a20s caller timeout interrupted the8-task sweep after three complete workload families; a60s timeout likewise interrupted the128-task sweep after three. All324 main cases had completed. Every completed timing sample was preserved. Separately identified operational drivers executed only each missing resume family, with the same9-sample schedule and RNG position. Any unsaved work from the interrupted families is unknown; no favorable sample selection or optimizer work occurred. All planned final timing cells are now present. Original locked code remained unchanged; continuation drivers are separately hashed.

## 9. Independent recount and internal reproducibility

The post-result audit independently recomputed the explicit task rule and argmax/error counts from every324 raw result file, with0 discrepancies. It checked216 policy-versus-index status/class comparisons, all equal. A separate process repeated54 retained episodes with bit-exact output/trace records, and restored36 saved workspaces then replayed their remaining events, all bit-exact at the final trace. The source/checkpoint/fixture lock remains intact.

These checks establish bounded internal consistency and repeatability, not external replication, production crash recovery, authentication, or general semantic memory. The common receipt mechanism simulates advisory publication, not actual tool actions against an external service.

## 10. Assessment and next design implications

**Working concept: yes.** Exact, bounded segments can be composed with the existing three-level HSA while preserving its decisions, managing revisions and interrupted work, and refusing unsupported truncation.

**Efficiency: partly.** Ordinary caching earns most of the improvement. The segmented scheduling/invalidation policy adds a smaller and nonuniform measured benefit, and its greedy packing occasionally increases neural calls. Do not replace all ordinary caching with it on these results.

The graph currently requires a global metadata base. A natural next design hypothesis is a small resident metadata/reference layer with selectively paged detailed evidence and a better measured scheduling policy. That would preserve the idea's division of responsibilities, but any actual graph or representation change requires a new protocol. The current working prototype remains a reference, not a whole-night NSS qualification. No follow-on study or DARP execution is included or authorized by these results.

## Evidence locations

- `PROTOCOL.md`, `SOURCE_LOCK.json`, `provenance/`: frozen scope and input identity.
- `source/sc01.py`, unchanged`source/nss_hsa/`, `checkpoints/`: executable component and retained parameters.
- `fixtures/`: all36 episode inputs.
- `results/episodes/`: all324 raw outcomes, including logits, source-bound receipts and explicit deferrals.
- `results/benchmark_n*.json`: all timing samples and payload counters.
- `results/audit.json`, `results/SUMMARY.json`: recount, reproducibility and aggregate tables.
- `failures/`: failed pre-lock verifier and both timing interruptions.

No historical SH01/SH02/SURFACE/TRACE/RECOVER result or gate was rewritten.
'''
    (ROOT/'REPORT.md').write_text(report)
    shutil.copy2(ROOT/'REPORT.md',ROOT.parent/'NSS_NBR02_SC01_Report_v0.1.md')
if __name__=='__main__':main()
