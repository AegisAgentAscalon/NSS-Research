# NSS — NBR-01 State/Depth Pilot001 v0.1

**Research began:20 trained checkpoints, a five-seed pilot, preserved failures, and a same-weight gating diagnostic.**

Read **REPORT.md** first. This is a **standalone research/evidence package**, not a replacement NSS release, patch, qualified neural Primary, or Forge trainer. MegaMind Alpha v0.5.0 remains unchanged. Its active adapters remain deterministic test adapters.

## Where to put it

Extract this folder beside the existing source folder inside `MegaMind_Alpha_Proto`. **Do not merge its contents into v0.5.0.** The study runs independently and does not open any NSS memory database.

```text
MegaMind_Alpha_Proto/
  MegaMindAlpha_v0.5.0_TriCoreFoundation001/
  NSS_NBR01_StateDepth_Pilot001_v0.1/
```

## Read or verify

No software installation is needed to read REPORT.md and the JSON results. Trained weights, raw per-seed metrics, protocols, code, logs and checksums are already included.

`VERIFY_RESULTS.cmd` checks the manifest, loads the20 existing data-only checkpoints, checks exact initial/final identities and state restore, and re-evaluates the3000 main-pilot metric cells. It does **not** retrain. `RUN_STUDY_TESTS.cmd` runs the28 unit tests. Both require the optional dependencies in `requirements-research.txt`; a missing dependency produces NOT_SUPPORTED, not an automatic install. Windows launchers are provided but **Windows execution has not been tested here**.

Equivalent commands from this folder:

```text
python run.py manifest
python run.py tests
python run.py verify
```

New receipts are written to a unique sibling `NSS_Run_Output` subdirectory, never into the checksum-closed research package. Reproduction requires the compatible software/backend; a failure on a different version does not establish that its behavior should be numerically identical.

## Explicit retraining

`REPRODUCE_PILOT.cmd` (or `python run.py reproduce`) explicitly performs20 small CPU training runs: five seeds, four architectures,600 optimizer steps each. It writes to a new sibling output directory and stops on errors. It is optional and not needed to inspect the delivered results. There are no downloads, network calls, private-data training, deployment actions or background schedules.

The trainer is a bounded diagnostic fixture, not a second product training engine. Generic Forge and independent Runtime remain unconnected. This fixture does not implement exact optimizer resume: interrupted attempts are retained and retried from their original seed, never falsely reported as resumed.

## Contents

`nbr01_pilot/`: task, models, state envelopes, training/evaluation, verification and diagnostic source. `spec/`: original and amended pilot protocols plus diagnostic registration. `evidence/pilot/`:20 completed runs with safetensors weights and state snapshots. `evidence/development/`: three earlier300-step runs and source snapshots, including negative results. `evidence/GATE_DIAGNOSTIC.json` and `GATE_ISOLATION.json`: explicitly post-pilot interventions. `evidence/SUMMARY.json`: all-seed aggregates. `evidence/INDEPENDENT_VERIFICATION.json`: fresh-interpreter replay receipt. `evidence/TRAINING_REPRODUCTION.json`: one full600-step optimizer trajectory reproduced exactly.

## Scope

This is eight-symbol selective recall, overwrite and missing-memory handling, not Japanese/English competence or general reasoning. The depth axis repeats a learned post-encoder readout; it does not yet test hard multi-hop reasoning or a full depth-recurrent Transformer. New learning was confined to synthetic preparation. All evaluation weights stayed fixed. **NBR-01 remains open overall; NBR-02–07 are not run.** No packed low-bit learning-state result is claimed.
