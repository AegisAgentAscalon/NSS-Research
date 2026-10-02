# Numerical Replay Contract v2 — LocalNexusPermissions002 release

## Confirmed problem, not a fabricated root-cause claim
The v0.4.7 archived NeuralProbe001 report has small bit-exact MSE disagreements on
this CPU. Its accuracy/count observations reproduce. The old plan recorded Python,
PyTorch and platform strings, but did not sufficiently identify CPU dispatch,
PyTorch's compiled math stack, or numerical backend configuration. Deterministic
algorithms do not promise identical results across all releases/platforms/backends.

An audit replay of the SAME archived artifacts under different MKL compatibility
settings changed which metrics disagreed: default had 27/60 MSE differences (max
4.405364961712621e-12); MKL_CBWR=COMPATIBLE had 40/60 differences (max
3.725290298461914e-9). All accuracy/counts remained exact. Switching grad/no-grad/
inference mode alone did not recover the old values. This establishes backend
sensitivity and incomplete binding; it does NOT identify the original archive's
unrecorded kernel/environment or conclusively explain its particular discrepancy.

## Forward fix
New plans use schema_version=2. The numerical environment additionally binds:
- hash of the PyTorch compiled build configuration;
- hash of stable CPU vendor/model/family/stepping/flags, plus dispatch capability;
- explicit values (including absence) for seven bounded backend environment controls;
- CPU float32, highest float32 matmul precision, disabled CPU autocast;
- deterministic algorithms, one intra-op thread, preserved/restored caller RNG;
- a versioned scoring path: reloaded_checkpoints_no_grad_v2;
- the unchanged strict rule: torch_fp32_mean_exact.

Training now seals the data-only checkpoints and computes report metrics by loading
those artifacts through the exact same scoring function used by subsequent replay.
The optimization task, budgets, losses, core/overlay sizes, and numerical format
claims were not changed. Identity/fingerprint differences block CURRENT evidence
reuse; they do not silently migrate or requalify an old result.

The execution guard saves/restores caller dtype, matmul precision, RNG, thread and
deterministic flags, and disables CPU autocast internally. Versioned CPU behavior
is a bounded local reproducibility contract, not a cross-machine universal promise.

## Historical evidence
Legacy schema-v1 plans and reports remain readable without rewriting their hashes,
metrics, thresholds or receipts. They cannot drive a NEW current-use qualification
or permission operation. Existing archived files and the original strict tool remain
byte-identical. The raw historical check is still run and its nonzero result remains
an advisory, not a PASS. The post-hoc tolerance diagnostic is only investigative.

For current claims, train/run explicitly under v2, bind and qualify that new result.
This is new evidence, not a retroactive amendment to the old measurement. Even a
1e-12 alteration of a fresh recorded MSE must still fail exact verification.

## Commands
```
python -m nss_base.neuralprobe001 --directory ../fresh-probe --keep-permission
python tools/verify_fresh_neural_evidence.py --report ../fresh-probe/report.json
python tools/verify_neural_evidence.py
```
The fresh-artifact command is a separate-process exact comparison under the matching
new fingerprint. It does not renew current data eligibility or grant qualification.
The final command intentionally retains the raw legacy audit, even when it fails.

## Primary documentation consulted
- PyTorch 2.10 numerical accuracy: https://docs.pytorch.org/docs/2.10/notes/numerical_accuracy.html
- PyTorch 2.10 reproducibility: https://docs.pytorch.org/docs/2.10/notes/randomness.html
- Intel oneMKL numerical reproducibility: https://www.intel.com/content/www/us/en/docs/onemkl/developer-guide-linux/2024-2/obtaining-numerically-reproducible-results.html

These sources motivate explicit boundaries. They do not prove the missing historical
machine settings. Audit evidence distinguishes observed experiments from inference.
