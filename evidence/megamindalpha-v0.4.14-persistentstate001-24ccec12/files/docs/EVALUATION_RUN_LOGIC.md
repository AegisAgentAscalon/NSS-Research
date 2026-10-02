# EvaluationRun001 — pseudocode implementation flows

Three helpers under the existing evaluation/qualification boundary. A completed development evaluation is NOT qualification or deployment permission. A successful operation may return a FAIL or INCONCLUSIVE evaluation verdict.

## EvaluationRun001 — exact plan and preparation

**ID:** `evaluation_prepare`  
**Owner:** evaluation_store (public source gates in evaluation_inputs)  
**Status:** local synthetic integer protocol only; implementation: `partial-simulator`  
**Purpose:** Capture reproducible development observations without granting data reuse or release authority.

**Inputs:** EvaluationPlan / exact report reference; Candidate+suite+fixture bytes; Optional current-use development snapshot adapter
**Outputs:** Prepared/finalized immutable run receipt; Historical report or typed failure; never an approval token
**Structural metrics:** 7 nodes; 9 transitions; normalized complexity 5. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Normalize exact proposed plan"]
  n_existing{"Run ID already present?"}
  n_same{"Plan matches existing run?"}
  n_capture["Verify and capture candidate / test / code / data bytes"]
  n_persist["Commit immutable PREPARED plan + material"]
  n_done(["Return receipt; existing record is historical only"])
  n_fail(["Typed failure; no approval or overwritten record"])
  n_start --> n_existing
  n_existing -->|"yes"| n_same
  n_same -->|"same plan"| n_done
  n_same -->|"different plan or corrupt record"| n_fail
  n_existing -->|"no"| n_capture
  n_capture -->|"valid current inputs"| n_persist
  n_capture -->|"input / permission failure"| n_fail
  n_persist -->|"committed"| n_done
  n_persist -->|"storage failure"| n_fail
```

### Pseudocode

```text
function PREPARE(plan):
  VALIDATE(plan); prior = LOOKUP(plan.run_id)
  if prior: REQUIRE(prior.plan == plan, CONSTRAINT_CONFLICT); return HISTORICAL_RECEIPT(prior)
  material = TRY(CAPTURE_EXACT_CURRENT_INPUTS(plan))
  ATOMIC_PUBLISH(PREPARED(plan, material))
  return RESULT(SUCCESS, prepared_receipt_with_no_verdict)
```

### Invariants

- Suite thresholds/test identities are pinned before computation.
- Only pure bounded integer checks can replay.
- Any result says authority NONE.
- Prepared runs have no verdict; finalization publishes report+receipt together.
- A valid report may say PASS, FAIL or INCONCLUSIVE; syscall SUCCESS is not evaluation PASS.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CAPABILITY_UNAVAILABLE
- CONFLICT_REQUIRES_REVIEW
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- INTERNAL_FAILURE
- RECOVERY_REQUIRED
- TRAINING_RESTRICTED
- VALIDATION_FAILED

### Forbidden edges

- Evaluator -> deployment
- Evaluation consumer -> private archive storage
- Stored historical score -> renewed data permission
- Artifact text -> dynamic code execution

### Optimization notes

- Replay bounded pure work instead of retaining half-trusted trial checkpoints.
- Recheck mutable source permissions; do not cache authority.
- One owner for evaluation rows, none for production configuration.

## EvaluationRun001 — bounded repeats and publication

**ID:** `evaluation_execute`  
**Owner:** evaluation_store (public source gates in evaluation_inputs)  
**Status:** local synthetic integer protocol only; implementation: `partial-simulator`  
**Purpose:** Capture reproducible development observations without granting data reuse or release authority.

**Inputs:** EvaluationPlan / exact report reference; Candidate+suite+fixture bytes; Optional current-use development snapshot adapter
**Outputs:** Prepared/finalized immutable run receipt; Historical report or typed failure; never an approval token
**Structural metrics:** 10 nodes; 13 transitions; normalized complexity 6. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Prepare or resume exact run"]
  n_final{"Already FINALIZED?"}
  n_gate["Recheck exact source/code/data eligibility"]
  n_compute["Execute one pure repeat; consume finite check budget"]
  n_more{"Another repeat fits frozen budget?"}
  n_derive["Derive complete PASS/FAIL or budget INCONCLUSIVE"]
  n_current["Final current-input and permission gate"]
  n_publish["Atomic report + completion receipt publication"]
  n_done(["Return finalized or historical receipt; authority NONE"])
  n_fail(["Typed failure; PREPARED remains without verdict"])
  n_start --> n_final
  n_final -->|"yes: history only"| n_done
  n_final -->|"no"| n_gate
  n_gate -->|"current inputs match"| n_compute
  n_gate -->|"changed / revoked / missing"| n_fail
  n_compute --> n_more
  n_more -->|"yes: next repeat"| n_gate
  n_more -->|"no"| n_derive
  n_derive --> n_current
  n_current -->|"unchanged and permitted"| n_publish
  n_current -->|"changed or revoked"| n_fail
  n_publish -->|"committed"| n_done
  n_publish -->|"storage failure"| n_fail
```

### Pseudocode

```text
function EXECUTE(plan):
  receipt = TRY(PREPARE(plan)); if receipt.finalized: return HISTORICAL(receipt)
  for repeat in FINITE_REPEATS(plan):
    REQUIRE(CURRENT_INPUTS_MATCH(), INCOMPATIBLE_CONFIGURATION)
    rows += PURE_CHECKS_WITH_REMAINING_BUDGET(repeat)
  report = DERIVE_VERDICT_AND_VALIDATE_EXACT_TRIAL_MATRIX(rows)
  TRY(RECHECK_INPUTS_AND_PERMISSIONS())
  ATOMIC_PUBLISH(report, exact_completion_receipt)
  return RESULT(SUCCESS, receipt_with_evaluation_verdict_and_no_authority)
```

### Invariants

- Suite thresholds/test identities are pinned before computation.
- Only pure bounded integer checks can replay.
- Any result says authority NONE.
- Prepared runs have no verdict; finalization publishes report+receipt together.
- A valid report may say PASS, FAIL or INCONCLUSIVE; syscall SUCCESS is not evaluation PASS.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CAPABILITY_UNAVAILABLE
- CONFLICT_REQUIRES_REVIEW
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- INTERNAL_FAILURE
- RECOVERY_REQUIRED
- TRAINING_RESTRICTED
- VALIDATION_FAILED

### Forbidden edges

- Evaluator -> deployment
- Evaluation consumer -> private archive storage
- Stored historical score -> renewed data permission
- Artifact text -> dynamic code execution

### Optimization notes

- Replay bounded pure work instead of retaining half-trusted trial checkpoints.
- Recheck mutable source permissions; do not cache authority.
- One owner for evaluation rows, none for production configuration.

## EvaluationRun001 — historical inspection versus current check

**ID:** `evaluation_current_use`  
**Owner:** evaluation_store (public source gates in evaluation_inputs)  
**Status:** local synthetic integer protocol only; implementation: `partial-simulator`  
**Purpose:** Capture reproducible development observations without granting data reuse or release authority.

**Inputs:** EvaluationPlan / exact report reference; Candidate+suite+fixture bytes; Optional current-use development snapshot adapter
**Outputs:** Prepared/finalized immutable run receipt; Historical report or typed failure; never an approval token
**Structural metrics:** 7 nodes; 9 transitions; normalized complexity 5. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Exact run or report request"]
  n_validate["Verify stored bytes, full trial matrix and receipt"]
  n_mode{"Historical or current check?"}
  n_hash{"Report finalized and expected digest matches?"}
  n_gate["Recheck actual candidate / suite / fixtures / code / data"]
  n_done(["Return explicitly scoped evidence; no release authority"])
  n_fail(["Typed failure; retain historical record"])
  n_start --> n_validate
  n_validate -->|"valid"| n_mode
  n_validate -->|"corruption"| n_fail
  n_mode -->|"historical inspect"| n_done
  n_mode -->|"current check"| n_hash
  n_hash -->|"yes"| n_gate
  n_hash -->|"no or incomplete"| n_fail
  n_gate -->|"current exact inputs permitted"| n_done
  n_gate -->|"revoked / missing / changed"| n_fail
```

### Pseudocode

```text
function VERIFY_CURRENT(id, expected_report_hash):
  run = TRY(READ_AND_VALIDATE_HISTORY(id))
  REQUIRE(run.finalized, INSUFFICIENT_EVIDENCE)
  REQUIRE(HASH(run.report) == expected_report_hash, CONSTRAINT_CONFLICT)
  TRY(CAPTURE_EXACT_CURRENT_INPUTS(run.plan))
  return RESULT(SUCCESS, point_in_time_check_not_a_permission_lease)
```

### Invariants

- Suite thresholds/test identities are pinned before computation.
- Only pure bounded integer checks can replay.
- Any result says authority NONE.
- Prepared runs have no verdict; finalization publishes report+receipt together.
- A valid report may say PASS, FAIL or INCONCLUSIVE; syscall SUCCESS is not evaluation PASS.

### Typed failures

- AUTHORIZATION_DENIED
- BUDGET_EXHAUSTED
- CAPABILITY_UNAVAILABLE
- CONFLICT_REQUIRES_REVIEW
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- INTERNAL_FAILURE
- RECOVERY_REQUIRED
- TRAINING_RESTRICTED
- VALIDATION_FAILED

### Forbidden edges

- Evaluator -> deployment
- Evaluation consumer -> private archive storage
- Stored historical score -> renewed data permission
- Artifact text -> dynamic code execution

### Optimization notes

- Replay bounded pure work instead of retaining half-trusted trial checkpoints.
- Recheck mutable source permissions; do not cache authority.
- One owner for evaluation rows, none for production configuration.
