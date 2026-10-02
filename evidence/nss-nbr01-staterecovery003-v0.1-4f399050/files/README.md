# NSS NBR-01 / StateRecovery003 v0.1

Native-state maintenance research: known-record recovery, fast/slow lanes,
false memories, qualified corrections and explicit reset. Start with REPORT.md.

**This is a standalone research package, not a foundation patch.** Extract it
beside the other studies inside `MegaMind_Alpha_Proto`. Do not merge into the
v0.5.0 foundation or previous studies. No source model is installed as a core.

## What is included

Code; 15 new fitted checkpoints; five reused frozen source representations plus
one development reference; protocol and local registration; all main metrics
and predicted answers; development failures; post-hoc diagnostics; numerical
and training replay receipts; scoped state snapshots; resource measurements;
and an SHA-256 manifest. Known-record and UNKNOWN failures are both preserved.

## Local checks

Run `RUN_STUDY_TESTS.cmd` on Windows, or from this folder:

```sh
python -B -m unittest discover -s tests -v
python -B tools/verify_manifest.py
```

The shell launcher does not install anything or use the network. A compatible
Python environment with torch, numpy and safetensors is required. Training also
uses psutil. Tested environment: Python 3.13.5, CPU PyTorch 2.10.0+cpu,
numpy 2.3.5, safetensors 0.7.0 and psutil 7.2.2 on Linux. These are observed versions,
not a claim that Windows or arbitrary framework builds have been qualified.
`ENVIRONMENT.json` records them; there is no automatic dependency installer.

`VERIFY_RESULTS.cmd` replays the main experiment in a new temporary directory.
It compares all per-cell numerical rows and saved predictions strictly; other
platforms/kernels can differ numerically. A mismatch should be investigated,
not silently recast as a pass. It does not overwrite the supplied results.

`REPRODUCE_ONE_TRAINING.cmd` retrains one entire 1,800-step trajectory into a new
temporary directory and checks its digest against the delivered checkpoint.
The strict identical-weight result was obtained in the recorded Linux CPU
environment; it is not a cross-platform floating-point guarantee.

For an explicit alternate output directory:

```sh
python -B tools/verify_results.py --output /path/to/new/verification
python -B run.py train --kind recurrent --rep-seed 303 --seed 503 --steps 1800 --output /path/to/new/training
```

Completed training/evaluation outputs are not overwritten. Temporary training
and evaluation are synthetic and local. No model downloads, external uploads,
repository actions, accepted-generation changes, permission grants, external
side effects or live NSS databases are involved.

## Scope

Exact addresses, clean qualification, a small known code bank and direct
code-target teaching are supplied. This tests a mechanism, not full cognition.
The recurrent candidate's severe false-UNKNOWN result stays in the main scores.
The later existence-flag intervention adds protected information and is labelled
post-hoc; it is not claimed as a learned solution. General binding, reasoning,
delayed credit, low-bit traces and companion integration remain open.
