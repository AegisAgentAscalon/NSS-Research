# ContextRetrieval001 — software context logic

Three read-only helpers of the existing context contract. Exact source-aware packets use a canonical-JSON byte budget. Native HSA/MSA, learned retrieval, tokenization and task mutation remain absent.

## Assemble a current bounded context packet

**ID:** `context_build`  
**Owner:** ContextService via existing task and archive owners  
**Status:** canonical; implementation: `partial-simulator`  
**Purpose:** Assemble a current bounded context packet

**Inputs:** Exact current TaskRecord/ticket and explicit selectors; Pinned archive refs and canonical-JSON byte budget
**Outputs:** Bounded context packet or precise typed inability; no permission or publication
**Structural metrics:** 9 nodes; 13 transitions; normalized complexity 7. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Validated point-in-time context request"]
  n_p1["Validate exact request, budget unit and current task-state identity"]
  n_p2["Preserve mandatory spine; verify referenced local sources"]
  n_p3["Hydrate facts; scoped v2 exposes open questions as data, while v1 retains its blocking gate"]
  n_p4["Check current retrieval permission for exact experience candidates"]
  n_p5["Fit required content; rank optional items and record explicit omissions"]
  n_p6["Recheck selected permissions, source bytes and current task before output"]
  n_done(["Return bounded read result; owners unchanged"])
  n_fail(["Return exact failure, no partial context or writes"])
  n_start --> n_p1
  n_p1 -->|"success"| n_p2
  n_p1 -->|"typed_error"| n_fail
  n_p2 -->|"success"| n_p3
  n_p2 -->|"typed_error"| n_fail
  n_p3 -->|"success"| n_p4
  n_p3 -->|"typed_error"| n_fail
  n_p4 -->|"success"| n_p5
  n_p4 -->|"typed_error"| n_fail
  n_p5 -->|"success"| n_p6
  n_p5 -->|"typed_error"| n_fail
  n_p6 -->|"success"| n_done
  n_p6 -->|"typed_error"| n_fail
```

### Pseudocode

```text
function BUILD_CONTEXT(request):
  request = TRY(VALIDATE_EXACT_SCHEMA_AND_BYTE_BOUNDS(request))
  view = TRY(TASK_OWNER.READ_CURRENT(request.ticket, request.record_hash))
  REQUIRE(view.identity == request.expected_identity, INCOMPATIBLE_CONFIGURATION)
  payload = COPY_MANDATORY_TASK_SPINE(view.record)
  TRY(HYDRATE_EXACT_REQUIRED_FACTS(payload, request))
  candidates = TRY(ARCHIVE_CURRENT_RETRIEVAL_VIEWS(request.references))
  REQUIRE(MANDATORY_FITS(payload, candidates), BUDGET_EXHAUSTED)
  payload = ADD_OPTIONAL_WITHIN_BUDGET(payload, explicit_ids, lexical_rank)
  TRY(RECHECK_SELECTED_PERMISSIONS_SOURCES_AND_TASK())
  return SEALED_READ_PACKET(payload, omissions, byte_accounting)
  # Optional denial is an omission; required denial returns no packet.
  # This software policy is not HSA/MSA or learned retrieval.
  # v2 includes scoped persistent state under payload.task as mandatory data, not instruction.
  # Open v2 questions stay visible for clarification; moving downstream still enforces resolution/deferral.
```

### Invariants

- One existing owner for task/current identity; no new database.
- Mandatory task spine and required evidence cannot be summarized away.
- Byte budgets do not claim tokenizer or native attention capacity.
- Raw evidence retrieval uses current reviewed-purpose permissions, not history inspection.
- Returned bytes have point-in-time validity, not a lease or revocable export.
- No external actions, new training, record mutation or profile change during context reads.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CONFLICT_REQUIRES_REVIEW
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- INTERNAL_FAILURE
- NEEDS_CLARIFICATION
- RECOVERY_REQUIRED
- RETENTION_RESTRICTED
- TRAINING_RESTRICTED
- VALIDATION_FAILED

### Forbidden edges

- Context -> Neighbor private SQL or direct record update
- Context -> Training or deployment authority
- Administrative source inspection -> Downstream retrieval use
- Source data -> Control instruction or authorization
- Bounded JSON bytes -> Claimed neural token/energy efficiency

### Optimization notes

- Read each local source once per assembly plus integrity recheck.
- No persistent permission cache or second task-head journal.
- Bound candidate arrays; deterministic greedy selection is not a global optimality claim.
- Reuse existing schema and flow rendering tooling.

## Revalidate a saved packet before current use

**ID:** `context_consume`  
**Owner:** ContextService via existing task and archive owners  
**Status:** canonical; implementation: `partial-simulator`  
**Purpose:** Revalidate a saved packet before current use

**Inputs:** Exact current TaskRecord/ticket and explicit selectors; Pinned archive refs and canonical-JSON byte budget
**Outputs:** Bounded context packet or precise typed inability; no permission or publication
**Structural metrics:** 7 nodes; 9 transitions; normalized complexity 5. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Validated point-in-time context request"]
  n_p1["Validate packet schema, expected digest and consuming caller"]
  n_p2["Build the original request again against live owners"]
  n_p3["Reject stale eligibility, stage, revision, source or changed payload"]
  n_p4["Return exact payload and state identity without an execution permit"]
  n_done(["Return bounded read result; owners unchanged"])
  n_fail(["Return exact failure, no partial context or writes"])
  n_start --> n_p1
  n_p1 -->|"success"| n_p2
  n_p1 -->|"typed_error"| n_fail
  n_p2 -->|"success"| n_p3
  n_p2 -->|"typed_error"| n_fail
  n_p3 -->|"success"| n_p4
  n_p3 -->|"typed_error"| n_fail
  n_p4 -->|"success"| n_done
  n_p4 -->|"typed_error"| n_fail
```

### Pseudocode

```text
function CONSUME_CONTEXT(packet, caller, expected_hash):
  TRY(VALIDATE(packet)); REQUIRE(HASH(packet)==expected_hash, VALIDATION_FAILED)
  REQUIRE(caller==packet.request.caller, AUTHORIZATION_DENIED)
  current = TRY(BUILD_CONTEXT(packet.request))
  REQUIRE(current==packet, INCOMPATIBLE_CONFIGURATION)
  return RESULT(SUCCESS, current.payload)
  # No historical receipt can renew source or stage permission.
```

### Invariants

- One existing owner for task/current identity; no new database.
- Mandatory task spine and required evidence cannot be summarized away.
- Byte budgets do not claim tokenizer or native attention capacity.
- Raw evidence retrieval uses current reviewed-purpose permissions, not history inspection.
- Returned bytes have point-in-time validity, not a lease or revocable export.
- No external actions, new training, record mutation or profile change during context reads.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CONFLICT_REQUIRES_REVIEW
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- INTERNAL_FAILURE
- NEEDS_CLARIFICATION
- RECOVERY_REQUIRED
- RETENTION_RESTRICTED
- TRAINING_RESTRICTED
- VALIDATION_FAILED

### Forbidden edges

- Context -> Neighbor private SQL or direct record update
- Context -> Training or deployment authority
- Administrative source inspection -> Downstream retrieval use
- Source data -> Control instruction or authorization
- Bounded JSON bytes -> Claimed neural token/energy efficiency

### Optimization notes

- Read each local source once per assembly plus integrity recheck.
- No persistent permission cache or second task-head journal.
- Bound candidate arrays; deterministic greedy selection is not a global optimality claim.
- Reuse existing schema and flow rendering tooling.

## Expand an exact selected source reference

**ID:** `context_rehydrate`  
**Owner:** ContextService via existing task and archive owners  
**Status:** canonical; implementation: `partial-simulator`  
**Purpose:** Expand an exact selected source reference

**Inputs:** Exact current TaskRecord/ticket and explicit selectors; Pinned archive refs and canonical-JSON byte budget
**Outputs:** Bounded context packet or precise typed inability; no permission or publication
**Structural metrics:** 7 nodes; 9 transitions; normalized complexity 5. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Validated point-in-time context request"]
  n_p1["Revalidate original packet through the current-use path"]
  n_p2["Require source already selected and exact task field or evidence byte range"]
  n_p3["Read through the source owner; reject split UTF-8 or mismatched digest"]
  n_p4["Rebuild a new packet under the same budget or return explicit overflow"]
  n_done(["Return bounded read result; owners unchanged"])
  n_fail(["Return exact failure, no partial context or writes"])
  n_start --> n_p1
  n_p1 -->|"success"| n_p2
  n_p1 -->|"typed_error"| n_fail
  n_p2 -->|"success"| n_p3
  n_p2 -->|"typed_error"| n_fail
  n_p3 -->|"success"| n_p4
  n_p3 -->|"typed_error"| n_fail
  n_p4 -->|"success"| n_done
  n_p4 -->|"typed_error"| n_fail
```

### Pseudocode

```text
function REHYDRATE_CONTEXT(packet, exact_selector):
  TRY(CONSUME_CONTEXT(packet))
  REQUIRE(SELECTOR_REFERENCES_SELECTED_SOURCE(exact_selector), INSUFFICIENT_EVIDENCE)
  request = COPY(packet.request); ADD_REQUIRED_EXACT_SELECTOR(request, exact_selector)
  return TRY(BUILD_CONTEXT(request))
  # No silent truncation, summary, auto-decomposition or change to TaskRecord.
  # Permission revocation blocks the new read; already exported bytes cannot be recalled.
```

### Invariants

- One existing owner for task/current identity; no new database.
- Mandatory task spine and required evidence cannot be summarized away.
- Byte budgets do not claim tokenizer or native attention capacity.
- Raw evidence retrieval uses current reviewed-purpose permissions, not history inspection.
- Returned bytes have point-in-time validity, not a lease or revocable export.
- No external actions, new training, record mutation or profile change during context reads.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CONFLICT_REQUIRES_REVIEW
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- INTERNAL_FAILURE
- NEEDS_CLARIFICATION
- RECOVERY_REQUIRED
- RETENTION_RESTRICTED
- TRAINING_RESTRICTED
- VALIDATION_FAILED

### Forbidden edges

- Context -> Neighbor private SQL or direct record update
- Context -> Training or deployment authority
- Administrative source inspection -> Downstream retrieval use
- Source data -> Control instruction or authorization
- Bounded JSON bytes -> Claimed neural token/energy efficiency

### Optimization notes

- Read each local source once per assembly plus integrity recheck.
- No persistent permission cache or second task-head journal.
- Bound candidate arrays; deterministic greedy selection is not a global optimality claim.
- Reuse existing schema and flow rendering tooling.
