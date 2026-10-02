# Logic Atlas reconciliation map — design only

This map references the actual flow IDs in the reviewed 25-flow schema-v2 Atlas. It does not replace, patch, regenerate, or claim to validate that repository. The new `sources/flowcharts/flows.json` is a documentation graph format, NOT an Atlas schema migration.

| Existing flow ID | Decisions | New figures | Proposed cases | Required reconciliation |
|---|---|---|---|---|
| master | D01-D08, D12-D15 | F01-F02 | LT-01, LT-06, LT-07, LT-11 | Separate live work, persistent records, candidate training, independent qualification and release. |
| core | D01-D03, D07, D12-D14 | F02-F03, F07-F08 | LT-07, LT-10, LT-14 | Core-only is mandatory; learned router/evaluator proposes rather than owns execution authority. |
| token_context_abi | D03, D15 | F02-F04 | LT-02, LT-14 | Preserve fixed tokenizer/ABI; revalidate TaskRecord fields for destination. |
| context_manager | D03, D15 | F03-F04 | LT-02, LT-03 | Preserve exact source refs/units and support bounded overflow/rehydration. |
| compute_discipline | D02, D10, D15 | F03-F04, F10 | LT-12, LT-13 | Charge loading, rebuilding and validation; stay is valid, repeated switching is bounded. |
| working_ar | D01-D03, D09 | F03-F04 | LT-02, LT-03 | Use portable typed stage handoffs; distinguish facts, assumptions, unresolved information and receipts. |
| overlay_index | D01-D02, D11 | F03-F04 | LT-01, LT-14 | Use evaluation-backed QAP metadata; reject unqualified unions even when components are individually valid. |
| overlay_runtime | D01-D03, D15 | F03-F04, F09 | LT-01, LT-03, LT-14 | One active set per stage; qualified directed edges including return to Q0; validate before no-op shortcut. |
| overlay_generation | D06-D11, D15 | F06-F07 | LT-04, LT-07, LT-09 | Freeze release membership; reuse unchanged artifacts only explicitly; new profiles/edges need qualification. |
| memory | D04-D06, D15 | F05 | LT-04, LT-05 | Separate raw evidence, interpretations, corrections, retrieval and training permission. |
| experience | D04-D06, D11 | F05-F08 | LT-04, LT-05, LT-09 | Persistent lineage, failed/corrected cases and immutable snapshot selection; do not replace evidence with retellings. |
| knowledge | D04-D06, D12 | F05, F08 | LT-04, LT-05, LT-10 | Approved knowledge updates may serve retrieval immediately; stale facts alone do not trigger a Core successor. |
| builder | D04-D09, D12-D14 | F05-F08 | LT-04-LT-11 | Human-assisted curation, scoped autonomy, training proposals and supported Core-fitness diagnosis. |
| overlay_trainer | D06, D09-D11 | F06 | LT-04, LT-09, LT-12 | Fixed approved snapshot and recipe; Core frozen; train intended profiles/handoffs; test actual numerical path. |
| qualification | D07-D08, D11, D13 | F06-F08 | LT-07-LT-09, LT-11 | Accepted Core-only evaluator is a learned witness, not release authority; protect test exposure and thresholds. |
| generation_intent | D03, D15 | F10 | LT-02, LT-13 | Carry verified content/constraints; do not rewrite checked results merely to impose style. |
| directional_guidance | D15 | F10 | LT-13 | Keep positive/negative origin explicit; do not invent an exclusion from a generic prompt. |
| darp | D10, D15 | F10 | LT-12, LT-13 | Optional mechanism; same applicable validation and output-commit boundary as AR. |
| action_boundary | D03, D15 | F09-F10 | LT-03, LT-13 | Durable action/output receipts, provider-scoped idempotency, uncertainty blocks blind replay. |
| checkpoint_recovery | D03, D15 | F04, F09 | LT-03, LT-14 | Pin ECID; reconcile outside-world effects; rebuild permitted computation; preserve source until publication. |
| core_upgrade | D12-D14 | F08 | LT-10, LT-11 | Evidence-driven successor proposal, separate approval/train/qualify/release, unchanged parent and complete source lineage. |
| nexus | D05, D08, D14-D15 | F01-F02, F06-F09 | LT-06-LT-08, LT-11 | Per-operation authority, revocation, exact artifacts; host permission does not replace runtime permit. |

Unchanged optional-research boundaries: `recurrent_depth`, `ambiguity_gate`, and `multimodal` retain their reviewed interfaces. Their integration still obeys the stage, validation and resource policies above.

## Implementation gate
Start from the user-confirmed repository baseline. Reproduce its tests before any edit. Reconcile one narrow interface/flow at a time, preserving outcome codes, cycle-budget rules, failure-reason propagation, action receipts and publication semantics. Add concrete validators/fixtures before promoting a proposed case to an executed test. Do not replace the reviewed 25 flows with the ten overview diagrams.

Any behavior-changing code requires a versioned repository pass and retained before/after evidence. No new neural training, Runtime adaptation, or automatic self-approval is authorized by this document update.
