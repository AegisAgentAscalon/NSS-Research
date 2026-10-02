# NBR-01 / IdentityBinding009
## Distinct records and provenance-aware recovery

**Date:** 21 September 2026. **Status:** completed bounded experiment; NBR-01 remains OPEN.

**Decision:** KEEP explicit, scoped record ownership as an engineering reference. KEEP the measured benefit of near-negative binder preparation at the moderately similar condition. KEEP the separation between internal-state recovery and external membership decisions as a candidate policy. REVISE the learned identity/read interface before claiming reliable coexistence of very similar entities. No candidate learned pipeline passed the full joint target.

This is a standalone research package, not a foundation update, accepted companion architecture, language-capable model, biological simulation, or deployment. Put it beside the earlier studies in `MegaMind_Alpha_Proto`; do not merge it into them.

## 1. Question, source, and scope

Study008 exposed a structural failure: a registry could assign a new identity correctly while a later numerical binder overwrote an older identity's record. This pass asks whether explicit record ownership or better binder preparation fixes that failure, whether a correct store is then used correctly by the frozen readers, and whether legitimate internal history improves recovery without admitting unfamiliar external queries indiscriminately.

The unchanged input plan is in `spec/NSS_NBR01_IdentityBinding009_Research_Plan_v0.1.md` (and DOCX). Resolved budgets, alternatives, and screens are in `spec/RESOLVED_PROTOCOL.md`. The experiment extends the NBR-01 temporal-state / internal-depth comparison. Candidates are trained beforehand; **all learned parameters remain fixed in scored evaluation**. Numerical working-state writes, registration, repair and clear operations are not optimizer updates. No delayed-credit, reinforcement-learning, or low-bit experiment was performed.

The parent008 implementation, frozen checkpoints and necessary parent006/007 modules are copied byte-for-byte into `reference/parent008`. Study008's report is `reference/Study008_REPORT.md`. Original mounted inputs were hashed before work; the 12 supplied ZIPs and all 61 tracked input files, including the two original Study009 plan files, remained unchanged at verification. This is a measured input inventory, not a claim that all historical repository releases were available.

### Information boundary

The synthetic task contains up to 16 identities and 16 records, one location relation, random numerical identity representations with 16 identity coordinates plus an UNKNOWN coordinate. The scorer knows the intended graph; the candidates do not receive it. They are supplied qualified events, scope, and a registry of available identity symbols. The registry contains symbols, **not relationships or answers**. A future identity's inactive row is zero until registration.

We retain two distinct input tracks. In the **resolved transaction** track, a registration/event supplies a checked identity handle, but the numerical binders still receive only the identity vector, stored keys and presence. The exact writer is explicitly allowed to use the handle. In the **observed** track, the resolver's own chosen index is used; the scorer never substitutes the intended index. Exact downstream bookkeeping cannot correct a wrong upstream resolution.

This study does not integrate the old Study005 learned presence maps: presence and ownership metadata are protected exact controls. It also does not retrain the frozen relationship readers. Results concern this finite symbolic task, not natural-language reference resolution.

## 2. Implementation and controlled candidates

`nbr009/state.py` introduces `nbr009-owner-state-v1`, with separately stored scope/epoch, registered identity, record owner, numerical key/value, relation presence, key/value readability, row revision, and transaction revision. A clear removes a relationship without unregistering the entity. Reset changes epoch, preventing stale handles from being valid in the new scope. Checked precommit/commit rejects stale revisions. Reads are nonmutating.

The exact identity writer selects an existing record by owner or allocates a vacant record; it does not re-resolve ownership using vector similarity. The inherited/continued learned binder chooses a record or NEW from numerical features. On a wrong existing-record write it can replace the value while the older key/owner remains, matching the failure under study. Guarded variants inspect the proposal and reject ownership conflicts; proposals, commits, and rejected valid writes are scored separately. An exact guard is not evidence that the underlying learner made a correct choice.

No protected destination ID or intact copy of the relationship value is kept in recovery state. Owner metadata can legitimately rehydrate a record's **key**; it cannot tell the system a lost destination.

### Preparation

Ten 818-parameter binder continuations were completed: ordinary additional preparation and near-negative preparation for each of five inherited pairs. New paired seeds are 1101–1105. Each fit used 1,200 AdamW steps, batch 128, learning rate .002 and weight decay 1e-4. Total: **12,000 completed optimizer steps and 1,536,000 training-example presentations**. Same draws, masks and steps were paired; the input curricula intentionally differ. This is not a matched-wall-time or identical-data comparison.

The near curriculum includes close distinct identities and close competing existing identities, with .01/.03/.10 perturbation scales. The forward architecture remains the inherited cosine/projection matcher and learned new-record threshold, including its capped logit scale. Successful training in one similarity range does not establish resolution at arbitrarily smaller separations.

One 1,200-step development fit (seed1191), 16-stream Stage A and selected Stage B pilots were retained. Five richer-cue **rule** calibrations use 4,096 unique labelled examples each, shared across four representation arms: 20,480 unique calibration labels, 81,920 feature evaluations. This diagnostic adds no trained neural matcher. A second cue is sometimes cleaner than the first, an explicitly declared information advantage.

An infrastructure interruption stopped preparation after pairs1–4 completed and pair5 ordinary last logged step800; unknown unlogged progress is not counted as completed work. Pair5 restarted from the same parent/seed/recipe. A timed-out first main invocation emitted no result files and was rerun unchanged. Logs and interruption notes are in `evidence/development`; no seed or unfavorable result was discarded.

### Lock and evaluation design

The source, spec and checkpoint lock covers 130 files. Lock SHA256: `405adde083395b360f420fccadc4bfc61bf11add54cd4913f5b23e7e90cba393`. It preceded main scoring but followed the disclosed pilot. This is a local lock, not externally timestamped preregistration.

Stage A: five pairs × six identity families × eleven variants × 64 episodes, ten lifecycle query points. Physical allocation, identity numbering and introduction order vary. Stage B: 61 scenarios/pair, batch64, key/value/query isolation, 64/1,024-step horizons, maintenance schedules and state/depth regression. Conditional cue diagnostic: twelve families × 1,024 episodes/pair, four feature arms. Main episodes/seeds are fresh; task design and inherited representations are not an untouched benchmark.

Percentages below are means across five pairs. `±` is the **sample standard deviation in percentage points**, not a confidence interval. Paired variants share source episodes; their results are correlated. Every per-pair count and failure is retained in `SUMMARY.json` and raw evidence. No percentage is a measure of overall research completion.

## 3. Result: exact ownership fixes storage; preparation helps only part of learned binding

The following measures whether the **entire logical relationship map** is correct immediately after the new identity's first relationship write. It includes old and unrelated relationships, not just the newest answer.

| Writer | Ordinary identities | Similar sources (.10) | Very close sources (.01) |
|---|---:|---:|---:|
| Inherited numerical binder | 99.69 ± 0.70 | 0.00 ± 0.00 | 0.00 ± 0.00 |
| Ordinary additional preparation | 100.00 ± 0.00 | 9.06 ± 3.01 | 0.00 ± 0.00 |
| Near-negative preparation | 100.00 ± 0.00 | 100.00 ± 0.00 | 0.00 ± 0.00 |
| Near-prepared binder + ownership guard | 100.00 ± 0.00 | 100.00 ± 0.00 | 0.00 ± 0.00 |
| Exact identity-keyed writer | 100.00 ± 0.00 | 100.00 ± 0.00 | 100.00 ± 0.00 |


In the .10 close-source condition, near-negative preparation reached 320/320 correct maps versus 29/320 for equal-step ordinary preparation and 0/320 for the inherited binder. All five near-prepared pairs passed this particular condition. This is evidence that the curriculum matters in this range, not simply that more steps always help.

At .01 separation, every unguarded inherited, ordinary-prepared and near-prepared binder committed to the wrong owner in all 320 first-write cases. Guarding the near-prepared binder blocked the damaging proposals but also rejected all useful new writes; correct-map accuracy was still zero. Rejection does not satisfy the write requirement.

The exact writer maintained the correct relation map at every saved phase in all six families and all five pairs. Across **7,680 targeted valid transaction comparisons** (first write, correction, clear and rewrite), it made no cross-owner commit. Denied and wrong-scope events were checked for byte/signature preservation. This establishes a bounded implementation contract using protected owner metadata. It is not learned recognition and not a proof of zero real-world failure probability.

## 4. Result: perfect records do not imply correct neural use

With the exact identity writer, the store is correct. The unchanged neural readers can nevertheless confuse very close identities. This table requires the old, new and unaffected queries to be **jointly correct** after the new write.

| Ambiguity family; exact writer | Shared reader | Gated reader | Exact owner traversal |
|---|---:|---:|---:|
| Ordinary | 100.00 ± 0.00 | 100.00 ± 0.00 | 100.00 ± 0.00 |
| Very close source identities | 20.00 ± 5.68 | 20.31 ± 4.42 | 100.00 ± 0.00 |
| Similar source identities | 99.06 ± 1.40 | 99.06 ± 0.86 | 100.00 ± 0.00 |
| Very close destination identities | 21.25 ± 5.70 | 0.62 ± 0.86 | 100.00 ± 0.00 |
| Very close intermediate identities | 17.50 ± 7.19 | 21.56 ± 6.39 | 100.00 ± 0.00 |
| Very close sources and intermediates | 5.94 ± 5.34 | 0.62 ± 1.40 | 100.00 ± 0.00 |


For very close sources, the primary reader scored 64/320 jointly correct cases despite a perfect relation map; exact owner traversal of that same store scored 320/320. Similar destination and intermediate identities expose further confusion. The exact reader selects by ownership after identity resolution, while the neural readers still perform their learned numerical matching. This is an information-use/representation limit, not evidence that storage forgot the relations.

Registration-only queries are essential: the new identity exists but its location has not been written. A fuzzy reader can already return the older similar entity's location before a new write occurs. We scored this phase, not just the post-write answer.

The resolved control uses unconditional nearest identity selection at query time. Its answers to **unregistered** queries before registration or after reset/fresh-scope rebuilding can therefore still be wrong. The exact owner traversal is not a novelty-recognition oracle. The perfect-store result must not be described as passing the full recognition lifecycle. The observed tracks retain the A/B selective resolvers, their mistakes and blocked valid writes.

**Joint conclusion:** no learned-writer plus frozen-reader setup passed the full required near-identity behavior in all core families; the principal learned comparisons passed zero of five joint pair screens. Exact ownership passed its narrower engineering screen. A neural reader or binder failure cannot be hidden by reporting only that screen.

## 5. Result: internal recovery benefits from legitimate ownership information

Stage B deliberately uses the exact-owner store as a controlled infrastructure reference. The internal policy reconstructs keys from stored owner handles and the existing identity registry. Numerical values have no protected destination ID; they are repaired from their current representation using nearest-code recovery. Externally arriving queries still face the existing A or B gate.

At 1,024 repeated noise events (per-coordinate standard deviation .02), repair every 32 events, eight-link queries and eight query rounds:

| Maintenance policy | Established-chain accuracy | Correct missing-link answer |
|---|---:|---:|
| Same geometric admission policy for internal/external inputs | 41.88 ± 10.50 | 100.00 ± 0.00 |
| Same learned admission policy for internal/external inputs | 11.88 ± 4.07 | 100.00 ± 0.00 |
| Rehydrate owned keys only; selective values | 59.38 ± 6.25 | 100.00 ± 0.00 |
| Recover values only; selective keys | 65.62 ± 11.05 | 100.00 ± 0.00 |
| Owned-key rehydration + nearest values; external gate A | 100.00 ± 0.00 | 100.00 ± 0.00 |
| Owned-key rehydration + nearest values; external gate B | 100.00 ± 0.00 | 100.00 ± 0.00 |
| Unconditional nearest-code maintenance and queries | 99.38 ± 1.40 | 100.00 ± 0.00 |


For the primary reader, shared-policy A recovered 67/160 supported answers, shared-policy B 19/160, and the split internal/external policies 160/160 each. Unconditional nearest maintenance was also strong at 159/160. One case does not establish a statistically general advantage over the simple nearest control. The important comparison is that selective external admission need not force the same overly conservative treatment on already-established internal fields.

Key-only rehydration and value-only recovery are useful interventions: neither alone matches their combination here. The implementation changes both the available owner-key reference and how previously unreadable values may be retried; it is not a learned reconstruction of an arbitrary lost identity. Retry from already stored information is not counted as a new observation or increased factual confidence.

### What this policy does not fix

Fully erased values were not reconstructed. A wrong but valid destination symbol could persist as a wrong answer: identity membership is not factual correctness. Deliberately stale ownership and wrong-scope conditions produced explicit invalid-state flags; any placeholder UNKNOWN in the saved answer array is not counted as a successful missing-information service. Valid but wrongly assigned metadata remains a vulnerability to be surfaced, not an infallible source of truth.

Moderately disturbed **external** queries remain difficult: the internal-A policy reached **67.50%** supported accuracy in the separate q20 query case. Restoring storage does not make the external observation more informative. The complete fault and common-noise results remain in the score tables; none was removed to promote the internal-policy headline.

### Temporal state and processing depth remain distinct

After 1,024 disturbance steps with repair every8, retained-state four-link tasks reached 100% supported accuracy at four/eight query rounds, and eight-link tasks reached 100% at eight rounds. Eight-link supported accuracy was zero at one, two or four rounds. Removing the retained state yielded zero supported accuracy at every depth. State removal is an information-removal ablation, not a fair architectural competitor.

These checks reproduce the bounded computational distinction: maintained state provides usable relationships; additional rounds traverse them. They do not establish unrestricted reasoning or replace the still-needed competent conventional-model quality/cost comparison.

## 6. Conditional diagnostic: informative identity evidence versus duplicated evidence

The separate rule-based diagnostic asks whether a second useful cue can resolve ambiguity in the first. It is **not** plugged into the unchanged 17-coordinate readers and is not a trained semantic encoder. Four feature controls use separately calibrated gates. A duplicated vector adds coordinates but no new observation; two independent views and a wider random code change the information/geometry available.

| Representation / evidence | Known with first-view noise .20 | Ordinary novel rejection | Novel close in first view |
|---|---:|---:|---:|
| Single 16-coordinate view | 68.48 ± 4.59 | 99.79 ± 0.08 | 0.00 ± 0.00 |
| Same view duplicated to 32 coordinates | 68.48 ± 4.59 | 99.79 ± 0.08 | 0.00 ± 0.00 |
| Two independent 16-coordinate views | 99.90 ± 0.07 | 99.96 ± 0.09 | 91.05 ± 5.20 |
| Single random 32-coordinate view | 99.73 ± 0.19 | 99.39 ± 0.26 | 0.00 ± 0.00 |


There are 5,120 main examples in each reported family/method. For noisy known inputs, two independent views reached 5,115/5,120 correct. A single 32-coordinate code also reached 5,106/5,120, so increased representation dimensionality/geometry explains part of the gain; the experiment does not uniquely favor multiple compartments.

For an unfamiliar identity close in its first view but independently represented in the second, the dual-view rule rejected 4,662/5,120 correctly: **8.95% were still falsely accepted**. When the unfamiliar identity was close in **both** views, every method failed to reject it in this test. Missing, shuffled, conflicting and jointly corrupted cues were retained and reduce usefulness. In the designated noisy-known condition the second view is less noisy than the first; this is intentionally more/better information, not equal-quality inputs.

The identical-observable/different-origin control produced identical decisions, as it should. No hidden origin indicator was supplied. These outcomes distinguish inadequate decision rules from cases where the offered observations do not support the desired distinction. They do not justify ignoring unfamiliar identities or requiring all future inputs to match a closed catalogue.

## 7. Complete state, preparation, and execution costs

The owned16-record state uses **3,864 raw bytes per stream**, including the registry, key/value arrays, active/presence/readability flags, owner/epoch/revision/allocation metadata. This is 528 bytes more than the parent008 raw state account. It excludes model weights, query temporaries, Python metadata, saved evidence and framework/OS memory. Protected keys can be reconstructed because the owner and registry retain identifying information; values have no shadow backup.

The ten completed fit/checkpoint loops total 29.32 seconds in their per-fit records. That excludes interpreter startup, development, interrupted attempts, historical parent preparation, scoring, reproduction and packaging. The sum of five completed main-process timers is 644.75 seconds; workers overlapped, so it is **not** elapsed end-to-end turnaround. Peak main-process RSS was 586,916 KiB, including PyTorch and large evidence arrays. Original fitting peak was not separately instrumented. The recorded completed fit/main work remained within the declared host ceiling; this is not the user's device budget.

Quiet single-process timings (one PyTorch thread, batch64, 5 warmups/50 measurements) gave median 0.858ms for clone+exact write, 1.030ms for clone+learned write, 3.027ms for clone+shared-A maintenance, and 1.789ms for clone+internal-A maintenance. Primary query medians were 2.085ms at one round and 11.127ms at eight. Signatures, Python work and decoding are included as labelled. These are current implementations, not optimized-kernel lower bounds, nor GPU or Windows projections. See `evidence/TIMING.json` for batch1, percentiles and all fields.

The conditional cue arms double feature/code storage where declared. Their benefit is not free and is not a packed low-bit result. Historical model acquisition and training remain additional lifecycle costs; no overall architecture-efficiency win is claimed.

## 8. Reproducibility, provenance, and package integrity

**158 distinct tests passed:** 45 new research tests, 45 unchanged parent008 tests, and 68 unchanged foundation tests. The full historical 1,111-test release qualification was not run.

All five complete main evaluations (15 A/B/CUE result files) were rerun in fresh interpreters. Every one of **20,375 saved arrays** matched exactly, and an independent NumPy scorer reconstructed **68,305 metric rows** from source graph/events, candidate state and saved answers. There are 15,920,640 saved prediction elements; these include repeated correlated phases/rounds/roles and are **not** that many independent experiments. `evidence/verification/FULL_REPLAY.json` records the comparisons.

One complete 1,200-step near-binder training trajectory reproduced identical loss/data records and safetensors checkpoint bytes. Its cue calibration also reproduced. Eighty research continuation cases (state/RNG, partial transaction, stale transaction, mid-maintenance and mid-query across modes/pairs) matched after fresh-interpreter restore. This is not a demonstrated production journal or integrated tri-core resume.

All main result arrays are retained. For delivery, the original compressed NPZ containers were repacked without changing any NPY entry, then XZ-compressed. `evidence/ARCHIVAL.json` and per-file archive receipts distinguish original-container, decoded-container and archive hashes, plus unchanged-entry hashes. **This is lossless evidence compression, not low-bit neural state.** The archived scorer verifies decoding/integrity and reproduces stored scores. The saved random cue evidence accounts for most of the package size.

The final delivery receipt is outside the ZIP to avoid a self-referential archive hash. It records fresh-extraction checks actually completed. No external replication, Windows execution, target-device profiling, long-running companion use, biological validation or language testing took place. Current full replay imports Unix resource telemetry and is marked unsupported on Windows without adaptation; checks/rescoring may be portable but were not tested there.

## 9. Keep, revise, and stop the open-ended sequence

**Keep:** exact scoped ownership as a tested software contract; explicit existence/readability; paired near-negative training as a useful preparation intervention at the moderately similar regime; compatible content repair and iterative readers; separate internal recovery and external recognition policies with their information advantages declared; strong simple rules and exact controls.

**Do not promote:** a learned identity system based on final answers alone; near-preparation as a solution to arbitrarily close codes; ownership metadata as proof of truth; additional cues as an equal-information neural win; or a perfect nominal score as complete memory qualification.

**Revise:** the learned binding/reading representation or interface for very similar identities. The exact writer isolates this failure instead of masking it with memory repair. Additional context can help when it adds genuinely distinguishing information, but the current cue arm is only a separate rule diagnostic.

**NBR-01 remains OPEN.** This pass does not start learning, quantization or an automatic Study010. `NBR01_STATUS_REVIEW.md` consolidates what is demonstrated, the declared scope of a usable reference, and the smallest remaining qualification comparison. Finishing a bounded NBR-01 decision should not require solving every ambiguous real-world identity problem; it does require an honest task scope, competent same-evidence conventional controls, and a quality/resource comparison rather than a chain of increasingly specialized wins.
