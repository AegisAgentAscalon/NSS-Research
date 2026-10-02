# LocalNexusPermissions002 — protocol logic

Trusted local protocol, not authenticated Nexus or an Aegis Runtime execution permit. Terminal SUCCESS can mean historical receipt or abandonment, not dispatch permission.

## Exact qualification to scoped local grant

**ID:** `permission_issue`  
**Owner:** LocalNexusPermissions002 local owners  
**Status:** Implemented local development protocol; implementation: `partial-simulator`  
**Purpose:** Bounded trusted-local replay authorization; not production security.

**Inputs:** Exact PermissionRequest; Current qualification/evidence refs; Local operator declarations
**Outputs:** Historical grant/receipt or point-in-time admission; Typed non-success without renewed authority
**Structural metrics:** 9 nodes; 12 transitions; normalized complexity 7. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Operation request + issuer + TTL"]
  n_valid["Validate fixed policy, schema and distinct roles"]
  n_old{"Identical request already issued?"}
  n_history(["Return historical grant; expiry/revocation unchanged"])
  n_check["Recheck exact current qualification, dependencies, data, code and numerical scope"]
  n_clock["Read trusted local clock and validate TTL"]
  n_commit["Atomically append ISSUE and journal head"]
  n_done(["Return nondelegable one-use local grant"])
  n_bad(["Deny with typed reason; retain audit where valid"])
  n_start --> n_valid
  n_valid -->|"valid"| n_old
  n_valid -->|"invalid"| n_bad
  n_old -->|"identical"| n_history
  n_old -->|"new"| n_check
  n_old -->|"conflicting request ID"| n_bad
  n_check -->|"current evidence"| n_clock
  n_check -->|"revoked/mismatched/failed"| n_bad
  n_clock -->|"valid"| n_commit
  n_clock -->|"rollback or invalid lifetime"| n_bad
  n_commit -->|"durable"| n_done
  n_commit -->|"failure before commit"| n_bad
```

### Pseudocode

```text
req = VALIDATE(request, fixed_policy)
REQUIRE(distinct_local_issuer_and_executor)
IF exact_prior_issue: RETURN history_not_renewal
QUALIFIED(exact_claim_and_prerequisites, current_source)
REQUIRE(monotonic_observed_clock AND bounded_TTL)
ATOMIC_PUBLISH(issue_event, journal_head)
RETURN local_grant_without_runtime_or_deployment_authority
```

### Invariants

- Local declarations are not authentication; a host grant is not an Aegis Runtime permit.
- Grants bind exact caller/task/operation, source state, action receipts, qualification claim, numerical environment and code.
- Single-use consumption precedes dispatch; unresolved consumed attempts never automatically retry.
- History inspection and reconciliation do not renew current authority or data permissions.
- No production checkpoint publication, external action creation, delegation or deployment authority.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- RECOVERY_REQUIRED
- TRAINING_RESTRICTED
- VALIDATION_FAILED
- CAPABILITY_UNAVAILABLE

### Forbidden edges

- Permission owner cannot edit qualification, dataset, neural or action-owner SQL.
- Qualification certificate cannot replace an operation grant.
- A consumed grant cannot be reset to GRANTED.
- A caller-provided result cannot substitute for the executor owner receipt.

### Optimization notes

- Bounded fixed fixture scope; no unbounded request loop.
- Reuse semantic owner APIs, not duplicated SQL or cached authorization.

## Single-use consumption, dispatch and receipt binding

**ID:** `permission_use`  
**Owner:** LocalNexusPermissions002 local owners  
**Status:** Implemented local development protocol; implementation: `partial-simulator`  
**Purpose:** Bounded trusted-local replay authorization; not production security.

**Inputs:** Exact PermissionRequest; Current qualification/evidence refs; Local operator declarations
**Outputs:** Historical grant/receipt or point-in-time admission; Typed non-success without renewed authority
**Structural metrics:** 12 nodes; 17 transitions; normalized complexity 9. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Exact request, grant, caller and executor"]
  n_validate["Validate exact request, grant and caller identity"]
  n_historyq{"Already COMMITTED?"}
  n_history(["Cross-check executor receipt; return history only"])
  n_live["Recheck expiry, revocation, evidence and unused status"]
  n_consume["Atomically consume: STARTED"]
  n_dispatch["Revalidate source; live dispatch check; append DISPATCHED"]
  n_execute["Rebuild fixed neural target; no new external effect"]
  n_stage["Atomically persist executor result and receipt"]
  n_finish["Read owner receipt; atomically append COMMITTED"]
  n_done(["Return completion; not production deployment"])
  n_bad(["Typed failure; spent attempt needs reconciliation"])
  n_start --> n_validate
  n_validate -->|"valid"| n_historyq
  n_validate -->|"invalid"| n_bad
  n_historyq -->|"yes"| n_history
  n_historyq -->|"no"| n_live
  n_live -->|"approved and unused"| n_consume
  n_live -->|"otherwise"| n_bad
  n_consume -->|"durable"| n_dispatch
  n_consume -->|"failed/interrupted"| n_bad
  n_dispatch -->|"admitted once"| n_execute
  n_dispatch -->|"revoked/expired/uncertain"| n_bad
  n_execute -->|"valid result"| n_stage
  n_execute -->|"failure"| n_bad
  n_stage -->|"durable receipt"| n_finish
  n_stage -->|"uncertain/interrupted"| n_bad
  n_finish -->|"durable completion"| n_done
  n_finish -->|"unavailable receipt"| n_bad
```

### Pseudocode

```text
VALIDATE(request, grant, exact_caller)
IF COMMITTED: REQUIRE(owner_receipt_matches); RETURN history
AUTHORIZE(current_evidence, clock, unused_grant)
ATOMIC_PUBLISH(STARTED)
VALIDATE(real_source_state, existing_action_receipts)
AUTHORIZE(current_evidence, clock); ATOMIC_PUBLISH(DISPATCHED)
result = fixed_neural_replay_without_external_actions()
ATOMIC_PUBLISH(executor_result_and_receipt)
ATOMIC_PUBLISH(COMMITTED_from_executor_receipt)
ON interruption: do_not_retry_consumed_grant
```

### Invariants

- Local declarations are not authentication; a host grant is not an Aegis Runtime permit.
- Grants bind exact caller/task/operation, source state, action receipts, qualification claim, numerical environment and code.
- Single-use consumption precedes dispatch; unresolved consumed attempts never automatically retry.
- History inspection and reconciliation do not renew current authority or data permissions.
- No production checkpoint publication, external action creation, delegation or deployment authority.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- RECOVERY_REQUIRED
- TRAINING_RESTRICTED
- VALIDATION_FAILED
- CAPABILITY_UNAVAILABLE

### Forbidden edges

- Permission owner cannot edit qualification, dataset, neural or action-owner SQL.
- Qualification certificate cannot replace an operation grant.
- A consumed grant cannot be reset to GRANTED.
- A caller-provided result cannot substitute for the executor owner receipt.

### Optimization notes

- Bounded fixed fixture scope; no unbounded request loop.
- Reuse semantic owner APIs, not duplicated SQL or cached authorization.

## Explicit spent-grant reconciliation or abandonment

**ID:** `permission_reconcile`  
**Owner:** LocalNexusPermissions002 local owners  
**Status:** Implemented local development protocol; implementation: `partial-simulator`  
**Purpose:** Bounded trusted-local replay authorization; not production security.

**Inputs:** Exact PermissionRequest; Current qualification/evidence refs; Local operator declarations
**Outputs:** Historical grant/receipt or point-in-time admission; Typed non-success without renewed authority
**Structural metrics:** 8 nodes; 11 transitions; normalized complexity 6. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Spent request and declared reconciler"]
  n_check["Check exact grant, roles and journal integrity"]
  n_lookup["Read authoritative executor result receipt"]
  n_found{"Matching receipt exists?"}
  n_record["Require dispatch history; append reconciled COMMITTED"]
  n_abandon["Confirm absence; append permanent ABANDONED"]
  n_done(["Return historical result or abandonment; no re-execution"])
  n_bad(["Hold spent status and return typed failure"])
  n_start --> n_check
  n_check -->|"valid spent grant"| n_lookup
  n_check -->|"invalid/unspent/role failure"| n_bad
  n_lookup -->|"owner readable"| n_found
  n_lookup -->|"missing/corrupt owner"| n_bad
  n_found -->|"yes"| n_record
  n_found -->|"no"| n_abandon
  n_record -->|"atomic"| n_done
  n_record -->|"undispatched or invalid receipt"| n_bad
  n_abandon -->|"atomic"| n_done
  n_abandon -->|"journal failure"| n_bad
```

### Pseudocode

```text
REQUIRE(explicit_reconciler_role AND exact_spent_grant)
receipt = executor.lookup(exact_request, grant_hash)
IF receipt: REQUIRE(dispatch_was_admitted); ATOMIC_PUBLISH(COMMITTED)
ELSE: ATOMIC_PUBLISH(ABANDONED_permanently)
DO_NOT_DISPATCH; DO_NOT_RESTORE_GRANT; RETURN history
```

### Invariants

- Local declarations are not authentication; a host grant is not an Aegis Runtime permit.
- Grants bind exact caller/task/operation, source state, action receipts, qualification claim, numerical environment and code.
- Single-use consumption precedes dispatch; unresolved consumed attempts never automatically retry.
- History inspection and reconciliation do not renew current authority or data permissions.
- No production checkpoint publication, external action creation, delegation or deployment authority.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- RECOVERY_REQUIRED
- TRAINING_RESTRICTED
- VALIDATION_FAILED
- CAPABILITY_UNAVAILABLE

### Forbidden edges

- Permission owner cannot edit qualification, dataset, neural or action-owner SQL.
- Qualification certificate cannot replace an operation grant.
- A consumed grant cannot be reset to GRANTED.
- A caller-provided result cannot substitute for the executor owner receipt.

### Optimization notes

- Bounded fixed fixture scope; no unbounded request loop.
- Reuse semantic owner APIs, not duplicated SQL or cached authorization.
