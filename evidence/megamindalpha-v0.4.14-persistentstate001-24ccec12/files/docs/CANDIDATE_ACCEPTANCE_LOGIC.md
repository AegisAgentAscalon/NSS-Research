# CandidateAcceptance001 — bounded integrated acceptance logic

A separate installed candidate-evidence adapter closes the local human-assisted learning/adoption/rollback loop. Roles remain attestations; no self-approval, native Runtime permit, generic neural-state migration or production authority.

## Candidate evidence and independent local qualification

**ID:** `candidate_evidence`  
**Owner:** CandidateEvidence resolves numerical lineage; Qualifications owns review/certificates  
**Status:** canonical; implementation: `partial-simulator`  
**Purpose:** Accept exact new candidate format without widening legacy probe claims or treating a score as release permission.

**Inputs:** Exact existing public-owner references; Bound candidate/source hashes; Declared local reviewer/caller and explicit operation
**Outputs:** Bounded certificate or REJECTED/INCONCLUSIVE history; Typed failure
**Structural metrics:** 12 nodes; 15 transitions; normalized complexity 8. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Prepared exact candidate claim + review"]
  n_old{"Exact completed decision exists?"}
  n_hist(["Return immutable history; no authority renewal"])
  n_roles["Check reviewer != submitter AND actual learner"]
  n_bind["Check source format, parent certificate, data, artifacts and receipts"]
  n_decision{"Reviewer requests numerical acceptance?"}
  n_no(["Record REJECTED or INCONCLUSIVE; no certificate"])
  n_score["Re-score saved candidate twice; no training"]
  n_pass{"All frozen acceptance requirements pass?"}
  n_publish["Recheck live source/prerequisites; commit exact certificate + receipt"]
  n_done(["QUALIFIED only for exact claim; no deployment authority"])
  n_fail(["Typed failure; retain previous accepted state"])
  n_start -->|"validated request/decision"| n_old
  n_old -->|"exact completed retry"| n_hist
  n_old -->|"new decision"| n_roles
  n_roles -->|"role mismatch"| n_fail
  n_bind -->|"missing / revoked / altered"| n_fail
  n_decision -->|"reject or inconclusive"| n_no
  n_score -->|"verified saved metrics"| n_pass
  n_score -->|"invalid / changed"| n_fail
  n_pass -->|"fails thresholds; verdict rejected"| n_no
  n_pass -->|"pass"| n_publish
  n_publish -->|"atomic commit"| n_done
  n_publish -->|"revoked / crash / mismatch"| n_fail
  n_roles -->|"authorized"| n_decision
  n_decision -->|"accept"| n_bind
  n_bind -->|"current evidence"| n_score
```

### Pseudocode

```text
VALIDATE(exact source format and claim; A2 != legacy A)
if identical completed decision: RESULT(history_only)
AUTHORIZE(reviewer not submitter AND not bound learning producer)
TRY(CHECK_PARENT_CERTIFICATE_AND_CURRENT_DATA())
if reviewer rejects or abstains: COMMIT(no_certificate); RESULT(review_status)
TRY(RELOAD_AND_EXACTLY_RECHECK_TWO_SAVED_EVALUATION_REPEATS())
if threshold failure: COMMIT(REJECTED, no_certificate)
else: RECHECK(live source, parent and local prerequisites); ATOMIC_PUBLISH(exact_certificate, receipt)
Never grant deployment authority from an evaluation or qualification result.
```

### Invariants

- New artifacts retain A2/A2B names, full candidate/parent lineage and code/environment identity.
- Parent Core approval is checked separately; it cannot substitute for candidate-family Core-only qualification.
- Actual learner producer cannot qualify itself through a different submitter label.
- Historical receipts remain readable after revocation; current use rechecks rights.

### Typed failures

- AUTHORIZATION_DENIED
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- VALIDATION_FAILED
- TRAINING_RESTRICTED
- RECOVERY_REQUIRED
- BUDGET_EXHAUSTED

### Forbidden edges

- Learner -> qualification certificate write
- CandidateEvidence -> qualification or generation private storage
- Candidate PASS -> deployment
- Candidate A2 -> legacy A relabel

### Optimization notes

- Reuse owner journal, checks and typed outcomes; no new database.
- Recheck mutable rights before current use. Immutable identity alone is not permission.
- Control cases share fixtures; unique crash/failure behavior remains tested.

## Whole candidate family adoption

**ID:** `candidate_adoption`  
**Owner:** Generations owns membership, release grant, staging and current/archive pointer  
**Status:** canonical; implementation: `partial-simulator`  
**Purpose:** Adopt only a currently qualified exact candidate family with fresh, separate release consent.

**Inputs:** Exact existing public-owner references; Bound candidate/source hashes; Declared local reviewer/caller and explicit operation
**Outputs:** Exact local publication receipt; Source-preserving typed failure
**Structural metrics:** 11 nodes; 15 transitions; normalized complexity 8. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Exact qualified candidate family"]
  n_family["Verify CORE/A2/A2B and both required return transitions"]
  n_review["Distinct family reviewer approves"]
  n_grant{"Fresh scoped release grant valid?"}
  n_stage["Prepare and stage whole candidate artifacts"]
  n_busy{"Any registered work open?"}
  n_wait(["RECOVERY_REQUIRED; keep parent current"])
  n_check["Recheck evidence, grant expiry/revocation and source epoch"]
  n_commit["Atomic current + predecessor archive + completion receipt"]
  n_done(["New local catalogue generation; old tickets stale"])
  n_fail(["Stop or abandon; no partial adoption"])
  n_start -->|"bound hashes"| n_family
  n_family -->|"exact closed profiles"| n_review
  n_family -->|"missing / mixed / unqualified"| n_fail
  n_review -->|"independent local attestation"| n_grant
  n_review -->|"wrong reviewer"| n_fail
  n_grant -->|"valid release-only approval"| n_stage
  n_grant -->|"learner/replay grant or expired"| n_fail
  n_stage -->|"durable complete stage"| n_busy
  n_stage -->|"corrupt / interrupted"| n_fail
  n_busy -->|"yes"| n_wait
  n_busy -->|"no"| n_check
  n_check -->|"all current"| n_commit
  n_check -->|"revoked / stale / expired"| n_fail
  n_commit -->|"committed"| n_done
  n_commit -->|"precommit interruption"| n_fail
```

### Pseudocode

```text
TRY(REQUIRE_EXACT_CANDIDATE_FAMILY_AND_QUALIFIED_CORE_ONLY())
AUTHORIZE(distinct_generation_reviewer)
AUTHORIZE(fresh_release_request, exact_source_epoch, exact_target, caller, expiry)
PREPARE_AND_STAGE_THROUGH_EXISTING_GENERATIONS_OWNER()
REQUIRE(no_open_registered_stage, RECOVERY_REQUIRED)
TRY(RECHECK_PARENT_AND_CANDIDATE_EVIDENCE_DATA_AND_RELEASE())
ATOMIC_PUBLISH(current_target, archived_parent, completion_receipt)
if exact completed retry: return historical receipt WITHOUT republish
```

### Invariants

- Only source-format-specific family membership is allowed; every family includes Core-only and qualified returns.
- Publication changes one existing owner transaction, not a second current pointer.
- Training approval and replay grants never authorize generation adoption.

### Typed failures

- AUTHORIZATION_DENIED
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- VALIDATION_FAILED
- TRAINING_RESTRICTED
- RECOVERY_REQUIRED
- BUDGET_EXHAUSTED

### Forbidden edges

- Trainer -> publish generation
- Qualification -> release grant
- Old grant -> different target/source
- Unfinished stage -> generation switch

### Optimization notes

- Reuse owner journal, checks and typed outcomes; no new database.
- Recheck mutable rights before current use. Immutable identity alone is not permission.
- Control cases share fixtures; unique crash/failure behavior remains tested.

## Candidate task, Core-only return and approved rollback

**ID:** `candidate_task_rollback`  
**Owner:** CatalogController / TaskRecord / Generations; candidate session only performs bounded numerical work  
**Status:** canonical; implementation: `partial-simulator`  
**Purpose:** Execute the staged new family; preserve task identity; return safely; rollback with new consent.

**Inputs:** Exact existing public-owner references; Bound candidate/source hashes; Declared local reviewer/caller and explicit operation
**Outputs:** Finished candidate task and exact parent rollback; Typed stop
**Structural metrics:** 13 nodes; 18 transitions; normalized complexity 8. Not runtime proof.

### Flowchart

```mermaid
flowchart TD
  n_start["Candidate family current"]
  n_pin["Pin declared A2B stage and bounded context"]
  n_work["Read staged artifact bytes; run actual fixed neural task"]
  n_end["Finish stage; qualified A2B -> A2 -> CORE"]
  n_state{"Prior neural state compatible?"}
  n_reuse["Use only compatible bound state"]
  n_rebuild["Reject stale state; replay from bound inputs; never repeat committed action"]
  n_compare["Compare rebuilt result with clean target"]
  n_close["Finish and close task"]
  n_grant{"Fresh parent rollback authorization valid?"}
  n_rollback["Stage and atomically restore exact parent artifacts"]
  n_done(["Parent restored; history/revocation checks complete"])
  n_fail(["Typed stop; preserve valid current state"])
  n_start -->|"current approval"| n_pin
  n_pin -->|"exact ticket"| n_work
  n_pin -->|"missing/revoked"| n_fail
  n_work -->|"result"| n_end
  n_end -->|"approved directed move"| n_state
  n_end -->|"unqualified transition"| n_fail
  n_state -->|"same valid ECID/task/input"| n_reuse
  n_state -->|"configuration changed"| n_rebuild
  n_reuse -->|"bound data"| n_compare
  n_rebuild -->|"safe replay"| n_compare
  n_rebuild -->|"uncertain action/invalid input"| n_fail
  n_compare -->|"exact fresh result"| n_close
  n_compare -->|"numerical mismatch"| n_fail
  n_close -->|"no open stage"| n_grant
  n_grant -->|"current parent evidence + new consent"| n_rollback
  n_grant -->|"expired/revoked/wrong scope"| n_fail
  n_rollback -->|"atomic restore, new epoch"| n_done
  n_rollback -->|"staging/publication failure"| n_fail
```

### Pseudocode

```text
PIN(exact_generation_epoch, profile, task, input_hash)
READ_STAGED_ARTIFACTS(); RUN_BOUNDED_CANDIDATE()
FINISH_STAGE(); REQUIRE(qualified_directed_transition)
if neural identity differs: REJECT_CACHE(); REPLAY_SAFE(bound_inputs, committed_receipts)
REQUIRE(rebuilt == fresh_target, VALIDATION_FAILED)
RETURN_TO_CORE_ONLY(); FINISH_AND_CLOSE_TASK()
AUTHORIZE(fresh_parent_rollback_request); STAGE(); ATOMIC_PUBLISH(parent_at_new_epoch)
AUDIT(history != renewed permission, revoked_prerequisite_blocks_use, mock_effect_count == 1)
```

### Invariants

- No arbitrary cache migration, reverse transitions or broadened task claims.
- Rollback restores parent artifact identity, not the old epoch or external world.
- Old publish receipt never republishes or executes a task.
- Original parent report and accepted Core/A/B stay unchanged.

### Typed failures

- AUTHORIZATION_DENIED
- CONSTRAINT_CONFLICT
- INCOMPATIBLE_CONFIGURATION
- INSUFFICIENT_EVIDENCE
- VALIDATION_FAILED
- TRAINING_RESTRICTED
- RECOVERY_REQUIRED
- BUDGET_EXHAUSTED

### Forbidden edges

- Rollback -> repeat committed external effect
- Closed task -> hidden reverse transition
- Historical candidate receipt -> new authorization

### Optimization notes

- Reuse owner journal, checks and typed outcomes; no new database.
- Recheck mutable rights before current use. Immutable identity alone is not permission.
- Control cases share fixtures; unique crash/failure behavior remains tested.
