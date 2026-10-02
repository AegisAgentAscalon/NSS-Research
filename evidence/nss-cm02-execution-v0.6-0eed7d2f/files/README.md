# NSS CM-02 — completed bounded study, execution v0.6

Start with **REPORT.md**. **STATUS.json** is the final status; protocol files retain their honest pre-generation/pending statuses and are not rewritten after locking.

## Main result

On 120 held-out query occasions repeated across five frozen readers, workspace and ordinary index both achieved **391/600 (65.17%)**, versus **307/600 (51.17%)** with no retained selection. Workspace/index routing and decisions matched exactly. Pinned exact lookup scored **100/120**; the separately declared revision-following exact policy scored **105/120**. None of this establishes native learned recurrence, token-syntax superiority or compression.

## Contents

- `raw/main/capture_run/` and `raw/main/replay_run/`: complete new main inputs, isolated truth, raw numerical outputs, management decisions, costs, independent score files and negatives.
- `failed_attempts/NSS_CM02_Execution_v0.5/raw/fixture/`: **completed fixture capture/replay**, explicitly carried into v0.6 after source-identity verification and re-scoring.
- `failed_attempts/`: full v0.3 scorer failure and v0.4/v0.5 partial captures, nested in order. Their main runs remain incomplete; do not confuse passed fixture receipts with completed main studies.
- `src/` and `protocol/`: locked scientific implementation, independent scorer, reviewed design, seeds, event templates and recovery amendments.
- `results/`: convenient descriptive tables derived without changing frozen decisions. The authoritative per-query rows and frozen summaries are under `raw/main/capture_run/scores/`.
- `audit/`, `logs/`, `provenance/`: checks, all-attempt ledger, resource evidence, export identities, replay and underflow provenance.

All **5,995 attempted forwards** across versions count, including two interrupted in-flight attempts. No training. Do not reset this historical ledger or quietly add more inference under this study.

## Integrity check — no numerical dependencies needed

```text
python VERIFY_STUDY.py
```

To also verify the extracted Q010 source/export dependencies:

```text
python VERIFY_STUDY.py --baseline /path/to/Q010_InferenceRecovery_v1.6
```

## Re-score without running the models

Extract the separately retained **Q010_InferenceRecovery_v1.6_RecoveryContext.zip**, SHA-256:

```text
9ac2801dc9a67ce3d7fbea5d4f79281b66176e961488fbffb6bf9c660056279e
```

Use the environment versions in `audit/ENVIRONMENT.json`. The following command writes to a **new directory outside this study** and checks byte equality of all 32 main/fixture score files:

```text
python RESCORE.py --baseline /path/to/Q010_InferenceRecovery_v1.6 --output /path/to/new_cm02_rescore
```

This loads numerical verification machinery, not learned model exports, and performs no training or model forwards. The original archive remains a necessary dependency; its old raw training histories are still missing. The CM-01 dependency is only additionally required to repeat the novelty audit against old cases.

## Optional new neural reproduction

An explicitly invoked new main reproduction can use:

```text
python REPLAY_STUDY.py --baseline /path/to/Q010_InferenceRecovery_v1.6 --workdir /path/to/new_cm02_reproduction
```

This is **separate future work with its own ledger**, at most 1,800 forwards, never modification of the delivered study. The convenience driver was syntax/CLI checked, but not executed for a third neural run during delivery. The original producer and exact replay already completed and their receipts are included. Execute in a durable local process; short per-command chat runtimes interrupted earlier attempts. Bitwise reproduction on different hardware/library versions is not promised.

## Scope limits

Two 56-byte ASCII packets are not two native learned token memories. W/I controllers are deterministic software around tiny fixed numerical readers. All original Q010 weights, thresholds and the reconstructed underflow amendment remain unchanged. This package does not restore missing optimizer/RNG histories, raw main training traces or missing original verifier source/failed row; it does not requalify original training or the whole NSS architecture.
