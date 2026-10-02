# Codex review — NSS NBR02 SH02 v0.1

## User direction
The user wants a clean hierarchical architecture before adding the rest of segmented context/HSA/DARP maintenance concepts. The objective is still efficient NSS maintenance. This pass isolates the hierarchy and cleans execution; it does not revive tri-core or authorize follow-on training.

## Delivered component
`nss_hsa/` separates immutable graph specification, compiled/cached topology plans, the SH01 feature adapter, an interchangeable attention backend, and the 18,500-parameter reader. Task queries are grouped four at a time with identical neighborhoods. Region/global singleton queries use a separate bucket. Gather K/V once per group and use small batched SDPA operations. Same SH01 graph, labels, features and weights; no approximate routing or training.

## Main findings
- 92 engineering case checks;623,800 scalar output/gradient comparisons with zero violations.
- All9,984 saved decisions across three available HSA finals and three exposed splits unchanged;2,918,400 full-reader/block stage scalars pass the frozen tolerance. Existing confirmation6,133/6,144 unchanged, not new qualification.
- Single-thread CPU batch1 at128 tasks:9.5426ms old gather ->2.5691ms packed (3.71x). At512:71.2465 ->12.6545ms (5.63x). Small8-task case is slower:0.6226 ->0.7934ms. Full dense remains faster except at512/batch1 in the observed grid; it is a different graph, not equal-quality evidence.
- Gathered K/V payload is about75% smaller, not total process/model memory. Plan build, feature construction and checked-entry costs are separately measured. Profiles identify old indexing/multiplication/reduction costs and remaining packed indexing/copy costs.
- Zero optimizer applications/new fits. Partial8803/HSA remains partial and unused.

## Negative/limited outcomes that must remain
`regression.py` returned exit1 on its retained archival bitwise-replay assertion. All nine old logit arrays differed slightly EVEN when running old source/weights here. Legacy max absolute difference<=2.3841858e-6; frozen numerical envelopes and classes match. Post-audit full-batch-then-slice replay did not remove this difference. Cause unresolved. All nine new clean files reproduce bit-exactly in a new current process. This is not a retroactive historical bitwise pass or an external replication.

The first benchmark call timed out after six complete conditions. The exact sixth and earlier samples are retained. A separately identified derived driver executed only the seventh, with reconstructed RNG position. No timings selected or backend changed. Original first-process terminal RSS/time unavailable; final-condition peak495,636,480bytes. All planned cost conditions are now present.

## Review priorities
1. Verify the two-bucket attention remains mathematically equivalent to SH01: exact edge sets, deduplication, one softmax, simultaneous layers, all parameter gradients.
2. Inspect the plan cache contract: topology/scope identity, mutation checks at trust boundaries, no evidence/KV/weight caching hidden inside it.
3. Check that payload and profiler-allocation totals are not misreported as whole-model peak memory.
4. Assess whether the current three-level O(N sqrt(N)) graph is an adequate bounded reference before designing recursive/bounded-fanout topology. Do not silently change it and reuse old accuracy as validation.
5. A same-graph optimized masked-dense execution baseline could establish a useful small-input dispatch path. It was NOT run here. Full dense cost measurements are not a substitute for an equal-quality/equal-graph comparison.
6. A stronger trained dense baseline and fresh larger-task qualification remain undone. This refactor does not need new fitting to validate preserved behavior, but it does not resolve those broader questions.

## Where to inspect
`ARCHITECTURE.md`, `PROTOCOL.md`, `SOURCE_LOCK.json`, `results/validation.json`, `results/regression.json`, `results/benchmark.json`, per-condition profiles, `results/post_audit.json`, `failures/`, and input lineage. The full package has runnable inference exports and fixtures; compact review ZIP omits those binaries.

No next experiment is dispatched by this review document.
