# OverlayCatalogController001 — pre-implementation decisions

1. This is deterministic LOCAL catalogue selection, not a learned router or serving
   backend. Exact case-sensitive capability labels and integer costs are reviewed
   fixture declarations, not new neural competence or energy/VRAM measurements.
2. One descriptor binds one exact generation manifest. It must describe every
   released profile, including CORE, and cannot add a subset/union. Profile ECIDs
   and sealed-JSON document byte counts are checked by the generation owner.
3. One profile must satisfy ALL requested labels. Mode, input-size and resource
   constraints apply before cost ranking. Only an explicitly qualified directed edge
   may change a task's profile; unchanged profile is a portable-record advance, not
   latent-state reuse. Lowest declared cost wins; ties retain the current profile
   where possible, otherwise request clarification. No inferred reverse/fallback.
4. The generation journal remains the sole owner of managed tickets and portable
   task heads. New typed catalogue/task events update tickets and task records in ONE
   transaction. No new catalogue database, separate current pointer, or neighboring SQL.
5. Reuse the existing TaskRecord semantics via factored portable-record helpers;
   the old integer RecoveryStore/handoff remains a separate verified consumer. Do not
   represent neural ECIDs as integer-fixture ECIDs or claim its caches were migrated.
6. Fresh tasks may select an approved WORK profile from portable initial inputs (no
   preexisting neural state). CONTROL/EVALUATION stages require CORE. Once a task
   exists, closing/reopening it cannot bypass transition checks; task IDs are not reused.
7. A handoff requires a finished source stage, exact source revision, fresh evidence,
   verified mock-action receipts, and complete required source fields. It preserves
   input pairs, facts, assumptions, clarifications, results, constraints and receipts.
   New ticket/state identity invalidates prior caches, even when weights stay the same.
8. Read/admission recheck current generation, exact descriptor, qualifications and
   dataset/source eligibility. Inspection/retry receipts are history, not permission.
   History may be finalized/cancelled after revocation, but no new stage/read is admitted.
9. Unfinished work remains pinned across restart. Explicit cancellation retains its
   record and all verified receipts, with a reason. Unknown/uncertain external effects
   block closure until reconciled by the existing ledger owner. This controller never
   performs or retries an external action, and does not manage arbitrary live outputs.
10. Test real stage transactions/crash windows, descriptor tampering, stale source,
    receipt drift, qualified transitions, unavailable/ambiguous selection and budgets.
    Keep unique regressions; factor repeated code instead of deleting meaningful tests.

## Source review refinements before final verification
- The generation owner is extended with typed catalogue/task events, not a second
  checkpoint store. Its pure query functions are extracted unchanged into one
  shared module so the release/task reducers cannot copy different rules.
- Portable source completion and record preservation/finish helpers are factored
  from the older StageHandoff001 path; both consumers now use those same rules.
- Exact costs are declarations. Actual serialized-artifact lengths are checked;
  the descriptor does not claim tensor residency or measured latency/energy.
- Whole-family eligibility is currently rechecked conservatively. Withdrawal of a
  prerequisite blocks selection rather than silently inventing a smaller fallback.
11. The journal extension uses named CATALOG_REGISTER/CATALOG_TASK events and new
    versioned controller command bodies, while retaining old event semantics.
    Old readers reject unknown kinds. New-reader/old-history compatibility does not
    imply downgrade compatibility after new task events have been written.
12. Failure after a successful commit never pretends that commit was rolled back.
    A subsequent current-use read can fail while the published task remains pinned;
    historical receipt retrieval is distinct from authorization to run it again.
