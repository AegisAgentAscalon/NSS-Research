# Maintenance / v0.4.12

The coordinator is added to the cumulative v0.4.11 source, not a fresh implementation
that forgets earlier contracts. No unique inherited regression is deleted.

## Shared mechanics instead of copied systems
- Reused `EventJournal` for small control metadata: plan, approval, phase claims,
  receipt references, withdrawal/cancellation and proposal. It is not another task,
  generation, archive or dataset head.
- Parameterized the existing `ProbeRuns` journal's filename, format and validators.
  CandidateRuns/CandidateEvaluations are fixed installed subclasses with separate
  formats. The underlying SQL schema and transactional behavior are unchanged; two
  more copies of the numerical journal implementation were not introduced.
- Reused frozen-checkpoint loading, no-op overlay initialization, optimizer loop,
  deterministic CPU context, encoding/targets and metrics from the existing backend.
- Extended the existing data-driven flowchart generator rather than adding a special
  diagram renderer. New schemas and a recorded-demo verifier are narrow tools.
- One cached, once-trained qualification fixture serves new tests; table-driven
  process exits share a single worker instead of duplicating whole test classes.

## Stale capacity assumption repaired
Full regression testing caught the inherited integer evaluator's 128-file metadata
inventory cap. This release legitimately binds 133 installed Python/schema/VERSION
entries. The old envelope rejected its own generated identity before reaching actual
evaluation, producing 56 failing/error test outcomes from one shared cause.

The generated implementation-inventory schema now allows a still-bounded 256 entries.
Every installed entry remains hashed; no module is omitted to squeeze under the cap.
A new test checks exact inventory coverage and rejects 257 entries. Suite, vector,
artifact-input and numerical acceptance limits are unchanged. The schema bytes are
part of the integer evaluator's exact implementation identity, so new plans bind the
new envelope. Older valid documents still fit; old hashes/reports are not rewritten.
The unchanged 110-test evaluation regression group passed after this repair.

## Other pre-release repairs
- A direct malformed cycle ID could raise an unhashable-TypeError at the new public
  gate. A reproduced failing regression now receives typed contract failure.
- Closed SQLite connections in new corruption-test fixtures explicitly, eliminating
  their development-run ResourceWarning. This was test hygiene, not an inherited
  runtime corruption defect.
- Corrected a new tooling test to retain the existing precise `research-policy`
  classification instead of incorrectly insisting every optional mechanism was
  labeled `research`. The parent policy was not changed to satisfy the test.

## Size accounting
Physical Python lines include comments and blanks; this is not a performance score.

| Area | v0.4.11 | v0.4.12 | Net |
|---|---:|---:|---:|
| Runtime | 9,266 | 10,186 | +920 |
| Tests/helpers | 6,524 | 7,047 | +523 |
| Tools | 1,013 | 1,126 | +113 |

Seven new runtime modules plus one small inherited-runtime refactor. No inherited
Python test file changed. The schema generator, release runner and dependency map
were updated intentionally. Historical docs/evidence remain labeled history; active
README, AGENTS, NEXT_STEPS, progress and implementation handoff were refreshed.

This pass consolidates mechanics but does not claim net code shrinkage, exhaustive
dead-code proof, faster training or native memory savings. Distinct tests are kept
because the new module must preserve the old behavior, not because higher counts are
inherently better. See CHANGE_ACCOUNTING.json and the actual release audit.
