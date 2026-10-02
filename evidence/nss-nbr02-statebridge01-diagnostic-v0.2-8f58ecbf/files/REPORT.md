# NBR-02 STATEBRIDGE01: a saved state is not the whole task
## Execution v0.2 / prospectively locked scientific protocol v0.1

**Disposition: full capture and genuine adaptive replay completed, but the original independent whole-trajectory numerical tolerance FAILED. No qualification is claimed.** The main results below are explicitly diagnostic. All scored A class vectors and joint-correctness decisions agree with an independent float64 reconstruction, and capture/replay match exactly. Those checks do not replace or waive the failed numerical requirement. The after-repair adequacy screens also fail independently of that exception.

The key observation is not immediate unreadability of the saved state. Updated weights read the old state correctly at every initial main query, then make mistakes as they continue the task. Rebuilding the prefix with the changed weights is usually worse than carrying the old state. The fixed rehearsal partially restores behavior but does not qualify a reliable continuation mechanism. Keeping a task on its original parameter revision preserves its tested progress, while also leaving that revision ignorant of the new association correction.

## 1. Scope and authorization

The user authorized the state/learning bridge and asked whether weights could remain unchanged during a task, with context organizing experience for later learning. We selected one exact-gradient reference to isolate the interaction, not another G/L comparison. A new compatible model and task were necessary: prior TS01 and NBR02 association models have different interfaces. No historical weights or hidden state were loaded.

This is a new 16,329-parameter GRUCell(16,64)+Linear(64,9), with 65,316 float32 parameter bytes and a 256-byte task state. Four new fits were trained. Task A tracks four completion flags and reports the entire checklist plus the next incomplete step/DONE. Task B is four scoped binary associations, using the same bit-0 output logit as A. That deliberately shared output is a study choice; it is not a diagnosis of the cause of earlier NSS failures.

Task markers distinguish the meanings. A's rules stay unchanged while one B label reverses. The recurrent task state, its source prefix and original weights are preserved separately from all learning scratch arrays. Queries perform no training, and prefix reconstruction never reapplies old optimizer steps. Task routing, no-op filtering, version checks, and source records are ordinary supplied code.

This does not implement learned token curation, a neural reviewer, Tertiary, self-play, a state mapper, production concurrent serving, or a new accepted NSS architecture.

## 2. Frozen task, fitting, and measurement

Each fit receives exactly 2,000 Adam updates: batch16 A episodes, alternating17/33 events, plus the four B associations. All A steps have bit and next-action supervision, and B has a binary objective. No correct state is an input. Only the terminal checkpoint is used; no checkpoint selection or fit retry.

A0 requires sufficient A competence, old B competence, a meaningful advantage over no-history reset, and exact unchanged carry/rebuild equivalence. All four fits attain160/160 joint A answers and4/4 B associations. Reset without history attains46/160. Main data are generated only after admission and the development stage.

There are32 fresh main A prefixes per fit: all16 endpoint bitmasks at lengths33 and65. Their last four public commands set the endpoint flags. Therefore this tests genuine dependence on earlier input than the final continuation cue, but not memory of every earlier event or arbitrary-horizon reasoning. The eight-event continuation leaves one flag untouched. Identical suffixes require different answers after different prefixes.

Eight B scenarios are four focal cues crossed with two receipt orders. They are not eight independent task families; cue identities and elementary orders are familiar. Two order identities were used in development. Main A prefixes are fresh and have no complete training-stream match, but the grammar and balanced end-state construction are shared.

Every scenario starts from its fit's terminal initial weights. It first creates the task-A states, then uses eight legitimate B receipts for online SGD (lr0.5, clip1), followed by four fixed repair batches (lr0.1, clip1). Each repair batch has eight actual previously observed length17 A training episodes plus all four currently released B labels. Neither current test-A labels nor hidden future feedback enter training.

At original, post-learning and post-repair weights, compare:

| Mode | Task state and weights |
|---|---|
| CARRY | Original saved h, current parameter revision |
| REBUILD | Same public prefix replayed at current weights, then the same suffix |
| RESET | Zero state without the prefix; an information-removal diagnostic |
| PINNED | Original saved h and original immutable weights |

Readouts occur at continuation positions0,1,2,4,8. Both bit-vector and next-action must be correct for joint success. All intermediate states/logits are retained. The independent task oracle, not a hidden-vector distance, supplies correctness.

## 3. Main paired continuation results — diagnostic, not qualified

Each cell below is4 fits ×8 B scenarios ×32 A histories ×5 readouts =5,120 related readings. Different modes and parameter stages are paired measurements, not new independent samples. This is a small procedural diagnostic, not an estimate of broad model accuracy.

| Parameter stage | CARRY | REBUILD | RESET | PINNED |
|---|---:|---:|---:|---:|
| Original | 5,120/5,120 (100%) | 5,120/5,120 (100%) | 1,472/5,120 (28.75%) | 5,120/5,120 (100%) |
| After B learning | 4,050/5,120 (79.10%) | 2,503/5,120 (48.89%) | 1,184/5,120 (23.13%) | 5,120/5,120 (100%) |
| After fixed repair | 4,519/5,120 (88.26%) | 3,355/5,120 (65.53%) | 1,216/5,120 (23.75%) | 5,120/5,120 (100%) |

Carry exceeds rebuild in every one of the32 fit/scenario context aggregates at both changed-weight stages. It does not win on every individual query: after learning, rebuild rescues13 carry errors while carry rescues1,560 rebuild errors; after repair those counts are19 and1,183. All exceptions are retained.

The after-repair adequacy rule requires A joint≥95%, loss versus original joint accuracy≤5 percentage points, and a correct changed-B answer. It needs29/32 scenarios and≥6/8 per fit. CARRY achieves9/32 (fits2,3,2,2); REBUILD1/32 (0,0,1,0). Both fail. These prospectively selected pilot floors are not universal operational tolerances.

## 4. The old state was initially readable; continuing the task was unreliable

At position0, before another A transition, changed weights read the original saved state correctly in **1,024/1,024** queries after online learning and after repair. Thus this dataset does not demonstrate that the state instantly became uninterpretable when weights changed.

| Continuation position | CARRY after learning | CARRY after repair |
|---|---:|---:|
| 0, immediate read | 1,024/1,024 | 1,024/1,024 |
| 1 | 1,022/1,024 | 1,024/1,024 |
| 2 | 790/1,024 | 986/1,024 |
| 4 | 604/1,024 | 815/1,024 |
| 8, endpoint | 610/1,024 (59.57%) | 670/1,024 (65.43%) |

Rebuilding was already weaker at its immediate read:483/1,024 after learning and611/1,024 after repair. Rebuilding uses the newly changed transition throughout the prefix. The original state carries information produced by the competent old transition, so retaining it can be preferable to recomputing with a damaged task mechanism.

This localizes the visible failures to processing/decoding under the changed model after its initial read. It does not uniquely identify which gate, parameter tensor, loss interaction, or representation is responsible. All six tensors were adaptive, and the shared B/A output deliberately allows interference. Neither "all state migration is broken" nor "rebuild always fixes it" is supported.

## 5. The learner did acquire B, but old B associations also suffered

| Current-weight B result | After online learning | After repair |
|---|---:|---:|
| Changed focal association | 32/32 | 32/32 |
| Other three associations | 64/96 | 83/96 |

Repair improved A continuation and most old B responses, while preserving the new B class. It was incomplete, not useless. No additional repair or different learning rate was tried after these observations.

The pinned old revision retains96/96 unchanged B responses but gives the now-obsolete focal answer in all32 contexts. Its perfect A continuation therefore cannot be counted as complete successful adaptation. It is a containment reference: the task can stay on its original competent version while learning occurs separately, but learned changes do not magically enter that old version.

There are2,240 saved B pre-feedback/post-update observations, with503 negatives across their labelled surfaces. Some surprise errors precede the first changed-label receipt. They must not be called failures to apply evidence not yet received. These overlap with other summary surfaces, so do not add them to separate query-negative counts as independent errors.

## 6. Per-task weight freezing and multiple tasks

The run uses32 logical A states sharing the same original parameter object. It does not create32 full model copies. Each state has a parameter-version identity and immutable-history reference; the actual original-weight continuation path is recomputed and verified. With pinned plus candidate revisions, parameter tensor storage is130,632 bytes, plus8,192 bytes for32 task states. These are components only, excluding optimizer, model runtime, history, gradients, and temporary/evidence arrays.

This supports a concrete narrow principle: retaining a state and the weights that produced its competent transition avoids this within-task parameter revision. It is not evidence of a scalable concurrent scheduler, atomic publication, general task isolation, or an efficient multi-version service. Execution here is serial.

A possible future scheduler can let many tasks share revision v while candidate v+1 is trained separately. New tasks or safe task boundaries can use v+1 only if its relevant competence is qualified. This study's changed model fails much old A behavior even after repair: a reset, task completion, or rebuild alone does not make it competent again. Versions cannot grow without bound; long-lived tasks create explicit residency/freshness/backlog trade-offs.

The compact-token idea could track task ID, pinned revision, event cutoff, evidence references, unresolved feedback and completion. That is proposed coordination, not a trained token interface in this run. A completed task or confident response is not automatically clean training data. Later learning requires lawful observations and corrections, source/version checks, deduplication, and failure retention; it must not apply a stale gradient to unrelated new weights.

## 7. The original numerical check failed; supplementary checks do not erase it

The original independent `source/score.py` uses a float64 NumPy GRU/backward implementation and Boolean task oracle, not Torch or producer logic. It checked37,178,292 scalar comparisons,488 recorded exact SGD updates and120 stage weight sets. All captured gradient and SGD application checks passed, but **11 array comparisons** in whole-prefix reconstruction exceeded the frozen `2e-6 + 2e-5*abs(reference)` envelope: ten logit comparisons and one state comparison. Maximum tolerance ratio was12.4231. The scorer raised an error before publishing its final tables. Its source and failed log are unchanged.

A labelled diagnostic copy publishes the same semantic results plus `strict_numerical_pass=false` and the complete failure list. It does not alter weights, outputs, thresholds, or the adequacy decisions.

Post-result localization then found:
- 21,498,624 scalar one-step comparisons, each starting from the captured predecessor state: zero failures, maximum tolerance ratio0.421119.
- 1,527,552 whole-prefix logit scalars:17 exceedances, maximum absolute difference4.33727e-05.
- 76,800 full-chain scored A queries: zero class-vector or joint-correctness disagreements; maximum query-logit difference9.83880e-06.

Accumulated float32/float64 trajectory differences are consistent with these observations. This is not a proved numerical error bound, and one-step agreement is a different test. The original whole-trajectory numerical admission remains failed. Report the class findings as reproducible diagnostic evidence, not a fully qualified study. No unrelated historical underflow amendment is applied.

## 8. Full adaptive replay, independent data audit, and omissions

A fresh process reinitialized and repeated every initial fit, probe, context update, fixture and readout. All1,656 original/replay files matched byte-for-byte:229,901,990 bytes per side. This includes complete initial training hashes/checkpoints, not merely frozen evaluation. The eleven diagnostic score/audit files also matched across the two independently rescored captures. This is internal reproducibility, not third-party replication or cross-device equality.

The independent data/ledger audit reconstructed3,208,000 A prefix targets and checked8,020 initial/probe input hashes, every training pre/post parameter-hash link, terminal files, and9,896 durable intent/commit pairs in the current primary run. Intent records include operations besides parameter applications; they are not all optimizer steps. Plain online/repair SGD has no optimizer slots. Initial Adam checkpoints include model/optimizer/runtime RNG/dedicated RNG/cursor at0,250,...,2000.

Initial-fitting raw gradients and full activation graphs were not captured at every step. Loss/norm/input and parameter identities were captured each step, with full checkpoints and exact independently reexecuted learning history. Online/repair gradients, pre/post weights and reconstruction states/logits are captured. This explicit omission does not retroactively restore missing historical Q010 evidence.

## 9. Earlier engineering stop and attempt accounting

v0.1 stopped on the first untrained-fixture update because a tensor shape property was called as a function. The exception occurred before the first tensor `copy_`. One update attempt, one backward, and three cell/head examples are charged; no durable completion or full gradient/post-state capture exists. Source, recipe and traceback remain in `attempts/v0.1`. It is not labelled zero work or silently treated as a committed update.

v0.2 corrected only that shape access and saved initial fixture weights before dispatch, then established a new source lock before any numerical work. No main fit had begun in the stopped version. No scientific threshold, event schedule, initialization seed or learning rate changed.

| Quantity, all attempts including v0.1 | Actual | Frozen cap |
|---|---:|---:|
| Parameter application attempts | 17,025 | 18,000 |
| Durable parameter application completions | 17,024 | — |
| Reverse-mode backward attempts | 17,017 | 18,032 |
| Recurrent cell examples | 7,393,659 | 12,000,000 |
| Output head examples | 7,425,147 | 12,000,000 |

The completed passes include isolated four wrong small-vector applications each; those are fault fixtures, not corruption of scientific weights. No fit retry, favorable-seed replacement or extra repair occurred. Independent NumPy arithmetic is additional audit work, not unreported neural training.

A reconstruction of the32 main prefixes costs1,568 extra recurrent event examples in addition to256 suffix examples:1,824 versus256 for one stage/scenario. This is7.125× as many event computations for that comparison, not a wall-clock ratio or global cost advantage. Exact ordinary checklist tracking needs only four logical bits plus bookkeeping; no neural compression superiority is claimed.

## 10. Delivery, future scope, and decision

Numerical NPZ files are losslessly encoded together. Every original NPZ file is reconstructed to its exact hash; original/replay aliases were created only after the genuine adaptive replay and exhaustive byte equality check. Expanded copies have a larger logical footprint than the delivered compressed archive. Restoration is not new inference or invented evidence.

Read the external delivery receipt for fresh-extraction, restoration, manifest and relocated diagnostic-rescore checks. The receipt can verify stored evidence; it cannot turn the original numerical exception into a pass. `source/score.py` is retained as the original strict check and is expected to fail on the preserved cases.

Record `RET-STATEBRIDGE-NUMERIC-001` for the whole-prefix arithmetic contract, and `RET-STATEBRIDGE-CONTINUATION-001` for incomplete post-learning/post-repair task competence. Per-task versioning and token-guided data curation remain separately scoped proposals. The next decision should not blindly add a state mapper: the current updated task operator itself is inadequate on rebuilt history.

NBR01 bounded closeout is unchanged; NBR02 stays active and mechanism-led. No tri-core or shared-backbone architecture is adopted. No old model is retrained, no RAG source retired, no Tertiary/self-play study run, and no automatic NBR03/04 advance. Existing workspace, dream, cost-accounting and foundation-return tickets remain. The user's original unspecified earlier NBR01 return is not silently assigned to a different question.

**Bottom line:** preserving h is not enough to preserve the task computation. Keeping h with its original weights preserves this task, while new learning on another revision still needs stronger old-task competence and a tested adoption boundary. Full history reconstruction was not a remedy for the changed model in this diagnostic.
