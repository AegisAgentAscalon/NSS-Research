# Integrated failure-first evidence contract

**Requirement:** assume inputs, learning records, derivatives, updates, evaluators, logs and delivery can fail. The finite detector catalogue does not cover every possible failure, and a log cannot guarantee a proved cause.

## Evidence chain and required snapshots

Link each public cue to its fit/condition/trial, parameter version, three causal input IDs, raw logits, cue-time h, pending graph/trace identity, receipt validation, derivative, clipped step, committed post-state and subsequent raw/probe scores. Preserve all before-feedback predictions even when the primary metric is a later read-only probe. Required arrays are referenced by digest and location; hashes without payloads are not substitutes for them.

Record the first observable divergence and downstream affected outcomes without dropping any of those outcomes. Keep observation, inference and a causally tested mechanism separate. Cause states remain NOT_ASSESSED, UNRESOLVED, HYPOTHESES_ONLY, TESTED_LOCAL_MECHANISM or EVIDENCE_UNAVAILABLE. An injected sign bug proves the detector sees that injected bug, not that every naturally bad learning result is a sign bug.

## Critical change from the earlier exact-diagonal addendum

For G: disagreement with exact cue-time differentiation is a numerical/implementation failure. For L: disagreement with its stated diagonal-sensitivity recurrence is a numerical/implementation failure. Disagreement of a correct L with the full dense exact gradient is an intended approximation diagnostic, not a stop by itself. Apply the separate same-prestate exact auditor to characterize that error; never compare differently trained G/L prestates as if they were the same derivative point.

A cue trace mutated during fillers or a pending weight-version change is a retention-contract error for either method. If trace/formula/step are correct but learning is poor, classify the scientific competence or retention failure without inventing an internal cause.

## Durable attempt accounting

Before possible model mutation, durably append UPDATE_INTENT with global attempt index, phase, fit, condition/trial/receipt IDs, pre-state digest, rule/config digest and expected evidence destinations. Flush and fsync before updater dispatch. Write required post-state/gradient metadata atomically; append/fsync UPDATE_COMMIT only after required artifacts have been flushed. A completion acknowledgment has exactly one matching intent.

An intent without a commit means COMPLETION_UNKNOWN. Charge its attempt and identify the last durable checkpoint. Do not infer that nothing changed or reapply the same feedback automatically. G pending graphs are not claimed portable checkpoints; retain reconstructible causal inputs and actual saved forward tensors. A safe-boundary restart needs a documented allowed recovery with remaining budget; this proposal has no automatic mid-transaction rescue.

A lightweight independent supervisor tracks sequence gaps, last completed update, worker heartbeat and both process/container memory. Sample at0.1seconds; document missed sub-interval peaks. On a resource breach or loss of required evidence capability, stop the worker after emitting the best available incident receipt. Before scientific work, reserve a1MiB emergency status file within the output cap. It is a bounded fallback, not protection from simultaneous host/storage loss.

Use structured binary/JSONL event tables, immutable lossless array chunks and per-chunk checksums. A checkpoint digest is insufficient without the required parameter/RNG/cursor payload. Ordinary SGD has no momentum slots; state absence must be algorithmically defined, not a missing-history claim.

## Observers cannot help the learner

Worker inputs exclude hidden targets before release, independent gradients, diagnostic labels, future prefixes and private scorer decisions. Observers must not consume model RNG, change tensors in place, detach a required gradient path or repair output before scoring. Read-only probes use scratch h; their classification/loss outputs never feed later learning. Each arm pays its actual archive/index/observer cost; a second arm's shared physical operation is not an inherent speed advantage.

Use independently implemented semantic truth, exact-table X, raw decoder and gradient/update auditor. They may operate on full persisted evidence but cannot send a better answer or update to the learner. No application of Q010's historical softmax-underflow amendment to this new cell or verifier.

## Different dispositions

| Event | Action |
|---|---|
| Malformed/mismatched synthetic receipt | Expected rejection; zero updater call; retain pending digest unchanged |
| Deliberately corrupted sandbox update | Expected injected failure; isolate weights and evidence; never count as main learning |
| Natural engineering mismatch, illegal update or observer leak | Stop affected run as invalid/incomplete, preserving attempts |
| Development G failure | BASELINE_INCOMPETENT; no held-out generation |
| Development L-only failure | LOCAL_RULE_COMPETENCE_DEFICIT; no confirmatory delay contrast |
| Validly executed poor held-out prediction/retention | Finish the authorized finite evaluation; scientific negative |
| Resource or recorder failure | Preserve partial evidence and unknown-completion window; no quiet extension |
| Authenticated false label with no public warning | Explicit detection limit, not oracle-assisted validation |

## What the final report must answer

For each declared scientific/engineering test: pass, fail, not reached or not tested, with exact denominator and budget. For each grouped incident: observed symptom, last verified boundary, first mismatching boundary, affected outputs, plausible alternatives, diagnostics actually performed and remaining unknowns. Include waveform-like numerical trajectory evidence only where it supports those questions, not indiscriminate logging.

Retain all raw negatives, surprises, aborted attempts, failed cost probes, fixture faults and packaging errors separately. Report observation costs and blind spots. A perfectly replayed poor learner is still poor; a passed detector test is not automatically a learned scientific success.
