# Post-result delivery check incident

After all three package-verification checks passed, a scratch script checking tool locks raised `KeyError: files`. It assumed the benchmark lock used the multi-file schema; that lock actually has a single `path` and `sha256`. The corrected checker handled both declared schemas and all five locks passed. No locked file, model, data, score, gate or optimizer count changed. The original failed query and explanation are retained in `failures/DELIVERY_LOCK_REVIEW_SCHEMA_ERROR.json`. This is a bookkeeping defect, not a failed numerical model comparison.
