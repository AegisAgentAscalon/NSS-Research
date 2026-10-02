# NSS NBR-01 — BindingDepth006 v0.1

**Standalone research: RUN. Full NBR-01: OPEN. Not a foundation update.**

Put this folder beside ExistenceContent005 and the v0.5.0 foundation inside
`MegaMind_Alpha_Proto`. **Do not merge directories.** No source archive from a
previous study is required to run this package's tests or selected replay.

Read `REPORT.md` for findings; `spec/PROTOCOL.md` for the locked design;
`SUMMARY.json` for all five-seed aggregates. Every main fit has safetensors weights,
loss history, seed/recipe, finite-check audit and hashes. `results/` contains full
predictions plus canonical relation snapshots. Development failures remain in
`evidence/development/`. No serving Primary or other role is replaced.

## Local use

Requires locally installed Python, NumPy, PyTorch and safetensors. The observed
versions are in `requirements.txt`; no launcher installs packages, downloads
models, uploads files, connects an account or starts a background service.
Windows launchers are provided but **Windows execution was not tested**.
Bitwise reproduction is established only in the recorded Linux CPU environment.

```
python run.py checks
python run.py rescore
python run.py replay --kind record_hop --seed 801
python run.py train --kind record_hop --seed 801
```

The first command checks source integrity and runs52 unit tests. The second
independently rescores every packaged result from saved relation snapshots. The
third reruns one complete main configuration with fixed weights and compares all
saved arrays. The fourth explicitly starts a new6000-step synthetic training run;
it does not deploy it. By default, new outputs are written to a unique directory
in `../NSS_Run_Output/`, not inside the source package. `--output` may specify a
new external output directory. Training weights, not optimizer-state checkpoints,
are saved: optimizer-resume training is not implemented by this research runner.
Full training reproduction here starts from the recorded seed.

`RUN_RESEARCH_CHECKS.cmd` and `RUN_RESEARCH_REPLAY.cmd` invoke the first and third
commands on Windows when dependencies are present. `scripts/portable_train.py`
leaves RSS null on platforms lacking the POSIX measurement, rather than inventing
a value. That portability path itself remains untested on Windows.

## What is, and is not, learned

Before evaluation, small neural readers and a source-matching binder are trained.
At evaluation, ALL their parameters stay fixed. A bounded record store receives
qualified write/clear events. The binder selects records by numeric content;
allocation, presence metadata, complete vector writes and scope guards are
engineered. Queries use repeated learned attention/GRU computation. Integer
paths and correct next slots never enter the neural readers.

This is not a language companion, an integrated neural role cycle, a biological
simulation, online parameter learning, reinforcement learning or low-bit learning.
It is a process-supervised, single-relation synthetic mechanism study.

## Reproduction details

Main readers: record_hop, gated_hop, untied_hop4, tied_attention,
fixed_attention4. Seeds801–805;6000 AdamW steps/reader,1200/binder. Exact lookup is
an untrained control. Four-stage controls cap at4 even under an8-round allowance;
`intervention/cycled4` is explicitly different and executes eight stages.

`evidence/INDEPENDENT_RESCORING.json` checks1,013,760 answer evaluations in7,920
rows. `FULL_REPLAY.json` covers25 neural evaluation configurations;
`EXACT_REPLAY.json` covers five exact-reader configurations. `continuations/`
contains20 memory/RNG and100 mid-query continuation fixtures, with fresh-process
verification. These are internal reproducibility checks, not external replication.

Study scripts used during execution are included for audit. Some batch/audit
scripts contain this session's `/mnt/data` work locations; `run.py` is the portable
user-facing entry point. Manuscript generation is not required to run the study.
