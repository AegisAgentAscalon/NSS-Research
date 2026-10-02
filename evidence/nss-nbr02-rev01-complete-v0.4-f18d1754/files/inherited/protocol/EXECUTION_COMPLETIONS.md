# DC01 execution completions v0.4 — frozen before numerical work

Scientific contract: integrated review v0.3, as authorized in the current user turn. No hyperparameter, sample, cue, threshold, or learning-rule change. Start clock 2026-09-25T05:14:17Z includes implementation.

## Enumeration and serialization
Phase strings: derivative, fixture, sandbox, cost, initial, warm, development, receipt_diagnostic, heldout. Session identifier is the first24 hex digits of SHA256(phase/arm/fit/base/delay/reversal/case), with missing integers -1 or0 and case empty. This opaque session string is the base string used for public receipt digest generation. kind=receipt. Fixed array order W,U,b,V,a. Public scope integers0/1 are the declared scope coordinates; only receipt/session IDs are opaque.

Workers receive only current cue/scope/receipt/context and sequential filler messages, then an outcome-bearing receipt; context is opaque session+trial, not reversal/base labels. Process file guards deny protocol, private input and auditor/generator sources. No independent gradient or gold label is returned to worker. Private scheduler and independent scorer legitimately retain whole source histories. This is concrete isolation, not a formal security proof.

Model state, exact gradient, local trace and head use deterministic Torch float32, vector shape fixed to single trials. Global norm uses concatenated row-major float32 gradient. Independent NumPy reference uses float64, same declared empirical tolerance. G uses a real 3-transition autograd graph. Its saved tensor/storage inventory is instrumented using identity-preserving saved-tensor hooks. Graph objects themselves are not serialized as portable checkpoints.

## Lossless durable evidence
records.bin consists of length:uint64LE + SHA256:32rawbytes + zlib payload. Payload: header length:uint32LE + canonical JSON header + array bytes. Within-pass array aliasing is performed only after actual newly captured bytes compare equal to a previously retained payload. Alias identity binds dtype, shape and SHA256; earlier retained arrays resolve all aliases. An alias is not a substituted model calculation. Each frame is fsynced before its commit event. JSONL log entries form a sequential hash chain. Each updater dispatch has fsynced intent, then durable gradient and post-parameters, then commit. An unmatched intent is completion-unknown. Replay uses a new worker, empty caches and independent regeneration/refitting; byte sharing across runs is permitted only after exact comparison.

Store all model parameter versions, raw gradients, clipping factors, actual three-step states/eligibility, filler states, query states/logits, checkpoint params plus Python/NumPy/Torch runtime RNG and private initialization/order/filler generator recipes/states. SGD has no momentum slots. Runtime no-ops do not invent nonexistent optimizer state. Probe checkpoints0/50; initial0/25/50/75/100; every condition/diagnostic end; clean/sandbox endpoints. Records keep all intermediate versions too.

## Bounds and monitoring
Declared 8,848 updates,330,584 cells,48,392 heads include adaptive replay; hard ceilings9,800/400,000/60,000 and5,000 G backwards unchanged. Recorder local cap per pass4,900updates/200,000cells/30,000heads/2,500backwards. Supervisor includes scheduler, worker and auditors, samples every0.1s, and stops on2h shared clock,3GiB RSS,3.5GiB container or256MiB new stored evidence. One1MiB emergency file is preallocated. Initial shell/read/copy prelude was not continuously sampled.

The declared full-component209MiB bound is checked against actual fixed dtype/shape allocations and cost-probe frame growth. Additional actual delivered-byte projection is two times measured dense-probe bytes/update times4,424, plus18MiB nonupdate/metadata reserve, assuming only a verified exact adaptive-replay duplication can be removed. Stop before main fits if projection exceeds64MiB or conservative time exceeds6,500s including work so far. This forecast is not a guaranteed compression/latency result; actual bytes remain hard-limited.

## Scoring and exclusions
Audit all pre-update gradients, pending versions, numerical state, local traces, committed steps and query outputs. Fault sign/double-step applications are intentionally wrong and isolated; independent audit must reject nominal SGD result and verify the intended defect. No natural bad prediction is engineering-stopped. All development conditions finish, then independent A0 decides whether to generate heldout. If A0 fails, replay the completed prefix only and mark heldout tests NOT_REACHED. Failed gates are not tuned.

No old Q010/CM/TS checkpoint is loaded. NBR-01 accepted bounded scope, RET-MW01-FIT-001 parked status and FCR-0103-001 roadmap remain. The parent Architecture Ledger is unchanged. All natural-failure explanations are graded as observations versus tested mechanics versus unresolved hypotheses.
