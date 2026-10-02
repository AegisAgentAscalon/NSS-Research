# NSS LB03-LEARNABILITY v0.1 — prospective protocol

**Question:** Can reduced-precision trainable working weights genuinely learn, rather than merely preserve an already-mastered skill? This is pass 61. Integration, post-learning repair, architecture growth, language work and codec optimization are excluded. Current user authorization explicitly enters a bounded training comparison.

## 1. Evidence and exact systems

Four inherited parent identities 4101–4104; GRUCell(26,64)+Linear(64,9), 18,249 learned coefficients, 17,856 matrix entries and 393 biases. All coefficients eligible for updates. Three matched modes: FP32-master control and FP16 nearest / stochastic master candidates. Every mode uses the identical four-code Q2 forward quantizer and inherited custom M8 optimizer. Full precision map and candidate selection appear in `docs/CANDIDATES.md`.

Source checkpoints are original pass-57 Q2_M8 step0000 and step1024 snapshots. Exact bytes and tensor hashes are verified; never substitute a later repaired state. Earlier originating full training histories are incomplete, which limits novelty claims but does not prevent the controlled continuations from these exact states. Source optimizer arrays are preserved in inputs but deliberately reset to zero and counter 0 for ALL modes, both regimes. This differs from pass 58's inherited counter and is part of the new declared design.

## 2. Two separate learning regimes, not a repair sequence

**EARLY:** Start each mode from pass-57 Q2_M8 step0000, which has learned float weights but has not undergone Q2 preparation. Train 512 joint A+original-B updates. This tests adapting the known task to the Q2 representation from a weak conversion. It is not training from random initialization and not acquisition of a new semantic procedure.

**NEW:** Independently start each mode from pass-57 Q2_M8 step1024. Change cue 2 from 0 to 1 and cue 5 from 1 to 0, retain the other six labels. Train 512 joint A+current-B updates from the first step. This is newly supplied association information, not novel-rule generalization. The inherited source model has not received these reversals. The held-out unit for B is not a new input: the eight fixed cue inputs are the acquisition probes. The unchanged start is an explicit no-learning comparator.

Old-task A practice is concurrent during every update, identically for all modes. This is a fixed retention control inside learning, not a later repair phase. There is no additional training once the 512-step endpoint is reached.

Each update receives the next one of 64 archived A batches (32 histories ×32 events) plus all 8 current cue inputs, with mean A cross-entropy + mean B cross-entropy. All modes within a parent receive the identical batches, labels, order and loss weights. Fresh optimizer for every branch; inherited equations beta=.9/.999, epsilon=1e-8, global clip=1, no weight decay. Cosine rate .003 to .0003 over 512 updates. Separate initial FP16 cast results are retained. Both FP16 candidates start with identical nearest-even casts.

## 3. Data and units

New panels: development 16 histories (24 prefix+32 scored events), confirmation 256 (same lengths), longer stress 32 (64 prefix+128 scored events). Equal four-family counts: mixed, idempotent, revision and reset. Reuse the archived public generator and exact task semantics. Explicitly exclude exact 32-event windows against the 64 retained A batches per parent, accessible prior low-bit fixture panels, and all newly selected panels. Freeze all concrete files before main work. Full ancestral data are not all available; familiar rules/short patterns recur.

Public A rules: all eight items initially pending; SET(i) marks i done until CLEAR(i) or RESET; CLEAR reopens; RESET reopens all; NOOP changes nothing. Required output is minimum pending index, or 8/DONE only when all done. The model sees event codes and its own state only. Authoring masks, expected labels and future events do not enter inference. Independent set and bitmask rules must agree. B uses zero-state inputs 18..25 and the declared label vectors in CONFIG.

Primary policy starts from zero and replays the entire history under the candidate's own effective weights, scores suffix only. Old-state migration is not tested. All source events, logits, unedited class predictions and final hidden states are retained. All 256 primary histories recur across four parents and three modes: neither events, stages, nor modes are independent populations.

## 4. Frozen budgets and execution order

24 branches =4 parents ×3 modes ×2 regimes; 512 actual applications each; exactly 12,288 main applications if complete. No extra main update allowance and no automatic replay of unknown tails. Maximum disposable preflight 96; timed disposable updates 144 (including warmups); selected audit-update replay maximum 48; global actual model-update ceiling 12,576. Unused allocations are not transferred into extra main training. No model reseeding, endpoint selection, learning-rate search, extra epochs or automatic candidate replacement.

Main training-core ceiling 900 seconds summed across journals; each branch wall cap90s and sampled process high-water RSS2GiB. New-study evidence cap256MiB, source archive bundle excluded and separately accounted. Time/RSS checks each update; anticipated storage checked before retained checkpoint/array publication. Calls may impose their own limits; missing/uncommitted update completion stops the affected branch, reports the cost uncertainty and never invents a resumed lineage. Scientific quality failure does not halt other valid branches.

Checkpoints0,64,128,256,512; development measures at these stages but no selection. Confirmation/stress only stages0 and512, first read by evaluation code after all fixed endpoints/STOP records are sealed. No results influence model preparation. Rotate mode order by parent and regime; run one branch at a time, one CPU intra/inter-op thread; deterministic PyTorch, MKLDNN disabled, no dropout/autocast/compilation. Exact stochastic-rounding seeds are fixed functions of parent/regime/tensor, not fitted to results.

Local protocol/source/input hashes are an auditable freeze, not independently witnessed preregistration. Code corrections before main are archived with preflight failures. After main starts, no scientific code/config changes; a technical fault is a stop, not an invitation to change gates.

## 5. Hypotheses and decisions

H1: FP16 masters can learn from imperfect Q2 conversion and save >=15% of the master+gradient+moment subtotal relative to M32. This is not a claim about whole RAM.
H2: Stochastic writes may avoid suppression of small updates and improve acquisition relative to nearest writes. It may also worsen quality; both signs and every parent are reported.
H3: Old-skill preservation on pass58 alone is insufficient; NEW probes and starting model outcomes distinguish actual changed-association learning from unchanged retention.

**Technical admission:** source hashes/shape/quantizer/gradient/optimizer checks; finite losses, gradients, masters and moments every update; FP64 Torch/NumPy/packed-C comparisons within1e-9+1e-8abs(reference), no argmax disagreement; safe snapshot/dtype/source bindings; all actual budgets honored. FP32 fixed-effective-weight forward/gradient diagnostic uses atol2e-6, rtol2e-4. Gradient of hard rounding is not checked against STE as if identical.

**EARLY useful learning per parent:** final event accuracy>=98%, whole-history>=90%, at least90% reduction in that mode's own initial event errors, all original B labels correct with minimum target score>=.80. A zero-error start cannot demonstrate this learning gain; record as non-informative. Require at least3/4 parents. Interpret candidates relative to equally prepared M32, not an unsupported teacher.

**NEW acquisition per parent:** both changed cues initially have wrong class, then all8 current classes correct with minimum target score>=.80. This includes retention of6 unchanged associations. Require3/4 parents. If the M32 control does not acquire, do not assign its failure uniquely to reduced masters. Report available learning curves and all branches regardless.

**NEW old-skill retention per parent:** event loss versus own stage0 <=1pp, whole-history loss<=2pp, at most one newly induced falseDONE on primary panel. Report stress separately, and require the same absolute98%/90% floors. Require3/4 parents. No repair is added for failure.

**Candidate comparability:** event loss versus matched M32 final<=0.5pp, whole loss<=2pp and at most one additional falseDONE per parent, on each primary regime; reference must itself reach useful learning. Both regimes need3/4 parents for a practically qualified learning candidate. No general equivalence claim from these few inherited parents.

**Resource criterion:** master+gradient+moment saving>=15%; no hidden FP32 master shadow. Descriptive whole-loop time and storage unions always reported. Runtime screen: median repeated disposable per-update time ratio<=1.25 in both benchmark regimes. Overall candidate qualified only with technical, useful-learning, retention, paired-quality and resource screens; otherwise report each positive and negative result separately. More written changes alone is not better learning.

## 6. Timings, memory and additional operations

Main journals distinguish gradient/update core time, checkpoint/I/O and whole branch time. Training benchmark uses parent4101, EARLY and NEW starts, 3 modes, one2-update warmup and3repetitions of5 updates, each from a fresh disposable clone and rotated/interleaved order. This is102 actual extra applications, below144 cap; it measures early-step overhead, not converged throughput or energy. Benchmarks never change retained main checkpoints.

At main steps1 and512 record unique autograd-saved storage union, master/gradient/moment/effective/RNG bytes and named C scratch; distinguish union from simultaneous peak. Process high-water RSS includes imports and corpus and is not isolated model memory. Record float-proposed versus stored changes and final Q2 code changes. Packed export storage is separate from training memory. Pass60 entropy coding is not applied here.

## 7. Audits and review

Retain every main update journal, source-bound checkpoint, exact materialized test, expected label, raw score/prediction, failed result and first-failure locator. Recount outputs with independent finite rules; replay every saved evaluated output in fresh processes. For source4101 and every mode/regime, replay4 main steps from a saved step64 checkpoint, compare state/RNG and nontiming journal values (24 extra audit updates, not zero-cost). Test corrupt/stale checkpoints on copies, not original files. Sample deterministic fixed-weight gradient comparisons and inherited optimizer reference checks. Preserve failure receipts before stopping.

Readable example indices0,64,128,192 give one primary history per family, across all modes and both regimes at endpoints; include both successes and errors, not selected winners. Same-author inspection is not independent semantic review. Automated public finite-rule review covers all arrays. No latent reasoning is inferred from a correct label, and no acceptance mask corrects a model answer.

## 8. Scope limitations

No new random initializations, no full-precision-forward new baseline (the established Q2/M8 system is the same-interface comparator), no study of new procedures, no learned source selection, no runtime adoption, no full companion, no automatic post-learning repair. Source acquisition/header/root mistakes and budget deviations remain separate from learning failures. Exact packed code fidelity is not training acceleration. License/attribution review is still required before public GitHub release.
