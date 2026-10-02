# MegaMind Alpha v0.4.14 — PersistentState001

Cumulative source checkpoint, extending the completed v0.4.13 trusted-local learning,
adoption and rollback demonstration. This new source-defined pass adds **reviewed,
scoped symbolic state updates**. It does not reopen the old local-demo finish line,
train a recurrent memory, or change generic Aegis Runtime.

## New connected behavior

A deterministic proposer submits a small, source-backed delta. A separate declared
local reviewer approves its exact contents. The existing `Generations` owner checks
scope, expected revision/hash/ECID, current artifacts and source permissions, finite
values, expiry and byte budget; event, next TaskRecord and current head commit in one
transaction. No second database or learned-state manager exists.

Legacy TaskRecord v1 remains supported unchanged. An explicit reviewed `BIND_STATE`
admits a running legacy record into scoped TaskRecord v2. New `UPDATE_STATE` operations
can change a goal, add/resolve/defer a question or add/retire/expire an attributed note.
They cannot change scope, instructions, permissions, source ownership, accepted weights,
profile identity or outside-world action receipts. ALL new state deltas require review
under this conservative first policy. Reviews are attestations, not authenticated users.

`ContextService` remains read-only. Scoped state is mandatory data in context packet v2;
it is not a new instruction channel. Unanswered questions remain visible for clarification,
but still block dependent handoffs until resolved or explicitly deferred. Permission
withdrawal, supersession, challenge, expiry, wrong scope or stale configuration blocks
current use. Historical inspection/retries do not renew authority or reopen work.

## Run and inspect

```console
python -m unittest discover -s tests -v
python -m nss_base.persistentstate001 --directory ../persistent-state-demo
python -m nss_base.catalog_cli --help
python -m nss_base.context_cli --help
python tools/run_release_checks.py --output ../state-release-checks --timeout 1800
```

Use a NEW empty output directory outside the source tree. The integrated demo reuses the
existing tiny neural-probe fixture; CPU PyTorch must be installed. No model or dataset is
downloaded. The symbolic delta feature itself does not train or execute a neural model.

On Windows, use the existing virtual environment, without activation-policy changes:

```powershell
.\.venv\Scripts\python.exe -m nss_base.persistentstate001 --directory ..\persistent-state-demo
```

Native Windows execution remains untested in this release. Do not introduce WSL for this pass.
Graphviz is optional and needed only to regenerate SVG/PNG illustrations.

## What to read

- `docs/PERSISTENT_STATE_001.md`: contract, data/authority boundaries, APIs and recovery.
- `docs/PERSISTENT_STATE_SOURCE_MAP.md`: source-to-code decisions and PS-01…PS-12 tests.
- `docs/PERSISTENT_STATE_LOGIC.md`: generated pseudocode and three helper flowcharts.
- `docs/implementation_packets/PERSISTENT_STATE_001.md`: compact owned build boundary.
- `docs/audits/persistentstate001/AUDIT_REPORT.md`: executed checks and limitations.
- `docs/MAINTENANCE_00414.md`: measured changes, consolidation and retained regressions.
- `NEXT_STEPS.md`: independent review and the separate trained temporal-state experiment.

The existing candidate-adoption demo remains available:
`python -m nss_base.candidateacceptance001 --directory ../candidate-demo`.
A2 is still distinct from A; evaluation, qualification and release are still separate.
NSS host approval does not replace a generic Aegis Runtime permit.

## Evidence limits

This is trusted-local, single-worker software. Scope labels/hash chains are not authentication,
encryption, host-tamper resistance or secure erasure. Current-use permission checks are
point-in-time, not cross-store leases or recall of exported data. State history may contain
retired text for explicit local inspection. Exact source attribution is not proof of truth.
No learned proposer, useful temporal neural state, local plasticity, adaptive production
weights, native low-bit speed/energy claim, DARP, HSA/MSA or Runtime integration is introduced.

The old pre-fix numerical report remains historical and its strict replay advisory remains
visible. Fresh numerical evidence still requires exact verification; do not relax it.

## Verification for this checkpoint

Clean-extracted source: **1,111 tests passed**, all **27 required gates passed**,
15 demonstrations, and 25 parent + 32 subordinate graphs structurally validated. The
unchanged historical strict numerical advisory is retained. See the current audit for
negative-first fixes, exact logs, final packaging requirements and evidence limits.
