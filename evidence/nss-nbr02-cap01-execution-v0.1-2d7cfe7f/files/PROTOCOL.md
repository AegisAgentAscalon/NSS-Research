# NSS NBR02 CAP01 — Cross-segment capability frontier v0.1

## Purpose and authorized scope
User authorized testing expanded maintenance capability, not merely execution speed. This first pass distinguishes execution reach beyond a complete-input/closure admission cap from the retained learned readers' ability to interpret that information. This is a new exact multi-pass inference executor, not unchanged SC02. Zero training, model downloads, output architecture changes or automatic follow-up runs.

## Frozen comparison
Preserve the three completed SH01 paired final models (8801/8802/8804), 18,500 parameters, 37 typed features, two attention blocks and original three-level task/region/global hierarchy. Each dense/HSA model retains its trained weights and connectivity. No refit, seed selection, extra training or depth change. The interrupted fourth HSA fit remains unfinished. Dense source-task fitting was weaker; this is not a best-tuned dense comparison.

Cross ordinary tiled retrieval versus hierarchy-grouped segmented execution with dense versus HSA readers. BOTH managers have exact identity lookup, public dependency links, multi-pass attention, file-backed intermediates, progress and checked JSON resumption. Ordinary uses groups of up to four sorted query rows; segmented groups up to four rows with identical key neighborhoods. Both compute exact backward closure, use the same key order and can do multiple passes. This does not establish a categorical distinction between ordinary retrieval and segmentation.

Retain running softmax maximum, denominator and weighted-value sum over key tiles: ONE joint softmax across all allowed keys, not an average of independently normalized segment outputs. No pruning, summary substitution, label-conditioned selection or changed layer ordering. Layer outputs are file-backed; global graph metadata is in RAM. Source and intermediate spools are outside the active tile and charged separately. File backing does not limit OS page cache or total RSS.

## Task and episodes
The unchanged learned rule: freeze -> DEFER; own progress complete -> COMPLETE; otherwise both prerequisites complete -> READY, else BLOCKED. Identity, two prerequisite IDs, source fields and hierarchy are supplied. Constraint/receipt fields remain distractors. No new semantic exception or transitive reasoning rule is introduced.

Three families: cross-region dispersed prerequisites; global freeze override; dependency revision after interruption. Two source snapshots per episode: the second flips prerequisite progress, activates the global override, or replaces one prerequisite respectively. Eight targets sampled independently of labels. Each eight-target decision vector is a maintenance job. An old interrupted computation must reject a revised source then restart under the new one; this is conservative restart, not selective migration.

Primary: n=8/32/128, two fixed base seeds per size, three families, two snapshots, three model seeds, two readers, two managers, cap32 =432 cases. Families reuse base worlds; six randomized base worlds underpin primary scenarios. Repeated targets/snapshots/policies are not independent replications.

Stress: n512, one base seed, three families, two snapshots, seed8801 only, both readers/managers, cap32 =24 cases. Not three-model confirmation at512.

Tile sensitivity: n128/512, one separate base each, dispersed family, two snapshots, seed8801, both readers/managers, cap16/64 =32 cases. TOTAL488 main cases,3,904 task observations counting repeated arms. Seeds and generator are pinned in source/fixtures.py. No replacement worlds or post-result tuning.

## Outcomes and controls
Primary: decision/whole-job correctness, class confusion, false COMPLETE/READY, coverage, numerical parity, dependencies and resource use. Report non-frozen cases separately. Descriptive usable operating point: >=95% decisions, >=90% macro recall over represented classes, >=90% exact eight-answer jobs. A miss never suppresses a case. No probability thresholds are tuned.

Resident-packet control: compute original dense full-input and HSA per-task complete backward-closure sizes; mark above-cap inputs unadmitted rather than truncate them. This admission-only control is NOT the strongest baseline: both main ordinary readers may stream beyond that boundary.

Exact symbolic control independently evaluates the known rule. It is a software ceiling and source of labels, not input to neural execution. A full same-weight neural computation provides stage/logit references OUTSIDE the cap experiment and its timer. There is no trained novelty, language-token or genuine agent-maintenance claim.

## Resource contract
Cap counts query plus key record positions (or initial encoder input tile), not every simultaneous tensor or total memory. At most four queries plus cap-minus-query keys. Separately count visible tensor payloads, score cells, rows read/written, archive/activation spool bytes, checkpoint bytes, graph index volume and process RSS. Full reference has additional uncapped memory. A case permits <=500,000 key tiles; main/audit process cap900s, RSS2GiB, evidence guard240MiB within256MiB with16MiB failure reserve. No optimizer initialized or stepped. Elapsed times are secondary single-execution costs, not repeated benchmark superiority measurements.

## Numerical, interruption and integrity checks
Float32 envelope unchanged: abs(error)<=2e-5+2e-5*abs(reference). Compare computed block1 rows, requested block2 rows and logits to full source SH01 arithmetic. Exact argmax parity is separate. A violation makes that case diagnostic; class parity cannot rescue it. Retain all counts and up to eight full numerical failure payloads to bound capture costs. Reference arithmetic is separate code path, not external replication.

Resume-family cases stop after seven processed key tiles, save partial softmax accumulators/cursor and source/spool/model hashes, restore and finish. Old snapshots must reject changed sources. Preserve selected paused files. Detect changed model/mode/scope/budget, corrupt spools/checkpoints/accumulators, invalid cursors/targets, nonfinite sources and inadequate tile budgets. Checksums detect accidental corruption, not an attacker replacing data and checksums. Fresh-process audit reproduces selected complete cases and paused checkpoints.

Implementation and engineering may be repaired before main freeze with failure evidence retained. No source/criterion changes after main lock. Main cases write atomic result files and an attempt journal; interrupted calls may execute ONLY missing cases with the same source and fixtures. Failed cases remain visible. No historical gate is changed.

## Interpretation
Capacity gain is completion beyond the old resident gate, with numerical parity and separately adequate learned behavior. Both ordinary and segmented managers may gain equally. HSA's structural bias may improve its decisions and reduce interactions, distinct from a segmentation interaction benefit. Exact execution reorganization should preserve existing answers, not invent a new neural capability. This pass does not test new rules, natural-language context, learned segmentation/summaries, cross-night learning, transitive reasoning, discovery of exceptions, or identity retention.
