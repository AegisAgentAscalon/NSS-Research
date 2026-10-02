# BoundedLearnerCoordinator001 — implementation packet

## Scope and owners
Installed human-assisted fixed A2 learning cycle. The coordinator owns plan/approval/
dispatch/receipt-reference state, not neural correctness, production state or permission
policy. `LearningCycles` uses the existing EventJournal. `CandidateRuns` and
`CandidateEvaluations` reuse ProbeRuns' journal mechanics with different versioned
formats. ExperienceArchive, DatasetSnapshots, Qualifications and Generations retain
all prior responsibilities. `learner_recipe.py` owns the fixed recipe, not the coordinator.

## Typed API
- `LearnerCoordinator.prepare(LearningPlan) -> CycleState`: validate exact parent and
  eligible selected records, persist or return the exact historical plan.
- `LearningCycles.approve(cycle_id, approver_id, expires_at, at) -> CycleState`:
  locally declared distinct operator approves once, maximum TTL 86,400 s.
- `LearnerCoordinator.advance(cycle_id, caller_id) -> CycleState | ContractError`:
  sequential snapshot/TRAIN/EVALUATE/propose. Terminal retry only reads history.
- `LearningCycles.cancel/withdraw(...) -> CycleState`: explicit immutable events.
- `LearnerCoordinator.check_proposal(cycle_id) -> CurrentAssessment | ContractError`:
  fresh source and numerical checks; always reports missing A2/A2B qualification.
- `CandidateRuns` / `CandidateEvaluations`: shared prepare/finalize/inspect/audit
  protocol. Distinct schema validators prevent substitution into probe evidence.

`schemas/learner_*.schema.json` are standard exchange schemas; manual owner validators
apply exact lineage, numerical finiteness, cross-field, role and recovery rules.
No JSON field names executable code. Installed collaborators are exact supported types.

## Preconditions
Exact Core-only parent qualification, code/environment/parent hashes, approved current
source revisions, pair codec, fixed recipe/criteria, separate local training approval,
unexpired time and sufficient bounded optimizer/per-check evaluation allocation.
Control-context/source refs only document origin; they do not confer authority.

## Postconditions
Either return immutable owner-referenced progress/proposal/history, or a typed failure
without changing production Core, accepted overlays, generation, task, or external
mock effect. A candidate training PASS means artifacts were produced, not qualification.
A numerical FAIL or INCONCLUSIVE can produce NOT_RECOMMENDED; it never deploys.

## State machine and boundaries
PLAN -> APPROVE -> START(SNAPSHOT) -> owner snapshot -> DONE(SNAPSHOT)
-> START(TRAIN) -> owner PREPARED -> compute -> owner FINALIZED -> DONE(TRAIN)
-> START(EVALUATE) -> owner PREPARED -> compute -> owner FINALIZED -> DONE(EVALUATE)
-> exact numerical/source recheck -> PROPOSED.

Cancellation is terminal. Withdrawal blocks new use. An already completed terminal
retry is historical. A claimed unsealed numeric attempt has no automatic retry route:
return RECOVERY_REQUIRED, cancel/abandon, and explicitly approve a new plan. A sealed
owner result can be reconciled without repeating numerical work. Dataset build retry
uses the existing owner's idempotency rules. There is no global cross-store transaction.

## Forbidden dependencies
Coordinator -> archive/source mutation, qualification review/minting, generation
publication, action executor, private SQL, arbitrary plugin invocation: forbidden.
Learner -> change criteria, Core weights, accepted overlay bytes or own approval: forbidden.
No new store duplicates a dataset, artifact family or current task/generation pointer.

## Concrete acceptance and test mapping
| Stimulus | Expected behavior | Tests/evidence |
|---|---|---|
| Missing/wrong/expired/withdrawn approval | deny before new numerical work | test_learner_lifecycle + CLI |
| Change plan, recipe, criteria, code, source revision or permission | typed rejection; no silent reroute | test_learner_contracts/lifecycle |
| 180/350-step approved fixed recipe | only new A2 changes; parent Core/A/B exact | lifecycle and connected demo |
| One training update, unchanged minimum requirements | FAIL/NOT_RECOMMENDED, not threshold lowering | lifecycle |
| Corrupt metric by 1e-12 | exact re-verification fails | lifecycle |
| Crash before owner commit | preserve prior committed state, require abandonment | recovery worker |
| Crash after owner commit before coordinator DONE | recover exact receipt, no refit | recovery worker |
| Retry final proposal after source revocation | same history, new current use blocked | lifecycle/demo |
| Unknown or malformed events / substituted receipt | typed validation failure | recovery |
| New A2 candidate numerical PASS | missing claims explicit, no deployment | connected demo/verifier |
| Stage/context/archive integrated | exact origin, reviewed snapshot, unchanged production and one mock action | boundedlearnercoordinator001 |

15 new actual process exits are exercised by one isolated plan-publication test and
14 table-driven phase-boundary cases. Other failures use assertions/mocks, not claims
of process crashes. Inspect release logs for measured results, not this planned table.

## Optimization and limitations
Reuse fixed journal mechanics and installed numerical helpers; do not introduce a
workflow language or duplicated policy owner. Only touched/new code is refactored;
distinct existing regressions remain. Evaluation repeat budgets are per check; extra
current-use and parent-evidence checks consume more compute and are reported as such.
Single cooperating local worker; human declarations are not authentication, backend
work is not adversarially sandboxed, and the task/learning sources are synthetic.
