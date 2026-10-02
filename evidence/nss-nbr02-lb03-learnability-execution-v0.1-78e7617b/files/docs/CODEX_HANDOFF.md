# Codex / research-group handoff — LB03-LEARNABILITY v0.1

## Current boundary

Pass 61 is a completed, user-authorized low-bit-training comparison. No follow-up, post-learning repair or companion integration is dispatched. Read `REPORT.md`, `SOURCE_RECONCILIATION.md`, `CANDIDATES.md` and the original pre-main `PROTOCOL.md` before interpreting the headline.

Complete archives 55–59 and context archive 60 were recovered: 2,909 payloads verified, with 24 exact model-lineage checks. The historical pass-57 budget overrun, incomplete ancestral training data, and unlogged tail costs remain explicit. No historical scientific result was rerun to repair documentation. Complete original ZIPs are supplied separately; the new study includes every selected starting checkpoint, input and source file needed for its own comparison.

## Actual experiment

Four inherited parents, 4101–4104, crossed with three master modes and two learning regimes yield 24 branches. Each received 512 updates. All **12,288 main updates** completed with no interruption or repetition. The 24 preflight, 102 timing and 24 audit updates are additional: **12,438 total**, below the 12,576 cap. The 45-file main lock and 192-file endpoint lock remain unchanged; all final models were sealed before confirmation.

Every branch uses Q2 forward matrices, FP32 effective tensors, gradients, training activations and biases, a custom M8 optimizer, and local FP64 update arithmetic. Persistent matrix masters are FP32 or FP16. No full FP32 master shadow or residual is retained in either FP16 candidate. All parameters remain eligible to learn.

EARLY starts from exact pass-57 Q2_M8 step 0: 512 A + original-B updates. It is not a new random fit. NEW independently starts from step 1024, reverses cues 2 and 5 in opposite directions, and performs 512 A + current-B updates. Old-task practice is concurrent from the start; there is no later repair phase.

## Outcomes that must stay separate

| Primary final result | M32 control | FP16 nearest | FP16 stochastic |
|---|---:|---:|---:|
| EARLY correct events / 32,768 | 32,732 | 32,760 | 32,742 |
| EARLY whole histories / 1,024 | 1,016 | 1,022 | 1,016 |
| EARLY false DONE | 1 | 0 | 7 |
| NEW current cue answers / 32 | 32 | 32 | 32 |
| NEW old-task events / 32,768 | 32,746 | 32,746 | 32,740 |
| NEW whole histories / 1,024 | 1,016 | 1,012 | 1,013 |
| NEW false DONE | 7 | 9 | 6 |
| NEW retention-screen parents / 4 | 3 | 2 | 3 |

Both candidates genuinely learned. Stochastic passes the frozen three-of-four complete screen separately in each regime, but only parents 4101 and 4103 pass both regimes. Nearest fails the NEW cohort. Do not describe either as uniformly reliable or generally equivalent to FP32.

Named master/gradient/moment arrays fall from 183,650 to 147,938 bytes (19.45%). The broader observed storage union falls by only about 1.41%; it is not simultaneous peak RAM. Nearest is 5.2–6.3% slower and stochastic 8.9–11.7% slower in the small parent-4101 timing comparison. No energy or throughput benefit is established.

## Numerical warning that must not disappear

The inherited naive NumPy sigmoid formula overflowed internally during NEW evaluation. Tested logits and states remained finite; the original precision and class-agreement gates passed. A separately frozen post-result stable equation agrees within that same tolerance, and all raw outputs replay bit-exactly. Gate inputs range approximately from −1,211 to +1,482; 10,587 repeated evaluated sites exceed the naive exponential's range.

Do not summarize this as “no numerical issues,” “every intermediate is finite,” or long-run plasticity qualification. Large saturated gate values remain a robustness concern. The stable audit explains output agreement; it does not retroactively replace the frozen implementation or establish the cause of the large inputs.

## Review priorities

1. Verify source and starting-state mappings, particularly the common optimizer reset versus source optimizer state retained only as evidence.
2. Check there is no hidden FP32 master/residual; inspect transient effective-matrix and saved-activation lifetimes.
3. Inspect every parent, separate-regime qualifications and their intersection rather than reporting only the best aggregate.
4. Review saturated-gate and optimizer behavior before extending the numerical claims.
5. Check tests and raw answers under explicit SET/CLEAR/RESET/NOOP semantics.
6. Confirm matched information, update exposure and budgets, with no selected seed or endpoint.

All 336 arrays were independently recounted and replayed; 120 checkpoints and 120 exports verified. Six four-update suffix/RNG replays matched, and 24 corrupted checkpoint copies were rejected. No independent external review has yet occurred.

The reproduction wrapper's help/compilation was checked. Its full retraining route was not executed; it does not imply another 12,288 updates. Individual scientific drivers and the full saved-output audits were executed. Code/checkpoint licensing and provenance need review before public release. Nothing was pushed to GitHub.
