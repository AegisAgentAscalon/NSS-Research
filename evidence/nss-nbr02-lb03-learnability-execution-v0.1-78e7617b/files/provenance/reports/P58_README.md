# NSS LB02-MASTER16 v0.1
**One question:** can the working matrix weights behind useful two-bit forward weights be stored at16bits while continuing the original task? This is not new-task repair.

Read `docs/REPORT.md`, then `docs/TESTS_AND_ANSWERS.md`. All12 matched continuation branches and84 scheduled output panels are retained. The model remains a small18,249-coefficient checklist/cue learner, not a language model or whole NSS.

## Components
- `inputs/parents/`: four exact LB02 Q2_M8 step1024 checkpoints (sourceprepared, before correction), original optimizer history included.
- `source/master16.c`: binary16 matrix storage, row-local Q2 quantization, M8 Adam with nearest/stochastic writes.
- `source/experiment.py`: effective-weight autograd leaves, explicit STE semantics, source-bound checkpoint format and packed inference.
- `source/task.py`: unchanged exact public event rules and independent set-based labels.
- `fixtures/`: fresh development, confirmation and stress, materialized and locked.
- `checkpoints/`: every32updates, all raw learning journals, source lineage, final receipts. No original source archive merged.
- `results/`: every evaluated token/event and raw score, packed two-bit exports, per-parent numerical comparisons and totals.
- `audit/`: engineering tests, fresh-process exact replay, memory probes, parameter-change and test-review records.

## Tested environment and read-only checks
Python3.13, NumPy2.3.5, CPU PyTorch2.10.0, one thread, Linux/GNU C. Actual version data in `protocol/ENVIRONMENT.json`. FP16 is supported through GNU `_Float16`; native Windows is untested. WSL/Linux is the documented practical route. No network, model download, external service, private user data or actual tool effect is involved.

After extraction:
```
python source/verify_package.py
python source/demo.py
```
The binaries were built with:
```
cc -O2 -std=gnu11 -shared -fPIC -fno-fast-math -ffp-contract=off source/master16.c -lm -o bin/master16.so
cc -O2 -std=gnu11 -shared -fPIC -fno-fast-math -ffp-contract=off source/inherited_kernels.c -lm -o bin/kernels.so
```
Rebuilding binaries on another host changes their hashes; retain the original archive and identify new host/source/binary identities separately rather than editing the original manifest to hide changes.

`python source/audit.py` performs an inference/recount/backward-storage audit, with no optimizer updates. It writes a new audit receipt. Run it in a copy, preserving original documentary outputs. This is not independent third-party replication merely because a second process runs it.

## Full scientific reproduction
A new authorized run must use a clean output directory, preserving the exact source/config/inputs/fixtures and recording new environment identity. `run.py` refuses to overwrite an existing branch START receipt. One branch per invocation, with256 updates and checkpoints every32; no automatic uncertain-tail replay. Run `preflight.py` on disposable copies first. The original numerical and decision rules are in PROTOCOL/CONFIG. Do not use this archive as permission to run an unbounded optimization sweep or repair experiment.

## Important limitations
Two-bit forward matrices are materialized in float32 for training. Biases, gradients, activations and optimizer scales remain wide. Local update arithmetic is wider too. The precise master arrays shrink; total process RAM does not shrink by the same percentage. M16 nearest discards many small updates on this near-mastered task. All original cues remain unchanged. This does not prove new-skill learning, long-run plasticity or ternary equivalence. Both candidates pass a newly declared local storage/continuation screen; old strict gates are unchanged.
