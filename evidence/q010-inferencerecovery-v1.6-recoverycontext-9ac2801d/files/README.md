# Q010 Inference Recovery v1.6 — start here

Read `REPORT.md`, then `STATUS.json`. Inference evaluation recovery is complete; missing historical optimizer/RNG checkpoints and raw main training traces remain missing. No main fit was retrained.

## Complete ZIP: restore exact duplicate files and check integrity

From the extracted package directory:

```text
python RESTORE_IDENTICAL_FILES.py
python VERIFY_PACKAGE.py
```

The ZIP stores byte-identical files once. `PACKAGING/IDENTICAL_FILES.json` binds every alias to canonical bytes and SHA256. Restoration makes all original capture/replay paths physically present. Existing different files are never overwritten. This is lossless packaging, not neural quantization or evidence exclusion.

## Inference-only commands

The measured numerical environment uses Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5, and safetensors. No automatic installation occurs. Use a new output path for each command. Set `OMP_NUM_THREADS`, `OPENBLAS_NUM_THREADS`, and `MKL_NUM_THREADS` to 1 in the launch environment. The worker also fixes Torch/inter-op threads and disables training.

```text
python recovery/worker.py audit --output new_export_audit.json --source-lock 930d3fb476962ff3d51a40d2add84e0c109ada09a5339c54471d6abeda53bf8c
python recovery/worker.py capture --seed 1201 --output new_capture_1201 --source-lock 930d3fb476962ff3d51a40d2add84e0c109ada09a5339c54471d6abeda53bf8c
python recovery/worker.py score --input new_capture_1201 --output new_score_1201 --source-lock 930d3fb476962ff3d51a40d2add84e0c109ada09a5339c54471d6abeda53bf8c
python recovery/worker.py capture --seed 1201 --output new_replay_1201 --source-lock 930d3fb476962ff3d51a40d2add84e0c109ada09a5339c54471d6abeda53bf8c
python recovery/worker.py compare --input new_capture_1201 --right new_replay_1201 --output new_replay_check_1201.json --source-lock 930d3fb476962ff3d51a40d2add84e0c109ada09a5339c54471d6abeda53bf8c
```

Repeat with seeds 1202–1205 to regenerate the other four paired evaluations. Add `--fixture` to a capture command for the explicitly smaller integration-development selection; never count it as full main evidence. The current result directories are immutable evidence, so do not run the supervisor over them in place.

## Important files

`results/analysis/STUDY_RESULT.json` contains complete coverage, candidate gates and historical gaps. `ALL_QUERY_SCORES.csv`, `ALL_NEGATIVE_QUERY_RESULTS.csv`, `METRICS_ALL_SEEDS_AND_POOLED.csv` and `WHOLE_MAP_DIAGNOSTICS.csv` preserve all results. Per-seed raw captures/replays and independent verification receipts live under `results/main/`. `audit/RECOVERY_TESTS.json` and `FRESH_MAIN_UNDERFLOW_REJECTION.*` document the numerical amendment. Original input archives are retained under `provenance/input_archives/`, including the unusable standalone Q009 ZIP as received.

The compact recovery-context archive contains review/continuation material but omits bulk raw main capture/replay trees and original ZIP inputs. It has its own explicit scope and file manifest. Use the complete archive for full raw-evidence inspection.
