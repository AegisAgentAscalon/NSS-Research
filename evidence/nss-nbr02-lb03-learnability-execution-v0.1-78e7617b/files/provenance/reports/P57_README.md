# NSS LB02-Q2-TRAIN v0.1

**Complete logical comparison, recorded operational budget deviation.** Two-bit effective matrix weights plus 8-bit optimizer-moment codes provide a promising research candidate. Preparation is near-perfect on the bounded panel; complete retention after a learned correction remains below its declared cohort working point. See `docs/REPORT.md` for positive results, failures and precision accounting.

## Offline demonstration
Use an existing Linux/x86-64 environment with NumPy and CPU PyTorch. The executed runtime was Python3.13.5, PyTorch2.10.0+cpu and NumPy2.3.5. No model download is required: all four parents, continuation checkpoints and packed exports are included.

```sh
python source/verify_package.py
python source/demo.py --seed 4101 --optimizer M8 --step 1024 --history 0
```

This prints the actual input events, predictions and expected finite-rule labels for one preserved example. It is not a new performance evaluation. The serving codes are two-bit; the demonstration still imports Torch and uses float64 recurrent arithmetic, not an 8KB whole-process runtime.

The supplied `bin/kernels.so` is an actual Linux/x86-64 shared library. On another compatible environment, compile the source into a separately identified binary:

```sh
cc -shared -O2 -fPIC -fno-fast-math -ffp-contract=off source/kernels.c -o bin/kernels.so -lm
```

Recompilation changes its identity. Verify the original package before any such change; do not pretend a new binary matches the old main lock. Native Windows is not validated; WSL/Linux is the relevant route. No silent installation or cloud fallback is provided.

## Audit versus repeat training
`python source/audit.py 4101` repeats retained inference checks and writes an audit receipt. It performs no optimizer update. It will touch its output/log files, so use a copied directory if preserving the exact extracted archive matters.

`study.py` is the original scientific trainer and refuses completed/partial journals. To reproduce training, make a separate run directory, bind new runtime/output identities, preserve the original inputs and protocol, and never overwrite original evidence. The two operational recovery scripts document this run's specific interrupted trajectories; they are not general retry permission.

## Evidence contents
- `protocol/`: prospective config, formulae, source locks, recovery appendices and source URLs.
- `inputs/`: original parents, exact replay batches.
- `fixtures/`: all tests, explicit labels, masks, family and prefix metadata.
- `checkpoints/`: complete saved masters, moment codes/arrays, RNG and update journals.
- `exports/`: 48 actual packed inference files.
- `results/`: raw logits, predictions and unedited outcomes for all candidates, scores and timing samples.
- `audit/`: independent recount, same-runtime exact replay, code decoding, fixture regeneration and review coverage.
- `failures/`: original precision-check failure and both caller-interruption journals.
- `docs/`: full report, architecture, eight predeclared tests with all responses, Codex handoff and current research checklist.

## Scope
No HSA/DARP/English-reader work, new parent fitting, multi-night deployment, energy measurement or native low-bit training. Matrix code precision is separate from master weights, gradient, optimizer, activations and recurrent state. Some tiny numerical differences are acceptable under the declared comparison; exact record integrity remains required. Two bits is an interim working direction; ternary remains the longer-term aim.
