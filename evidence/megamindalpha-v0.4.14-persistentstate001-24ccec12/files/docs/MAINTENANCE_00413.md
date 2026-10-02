# Maintenance and change accounting — v0.4.13

## What was reused instead of duplicated
- Existing Qualifications journal owns both closed evidence formats. CandidateEvidence
  reads public numerical/archive/snapshot/cycle receipts; it owns no database or approval.
- Common neural state/predict/replay mechanics are factored into FrozenSlotSession;
  original and candidate sessions retain disjoint slot names and exact catalogues.
- Existing replay observations now have one implementation in neural_checks. The
  verifier creates only an isolated mock marker; it never repeats the user's effect.
- Shared CLI source selection is defined once for qualification/generation/catalogue/
  context. The legacy flags remain supported; mixed and dynamically loaded sources fail.
- Learner-owner config validation and the complete task-to-candidate fixture were
  extracted rather than copied into the acceptance demo and tests.
- Existing schema and graph tools generate the new closed formats and three helper
  graphs. No new generator, store, global manager or arbitrary plugin engine.

## Stale assumptions corrected, not safety gates removed
The original `claim(...)` API remains legacy-strict. New A2/A2B parsing requires the
explicit CandidateEvidence001 format. This avoids broadening a legacy acceptance rule
merely to make new tests pass. Its inherited unknown-profile regression remains intact.
The actual learner producer is checked independently of the request submitter so a new
submitter label cannot bypass self-review separation. Parent qualification is checked
before costly verification and again before commit.

Prior NEXT_STEPS remains in PREVIOUS_HANDOFF.md as historical audit material. Active
README/handoff/inventory no longer claim that new-candidate adoption is missing. The
learner's own proposal-only stop remains correct, with downstream acceptance separate.

## Actual size changes
Physical lines include comments; these are not runtime-cost measurements. No claim of
net code shrinkage or speedup follows. Distinct regression tests were preserved; new
crash/mutation cases share a genuinely trained fixture and parameterized mechanics.

| Python area | Before | After | Added / removed lines |
|---|---:|---:|---:|
| nss_base | 10186 | 10708 | +650 / -128 |
| tests | 7047 | 7700 | +653 / -0 |
| tools | 1126 | 1201 | +89 / -14 |

No inherited test file was modified or deleted. There was no proven redundant old
behavioral regression to remove this pass. Removing tests solely to shrink the number
would be the wrong optimization. The closed-format boundary is covered by old and new
regressions instead. Exact lists and counts are in the current CHANGE_ACCOUNTING.json.
Static import checks cover reviewed Python import edges, not arbitrary runtime behavior.
