# Codex review handoff — SURFACE01 Execution v0.1

Disposition: **STOP_BASELINE_COMPETENCE**, not a completed update-surface comparison.

The owner dispatched the preceding SURFACE01 proposal. The implementation items were frozen before four new parent fits. All four received 2,000 updates; no replacements or extensions. Preflight used 48 applications including exact fresh-process resume checks. Total 8,048 applications. Main B adaptation: zero. Main confirmation: not generated.

Three parents were perfect on their own admission panels. Parent 4103 made six false-DONE predictions in one idempotent history (8,186/8,192 correct suffix events; 255/256 whole histories). Only its zero-false-DONE criterion failed; its other accuracy thresholds and B screen passed. Cohort rules therefore blocked all correction contexts.

The case is in `failures/parent_4103_idempotent_first.npz`: row 120, prefix length eight; absolute events 17–22 / suffix positions 9–14. Correct answer stays item 5. Repeated SET(1), two NOOPs and repeated SET(3) leave exact mask 223 unchanged, but the prediction becomes DONE and its assigned probability rises to 0.994094. Actual SET(5) at event 23 makes DONE valid; do not call that learned recovery. The failure is within the 32-event training length, before any main correction.

Retained-array analysis shows mask 223 in 49,823 training events and the immediate idempotent SET(1) transition at that mask 1,389 times. This rules out absence of that exact symbolic mask/transition, not lack of a sufficiently learned history-dependent representation. A predeclared sample of 160 actual training streams had five wrong events in one stream; no false DONE. Capacity, objective, optimizer and representational causes are not isolated.

Independent full-trajectory numerical checks passed without tolerance changes. Fresh-process replay matched all four parent panels exactly. All eight injected fault controls were detected. Model tensor hashes checked for all 33 retained checkpoints. These are internal checks, not independent scientific replication. This execution does not repair the historical STATEBRIDGE numerical gate.

Review should check: adherence to the frozen gate and exact numerator scopes; the boundary between admission and unopened confirmation; complete artifact/manifest preservation; adequacy and limits of the reference and fault tests; and whether the failure suggests a better versioned baseline semantic-invariance diagnostic. Do not reinterpret the result as an update-surface comparison or choose a model topology. Do not automatically rerun training or relax a gate. Historical tri-core is not a required successor architecture.
