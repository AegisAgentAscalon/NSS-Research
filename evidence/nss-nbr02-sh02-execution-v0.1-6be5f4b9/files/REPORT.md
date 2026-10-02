# NSS NBR02 SH02 — Hierarchical-reader cleanup report v0.1

**Local study date:** 27 September 2026, America/Detroit; operational timestamps are UTC, 28 September.
**Disposition:** clean executable component; functional and tolerance-based numerical parity established on the specified checks; archive bit-for-bit replay mismatch retained. **No universal runtime or whole-maintenance efficiency claim.**
**Training:** zero optimizer applications, zero new fits, zero model downloads. Backward/gradient tests did not modify weights.

## 1. Main result

SH01's hierarchy is now an isolated, versioned graph/plan/backend/reader package. Shared-neighborhood packing reuses gathered keys and values across the four query records of each task rather than gathering the same neighborhood four times. The two-bucket execution uses native PyTorch SDPA on selected neighborhoods, preserving one joint softmax, all original allowed edges, original feature vectors and every learned parameter.

At128 tasks/batch1 the cleaned path is 3.71x faster than the old HSA path in this timing session. At512 it is 5.63x faster. At8 tasks/batch1 it is slower. Relative to full dense attention it wins only at the512-task batch1 size in the measured set; full dense uses a different graph and is not an equal-quality comparison. These are measured conditions, not a universal backend crossover.

Every one of 9,984 retained task decisions across the three complete HSA finals and all development/confirmation/stress panels is unchanged. Previously reported confirmation correctness remains 6,133/6,144 (99.8210%). Existing errors remain errors; no repair was applied. The old incomplete8803/HSA fit was neither completed nor selected.

## 2. Architecture deliverable

See `ARCHITECTURE.md`. The package separates typed evidence encoding, immutable topology, plan compilation and bounded cache, numerical execution, learned reader, and advisory JSON output. There is no context manager or output-generation mechanism newly layered on top.

The three levels are task records, regional metadata anchors, and a global anchor. Prerequisite links are supplied metadata. Plans are independent of evidence values and weights. A source-value change reuses topology but recomputes neural features; a dependency/scope/layout change creates a new plan. The cache stores no activations or K/V values. Restart validates topology checksums and reconstructs indices. These are software contracts, not learned capabilities.

The planner allows variable numbers of prerequisites, but the trained37-feature adapter deliberately retains exactly two. With bounded prerequisites and square-root regions, allowed-edge growth is O(N sqrt(N)), not linear. DARP, language tokens, a25,000-token workspace, autonomous diagnosis and full nightly maintenance remain outside scope.

## 3. Correctness and failure-first validation

The locked engineering suite passed **92/92 case checks**. Forty-eight cases compare fresh graph layouts and exact feature encodings with SH01 (three worlds per case);24 cases compare native attention outputs and Q/K/V gradients in float32/float64; four compare full-reader input and parameter gradients. Additional cases exercise degenerate/variable-dependency topology, bounded cache eviction, forbidden-edge noninterference and dispatcher-visible shape inspection. Twelve explicit fault checks cover invalid dependencies/layout/scope, corrupt/stale/mutated plans, malformed/nonfinite features and model mutation. Case checks contain multiple assertions and are not independent scientific trials.

Engineering scalar comparisons: **623,800**, zero tolerance breaches. Float64 includes a separately indexed NumPy attention reference. Envelopes remain SH01's float32 `2e-5 + 2e-5*abs(reference)` and float64 `1e-10 + 1e-9*abs(reference)`. No tolerance changed after results.

Full saved-model regression checks all logits against legacy and same-graph masked reference, and both attention-block outputs against legacy: **2,918,400 stage scalars**, zero violations. Additional comparisons to all saved logits also pass. The tests check gradients but perform no optimizer steps.

### Retained learned behavior

| Model | Split | Correct / decisions | Whole worlds correct | False COMPLETE | Changed predictions |
|---|---|---|---|---|---|
| 8801 | development | 256/256 | 32/32 | 0 | 0 |
| 8801 | confirmation | 2048/2048 | 256/256 | 0 | 0 |
| 8801 | stress | 1023/1024 | 63/64 | 1 | 0 |
| 8802 | development | 256/256 | 32/32 | 0 | 0 |
| 8802 | confirmation | 2038/2048 | 247/256 | 1 | 0 |
| 8802 | stress | 1016/1024 | 56/64 | 0 | 0 |
| 8804 | development | 256/256 | 32/32 | 0 | 0 |
| 8804 | confirmation | 2047/2048 | 255/256 | 0 | 0 |
| 8804 | stress | 1024/1024 | 64/64 | 0 | 0 |

The source fixtures are exposed regression fixtures, not new reserved confirmation. Repeated worlds across seeds and task decisions within worlds are not independent trials. Accuracy preservation is a refactor result, not new learning evidence or increased model competence.

### Historical bitwise replay limitation

The regression driver retains a stricter archival bit-for-bit check. **All nine historical output files differ in their least-significant output values even when using the unchanged SH01 source and original parameter tensors in the current runtime.** That made `regression.py` return exit1; this is not erased or reported as an all-pass exit.

Post-result replay following SH01's full-batch-then-slice convention did not eliminate the differences. The legacy/archive maximum absolute difference was at most **2.38418579e-06**. All legacy/archive tolerance checks passed, with no changed class decisions. The cause is unresolved; it must not simply be called a proven hardware or rounding cause. Two independently launched current processes reproduced all nine NEW cleaned-output files bit-for-bit, and scalar recounts agreed. This supports current-environment reproducibility, not historical bitwise identity or external replication.

Raw legacy/archive arrays are retained under `failures/legacy_bit_mismatch_*.npz`; the first strict-driver receipt and post-audit results are preserved. No historical gate in SURFACE/TRACE/RECOVER/SH01 was changed.

## 4. Runtime measurements

One CPU thread, PyTorch2.10.0+cpu, identical8801/HSA weights and supplied inputs across timing backends, five warmups and31 deterministically shuffled/interleaved repetitions per condition. Includes feature projection, two attention/FFN blocks and readout; excludes feature/plan construction, separately reported below. `full_dense` is a different graph and its shared-weight outputs are not a newly trained dense comparator. Timings use steady-state, already-validated plans; checked-entry timings are also retained.

### Batch1 primary reader timings

| Tasks | Positions | Old HSA ms | Packed HSA ms | Full dense ms | Old/packed |
|---:|---:|---:|---:|---:|---:|
| 8 | 36 | 0.6226 | 0.7934 | 0.2663 | 0.78x |
| 32 | 135 | 1.7751 | 1.2772 | 0.5324 | 1.39x |
| 128 | 524 | 9.5426 | 2.5691 | 1.9619 | 3.71x |
| 512 | 2072 | 71.2465 | 12.6545 | 19.5640 | 5.63x |

The512-task fixture contains2,072 record positions and is a cost probe only; it is not a test of512-task learned competence or language context. Larger-size timing alone does not establish a full maintenance benefit.

### Batch16 auxiliary timings

| Tasks | Old HSA ms | Packed HSA ms | Full dense ms | Old/packed |
|---:|---:|---:|---:|---:|
| 8 | 4.5942 | 2.6222 | 1.0156 | 1.75x |
| 32 | 20.4133 | 9.5186 | 4.6354 | 2.14x |
| 128 | 238.6076 | 69.5437 | 29.7374 | 3.43x |

The packed path improves on old HSA in these batch16 conditions, but full dense remains faster in every measured batch16 shape. No automated fastest-backend selection was introduced.

### Cold preparation and reuse charges

| Tasks, batch1 | Plan build ms | Features/specs ms | Warm cache lookup ms | Full cold packed pipeline ms |
|---|---:|---:|---:|---:|
| 8 | 0.1724 | 0.1443 | 0.0111 | 1.1789 |
| 32 | 0.3495 | 0.3044 | 0.0114 | 1.7587 |
| 128 | 1.0362 | 0.9391 | 0.0154 | 4.5051 |
| 512 | 5.5831 | 3.5550 | 0.0348 | 20.1825 |

Cold pipeline measures feature/spec creation, plan construction and one packed reader call together. Component medians need not sum exactly to pipeline medians. Plan cache lookup avoids reconstruction only when topology is reusable. At128 tasks/batch1 plan construction costs about1ms and the full cold pipeline is about4.5ms in this session. The graph is not free, and source retrieval/JSON/archive lifecycle costs are not included in these reader-level measures.

## 5. Memory and operator observations

| Tasks, batch1 | Old gathered K/V bytes/layer | Packed gathered K/V bytes/layer | Reduction |
|---|---:|---:|---:|
| 8 | 175,104 | 41,984 | 76.02% |
| 32 | 864,000 | 210,944 | 75.59% |
| 128 | 4,829,184 | 1,189,888 | 75.36% |
| 512 | 31,295,488 | 7,755,776 | 75.22% |

This is known gathered K/V tensor payload per layer, NOT a75% reduction in total model/process memory. Query packing, result concatenation, mask/index tensors and native-kernel workspace remain. Full dense SDPA need not materialize all logical pairwise scores. No overall memory or energy win is claimed.

CPU operator profiles at128 tasks (batch1 and16, five calls each) show `aten::index` as the largest self-time entry in the old HSA implementation, with elementwise multiplication and reductions also prominent. Packed execution reduces gathered payload and replaces the large elementwise attention calculation with SDPA calls; indexing remains a major cost, and batch16 introduces substantial copy/fill overhead. This is a profiled localization, not a separately randomized causal decomposition of each optimization.

Profiles retain per-operator input shapes, self-time and allocation totals. Positive allocation sums are not peak-live memory, and profiling overhead affects timings. Wall-time tables come from unprofiled calls. The final-condition process peak RSS was 495,636,480 bytes; the original interrupted process's terminal RSS is unavailable. A whole-sweep peak cannot be invented from the surviving value.

## 6. Operational record

The first benchmark tool call reached its20-second caller timeout after six of seven cost conditions had durable timing records. Training was not involved. The first six conditions and console are retained under `failures/cost_runner_timeout/`; only the seventh (batch16/tasks128) was executed by an explicitly derived continuation driver. The ordering RNG was advanced through the six completed conditions. No timed samples were selected for favorable performance, no backend changed, no completed condition was rerun for replacement.

The merged final timing file contains all seven planned conditions. Original `benchmark.py` stayed source-locked; `complete_costs.py` is a separately identified operational driver. End-to-end wall time and terminal peak RSS of the first process are unavailable. Script section times, raw timing samples, and known continuation times remain available. The typed JSON demo completed without any external action.

## 7. Integrity and interpretation

All140 upstream SH01 manifest payloads and ZIP CRC verified before use. Three inference exports strip optimizer/RNG state but preserve exact tensor hashes and source-file identities. All locked source files remained byte-identical; post-result replay and continuation drivers are separately identified. Delivery manifests cover the new package; its ZIP is verified after creation.

What this earns: a cleaner, tested hierarchical component and a substantial execution improvement over its predecessor at medium/larger tested sizes. It does not prove universally faster HSA, a scalable recursive hierarchy, better learned accuracy, a stronger-dense comparison, segmented-context/HSA synergy, or efficient full-night NSS maintenance. It is a working foundation for those subsequent tests, not authorization to run them now.

## 8. Implementation references

External implementation guidance only; the measured results above come from this package.
- PyTorch2.10 scaled-dot-product attention semantics, masks and numerical caveats: https://docs.pytorch.org/docs/2.10/generated/torch.nn.functional.scaled_dot_product_attention.html
- PyTorch2.10 profiler and collection overhead: https://docs.pytorch.org/docs/2.10/profiler.html
- FlexAttention plan/mask reuse as a future backend lead, not an implemented dependency: https://pytorch.org/blog/flexattention/
