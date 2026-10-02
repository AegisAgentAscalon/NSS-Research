# NSS-NBR02-DC01 — preflight stop and failure analysis
## Execution v0.4 / integrated scientific protocol v0.3

**Status: STOPPED_AT_STORAGE_ADMISSION. The main learning study was not run.** The fixed derivative diagnostics, clean integration fixtures, bounded detector checks and two 50-update cost probes completed. A fresh process reproduced that same completed prefix and the same admission stop. This is neither a learned scientific pass nor a learned scientific failure.

The natural blocking failure was the **implementation's conservative estimate of delivery size**, not exhausted disk/RAM, incorrect learning arithmetic, or a failed immediate-feedback learning gate. A0, the main fit/development stage, and held-out D2/D3 were NOT_REACHED. No held-out labels or concrete held-out streams were generated.

## 1. What failed, exactly

The cost pair produced 835,336 bytes of additional `records.bin` data for 100 total update applications. Before any main fit, the frozen implementation extrapolated:

- measured 8,353.36 stored bytes per probe update;
- 4,424 total applications in one complete pass, including fixtures;
- an implementation-chosen **2× conservatism factor**;
- 18 MiB reserved for non-update evidence/metadata;
- exact adaptive-replay deduplication assumed only after actual byte equality is verified.

The result was **92,784,897 bytes (88.49 MiB)** against **67,108,864 bytes (64 MiB)**. The difference is 25,676,033 bytes. Both fresh executions obtained the same measured growth and projected size, and both stopped at `driver.py`'s `STORAGE_PROJECTION_FAIL` boundary before main initialization/fitting.

This formula was written into the implementation completion record and source lock before numerical work. It is **not a scientific threshold supplied by Codex**, nor an observed full-study archive size. Its 2× allowance is a conservative engineering choice made in this implementation. The frozen protocol requires feasible delivery before main fitting; it does not prove that this particular extrapolator is tight.

Without the multiplier, the same simple extrapolation plus reserve is 55,829,632.64 bytes (53.24 MiB), below the gate. **That is not a demonstrated safe full-run bound.** Dropping the factor solely to continue would waive the very admission check whose failure we are preserving.

An additional post-stop review found that the `fixed_full_raw_schema_bound` check copied the proposal's 209 MiB component allowance and compared it with the cap; it did **not** independently derive a complete worst-case count of every actual serialized field. Its boolean must not be reported as a proved raw-schema size bound. This is a second, documented admission-readiness gap. No main experiment was admitted on its basis.

### What the first failure tells us

The last verified numerical boundary is correct update application and durable checkpointing through both cost probes. The first natural failing boundary is the **full-run evidence-size forecast**. The mechanism causing that software stop is independently reproduced arithmetic. Whether the complete study would actually exceed 64 MiB is **unresolved**, because it was never generated.

This is an engineering issue to address with better component accounting and lossless delivery, not evidence that eligibility learning fails. It does not justify reducing seeds, deleting failures, relaxing scientific gates, or reusing probe weights as main fits.

## 2. What numerical checks did work

The four frozen derivative cases were run for both methods. Diagonal cases matched the exact derivative under the unchanged empirical tolerance. In the coupled zero-state witness, the exact encoder-gradient squared norm was 47/32 and the squared difference from the approximate rule was 3/8, giving relative discrepancy **0.5052911526399113**, as derived before execution. The difference is intentional; its U gradient is zero in that particular witness. The nonlinear cases separately exercised nonzero state and U derivatives.

All captured G gradients matched independent NumPy reverse differentiation. All captured L gradients matched an independent implementation of the declared local recurrence. Correctly implemented L could differ substantially from the exact derivative calculated at L's own pre-update weights; those differences remain measurements, not implementation-error flags.

The complete prefix audit checked **306,968 scalar comparisons per pass**, with maximum empirical tolerance ratio **0.04156** (failure would require a ratio above 1). It reconstructed forward states, local traces, logits, probability outputs, raw gradients, clipping factors and resulting parameters. The check uses `2e-6 + 2e-5*abs(reference)`, not a proved numerical bound and not Q010's old underflow amendment.

The 12 clean fixture updates per pass crossed two diagnostic labels and three delays (0, 8, 32) for G/L, resetting the fixture model each time. All 12 post-update scratch queries were correct. Per-method equal-delay checks matched **88 arrays / 24,960 elements**. This is a tiny fixture result, not four-fit learning competence or full condition-stream delay qualification.

## 3. Deliberate failures versus natural failures

The 14-category detector catalogue was exercised through a mixture of pure state-machine checks, copied numerical records, a small separate intent-only process, a bounded synthetic quota sink, package/schema checks, and actual sandbox updates. Each recorded its declared clean/tolerated control.

**Eight actual intentionally wrong update applications per pass** crossed G/L, two targets, and sign-reversal/double-step defects. The independent audit found the raw derivatives valid and the committed parameters inconsistent with the prescribed SGD step, exactly locating the injected defect at application. Those weights were isolated and never used for any scientific fit.

Other checks covered unknown/consumed/wrong-scope receipt envelopes, missing feedback, mutated trace copies, stale versions, wrong replacement logits, local-factor omissions, unreleased-field/schema rejection, lost commit, missing/altered members, logging quota, post-feedback predictions mislabeled as raw predictions, missing report fields and an authenticated false-outcome detection limit.

**Coverage limits:** these are bounded detector tests, not comprehensive fault coverage. The wrong-live-graph construction was not run as a separate neural backward. Some receipt and recorder checks used isolated synthetic helpers rather than the full runtime path. The later six-transaction per-fit live rejection diagnostic was NOT_REACHED. Retained source, fixture outcomes and base numerical arrays define the copied mutations; temporary corrupted memory copies were not separately claimed as captured full-runtime failures. The final delivery was tested separately using real extraction and re-scoring.

The authenticated wrong-label example deliberately remained undetectable from its public fields. The scorer's private truth was not used to reject it in a learner.

## 4. Cost-probe observations, not efficacy conclusions

The two fixed cost-only fits each completed 50 updates on old cues and were discarded. Their earlier predictions were recorded before the current outcome was released:

| Cost arm | Correct raw predictions | Incorrect raw predictions |
|---|---:|---:|
| G | 43/50 | 7/50 |
| L | 42/50 | 8/50 |

Those counts describe one paired initialization and a repeated old-cue teaching schedule. They are **not** development A0, held-out adaptation, retention, noninferiority or generalization results. They did not select a seed, learning rate, checkpoint, architecture or longer run.

The mean relative encoder-gradient difference between the local equation and the exact derivative **at L's own prestate** was about 0.6468 across its 50 updates (maximum 0.8008). This is a relative vector-norm diagnostic, not a 64.68% prediction-error rate. Its effect on the main learning/retention outcomes remains untested.

All 15 raw cost-probe prediction errors remain. A post-stop grouping found three first-exposure errors in each arm, plus four repeat-after-feedback errors for G and five for L. These are observed timing categories, not proof of a particular learning defect; the last such sampled errors occurred at trials16 and18 respectively. Six raw clean-fixture errors, four sandbox pre-update errors and two derivative-case raw errors are also retained separately. All 12 clean-fixture post-receipt answers were correct. Those diagnostic repetitions and replay do not add independent task samples.

## 5. Attempts, evidence and replay

| Work across original prefix plus fresh prefix replay | Actual | Original full-run ceiling |
|---|---:|---:|
| Update applications | **240, all committed** | 9,800 |
| Of which cost-probe updates | 200 | Included above |
| Clean fixture applications | 24 | Included above |
| Deliberately faulty sandbox applications | 16 | Included above |
| Recurrent transitions | **1,160** | 400,000 |
| Head evaluations | **280** | 60,000 |
| G backward calls | **128** | 5,000 |
| Main models fitted | **0** | Eight proposed main arm/fit combinations |

Every real updater attempt has a matching durable commit. There are **no unknown-completion neural updates**. The synthetic FF09 lost-commit process is explicitly separate: it executed no learner mutation. The worker was terminated by its scheduler at the admission exception rather than exiting through its normal finish command; its last evidence frame and all 120 update commits per pass were durable and checked.

Fresh-process prefix replay independently reinitialized and repeated the diagnostics, fixtures and cost-probe optimization. It matched **442 record frames, 1,266 arrays / 563,260 numerical elements**, the public message stream, private instantiated inputs, complete event hash chain, and ten stage-level scientific CSV outputs. It reproduced the same storage admission failure. No third learning run occurred.

The source lock's 30 source/protocol identities remained unchanged. The scoped historical scan checked 12,319 directly accessible text members for the 120 new seed values; it found no collision. Nested compressed/binary evidence and unknown historical RNG draws were outside that scan. Labels, orders and 544 prefit input transactions were checked without generating held-out labels.

Peak sampled process-tree RSS was **611,106,816 bytes**; peak sampled container memory was **1,607,864,320 bytes**. The shared clock through the replay stop was **544.84 seconds**, including implementation. Sampling was 0.1 seconds; the initial inspection/copy prelude was not continuously measured. No actual disk, memory or wall limit was reached. The delivered prefix is small; that does not establish the size of the unexecuted full study.

## 6. Post-stop engineering measurement and next proposal

Without any new model computation, the retained primary `records.bin` was decoded and its exact frame envelopes recompressed together with XZ. The bytes round-tripped exactly:

| Retained-prefix representation | Bytes |
|---|---:|
| Current individually zlib-compressed frames | 1,050,202 |
| Decoded frame envelope stream | 1,871,760 |
| One lossless XZ envelope stream | 542,940 |

This exploratory, post-stop measurement suggests avoidable per-frame compression overhead. It does **not** prove full-study fit or authorize resuming the closed run. Its purpose is to propose an evidence-backed codec/admission revision rather than waive the failure.

The next focused engineering change should (1) derive per-component bounds from actual serialized shapes/counts, (2) validate a compact lossless envelope on these retained probes without reusing their fitted weights, (3) include JSONL, RNG/cursor records, all negatives, failed attempts and genuine replay evidence, and (4) pass a versioned cost gate before the unchanged scientific main study is authorized to continue. No model, learning rate, seed, target, threshold, fit count or data split needs changing to address this blocker.

## 7. Program and architecture status

NBR-01 remains CLOSED_BOUNDED_RECOVERED_EVIDENCE. NBR-02 DC01 is **PREFLIGHT_BLOCKED**, not scientifically qualified or closed. `RET-DC01-DELIVERY-001` records this readiness blocker. `RET-MW01-FIT-001` remains PARKED_OPEN. `FCR-0103-001` still schedules revisiting the unresolved 01–03 foundations after NBR-03 and before NBR-04. No NBR-03 or NBR-04 test is dispatched.

The maintained-token concept, frozen NSS role boundaries, parent Architecture Ledger and all historical Q010 evidence gaps remain unchanged. Historical models were neither loaded nor trained. The old underflow amendment was neither altered nor used for this new tanh/gradient audit. All G01–G22 questions remain in `protocol/PROGRAM_CONTEXT.md`.

**Conclusion:** the update arithmetic and a bounded set of failure checks survived preflight, but the implementation did not earn permission to start the main study. We know exactly which gate stopped it and how that gate computed its decision; we do not yet know the full experiment's learning result or true delivery size.

## Delivery verification

A fresh extracted copy verified all manifest payloads and frozen source identities. Independent relocation re-scoring reproduced ten CSV tables byte-for-byte with zero additional learner forwards or updates. The final external delivery receipt records the exact ZIP identity and final verification. No historical archives are needed to re-score this executed prefix.
