# NSS NBR02 SC01 — Segmented Maintenance Workspace v0.1

User-authorized component implementation and bounded tests, following the proposed SC01 comparison. No optimizer updates, new fits, DARP, language-model download, architecture-depth change, or actual nightly candidate training. Three task/region/global levels and all SH02 weights and graph semantics remain fixed. This version introduces an **exact backward-closure execution interface**, not approximate truncation or a new learned segmentation policy.

## Questions and operational definition
1. Can a bounded workspace process maintenance requests, preserve already recorded work across an interruption, detect changed evidence/dependencies, and explicitly defer a request that cannot fit?
2. Does dependency-aware segmentation add benefit beyond ordinary indexed retrieval AND a strong conventional cache?
3. What remains of the proposed context saving when the full two-layer SH02 dependency closure is respected?

The main unit is an episode of maintenance requests/source changes/checkpoint-resumption, not a language token or an optimizer step. Outputs are advisory dispositions and version-bound task receipts. These are synthetic typed maintenance tasks, not a whole companion or autonomous repair mechanism. Small and larger workloads are both retained; larger shapes are transfer/cost diagnostics, not trained competence qualification.

## Fixed comparison
- INDEX: exact indexed archive, caller task order, greedy budget-fitting groups, no transient evidence or neural-result cache.
- CACHE: same management interface/order/grouping; bounded ordinary LRU evidence rows and **per-task memoized neural results**. On each result lookup, validate the complete source-version dependency fingerprint. This is a deliberately stronger baseline than caching raw input alone.
- SEGMENT: same evidence/result capacities and same persistent job/receipt contract; order pending work by incremental overlap of exact required rows, and use explicit revision-event invalidation for memoized results. Missing revision events are errors. Restart independently validates result fingerprints. This is a combined scheduling/invalidation policy, not a claim that its techniques are novel or unavailable to ordinary software.

All methods have the SAME common durable job-progress/receipt mechanism and a bounded 16-entry topology execution-plan cache. Ordinary methods may resume completed work without repeating an already-receipted advisory. Correctness is not manufactured by withholding persistence from the baseline. Cached mistakes stay mistakes.

## Neural information contract
A final task query requires its original block-2 key set; those block-1 positions require their complete original block-1 input key sets. Take that full two-hop backward closure, retain global row identities and exactly compiled37-channel features, and perform unchanged per-row encoder, normalization, QKV, joint-softmax attention, residual/FFN, and final head computations. Queries sharing neighborhoods are packed together; no edge is omitted or re-normalized separately by hierarchy level. Batch1 CPU for SC01; preexisting weights8801/8802/8804,18,500 parameters. Original8803 remains incomplete.

The active cap counts **input record rows** for one closure, NOT total process memory or25,000 language tokens. Transient evidence-cache payload can also contain at most the same number of rows; active tensors, intermediate activations, plan indexes, provenance, result memo, durable receipts and full archive are additional and separately reported. Plan, feature, archive ingestion, invalidation, serialization, cold restart and reader work must be charged. No claim of out-of-core storage: the exact archive is simulated in RAM and its bytes/RSS are reported.

## Fixtures frozen before main results
Fresh generator is the copied source SH01 observable-world generator; never choose fixtures based on correctness. Fixed seeds932101 and932102, sizes8/32/128, six families(reuse, sweep, churn, revisions, resume, oversize),36 episodes total. Every model and every policy receives the same events:324 condition executions. Standard active-row budgets40/128/384; oversize budgets16/32/128. Result LRU32 entries for CACHE/SEGMENT. Each normal episode has12 requests for up to8 tasks; resume includes an additional paused12-task(maximum) job, first2 tasks before checkpoint, a correction while inactive, and subsequent continuation. Families are as encoded in locked `fixtures.py`.

Reuse repeats a selected set. Sweep visits disjoint sets when size permits; at8 tasks it necessarily repeats, and at32 the result cache can retain all tasks. Churn changes one progress record before each job. Revisions includes receipt, dependency and global-flag changes. Resume uses JSON checkpoint/reconstruction with common receipts. Oversize is an explicit-deferral test, NOT a fast successful-maintenance comparison.

## Criteria and accounting
- Exact software contracts: no source/scope/model/graph mismatch, silent budget overflow, stale emitted result, missing obligation hidden as completion, or duplicate receipt for the same job/task/evidence signature. Known malformed cases must be rejected, honest budget deferrals disclosed.
- Preserve same-weight full-SH02 behavior on available answers: zero changed classes and zero scalar tolerance breaches. Float32 <=2e-5+2e-5*abs(reference); float64 <=1e-10+1e-9*abs(reference), based on COMPUTATION dtype, not the container type after JSON reconstruction. Historical gates stay unchanged.
- Absolute learned accuracy is compared with the explicit source rule, separately from architectural equivalence. Report by size/model/family; repeated answers and memo hits are not independent neural trials. No requirement to repair existing model errors or attain100% broad competence.
- Benchmark full selected pipeline (in-memory archive ingestion and revisions, selection, cache checks, encoding/reader, progress updates, serialization/reconstruction). Reference scoring, diagnostic payload accounting and result publication occur outside the timed core and are reported separately. No hidden artificial disk latency. Fresh processes/model loading are not in per-episode core timing and must be disclosed.
- Formal timing: seed932101, sizes8/32/128, familiesreuse/sweep/churn/resume, model8801 only, three policies, one warmup then9 shuffled interleaved measured repetitions using RNG932901. No fastest-run selection. Same graph and weights in all arms. All raw samples retained. Unfit/deferral workloads cannot be compared as if useful work completed.

## Failure-first engineering, lock, resources
Engineering uses distinct seeds991xxx. Fixes before the source lock preserve failed source/receipts. Main source and fixture hashes are pinned before results. Unexpected model/numerical failure does not erase other valid measurements; mark affected claims unadmitted. Any post-lock bug fix requires a versioned amendment, not a silent overwrite.

Each main shard (one size and fixture seed) has600s wall and2GiB process RSS cap; total planned main computation budget3600s (six shards), evidence <=128MiB with16MiB reserved for failures. Each condition writes an atomic JSON result. Caller interruption leaves completed conditions intact and permits only inference-only continuation of missing conditions under unchanged source. Unknown work is reported, never invented. All completed raw outputs, fixtures, logs, fault checks, hashes, and runnable source must be delivered. Post-run audit may re-score retained outputs and repeat inference; no new study conditions or tuning are authorized.

## Boundaries
This implements program-managed records and deterministic segmentation/scheduling. It does not establish a model learned to write JSON or discover dependencies, a25,000-token maintenance budget, semantic summarization, neural-state migration across weight revisions, core identity retention, lifelong learning, native storage/GPU efficiency, or a full NSS night. HSA identity and records remain separate from future DARP output generation.
