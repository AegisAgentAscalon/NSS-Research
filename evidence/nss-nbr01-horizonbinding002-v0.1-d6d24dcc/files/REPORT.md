# NSS NBR-01 / HorizonBinding002
## Longer horizons, addressed memory, and write-admission uncertainty

**20 September 2026 · Standalone research package v0.1**  
**Main experiment RUN; supplementary controls RUN; interface diagnostic POST-HOC.**  
**Full NBR-01 remains OPEN. No architecture replacement, product integration or production qualification.**

## Decision brief

The result is **not “hard gates always win.”** Better-prepared soft state retained clear records through the longest tested streams. But long-lived false memories, missed weak writes, corrupted observations and misinterpreted tool output exposed different failures. Memory persistence, update qualification, uncertainty, and message interpretation should not be collapsed into one number or one gate.

Keep exact records and the existing tri-core + Validator foundation. Carry explicit no-op capability and qualified admission forward as candidates, but do not harden every continuous state variable indiscriminately. Retain a separate way to represent uncertain beliefs. Fix evidence-interface semantics before interpreting every failure as inadequate neural capacity. This study does **not** justify replacing the Primary, merging roles, or claiming a recurrent-versus-Transformer winner.

## 1. What ran and what stayed unchanged

The reference archives were verified and remain unchanged: MegaMind Alpha v0.5.0 TriCoreFoundation001, the recovered v0.4.14, and NBR-01 Pilot001. The new study imports no serving NSS source, writes no live NSS database, changes no accepted generation, downloads no model, and connects neither generic Forge nor the independent Runtime. The serving foundation still has its labelled test adapters; these trained models have not been installed as cores.

The four mechanisms are alternative memory learners, not the four NSS roles. There are **40 freshly trained checkpoints**: four mechanisms × two preparation curricula × five seeds (301–305). Each fit completed **2,400 AdamW steps, batch 48**. This is **96,000 optimizer steps**, **4,608,000 example presentations**, **18,432,000 supervised key-answer labels**, and **94,968,192 event presentations** in the completed main fits. Every main fit is retained, including failed competence screens. No parameter changes during evaluation.

The short curriculum uses 1–16 events; the wider curriculum uses 1–64. Within a seed/curriculum, all neural mechanisms received exactly matching batches and task labels. Across curricula, the number of examples and optimizer steps match, but event exposure, training difficulty and computation differ. This is **not** equal-compute or best-tuned architecture comparison. Extra gate calibration uses 20,480 labelled-event presentations across ten soft checkpoints: five distinct 2,048-event sets are reused across the two curricula, so there are **10,240 unique calibration labels**. That extra information is counted, not hidden.

Completed development: one 450-step soft fit plus four 1,800-step fits on seed141. An earlier, slow GRUCell implementation was interrupted by a 200-second host-command deadline after its last logged 1,200-step point; it has no completed checkpoint and is not counted as a completed fit. Its source, logs and failed screens remain. Packed exact-address GRU execution replaced that implementation before main training; equivalence is unit-tested. The final 2,400-step protocol was frozen before any main seed training or protected episode scoring. These are locally recorded registrations, not an independently timestamped/blinded preregistration.

## 2. Task, horizons, and supplied structure

Each stream has **four explicit addresses**, each holding one of eight possible values or UNKNOWN. An event contains an address, value and visible synthetic admission score. The clean environment accepts scores ≥0.5; lower scores must leave that address unchanged. An explicit RESET clears the scope. This signal is neither real-world factual confidence nor an authorization primitive.

The addresses, address dispatch, and reset contract are supplied structure, **not learned arbitrary entity binding**. The gated candidates learn a value representation, state-write strength and readout. The GRU uses the same exact address separation. The two-block full-history cross-attention Transformer reads every available event with an explicit address mask and relative log-age bias; it is not Pilot001's all-token self-attention encoder, a language model, or a secretly truncated baseline.

Evaluation uses **0/16/64/256/1,024/4,096 additional events after an eight-event setup**; the largest stream contains **4,104 events**. In retention and overwrite cases the following events are distractors. In the interference condition other addresses continue receiving real updates; only the designated protected address has the full long retention requirement. Do not describe all current records in that condition as4,096-event-old memories.

Conditions are clear retention; two known/two missing records; replacement with a different value; competing writes to other addresses; near-boundary rejected signals0.480–0.499; near-boundary valid writes0.501–0.520; explicit reset; and separately corrupted observations. Each cell has128 streams per seed and four key queries. There are **30,720 distinct protected streams**, **3,840 model metric cells**, **240 exact-control cells**, and **1,966,080 model answer evaluations**. These are repeated evaluations of shared test cases, not millions of independent test instances.

Near-boundary scores are still unambiguous under the supplied clean policy. In the noise challenge, Gaussian sigma0.10 corrupts the observed score while the environment target follows the uncorrupted intended score. All inference arms, including the exact ledger, see only the same corrupted observations. This deliberately changes observability and the data distribution; errors there are not automatically retention errors.

## 3. Competence gates: no hiding weak controls

The registered baseline requires each seed to achieve at least 95% on each specified short known-record and missing-record condition. The clean long-horizon gate also requires at least 95% at 4,096 and no more than a 1-percentage-point retention drop versus 16. The low-margin challenge is a separate gate. The table reports counts out of all five seeds; failures are never dropped.

| Mechanism | Preparation | Baseline | Clean long horizon | Low-margin challenge |
|---|---|---|---|---|
| Addressed GRU | short | 0/5 | 0/5 | 0/5 |
| Addressed GRU | wide | 4/5 | 0/5 | 0/5 |
| Hard gate trained from scratch | short | 5/5 | 5/5 | 0/5 |
| Hard gate trained from scratch | wide | 5/5 | 5/5 | 0/5 |
| Same weights, close low gates only | short | 5/5 | 5/5 | 0/5 |
| Same weights, calibrated hard gate | short | 5/5 | 5/5 | 5/5 |
| Same soft-trained weights, fixed hard gate | short | 5/5 | 5/5 | 0/5 |
| Soft state, native | short | 5/5 | 0/5 | 0/5 |
| Same weights, close low gates only | wide | 5/5 | 5/5 | 0/5 |
| Same weights, calibrated hard gate | wide | 5/5 | 5/5 | 5/5 |
| Same soft-trained weights, fixed hard gate | wide | 5/5 | 5/5 | 0/5 |
| Soft state, native | wide | 5/5 | 5/5 | 0/5 |
| Same reader + exact selected records | short | 5/5 | 5/5 | 0/5 |
| Full-history cross-attention reader | short | 0/5 | 0/5 | 0/5 |
| Same reader + exact selected records | wide | 5/5 | 5/5 | 0/5 |
| Full-history cross-attention reader | wide | 0/5 | 0/5 | 0/5 |


The bare full-history reader failed the baseline screen in **all five seeds in both curricula**. The wider GRU passed in4/5; the short GRU passed in0/5. Their later percentages are reported below, but **are not evidence that attention or recurrence as an architecture is inherently inferior**. The exact-memory-assisted reader supplies a competent clean-task system control. A stronger unassisted attention learner remains an open control requirement for architecture ranking.

## 4. Clear-record retention is not the whole memory problem

The following means and sample standard deviations are across the five wider-curriculum runs. Columns are additional post-setup events. The task and parameters are fixed within each comparison.

| Mechanism | 16 | 64 | 256 | 1,024 | 4,096 |
|---|---|---|---|---|---|
| Soft state, native | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Same soft-trained weights, fixed hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Same weights, close low gates only | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Same weights, calibrated hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Hard gate trained from scratch | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Addressed GRU | 96.17 ± 1.58% | 61.25 ± 7.54% | 0.00 ± 0.00% | 0.00 ± 0.00% | 0.00 ± 0.00% |
| Full-history cross-attention reader | 97.85 ± 1.01% | 89.80 ± 2.12% | 63.52 ± 9.10% | 23.16 ± 5.60% | 15.70 ± 9.33% |
| Same reader + exact selected records | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |


**Important correction to a too-simple reading of Pilot001:** the present native soft-state learner retained clear records at 100% through 4,096 in both curricula. Exact binary admission is therefore not established as necessary for this bounded task. The task, representation and preparation differ from Pilot001; we have not isolated which change explains the entire cross-study improvement.

The short-prepared soft learner nevertheless failed the missing-record requirement at 4,096: **known-record accuracy 100%, UNKNOWN accuracy 0%** in the two-known/two-missing condition. It confidently returned values for empty slots. Wider preparation reached100% on both metrics. So a recall-only score would have hidden a severe failure. The wider curriculum gives more event exposure; this is not proof that a free or uniquely optimal curriculum intervention has been discovered.

Direct hard-gate training also changed its result: it passed the clean-task gates in all ten present fits, unlike the1/5 competence result in the old one-record pilot. The earlier failure was scoped to that formulation and preparation, not a universal inability to train hard gates.

In the competing-write condition, every wider-prepared gated variant and the exact-memory-assisted reader reached 100% overall accuracy and 100% protected-address recall at the longest horizon. Address isolation is explicitly supplied by the implementation, so this demonstrates operation of that separated state—not learned binding of arbitrary entities.

## 5. A learned blend coefficient is not a calibrated qualification probability

All values below are at the4,096-event challenge in the wider-curriculum branch.

| Mechanism | Clear retention | Ignore weak false updates | Accept weak true updates |
|---|---|---|---|
| Soft state, native | 100.00 ± 0.00% | 0.00 ± 0.00% | 100.00 ± 0.00% |
| Same soft-trained weights, fixed hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Same weights, close low gates only | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Same weights, calibrated hard gate | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |
| Hard gate trained from scratch | 100.00 ± 0.00% | 100.00 ± 0.00% | 0.00 ± 0.00% |
| Same reader + exact selected records | 100.00 ± 0.00% | 100.00 ± 0.00% | 52.27 ± 16.72% |
| Exact observation-policy ledger | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |


The fixed hard gate solved one problem and created another. It ignored near-boundary invalid events, but **rejected every near-boundary valid write** in the tested cells. A 0.5 threshold on the *learned gate* did not implement a 0.5 threshold on the *observed event score*. Across the soft checkpoints, fixed admission began at input scores approximately 0.544–0.547. Training had left a gap between 0.45 and 0.55. The gate was trained to control interpolation strength, not to provide a calibrated probability of validity.

The registered calibration arm uses separate labelled admission examples to choose a gate threshold before protected episode scoring. **With the same learned weights**, it reached100% on both low-margin conditions in every seed/curriculum. This is a real intervention result with an extra teaching cost, not a discovery that 0.5 is universally the wrong threshold or proof that qualification can be learned without relevant evidence.

Where qualification is already exactly specified, the simple exact policy remains the stronger straightforward implementation. This finite-record task does not justify replacing exact storage with neural storage. The neural mechanism is being studied for future structured/approximate working state, not as the cheapest way to remember four integers.

## 6. Corrupted input requires uncertainty, not just longer memory

In the noisy-observation challenge, scores no longer perfectly reveal which updates the environment intended. The exact observation-policy ledger is therefore **not an oracle for hidden intent**. Wider-curriculum results at 4,096 are:

| Mechanism | Answer accuracy, mean ± sample SD |
|---|---|
| Soft state, native | 58.55 ± 0.84% |
| Same soft-trained weights, fixed hard gate | 60.00 ± 0.91% |
| Same weights, calibrated hard gate | 48.79 ± 1.27% |
| Hard gate trained from scratch | 60.27 ± 1.49% |
| Addressed GRU | 44.77 ± 1.38% |
| Full-history cross-attention reader | 42.54 ± 2.25% |
| Same reader + exact selected records | 45.82 ± 1.97% |
| Exact observation-policy ledger | 48.83 ± 1.25% |
| Noise-model-informed belief filter | 62.73 ± 1.13% |


The calibrated hard gate almost exactly follows the observation-policy ledger: both are around 49% on the hidden-intent target. The conservative fixed gate is around 60%, but its apparent noise robustness comes with the already-demonstrated0% acceptance of weak legitimate clean writes. That tradeoff must not be hidden by quoting only the favorable condition.

A supplementary **noise-model-informed belief filter** retains a distribution over values rather than immediately replacing a record on every accepted signal. It reached **62.73 ±1.13%**. Its update prior (.08), score ranges and noise sigma are supplied from the generator; the neural learners were trained on uncorrupted observations. This is a useful explicitly better-informed control, **not a matched-knowledge architecture victory**, and it still makes substantial errors. Noise-aware training and fair belief-control comparisons remain open.

An additional censored-observation diagnostic supplies identical visible streams with two incompatible hidden intended updates. The pairwise maximum is50% without additional evidence **by construction**. This is an information-loss sanity check, not a new empirical law about cognition. It does not imply that every error in the broader noisy task is irreducible.

## 7. Correct retrieval can still fail at the receiving interface

The exact tool selected the right records under the clean policy, yet the wider reader answered near-boundary valid records correctly only 52.27% of the time. The code retains the original score in the selected record, and the learned reader can effectively reject it again. Thus “retrieved the correct source” and “used the source correctly” are separate achievements.

After inspecting the main results, a **post-hoc, explicitly registered diagnostic** compared the raw selected record with a dedicated synthetic qualified-event view. The latter encodes the exact service's qualification in the model's trained WRITE-strength range (.85). It preserves original observations separately and does **not** claim that their original score was.85. This is a new interface interpretation, not a permissible silent boost to factual confidence.

| Reader input view, wider preparation | Weak true writes, 4,096 | Corrupted observations, 4,096 |
|---|---|---|
| raw_selected_records | 52.27 ± 16.72% | 45.82 ± 1.97% |
| qualified_event_view | 100.00 ± 0.00% | 48.83 ± 1.25% |


The same reader weights recovered 100% on the weak-write cases with the qualified view, while noisy cases still matched the imperfect observation-policy ledger at 48.83%. That supports an interface interpretation for this particular extra error. It does not repair hidden-intent information or establish a qualified real-language Primary/auxiliary bridge. All original failures remain in the main scores.

**Engineering implication:** preserve original measurements/provenance, explicit qualification status, uncertainty, and permission authority as different fields. A confidence-looking float should not stand in for all of them. The serving Validator remains advisory; none of this transfers permission or release authority to it.

## 8. What the two studies establish together

Pilot001 used one record and categorical WRITE/DISTRACTOR symbols, trained through delay 16 and tested through 128. Its soft learner failed at long delay; post-hoc suppression of low gates recovered recall with unchanged weights. That supported a residual-write explanation in that learner.

HorizonBinding002 expands to four supplied addresses, up to 4,104 total events, wider preparation, weak signals, missing records, reset and observation corruption. It shows that better-prepared soft state can retain clear records, direct hard training can succeed, missing-state hallucination deserves its own metric, naive hard thresholds can erase legitimate weak writes, and qualification is not the same as probabilistic belief. The interface diagnostic adds a bounded example of correct records being mishandled by their recipient.

The studies are related mechanism investigations, **not directly matched architecture trials**. Together they support separating reliable record retention, approximate working state, uncertain beliefs and evidence interpretation. They do not establish a general cognition architecture, limitless compressed memory, Japanese/English competence, or superiority over strong language models with the same tools.

## 9. Resources and recovery

| Model | Parameters | Weight bytes | AdamW tensor bytes | Ten-fit training-loop seconds |
|---|---|---|---|---|
| gru_slots | 2681 | 10724 | 21492 | 125.38 |
| hard_slots | 1050 | 4200 | 8444 | 80.89 |
| soft_slots | 1050 | 4200 | 8444 | 80.91 |
| tape_reader | 5771 | 23084 | 46316 | 156.78 |


The completed main training loops total **443.95 seconds** on the sandbox CPU with one PyTorch thread. Timings exclude interpreter startup, development failures, scoring, diagnostics, replay, reporting and the separate full training reproduction. Concurrent audit work and ordinary host variability mean these are descriptive measurements, not dedicated comparative performance benchmarks. They are not the user's PC timings.

Each recurrent session retains4 × 16 float32 values: **256 raw state bytes per stream**, excluding weights, metadata, input chunks and temporary operations. The current full-tape session retains3 float32 fields per event: 49,248 raw bytes at4,104 events. A four-record selected-source view is 48 raw bytes, plus a 32-byte answer tensor; the reference helper currently derives it from the supplied full tape. That is not a measured complete streaming archive cost.

The belief reference retains 36 float64 probabilities, 288 raw bytes per stream, and its batched implementation materializes posterior work arrays across the tape. No constant total-peak claim is made. Training-process 5 ms RSS samples peaked around 336 MB, mostly interpreter/framework and allocator state; sampling can miss short peaks. Exact activation peaks, complete lifecycle memory, target-device latency and energy remain unmeasured. Gate decisions do not mean the weights, states or learning traces are packed to one bit.

Seventy actual model/policy configurations passed scoped snapshot/restore/continue checks to 4,104 events, including fixed and calibrated policies. Repeated queries do not advance the event clock or mutate retained state. Incompatible scope, weights, mode or threshold are rejected. Exact continuation uses the same chunk boundaries; alternative chunk splits are tolerance-tested in the unit suite, not asserted bit-identical for arbitrary floating-point evaluation orders.

Even a threshold change with unchanged weights changes transition semantics. These snapshots require compatible policy identity. Nothing is silently promoted into a serving generation.

## 10. Verification and evidence map

**33 new unit tests passed.** The unchanged foundation passed its 68-test foundation suite afresh with Python site packages disabled; all 974 foundation manifest entries matched. The historical 1,111-test full release qualification and Windows execution were not rerun.

All40 main checkpoints were loaded in a fresh interpreter. Initial seeded identities, changed-element counts, final tensor identities, matching training-stream groups and all**3,840 model metric cells** were reproduced, including prediction and dataset digests. The240 exact-control cells, 30 belief-filter cells, 120 post-hoc interface cells, 70 lifecycle configurations and 80 censored-observation configurations were separately reproduced. These repeated checks are not additional independent seeds.

One entire 2,400-step soft-state training trajectory (wide, seed 303) was rerun from initialization. Its batch digest, final weights, changed-element count and safetensors checksum matched exactly. We did not retrain all 40 models twice and do not claim cross-platform bit-identical optimization.

See `spec/REGISTRATION.json`, `spec/protocol.json`, `spec/SUPPLEMENT_REGISTERED.json`, and `spec/INTERFACE_DIAGNOSTIC_POSTHOC.json` for chronology and locked files. Main results are `evidence/results/*.eval.json`; aggregations and per-seed screens are in `SUMMARY.json`. The exact code, all trained checkpoints, developmental failures and logs are included. The archive-level delivery receipt is supplied separately after a fresh ZIP extraction check.

Project basis: the NSS cognition/architecture/low-bit handoff, especially its source/role requirements and NBR-01 design on pages 3–6 and20–21. Earlier numerical findings are indexed in `reference/PILOT001_REFERENCE.json`. Those documents motivate the experiment but do not supply these new measurements.

## 11. Back to the drawing board

**Keep the tri-core + Validator framework and exact evidence substrate.** No new result here tests the full topology or justifies another architecture restart.

**Revise the memory-update contract, not every state into a binary state.** Support a genuine no-op for clearly irrelevant events; retain uncertainty in a separate belief/hypothesis representation; carry explicit address/scope and qualification metadata. Use exact rules where rules are actually known, and require evidence/calibration where they are learned.

**Make interface semantics part of qualification.** Preserve original score, source and status separately. A selected source is not automatically understood by a receiver; a critic's opinion is not permission. Changing a gate/threshold/view requires a named policy/schema revision and appropriate state reconstruction or qualification.

**Do not close the broader research questions.** These results address bounded temporal retention and stability, not hard recurrent reasoning, learned arbitrary binding, delayed-credit learning, low-bit eligibility traces or a useful integrated companion cycle. NBR-01 stays open; NBR-02–07 remain not run in this package. The next design discussion should use these distinctions before choosing the harder depth/learning experiment. These are recommendations, not an accepted replacement architecture.
