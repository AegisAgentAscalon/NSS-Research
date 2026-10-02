# Codex review handoff — CAP01 v0.1

## User intent
The user clarified that segmented context plus HSA is primarily intended to expand NSS maintenance capability, not merely lower milliseconds. They authorized the proposed capability-oriented test. No subsequent training/architecture run is authorized by this delivery.

## What ran
488 new inference cases; six exact retained dense/HSA final models from SH01 seeds8801/8802/8804. Three-level graph,37 features,18,500 parameters unchanged. New executor streams ONE softmax across key tiles and preserves layer results externally. Both ordinary and hierarchy-grouped managers get this feature, exact retrieval and JSON-resumable partial computation. Main cap32 is an active neural record tile, not total memory. Zero updates/downloads/new fits.

Primary432 cases at8/32/128 tasks, six base worlds reused across three scenario families and two revisions.512-task stress24 cases uses one base world/one paired model seed. Additional tile16/64 sensitivity32 cases uses two different worlds. All results present.

## Headline findings
-4,078,784 stage/logit comparisons:0 tolerance violations;3,904 repeated task observations:0 class differences versus full same-weight reference.
-32 tasks/135 encoded rows: HSA240/240 unfrozen decisions and30/30 eight-answer jobs while the old single-target closure required69–96 rows, exceeding cap32.
-128 tasks: HSA235/240 unfrozen decisions and25/30 whole jobs; dense188/240 and3/30. HSA's five misses repeat parent8802/task124, incorrectly READY. This is not five independent faults.
-512-task single-world stress: HSA35/40 unfrozen decisions vsdense16/40, but all five unfrozen jobs have an error (same HSA target386). Another512 sensitivity world is16/16 per tile condition. Do not claim monotonic maximum context, broad512 competence or adequate sample size.
-244 ordinary/segmented policy pairs have the same classes and admitted numerical agreement. The custom grouping did not add a capability advantage over fair ordinary streaming.
-152 pauses resumed;76 revised-source old checkpoints rejected.40 fresh final replays and14 saved partial resumes bit-exact.488 independent recounts;41 lock entries unchanged.29 preflight cases passed.

## Questions worth auditing
1. Does the executor preserve the original joint softmax and simultaneous two-layer semantics, including masked tiles with no valid keys for one query?
2. Are the active-tile cap, source/activation spools, global index metadata and full-reference memory reported distinctly enough? All-world ingestion is outside the neural tile cap; OS page caching remains possible.
3. Is the ordinary baseline fairly given all multi-pass/continuation information? It shares the capacity mechanism and should not be called an inferior single-pass baseline.
4. Do the label/class/whole-job tables avoid multiplying evidence across scenario revisions, policies and tile sizes? Larger source population is not a longer novel reasoning chain.
5. Is the dense preparation caveat prominent? Same historical fixed-budget training is not equal source competence, optimized dense scaling or proof of a dense architectural limit.
6. A next candidate would need a broader large-layout training/evaluation curriculum and retained small-layout tests, not automatically more hierarchy levels or another cache. Genuine multi-step maintenance would require new task semantics and suitable reader preparation; it was not tested here.

## Original boundaries retained
No SH01/SH02/SC01/SC02 gate is edited. Incomplete8803 remains incomplete. No natural-language token budget, DARP, learned summarizer, autonomous repair, next-day identity or whole-NSS architecture was qualified. The fixture can be solved exactly by ordinary code; harness behavior is not claimed as learned intelligence.

The full ZIP contains exact fixtures, six compact checkpoints, main observations and original paused spools. The review ZIP intentionally omits the checkpoints, bulk cases and spool arrays. Numerical full-stage arrays are regenerable rather than retained for every successful case; recorded comparisons and every final target logit remain available.
