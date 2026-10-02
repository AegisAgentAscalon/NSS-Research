# NSS SC02 — Incremental segmented maintenance architecture v0.1

## Scope
Execution optimization around the unchanged SH02 three-level task/region/global reader.37 feature inputs, two32-wide attention blocks,18,500learned parameters. Existing checkpoints unchanged. Typed, software-managed maintenance, not natural-language notes, autonomous learning, tri-core, DARP or25,000-token qualification.

## Authority and lifetimes
The RAM-backed Store retains exact world evidence, immutable encoded row bytes, monotonically advanced row versions and scoped revision events. Learned tensors and caches are not sources of truth. Workspace receipts remain bound to job, task, model and complete relevant source-version fingerprint. The source model and source revisions are never replaced with a cached inference result.

`IncrementalStore` subclasses the unchanged SC01 Store:
- Initial ingestion and restoration build the identical37-feature representation with vectorized assignments. It preserves address shape, two-prerequisite, binary-field, nuisance-shape and finite-feature validation.
- Progress, receipt and constraint edits regenerate the matching detail row; the freeze bit regenerates the global row. The exact changed row advances its revision once.
- Dependency edits are validated on a detached world, then fully rebuild topology and features. Invalid edits leave the accepted source world intact.
- Resizing, arbitrary concurrent edits and untrusted direct mutation outside the publication API are not supported.

`IncrementalWorkspace` retains SC01's active input cap, result cache, ledger and exact two-layer backward-closure execution. A segment still supplies every required original dependency or explicitly defers the task. It is not a new hierarchy level.

## Common fast execution (F/P/I)
A graph is derived once per topology rather than regenerated for every segment plan. Exact per-task closures and bounded16-entry slice plans reuse this graph. A bounded result-cap-sized signature memo retains the previous canonical SHA256 signature only when the complete dependency row-version tuple, task, IDs and topology still match. It does not replace a full version check with an approximate hash test. The signature string remains byte-identical to SC01's signature on the same evidence/model.

Existing model hashes are checked on first binding. Later calls verify that parameter references, mutation versions, dtypes and devices remain bound. Mutation or replacement requires a new workspace/model revision rather than reusing stale state. Unsupported hostile mutations that bypass both object/version tracking and the publication interfaces are outside the threat model.

## Work grouping (P/I only)
Original event-driven result invalidation is retained. Two possible complete packings are considered: original request order and the original greedy minimum-additional-closure ordering. Compare lexicographically by reader-group count, total closure rows and first-block output rows; ties use request order. Both use the same exact input cap. The chosen list is consumed across the current pending tasks, and discarded when no longer applicable.

This is a cheap heuristic, not an optimal solver. Less nominal work need not mean lower runtime, as measured. F remains a valid alternative rather than assuming the added scheduler is always useful.

## Experimental first-layer cache (I only; not recommended by current timing)
A row entry stores an exact first-attention-block output tensor, plus its topology and the version tuple of ALL original input rows in that query's neighborhood. Entries are bound to the workspace's accepted model. A cache hit requires full neighborhood-version agreement. Dependency/topology changes clear incompatible entries.

For a segment:
1. Determine the original first-layer output rows required by the final task queries.
2. Reuse valid entries; collect the missing first-layer rows.
3. Form the exact union of inputs for those missing rows and compute them with the unchanged encoder/first block.
4. Assemble all required first-layer rows, preserving their original row IDs and stage ordering.
5. Execute the unchanged second block, final norm and head.

Per-query attention retains one joint softmax over the original keys. There is no cross-layer in-place mixing. Cache tensors are individually cloned so a tiny row does not retain a full batch allocation through a view. An LRU retains at most record_cap32-float rows. A separate16-entry partial-stage plan cache exists only for this path.

The raw active segment is still admitted against the original closure-row cap even if cached intermediate values could theoretically avoid some input loading. This pass did not change information admission or hide new cache memory inside the existing cap.

## Checkpoints
Durable JSON includes the same jobs, pending work, receipts, bounded final-result memo, revision cursor and scope/model identity, with two additional explicit feature flags. It is serialized/digested once. Restore independently validates final-result fingerprints and preserves prior obligations. Raw-row, graph-plan, exact-signature and intermediate-neural caches are cold after restart; their subsequent rebuilding cost is included. No hidden state or activation cache crosses a model-weight update.

## Memory
Original active record budget40/128/384 at 8/32/128 tasks, plus separate raw row/result/plan caches and archive. Common exact-signature memo is additional metadata. I adds at most49,152tensor bytes in the largest tested setting, plus neighborhood validity and partial-plan metadata. These are not equal-total-memory arms. Total RSS, typed-row payloads, JSON metadata and per-stage allocations are distinct accounting measures.

## Implementation map
- `source/sc01.py`: unchanged upstream baseline and canonical signatures/ledger.
- `source/nss_hsa/`: unchanged SH02 hierarchy, features, attention and reader modules.
- `source/sc02.py`: incremental publisher, common fast workspace, optional scheduling and optional first-layer cache.
- `scripts/runner.py`: identical episode/event/scoring contracts across five arms.
- `tests/preflight.py`: publication equivalence, revision/restore/eviction and failure injection checks.
- `PROTOCOL.md`, `SOURCE_LOCK.json`, `FIXTURE_LOCK.json`: prospective boundaries and identities.

## Current evidence
F/P reduce runtime materially in several medium/large source-change workloads. Scheduling has mixed extra value; tiny jobs can be slower. I reduces first-layer computation but loses elapsed time in all 20 measured cells; leave it optional/experimental. Exact numerical/class equivalence and maintenance receipts passed the bounded fixtures. None of this establishes identity preservation for a full companion, language-token efficiency or an autonomous complete nighttime routine.
