# NSS LB03-LEARNABILITY v0.1 — pass 61

A bounded, reproducible mixed-precision training comparison. Read `docs/REPORT.md` first, then `docs/SOURCE_RECONCILIATION.md`. The report separates early Q2 preparation, genuinely changed associations, old-skill retention, storage, speed and numerical warnings. No post-learning repair phase or broader companion integration.

## What is included

Exact eight source checkpoints, replay inputs, frozen new fixtures, inherited kernels and new training code; all 24 training journals and 120 checkpoints; 120 packed exports and 336 raw evaluation arrays; candidate hypotheses, protocol/input/endpoint locks; every evaluated input/answer; numerical-warning logs, independent recounts, fresh-process replays and exact update/RNG replay; budget and memory records. Historical passes55–60 are fully mapped. Their unchanged original ZIPs are in a separate complete-records bundle, not silently duplicated here.

## Read-only file verification

```
python tools/verify_package.py /path/to/NSS_NBR02_LB03_LEARNABILITY_Execution_v0.1.zip
```

This streams bytes and validates exact membership, hashes and CRC. It runs no model. Hashes are not authentication of an adversarial publisher.

## Test environment

Observed Linux x86-64; Python3.13.5, NumPy2.3.5, PyTorch2.10.0+cpu, GCC14.2.0. CPU one intra/inter-op thread, MKLDNN disabled, no dropout/autocast. Checkpoints use safe `torch.load(..., weights_only=True)` for source states; new states/results are NPZ without pickle. Install dependencies through your normal approved environment. No external model download or private data is needed. Other hardware/versions are unqualified until tested.

The shipped C shared libraries correspond to the frozen source/compiler flags in `protocol/ENVIRONMENT.json`. Recompile on a compatible host with:

```
gcc -O2 -fno-fast-math -ffp-contract=off -fPIC -shared -std=gnu11 source/master16.c -lm -o bin/master16.so
gcc -O2 -fno-fast-math -ffp-contract=off -fPIC -shared source/kernels.c -lm -o bin/kernels.so
```

**Rebuilding changes binary identity.** Do not overwrite the retained package and then claim its original lock passed. Use a separate run directory and a new environment lock.

## Reproduce the audit on unchanged archived binaries

```
python tools/reproduce.py /tmp/nss_learnability_audit --audit
```

This copies the evidence to a new directory and runs four fresh processes. It replays every saved output plus **24 metered optimizer updates on disposable saved-step64 copies**, checks altered snapshots and compares a stable sigmoid equation. It does not change retained main checkpoints. The selected-step replay and every saved output were actually executed in the original audit. The wrapper is a convenience entry point; whole-wrapper execution is not claimed as an additional experiment.

## Explicitly repeat training

```
python tools/reproduce.py /tmp/nss_learnability_new_run --train
```

This is a new, separately identified experiment:24 preflight updates,12,288 main updates, followed by fixed-endpoint evaluation. No overwrite, resume of unknown tails, parameter tuning, result-selected checkpoint, or repair phase. A different host may produce different timings and slight floating results; document changes rather than claim original identity. The direct drivers and audit were tested individually; this full retraining wrapper was not executed during delivery, so no additional12,288 updates are implied.

Comparison benchmark is separately available as `tools/benchmark.py` and uses102 disposable updates. Its ledger prevents silently treating timing work as free. `tools/finalize_analysis.py` is original retrospective accounting and refers to the documented original regeneration directory; use its saved output or explicitly bind a new audit path rather than assuming it is a portable scientific driver.

## Current recommendation

Stochastic FP16 matrix masters pass the predeclared separate-regime screen (three of four parents in each), with a19.45% saving in master+gradient+moment arrays. Only two parent identities pass both regimes; no general equivalence or every-parent reliability. Nearest FP16 learns but fails the new-learning retention cohort. Both are slower in the small timed sample. Wide activations/gradients remain; broad counted storage saving is only about1.41%, not19.45% wholeRAM.

Large sigmoid preactivations cause overflow warnings in the inherited naive NumPy reference. Finite outputs and original numerical gates pass; stable reference agrees. Warnings remain evidence, not suppressed or retroactively erased. See `failures/NUMERICAL_WARNING_AND_DIAGNOSIS.json`.

## Publication and etiquette

No public release or license assignment is made. Read `ATTRIBUTION.md` and `LICENSE_DECISION_REQUIRED.md`. Keep all failures and denominators, disclose same-author review, and distinguish internal reproduction from independent replication. Do not publish only the best checkpoint or silently turn metadata/guards into learned ability.
