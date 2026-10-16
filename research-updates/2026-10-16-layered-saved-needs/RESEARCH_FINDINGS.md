# LAYERED01: which task demands still need work?

Saved-data analysis, 16 October 2026. Reviewed descriptive findings; no new model operations.

## Bottom line

The useful next target is keeping task outputs reliable throughout a delay while preserving older task skills, alongside remembering the final facts. More cycling alone did not solve that combination.

Parent 4101 improved on redundant-delay memory probes but deteriorated during delay/interference events. Parent 4102 improved on every recorded memory-probe cell, yet introduced errors on older prospective tasks. These are different failure patterns under one schedule comparison, not evidence for choosing a different recipe for each parent.

The original outcome remains **NO_QUALIFYING_CYCLIC_DOMINANCE**. Both panels are development data. This analysis proposes a subsequent hypothesis; it neither qualifies the model nor authorizes another training run.

## Study and unchanged verdict

CYCLIC used S256 → L256 → S256 → L256; BLOCKED used S512 → L512. Both parents started from their own original T0 and received 1,024 updates, 512 SHORT and512 LONG updates, and a continuous matched learning-rate schedule. Intermediate exposure differs.

The original saved audit reports 4,136 main/audit updates, 135,264 saved paths independently recounted, 2,740 exact repeat comparisons, and 88 training containers checked. This task did not rerun those operations. It rechecked selected saved scalar/prediction records and their hashes.

| Development panel | Parent | CYCLIC wrong | BLOCKED wrong | CYCLIC fixes | CYCLIC harms | Targets |
|---|---:|---:|---:|---:|---:|---:|
| existing | 4101 | 4 | 3 | 3 | 4 | 1680 |
| existing | 4102 | 8 | 19 | 16 | 5 | 1680 |
| confirmation | 4101 | 8 | 4 | 4 | 8 | 1680 |
| confirmation | 4102 | 4 | 13 | 12 | 3 | 1680 |

These are the unchanged primary NOOP_R64 memory answers. Pooled errors improve from 22 to 12 on the existing panel and from 17 to 12 on the prior-confirmation panel, but parent 4101 worsens in both. CYCLIC harms 82/764 existing schedule guard comparisons and 21/152 prior-confirmation schedule comparisons. It also fails 141/1,528 and 42/304 inherited practical S/T0 guard comparisons, respectively. Guard comparisons overlap; these are not counts of unique errors or unique cases. Neither practical qualification nor adoption follows from pooled improvement.

“confirmation” in machine-readable paths is the historical panel name. It is now development data. R128 is descriptive only. Comparisons with the older SL512 run change duration and learning-rate stretch together and cannot isolate a duration benefit.

## All matched memory-probe cells

Every row below has 1,680 matched answers. Fix means CYCLIC correct/BLOCKED wrong; harm means the reverse. Both-correct and both-wrong answers are retained in the machine-readable tables. Cases are paired by exact source ID, cell, truth configuration and probe number, with matching targets.

| Panel | Parent | Cell | CYCLIC wrong | BLOCKED wrong | Fixes | Harms |
|---|---:|---|---:|---:|---:|---:|
| existing | 4101 | BASE_R0 | 0 | 0 | 0 | 0 |
| existing | 4101 | NOOP_R128 | 15 | 7 | 7 | 15 |
| existing | 4101 | NOOP_R32 | 2 | 0 | 0 | 2 |
| existing | 4101 | NOOP_R64 | 4 | 3 | 3 | 4 |
| existing | 4101 | REDUNDANT_R128 | 68 | 102 | 78 | 44 |
| existing | 4101 | REDUNDANT_R32 | 26 | 73 | 59 | 12 |
| existing | 4101 | REDUNDANT_R64 | 56 | 83 | 62 | 35 |
| existing | 4102 | BASE_R0 | 2 | 8 | 7 | 1 |
| existing | 4102 | NOOP_R128 | 8 | 19 | 16 | 5 |
| existing | 4102 | NOOP_R32 | 8 | 14 | 13 | 7 |
| existing | 4102 | NOOP_R64 | 8 | 19 | 16 | 5 |
| existing | 4102 | REDUNDANT_R128 | 15 | 38 | 28 | 5 |
| existing | 4102 | REDUNDANT_R32 | 10 | 23 | 18 | 5 |
| existing | 4102 | REDUNDANT_R64 | 15 | 35 | 26 | 6 |
| confirmation | 4101 | BASE_R0 | 0 | 0 | 0 | 0 |
| confirmation | 4101 | NOOP_R32 | 3 | 0 | 0 | 3 |
| confirmation | 4101 | NOOP_R64 | 8 | 4 | 4 | 8 |
| confirmation | 4101 | REDUNDANT_R64 | 55 | 84 | 66 | 37 |
| confirmation | 4102 | BASE_R0 | 1 | 5 | 5 | 1 |
| confirmation | 4102 | NOOP_R32 | 4 | 12 | 11 | 3 |
| confirmation | 4102 | NOOP_R64 | 4 | 13 | 12 | 3 |
| confirmation | 4102 | REDUNDANT_R64 | 14 | 36 | 27 | 5 |

There are 23,520 matched memory answers on the existing panel and 13,440 on the prior-confirmation panel, across both parents. Parent 4101's redundant-delay gains coexist with NOOP_R32/R64 net harms in both panels. Parent 4102's cell totals all improve, but every cell still contains individual harms. Aggregate gains do not imply universal preservation.

## Task demands beyond the final memory probe

The following windows have their original complete denominators. Windows overlap, so their counts must not be added. Evaluation delay identifies the fixture, not the training regime or a causal mechanism.

| Parent/panel | Task demand and source window | CYCLIC wrong | BLOCKED wrong | Targets |
|---|---|---:|---:|---:|
| 4101 existing | REBUILD R64 delay | 219 | 0 | 35,840 |
| 4101 existing | SPAN NOOP_R64 interference | 188 | 0 | 35,840 |
| 4101 existing | SPAN REDUNDANT_R64 interference | 384 | 206 | 35,840 |
| 4101 existing | tail02_new R64 full path | 54 | 0 | 21,728 |
| 4101 existing | fresh R0 future window | 12 | 38 | 1,024 |
| 4101 prior-confirmation | SPAN NOOP_R64 interference | 298 | 0 | 35,840 |
| 4101 prior-confirmation | SPAN REDUNDANT_R64 interference | 407 | 234 | 35,840 |
| 4102 existing | prospective future window, each of R0/R8/R64 | 24 | 0 | 1,408 each |
| 4102 existing | SPAN REDUNDANT_R64 interference | 0 | 130 | 35,840 |
| 4102 existing | SPAN NOOP_R64 continuation | 8 | 93 | 10,080 |
| 4102 prior-confirmation | SPAN REDUNDANT_R64 interference | 0 | 131 | 35,840 |
| 4102 prior-confirmation | SPAN NOOP_R64 continuation | 4 | 66 | 10,080 |

For parent 4101, remembering more redundant-delay probe answers does not mean reliable behavior during the preceding delay. For parent 4102, the memory and continuation gains are real at these recorded units, while the prospective-task regressions show a separate preservation problem. The prospective response window itself has zero errors under either schedule; the reported harms are in its broader future window, which includes other targets. They do not establish a response-specific failure. All task families and all original error codes remain in the grouped outputs; no unobserved error mechanism was inferred.

Across all recorded changed positions in the matched comparison:

| Panel | Parent | Fixes | Harms | Different wrong answer |
|---|---:|---:|---:|---:|
| existing | 4101 | 413 | 2351 | 0 |
| existing | 4102 | 1163 | 122 | 23 |
| confirmation | 4101 | 127 | 670 | 0 |
| confirmation | 4102 | 319 | 12 | 2 |

This changed-position table has no both-correct denominator and includes descriptive R128. It is not an error-rate estimate. Excluding R128, existing-panel parent 4101 has 249 fixes and 819 harms, while parent 4102 has 453 fixes and 112 harms. Full grouped rows include the different-wrong cases rather than treating them as repairs.

## Preservation, acquisition and losses across the five stages

These histories cover the fixed diagnostic subset only: 194 paths / 13,952 scored events per parent/order on the existing panel, and 32 paths / 2,176 events on the prior-confirmation panel. Each path's index0 is unscored and excluded, exactly as in the original scoring. All 32 correctness patterns and all four adjacent transitions are retained, including zeros.

| Panel | Parent | Order | Wrong at 0 | 256 | 512 | 768 | 1024 |
|---|---:|---|---:|---:|---:|---:|---:|
| existing | 4101 | BLOCKED | 204 | 280 | 344 | 356 | 341 |
| existing | 4102 | BLOCKED | 0 | 0 | 0 | 0 | 0 |
| existing | 4101 | CYCLIC | 204 | 280 | 337 | 547 | 402 |
| existing | 4102 | CYCLIC | 0 | 0 | 1 | 0 | 0 |
| confirmation | 4101 | BLOCKED | 0 | 2 | 0 | 0 | 12 |
| confirmation | 4102 | BLOCKED | 2 | 0 | 0 | 0 | 0 |
| confirmation | 4101 | CYCLIC | 0 | 2 | 0 | 0 | 0 |
| confirmation | 4102 | CYCLIC | 2 | 0 | 0 | 0 | 0 |

For existing-panel parent 4101, CYCLIC's second short block introduces 210 wrong events and repairs none on this subset. The final long block repairs 145 and introduces none, leaving 65 of those midpoint-correct events wrong. Thus this subset does **not** support the simple story that the final long block erased recoveries achieved at768. No scored event has the pattern wrong512 → correct768 → wrong1024 in either order or parent on the retained subset. This does not rule out losses outside that subset.

At the existing-panel endpoints, parent 4101 CYCLIC loses 206 previously correct events, acquires 8 previously wrong ones, and retains 196 baseline errors; BLOCKED loses 145, acquires8, and retains196. Both retain the same196 always-wrong events across all five stages. Those unresolved cases are a second target alongside preservation. Parent4102 ends with no errors in the existing fixed subset under either schedule; its one CYCLIC midpoint error is repaired. The broader prospective-task harms therefore cannot be inferred away from this small subset.

On the prior-confirmation subset, parent4101 CYCLIC ends with zero errors; BLOCKED introduces12 in the last stage. Parent4102 acquires its two baseline-wrong events and retains them under both schedules. Whole-path results are separately preserved in the output tables. Endpoint categories partition their denominator; always-correct and transition-specific categories overlap them and must not be summed.

## A targeted curriculum hypothesis for the next preregistration

Question: can a single task-demand-balanced preservation curriculum retain the long-delay memory improvements without introducing delay-output and older prospective-task errors?

A minimal comparison would keep the CYCLIC schedule and total update/example budget fixed, with one unchanged CYCLIC control and one predeclared exposure-rebalanced curriculum for both parents. Before any run, define the training inventory structurally, not by selecting the inspected failing case IDs:

1. **Delay/interference stability:** represent no-op and redundant delay paths, plus the existing REBUILD family, with targets throughout the delay as well as the final memory probes. Retain all truth configurations and probe positions; do not overweight one token or inspected example.
2. **Older task preservation:** retain the existing prospective, fresh and tail task families, with matched cue/response and neutral/delay positions. Parent4102's prospective future-window errors make this a binding readout even though its memory probes improve.
3. **Unresolved acquisition:** include structurally balanced coverage of the source task families containing the always-wrong baseline cases, without copying the inspected test instances into training. This is a need suggested by the fixed subset, not proof that a particular objective will fix it.

Use a frozen training-only inventory to choose exact quotas and a single global rule; require an exact token-path disjointness check against all evaluated cases. Match total examples, updates, masks, reduction divisor, background processing, optimizer and learning-rate schedule. Do not combine changed loss weights or architecture with the first curriculum test. If exact task quotas cannot be matched within that budget, resolve and preregister the change before running. This proposal deliberately leaves numeric quotas and the resource allowance for that review rather than inventing a tuned ratio here.

Freeze an additional, structurally sampled unseen realization set before training and preserve the original panels as development checks. Retain the original primary and practical guards, separately report both parents and all task-family harms, and inspect intermediate histories without selecting a best checkpoint or a different order per parent. New realizations of the same templates would not establish a new semantic distribution. This is a proposed experiment only; no training or evaluation is authorized by this document.

## Verification, provenance and limitations

The analysis verified all178 retained original files against the recovery receipt before and after calculation. Independent code checked all36,960 matched memory rows,840 memory groups,14,848 retention pattern rows,464 stage-margin rows,1,856 transition rows,464 category rows,887 swap groups,506 error groups and590 paired window rows. It also reconciled800 original full-path/all/cue stage rows and640 transitions. Narrower retention-window masks are absent from the compact records and were not reconstructed.

A draft initially included unscored index0; independent review caught this. The draft was rejected, the correction is recorded, and current counts use only positions1..n-1. All904 excluded index0 entries were correct at all five stages. A phase-specific category name was also replaced with the neutral wrong512_correct768_wrong1024 because stage512→768 is LONG for BLOCKED. Neither correction changes scientific criteria; originals remain immutable.

This is a partial documentary recovery. Earlier cloud study bodies, original raw arrays/checkpoints, native runtime dependencies and some post-upload original closure records are unavailable here. No absent record or result was reconstructed. Original timing and logging stops remain failures; the verified recovery's scientific status is retained separately. The supplied compact data supports rerunning this saved-data analysis, not reproducing the original training or raw-array audit. No causal mechanism, significance, population generalization, independent training replication, fresh confirmation or adoption claim is made.

## Public release scope

The six files in this study batch form an owner-authorized public saved-data analysis release for NSS-Research. They include a self-contained input subset and a reviewed portable analysis export. The owner authorized publication on16October2026: research prose, data and metadata under CC BY4.0, and the two analysis scripts under MIT. Licensor: AegisAgentAscalon. This scope does not convey rights to private checkpoints, third-party packages or missing materials. Repository license notices and per-file catalog mappings provide the applicable terms.

The original proposal is preserved privately. Only approval/license markers were finalized for this release; scientific results, criteria, source code and saved data are unchanged. Original frozen planning documents inside the source archive retain their historical no-publication wording; the current release manifest records the later authorization. Publication execution and remote-commit verification are handled separately.

The older combined six-file candidate is not part of this release. It needs48absolute runtime-path occurrences in46nested local result values cleaned, plus its archived copy and an operational transport path. The present batch avoids that combined local lane and excludes delivery identities, operational receipts, private approval text, raw checkpoints, native dependencies and rejected draft outputs.
