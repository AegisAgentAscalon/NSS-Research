# Codex handoff — complete NBR02-DC01 v0.5; analyze before new candidates

The user requested repairing the storage stop and completing the full gated pass before another Codex review. The full run and full fresh adaptive replay are now complete. Read REPORT.md, scores/DECISIONS_AND_SUMMARY.json, CANDIDATES.md, and ARCHITECTURE_EVIDENCE_UPDATE.md. This handoff requests critique/proposal work, not automatic further fitting or a phase transition.

## Result and failure evidence

A0 passed4/4 in both exact-gradient G and approximate-eligibility L. At delay0, primary POST-receipt/reset performance is G302/320=94.375%, L301/320=94.0625%; own-initial frozen controls224/320; causal exact X80/80 unique occasions. Four fits repeat80 query occasions; delays are invariant repetitions. D1, D2 for both learners, and D3 the predeclared small-sample L-noninferiority screen pass. All old-cue endpoint classifications remain correct512/512 per learner, but old-cue log loss increases from~.00236 to.01618/.03879.

Every held-out learned post-feedback error is the FIRST corrective receipt after reversal: G14/32,L13/32 correct, then both32/32 after the next receipt. All37 delay0 misses have correct receipt binding, retained state, rule-specific gradients and update arithmetic; loss decreases but class remains wrong. All32 first-reversal gradients/arm are clipped (raw normsG5.20–6.99,L5.87–7.61,clip1). This suggests, but DOES NOT PROVE, a correction-dose explanation. Inspect scores/FIRST_REVERSAL_FAILURES.csv. Before-feedback mean loss is worse than own frozen controls despite better classification: G.7148 vs.5682,L.7247 vs.5862, due expensive confident reversal surprises. Do not replace raw predictions with post-feedback answers.

The local equation has mean encoder-gradient relative discrepancy~.7668 and cosine~.6468 against exact math at L's OWN pre-update weights, while passing this small task's performance screen. Approximation is not a formula bug or a76.68% task error. Three upstream transitions plus detached waiting, explicit single receipt and fixed pending weights are narrow; global cue coordinates already identify scope. Broad causal credit, concurrent pending updates, old-parameter gradients and superiority to exact bookkeeping remain untested.

## Repair, verification and costs

Live numerical code/equations/seed/task/scoring were unchanged; v0.5 changes engineering cost admission and delivery only, plus reduces local limits to carry prior work. Whole-envelope XZ forecasts62,694,619bytes instead of the old92,784,897 with the same2x margin. No copied209MiB proof; component counts and actual encoded capture are separately audited. Full replay matches42,402frames,117,866arrays,29,728,572elements and27 stage CSVs.9,088total committed update attempts INCLUDE the240old stopped-prefix applications; cap9,800. No unknown completion or selected fits. Source/hash/readout checks and final delivery receipt define actual verification; this is internal replay, not third-party replication.

All3,238 query errors across primary phases are retained. The full ZIP restores every raw source/frame/score; the compact handoff does NOT independently verify numerical claims. Prior v0.4 remains stopped, not overwritten. Historical Q010 optimizer/RNG/training gaps remain.

No overall efficiency claim: essential L trace is2560bytes (2760including retained cue payload); G saved graph tensor storage contains540nonparameter bytes plus shared model buffers on this short graph. Native graph nodes, diagnostic copies and backing arrays complicate comparison. OBS-DC01-COST-001 documents that the inherited Python walker misses ndarray.base/native graph allocations. Fix that inventory before a memory-win claim; it did not change stored numerical arrays or measured process caps.

## Requested next review

Critique REV01 (single clip-factor intervention with strong old-knowledge and before-feedback probability checks), CAUSAL01 (earlier scope necessary, causal length separate from waiting), and conditional BLOCK01 (explicit block eligibility and all costs). Prefer one bounded discriminating test, not simultaneous changes to training, task, state and readout. Use the now-known errors for development/regression, not fresh confirmation. No reserve-budget fits or unrequested parameter search. Any result with a larger step must retain its stability costs.

## Program status — do not omit

NBR-01 is CLOSED_BOUNDED_RECOVERED_EVIDENCE under the adopted decision, not pending or broadly qualified. NBR-02 is ACTIVE, with a completed bounded DC01 result pending review; no automatic closeout or NBR-03 run. RET-MW01-FIT-001 remains PARKED_OPEN: maintained tokens support information management, but the earlier derived-progress repair was not qualified. FCR-0103-001 requires revisiting residual01–03 foundations after03 and before04. Keep all G01–G22 in protocol/PROGRAM_CONTEXT.md; its proposal-status paragraphs are historical snapshots superseded here, not grounds to revert NBR-01 closure. Parent Architecture Ledger and frozen core-role boundaries remain unchanged.
