# CandidateAcceptance001 — executable integration contract

**Version:** v0.4.13. **Scope:** one cooperating trusted-local worker and an installed
synthetic neural recipe. Declared role separation, not authenticated authority or
independent scientific validation. Full official NSS documentation is not silently
rewritten by this source-only integration release.

## Ownership and interfaces
| Owner | Public input | Output / owned state |
|---|---|---|
| CandidateEvidence | Existing learning, numerical, archive, snapshot and parent source owners | Exact candidate evidence view; read-only, no new store |
| Qualifications | Exact request + declared review, with installed source | Immutable request/decision/certificate/revocation history |
| Generations | Exact qualified family, generation review, release request and grant | Existing staged artifacts, current/archive pointer, tickets and completion receipts |
| CatalogController / ContextService | Approved descriptor, portable task request, exact source refs | Existing stage/task records and read-only bounded context |
| CandidateSession | Exact four checkpoint objects, fixed input pairs and profile | Ephemeral numerical prediction/recovery, never authority |
| CandidateAcceptance001 | Explicit empty demo directory | Scripted application wiring and evidence exports |

The adapter inherits only legacy request/guard mechanics, not its data interpretation.
`qualification_sources.require_source` permits exact installed classes only. There is
no callback, plugin import string or private cross-owner SQL. Common neural state/replay
mechanics now serve both families through a fixed session implementation.

## New evidence identity
`source_format = MegaMindAlpha.CandidateEvidence001` distinguishes new owner records.
The binding retains Core generation/tokenizer/context/overlay ABI, runtime/code/
environment hashes, seed and precision. Its distinct fields include:

- exact cycle and proposal hashes, actual learning producer;
- fixed training and evaluation owner receipts and report hashes;
- snapshot identity and selected archive revisions/rights;
- parent binding and parent Core certificate identity;
- installed recipe/criteria/test/retention hashes;
- checkpoint hashes for core, preserved A, preserved B and new A2;
- candidate-family ECIDs for CORE, A2 and A2B.

Shapes are generated in `schemas/qualification_binding.schema.json` (old OR new
format), request/review schemas, and generation/catalogue schemas. Owner validators
also enforce disjoint source-family semantics, exact receipts, role relationships,
current permission and numerical equality. Structural JSON validation alone is not
acceptance. Original reports and policy hashes stay unchanged; new code-bound evidence
must be generated after implementation changes.

## Exact supported qualification claims
| Claim | Required candidate-family claims |
|---|---|
| PROFILE CORE | None locally; exact accepted parent Core certificate checked separately |
| PROFILE A2 | Candidate PROFILE CORE |
| PROFILE A2B | Candidate PROFILE CORE |
| A2B -> A2, replay | Candidate CORE, A2B and A2 |
| A2 -> CORE, replay | Candidate CORE and A2 |

The new candidate checker does not silently inherit the original AB ablation claim.
Its binding names candidate_A2_profile_and_recovery_v1 and pins the learning criteria:
updated-task accuracy, retention outside the intentionally changed symbols, gain over
the accepted parent on the updated task, and exact saved-metric replay. A2B acceptance
is not a new proof of modular superiority. The common store policy stays pinned; the
source-specific checker/criteria/protocol/code hashes make this distinction explicit.

No B-only, A2B->CORE shortcut, reverse transition or arbitrary union is inferred.
Candidate A2 is never substituted for legacy A. The parent certificate is a separate
lineage dependency; it cannot serve as the new family's CORE certificate.

## Preconditions
The learning cycle is PROPOSED, not withdrawn; candidate and evaluation records are
FINALIZED with exact receipts. The frozen parent Core and A/B payloads are unchanged.
Current source revisions and training-use permissions pass through archive/snapshot
public consumption APIs. Parent numerical evidence and its qualified Core certificate
remain eligible. The code and numerical environment match the recorded contract.
Reviewer is permitted and differs from both the request submitter and actual trainer.

For publication: all required profile/transition certificates and family review pass;
a distinct release owner approves the exact target/source epoch and caller with expiry;
complete staged bytes match; no registered work remains open. Checks repeat on resume
and before publication. Qualification does not grant a lease across independent stores.

## Behavior and unsuccessful outcomes
1. Prepare an immutable exact claim. Inconsistent duplicate IDs fail.
2. A completed identical decision returns HISTORY only. It cannot recreate permission.
3. A review can reject or abstain without numerical execution; its record has no
   certificate. ACCEPT requires current source/parent/prerequisite checks before work.
4. Re-score the saved checkpoint twice through the installed candidate evaluator.
   Metrics must exactly reproduce the sealed report under its numerical contract.
5. A genuinely undertrained candidate returns REJECTED, not an invented success.
   A passing candidate must satisfy the frozen Core/retention/gain requirements and
   the named profile or replay checks. Retention covers 49 unchanged-symbol pairs;
   intentional changes at symbols 5/6 are not advertised as preserved behavior.
6. Recheck current eligibility and atomically record the verdict/certificate/receipt.
7. Propose/review the family through Generations; then issue fresh RELEASE approval.
   Existing training grants and NEURAL_PROBE_REPLAY requests remain incapable of this.
8. Stage complete bytes; parent stays current. An open stage returns RECOVERY_REQUIRED.
9. Recheck and publish target/current/archive/completion together. Old tickets are stale.
10. Run the managed task against staged bytes, with a qualified Core-only return.
    Rebuild incompatible ephemeral activations from pinned inputs. Never repeat receipts.
11. Rollback uses new approval, current parent evidence and a new epoch. Historical
    publish receipts do not republish, and checkpoint rollback cannot undo the world.

Typed non-success outcomes include VALIDATION_FAILED, INCOMPATIBLE_CONFIGURATION,
INSUFFICIENT_EVIDENCE, AUTHORIZATION_DENIED, TRAINING_RESTRICTED, CONSTRAINT_CONFLICT,
BUDGET_EXHAUSTED and RECOVERY_REQUIRED. Valid review operations may return REJECTED
or INCONCLUSIVE instead of QUALIFIED. Failure to publish preserves the current family.
No claims of successful completion are required for impossible or revoked requests.

## Postconditions and invariants
- On acceptance, a certificate covers exact evidence and claim only; it has no
  production deployment or Runtime execution authority.
- On local publication, target and archived predecessor agree with one durable
  receipt. Before commit the source remains current. Retry never repeats adoption.
- Candidate Core-only profiles are mandatory. Every allowed specialist has a qualified
  directed route back to Core-only; no arbitrary drop-an-overlay fallback.
- Accepted Core/A/B, parent report and learner proposal do not change.
- New-family managed task records retain their authoritative input/source/receipt
  identity. Unfinished work blocks catalogue replacement.
- Withdrawn parent qualification/data or new candidate data blocks subsequent use;
  immutable records can still be inspected as history, not as valid current permission.
- Qualification checks may repeat after interrupted verification, within fixed per-check
  bounds. They never call training. No claim of global wall-clock/energy quota is made.

## Crash and recovery contract
Qualification fault points: after verification, before decision commit, after decision
commit. The first two leave PREPARED with no new certificate; the last leaves an exact
qualified receipt that can be read without rechecking or renewing its authority.

Release fault points: before/after grant, prepare, stage and publish commit. Stages
prior to PUBLISHED retain the original current pointer. Resumption rechecks roles,
rights, grant expiry and source epoch. Expired/revoked staged operations cannot publish;
explicit abandonment does not reset the old grant. Fresh rollback is a new operation.

## Concrete verification mapping
- Evidence/lineage/roles/negative training: `test_candidate_acceptance_evidence.py`.
- Family, source epoch, current rights, staged bytes, rollback: `..._release.py`.
- Three qualification + eight release commit crashes and two revoked/expired resumes:
  `..._crashes.py`. These use actual child-process termination, not exception-only mocks.
- Existing/new CLI source selection, wrong mixed formats, generated schemas: `..._cli.py`.
- Full upstream learning and downstream execution/rollback: `candidateacceptance001`.
- Recorded owner-backed whole-loop history: `tools/verify_connected_alpha.py`.
  That tool is an acceptance witness checker, not a scientific validator or authority.

## CLI source selection
The existing qualification/generation/catalogue/context commands accept either:
```text
--journal <original-probe-journal> --data <original-probe-data>
```
or:
```text
--candidate-config <existing-learner_owners.json>
```
These cannot be mixed. The config maps already existing public owners; it does not
create them, approve a plan or import executable plugin code. History/audit commands
can operate without a current source because they do not grant current use.

## Remaining limitations
Trusted local roles are declared labels; a malicious operator controlling all files and
metadata can rewrite evidence. This is not PKI, production authentication, adversarial
isolation or distributed exactly-once semantics. All model tasks are small and linear;
fixtures and checks are developer-visible. No learned evaluator/router, autonomous
curation, production hardware paging, native serving cache or Runtime permit is added.
Transition checks cover four fixed pair inputs; broader tasks require new experiments.
The snapshot validation record remains development lineage, not a hidden benchmark.
