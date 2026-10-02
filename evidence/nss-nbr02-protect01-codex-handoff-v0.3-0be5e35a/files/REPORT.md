# NSS-NBR02-PROTECT01 — executed development screen and admission stop
## Execution v0.3 / scientific protocol v0.2

**Disposition: STOPPED AT A0. The complete authorized preflight, initial-fitting and development prefix was executed and independently replayed. No held-out labels or conditions were generated.** The frozen gate's machine label is `BASELINE_INCOMPETENT`; the more specific observed cause is a G-arm relative-improvement shortfall, not failure of its absolute accuracy or old-knowledge requirements.

The numerical protection implementation passed its bounded checks. Both methods protected old class answers in the development projection branch, but that branch gave up some of the stronger correction's immediate successes. These are **development-only exploratory observations**, not the intended held-out protection qualification. No thresholds, seeds, optimizer schedules, constraints or outputs were changed in response to them.

## 1. Why the run stopped

A0 required at least three of four fits in **each** learning arm to satisfy all three: 8/8 initial old associations; at least 16/20 B1 development primary answers; at least four additional correct answers over that fit's own frozen control. All eight fits met the first two requirements. G met the third in two fits, L in four. The source stopped before drawing held-out mappings, as required.

| Arm | Fit (zero-based) | Old initial inventory | B1 development /20 | Own frozen /20 | Gain | A0 |
|---|---:|---:|---:|---:|---:|---|
| G | 0 | 8/8 | 17 | 11 | +6 | Pass |
| G | 1 | 8/8 | 18 | 17 | +1 | Fail |
| G | 2 | 8/8 | 19 | 14 | +5 | Pass |
| G | 3 | 8/8 | 17 | 14 | +3 | Fail |
| L | 0 | 8/8 | 18 | 14 | +4 | Pass |
| L | 1 | 8/8 | 18 | 14 | +4 | Pass |
| L | 2 | 8/8 | 19 | 14 | +5 | Pass |
| L | 3 | 8/8 | 18 | 14 | +4 | Pass |

An important post-result design observation: G fit1's frozen score of17/20 leaves at most three possible gains. A requirement of four gains is mathematically unattainable in that realized fit, even for20/20 performance. The group rule permits one failing fit, but G fit3 also misses the relative threshold by one answer. This identifies a headroom issue in the admission design; it does not authorize changing it now, dropping a fit, selecting new labels, or declaring the held-out study complete. Nor does the machine status establish that the exact learner is generally incapable of the task.

All four development bases were run for all fits/branches before computing A0. B1 alone supplied admission and calibration. Frozen limits were G loss0.006258498049799929 / probability-margin0.012276683402895394; L loss0.01 / margin0.02. These realized limits were archived, but never applied to a held-out test because that test was not admitted.

## 2. What was actually executed

Eight new initial fits (G and L at four paired seeds) each received100 old-association updates. The same 674-parameter dense tanh model and inherited G versus diagonal-sensitivity L learning equations were retained. No historical Q010, TS01/02/03, DC01 or REV01 checkpoint was loaded, forwarded or retrained.

Each context shares its first two updates, then forks at the first validated receipt disagreeing with the same cue/scope's prior public label. B1 uses clip1; B2 uses clip2; P projects the clip2 displacement against eight exact old-margin gradients; S uses B2's actual float32-applied direction at P's actual applied norm. The remaining three receipts use clip1 in every branch. P/S independently recompute the old gradients and projection. All four starting forward values and method-specific raw gradients match exactly before their different steps.

The executed primary prefix contains12 clean contexts, four cost-probe contexts,32 development method/fit/base contexts, eight initial fits, derivative/solver diagnostics and eight isolated faulty updates. There are no held-out contexts. Read-only inventories follow every branch application, and each context has an independently executed frozen trajectory. The exact control only uses labels actually released by public receipts.

The complete eight-cue buffer is explicit: scoped cue/feature hash, observed label, receipt/version provenance and validity. Technical fixtures import explicitly declared synthetic historical receipts without training; those are not secretly initialized scientific labels. L+P and L+S are hybrid computations because their protection rows use exact reverse-mode derivatives.

## 3. Development results: useful trade-off, not confirmation

Each first-correction cell is four development bases × four fitted models =16 repeated model/base outcomes. These are not16 independent task families, and these are not held-out results.

| Arm | B1 clip1 | B2 clip2 | P protected | S same-size original direction |
|---|---:|---:|---:|---:|
| G | 7/16 | 16/16 | 13/16 | 15/16 |
| L | 9/16 | 16/16 | 10/16 | 16/16 |

P never regressed a first-correction success of B1, but lost three of B2's successes in G and six in L. P therefore did **not** preserve every fast flip even on these development contexts. L's mean first-correction loss was0.8540 for P versus0.7857 for B1: the modest class-count gain does not imply improved probability quality.

P retained all eight old class answers in every development case at all four tail checkpoints:512/512 old class observations per method. Those are128 model/base/cue combinations observed four times, not512 unrelated facts. B1 and B2 also retained all old classes in this development sample. S retained all G old classes; one L model/base/cue became wrong after trial4 and remained wrong at trials5/6. This differs from REV01's old-class failures because these are new fits and mappings, not a repair of its outcomes.

### The norm-matched comparison

| Arm / final development tail | B2 mean old loss | P mean old loss | S mean old loss |
|---|---:|---:|---:|
| G | 0.0388470 | 0.0018223 | 0.0444573 |
| L | 0.0655473 | 0.0097994 | 0.0645918 |

Lower is better. P preserves old-answer probability quality much better than S at their checked step norms, but its first-correction focal accuracy is lower. This supports a **development trade-off** between direction and adaptation, not a combined success or a general direction-superiority theorem.

G P norms range1.35117–1.67833 (mean1.53918); L1.64689–1.84219 (mean1.76690). No development P is a zero step. Maximum relative P/S actual norm mismatch is1.61e-8, below the declared1e-4 limit. Their directional cosines average0.76959 for G and0.88345 for L. These comparisons use real stored float32 displacements, not only intended vectors.

## 4. First-order protection is not finite-step immunity

All captured protection rows, QP certificates and applied-step checks passed. Nevertheless, actual old logit margins fell in28/128 G and59/128 L first-correction old readouts under P. All those drops exceed1e-6; the largest declines are about0.20540 and0.83066 logit-margin units respectively. No old class flipped in P.

Captured-gradient predictions for actual P displacements have minimum values around−2.01e-7 (G) and−2.62e-7 (L), within the explicit normalized-row/float32 rounding envelopes. They are not asserted to be literally nonnegative. Real drops much larger than those rounding residuals are retained as nonlinear finite-step effects relative to the local margin approximation, not silently recategorized as solver defects.

The result does not uniquely identify a full learning-history or internal-representation cause. Exact G and approximate L have different trained prestates. Their differing outcomes cannot by themselves prove that approximation caused the extra interference. The old buffer also covers this toy's entire old inventory; no preservation of unbuffered skills or plasticity restoration is established.

## 5. Numerical and failure-first checks

The16 pinned rational solver fixtures passed, including zero rows/target/projection, duplicate and dependent constraints, near-dependent geometry, the narrow cone and row permutation. The finite SVD support procedure checks all subsets except the explicit zero-target case, stores singular values and compact status for every candidate, and retains a full selected certificate. No ridge, row deletion, renormalization, post-score shrinking, retry or rollback occurred.

Eight focal derivative diagnostics preserve G/L's exact-versus-approximate distinction; eight fixed margin-gradient diagnostics test both labels. Every natural old derivative is independently reconstructed in float64 NumPy. Each P/S pair independently recalculated and exactly matched its A/C/solution/cast/control arrays. Certificate verification checks KKT and the selected objective; it is not a second independently optimized solver.

Thirteen non-neural contract tests and the14-category clean/fault catalogue passed. Eight deliberately wrong sign/double updates per pass remained isolated and were correctly detected. Copied certificate/cast corruptions were rejected. Some fault tests are synthetic/copy-based; they are not exhaustive live fault injection. The independently supervised numerical runs, durable intention/commit log and worker file isolation are bounded checks, not a formal information-flow or crash-proof guarantee.

The primary independent audit checked4,305,048 scalar comparisons, maximum tolerance ratio0.119214 under the unchanged empirical2e-6+2e-5*abs(reference) envelope. Q010's unrelated softmax-underflow amendment was not used. Every real attempted update had a durable completion.

## 6. Work and complete adaptive replay

| All actual capture + replay work | Count | Global ceiling |
|---|---:|---:|
| Update attempts / commits | 3,400 /3,400 | 7,000 |
| Recurrent cells | 86,472 | 240,000 |
| Heads | 26,584 | 75,000 |
| Reverse-mode calls | 3,260 | 8,000 |
| Exact old-margin reverse calls (included above) | 1,552 | 4,500 |
| Local focal derivatives | 1,708 | 4,000 |
| QP calls | 224 | 600 |
| Support candidates | 56,832 | 153,600 |
| SVD calls | 56,834 | 153,600 |

The update total includes448 clean/fault fixture applications,200 cost-probe applications,1,600 initial-fit applications and1,152 development applications. Replay is not a second scientific sample. The planned5,704-application full study was not completed because A0 deliberately prevented the2,304 capture/replay held-out updates. Unused capacity is not permission to bypass the stop or add fits.

A fresh process repeated every executed initialization, fixture, probe and development update, reproduced the same stop and matched17,660 frames /55,118 arrays /13,484,996 numerical elements. Public messages, authority tables, scoped receipts, initial/final parameters, calibrated limits, candidate statuses,12 scientific table/decision files and independent audit summaries matched exactly. Timings and process-memory samples are not expected to match. This is internal adaptive reproduction, not third-party or cross-device replication.

The storage admission passed using explicit per-record-kind measurement: projected delivery64,476,968 bytes (<67,108,864) and projected encoded live evidence177,399,955 bytes (<268,435,456). Forecasts are empirical, not worst-case proofs. Actual schema observations and all record kinds are retained. Full source/seed locks precede generation; a scoped direct-seed scan found no collision in276 available REV01/DC01 text members (39,653,276 bytes). Missing/unexpanded historical random histories are not exhaustively audited. Old/main binary-pattern overlap is reported without resampling; held-out mapping seeds are allocated but never drawn.

Numerical stage wall times were53.19 and52.23seconds, excluding the earlier implementation work but included in the shared clock. Peak sampled supervised process-tree RSS was842,477,568 bytes, and container current2,096,238,592 bytes. The host was CPU-only, one numerical thread, four CPU equivalents and a4GiB container limit. Native-memory object accounting remains incomplete (OBS-DC01-COST-001); no overall resource superiority is claimed. Delivery QA is recorded separately against the same two-hour clock.

## 7. What the last Codex pass should decide

**First audit the A0 headroom issue, without retroactively waiving it.** Determine whether a future competence contract should separate absolute ability from improvement opportunities, and retain a strong frozen control. Do not choose easier seeds or weaken the control simply to admit this design.

**Then adjudicate the protection trade-off.** The implementation produced a real norm-matched P–S comparison: P better preserves old confidence, but loses some of the clip2 first flips. A first-order safety projection is not a guarantee of real margin monotonicity. Decide whether the next version needs only a new confirmation contract or a substantive change to its correction objective. Return one bounded recommendation, not another growing candidate list.

The development tables are now known evidence and may guide a new proposal. They cannot become its untouched confirmation set. Neither a revised A0 nor a later positive experiment changes this stop or REV01's failed screens.

## 8. Architecture/program disposition

AER-NBR02-PROTECT01-001 records an implemented buffered-protection interface and a development-only trade-off. PROTECT01 remains NOT_QUALIFIED; its held-out scientific gate is NOT_ASSESSED. New ticket RET-PROTECT01-A0-001 preserves the admission problem and source/data identities. RET-REV01-RETENTION-001 remains open.

NBR-01 stays CLOSED_BOUNDED_RECOVERED_EVIDENCE; NBR-02 stays active. RET-MW01-FIT-001 is PARKED_OPEN; RET-DREAM-MAINT-001 is DEFERRED_DESIGN; OBS-DC01-COST-001 remains open. FCR-0103-001 requires the user's planned01–03 foundation return after03 and before04. All G01–G22 questions are included. No dream rehearsal, PAIR01, REHEARSE01, precision study, core replacement or historical training requalification occurred. The parent Architecture Ledger is unchanged.

## 9. Package and audit boundary

The full package contains all new source, fixed protocol, eight new initial trajectories, every recorded parameter/gradient/update, synthetic fixtures, primary/replay development observations, all1,796 incorrect query rows, and the exact stop. The1,796 count spans12,372 primary-capture neural query rows including technical/frozen controls; it is not an independent-sample error rate for one candidate. No held-out result or missing historical training record is fabricated.

The binary frame archive may be losslessly encoded for delivery. Run RESTORE_EVIDENCE.py and VERIFY_STUDY.py after extraction. Restoration restores captured bytes, not model-generated evidence. RESCORE.py runs only the independent NumPy evaluator. The final external delivery receipt reports fresh-extraction/restoration and relocated numerical re-scoring; it is not implied by this narrative alone.
