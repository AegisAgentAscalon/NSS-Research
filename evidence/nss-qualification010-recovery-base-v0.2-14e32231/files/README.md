# Qualification010 Recovery Base v0.2

**Status: verified original parent bytes + newly tested recovery helpers. NOT the lost Qualification010 release, not a complete reconstruction, and not requalification. No training was run.**

## The important recovery

The inherited compact reader selected by the historical Qualification010 report was not newly trained in that study. All five `record_hop_801` through `record_hop_805` checkpoints survive byte-for-byte inside Study009. The 009 owned-record store, catalogue/identity machinery, internal maintenance, exact traversal and inherited reading source also survive. We can restore this foundation without retraining its weights.

What remains missing is the original 010-specific source and protocol, its 15 NEW main checkpoints (ordinary reader continuations, close-identity continuations, and the task-adapted attention stack), development artifacts, full scoring/evaluation implementation and raw main evidence. A trained 009 binder is not an 010 reader continuation. Similar parameter counts are not evidence of interchangeability.

## What changed since the previous starter

The previous 4.22 MB starter already contained 129 exact parent files and these inherited weights. This v0.2 package does not claim newly discovering those checkpoints. It turns the starting point into a more inspectable and executable recovery base:

- 134 exact parent source/checkpoint/calibration/specification files, with member-level provenance.
- A 35-checkpoint tensor inventory with names, dimensions, dtypes, parameter counts and file hashes. Five are the selected compact-reader checkpoints; the others are earlier controls/learning components, not the missing 010 weights.
- A source-symbol index and source-to-target recovery map.
- A structured transcription of the historical training recipe plus a 15-job ledger with absent outputs explicitly null.
- A new, labelled cap-only adapter implementing the report's 80-to-20000 limit change without changing learned values; tested against the original forward calculation at cap80.
- New limited smoke checks that actually exercise the inherited reader, cap-only variant and exact control across all five pairs. They do not claim original 010 replay.
- Ten new recovery tests, the unchanged 45-test parent suite, and a manifest verifier with exact fresh-smoke replay.

## Use on your laptop or in the selected research workspace

Extract into its own directory inside `MegaMind_Alpha_Proto`. Do not merge it into Study009 or overwrite the original starter. `RECOVERY_PROGRESS.md` gives the finding; `RECONSTRUCTION_MAP.md` identifies the missing work; `CODEX_START_HERE.md` is the handoff.

Python 3.11+ is needed for the standard-library verifier as written. Neural checks require the already-installed parent dependencies (`reference/parent009/requirements.txt`). No command installs dependencies or accesses a network.

```text
python -B verify_recovery.py
python -B verify_recovery.py --parent-tests --recovery-tests --replay-smoke
```

A replay mismatch on a different numerical environment needs investigation; it is not automatically proof of archive corruption. The independent manifest-only check separates file integrity from environment-dependent execution. Tested here on Linux CPU, not on the user's laptop or Windows. Some preserved full-parent evaluators still use Unix-only resource telemetry; the limited smoke does not run those evaluators.

## Status boundaries

`historical_qualification010/` contains unchanged original reports/receipt. Their PASS labels are historical, not new results. `reference/parent009/` contains immutable original bytes. `recovery/`, `scripts/`, `tests/` and the new specifications are new recovery work with declared limits. `audit/reference_smoke/` is new recovery evidence, not Study010 main evidence.

The original 010 archive is identified historically by 302,820,867 bytes and SHA256 `0d8a0e01cc89e9b221a16939a7ebaacd58fd3ed02cbf3fe0e8e64b7429f2d5fe`. A rebuilt release must have a different identity, such as `Qualification010_Reconstruction_v0.2`, unless the original bytes are actually found.

NBR-02 remains paused. No agent team, repository publication or deployment was launched here.
