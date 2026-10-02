# QualificationEvidence002 — public API and limits

## Roles and claim scope
The producer submits evidence; a distinct declared reviewer decides whether to
accept, reject or defer. Roles are LOCAL ATTESTATIONS, not authentication. The
certificate only states that the named local workflow checked a narrowly defined
claim. It is not a permit to train, execute a transition, deploy or redistribute.

Supported evidence adapter: `NeuralEvidence(journal_directory, data_directory)`
using existing public ProbeRuns, ProbeData and NeuralSession interfaces. Only the
four neural profiles CORE/A/B/AB and replay transitions AB->A/A->CORE are supported.
A2, joint control, other generations and integer-evaluation claims need future
explicit adapters. Their artifacts may be bound as report lineage, not qualified.
Profile checks cover exactly64 visible test pairs. Transition checks cover the
first4 test pairs; no universal transition claim follows from this sample.

Every non-Core profile needs an exact Core-only certificate. Every transition
also needs the source/destination profile certificates. Prerequisites bind the
SAME run, trial, all checkpoints, protocol, data, ECIDs, code and environment.
AB qualification cannot be substituted for A; a direction is not its reverse.

## APIs
- `NeuralEvidence.propose(...)` returns an exact request (no approval, no storage).
- `Qualifications.create(directory, operators)` creates the local owned journal.
- `prepare(request, source=...)` validates and stores PREPARED; exact retry is history.
- `decide(decision, source=...)` verifies a proposed acceptance, records a decision,
  and issues a certificate ONLY when complete fixed checks PASS. Human REJECT or
  INCONCLUSIVE does not run checks or produce a certificate. Upstream incomplete
  evidence has no issuable candidate trial; a completed FAIL is recorded rejected.
- `inspect(id)` returns immutable decision history, with no current eligibility claim.
- `check_use(id, certificate_sha256=..., expected_claim=..., expected_binding=...,
  source=...)` validates exact scope, current source and transitive revocation.
- `revoke(document)` appends an irreversible withdrawal; exact retry returns history.
- `history(id)` includes the original record and withdrawal events separately.
- `audit()` checks stored chain/invariants, NOT current eligibility or source rights.

Before acceptance, original scores are re-executed through the numerical public
verifier twice. Requested replay is independently repeated using fresh modules and
an isolated mock ledger. It never opens or replays the source run's action store.
Two repeats measure repeatability of fixed checkpoints; they are NOT two new model
seeds or independent retraining. Role separation is not independent science.

## State machine / ownership
PREPARED -> QUALIFIED, REJECTED or INCONCLUSIVE. Terminal decisions never change.
Revocation is a separate immutable event. A new review requires a new request ID.
Every prepare/decide/revoke event and chain head are atomically committed together.
No materialized revocation index can diverge from the event log. The bounded journal
supports at most2000 events and32MiB history; capacity errors fail explicitly.
Corrupt/missing records are not automatically repaired. Before committing, the new
journal state is validated. Numerical checks happen outside the short publication
transaction, with prerequisites/source checked again before commit.

## Field schemas / validators
Seven JSON Schemas are in schemas/qualification_*.schema.json. Exact pure validators
in qualification_contracts.py additionally enforce UTC calendar validity, role
separation, prerequisite closure, code/policy identity and candidate scope. Source
adapter validates actual evidence bytes and rechecks current-use permission. Frozen
policy bytes are exported in fixtures/qualificationevidence002/policy.json.
Requests cannot supply thresholds, test code, arbitrary scores or arbitrary backends.

## Typed failure results
ContractError preserves VALIDATION_FAILED, INCOMPATIBLE_CONFIGURATION,
INSUFFICIENT_EVIDENCE, AUTHORIZATION_DENIED, TRAINING_RESTRICTED, BUDGET_EXHAUSTED,
CONSTRAINT_CONFLICT, RECOVERY_REQUIRED and CAPABILITY_UNAVAILABLE. Contract errors
leave prior state intact; they do not synthesize an evaluation or reviewer verdict.
CLI emits the typed code as JSON and exits1. Successful command exit does not imply
acceptance: a REJECTED review can be successfully and durably recorded.

## CLI example (paths explicit; stdout is the output document)
```console
python -m nss_base.qualification_cli --store ./claims init --operators ./operators.json
python -m nss_base.qualification_cli --store ./claims propose --journal ./probe/journal --data ./probe/data --run-id probe-001 --seed 101 --precision fp32 --claim ./core-claim.json --producer local-builder --request-id core-review --at 2026-09-11T12:00:00Z > request.json
python -m nss_base.qualification_cli --store ./claims prepare --request ./request.json --journal ./probe/journal --data ./probe/data
python -m nss_base.qualification_cli --store ./claims review --decision ./decision.json --journal ./probe/journal --data ./probe/data
python -m nss_base.qualification_cli --store ./claims inspect --request-id core-review
python -m nss_base.qualification_cli --store ./claims audit
```

See qualificationevidence002.py for complete SCRIPTED fixture roles/documents.
Inspecting history does not require PyTorch; neural acceptance and current source
validation do. No implicit software/model/data downloads occur.

## Limits
Single trusted local process/role model. No PKI, signed human identity, hostile
filesystem defense, distributed transactions, source-use lease or general concurrency
claim. Hash chains cannot detect coherent rewriting of all events AND metadata.
Revocation cannot recall exports, undo previous external effects or unlearn weights.
Changed source/permission/code/backend blocks new use; identical terminal retries
remain historical. No old integer runtime flags are reinterpreted as real authority.

The historical-reference numeric audit is separate: the strict legacy checker still
fails tiny archived MSE differences. Post-hoc tolerance audit confers no qualification.
The new live pipeline does not silently accept stale or approximate historical scores.
