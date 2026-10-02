# NSS NBR-01 — MembershipRepair008 v0.1

**RUN. Full joint criterion NOT MET. NBR-01 remains open.**

Read `REPORT.md` first. This is a standalone research bundle, not a patch or a new
accepted NSS runtime. Keep it beside the earlier studies in `MegaMind_Alpha_Proto`.
Do not merge it into the v0.5.0 foundation.

The simple and learned admission gates reduce ordinary false identity matches,
preserve nominal repair and writable registration, but reject too many altered
familiar queries. Near-duplicate registration also exposed an existing binder
aliasing failure. All failed/stress cases remain in the results.

## Included
`nbr008/` contains the numerical mechanisms, generators and frozen evaluation.
`reference/` contains hash-recorded inherited code and trained checkpoints.
`checkpoints/` contains all five fitted heads and their calibration evidence.
`spec/` contains the supplied plan, execution contract and pre-main local lock.
`results/` contains per-pair records and all saved numerical decision/state traces.
`SUMMARY.json` aggregates every main stratum; no seed was removed.
`evidence/` contains pilot failures, tests, replay/reproduction and diagnostics.

## Running checks
The exact tested environment was Linux CPU, Python 3.13.5, PyTorch 2.10.0+cpu,
NumPy 2.3.5 and safetensors 0.7.0. No packages are installed or downloaded by any
convenience command. `requirements.txt` records versions, not a claim of universal
platform compatibility.

```
python run.py checks
python run.py rescore
python run.py replay --pair 1
```

`checks` verifies packaged integrity and runs the 45 new tests. `rescore` checks
all saved outputs without running neural inference. `replay` reruns one complete
pair, including all main gate/control combinations, and compares every saved
array with the original. It creates a separate directory under the sibling
`NSS_Run_Output`, not inside the release folder. A full pair took minutes here;
there is no target-device speed guarantee.

The full evaluator's resource telemetry uses the Unix `resource` module.
Windows execution was NOT_RUN and the convenience replay entry reports it as
unsupported on Windows rather than pretending a port has been validated. The
checks and independent-rescore launchers are supplied but untested on Windows.
They still require the indicated Python dependencies where imported.

Large evidence arrays may have the extension `.npz.xz`: these are ordinary,
lossless compressed result files. The provided scorer and replay comparator read
them directly. Decompression reconstructs the original NPZ bytes and digest;
it is NOT low-bit neural-state storage. The main algorithms/checkpoint data keep
the original floating-point precision.

## Interpretation boundaries
All learned parameters were fixed during evaluation. Explicit REGISTER/WRITE
changes scoped buffers/reference membership, not learned model parameters.
Protected identity references contain symbols, not graph edges or factual truth.
Record presence is an explicit Boolean control. Queries do not register objects,
clear entries, or change stored evidence. Rejection does not prove nonexistence.

Main evaluation repeated all five inherited parent pairs with five fresh gate
fits and new episodes. It is internally reproducible, not independent external
replication, natural-language entity understanding, production qualification,
or a demonstration of the complete tri-core companion. No delayed-credit,
reinforcement-learning or 1–8-bit learning-state experiment was performed.

## Source and result integrity
`MANIFEST.sha256` covers the delivered files except itself. The local execution
lock covers the frozen numerical source/checkpoints/calibration. Reporting,
transport and convenience scripts added after scoring are not represented as
pre-registered neural mechanisms. Lossless transport has its own receipt.
The final fresh-extraction delivery receipt accompanies the ZIP separately.
