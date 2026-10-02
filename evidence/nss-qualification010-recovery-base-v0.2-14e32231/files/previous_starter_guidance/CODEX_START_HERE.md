# First Codex assignment: recover Qualification010 as a new, auditable release

## Mission

Reconstruct the missing **NSS / NBR-01 Qualification010** study from verified Study009 inputs and the three surviving Study010 documents. Work in a new candidate directory/branch, not inside the immutable starter or an accepted study. Do not produce a lookalike archive with invented historical evidence. Suggested identity: `NSS_NBR01_Qualification010_Reconstruction_v0.2`.

Use the user's selected Astra/Ultra configuration where it is actually available. Inspect the installed client and permissions rather than assuming a model identifier or unlimited agent capacity. Parallel delegation is useful, but this work order does not itself change account settings or buy compute.

## Read in this order

1. README.md and AGENTS.md.
2. historical_qualification010/REPORT.md.
3. historical_qualification010/NBR01_STATUS_REVIEW.md.
4. historical_qualification010/NSS_NBR01_Qualification010_v0.1_DELIVERY_VERIFICATION.json.
5. audit/PARENT009_ARCHIVE_AUDIT.json and audit/PARENT_SUBSET_PROVENANCE.json.
6. RECOVERY_SPEC.md and TEAM_WORKFLOW.md.
7. Relevant actual source under reference/parent009/; in particular nbr009/state.py, nbr009/readout.py, nbr009/stage_b.py, and the parent006 model/data definitions.

## Initial parallel assignments

- **Source/contract researcher:** map inherited functions and checkpoint hashes to every recoverable reported requirement. Produce RECOVERY_MAP and MISSING_DECISIONS. Read-only on references.
- **Implementation owner:** propose the smallest new Study010 module layer, training recipe, task-adapted attention reader and explicit resume state. Implement only in the new candidate tree.
- **Measurement reviewer:** derive evaluation and independent scoring from the declared task/source events. Review leakage, unknown/missing metrics, whole-store integrity, chronology, pairing and resource boundaries. Own test specifications/scorer in an isolated area.
- **Reproducibility/release reviewer:** test fresh extraction, checkpoint reload, deterministic state/RNG continuation, portable execution, artifact partitioning and reconstruction lineage. Initially this role can run after implementation instead of consuming another concurrent worker.

The coordinator resolves disagreements with source evidence and explicit decisions, not a majority vote. Return one consolidated report with pointers to each worker's output.

## Phase 1 deliverable: audited reconstruction plan and runnable parent smoke checks

Run the starter verifier and 45 parent tests, load all five inherited families, record installed dependencies and hardware, compare local files to the starter hashes, and search the user's specified project folder for any genuinely recovered Study010 code/checkpoints. Match an alleged original full archive against the historical hash before using that label.

Produce a source-to-target map, unknowns list, proposed frozen configuration and measured compute/storage envelope. Do not fill missing architecture details or acceptance cells silently. Optional local implementation/unit tests are appropriate; no full multi-fit launch until the budget is explicitly resolved. If actual Study010 files are found later, preserve them and compare rather than overwrite the new work.

## Phase 2 and 3, after the scoped plan/budget is agreed

Rebuild missing functionality; demonstrate visible-fact competence in development; freeze source, data generator, job list, thresholds and resource limits; execute the declared comparison with all seeds retained. Compare to the historical report after scoring, while reporting uncertainty and all deviations. A new main test set should be distinguishable from development and from any recovered historical set.

Separately implement an independent scorer from actual source events and candidate stores. Replay all main configurations from checkpoint in fresh interpreters; rederive summaries; test state/RNG/transaction/mid-query continuation; reproduce one full training trajectory under the measured compatible environment. Preserve negative close-identity, novelty and corruption cases. Failing broader cases must not disappear because the nominal scope passes.

## Completion boundary

A downloadable, locally persisted new release with source/config/seeds, actual checkpoints, raw results, costs, new verification receipts and a historical-versus-new comparison. It may pass or fail the new declared scope; both are legitimate results. Do not report full recovery until the delivery verifier can restore and check the actual files. No automatic move to NBR-02.
