# QualificationEvidence002 — executable workflow logic

Trusted-local workflow, not authenticated authority. SUCCESS may return a rejected or inconclusive review record: only a QUALIFIED certificate can satisfy its exact claim. No result authorizes deployment.

## Qualification request, review and immutable issuance

**ID:** `qualification_review`  
**Owner:** QualificationEvidence002 local journal + built-in numerical evidence adapter  
**Status:** implemented trusted-local development workflow; authentication and independent scientific validation absent; implementation: `partial-simulator`  
**Purpose:** Exact claim review, current eligibility and durable history; no execution or deployment permit.

**Inputs:** PinnedQualificationRequest; LocalReviewerDecision; PublicProbeEvidence; ExactPrerequisiteRefs
**Outputs:** HistoricalReceipt; ClaimScopedCertificate or no certificate; CurrentUseObservation or typed failure
**Structural metrics:** 13 nodes; 18 transitions; normalized complexity 9. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Exact candidate claim + report + local operator"]
  n_validate["Validate schema, policy and identity"]
  n_old{"Exact historical request/decision exists?"}
  n_history(["Return history only, not current eligibility"])
  n_prepare["Verify Core/endpoint prerequisites and live source; persist PREPARED"]
  n_role{"Distinct declared reviewer?"}
  n_accept{"Reviewer recommends acceptance?"}
  n_check["Recompute exact checkpoint results twice; check precise transition fixture"]
  n_current["Recheck source and prerequisite eligibility before publication"]
  n_seal["Atomically append decision + certificate if PASS + receipt + journal head"]
  n_negative["Prepare explicit REJECTED or INCONCLUSIVE review without certificate"]
  n_done(["Return immutable decision receipt; no deployment authority"])
  n_failed(["Preserve previous valid history; return actual typed failure"])
  n_start --> n_validate
  n_validate -->|"valid"| n_old
  n_validate -->|"invalid"| n_failed
  n_old -->|"identical completed operation"| n_history
  n_old -->|"new request"| n_prepare
  n_prepare -->|"valid and current"| n_role
  n_prepare -->|"blocked"| n_failed
  n_role -->|"yes"| n_accept
  n_role -->|"no"| n_failed
  n_accept -->|"yes"| n_check
  n_accept -->|"reject/inconclusive"| n_negative
  n_check -->|"valid PASS or FAIL result"| n_current
  n_check -->|"contract/check error"| n_failed
  n_current -->|"current"| n_seal
  n_current -->|"stale/revoked"| n_failed
  n_negative --> n_seal
  n_seal -->|"commit"| n_done
  n_seal -->|"rollback"| n_failed
```

### Pseudocode

```text
VALIDATE(request and reviewer decision)
REQUIRE(distinct declared reviewer, AUTHORIZATION_DENIED)
if exact terminal retry: return historical receipt only
persist immutable request if absent
if accept: check exact artifacts with built-in numerical verifier; recheck prerequisites/source
else: record rejected or inconclusive decision; do not execute numerical checks
ATOMIC_PUBLISH(event, receipt, journal_head); return RESULT(SUCCESS, scoped decision)
```

### Invariants

- Exact Core-only and endpoint prerequisites required.
- Roles are local attestations, not authenticated identities.
- Candidate check and human decision are distinct.
- History does not restore source permission or claim eligibility.
- All mutations append an event and head in one transaction.
- No evaluation PASS self-promotes.

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

- Producer -> own review
- Certificate -> implicit deployment
- AB approval -> inferred subset/reverse transition
- Qualification -> source SQL or report mutation
- Revoked evidence -> new use via historical retry

### Optimization notes

- Store exact source identities plus compact verification, not duplicate training tensors.
- One bounded event log owns decisions and revocation; no competing current/permission pointer.
- Check pinned bytes and fresh permissions at consumption; hashes do not authenticate hostile edits.

## Consume exact qualification with live revocation checks

**ID:** `qualification_consume`  
**Owner:** QualificationEvidence002 local journal + built-in numerical evidence adapter  
**Status:** implemented trusted-local development workflow; authentication and independent scientific validation absent; implementation: `partial-simulator`  
**Purpose:** Exact claim review, current eligibility and durable history; no execution or deployment permit.

**Inputs:** PinnedQualificationRequest; LocalReviewerDecision; PublicProbeEvidence; ExactPrerequisiteRefs
**Outputs:** HistoricalReceipt; ClaimScopedCertificate or no certificate; CurrentUseObservation or typed failure
**Structural metrics:** 8 nodes; 10 transitions; normalized complexity 5. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Exact expected claim, candidate binding and certificate hash"]
  n_journal["Validate entire bounded journal chain"]
  n_local{"Accepted, unrevoked Core/endpoint dependency closure?"}
  n_scope{"Claim/binding/hash match exactly?"}
  n_source["Check public source bytes, current eligibility and verifier backend"]
  n_current{"Still usable now?"}
  n_done(["Evidence satisfies this claim now; NOT an execution permit"])
  n_failed(["Typed failure; historical receipt remains unchanged"])
  n_start --> n_journal
  n_journal -->|"valid"| n_local
  n_journal -->|"invalid"| n_failed
  n_local -->|"yes"| n_scope
  n_local -->|"no"| n_failed
  n_scope -->|"yes"| n_source
  n_scope -->|"no"| n_failed
  n_source --> n_current
  n_current -->|"yes"| n_done
  n_current -->|"no"| n_failed
```

### Pseudocode

```text
VALIDATE(journal chain)
REQUIRE(exact accepted dependency closure, INSUFFICIENT_EVIDENCE)
REQUIRE(not revoked, AUTHORIZATION_DENIED)
REQUIRE(exact scope and bindings, INCOMPATIBLE_CONFIGURATION)
recheck public source eligibility and verifier backend
return RESULT(SUCCESS, evidence_observation_without_permit)
```

### Invariants

- Exact Core-only and endpoint prerequisites required.
- Roles are local attestations, not authenticated identities.
- Candidate check and human decision are distinct.
- History does not restore source permission or claim eligibility.
- All mutations append an event and head in one transaction.
- No evaluation PASS self-promotes.

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

- Producer -> own review
- Certificate -> implicit deployment
- AB approval -> inferred subset/reverse transition
- Qualification -> source SQL or report mutation
- Revoked evidence -> new use via historical retry

### Optimization notes

- Store exact source identities plus compact verification, not duplicate training tensors.
- One bounded event log owns decisions and revocation; no competing current/permission pointer.
- Check pinned bytes and fresh permissions at consumption; hashes do not authenticate hostile edits.

## Withdraw claim without deleting accepted history

**ID:** `qualification_revoke`  
**Owner:** QualificationEvidence002 local journal + built-in numerical evidence adapter  
**Status:** implemented trusted-local development workflow; authentication and independent scientific validation absent; implementation: `partial-simulator`  
**Purpose:** Exact claim review, current eligibility and durable history; no execution or deployment permit.

**Inputs:** PinnedQualificationRequest; LocalReviewerDecision; PublicProbeEvidence; ExactPrerequisiteRefs
**Outputs:** HistoricalReceipt; ClaimScopedCertificate or no certificate; CurrentUseObservation or typed failure
**Structural metrics:** 7 nodes; 7 transitions; normalized complexity 4. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Exact certificate withdrawal by declared reviewer"]
  n_validate["Validate operator, target hash, time and operation identity"]
  n_old{"Identical withdrawal already recorded?"}
  n_history(["Return historical withdrawal receipt"])
  n_write["Append immutable REVOKE event and head in one transaction"]
  n_done(["Future dependent consumption blocked; no exported-data recall"])
  n_failed(["Fail closed; prior history intact"])
  n_start --> n_validate
  n_validate -->|"valid"| n_old
  n_validate -->|"invalid"| n_failed
  n_old -->|"yes"| n_history
  n_old -->|"no"| n_write
  n_write -->|"commit"| n_done
  n_write -->|"rollback"| n_failed
```

### Pseudocode

```text
VALIDATE(revocation)
REQUIRE(declared reviewer, AUTHORIZATION_DENIED)
if exact retry: return history
REQUIRE(exact accepted certificate hash, CONSTRAINT_CONFLICT)
ATOMIC_PUBLISH(revoke_event, receipt, journal_head)
all future uses re-evaluate dependency revocation; return RESULT(SUCCESS, withdrawal_receipt)
```

### Invariants

- Exact Core-only and endpoint prerequisites required.
- Roles are local attestations, not authenticated identities.
- Candidate check and human decision are distinct.
- History does not restore source permission or claim eligibility.
- All mutations append an event and head in one transaction.
- No evaluation PASS self-promotes.

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

- Producer -> own review
- Certificate -> implicit deployment
- AB approval -> inferred subset/reverse transition
- Qualification -> source SQL or report mutation
- Revoked evidence -> new use via historical retry

### Optimization notes

- Store exact source identities plus compact verification, not duplicate training tensors.
- One bounded event log owns decisions and revocation; no competing current/permission pointer.
- Check pinned bytes and fresh permissions at consumption; hashes do not authenticate hostile edits.
