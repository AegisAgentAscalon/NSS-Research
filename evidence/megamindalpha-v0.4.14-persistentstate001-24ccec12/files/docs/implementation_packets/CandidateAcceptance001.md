# CandidateAcceptance001 — bounded implementation plan (v0.4.13)

Extend the reviewed v0.4.12 checkpoint; do not substitute A2 for A or bypass review.

1. Add a closed installed CandidateEvidence adapter for completed learning-cycle,
   CandidateRuns and CandidateEvaluations public receipts. Bind exact parent Core,
   candidate, recipe, dataset, code/environment, fixtures and review-only proposal.
2. Preserve legacy probe evidence format. Add explicit candidate-only profiles
   CORE/A2/A2B and directed replay edges A2B->A2 and A2->CORE. No arbitrary mixing.
3. Reuse qualification journal ownership and decisions; enforce current parent
   certificate eligibility, producer/reviewer separation and exact repeat checks.
4. Reuse the generation manifest/closure/publication and stage/controller owners.
   A fresh generation review and expiring single-use release grant are required.
   Existing replay grants do not authorize candidate publication.
5. Demonstrate the complete existing task->archive->review->snapshot->new A2 training
   path followed by independent qualification, staged publication, an A2B/A2/CORE
   task, current permission withdrawal behavior, explicit rollback and no duplicate
   mock external action. Do not rewrite the immutable learning proposal.
6. Add failure and real subprocess-crash tests. Preserve distinct inherited
   regressions, factor shared mechanisms, update schemas/logic/handoff/inventory,
   and verify the final extracted release.

Scope: one cooperating local worker, declared role identities, developer-visible
symbol tasks and fp32 reference execution. No production auth, Runtime permit,
learned evaluator/router, generic serving cache migration or packed ternary claims.

Implementation source guards are point-in-time checks, not cross-store leases.
Qualified transition claims remain restricted to the four installed input pairs.
The inherited managed-stage controller can preserve broader portable task state;
new candidate neural recovery in this demo is restricted to its qualified fixture.
