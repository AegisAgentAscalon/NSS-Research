# Maintenance — v0.4.11

No unique inherited regression was removed or weakened. Test growth covers new
packet/permission/read boundaries, not a claim that more tests equal better AI.

- Shared exact task-source verification between StageHandoff and context; old
  `source_fields` is now a compatibility wrapper over one bounded read/parser.
- Shared the archive's exact-current review/permission/revocation check between batch
  reads and the additive public exact-evidence retrieval method. No private inspection
  API is used to bypass purpose checks.
- Extracted existing catalogue-demo setup into `prepare_catalog`; the old and new
  demos use that one exact trained/qualified fixture bootstrap rather than duplicate it.
- Reused the generation schema generator and data-driven logic renderer. No new
  one-off generation/rendering tool or database was added.
- Removed unused imports from the new code/tests; parameterized mutation/budget/crash
  cases share fixtures. No inherited assertion was invalidated by this API addition.
- Replaced active README, AGENTS, NEXT_STEPS and Codex work order; kept the prior Codex
  handoff explicitly in audit history rather than as a competing live instruction.

| Python area | Before physical lines | After | Added / removed |
|---|---:|---:|---:|
| nss_base | 8677 | 9266 | +606 / -17 |
| tests | 5998 | 6524 | +526 / -0 |
| tools | 943 | 1013 | +72 / -2 |

Counts include comments/blank lines, exclude generated docs. They are not speed,
energy, maintainability or coverage metrics. The implementation is larger because
it adds a subsystem; actual shared mechanics were consolidated rather than hidden.
See audits/contextretrieval001/SOURCE_DELTA.json for per-file accounting.
