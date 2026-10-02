# Source reconciliation and acceptance map — PersistentState001

Basis: `NSS_Fruit_Fly_Inspired_Persistent_State_and_Learning_Addendum_v0.2(1).docx`,
v0.2, 12 September 2026, especially §§6–7 (pp9–10), §18 (p21), §23 (p26).
The user approved the first S1 work order, not live learning or generic Runtime changes.
The provided reconciliation v0.1 and PS-01…PS-12 cases guide this implementation.
Original source and architecture files remain unchanged; this file records choices.

## Source-derived requirements vs initial engineering choices
- Source: validated scoped deltas and explicit review for consequential/identity content.
  Choice: require distinct local review for ALL S1 state writes, until classification is demonstrated.
- Source: explicit budgets/expiry; no silent removal of consequential information.
  Choice: byte-bound complete record/context, preserve full accepted state in each packet,
  expired optional note blocks current use until explicit reviewed removal. No auto compression.
- Source: version/scope/ECID and recovery. Choice: v1 stays legacy; BIND_STATE admits a
  running record into v2. No auto migration or inferred identity for historical sessions.
- Source: evidence, interpretation, challenge and rights stay separate. Choice: use existing
  exact task fields and approved ExperienceArchive refs; identity flags depend on review.
- Source: state as data, not root policy. Choice: protected schema fields plus explicit data
  authority label. Neural channel behavior is not tested by these software checks.
- Source: preserve accepted weights/effects. Choice: no training/effect callbacks in state
  operations; integrate with actual archived probe artifacts and existing receipt checks.
- Source: h/E/W and expanded candidate learning are later research. Not implemented here;
  this pass does not narrow the addendum's eventual overlay/Core learning scope.

## Concrete acceptance coverage
Names below are tests in test_persistent_state.py unless noted. They define stimuli and
expected outcomes; actual execution status is reported by the release audit, not this map.

| Case | Named behavioral coverage |
|---|---|
| PS-01 restart | test_bind_update_restart_preserves_goal_question_sources_and_effects; real commit/reopen subprocess cases; persistentstate001 unchanged-artifact assertion |
| PS-02 scope/ECID | test_bound_scope_rejects_wrong_agent_project_session_and_legacy_reads; test_wrong_caller_scope_and_ecid_updates_do_not_commit |
| PS-03 stale revision | test_revision_and_hash_conflicts_return_reproposal |
| PS-04 duplicates | test_duplicate_identical_event_is_history_different_content_is_rejected; duplicate_after_source_withdrawal_is_history_not_current_use |
| PS-05 process crash | test_persistent_state_crashes: before/after BIND_STATE and UPDATE_STATE (four actual process exits) |
| PS-06 protected authority | test_protected_fields_and_unrestricted_patch_rejected; test_notes_remain_attributed_data_and_control_policy_is_unchanged; test_scope_bound_budget_cannot_be_changed_by_a_delta |
| PS-07 malformed | test_malformed_finite_enum_and_confidence_fields; test_schema_exports_accept_current_forms_without_mutating_v1 |
| PS-08 source loss/revocation | test_missing_tampered_source_rejected_and_state_unchanged; test_archive_revocation_blocks_current_notes_not_historical_inspection; test_source_revocation_after_validation_before_commit_is_caught; test_old_packet_rejected_after_update_or_scope_substitution |
| PS-09 budget/expiry | test_state_budget_and_context_overflow_preserve_mandatory_content; test_expiry_requires_explicit_receipted_removal; test_mandatory_and_identity_note_cannot_autoexpire; test_all_expired_notes_can_be_retired_in_one_bounded_reviewed_event |
| PS-10 review/identity | test_no_self_review_or_unrecognized_reviewer_or_unbound_review; test_identity_interpretation_requires_reviewed_archive_and_challenge_blocks_use; demo explicit no-review refusal |
| PS-11 effects | test_pending_external_action_blocks_state_until_reconciled (real child exit); demo verifies one prior committed effect; all inherited action/receipt tests |
| PS-12 closed/new session | test_same_scope_rebind_rejected_and_closed_stage_history_only; test_new_session_requires_new_task_admission_not_closed_ticket_reuse |

Additional checks: source-backed exact question resolution, explicit deferral without a
fabricated answer, maximum ID boundaries, multiple question resolutions in one event,
scoped CLI history, wrong archive, training != retrieval permission, distinct revision
history after correction, approved profile handoffs and prohibition of legacy scope bypass.

## Reconciliation fixes
The parent working_ar owner description incorrectly gave managed-state ownership solely
to RecoveryStore. It now identifies Generations for managed TaskRecord heads; RecoveryStore
remains the older separate proof, not a revived competitor. Parent learned AR cognition is
still marked unimplemented. Context v2 intentionally exposes unanswered questions for
clarification; legacy v1's gate is unchanged and MOVE still enforces dependencies.

## Not established
No automatic factual/sensitivity/identity assessment, native h persistence, sparse learning,
self-improvement quality, energy/speed gain, production user authentication, semantic
prompt-injection immunity, safe erasure or native Windows qualification. Source provenance
is not truth; a local human-review label is not an authenticated human signature.
