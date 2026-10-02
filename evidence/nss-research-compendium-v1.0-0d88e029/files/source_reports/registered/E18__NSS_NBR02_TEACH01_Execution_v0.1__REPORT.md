# NBR02-TEACH01 — Primary-guided consolidation with recent experience
## Execution v0.1 / prospective protocol v0.1 · measured host date 26 September 2026

**Result: the teacher-plus-recent-evidence branch met the bounded feasibility screen in 32/32 assessment contexts for each learner. Its predeclared incremental-teacher discriminator also passed. However, ordinary replay and the other deep-consolidation branches met the same feasibility screen, and even no deep consolidation qualified at 29/32.** This is a modest mechanism result, not evidence that a complete three-core architecture is necessary, uniquely best, economical, or nearly fully reparative.

The actual teacher/student computations ran and were independently audited and replayed. Tertiary was a fixed, inspectable curriculum coordinator, not a learned model. No historical model, serving Primary, architecture master, or old study was changed. No source retirement, enlargement, self-play, live-state migration or deployment occurred.

## 1. Which direction this tests

The user returned to the idea of a stable Primary teaching the adaptive Secondary during a deeper dream, with current retained experience preserving acquired changes. This is **Primary → Secondary**. The separate broader target of teaching a cloned successor Primary from Secondary, and growing cores, remains deferred.

The source concept explicitly recommends separating teacher availability from recent replay before crediting a trained Tertiary. This pilot is an investigator-specified realization of that discriminator. The finalized protocol and executable implementation were exported before any model work. New limits and task decisions are laboratory choices, not production NSS policy.

## 2. Actual learner and evidence arrangement

Four fresh Primary-surrogate models learned eight stable binary associations with 100 exact-gradient updates each. All four finished 8/8 correct and were frozen thereafter. They use the same 674-parameter, 16-unit dense tanh recurrent family as the earlier experiments, not general language or identity models. Both exact-G and approximate-local-L Secondary surrogates start from the corresponding teacher's weight copy and then learn independently. This common start is a new design choice, not a claim that earlier G/L studies did the same.

The Secondary's compact old-record buffer contains four of the eight old associations, one per scope/label combination. The other four have cue descriptors but no direct hard-target access in compact replay. A teacher can provide its own distributions on them. The full audit source is retained; **no data was actually deleted**. This is numeric record lookup, not a language RAG implementation.

The teacher never receives the new focal labels. Each student sees an original focal association and then a lawful reversal, receives identical light four-record repair after three stages, and reaches a common pre-dream state. Six branch copies then receive the declared deep treatment. The two subsequent real receipts continue learning after dream completion, with no extra repair.

There are four development and eight assessment focal bases crossed with four teacher initializations and two student learning rules: 96 method/fit/base contexts. Every context restarts from its teacher checkpoint. Eight assessment bases × four fitted teachers = 32 contexts per method, not 32 independent task families. Repeated records/checkpoints/replay do not create new independent tasks. The association grammar is shared; this is not broad task generalization or cumulative learning.

## 3. Controls and actual teaching

All active deep treatments use eight updates of eight examples each, with the same half-size post-clip step. Four compact old examples remain in every batch. Two slots switch between extra compact-old practice and teacher outputs; two other slots switch between extra compact-old practice and the current focal record. Teacher targets are real frozen-model soft probabilities at temperature 1, not evaluator gold. They are cached from a version-bound teacher phase, and queries and cache reads are counted.

| Branch | Deep treatment |
|---|---|
| NONE | No deep consolidation; retains the common prior light repair. Cheaper, not an entirely unmaintained learner. |
| REPLAY | Compact old-record hard targets only. |
| TEACHER | Compact old records plus teacher targets for the four omitted old associations. |
| RECENT | Compact old records plus the latest validated focal record. |
| BOTH | Compact old records plus teacher targets plus the latest focal record. |
| FULL_RECORDS | Same inputs as BOTH, but missing-old hard labels supplied from an explicitly expanded buffer instead of teacher outputs. |

All G examples use exact reverse-mode gradients. All L examples, including soft-label distillation, use its existing approximate local equation. No exact-old protection hybrid, projection, model-size change, learned selector or output repair was added.

The full-record comparator is an information/storage upper reference, not an equal-memory competitor. It is important because a teacher might merely substitute for unavailable old labels rather than provide some unique learning advantage. Teacher snapshots/caches are not free, and the four missing one-bit toy labels are vastly smaller than the teacher model. There is **no storage-efficiency victory** here.

## 4. Primary results

The fixed screen requires current focal probability at least .75 and class correctness, average old-probability decrease at most .03 from the common post-receipt2 anchor, no individual old decrease above .20, at least seven of eight old classes correct, and a positive nine-record current-target probability gain. These must hold at dream completion AND after each of the two additional receipts. A method-level branch needs at least 29/32 successful assessment cycles and at least 6/8 in every fit. Raw intermediate behavior is separately retained; this is recovery/persistence, not prevention of every transient dip.

| Branch | G cycles | L cycles |
|---|---:|---:|
| NONE | 29/32 | 29/32 |
| REPLAY | 32/32 | 32/32 |
| TEACHER | 32/32 | 32/32 |
| RECENT | 32/32 | 32/32 |
| BOTH | 32/32 | 32/32 |
| FULL_RECORDS | 32/32 | 32/32 |

All rows satisfy the method-level primary criterion. Thus a blanket PASS alone does not establish that the teacher, recent replay, or even deep consolidation is necessary at this difficulty. The cheaper reference matters. All actual post-update inventory class answers were correct across the recorded pilot; the measured differences are probability quality and the defined full-cycle operating limits, not repair of lost class answers.

The teacher-value discriminator was separately fixed: BOTH versus RECENT must lower final omitted-old mean loss in at least 6/8 base means, with pooled decrease >=.001 nats and no more than one added focal-class error. It passed for both learners, with 8/8 favorable base means, no added focal class error, and decreases .00188304 G / .00213751 L. This is an exploratory margin, not a confidence interval or global distillation theorem.

## 5. What the teacher and current records contributed

Final mean loss on the four old associations whose direct labels were omitted from the compact buffer:

| Branch | G | L |
|---|---:|---:|
| NONE | .02240566 | .02174632 |
| REPLAY | .01197906 | .01228108 |
| TEACHER | .01051281 | .01057802 |
| RECENT | .01365918 | .01400690 |
| BOTH | .01177614 | .01186940 |
| FULL_RECORDS | .01160528 | .01168791 |

Adding Primary teaching to the recent-replay branch reduced this loss by about 13.8% for G and 15.3% for L. These are relative changes in probability loss, **not percentage-point accuracy gains**. All these final class answers were already correct.

Adding recent evidence to teacher-only consolidation reduced final focal loss from .00890181 to .00728793 (G) and .00891720 to .00730179 (L), while slightly worsening old-answer loss. The new answer remained correct with or without that replay. This is complementary confidence management, not proof that RAG was necessary for remembering the new association in this tiny task.

FULL_RECORDS was slightly better than BOTH on final old and focal mean loss. Direct current labels are a strong reference. The teacher's practical role here is to supply useful base behavior not directly present in the compact replay buffer, not to outperform complete accurate records.

The factorial contrasts and all per-fit/base results are in analysis/PAIRED_CONTRASTS.csv and analysis/FACTORIAL_INTERACTION.csv. They are descriptive and do not claim universal synergy. The same teacher can improve one side while recent replay favors another; all components remain visible.

## 6. Failure and interpretation limits

There are 189 incorrect recorded query rows in primary capture: 43 during teacher-training pre-feedback predictions, 52 development focal pre-feedback predictions and 94 assessment focal pre-feedback predictions. Every row, including all correct rows, remains retained. No inventory class error was observed. The six NONE cycle failures across G/L concern the operating envelope rather than incorrect old classifications. Replay is not a second scientific sample.

The source interval contains no accumulated long-term plasticity decline, no actual lost-class recovery, no tests of many general capabilities, and no subsequent wholly new task after the dream. T7/T8 repeat an old protected cue and the current focal association. The Primary is the same size as the student, not a larger general teacher. Its own eight foundational answers were all correct, so fallible/wrong teacher targets were not a scientific treatment. It does not know focal targets and is never asked to supersede their current record with an obsolete teacher target.

The record shortlist is supplied by code; a learned Tertiary did not diagnose failures or select a better curriculum. The pilot implements numerical distillation/rehearsal, not semantic natural-language retrieval, identity repair, or live Primary/Secondary/Tertiary concurrency. Cached Primary targets are used during student updates; always-active Primary coordination is not separately implemented or evaluated.

These boundaries mean the result supports a **small part** of the proposed dream: fixed foundational teaching can complement recent evidence in repairing an adaptive student's probability quality. It does not validate the full dream, approach complete repair in general, or justify erasing the retrieval archive.

## 7. Execution, costs and source integrity

Both full adaptive executions completed with identical recorded numerical evidence, inputs, gates, teacher versions and score tables. No teacher or student fit was retried, selected away, extended or tuned. All four teacher fits and all G/L development student admissions passed.

All-attempt capture plus replay: 12,528 parameter applications/commits, 68,132 example-gradient calculations, 538,956 cell evaluations, 179,652 head evaluations, 57,600 source-record fetches, 6,144 teacher-cache reads. These stay within the frozen caps. The application count includes four deliberately wrong sandbox updates per pass; their weights never enter scientific learning. Four additional clean batch applications per pass and soft-target derivative checks are retained. Teacher fitting, fixed teacher queries, and student work all count. Equal student batches do not imply equal whole-system memory or computation cost.

Independent NumPy audits reconstruct forward states, exact/local soft-target derivatives, authoritative targets, batch reductions, norm clipping, exact defined parameter subtraction, teacher immutability and candidate-state lineage. Each audit checked 29,078,932 scalars, maximum tolerance ratio .0608648 under the declared empirical envelope. Arithmetic tolerance is not a formal rounding proof. All update intents had durable commits; no unknown-completion neural update occurred.

Fresh adaptive replay matched 7 raw files including a 263,184,960-byte numerical stream, plus all 6 independent audit/score files. That stream contains 15,046 frames, 116,296 arrays and 56,445,194 elements **per pass compared**. Duplicating the count does not add scientific cases. Native training memory and deployed latency have not been exhaustively profiled. Sampled peak child RSS was 330,551,296 bytes; the largest sampled container reading during neural stages was 3,460,104,192 bytes, below the frozen 3.5GiB limit. Sampling can miss short peaks.

## 8. Engineering incidents and delivery scope

Before the source lock, a requested streaming terminal session was unsupported. No execution worker or new source-lock artifact existed after that rejected invocation; preparation proceeded with bounded foreground calls.

After the successful primary execution/audit, a compound shell call timed out after finishing a lossless XZ encoding. The verified primary evidence and encoding receipt survived. The subsequent status update and replay directory had not been created, and no worker was observed. Replay was then dispatched once through its own foreground call and completed. This was not a scientific retry or an unknown-completion update.

The primary numerical stream is losslessly encoded; its decoded size/hash was verified before removing the redundant raw copy. The replay stream was independently produced and verified against that identity before replacing duplicate storage by a declared alias. Six identical replay scoring files are also aliased after equality. Restoration recreates original retained bytes, not invented model outputs. Expanded logical byte totals count aliases; they are not the concurrently encoded storage footprint.

Eight post-execution copied-evidence checks cover teacher-target alteration, obsolete focal label, wrong scope, changed prestate, wrong parameter application, and complete/missing commit records with clean controls. These are separate small copied-record probes, not a live adversarial core/credential system. The four actual wrong-sign numerical applications in each pass were independently detected. The pilot has no formal file-isolation or authenticated external-measurement guarantee.

Final fresh-extraction verification and relocated NumPy rescoring are reported in the external delivery receipt. This report does not substitute for that receipt.

## 9. Architecture and next boundary

AER-NBR02-TEACH01-001 records a bounded Primary-surrogate→Secondary-surrogate teaching result with a fixed coordinator and current evidence. Retain the combined branch as a mechanism reference, not as a uniquely necessary or efficient production choice. All former scientific screens stay unchanged.

NBR01 remains bounded-closed; NBR02 active. MICROMACRO01 remains a different retained reference. Primary-generation renewal, core enlargement, RAG retirement, learned Tertiary and self-play remain deferred. Pending state/weight migration, native cost-accounting gaps, the parked NBR01 question, and FCR-0103-001 remain open. No serving adoption or further numerical campaign is dispatched.

**Bottom line:** the proposed teaching direction is executable and contributes a small, consistent improvement on old associations not directly available in the compact replay buffer, while source-grounded recent rehearsal supports the newly learned answer. Simpler replay also works here, and complete hard records are slightly stronger. This is evidence for the ingredients, not a demonstration that the complete dream architecture has been built or optimized.
