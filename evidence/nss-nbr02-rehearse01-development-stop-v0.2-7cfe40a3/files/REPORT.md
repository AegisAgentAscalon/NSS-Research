# NSS-NBR02-REHEARSE01 — strong correction followed by lawful rehearsal
## Execution v0.2 / reviewed scientific protocol v0.1

**Disposition: STOPPED_AT_A0. G has a genuine normalized learning-gain shortfall in two fits; L passes in four. No held-out label map or condition was generated.** All prescribed preflight, eight fresh initial fits, all development branches, independent numerical scoring, and a fresh adaptive replay of the completed prefix ran successfully. This is not a qualified held-out rehearsal result.

The development observations are promising but incomplete: one old-record rehearsal batch kept every immediate strong-correction focal answer and all old classes through the remaining receipts, with much better old confidence than extra focal practice. However, the calibrated old-confidence envelope is still exceeded at some development checkpoints. Those observations do not override the failed admission or establish restored plasticity.

## 1. Actual question and intervention

The 674-parameter dense tanh learner and its three-event START/PRIME/CUE input are inherited. G uses reverse-mode gradients; L uses the specified diagonal-sensitivity approximation, including for each rehearsal example. No exact-old-gradient protection or QP occurs. All online steps are ordinary float32 SGD with learning rate1 and norm clipping1, except the first publicly identified changed-label correction in U/F/R, which uses clipping2.

After sharing the first two released receipts, the same parameter/pending state is forked into:

| Branch | Changed-label update | Extra operation |
|---|---|---|
| B1 | Clip1 | None |
| U | Clip2 | None |
| F | Clip2 | One clip1 mean-gradient batch of eight copies of the newly released focal example |
| R | Clip2 | One clip1 mean-gradient batch of the eight current lawful old records |

All later real receipts use clip1. A branch consumes the changed receipt once. Rehearsal has its own operation ID and parameter version and reuses prior evidence; it is not eight new observations. All eight per-example gradients are actually recomputed at one common post-clip2 prestate, serially accumulated in float64, divided by8, cast once to float32, clipped once and applied once. For F the repeated gradients average to one gradient; the computation is fully charged. For L all replay derivatives remain local, not a hybrid using exact old derivatives.

The writer, public scoped-label-change detector, fixed complete eight-record buffer, receipt authority and resets remain supplied software. These toy conditions restart from the respective initial-fit checkpoint. There is no cumulative lifelong learner, Tertiary dream implementation, maintained-workspace repair, plasticity-restoration test or architecture-scale qualification.

## 2. Why admission stopped

The prospective gate required each fit to have8/8 initial old associations, at least16/20 ordinary B1 development primary successes, and recovery of at least half of its own frozen control's net errors on fixed K. K is four development bases times focal post-feedback trials3,4,6: twelve opportunities. H=12−N_K. H=0 would be unidentifiable; it never occurred here. Each method required three of four fits to qualify jointly.

| Method | Fit | Old /8 | B1 overall /20 | Frozen overall /20 | B1_K /12 | N_K /12 | H | Net gain/H | Fit |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| G | 0 | 8 | 18 | 17 | 10 | 9 | 3 | 1/3 | FAIL |
| G | 1 | 8 | 16 | 14 | 8 | 6 | 6 | 2/6 | FAIL |
| G | 2 | 8 | 18 | 14 | 10 | 6 | 6 | 4/6 | PASS |
| G | 3 | 8 | 16 | 8 | 8 | 0 | 12 | 8/12 | PASS |
| L | 0 | 8 | 19 | 17 | 11 | 9 | 3 | 2/3 | PASS |
| L | 1 | 8 | 17 | 11 | 9 | 3 | 9 | 6/9 | PASS |
| L | 2 | 8 | 17 | 14 | 9 | 6 | 6 | 3/6 | PASS |
| L | 3 | 8 | 16 | 8 | 8 | 0 | 12 | 8/12 | PASS |

**G:2/4, L:4/4. All fits meet the absolute floors.** Unlike PROTECT01's ceiling issue, the present requirements are attainable in every fit. G0 andG1 fall short under the fixed rule. This does not establish that G generally cannot learn. It establishes that this baseline did not meet this particular prerequisite consistently enough across the fixed fits. Neither the gate, seeds, label maps nor training duration was altered afterward.

Development calibration, not held-out evidence: G tau_loss=0.009116187681773177 and tau_margin=0.01773258733424804; L tau_loss=0.01 and tau_margin=0.02. U/F/R scores played no role in these choices. The group decision and initial checkpoint hashes were locked with heldout_not_generated=true. No admission waiver, seed replacement, automatic tuning, or additional candidate followed.

## 3. Exposed development: immediate correction

Each cell below is four development association bases repeated across four fits, sixteen model/base outcomes. The four branches are paired. They are not sixteen independent task families and are not held-out confirmation.

| Method | B1 first-correction correct | U | F after extra | R after extra |
|---|---:|---:|---:|---:|
| G | 4/16 | 16/16 | 16/16 | 16/16 |
| L | 5/16 | 16/16 | 16/16 | 16/16 |

U/F/R have bit-identical parameters immediately after clip2. Both F and R preserved every strong-correction focal class success after their extra batch. F further increased focal confidence; R slightly reduced it, while keeping the class correct.

| Method | U focal loss | F post-extra focal loss | R post-extra focal loss |
|---|---:|---:|---:|
| G | 0.068150 | 0.008651 | 0.087837 |
| L | 0.037131 | 0.007338 | 0.054975 |

This is a specific finite-budget trade-off, not an automatic advantage of rehearsal for every measure.

## 4. What the extra step did to old answers

At the immediate post-strong-correction readout, **all128 old model/base/cue answers were still class-correct per method**. Thus this development sample does not demonstrate repair of an old class answer that the strong correction had already made wrong. It does demonstrate changes in probability quality and later retention.

### Immediately before and after the extra batch

| Method | Old loss before extra (U/F/R) | After focal practice F | After old-record rehearsal R |
|---|---:|---:|---:|
| G | 0.022229 | 0.070237 | 0.013178 |
| L | 0.049394 | 0.072631 | 0.016503 |

Lower loss is better. F and R spend one additional application and eight example-gradient calculations each, but their data and resulting gradient norms differ. Old-record selection improved old probability quality relative to both U and F on these development means. This is not an equal-step-norm experiment or proof that all forms of replay selection are effective.

### Old classes across all four recovery-primary checkpoints

| Method | U | F | R |
|---|---:|---:|---:|
| G | 509/512 | 507/512 | 512/512 |
| L | 512/512 | 512/512 | 512/512 |

Each512 contains128 model/base/cue combinations checked four times. G-U's three failures are the same old cue in one fit/base, wrong after receipts4,5,6. G-F makes that same cue wrong immediately after extra practice and through all four checkpoints, and one additional old cue wrong at the final checkpoint. Those are five repeated observations over two distinct model/base/cue failures—not five independent memories. R has no old class error in these development observations.

**No already-wrong old class was repaired by R at the extra step, because none was wrong before it.** Its observed benefit is confidence recovery and preserving class answers through the subsequent updates. It cannot be called a demonstration of repairing arbitrary forgetting or preventing all transient harm.

### Old confidence remains imperfect

Descriptively applying the newly calibrated envelope to the now-exposed development base/checkpoint summaries finds R outside it at **2/16 G cells and5/16 L cells**. These are diagnostic uses of development data, not an official held-out gate. For comparison, U exceeds it at11/16 G and13/16 L, and F at12/16 G and14/16 L.

Some R deviations are small; others are substantive. For example G base2 at receipt4 has mean loss increase0.025150 over B1 versus allowed0.009116; L base2 at receipt4 increases0.025470 versus allowed0.01. Final mean old loss is G R0.030882 versus U0.043922/F0.046470, and L R0.031669 versus U0.053660/F0.057886.

These improvements do not turn the unresolved reliability requirement into a pass. A gate-only restart would still need to confront the remaining confidence trade-off.

## 5. Batch diagnostics and failure localization

Every batch's source list, eight raw gradients, common prestate, float64 accumulator/mean, float32 cast, clip product and applied weights are preserved and independently checked. U/F/R pre-extra weights match; branch reconstruction is not labelled as new pre-feedback prediction. The correct causal source record is fixed before each gradient. A source receipt is not consumed again during rehearsal.

Mean development raw batch norms are G:F0.35838/R0.09616 and L:F0.20632/R0.22222. R mean cancellation ratios (norm of mean divided by mean individual norm) are0.74074 and0.80738. R's eight gradients are not simply cancelling to zero. These descriptive measures do not establish an optimal dose or authorize increasing it.

Fixed derivative diagnostics matched the exact-G and approximate-L equations separately, including the inherited coupled witness. The independently reconstructed exact gradient at L's prestate remains diagnostic only. The scorer checked5,178,824 scalar comparisons per pass; maximum tolerance ratio0.0601782 under2e-6+2e-5abs(reference). This is an empirical tolerance, not a formal floating-point bound. Clipping-factor/product/application byte checks and exact replay are separate checks.

Eleven non-neural contract methods passed, including reducer repetition/cancellation/subnormal cases, authority errors, duplicate receipt treatment, and synthetic admission edge cases. Eight isolated wrong-sign/double batch applications per pass were actually executed and independently rejected as incorrect applications. Seven post-capture detector checks passed: one verifies the eight live sandbox applications, while the others test copied mean/product corruption, missing-commit classification, and truncation. These are bounded fixtures, not comprehensive runtime fault injection or a formal information-flow security proof. Worker file access to private/protocol/scorer paths is blocked and explicitly tested.

All natural parameter applications had matching durable intents and commits. The actual first observed gate failure is the normalized development gain, not a missing receipt, damaged trace, wrong batch mean, lost log or resource stop. Its internal learning cause is not established.

## 6. Data and verification boundaries

The proposal ZIP identity was verified before implementation. Thirty-three direct seeds are hash-derived exactly as reviewed. A scoped scan examined421 retained DC01/REV01/PROTECT01 text/source/receipt members totaling99,961,601 bytes with no direct-seed collision. This is not an exhaustive historical stochastic-state audit.

Old and development maps differ from the compared DC01 maps. All four new development abstract label sequences occur in DC01's small binary grammar. They remain in the data; no resampling or easier-case selection occurred. Only old and development maps were instantiated. Held-out seeds exist as allocations, but held-out labels and streams do not.

The scorer independently regenerates the permitted maps, initial parameter bytes, teaching order and receipts, reconstructs all forward/local/exact derivative calculations, checks the lawful table and batch authority, and calculates the gate from raw logits. It imports no producer/controller/model code. Its re-use of a prior independent NumPy reference is documented, not misrepresented as third-party replication.

Fresh adaptive replay starts new processes, model instances, generators, counters and recorder caches; it repeats every executed fixture, probe, initial update, development receipt and extra batch. It reproduces the same admission stop and matches **19,428 frames /61,150 arrays /14,577,108 numerical elements**. The complete raw framed-record files, public messages/responses, event logs, instantiated plans, source-gate locks and thirteen final audit/score files match byte-for-byte. Measurement timestamps, supervisor resources and runtime forecasts are excluded from equality, not scientific values.

There are13,220 scored neural query/diagnostic rows in the primary capture and **2,046 incorrect rows**, including expected untrained/derivative/fault diagnostics and frozen controls. Development contributes271 of those failures across all its recorded surfaces. Replay is not additional scientific sample size. Every correct and incorrect row remains available.

## 7. Cost and evidence

| All capture plus adaptive replay | Actual | Global cap |
|---|---:|---:|
| Update attempts / durable commits | 3,576 /3,576 | 7,000 |
| Cell examples | 91,896 | 260,000 |
| Head evaluations | 28,392 | 80,000 |
| G reverse calls | 2,524 | 6,000 |
| L gradient examples | 2,524 | 6,000 |
| Replay-record fetches | 1,664 | 4,800 implementation ceiling |

Per pass:800 new initial applications +640 development applications +100 cost-probe applications +240 clean-fixture applications +8 sandbox applications =1,788. The missing held-out portion would have added2,560 capture/replay applications; it was not spent. Unused budget does not authorize bypassing A0 or fitting further models.

Forty complete main checkpoint records retain weights/runtime RNGs/dedicated initialization and teaching-order states/cursors at0,25,50,75,100 across eight fits. Probe, branch and fixture checkpoint records are also retained; there are580 checkpoint frames per pass. Plain SGD has no momentum slots. Every actual parameter version is recorded in raw updates. No old Q010/TS/previous-NBR02 model was loaded or changed.

Cost admission passed before main fitting: forecast delivery58,300,649 bytes (<64MiB), live encoded evidence186,011,932 bytes (<256MiB). These are empirical per-kind forecasts with the frozen1.5/1.35 multipliers and18/32MiB reserves, not worst-case compression proofs. Logical no-alias observed-shape projection was255,569,312 bytes and is separately reported.

The inherited Python object inventory still has known NumPy-backing/native-graph omissions (`OBS-DC01-COST-001`). Numerical records and process/container measurements remain valid within their scopes; no whole-memory superiority is claimed. Historical softmax-underflow and missing Q010 training/RNG evidence are not repaired or repurposed by this new learner.

No failed scientific fit, unknown-completion update or post-result scientific source change occurred. One pre-execution inspection tried to read an unsurfaced companion from the shallow attachment folder; the valid full proposal ZIP supplied it after extraction. That inspection issue is documented and did not consume model work. Final archive integrity and relocated rescoring are recorded in the delivery receipt.

## 8. Program and next-step boundary

`RET-REHEARSE01-A0-001` records the normalized-gain admission stop. `RET-REHEARSE01-RECOVERY-001` preserves the useful but unqualified development rehearsal signal and remaining confidence deviations. PROTECT01/REV01 historical failures are unchanged. NBR-01 remains bounded-closed; NBR-02 active but REHEARSE01 held-out qualification is NOT_ASSESSED. Parent architecture ledger bytes are not overwritten.

The user requests returning to the skipped NBR-01 question after a qualifying pass, rather than advancing without Codex. This study did not earn that pass, and no next experiment or stage progression has been dispatched. The exact skipped question was not named by ID: the explicitly parked maintained-workspace/derived-progress ticket `RET-MW01-FIT-001` and the earlier Q010 public-input identity candidate are distinct. Confirm the intended ticket at a later dispatch; do not silently identify them with one another. `RET-DREAM-MAINT-001` remains deferred and `FCR-0103-001` remains the broader foundation return plan.

**Scientific interpretation:** old-record rehearsal is a credible development lead here: it retains the fast class correction and improves old probability quality relative to extra focal practice. It is not a held-out success, complete confidence restoration, proof of general forgetting prevention, or a reason to tune this run until it passes. The next useful design discussion should separate absolute baseline competence from the amount of first-reversal recovery demanded of B1, while retaining strong controls and unexposed confirmation—not repeat fits in search of a passing seed.
