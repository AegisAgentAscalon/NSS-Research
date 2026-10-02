# CAP01 — working cross-segment maintenance reader

Start with `REPORT.md`, `ARCHITECTURE.md`, `PROTOCOL.md`, and `CODEX_REVIEW.md`.

This artifact implements and tests paged attention over the retained SH01 typed maintenance task. It is not a language model, an optimizer run or a complete nighttime NSS implementation. Ordinary and hierarchy-grouped policies share exact multi-pass computation.

## Reproduction
Preserve the delivered ZIP unchanged and use a separate unpacked working copy, since rerunning scripts writes new receipts. Tested runtime: Python3.13.5, NumPy2.3.5, PyTorch2.10.0+cpu; one CPU thread; no network or external credentials.

From the package directory:

```
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python tests/preflight.py
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python scripts/audit.py recount
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python scripts/audit.py replay 0 12
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 python scripts/audit.py resume 0 4
```

`results/AUDIT_REPLAY_PLAN.json` identifies40 selected reproducibility cases. Use further index ranges to cover the remaining cases. Files under `results/paused/` include actual saved partial-softmax state and required source/layer arrays. Those original files should not be advanced in place; the audit makes working copies first.

`run.py start end` executes only result files absent in its [start,end) range, under the frozen source/fixture lock. It deliberately does not overwrite retained cases. To run the entire study again, use a NEW copy/directory with prior main results moved aside; do not silently replace historical observations. `prepare` generates the prospective fixtures and lock and must not be used to relabel a modified retrospective run as original.

The comparison manifest records exactly488 planned cases. Inputs are stable typed JSON records, not a tokenizer's language tokens. The active row budget is not total memory; full source ingestion, graph metadata and intermediate arrays are external to the neural tile.

`MANIFEST.json` covers delivered payloads with bytes and SHA256. Checkpoint files contain only inference tensors plus provenance; no optimizer state is needed. No font or external proprietary data is included.
