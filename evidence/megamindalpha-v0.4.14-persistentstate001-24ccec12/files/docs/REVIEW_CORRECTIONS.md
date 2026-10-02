# Logic Atlas 001 correction review

Reviewed supplied repository 0.4.0-logicatlas001 and its matching Word artifact. Corrected release: **0.4.1-logicatlas001-corrected**, Word **v0.2**, atlas data schema **v2**. The original Word document remains in `docs/artifacts/` as historical input. No neural training or new NSS subsystem was implemented.

## Corrections

| Finding | Correction and evidence |
|---|---|
| Malformed atlas collections could raise untyped Python exceptions; duplicate JSON fields could be silently accepted. | Strict JSON loader; explicit shape, scalar, enum, identifier and field validation. Malformed-input regression tests. |
| Terminal mappings did not cover every terminal, and a reachable closed cycle could pass validation. | Exact terminal coverage, success/non-success separation, exit reachability, duplicate condition rejection and contradictory unconditional-exit rejection. Negative graph tests. |
| Single-code failure sinks lost the distinction between denial, exhaustion and invalid input. | Schema v2 terminal values are allowed-outcome lists; propagate the actual code unchanged. TRY/REQUIRE specify fail-fast behavior and common helper failure envelopes. |
| The reported cyclomatic upper bound was incorrect for multiple exits and was not an implementation bound. | Join T terminals to a virtual exit: E - N + T + 1. Count only explicit graph edges. A two-exit regression verifies the formula. |
| Several refinement/context loops checked a budget without consuming it, or could retry with no progress. | Explicit budget claims and evidence/progress checks; budget-before-pass graphs; exhaustion/stall returns typed non-success. These are specification changes, not implemented cognition. |
| Overlay lookup could combine independently qualified overlays without qualifying the resulting combination. | Select one exact qualified profile and preserve its ordered membership. No inferred union qualification. |
| Action and learning diagrams omitted some authority or durability boundaries. | Fresh scoped action/deployment authorization, separate training authorization, UNCERTAIN before effect, explicit reconciliation, archive-before-eligibility, Core-upgrade continuity/migration gates. |
| STAGED recovery ignored a failed target load; reuse was reported as replay. | Resume checks load, source/target ECID and directed edge; replay reporting follows transition policy. Regression tests retain the source on failure and verify reuse reporting. |
| Re-reading a published attempt failed after a later recovery changed the current checkpoint. | An already-published attempt returns its immutable historical result without moving the current pointer or recomputing. Tested across two successive recoveries. This read is not a fresh activation. |
| Missing/corrupt initial recovery records could escape the typed public boundary; task pointers and prepared input bindings were incomplete. | Public ContractError boundary returns readable current state or None; reject cross-task pointers and substituted portable inputs; recheck staged bindings before publication. |
| Compression guidance encouraged unsafe validation caching; Mermaid labels/IDs could conflict with syntax. | Limit validation reuse to unchanged bytes/scope/authority; quote labels and prefix node IDs. Regenerate Markdown, DOT and PNG views. |

## What the evidence establishes

The full deterministic suite contains 81 tests: the 67 supplied tests plus 14 regressions. It exercises integer Core/Overlay recovery, exact clean-run equivalence, local artifact identity, explicit directed transitions, mock action reconciliation/idempotency, process-crash publication and the new validator/resume cases. Both demos and all 25 atlas graphs are checked separately. `TEST_RESULTS.txt` records commands and outcomes.

Graph validation is structural. Reachability of an exit does not prove termination for arbitrary predicates. Pseudocode helpers are design contracts, not executable implementations; allowed failure envelopes are not exhaustive branch proofs. The `forbidden_edges` strings are reviewed constraints, not an import/dependency enforcement system. `canonical` means canonical design; `partial-simulator` means only a subset is represented by Recovery 001A/001B.

The simulator does not establish neural compatibility, model quality, real Nexus authority, multi-runner safety, arbitrary power-loss durability, protection against an attacker who can rewrite the local database, or exactly-once execution in arbitrary external services. SQLite/storage exceptions outside modeled ContractError cases are not all normalized. RecoveryStore is a storage primitive, not an authorization API. Hashes identify content; they do not authenticate it.

## Review boundaries and next step

This is a bounded correction pass, not formal verification of 25 planned subsystems. Keep the unconditional qualified Core-only profile and existing failure-retention rules. Read `NEXT_STEPS.md` before further implementation; local qualification-evidence binding remains the suggested next separately authorized slice.
