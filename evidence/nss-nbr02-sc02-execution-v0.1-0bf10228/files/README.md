# NSS SC02 execution package v0.1

Start with REPORT.md and ARCHITECTURE.md. CODEX_REVIEW.md provides review questions.

This package is self-contained for inference and evidence inspection. Python 3.13.5, NumPy 2.3.5 and PyTorch 2.10.0+cpu were used; exact versions/runtime are in result receipts. Standard library plus numpy/torch are needed. Hardware/runtime differences can change performance and tiny floating-point values. No model download or GPU is required. Do not load untrusted arbitrary pickle checkpoints; these checkpoint files are the pinned project artifacts covered by the manifest.

Read-only demonstration:
```
python examples/demo.py
```

Reproduction should occur in a COPY of this folder so the original evidence remains intact. `tests/preflight.py` writes new engineering receipts. `postrun/audit.py --recount` verifies existing results; `--replay 32` reruns the declared32-task replay subset; `--snapshots` reruns retained JSON handoffs. Benchmark scripts write benchmark results, so run them in a scratch copy.

The main source lock and fresh fixture lock are already present. The main driver refuses to overwrite existing condition files. To perform a clean reconstruction, copy the package, move existing `results/` to a preserved reference directory, create a new results directory, and invoke `scripts/main.py --n 8`, then32,128. This recomputes all conditions rather than adding training. Keep all failures and output receipts. Main inference-only budget/guards are described in PROTOCOL.md.

Primary code:
- `source/sc02.py`: new incremental machinery and the optional, measured-negative intermediate cache.
- `source/sc01.py` and `source/nss_hsa/`: unchanged comparison implementation.
- `scripts/runner.py`: common maintenance episode execution.
- `scripts/benchmark.py`: interleaved complete-episode timing.
- `operational/complete_n128.py`: historical exact-missing-condition completion after a caller timeout; not a recommendation to ignore failed gates.

Numeric drift allowed only within the original declared comparison envelope. The demonstrated advantages are implementation- and workload-dependent, not proof that segmentation is universally faster than caching. I is intentionally included even though it was slower; the package does not select or hide results by favorability.
