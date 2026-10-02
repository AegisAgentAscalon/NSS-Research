# Maintenance — v0.4.10 OverlayCatalogController001

## Scope and principle
Count unique behaviors, owners and repeated mechanics, not lines or tests as a
success target. This is a bounded implementation plus a focused refactor, not a
repository-wide dead-code proof or an optimization benchmark.

## Consolidation and removal
- Fact/source recovery, record-preserving stage advancement and record finishing
  now have shared portable helpers in `task_records.py`. Both the old integer
  StageHandoff backend and the new neural-artifact stage owner call them. Removed
  copied handoff/finish mechanics instead of allowing them to drift independently.
- Extracted existing pure generation-state queries into `generation_views.py`.
  Release and task reducers share them; existing tested imports remain compatible.
  This avoids both a circular dependency and a second set of current/profile rules.
- No new database or current-generation/task-pointer manager. The original generation
  journal owns release, catalogue, task ticket, portable record and operation receipt.
- Existing schema and data-driven diagram generators were extended. No seventh
  bespoke generator or copied renderer was introduced.
- Replaced stale active Codex handoff instructions with one current entry point;
  their previous text is an explicit historical audit attachment, not build guidance.
- Test fixture construction is reused and copied into isolated stores. Current-use
  permission/evidence decisions are never cached across tests or operations.
- Retained all distinct inherited unit, integrity and crash regressions. No test
  was removed merely to reduce the count; no perpetual source-freezing test returned.

## Measured source size
Physical lines include comments and blank lines, exclude generated documentation.

| Python area | Before | After | Net |
|---|---:|---:|---:|
| Runtime | 7,919 | 8,677 | +758 |
| Tests/helpers | 5,454 | 5,998 | +544 |
| Build/development tools | 912 | 943 | +31 |

Runtime diff: 894 inserted and 136 removed lines. Tool diff: 33 inserted and 2
removed. Extracted functions contribute to these diff counts, so they are not
independent measures of new functionality or runtime speed. No latency, energy or
memory-performance gain is inferred from code size.

Three inherited runtime modules changed (`generation_store`, `generation_state`,
`task_records`). The other 50 runtime files and all 47 inherited Python test/helper
files remain byte-identical. Six runtime files and four shared test/helper files
were added. Two tools changed; the tool count stayed at 18.

`tools/audit_maintenance.py` reports size and checks retired tooling/source-freezing
assertions. `tools/check_dependencies.py` checks actual static import boundaries.
Neither establishes freedom from every possible unused or dynamically coupled path.

## Deliberate limits
The old integer RecoveryStore remains because it has a distinct recovery regression
purpose; it is not relabelled as the neural stage owner. Historic evidence remains
identified and inspectable. The current journal is bounded to 2,000 events/32 MiB;
no unbounded-scale/performance claim is made. Future ContextRetrieval001 must reuse
the current task owner rather than create a rival working-state database.
