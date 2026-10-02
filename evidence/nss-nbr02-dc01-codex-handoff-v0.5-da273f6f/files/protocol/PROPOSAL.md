# NSS-NBR02-DC01
# Integrated delayed-update proposal v0.3

**Date:** 25 September 2026. **State:** PROPOSED_NOT_DISPATCHED. This version reconciles Codex's DC01 v0.2, Chat's earlier exact-diagonal alternative, and the failure-first requirement. Source-derived commitments are identified in `REVIEW_AND_DELTAS.md`; concrete choices below are reviewer proposals, not executed facts.

## 1. Question and bounded expectations

Can a specified approximate eligibility learner acquire and retain simple associations while preserving the information needed to update from a delayed, identified receipt? Compare it against the same network trained by exact reverse-mode gradients, matched frozen-learning controls and causal exact bookkeeping.

One receipt is pending. Cue-time weights remain fixed. Feedback delays are 0, 8 and 32 intervening events. Those events are not ancestors of the scored prediction. Therefore waiting should not change a method's eventual update. Delay is an invariance/retention control; the scientific comparison is approximate versus exact learning and their full costs.

Not tested: ambiguous temporal credit, concurrent pending decisions, stale-parameter learning, native management-token writing, low-bit traces, the parked derived-progress repair, integrated NSS cores, or a broadly superior learning law. NBR-01 remains closed at bounded recovered-evidence scope. No historical model is loaded or changed.

## 2. One main model, two learning implementations

Use a float32 tanh cell with H=16 and D=23 and a two-class readout:

    h[t] = tanh(W x[t] + U h[t-1] + b)
    z = V h[cue] + a; p = softmax(z)

W is 16×23, U is 16×16, b is length 16, V is 2×16 and a is length 2: **674 trainable parameters / 2,696 tensor bytes**. Live h occupies 64 bytes. All these are laboratory adaptive parameters, not frozen serving-core parameters.

A trial starts at h=0 and has three causal transitions: START, PRIME(scope), CUE(identity). It then has d detached filler transitions and one receipt. No other hidden recurrent iteration is added. Queries reconstruct their three-event input from zero h using scratch state; they mutate no live state, pending trace or parameter.

Initialization is paired between G and L. Using a dedicated PCG64 stream, draw W row-major uniformly in ±sqrt(6/(23+16)), U row-major uniformly in ±0.05 then add 0.25 to its diagonal, set b=0, draw V row-major uniformly in ±0.02, and set a=0. Cast each tensor to float32. No labels influence initialization. No draws are made in this document. Dense off-diagonal U is not projected back to diagonal.

Use plain SGD, learning rate 1.0, global raw-gradient L2 clipping at 1.0, no momentum, decay, adaptive schedule or projection. Calculate every component from the same pre-update version before mutating any tensor. These hyperparameters are unvalidated proposed values, not a prediction that competence will pass.

**G** retains the actual computation graph through the three upstream transitions and cue logit. At receipt, cross-entropy uses the saved cue output and now-released target. Fillers use detached h and do not attach to that graph.

**L** uses the local sensitivity recurrence in `EQUATIONS_AND_WITNESS.md`, with no autograd graph. It retains 640 float32 eligibility entries plus cue h, p and V: **2,760 bytes of pending numerical payload**, excluding working trace copies, IDs and overhead. The recurrence intentionally omits cross-neuron derivative propagation; L is approximate for the dense model. The output-layer derivative is exact for its own cue-time state.

**N_G/N_L** freeze their corresponding arm's initial-fit checkpoint and execute the same public transactions and scratch probes without parameter updates. **X** maintains only last-observed labels and legal receipt bindings. It is not initialized from hidden truth and cannot know a new or reversed target before feedback.

## 3. Public information and data split

There are two scopes and twenty globally distinct cue coordinates: eight initial/old cues, four development focal cues and eight held-out focal cues. START and two scope coordinates complete D=23. The exact ID/coordinate table and allocation are in `DATA_CONTRACT.md`.

Only the eight old cues occur in initial learning, cost probes and receipt-rejection diagnostics. Development focal cues do not occur in initial fitting. Held-out focal cues occur in neither initial fitting, probes, fixture, development nor fillers. Old protected cues recur deliberately across splits; it is their retention that is tested. Fresh focal identities and labels, not merely different wire IDs, distinguish the held-out associations.

Four paired initialization seeds each receive exactly 100 zero-delay transactions on the eight old cues: twelve random full cycles and four entries of a thirteenth cycle. The two 50-update cost probes use an independent paired initialization and only old cues. Probe weights are discarded. No best checkpoint, seed or learning rate is selected.

There are four development bases and eight held-out bases. Each base chooses one new focal cue f and one already-learned protected cue p from the other scope. Crossing delays {0,8,32} with stable/reversal policies gives 24 development and 48 held-out streams. Every condition starts from its arm/fit's same initial-fit checkpoint. Adaptation persists between trials within that condition, not between conditions.

The six update cues are **f, p, f, f, p, f**. Stable streams keep f's newly released label. Reversal streams silently flip it at trial 3. Targets are revealed only by the applicable receipts. Fillers are old-cue one-hots, alternately from opposite/same scope, with no label; d=8 is the prefix of d=32. The filler prefix and cues are identical across reversal variants.

At each CUE, retain its before-feedback prediction and later score it against its released target. These are raw predictive diagnostics, including new-association uncertainty and unannounced reversal errors.

**Primary score:** after the receipt and reset of trials 2,3,4,5,6, make one scratch read-only probe of that trial's cue. The probe uses the just-current association and is before the next update. There are five primary probes per stream, 240 held-out occasions repeated across fits. These measure post-feedback adaptation, not prediction of an unreleased target. They must not be mixed with the earlier before-feedback scores.

After trial 6, inventory all eight old cues and the current focal cue with no updates. Also inventory eight old cues immediately after initial fitting. Losing an old label and learning a new one are separately scored. Primary exact-X probes will normally be correct immediately after observing the same cue's receipt; this is a simple causal correctness control, not a demanding generalization claim. Its before-receipt UNKNOWN/surprise errors remain visible.

## 4. Receipt semantics and reset boundaries

BEGIN requires no pending receipt and clears only ephemeral state. Learned weights persist. START/PRIME/CUE are public causal inputs. CUE creates an immutable pending snapshot keyed by schema version, scope, opaque receipt ID and parameter-version identity. A receipt carries only those metadata plus its binary outcome: it cannot replay the cue vector or expose a future label.

Parameters and the saved cue-time trace/graph may not mutate during fillers. The live detached filler state may change. Valid feedback consumes exactly one pending record, produces at most one parameter update and clears h/eligibility/graph. A read-only probe must use scratch arrays without disturbing even an empty-context state inventory.

A single pending receipt cannot honestly support a permutation among multiple valid outstanding labels. The six-update development diagnostic therefore reorders whole old-cue transactions and injects foreign-scope/previously consumed IDs for rejection before each scheduled valid receipt. No wrong label is accepted under a superficially valid ID and then called an observable queue error.

Receipt rejection, changed trace, stale version, duplicate application and failed durable logging have explicit records. A valid but false authenticated outcome can be indistinguishable from a genuine reversal; do not use the scorer's hidden truth to detect it in the learner.

## 5. Admission and stop decisions

**E0: engineering admission.** Source/data/parameter identities, authority, scalar arithmetic, cue-only graph ancestry, L-formula fidelity, control resets, observer isolation, clean/fault detector fixtures and per-arm exact delay invariance must pass. Numerical comparison uses abs(diff)≤2e-6+2e-5 abs(reference), an empirical tolerance, not a proved bound. Dense L-versus-exact-gradient disagreement is measured, not rejected as an implementation error.

**A0: immediate-feedback competence for both arms.** For each arm, at least three of four fits must jointly satisfy: (i) 8/8 old-cue initial inventory correct; (ii) at least 32/40 zero-delay development primary probes correct; (iii) at least eight more correct than that fit's own N on those forty probes. No illegal update is allowed. The 8/8 initial requirement is a reviewer addition so a weak old-association baseline cannot make retention claims vacuous.

Evaluate the entire planned development stage and report every fit, including all old-cue inventories. If G fails A0, stop before held-out generation as BASELINE_INCOMPETENT. If G passes but L fails, stop as LOCAL_RULE_COMPETENCE_DEFICIT. If both pass, retain **all four fits**, including an individually failing fit, for held-out scoring. No extra fitting or outcome-dependent seed selection follows from failure.

Engineering or resource failures stop as invalid/incomplete. A scientifically poor held-out result under an otherwise valid contract is fully evaluated and preserved. No post-hoc denominator reduction, output repair or new favorable rule is permitted.

## 6. Held-out questions, not one misleading PASS

Report each base, family, fit, delay, reversal policy, before-feedback prediction, primary probe and inventory. The four held-out families are two-base bookkeeping groups; repeated fits and invariant delays do not create independent association tasks.

**D1: mathematical implementation and delay fidelity.** G must match independent exact derivatives and update arithmetic. L must match its independently implemented approximate recurrence and SGD arithmetic. For each, identically ordered receipts must produce bit-identical cue predictions, gradients, post-update parameters and scratch probes across delays on the pinned deterministic implementation; live filler h/timing/costs are excluded. Same-method fresh adaptive replay is separately mandatory. No G/L trajectory identity is demanded.

**D2: adaptation with unrelated-old retention, assessed per learned arm.** On the three focal primary probes per stream (trials 3,4,6), require mean log-loss improvement of at least 0.05 nats over its own N in at least six of eight held-out bases, averaging four fits and the two policies at d=0. Require that each base's mean old-cue inventory accuracy loses at most five percentage points from its initial-fit inventory in at least six bases, and no more than five points pooled. Publish actual class gains, reversal recovery and all failures; lower loss need not cross the class boundary.

**D3: L noninferiority screen.** At d=0, L's primary accuracy may be at most five points below G pooled and in at least six of eight bases. L's mean primary log loss may exceed G by at most 0.05 nats pooled and in at least six bases; old-cue retention may be at most five points below G pooled. A noninferiority pass is a proposed small-sample decision, not a confidence bound or broad superiority result.

**Resource claim.** No blanket efficiency PASS. A useful approximation claim additionally needs D2/D3 and an explicitly named measured resource improvement. Report L/G pending numerical bytes, all unique resident/transient storage, trace work, exact-gradient work, update work, latency and instrumentation separately. Runtime is descriptive on this tiny instrumented task. If trade-offs conflict, report a trade-off, not overall superiority. L may use more memory than the short exact graph.

## 7. Independent mathematics and the nonzero witness

The full formula, its omitted terms and the fixed analytic witness are in `EQUATIONS_AND_WITNESS.md`. The proposed witness's exact encoder-gradient norm squared is 47/32; squared error is 3/8. Its relative difference is sqrt(12/47)>0.05, above a 1e-3 exact-norm floor. These are algebraic consequences of a specified toy point, not a trained result or a performed runtime check.

Four fixed derivative diagnostic cases are executed per pass: diagonal/zero activation, coupled/zero activation, diagonal/nonzero activation and coupled/nonzero activation. They make no parameter updates. Diagonal raw gradients must agree; coupled cases must each match their own independent equations. Only the algebraic coupled-zero witness carries the ≥0.05 divergence gate. Its U-gradient is zero, explicitly; the nonlinear case and every recorded natural update audit U.

For each L update, additionally compute the exact gradient at **L's own pre-update weights and causal prefix**, using independent NumPy math, and record absolute/relative differences and angle when defined. Comparing G and L gradients at different learned weights cannot isolate approximation error. The auditor never supplies its gradient to the learner. Intentional approximation is not mislabeled a numerical failure.

## 8. Failure-first observability

Every operation links run→fit→condition→trial→cue→pending snapshot→receipt→gradient→update→subsequent score→artifact. Full raw evidence and a failure index distinguish scientific misses, expected surprises, engineered fault fixtures, invalid execution and unknown completion.

Write an attempt intent durably before any possible mutation; acknowledge only after required post-state evidence is durable. Use an independent supervisor, heartbeat, sequence-gap checks and a preallocated 1 MiB emergency record inside the cap. A hash without its required arrays is not a recoverable record. Pending G graphs are not claimed portable serialized checkpoints; retain their reconstructible inputs and forward tensors.

The finite fault suite covers receipt identity, omissions, snapshot/version mutation, wrong graph ancestry, incorrect local arithmetic, incorrect SGD application, leakage, log truncation, quota failure, packaging omissions and scorer timing. It includes clean controls and an explicit unidentifiable authenticated-wrong-label example. Eight isolated deliberately wrong optimizer applications per pass are charged to sandbox fault fixtures, never to learning evidence. Other injected checks mutate copies or pure state-machine records and use no extra optimizer steps.

For a natural failure, separate observed facts, first observable divergence, candidate explanation, tested mechanism and evidence gaps. A recorded wrong answer is not proof of a decoder fault. A successful detector fixture does not prove that all natural failures have that cause. See `FAILURE_OBSERVABILITY.md`.

## 9. Counts and ceilings

Four fits × two arms × (100 initial +72×6 condition +6 receipt-diagnostic updates), plus two 50-update probes = **4,404** primary updates. Full adaptive replay repeats those 4,404, including probes. Add twelve clean-fixture applications and eight sandbox fault applications per pass: **8,848 planned update attempts**, below the proposed **9,800 global / 4,900 per-pass cap**. The 952 remainder is reserve, not permission for extra fits or post-result tuning.

Planned primary-plus-replay forward totals, including N, scratch probes and inventories, are **330,584 cell examples and 48,392 head evaluations**. Proposed hard ceilings are 400,000 and 60,000. G requires 4,424 SGD-associated backward calls plus eight derivative-only backwards; L has no autograd backward. Count all attempts before dispatch; interrupted calls and rejected work at the actual updater boundary stay charged.

Two-hour shared clock includes implementation after authorization, preflight, fault checks, cost probes, initial/development/main work, scoring and full adaptive replay. Memory stops: 3 GiB process tree or 3.5 GiB container current. New uncompressed evidence≤256 MiB; one delivery ZIP≤64 MiB. No prior archive/model is duplicated. Full planned numerical records have a component allowance of 209 MiB before the 47 MiB reserve; implementation must prove its actual schema fits those ceilings and the ZIP projection before main fitting.

Storage is losslessly chunked, with genuine repeated computations deduplicated only after equality verification. It must not substitute reconstructed values for missing captures without explicit labeling. Logs, fault evidence and unsuccessful attempts count. A capacity/competence failure stops instead of extending the clock or removing negatives. The detailed arithmetic lives in `CALL_AND_RESOURCE_LEDGER.json`.

## 10. Preflight and execution order

Future separate authorization permits implementation under this reviewed design, not a changed scientific contract. Then: pin source/environment/seed identities; independently verify schemas and static ledgers; implement recorder and non-neural detectors; run fixed derivative diagnostics and clean/sandbox fixtures; run fixed cost probes; validate evidence/time projections; fit initial models; execute development and receipt diagnostics; freeze A0; only on both-arm admission generate held-out concrete streams; execute all retained fits; score independently; perform full adaptive replay; verify and re-score a relocated delivery.

CPU float32, one intra-op/inter-op thread, deterministic algorithms, no GPU, compilation, dropout or autocast. The observed review host is CPU-only package metadata with four CPU equivalents and a 4 GiB container; no Torch runtime/model was imported. Runtime compatibility, achieved learning and actual resource feasibility remain untested.

Replay of an early-stopped study covers only the completed causal prefix within the same cap; it cannot manufacture held-out work that was never admitted. No automatic restart of an unknown-completion update. Relocation re-scoring uses stored arrays and does not execute a third adaptive run.

## 11. Program and architecture disposition

DC01 is a study-local ST-09/ST-10/ST-02/IF-01 learning interface. The maintained token direction and ST-04→IF-02→ST-02 repair ticket remain parked and unqualified. Dense 16-unit recurrence and the proposed approximated update are not promoted into production architecture. All NSS role and historical evidence boundaries remain.

The user's new direction creates **FCR-0103-001**, a foundation-consolidation checkpoint after NBR-03 closeout and before NBR-04. Revisit residual issues from 01–03 with specific hypotheses and fixed regression panels, not automatic retraining. Resolve priority dependencies or obtain an explicit owner decision on residual blockers before advancing. This does not reopen NBR-01's accepted bounded scope or claim all 22 research questions must be solved before later research. Detailed clearance is proposed in `ROADMAP_AND_RETURN_GATE.md`.

## 12. Readiness statement

The model, equations, observation timing, mapping split, reset policy, margins, source precedence and budget are now specified as a single **proposal**. The implementation source lock, measured cost bound, actual derivative checks, seed/history audit and experimental competence checks still must be produced. No such pass is asserted by documentation checks.

This package makes a future run decidable: if it learns poorly, loses a trace, computes the wrong approximate rule, applies a correct update incorrectly, or fails to retain evidence, the result has a distinct classification and the relevant records. It cannot guarantee that every scientific failure will have an immediately known internal cause.
