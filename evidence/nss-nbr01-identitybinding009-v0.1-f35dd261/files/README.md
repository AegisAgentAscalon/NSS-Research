# NSS / NBR-01 — IdentityBinding009

**Completed 21 September 2026. Standalone research package; NBR-01 remains OPEN.**

Read `REPORT.md` for results and `NBR01_STATUS_REVIEW.md` for the consolidated decision.
The original approved plan, resolved protocol and pre-main source/checkpoint lock are
in `spec/`. No test-time parameter learning, low-bit learning state, model downloads,
external data uploads, or companion deployment were performed.

## Keep directories separate

Extract this as its own folder beside the previous studies in `MegaMind_Alpha_Proto`.
It is not a patch and is not to be merged into the foundation or the older studies.
The required frozen code/models are already included in `reference/parent008`.
All original source ZIPs and plans remained unchanged.

## Main result

Exact record ownership prevents cross-identity overwrites in this bounded store.
Near-negative preparation helps a numerical binder with moderately similar identities
but does not resolve the tightest collisions. Even a perfect store can be misread by
the frozen numerical readers. Internal recovery can use genuine source ownership
without treating all external queries as familiar. Strong simple controls remain.
No learned pipeline passed the complete joint near-identity requirement.

## Run without modifying the release

From this folder, with the dependencies in `requirements.txt` already available:

```text
python run.py integrity
python run.py checks
python run.py rescore
python run.py resume
python run.py replay --pair 1
```

`integrity` uses only the Python standard library. `checks` runs the 45 new research
tests. `rescore` rederives all saved main metrics; it can take several minutes.
`resume` checks all 80 saved state/RNG/partial-transaction/query continuations.
`replay` regenerates the selected pair's three complete evaluations in a fresh process
and compares every saved array. Repeat with pairs 2–5 for the full main replay.

Outputs default to a new sibling `NSS_Run_Output` folder. `--output <new-folder>`
may select another location outside this release. No existing output is overwritten.
Tests and verification do not install dependencies or request network access.

The measured host was Linux, Python 3.13.5, PyTorch 2.10.0+cpu, NumPy 2.3.5 and
safetensors 0.7.0, with one PyTorch thread per process. Full evaluation currently uses
Unix `resource` telemetry and is **NOT_SUPPORTED on Windows** without adaptation.
The remaining commands were also **not tested on Windows**. Local/device execution
is not implied by passing Linux internal reproducibility checks.

## Evidence layout and storage

- `checkpoints/`: ten trained 818-parameter binder continuations and five rule-cue calibrations.
- `evidence/results/`: all main A/B/CUE inputs, candidate states, decisions, answers and independently scored tables.
- `evidence/development/`: pilot and infrastructure-interruption records; no failed seed removed.
- `evidence/verification/`: all-pair fresh replay, complete training/calibration reproduction, 80 continuation fixtures and test logs.
- `evidence/TIMING.json`: raw state bytes, batch1/batch64 timing, measurement boundaries.
- `SUMMARY.json`: every aggregate metric with per-pair variability/counts.
- `MANIFEST.json`: SHA256 for every packaged file except itself.

Main result files are `.npz.xz`. Each original NPZ was losslessly repacked with identical
NPY entries and XZ-compressed. Per-file `.archive.json` receipts distinguish original,
repacked, and archive checksums; `evidence/ARCHIVAL.json` records the transformation.
The scoring/replay helpers verify and decode these into temporary files. Most package
space is retained random cue data. Nothing was rounded or dropped; this is **not a
low-bit neural-memory result**. Allow approximately 2 GB of working space for full
replay/temp decoding, in addition to the archive/extraction. Actual use depends on
which outputs are retained; this is a practical allowance, not a measured peak promise.

## Scope

Protected ownership/registration records are explicit engineering controls, not learned
semantic judgment. There is no hidden destination backup. The conditional second-cue
experiment changes the available information and is not integrated into the old reader.
Scored learned weights stay fixed. Research-state resume is not an integrated runtime.
The final delivery verification is supplied beside the ZIP so its own archive hash is
not self-referential. External replication, target-device profiling, language competence,
biological fidelity, full release qualification and long-term companion reliability remain untested.
