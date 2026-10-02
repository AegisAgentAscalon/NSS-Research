# NSS SC01 — Segmented Maintenance Workspace architecture v0.1

## Intent and boundary
A software-managed working set for typed NSS maintenance inputs, integrated with the fixed three-level SH02 reader. The design separates authoritative evidence, explicit work state, attention dependencies, neural arithmetic and emitted receipts. No new learning or output-generation architecture is introduced.

## Information path
1. A trusted archive publishes a scoped immutable world revision and encoded record rows. Rows retain exact global IDs, content and monotone changed-row versions. The archive is RAM-backed in this prototype; it is not the bounded active workspace.
2. A maintenance request names exact task IDs and a job ID. The ledger checks previously completed task receipts against current model/evidence dependencies before reusing them.
3. The planner works backward from selected output queries through the two original attention blocks. It gathers all input rows needed to reproduce those queries, without reindexing the world semantically, dropping graph edges, or replacing exact data with generated summaries.
4. A group is admitted only when its complete input closure fits the active-row cap. More work is partitioned into further groups; a single task whose closure cannot fit is explicitly deferred.
5. The unchanged learned modules process the admitted closure. Outputs are advisory class/logit records, not permission or proof that an action was executed.
6. A durable receipt binds job, task, model and evidence fingerprint to the result. A repeat with the same fingerprint is idempotent; changed evidence produces an explicitly version-distinct receipt.
7. Interruption serializes jobs, pending work, receipts and bounded result memo. Source-row and graph-plan caches are discarded and rebuilt after restore, with their cost charged. Restored result entries are independently revalidated.

## Three retained hierarchy levels
Task rows, regional metadata anchors, global anchor. Every query keeps its original SH02 neighborhood and one joint softmax. Per-layer computation remains simultaneous. The segment is an execution/work unit, not a fourth hierarchy level.

A two-layer task result depends on block1 representations for all keys of its final query; each of those representations depends on its original input neighborhood. Thus:
- Needed final positions: target task-query IDs.
- Needed first-layer positions: union of original neighborhoods for those queries.
- Needed input positions: union of original neighborhoods of those first-layer positions.
The current all-regional-anchor path entails global task-query metadata, even for a single target. Exact detail paging is possible, arbitrary independent local islands are not.

## Code interfaces
`Store(world, scope)` validates and publishes the exact typed record world. `mutate(change)` supports the declared evidence and dependency changes and records changed encoded rows. Source IDs/scopes/model IDs are part of cache/receipt validation. Arbitrary concurrent mutation and untrusted authenticated storage are not implemented.

`make_plan(spec, targets)` yields two stage plans and their required input IDs. `slice_forward(model, rows, plan)` uses the existing encoder, blocks, norms and head on that exact dependency subgraph. It does not edit parameter tensors. Grouped key/value gathers and backend workspace are additional to the input-row budget.

`Workspace(store, model_id, policy, record_cap, result_cap=32)` implements the three comparison policies. `job(id,tasks,model,limit_tasks=None)` completes available work, records remaining tasks, and emits explicit budget-deferral trace entries. `snapshot()` and `restore()` implement checked JSON continuation.

The policy distinction is practical, not a uniqueness claim:
- INDEX uses exact retrieval without source/result memoization.
- CACHE adds conventional LRU source and per-task result reuse, validating full dependency-version fingerprints at lookup.
- SEGMENT adds revision-event invalidation and dependency-overlap work ordering with the SAME cache capacities.
All retain the same common job and receipt semantics. Ordinary caching can implement similar features; the experiment measures this implementation rather than proving an architectural category is inherently superior.

## Resource lifetimes
- Accepted parameters: same fixed checkpoint throughout SC01.
- Exact archive: full raw world, encoded row bytes, revision events; retained outside active cap and charged separately.
- Active input: one complete segment's record rows, at most the declared cap.
- Transient source cache: at most the same row count, separately allocated.
- Numerical activations: temporary per-forward state, not a persisted cross-model KV cache.
- Graph metadata and plans: bounded16-plan cache plus per-world graph/closure indexes; no source values or learned activations in plans.
- Result memo: bounded32 task results, exact numerical dependencies and model identity; stale entries cannot be used after known relevant revisions.
- Durable job/receipt history: versioned records retained across restarts. This prototype does not yet compact long-running histories or bound total months-long backlog.

The active cap is NOT a total process-memory cap. Source cache, active tensors, row indexes, activations and archive can coexist. Encoded positions are NOT language tokens. Report uses measured runtime/RSS and separately labeled serialized/tensor payloads.

## Failure and acceptance behavior
Missing/malformed records, wrong scope/model revision, corrupted checkpoint, missing revision notification, invalid dependency, nonfinite input and graph mismatch have distinct errors. Full closure too large is an explicit deferral, not silent truncation. Recorded source truth is distinct from an imperfect neural decision. A cached wrong prediction remains wrong, with unchanged source references.

Numerical execution uses the original float32/float64 tolerances, with exact class preservation required for comparison to full SH02. JSON's storage dtype does not determine numerical-computation precision. Record/checksum integrity is exact; harmless admitted floating-point differences need not be bit-identical. Checksums are not cryptographic authentication of an untrusted publisher.

## Known limits
Fixed engineered features, exactly two prerequisites per task, supplied dependency identities, in-memory archive, single-thread CPU/batch1 timing, only two initial fresh-world seeds per task count, no natural-language read/write, no learned segmentation, no actual candidate learning or weight migration, no DARP. Current greedy scheduling is not optimal and sometimes increases reader calls. Global metadata needs limit context shrinkage. These are measured/reviewable constraints, not reasons to add more hierarchy levels automatically.
