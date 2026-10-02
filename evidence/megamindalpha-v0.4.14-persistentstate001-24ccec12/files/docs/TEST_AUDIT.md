# Current verification boundary

EvaluationRun001 checks and evidence are in docs/audits/evaluationrun001/.
The final fresh-extracted ZIP verification is delivered adjacent to the archive.
Historical results below remain scoped to their original version.

---

# Recovery Experiments 001A/001B test audit

## Current validation summary

Corrected 0.4.1 suite: **81 tests passing** (67 supplied + 14 regressions). Both recovery demos and all 25 atlas graphs validate. The final handoff is also tested from a clean ZIP extraction; command output is in `TEST_RESULTS.txt`. See `REVIEW_CORRECTIONS.md` for regression scope and evidence limits.

## Logic Atlas 001 structural coverage

| Requirement | Tests and interpretation |
|---|---|
| All flow graphs validate | `test_all_flows_validate_and_are_reachable` checks atlas schema plus reachability for all 25 flows. |
| Explicit failure/forbidden edges | `test_every_flow_has_explicit_failure_and_forbidden_edges` ensures every flow states failure codes, invariants, and prohibited dependencies. |
| Research mechanism separation | `test_research_mechanisms_are_not_canonical_prerequisites` protects HSA/MSA, recurrent depth, Directional Guidance, and DARP as separately qualified mechanisms. |
| Core-only rule | `test_core_only_rule_is_explicit` protects the unconditional Core-only guarantee and source retention on failed transitions. |
| Replay/action separation | `test_recovery_and_action_flows_separate_replay_from_side_effects` requires replay-safety plus idempotency semantics and explicitly forbids repeating committed effects. |
| QAP + transition qualification | `test_overlay_runtime_requires_profile_and_transition_qualification` requires both destination profile and directed edge qualification in pseudocode. |
| Claim-scoped qualification | `test_qualification_is_claim_scoped` protects exact-hash/test-scope evidence semantics. |
| Terminal discipline | `test_no_terminal_has_outgoing_edge` forbids success/failure states from continuing silently. |
| Complexity review | `test_metrics_are_bounded_and_nonzero` catches accidental logic explosions in the specification graph; it is not a performance benchmark. |
| Negative validator tests | Unknown outcomes and unreachable nodes must fail atlas validation. |

These tests validate the **specification graph**, not future subsystem implementations. Implementation tests must separately prove that code conforms to the selected flow.

## 001B coverage and evidence

| Requirement | Tests and interpretation |
|---|---|
| Durable attempt binding | `test_durable_attempt_links_source_inputs_target_and_actions` checks source checkpoint hash/ECID, target ECID, portable input descriptor, action keys, and published/staged hash equality. |
| Atomic target publication | `test_atomic_publication_exact_clean_equivalence` plus crash-window tests show source remains current until publication and recovered A exactly equals clean A. |
| Crash after prepare/compute/stage/publish | `test_process_crash_windows_preserve_or_publish_atomically` launches real child processes that exit 73 at four boundaries, then restarts and verifies PREPARED/STAGED/PUBLISHED semantics. |
| Source retention on failure | `test_failure_retains_published_source_and_attempt_is_durable` verifies load failure records FAILED and leaves AB current. |
| Current-pointer stale writer rejection | `test_current_pointer_compare_and_swap_prevents_stale_publish` changes current source before publish and requires rejection. This is a stale-state guard, not a concurrency claim. |
| Unresolved actions | `test_unresolved_action_blocks_attempt_creation` prevents an attempt when the task has UNCERTAIN action state. |
| Action-set binding | `test_action_set_change_blocks_resume_and_retains_source` adds a committed task action after PREPARED and requires recovery failure/source retention. |
| Committed receipt integrity | `test_corrupt_committed_receipt_blocks_recovery` verifies a corrupted COMMITTED ledger receipt cannot authorize replay. Replay-safe checks also require matching mock-world receipt. |
| Resume authorization | `test_resume_requires_authorization_until_published` proves PREPARED state cannot resume without a new simulated authorization signal. |
| Durable checkpoint corruption | `test_staged_checkpoint_corruption_fails_closed` requires stored hash/body validation and preserves source. |
| Missing recovery database | `test_missing_recovery_database_fails_closed_when_directory_survives` checks fail-closed surviving-directory behavior. |
| Attempt schema/semantic consistency | `test_attempt_schema_semantics` validates the serialized record and status-dependent fields. |
| Historical order audit | `test_historical_runtime_order_is_part_of_reuse_and_identity` guards the corrected v0.1 order-sensitive reuse/identity behavior. |
| End-to-end 001B | `test_end_to_end_001b_demo` verifies SUCCESS, exact match, profile A current, and PUBLISHED attempt. |

## 001A retained coverage

The prior 42-test suite remains intact: exact recovery/clean equality, stale ECID/cache rejection, strict serialized schemas, actual local artifact hashes, directed transitions, Core-only fallback, dependency/exclusion rules, action idempotency, four action crash windows, explicit reconciliation, corrupted/missing evidence rejection, and the 001A end-to-end demo.

## Audit defects found and corrected during 001B

1. **Historical runtime order semantics:** the retained v0.1 `Catalog` used set comparison for `reuse` and sorted overlay artifacts in ECID identity. That could treat a changed operation order as equivalent. It now requires exact ordered overlays and hashes ordered artifacts.
2. **Resume authorization:** an existing PREPARED/STAGED 001B attempt originally could resume without rechecking the simulated authorization flag. Resume now requires authorization until the attempt is already PUBLISHED.
3. **Committed action evidence strength:** 001A considered any well-formed COMMITTED ledger status replay-safe. Recovery-safe verification now checks the deterministic receipt and corresponding authoritative local mock-world receipt.
4. **001B demo accounting:** an unrelated historical action was initially included in the 001B demo effect count during development; removed before handoff so the 001B demo models one task-local committed effect.

## Evidence limits / untested claims

- No multi-runner/concurrent publication safety; compare-and-swap is tested only as a stale-pointer invariant under a single runner.
- No OS/hardware power-loss laboratory test; child-process termination is the tested crash model.
- No arbitrary external system exactly-once guarantee; the local mock world is idempotent and authoritative by construction.
- No signatures/PKI or hostile privileged-tamper protection.
- No neural execution, overlay cooperation evidence, identity evaluation, or model-quality claim.

These limits are intentional. The next pass should not broaden scope without explicit authorization.

## StageHandoff001 — 0.4.2 reviewed-baseline branch
The current check is **128 tests**, not a carry-forward of historical counts.
47 new test methods cover the bounded working-state extension and its negative,
crash/retry and static-import paths. Original 81 test sources are unchanged.
See `audits/stagehandoff001/AUDIT_REPORT.md`, `checks.json`, full logs and
`new_test_inventory.json`. Acceptance against LT-01/02/03/14 is partial software
fixture coverage, as detailed in `STAGE_HANDOFF_001.md`, not neural qualification.
