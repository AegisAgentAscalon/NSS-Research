# NSS NBR02 CYCLE01-A — Two-night maintenance feasibility

**Version 0.1 • 29 September 2026 • COMPLETE_DEVELOPMENT_FEASIBILITY / PROMISING_BALANCED_REPLAY_SIGNAL / RESERVED_MAIN_NOT_RUN**

## 1. The question, in plain English
Can we keep the working model unchanged while a copy learns, check the copy before using it, and repeat the process from the model that was actually accepted? We deliberately left the weak English-reader work parked. This pass uses the original, small recurrent checklist learners and their established finite cue interface.

**Encouraging observation:** after two simulated nights, the balanced-replay route had an accepted model with all eight current cue answers correct in all four retained parents. It retained 2,046/2,048 observed continuing-checklist answers (99.90%) across both days, with no false-DONE on those continuations. This is not perfect task continuity: two of the 32 repeated model/history combinations had an error. Only one parent accepted a revision on BOTH nights; the other three rejected the first candidate and caught up on the second. This is a small, exposed development rehearsal, not a fresh confirmatory result or proof of lifelong learning.

**Mechanism:** rehearsing the old checklist while also continuing to train on the current corrected associations. The new examples were not removed from the objective during repair. Additional current-B exposure is a confound to resolve before attributing an architectural advantage.

## 2. Where this sits in the research
The previous reader sequence investigated evidence interpretation. CYCLE01 now asks about successive model maintenance. Its scope is different from COMP01 language competence, PREP01 note preparation, HSA context processing and DARP output construction. Those components were not loaded or changed.

RECOVER01 previously measured a large single-context recovery effect, but every correction began from the original parent. Here, every branch starts night two from its own actual accepted night-one weights and carries the live task state and event cursor forward. Rejection retains the old revision and records the unmet learning, instead of pretending the correction succeeded.

Sources: `provenance/RECOVER01_REPORT.md` §§1–7; `provenance/NSS_Evidence_Led_Research_Plan_v0.1.md` §6; the frozen `protocol/PROTOCOL.md`.

## 3. What was reused and what changed
All four exact SURFACE01 parents (4101–4104) were recovered from the verified RECOVER01 v0.2 execution archive. No new initial fit, model download, replacement seed or later checkpoint selection. Each is GRUCell(26,64)+Linear(64,9), 18,249 learned parameters.

The original float32 values were copied exactly into float64 computation and maintenance training. This is a PROSPECTIVE change of execution precision to give this feasibility study a clean independent arithmetic comparison. It doubles the bare parameter-value bytes from 72,996 to 145,992. It is not a low-memory or runtime improvement, not bit-identical historical execution, and does not fix or relabel the old float32 numerical failures. No post-result tolerance change occurred.

### The public task contract
**Checklist A:** exactly eight required items; all initially incomplete. SET completes the named item; CLEAR reopens it; RESET clears all completion; NOOP leaves state unchanged. These changes persist until another explicit event changes them. The required answer is the lowest-numbered incomplete item, or DONE only if all eight are complete. This avoids the earlier unstated English persistence assumption.

**Association B:** eight named cue assignments, initially alternating binary values. Day one changes cue 0; day two changes cue 1 while retaining the first source correction. The ledger receives each update immediately; the model's daytime weights remain unchanged. The neural cue test supplies only the cue, not its correct label. This measures learned associations, not new procedural generalization.

The exact current ledger answers all eight assignments in every policy. Frozen weights retaining obsolete B answers are NOT evidence that the complete system must ignore current facts. Source-backed answers and answers stored in model weights are separate measurements.

### Conditions
| Policy | What happens during a learning night | What it isolates |
|---|---|---|
| FIXED | No model update; current evidence ledger available. | Stable existing skills and current-source access without neural acquisition. |
| LEARN | 64 updates on all current B assignments. | Acquisition without old-task repair. |
| REPLAY | 64 B updates, then 32 old-A-only updates. | Ordinary repair that omits B from the repair loss. |
| BALANCED | 64 B updates, then 32 updates on A plus current B. | Repair while still practicing the corrected associations. |

REPLAY and BALANCED use identical retained A batches. All parameters are eligible to change in the candidate. Each training phase starts fresh Adam, learning rate .003, clip 1. Training state is separate from the saved work state. B phases are independently run and counted even when starting from identical parents; this is not an equal-compute comparison.

This tests one fixed learning rate. It does NOT execute the old two-factor BALANCE01 proposal (which also varied update size).

## 4. Data, acceptance and resumption
A 32-history guard panel (eight per family) tests old skills before adoption. Eight other histories span two nights, with 32 continued events on each day after prefixes of length 8 or 24. All fixtures and both nights are DEVELOPMENT. The guard is explicitly used for selection; the continuing histories do not influence adoption, but are not called reserved confirmation.

Replay contains 64 preselected original batches per parent (two nights of 32). New task streams were checked against the original training windows; no exact training-window reuse occurred. Same finite rules and short patterns recur. There is no new-rule claim.

The predeclared gate requires all eight current B labels and assigned target probabilities >=.80, old-task event accuracy >=98%, whole-history accuracy >=90%, bounded losses against BOTH original and prior-revision anchors, no new false-DONE on the guard, and valid source/lineage/numerical checks. Whole-history loss allowance is 2/32 histories; no perfect-recovery requirement. Probability scores are not calibrated reliability guarantees. This is a fixed engineering policy, not a proven optimum.

Before each night, the accepted weights and actual live task state are serialized. Candidate training cannot modify either. If rejected, the old model and state continue; if accepted, the candidate continues from the carried state. REBUILD is additionally scored but is never substituted because it happens to look better. The scripted source events occur independently of model answers—no real external action is executed.

Candidate continuation probes are calculated by the test harness, but the gate reads guard+B results only, not the continuing-history answers. The selected probe's final state is reused to advance the scripted day; that arithmetic reuse is recorded rather than counted as another forward.

## 5. Observed results
### Accepted models at the end of the second night
| Policy | Accepted learning revisions / 8 attempted nights | Neural current cue answers | Guard checklist answers | Both-day continuing answers | Entire two-day histories correct |
|---|---:|---:|---:|---:|---:|
| FIXED | No candidates proposed | 24/32 | 4,096/4,096 | 2,048/2,048 | 32/32 |
| LEARN | 0/8 | 24/32 | 4,096/4,096 | 2,048/2,048 | 32/32 |
| REPLAY | 0/8 | 24/32 | 4,096/4,096 | 2,048/2,048 | 32/32 |
| BALANCED | 5/8 | **32/32** | **4,087/4,096 (99.78%)** | **2,046/2,048 (99.90%)** | **30/32 (93.75%)** |

FIXED/LEARN/REPLAY's perfect old-task totals reflect keeping the original checkpoint, not successfully learning and repairing. Their eight outstanding neural association corrections were still present at the end (two per parent). The exact source ledger remained fully current in every policy. BALANCED had zero incorrect current cue classes at the endpoint.

Denominators: 32 B answers = eight fixed cues x four parents. Guard 4,096 = 32 histories x 32 events x four parents. Live 2,048 = eight histories x two 32-event continuations x four parents. The same histories are shared across parents and policies. There are four inherited model fits and eight unique continuing histories—not thousands of independent trials. No significance or general equivalence claim.

### Balanced route by parent
| Parent | Night 1 accepted? | Night 2 accepted? | End guard answers | End B classes | Correct continuing answers, both days |
|---|---|---|---:|---:|---:|
| 4101 | No | Yes | 1,023/1,024 | 8/8 | 511/512 |
| 4102 | No | Yes | 1,017/1,024 | 8/8 | 512/512 |
| 4103 | Yes | Yes | 1,024/1,024 | 8/8 | 511/512 |
| 4104 | No | Yes | 1,023/1,024 | 8/8 | 512/512 |

Only 4103 provides two consecutive accepted weight changes. The other three demonstrate deferred first-night adoption followed by catch-up, not two successive accepted updates. 4103 was the historically imperfect SURFACE01 parent; it was retained, not replaced or selected as the only model to report.

### What was rejected and why
All LEARN night-one candidates acquired the new cue but severely damaged the old checklist. REPLAY recovered much of A, but its night-one current-B probability scores fell below the declared .80 band despite retaining the correct class labels. Those are confidence-threshold misses, not class reversions. Night-two LEARN/REPLAY candidates still missed both changed cue classes in this budget.

Three BALANCED night-one candidates also failed the old-task guard because of new false-DONE outputs; one additionally lost three whole histories. They were not deployed. The fourth candidate's modest non-completion losses stayed inside the fixed rule and it was accepted. All four final BALANCED night-two candidates satisfied the unchanged gate.

These results are already conditioned on the selected gate. A different gate could yield different accepted histories. Do not rank policies solely on their accepted old-task accuracy while ignoring deferred learning or gate-dependent rejection.

### Remaining errors
Two accepted continuing-answer errors remain, both at the same source occasion in different parents (4101 and 4103). After a SET(1) event on the second day, item 0 remained incomplete, but the model answered item 7. This was an incorrect next-item answer, not a false-DONE. The fixed reader was correct there. Repeated source occasion across models is not two independent failure scenarios.

At the final guard, nine answer errors remained across the BALANCED parents; 125/128 guard histories were completely correct. No accepted continuing output claimed DONE when an item remained pending. These are scoped measured behaviors, not a proof that false completion is impossible.

## 6. Interpretation — why this is good news and what it does not prove
**Useful positive lead:** a small existing learner can reach a state that contains the current corrections while retaining nearly all sampled old-task behavior. The day/night design keeps intermediate training damage out of the selected serving path, and rejected work remains visible as missed acquisition. Numerical verification and exact state/parent bookkeeping worked in this new precision contract.

**What contributed:** BALANCED does not merely rehearse old examples; it keeps practicing current B during repair. It consequently has 96 B-loss exposures versus 64 in LEARN/REPLAY, along with 32 A batches. We did NOT include a B96-only control in this first feasibility pass. Extra B practice, the joint objective and the acceptance history are not disentangled. No general balanced-replay superiority, more efficient learning, or causal proof that an extra architecture is required follows.

**Development only:** the arithmetic and orchestration are feasible. Two nights, four inherited fits and tiny finite cue assignments do not establish sustainable lifelong learning, new procedure acquisition, identity continuity, personal memory, open language, native low-bit execution or a real overnight wall-time budget. The main CYCLE01 confirmation remains unrun.

**Reuse existing findings:** this does not erase RECOVER01's strong ordinary-replay effect or failed numerical contract. It adds a new bounded lifecycle feasibility, with a modified repair objective and precision. Exact lookup is still a valid alternative for facts; parameter learning would need stronger justification for general companion deployment.

## 7. Evaluating the test as well as the answer
The public rule explicitly defines persistence, scope, initial state, ordering and DONE. Independent set/Boolean/bitmask derivations agree on the finite event semantics. The task does not ask about ambiguous dated English observations. The test kit retains exact encoded events, actual carried numerical state, source versions, model identities, predicted class scores and answers. These are actual numerical model inputs; the readable event descriptions are derived explanations, not language the model generated or read.

All 126,976 retained A suffix predictions were recounted against the explicit public sequence, including nominal passes and failures. Every B stage retains its cue IDs, current teaching targets, unedited class predictions and logits. No hidden answer-key corrections are applied to outputs. The exact-rule check is software, not a neural critic. Four illustrative public question/response situations are separately explained in `TESTS_AND_ANSWERS.md`; they are selected demonstrations, not an independent semantic review or an unbiased estimate.

The evaluator itself has positive and negative tests for absent acquisition, false completion, accumulated loss, numerical failure and stale/corrupt state. As elsewhere, rejecting a wrong candidate is containment; it is not a correct model answer or successful new learning.

## 8. Verification, costs and interruption
- 16 preflight groups passed, including all 256 checklist states x 18 next events (4,608 explicit rule cases), independent NumPy recurrent equations, objective/finite-difference checks, isolation, cumulative source updates, rejection, and exact optimizer resume on disposable copies.
- 2,048 actual DEVELOPMENT optimizer applications plus seven disposable applications: **2,055 total**. Zero new parent fits and zero model updates during audit. No completed update was replayed.
- All 16 policy/parent branches and all 32 night receipts completed. The audit recomputed the 32 decisions and verified all 16 night-one-to-night-two task-state links.
- 160 scientific checkpoint files passed their stored tensor hashes; 80 training-stage checkpoint hashes matched their exact update-journal entries. The disposable preflight checkpoint is separate.
- 232 retained array files were independently recounted and every saved logit/final-state/boundary array reproduced bit-for-bit in a fresh process.
- Those recorded evaluation files contain **9,304,960 scalar comparisons**, with zero violations of the prospectively fixed float64 envelope and zero argmax differences. Additional prefix and preflight checks are retained separately; this total is not an attempt to count every arithmetic operation. Historical float32 gates remain unchanged.
- The sum of known completed branch-core and continuation timings is **9.873 seconds**, excluding the interrupted branch's first core, imports/startup, preparation, auditing, tools, writing and packaging. It is NOT total research wall time or an optimized night cost. Fresh audit core: **1.394 seconds**. Maximum recorded completed-branch/resume RSS: **335,753,216 bytes**; the interrupted process's terminal peak is unavailable. This is not isolated policy memory, energy, or qualification of the owner's device.
- Runtime/gradient finiteness, update counts and per-process RSS checks were applied in code. Directory size and aggregate known core-time checks are separately verified; storage is not an OS-enforced sandbox and not sampled at every write. The archive and framework allocations lie outside a claimed active-token limit; no 25k-token claim is made.

**External caller interruption:** a shared shell call timed out after 15 complete branches and the final branch's second B64 checkpoint. The checkpoint and journal agreed. Locked source ordering established that repair could not have started before the absent acquired-stage files were written. A separately frozen operational continuation therefore repeated only incomplete inference and executed exactly the missing 32 AB steps. No optimizer tail was repeated; discarded inference count and first-process terminal time/RSS are unknown. The original lock, outcomes and 120-second caller failure remain documented. No score/tolerance/source-task change followed the interruption.

Source RECOVER01 ZIP receipt SHA, exact membership and all 1,807 declared payload hashes/CRCs were checked before selected inputs were extracted. That is file verification, not a rerun of RECOVER01. New source/input lock has 20 objects; operational continuation has two; the post-result audit has one. All remain unchanged.

## 9. Decision and next few steps
**Completed now:** CYCLE01-A protocol, engineering and two-night development feasibility. The balanced route is a promising candidate, not an adopted NSS learner or a confirmed winner.

**Next:** specify and run one longer, fresh-confirmation cycle comparison. Start from all four original parents, keep each branch's accepted history, include a no-update night and a late new correction, and report both per-event and whole-task retention. Add the straightforward extra-B-practice control before assigning the benefit uniquely to joint replay. Do not select only 4103 or use this development panel as a new exam.

**Afterward:** test genuinely new procedural learning when the accepted-cycle question is informative, or choose ONE targeted interference mechanism if the longer comparison exposes a clear need. Facts can remain in exact records. Do not make a perfect English reader a prerequisite; do not restart HSA/DARP, scaling or a generic curriculum campaign.

No full CYCLE01-B, longer run, procedure learning, deployment, or further experiment occurred in this pass.

## 10. Evidence navigation
- `protocol/PROTOCOL.md`, `CONFIG.json`, `LOCK.json`: prospective task, scope, budgets, source identities.
- `protocol/OPERATIONAL_CONTINUATION_01.md`, `CONTINUATION_LOCK.json`: verified phase-barrier continuation.
- `inputs/parents/`, `inputs/replay/`: exact source parents and pinned replay slices.
- `fixtures/guard.npz`, `live.npz`: every public event sequence, expected labels and source masks.
- `results/<seed>_<policy>/`: exact test arrays, source-bound start/end snapshots and adoption receipts.
- `results/*updates.jsonl`: every actual optimizer application and objective loss.
- `checkpoints/`: original/candidate/accepted model identities and resumable optimizer states.
- `audit/`: independent recount, full retained-output replay and checkpoint manifests.
- `provenance/`: source report/task implementation and archive verification.

Original research archives were not merged or altered. This remains internal reproducibility rather than third-party replication.
