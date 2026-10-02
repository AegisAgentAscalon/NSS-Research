# SURFACE01 Execution v0.1

**Outcome: STOP_BASELINE_COMPETENCE.** Start with `REPORT.md`, then `CODEX_REVIEW.md`.

The archive includes all four parent fits, intermediate checkpoints, exact training and admission data, numerical checks, failure histories, source lock and original proposal. Main adaptation and confirmation were not entered. The deliberately corrupted checkpoint fixture in `fixtures/` is an authored detector test, clearly named; it is not a usable model checkpoint.

To repeat the already completed inference-only parent audit in a matching environment, from this directory run:

```sh
python source/study.py verify
```

That command performs no training and writes an internal replay receipt. Preserve the delivered archive before rerunning tools, because receipts are rewritten. The execution environment is pinned in `protocol/environment.json`. No cross-version bitwise guarantee is made. No model download is required.

Inspect `MANIFEST.json` for file sizes and SHA-256 hashes; `MANIFEST.sha256` hashes the manifest itself. A separately delivered receipt supplies the ZIP hash and integrity check. Resuming the research or running a new protocol is not authorized merely by possessing this archive.

`source/adapt.py` is the frozen implementation for the blocked correction phase. It was not executed in the main study and is not qualified by the baseline outcome.
