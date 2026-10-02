# Work, storage and admission worksheet — proposed, not measured

## W1. Update schedules

One full pass: 800 initial updates +96 main method/fit/base contexts×18 +100 probe applications +12 clean contexts×18 +8 fault applications = **2,852**. Capture plus full adaptive replay = **5,704**; hard cap7,000. A context has two common receipts then four four-update tails. A zero P/S application is still an attempt and commit. No second adaptive correction at one receipt.

The12 clean contexts are two fixed synthetic cases ×G/L×delays0/8/32. Start from an untrained fixture initialization and import eight authenticated **fixture-only** historical observation records into its buffer without training. This is a proposed explicit fixture input type, not a claim that the untrained weights know those labels. Its source/authority must be exercised by the normal checker; no hidden scorer table is copied into a scientific model. Each clean context includes its own frozen N trajectory. Low untrained accuracy is expected.

The100 cost-probe applications comprise14 old-cue warmup updates per method, then two independent four-tail contexts (2×18) each restarting from that method's step14 probe state: 2×(14+36)=100. This replaces the old cheap-only probe. The two technical focal coordinates are in the development coordinate range, with a separately fixed synthetic label map; actual main-development labels are not generated for these probes. No held-out coordinates or target labels. Probe weights are discarded. Query the eight old cues once after each probe warmup; each probe context includes N and full after-receipt inventories. A cost forecast based only on the14 warmup steps is invalid.

Eight isolated faulty applications per pass use the inherited G/L ×two fixed targets×wrong-sign/double-step schedule, plus one post-state query each. Projection/constraint corruption tests use copied certificates and do not add optimizer applications. No faulty weights seed scientific work. Additional live fault categories require a new ledger, not uncharged calls.

## W2. Full proposed call arithmetic

| Quantity | One pass | Capture + complete adaptive replay | Proposed cap |
|---|---:|---:|---:|
| Parameter applications | 2,852 | 5,704 | 7,000 |
| Recurrent cell evaluations | 92,388 | 184,776 | 240,000 |
| Head evaluations | 29,676 | 59,352 | 75,000 |
| All reverse-mode calls | 3,230 | 6,460 | 8,000 |
| Exact old-margin reverse calls, included above | 1,800 | 3,600 | 4,500 |
| QP calls | 240 | 480 | 600 |
| Active-support candidates, maximum | 61,440 | 122,880 | 153,600 |

There are112 contexts per pass (96 main,4 probe,12 clean). P and S independently compute8 old derivatives:1,792 old-margin forward/backward evaluations, plus8 fixed old-margin numerical checks. All eight old records are charged even if a row is zero or duplicated. G accounts for half of2,852 focal update derivatives plus4 no-update derivative diagnostics. L focal sensitivities are separately counted; exact old derivatives in L+P/S are hybrid work.

Each update exposure—including the three fork reconstructions—uses3 cells/1head. Nine scratch queries follow each of the18 applications in every context. N adds6 transaction forwards plus54 post-receipt queries per context. Initial inventories account for8fits×8old cues plus their frozen copies (128 queries). The sandbox has8 queries; the focal and margin diagnostic families each have8 forwards. Probe warm inventories add16 queries. The JSON gives each term rather than folding them into an opaque allowance.

Clean fixture waits apply only to15 actual cue episodes in the four-tail path (18 exposures minus3 reconstructions), plus6 in N. Across two cases, two methods and d0/8/32, this adds3,360 cells per pass and zero heads. Reconstructing a saved cue is not another detached waiting period.

A QP enumerates at most256 supports. Budget at most255 subset SVDs plus one full-row rank SVD per call. A normalized full constraint product has8×674=5,392 scalar multiply-accumulate positions; record the actual matrix operations and launches. These are finite operation bounds, not vendor-FLOP or latency measurements. Independent certificate/derivative scoring, exact-X and authority checks are outside neural counts but inside time/storage accounting.

## W3. Component sizes and a schema that must still be proved

One float32 parameter/gradient vector:2,696bytes. One8×674 float32 Jacobian:21,568bytes; its float64 version:43,136bytes. Each P/S solve needs separately owned or explicitly shared named arrays for captured A, normalized C, scales, d2/dP, chosen multipliers and actual deltas. Eight simultaneously retained autograd graphs are not required; process old records sequentially. Graph saved-tensor ownership and native overhead still require measurement.

The full schedule reserves224 protection solves per pass and448 across replay. Raw A32 arrays alone are9,662,464bytes across those solves; A32 plus one normalized C64 is28,987,392bytes. These are literal component calculations—not whole-study or resident-memory totals, and not necessarily all stored simultaneously. Genuine repeat arrays may be aliased only after computation and byte equality have been recorded. No result can be reconstructed after a crash and presented as its original capture.

Proposed compact per-QP subset-status layout:256 rows×at most128 fixed-width bytes =32,768bytes, plus a single full chosen KKT certificate and arrays. Do not record256 full674-vector candidates unless the storage budget explicitly accommodates them. The score-relevant original A, selected step and all actual outputs must remain. This encoding choice changes retained diagnostics, not the mathematical solver; it is stated before execution.

The implementation must produce a record-kind manifest with full counts, dtype/shapes, bounded headers, authority/provenance strings, parameter snapshots, gradients, both Jacobians, solver summaries, branch/frozen/control records, full RNG/cursors, fault logs, manifests and1MiB emergency reserve. It must include independent scoring scratch space and peak simultaneous archive/restore buffers. A copied209MiB allowance or update-only compressed-size extrapolation is not a derivation.

Measure decoded and losslessly encoded sizes separately on clean/probe work. Project by record kind and show uncompressed/encoded totals, safety margins and added nonnumeric overhead. A compressed-size forecast is empirical. Actual stored evidence≤256MiB and single ZIP≤64MiB remain hard limits. No compression ratio or final ZIP size has been measured for PROTECT01.

## W4. Cost claim limits and schedule

The intended host metadata is recorded separately: a CPU-only Torch package, four CPU-equivalents of quota,4GiB container maximum. No neural runtime, SVD timing, native memory instrumentation or cost probe was run in this review. Pin real runtime/BLAS details in the authorized source lock.

P/S must pay equal old-gradient/solver work and public-buffer construction; B1/B2 are explicitly cheaper references. Shared diagnostic data may be deduplicated for archival storage, not charged as a deployed inference speed advantage. Inspect NumPy backing-array ownership and native graph storage; until validated, OBS-DC01-COST-001 prevents a whole-memory superiority claim. Component arrays, wall timings and sampled RSS may still be reported honestly.

Order: source/seed/ledger lock → non-neural authority/codec/solver/cast checks → untrained gradient/clean/fault fixtures → expensive-operation cost probes and schema admission → eight initial fits → development and B1-only competence/calibration → lock held-out admission → generate/evaluate held-out → independent scoring → full fresh adaptive replay → fresh extraction/relocation re-score.

The active two-hour cap includes implementation, setup, every stop/attempt, audit and delivery QA; inter-turn pauses must be explicitly accounted. An unknown-completion mutation is never silently repeated. Failed attempts use reserve but do not authorize extra fits or altered science. If a cap/source/solver/control failure prevents completion, retain the partial record and return a specific blocker. Do not squeeze the study in by deleting unfavorable cases or omitting replay.
