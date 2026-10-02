# NSS LB01-T3-TARGET — Model-only ternary working-point test
Version 0.1 · 29 September 2026 · Prospective specification

## Question and scope
Can an existing useful two-bit checklist model be converted to a useful scaled ternary model, and does a gradual switch preserve its skill better than an immediate switch? The owner authorized the next target after explicitly restricting the phase to MODEL quantization. All training here is fixed-budget preparation to obtain the target weights. No training-efficiency intervention, new association, repair after new learning, optimizer compression, master precision comparison, new backbone, HSA or DARP is introduced. This is a small GRU study, not a BitNet Transformer reproduction.

## Parents and comparators
Reuse all four exact LB02-Q2-TRAIN Q2_M32 step1024 masters (4101–4104), with original A task and original eight B associations. No selected winner, new random parent or post-correction checkpoint. All arms for a parent start with identical FP32 master tensors; each starts fresh FP32 M32 optimizer state. Previous preparation costs remain inherited, not free or equal to training from scratch.

Three arms each receive 1,024 additional identical A+original-B batches, comprising the parent's 64 retained 32x32-event batches repeated 16 times:
- Q2_CONTROL: unchanged four-code affine row quantizer throughout.
- T3_DIRECT: original LB01 per-row absmean signed ternary quantizer from the first update.
- T3_RAMP: effective matrix `(1-a)Q2(W) + a T3(W)`, with `a=(i-1)/511` for steps1–512, then a=1. This temporary mixed representation is NOT ternary during the ramp. The final512 updates and deployed endpoint are fully ternary.

The only intervention is the forward matrix representation/switch schedule. Biases, GRU graph, hidden width64, original 18,249 coefficients, A/B targets, loss, batches, optimizer and schedule stay fixed. No activation quantization, update speed optimization or comparison of learning-state compression. All matrices including readout are quantized. Four-step model registration does not add learned parameter counts.

## Quantizers and fixed preparation
Q2 exactly reuses `quant2/hard_q2` from the source archive. T3 for each row uses `s=max(mean(abs(W)),1e-8)` (float64 reduction, stored FP32), `q=clip(round_even(W/s),-1,1)` and hard forward `s*q`. Scales are derived, not learned. Identity straight-through backward is a declared surrogate; it is not the exact derivative of discrete rounding. The ramp uses an identity surrogate through its hard mixture.

Use unchanged custom C M32 Adam: beta .9/.999, epsilon1e-8, no decay, clipping1, FP32 masters/gradients/moments with double local optimizer arithmetic. Learning rate cosine .003→.0003 across1,024 updates. No phase resetting within the comparison. Original eight B cues remain0,1,0,1,0,1,0,1. Final endpoint is fixed at1024;256/512/768 are development-only diagnostic curves and are never selected as better confirmation endpoints.

## Public test contract
Eight items initially unfinished. SET(i) completes i until CLEAR(i) or RESET; CLEAR reopens i; RESET reopens all; NOOP changes nothing. Answer the smallest unfinished index, or8/DONE only when all are done. Inputs are event codes only; no target checklist masks, labels, checker feedback, sentence summaries or external correction is provided. Task B is eight original zero-state cues. All answers and logits are retained unmodified.

## Fixtures and endpoint evaluation
Fresh deterministic panels, seeds and sizes fixed in CONFIG.json: development16 (24+32events), confirmation256 (24+32), stress64 (64+192). Balanced mixed/idempotent/revision/reset families. Exact histories and32-event windows excluded against the accessible replay subset and copied LB01/LB02/MASTER16 panels, and earlier generated panels. Not all historical ancestral training streams are available; known rules, primitive states and shorter patterns recur. Generation and hashes freeze before main fitting.

Primary policy: REBUILD from zero under each candidate's own quantized weights, reading all prefix and suffix events. No old-state CARRY hypothesis or changed-weight task migration in this pass. Reference evaluations: original float parent, unchanged Q2 prepared parent, initial directT3 conversion; candidate final endpoints. Curves use only development. Evaluate the same histories for every endpoint. All confirmation scoring occurs after all12 fits finish. Prior case IDs/results are not used for tuning.

Each final Q2/T3 is exported to real packed codes and compared against separately decoded NumPy equations and built-in Torch GRUCell arithmetic. Original C kernels read packed weights without retaining a dense weight matrix. Inference hidden state, gates and accumulations remain FP64. Per-row scales and393 biases remain FP32; the full model is not1.58bits/coefficient, nor native integer arithmetic. No throughput superiority is sought. Record numerical body, complete file bytes, resident arrays, preparation time and sampled process memory.

## Decisions fixed before evaluation
Per-parent primary working point: event accuracy>=98%, whole continuations>=90%, event loss from its own unchanged preparedQ2<=1percentage point, zero newly induced falseDONE at Q2-correct positions, all8 original B classes correct and minimum assigned target score>=.80. Three of four parents required for a nominal ternary cohort working point. Report immediate and ramp arms separately; no pooled winner assembled per parent. The long-stress panel uses the same absolute98%/90% thresholds and zero additional falseDONE relative to Q2 as a SEPARATE robustness screen. Stress never substitutes for a primary failure, and primary never conceals a stress failure.

Compare candidate vs Q2 parent and matched Q2 continuation, per family and parent: whole accuracy, raw errors, pre-existing/gained/lost errors, falseDONE and original B scores. No significant/equivalent/population claims from repeated events or four inherited model clusters. A favorable direction for ramp is descriptive unless consistent quality warrants it; no rule requires it to win. A practical two-bit result remains useful if ternary misses. No post-result gate relaxation, fourth arm or additional update budget.

## Failure-first and semantic review
Preflight includes all4608 state/event truth pairs under independent bitmask/set implementations, all243 five-trit and256 four-code byte patterns, padding/corruption rejection, exact quantizer endpoints, ramp endpoints, identity-surrogate gradients, all-parameter gradients, optimizer arithmetic and exact resumption on disposable copies, parent immutability, explicit full-precision/bias accounting, and Torch/NumPy/packed whole-trajectory numerical tests. Fixed comparison envelope `1e-9+1e-8*abs(reference)` matches inherited inference contract; this compares equivalent weights, not quantized vs float parent behavior.

For every scored array preserve full input fixture, unedited logits/predictions, true targets, prefix and source/model identities. Independently recount with set semantics. Eight prospectively listed primary histories span all four families, including passes and failures; show all events and final candidates. Add first errors as explicitly retrospective examples. Finite-rule coverage is not an independent semantic language critic or private-chain-of-thought review.

Exact evidence/integrity errors stop rather than repairing an answer. Behavioral failures are retained and do not suppress other valid arms. Full logged numerical violations stop their profile and make its technical status explicit, with raw evidence retained. Preserve bug source/traceback before prelock repairs. Never call a known unfinished transaction complete.

## Budgets, durability and audit
12×1,024=12,288 maximum ACTUAL main applications; up to48 disposable preflight applications; total<=12,336. Run bounded synchronous chunks, checkpoint every64 updates with journal step reconciliation; durable full source/optimizer/RNG checkpoints at0/256/512/768/1024. Automatic replay of an unknown tail is NOT authorized. On mismatch stop affected arm; retain partial result instead of exceeding actual work cap. Per branch accumulated measured wall<=180s, per process peakRSS<=2GiB, evidence guard224MiB with explicit failure receipt reserve. Source/compiler/model startup and document/packaging costs separated; sampled caps not OS sandbox. Check storage before and after declared checkpoint/evaluation writes; actual individual-write race remains bounded not concurrent shared-write sandbox.

Post-result independent recount of every array; fresh-process re-evaluation of all saved model/panel profiles; packed payload decode and hash checks; unchanged source/fixture/parent locks. Selected restart after a split within inference must reproduce full run. Audit does not train. No old archives merged or models rescored as historical qualifications. SHA/CRC are integrity checks, not independent scientific replication or publisher authentication.

## Stopping
Publish the new protocol, source, original identities, checkpoints, packed candidates, all outputs, failure evidence, audit, report and checklist update. Then stop. No additional phase or movement to training research follows automatically.
