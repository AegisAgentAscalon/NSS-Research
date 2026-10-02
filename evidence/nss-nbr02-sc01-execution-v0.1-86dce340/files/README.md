# NSS SC01 v0.1

A runnable, typed-record segmented-maintenance prototype over the unchanged SH02 hierarchy. Read REPORT.md and ARCHITECTURE.md first. It does not train a model or perform real external actions.

## Local use
Requires Python with NumPy and PyTorch (exact execution versions are in the JSON runtime receipts). From this directory:

```bash
python scripts/check_lock.py
python tests/preflight.py
python scripts/demo.py
```

The demo uses a retained synthetic world and the8801 checkpoint; it prints scoped advisory results. It does not run the main comparison.

`python scripts/audit.py` rechecks retained outcomes and repeats the declared retained cases. It writes new audit outputs in the local copy. Keep the delivered ZIP unchanged as original evidence.

The main driver refuses to overwrite completed conditions. To reproduce main executions, create a separate clean directory containing source/,scripts/,tests/,checkpoints/,fixtures/,PROTOCOL.md and SOURCE_LOCK.json, then run, for each size8/32/128 and seed932101/932102:

```bash
python scripts/run.py --n 8 --seed 932101
```

The timing driver uses fixed nine-sample schedules and may exceed short tool-call limits; keep completed outputs and identify any continuation explicitly. No best-run selection. `scripts/complete_timing*.py` are specific retained operational continuations, not general alternate experiments.

## Provenance and evidence
MANIFEST.json lists every final payload except itself. `python scripts/verify_package.py` checks payload size/hash consistency. SOURCE_LOCK.json is the original pre-main lock; operational continuation/audit/reporting tools added afterward are separately recorded in provenance/POST_LOCK_DRIVERS.json. Model and original HSA source bytes are unchanged. Read failures/ for the pre-lock verifier issue and timing interruptions.
