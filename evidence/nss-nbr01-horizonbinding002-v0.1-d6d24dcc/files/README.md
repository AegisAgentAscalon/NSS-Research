# NBR-01 / HorizonBinding002 — Longer Horizons, Addressed Memory and Admission

Standalone research follow-up to `NSS_NBR01_StateDepth_Pilot001_v0.1`.
It is **not** a new MegaMind serving release, an NSS source patch, or a replacement
for the tri-core foundation. No accepted model, live database, Forge or Runtime
is modified. Keep this directory **beside**, not merged into, the earlier pilot
and `MegaMindAlpha_v0.5.0_TriCoreFoundation001` inside `MegaMind_Alpha_Proto`.

Start with **REPORT.md** (combined interpretation), **spec/protocol.json**
(registered methods/criteria), and **evidence/results/SUMMARY.json** (all-seed
aggregates; raw rows remain alongside it). Negative results are included.

## What the task means

There are four supplied addresses, eight values and an UNKNOWN answer. Each
observation carries an explicit synthetic admission score. By the task's rule,
score >= 0.5 qualifies an update; lower scores must not update that address.
Address4 resets the scope. This scalar is not real-world truth, factual confidence
or Runtime authorization. Address dispatch and reset semantics are openly
engineered scaffolding. We do not claim to learn arbitrary entity binding.

All evaluation weights remain fixed. The models are prepared with supervised
AdamW; this is not an eligibility-trace, post-gradient-descent, online-learning
or packed-low-bit experiment. Four-slot neural state remains float32.

The two-block full-tape cross-attention reader is a transparent efficient
Transformer control with query access to every supplied event. It differs from
Pilot001's all-token self-attention encoder. It is not a frontier language model
and the study is not an equal-compute architecture ranking.

## Run checks or replay the supplied evidence

The research dependencies are listed in `requirements-research.txt`. Nothing in
this package installs software, fetches models, connects accounts or deploys a
model automatically. Python/PyTorch must already be available. Windows launchers
are provided but were not executed on Windows in this study.

```text
python run.py tests --output ../HB002_test_output
python run.py verify --output ../HB002_fresh_verification
```

The first command runs 33 unit tests. The second reloads the 40 supplied trained
checkpoints, regenerates the protected episodes, and checks every model metric
and prediction digest against the retained evaluation. It is slower than unit
tests and writes new verification files outside this package.

## Reproduce training or evaluate again

Use a new destination. Existing completed runs and calibrations are not silently
overwritten.

```text
python run.py train-all --steps 2400 --output ../HB002_fresh_training
python run.py evaluate --output ../HB002_fresh_evaluation
```

`train-all` prepares all40 model/seed/curriculum fits. `evaluate` evaluates the
**bundled** checkpoints in `evidence/main`, not an arbitrary external training
directory. To inspect a newly trained model, use the published `load_model` and
`evaluate_checkpoint` functions with an explicit new path. The supplied
verification routine compares the bundled evidence, not a newly invented model.
No optimizer-resume support or cross-platform bit-identical training is claimed.

## Layout

- `nbr01_horizon/`: data, models, trainer, evaluation, isolated snapshot handling,
  fresh-process replay and additional checks.
- `tests/`: independent exact-control fixtures, real gradients, algebra/GRU
  equivalence, reset, integrity, scope and state continuity.
- `spec/`: pre-main registration, final protocol, development protocol/history.
- `evidence/development/`: all completed development fits, failed competence
  screens, a source snapshot and the interrupted GRU attempt record.
- `evidence/main/`: 40 real trained safetensors checkpoints, training metrics,
  source identities and pre-run receipts.
- `evidence/results/`: fixed calibration records, protected episode scores,
  exact-memory controls and all-seed summaries.
- `evidence/`: result replay, additional checks, input-preservation receipts and
  foundation regression logs.

The frozen experimental files in `spec/REGISTRATION.json` were locked before
main training/scoring. Supplementary replay/reporting files are not allowed to
change those experimental files. Protocol decisions are local registrations,
not third-party timestamped or blinded preregistrations.
