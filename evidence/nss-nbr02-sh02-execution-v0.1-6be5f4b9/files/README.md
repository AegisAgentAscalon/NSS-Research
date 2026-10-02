# NSS NBR02 SH02 v0.1

Clean hierarchical maintenance-reader component and engineering evidence. Start with `ARCHITECTURE.md` for the design and `REPORT.md` for outcomes. No model training or optimizer updates occurred.

## Run locally

Python with NumPy 2.3.5 and PyTorch 2.10.0 was tested on CPU. From this folder:

```bash
python scripts/demo.py
python tests/validate.py
python scripts/regression.py
python scripts/benchmark.py
python scripts/post_audit.py
```

`demo.py` uses the included trusted SH01 inference checkpoint and typed maintenance world, writes `examples/output.json`, and executes no external action. Its scores are not calibrated probabilities. It is not a general-language system.

`regression.py` preserves a strict historical bit-for-bit replay check as well as numeric/class checks. In this runtime it returns exit1 because all nine old archive logit arrays differ by small amounts even under the legacy code. Numerical tolerance and class parity passed; the failure is retained, not silently removed. See the report and `post_audit.py` results. Running scripts again may overwrite their result JSON; copy the package before reproducing it to keep the delivered evidence immutable.

`benchmark.py` executes all seven planned cost conditions. The original call's 20-second tool timeout occurred after six; `complete_costs.py` completed only the final condition. Delivered `benchmark.json` combines the retained first six conditions with that completion. Do not run `complete_costs.py` as a fresh full benchmark. Timing is hardware/session-dependent; larger sweeps need an adequate caller timeout.

## Layout

- `nss_hsa/`: isolated topology, plan/cache, feature adapter, reader and attention code.
- `checkpoints/`: three inference-only SH01 exports with unchanged parameter hashes.
- `fixtures/`: previously exposed SH01 regression fixtures, not fresh confirmation.
- `reference/`: old source, report and saved output files for exact comparisons.
- `tests/`: numeric, gradient, graph, corruption and restart checks.
- `results/`: raw timing repetitions, parity measurements, profiles and audits.
- `failures/`: historical bitwise replay differences and the interrupted cost-run evidence.
- `provenance/`, `SOURCE_LOCK.json`, `MANIFEST.json`: source and artifact integrity.

No external model/service/GPU is required. No tri-core, DARP or new segmented-memory policy is implemented here. Plan reuse is not neural activation reuse. This is a bounded prototype; read its limitations before building a production dependency on it.
