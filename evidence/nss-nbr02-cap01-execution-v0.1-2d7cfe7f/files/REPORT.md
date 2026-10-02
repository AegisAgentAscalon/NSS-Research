# NSS NBR02 CAP01 — Cross-segment capability frontier report v0.1

**Disposition: COMPLETE_BOUNDED_CAPACITY_DIAGNOSTIC.** All488 planned executions completed. The new executor finishes exact reader computations beyond the old simultaneously-resident closure limit, with zero class or numerical-equivalence failures. Ordinary multi-pass retrieval obtains the same answer capability as the hierarchy-grouped segmented manager. HSA retains a strong but bounded advantage over the retained dense readers; some larger layouts expose learned errors despite complete evidence access. This is neither a universal segmentation win nor a disproof of expanded-context capability.

**Training:** zero optimizer applications, zero new fits, zero downloads. All six source model states remain unchanged. The original interrupted fourth HSA fit remains untouched. Source and fixture lock precedes main execution.

## 1. What changed from SC02
SC02 required a task's entire original two-layer input closure to fit its active-row allowance. CAP01 instead carries an unfinished attention calculation across bounded key tiles and stores layer results externally. It retains ONE softmax across the entire allowed neighborhood. It does not discard distant keys, average independently computed segment answers, change dependencies, or supply oracle answers.

Both ordinary and segmented managers receive this ability. Ordinary groups consecutive queries; segmented groups queries with identical hierarchical neighborhoods. Both have complete index access, identical current evidence, multipass inference, external stage files, and checked interruption/resumption. The distinction is a tested concrete grouping policy, not a categorical claim that retrieval cannot maintain progress.

The reader remains a37-feature,18,500-parameter, two-block trained maintenance classifier. Its rule is unchanged: global freeze -> DEFER; own completion -> COMPLETE; otherwise READY only when both declared prerequisites are complete, else BLOCKED. Source revisions and an existing global override are tested; no new semantic exception or transitive rule was secretly given to the model. Receipt/constraint fields remain distractors. An exact ordinary-code scorer is a ceiling/control.

## 2. Frozen workload and comparators
Primary:432 cases =3 task counts(8/32/128) ×2 base worlds ×3 scenarios ×2 snapshots ×3 paired model seeds ×2 reader types ×2 managers, cap32. The three scenarios reuse a base world: dispersed prerequisites, global override, and revised dependency after interruption. Thus six random base worlds underpin the primary scenario grid, not432 independent worlds.

Stress:24 cases at512 tasks, one base world and only paired seed8801. Separate tile-size sensitivity:32 cases, two additional base worlds at128/512, cap16/64, seed8801. Total488 cases and3,904 repeated task-answer observations. All case IDs, fixtures and generation seeds are retained. No cases were dropped or tuned after main execution.

The dense fits were already weaker on their original training task. They are source-matched fixed-budget comparators, NOT a best-tuned dense baseline. A new matched large-context training comparison would be needed before assigning all generalization differences to architectural limits.

## 3. Capability results — non-frozen decisions
The table excludes the easy all-DEFER snapshots. Ordinary and segmented management have IDENTICAL class results; do not double the evidence by counting both as separate capability replications.

| Source task count | Total encoded positions | Dense correct | HSA correct | Dense entirely correct jobs | HSA entirely correct jobs |
|---|---:|---:|---:|---:|---:|
|8, primary|36|204/240 (85.000%)|240/240 (100%)|6/30 (20%)|30/30 (100%)|
|32, primary|135|225/240 (93.750%)|240/240 (100%)|15/30 (50%)|30/30 (100%)|
|128, primary|524|188/240 (78.333%)|235/240 (97.917%)|3/30 (10%)|25/30 (83.333%)|
|512, separate one-pair stress|2,072|16/40 (40%)|35/40 (87.500%)|0/5|0/5|

Each job comprises eight selected target decisions, NOT all tasks in the archive. The128 row therefore does not mean that all128 tasks were jointly solved. Task count changes the available context and distractor/dependency population. It does not increase the number of prerequisite hops in the learned rule.

With frozen snapshots included: dense/HSA correct were252/288 vs288/288 at8;273/288 vs288/288 at32;236/288 vs283/288 at128;24/48 vs43/48 at512. These easy override cases are not allowed to conceal prerequisite-reading weaknesses. Per-class confusion matrices and per-parent rows are in `results/SUMMARY.json`.

The descriptive working-point criteria were >=95% decision accuracy, >=90% represented-class macro recall and >=90% wholly correct jobs. The HSA primary8/32 points meet them. The128 point retains high answer accuracy but misses the whole-job target. The512 stress point misses them. This is a bounded observed frontier for the listed worlds/weights, not a universal maximum task count.

## 4. The larger-context execution boundary really moved
| Task count | Full encoded positions | HSA single-target original closure range | Active primary tile cap |
|---|---:|---:|---:|
|8|36|30–36|32|
|32|135|69–96|32|
|128|524|218–260|32|
|512|2,072|602–755|32|

For32 tasks and larger, no selected target's complete original HSA closure fits32 positions. Original dense resident inference requires the full input collection and also exceeds32. The resident-packet controls therefore cannot admit these complete computations. Both main streaming managers finish them without truncation, at the original numerical quality.

This is a demonstrated expansion of executable input reach under an ACTIVE RECORD TILE budget. It is not a total-memory reduction, a fixed32-token language context, or proof of unique superiority to ordinary multi-pass retrieval. The ordinary streaming comparator already implements the central cross-segment carry mechanism too.

At512 tasks, the executor can work through2,072 encoded positions without simultaneously feeding them all into attention. It does not store2,072 positions' worth of task meaning in a magical32-position neural state: it rereads file-backed evidence/intermediates and retains the partial arithmetic needed to combine those reads.

## 5. Where the learned failures are
HSA's five primary128 non-frozen errors all involve parent8802 and target124, repeated across source scenarios/snapshots. It declares READY when at least one prerequisite remains incomplete. They are NOT five independent discovered defects. The512 stress likewise repeats one target386 failure for parent8801 across five non-frozen jobs. Full resident references make those same errors.

Therefore these specific misses are not missing information introduced by the new segment executor. The model still cannot always interpret its available evidence correctly in the larger layouts. This does not establish the internal cause: insufficient large-context preparation, address binding, attention dilution and other mechanisms have not been isolated by interventions.

The separate sensitivity world is an important limitation on monotonic claims. At128, seed8801 produced14/16 correct decisions at each of cap16 and64 (no fully correct eight-target job). At512, it produced16/16 at EACH cap on the other new world, despite its87.5% non-frozen result on the primary stress world. These are different random layouts and only two snapshots each; they do not reverse or replace the unfavorable stress outcome. The results are layout-dependent and too small to certify a general512-task frontier.

`failures/BEHAVIORAL_CASES.json` preserves erroneous tasks, actual source prerequisites/progress, logits, same-weight reference logits and source identities. No post-result training or repair was applied.

## 6. Numerical and lifecycle outcomes
All488 cases completed and all3,904 class decisions matched full same-weight reference execution. Across computed first-layer rows, selected second-layer rows and logits,4,078,784 scalar comparisons had zero violations of the original float32 envelope `2e-5 + 2e-5*abs(reference)`. Maximum absolute difference was1.04904175e-5; maximum error/tolerance ratio0.190267. These are repeated numerical comparisons, not independent tasks.

All244 ordinary-versus-segmented policy pairs preserved decisions and passed the same numerical envelope. Reorganization did not add a hidden accuracy benefit. Stored output probabilities/logits are not calibrated reliability guarantees.

152 cases paused after seven key tiles and resumed from checked JSON plus stage files. All76 old-snapshot attempts against revised evidence were explicitly rejected. The changed snapshots then ran from a fresh binding; this is safe rejection/restart, not selective state migration.14 representative paused checkpoints retain their original spool files for replay.

Engineering passed29 cases:16 full/stream/resume numerical cases and13 invalid-input/fault controls. Forty selected final cases reproduced bit-for-bit in fresh processes, as did all14 retained interrupted computations. An independent scorer recounted all488 results with zero discrepancies;244 paired policy comparisons and all41 source/fixture-lock entries were checked. These are bounded internal verification, not third-party replication or production crash-recovery qualification.

## 7. Cost of buying capacity
The full-capacity mechanism adds passes, storage and validation; it is not a free context extension. Representative FIRST-snapshot dispersed jobs below use seed8801 and the segmented grouping policy. Timing is a single observed execution, not a repeated speed benchmark; models/connectivity differ.

| Tasks | Dense score cells | HSA score cells | Dense core seconds | HSA core seconds |
|---|---:|---:|---:|---:|
|8|3,168|1,456|0.0124|0.0215|
|32|38,610|4,398|0.0419|0.0253|
|128|557,536|12,010|0.5097|0.0821|
|512|8,619,520|28,316|6.4958|0.1558|

Score cells include heads and selected union-key tiles, including masked cells within a group. These are actual counts in this executor, not total FLOPs. HSA can avoid connections already absent from its declared graph; it does not drop new edges to make the timing look better. Smaller cap16 tiles finish with matching outputs but more passes than64 on the same sensitivity fixtures. Those are capacity/compute tradeoffs, not learned improvement from a smaller tile.

Main execution cores summed to211.841 seconds; synchronous runner receipts summed to231.615 seconds. Full-reference scoring, analytical resident-admission checks and some study bookkeeping are outside the per-case core; reference timings are recorded separately. Preflight, audit, preparation and report production are additional. Zero optimizer applications occurred.

At cap32 the maximum counted live tensor payload at the attention accounting point was17,936 bytes. This is a PARTIAL named-tensor measurement, not peak allocation or total working memory. Encoder outputs, model parameters, graph indexes, allocator workspaces, retained Python metadata, file spools and OS cache must not disappear from accounting.

Source + embedding + two stage arrays occupied19,664/72,332/279,280/1,102,816 bytes at8/32/128/512 respectively. Individual resume envelopes were1,791–2,381 bytes plus those referenced arrays. Main process peak RSS was383,250,432 bytes and includes full-reference work and framework overhead; per-policy isolated RSS was not established. The complete source compiler is not constrained to32 raw rows while ingesting an archive. The active cap governs the neural tile after ingestion.

## 8. Operational and evidence boundaries
The container rejected an attempted interactive-session invocation before execution. No scientific work or files were produced by that invocation; it is logged. Main work was then deliberately split into synchronous, nonoverlapping case ranges. No main caller timeout, skipped case, sample replacement, uncertainty about optimizer steps, or scientific gate relaxation occurred.

Archive integrity checks verified all906 SC02 and140 SH01 input-manifest payloads. Six compact inference files preserve exact state tensors from the retained final checkpoints. Source lineage is in `provenance/INPUT_AUDIT.json`. Main code and fixtures were frozen before main results. Post-result recount/report scripts are separately included rather than silently added to the prospective source lock.

Every main case retains target labels, predictions, streamed/full-reference logits, stage comparison statistics, resource counters, source identity and status. All per-stage arrays are not retained for every successful case; they can be recomputed from the saved source/models/fixtures. Selected original paused spools are retained. Failed behavior evidence is not erased by clean arithmetic.

## 9. Assessment and next implication
1. **Yes: cross-segment computation expands executable context reach under a fixed active tile.** Computations that needed69–755 input positions per HSA target can finish using32-position tiles.
2. **Yes, bounded: HSA uses the larger accessible evidence well on some layouts.** Primary32-task results were perfect on this small grid;128-task answer accuracy remained97.917% outside freeze cases.
3. **Not established: unique capability from custom segmented grouping.** The fair ordinary streaming comparator matched each reader's decisions. Shared persistent arithmetic is doing the capacity work.
4. **Not established: broad reasoning or universally reliable large context.** The same known rule was tested, and both128/512 include failed whole jobs. More evidence access does not automatically produce better interpretation.

The next scientifically distinct question is whether a properly prepared learner retains high accuracy across MANY larger, diverse dependency layouts, and whether its working records can support genuinely new multistep maintenance. That would require prospective tasks and matched training/retention controls. No such next experiment is run or implicitly authorized here. Current results do not qualify natural-language context, a25,000-token budget, DARP, generated summaries, autonomous night learning/repair, companion identity, or an overall NSS successor architecture.

## Files
- `PROTOCOL.md`, `SOURCE_FIXTURE_LOCK.json`, `CASES.json`: frozen definition and identities.
- `source/cap01.py`, retained source modules: working implementation.
- `fixtures/`, `checkpoints/`: exact inputs and six final reader states.
- `results/cases/`, `results/SUMMARY.json`: complete main observations.
- `results/paused/`:14 original interrupted calculations.
- `results/RECOUNT.json`, `REPLAY_*.json`, `RESUME_AUDIT_*.json`: internal audits.
- `failures/BEHAVIORAL_CASES.json`: supported failure observations.

Historical SH01/SH02/SC01/SC02 and other NSS results remain unchanged.
