# New tests — actual test method index

Tests contain concrete fixtures, stimuli and asserted outcomes. Process crashes use os._exit(83).

## test_numerical_environment_v2.py

- `test_new_plan_records_backend_execution_contract`
- `test_fresh_stored_checkpoints_reproduce_all_metrics_exactly`
- `test_tiny_mse_change_is_still_rejected`
- `test_backend_environment_change_blocks_current_reuse`
- `test_backend_build_identity_change_blocks_reuse`
- `test_cpu_identity_change_blocks_reuse`
- `test_missing_numerical_field_invalid`
- `test_numerical_policy_cannot_switch_to_tolerance`
- `test_unknown_backend_env_key_invalid`
- `test_oversize_env_value_invalid`
- `test_legacy_plan_readable_but_not_current_evidence`
- `test_historical_archive_is_still_legacy_readable`
- `test_separate_process_replays_fresh_artifacts_exactly`
- `test_separate_process_changed_backend_fails_before_scoring`
- `test_execution_guard_restores_default_dtype_precision_and_rng`
- `test_autocast_disabled_inside_bound_guard`

## test_permission_cli.py

- `test_help_is_available`
- `test_missing_store_is_not_created_by_audit`
- `test_inspect_does_not_renew_permission`
- `test_cli_denies_unknown_actor`
- `test_cli_reconcile_abandons_without_executing`

## test_permission_contracts.py

- `test_epoch_rejects_bad_types_bounds`
- `test_missing_store_not_recreated`
- `test_missing_executor_not_recreated`
- `test_create_existing_store_refused`
- `test_create_existing_executor_refused`
- `test_operator_roles_bounded_distinct`
- `test_duplicate_json_keys_rejected`
- `test_nonfinite_and_overdeep_json_rejected`
- `test_exact_request_roundtrip`
- `test_extra_field_rejected`
- `test_missing_field_rejected`
- `test_unsupported_operation`
- `test_request_schema_bool_or_unknown`
- `test_profile_claim_not_operation_authority`
- `test_unqualified_reverse_rejected`
- `test_input_scope_not_widened`
- `test_boolean_symbols_rejected`
- `test_bad_state_certificate_hash`
- `test_duplicate_action_receipts`
- `test_invalid_ttl_does_not_issue`
- `test_mutated_policy_fails_closed`
- `test_returned_request_cannot_mutate_store`

## test_permission_crashes.py

- `test_crash_before_consume`
- `test_crash_after_consume`
- `test_crash_after_dispatch`
- `test_crash_before_executor_commit`
- `test_crash_after_executor_commit`
- `test_crash_before_completion`
- `test_crash_after_completion`
- `test_crash_before_issue`
- `test_crash_after_issue`
- `test_crash_before_revoke`
- `test_crash_after_revoke`

## test_permission_execution.py

- `test_success_has_bound_receipt_and_one_old_effect`
- `test_retry_does_not_dispatch_or_recompute`
- `test_committed_history_survives_expiry_and_revocation`
- `test_no_grant_no_result`
- `test_wrong_source_state_burns_grant_without_execution`
- `test_missing_mock_world_receipt_blocks_replay`
- `test_request_with_missing_old_actions_cannot_dispatch`
- `test_reconcile_without_consumption_forbidden`
- `test_consumed_without_result_requires_explicit_abandonment`
- `test_dispatched_without_result_abandoned_not_reissued`
- `test_reconcile_existing_result_no_new_execution`
- `test_completion_needs_authoritative_receipt`
- `test_executor_cannot_complete_undispatched_grant`
- `test_wrong_reconciliation_role`
- `test_caller_cannot_fabricate_executor_receipt`
- `test_missing_executor_store_fails_without_recreating`
- `test_deleted_runtime_result_blocks_committed_retry`
- `test_tampered_runtime_result_fails_closed`
- `test_reopened_owners_return_same_historical_receipt`
- `test_result_identity_collision_rejected`
- `test_qualification_history_unchanged_by_permission_execution`
- `test_denial_does_not_disclose_raw_values`
- `test_unknown_execute_fault_fails_before_consumption`
- `test_separately_qualified_return_to_core_is_permitted`

## test_permission_store.py

- `test_qualification_alone_does_not_issue_grant`
- `test_issue_exact_grant_has_no_deployment_authority`
- `test_self_issue_denied`
- `test_unknown_issuer_denied`
- `test_unknown_caller_denied`
- `test_expired_retry_does_not_renew_grant`
- `test_issue_same_id_other_ttl_conflicts`
- `test_issue_same_id_other_request_conflicts`
- `test_wrong_request_fields_cannot_reuse_grant`
- `test_wrong_grant_hash_denied`
- `test_wrong_actor_cannot_consume`
- `test_expiry_at_boundary_denied`
- `test_just_before_expiry_allowed`
- `test_clock_rollback_denied`
- `test_consumption_is_single_use`
- `test_second_owner_cannot_consume_same_grant`
- `test_dispatch_requires_consumption`
- `test_dispatch_cannot_repeat`
- `test_expiry_between_consume_and_dispatch`
- `test_grant_revocation_before_use`
- `test_grant_revocation_after_consumption`
- `test_revocation_idempotent_and_not_reversible`
- `test_wrong_revoker`
- `test_revoked_qualification_blocks_issue`
- `test_revoked_prerequisite_blocks_consumption`
- `test_revoked_prerequisite_blocks_dispatch`
- `test_source_withdrawal_blocks_issue`
- `test_source_withdrawal_blocks_consumption`
- `test_source_withdrawal_blocks_dispatch`
- `test_source_binding_changed_rejected`
- `test_policy_and_role_mutation_detected`
- `test_deleted_event_detected`
- `test_missing_head_detected`
- `test_mutated_event_detected`
- `test_unknown_fault_points_do_not_issue`
- `test_self_issue_denied_even_when_actor_has_both_roles`
- `test_completion_receipt_never_upgrades_host_to_runtime_permit`

