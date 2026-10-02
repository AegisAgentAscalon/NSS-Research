# NSS CM-01 execution v0.2

Read REPORT.md for results and limitations, and ALWAYS_RESIDENT_ADDENDUM.md for the proposed architectural interpretation. STATUS.json separates completed work from unrun candidates.

This is the complete evidence package for the **new bounded CM-01 study**, not a complete Q010 archival replacement. No old model/archive ZIP is duplicated.

## Integrity

Run `python VERIFY_STUDY.py` after extraction. It checks all manifest-listed files without loading models or running experiments.

## Tables

- results/main/HELDOUT_PAIRED.csv: all five held-out families and all three roles.
- results/main/FULL_GRID.csv: every split/family/model seed/role/arm/stratum/subtype/noise cell.
- results/main/DECISIONS.csv: all 23,040 main interface decisions.
- results/main/CONTROLS.csv: all 1,024 main non-neural control decisions.
- results/main/NEGATIVE_OUTCOMES.csv: all 10,571 incorrect main learned-interface decisions. Incorrect controls remain in CONTROLS.csv.
- results/fixture/: corresponding eight-case integration-fixture evidence and outcomes.

B/C are encoding controls, not independent learned models. Count unique episodes and model repetitions separately.

## Complete new raw evidence

raw/fixture and raw/main each contain capture_run and replay_run. Inputs contain public numeric arrays, observable journal, and a separate protected.jsonl truth ledger. The inference producer is blocked from opening that ledger. Capture folders retain numerical outputs, transition traces, routing, controls, model identities, costs and attempt counts. Replay is a deterministic fresh-process rerun, not extra scientific sample size.

## Dependency and reproduction

The existing Q010_InferenceRecovery_v1.6_RecoveryContext.zip is required for model inference. Expected SHA-256: `9ac2801dc9a67ce3d7fbea5d4f79281b66176e961488fbffb6bf9c660056279e`.

Extract it, verify it with its VERIFY_CONTEXT.py, and use REPLAY_STUDY.py for a separately logged future local reproduction. Consult `python REPLAY_STUDY.py --help`. The historical source/run_stage.py intentionally refers to the original study clock; it is retained as execution evidence, not the future-run driver. Do not rerun source/prepare.py or change the locked protocol.

The current package already contains exact local CPU replay results. A future backend/version/host may differ; do not alter numerical tolerances to force a pass. requirements_snapshot.json records the actual library versions; it is a version record, not an instruction to replace your environment.

Historical missing training evidence and old verifier errors remain. See REPORT.md and provenance/. CM-02–05 were not automatically executed.
