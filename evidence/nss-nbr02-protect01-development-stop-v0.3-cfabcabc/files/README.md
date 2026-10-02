# PROTECT01 v0.3 — complete evidence of a development-admission stop

Start with REPORT.md. This is **not a completed held-out study**. The frozen A0 rule admitted only2/4 G fits when3 were required. L admitted4/4. Every absolute accuracy/old-inventory floor passed. The G failure is specifically the own-frozen gain criterion, including one fit with insufficient mathematical headroom. The original gate was not changed. No held-out mappings or conditions were generated.

All actual preflight, eight new initial fits, development branches, negatives, and their fresh adaptive replay are retained. PROTECT01 has no held-out qualification. Analysis under `analysis/` is clearly retrospective development exploration, not a new official pass.

## Restore and verify

```text
python RESTORE_EVIDENCE.py
python VERIFY_STUDY.py
python RESCORE.py --output /new/external/audit_directory
```

Restoration losslessly groups recorded headers/numeric bytes and restores the original frame files using the captured zlib1.3.1 compression implementation. It verifies every target SHA-256. An alias is restored only after the independent executions were compared exactly. Restoration invokes no models and does not invent missing evidence.

Verification checks manifest bytes and source locks. Re-scoring uses NumPy and the recorded parameters/states; it performs no model forwards or adaptive updates. The empirical float64-reference tolerance is not a proof of roundoff bounds.

`REPLAY_STUDY.py` is a separate, explicitly opted-in *new learning reproduction*. It does not extend the archived ledger; its helper was syntax/CLI checked, not used for a third run. Same-host bit equality is not promised for arbitrary new BLAS/PyTorch builds.

## Sources and evidence

- `source/`: actual locked production, projection, independent checker, streaming worker and supervisor.
- `inherited/`: read-only source references copied from REV01, not historical weights.
- `protocol/`: approved v0.2 proposal and explicit pre-generation implementation completions.
- `raw/primary`, `raw/replay`: all executed events, parameters, gradients, projection certificates, snapshots, scores, controls and exact stop.
- `analysis/`: development-only paired trade-off and admission-headroom summaries.
- `audit/`: source/environment/seed identities, accounting, monitored resources and replay comparison.
- `program/`: all G01–G22, bounded NBR01 closure context and return-map continuity.

No old archive is required for numerical re-scoring of these new records. Input hashes identify its historical source lineage. Native/backing memory-accounting limitation OBS-DC01-COST-001 remains open; no overall efficiency claim follows from score or partial object inventories.
