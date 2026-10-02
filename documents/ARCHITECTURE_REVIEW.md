# NSS architecture review — updated 2026-09-29

## BRIDGE01 and low-bit research priority — 29 September 2026

The user now prioritizes low-bit inference and training. Earlier COMP01/MEM01/PREP01/CYCLE01 and DIRECT01 questions remain retained and deferred; they are not a prerequisite waterfall for this new branch. [BRIDGE01 review](Research/NSS_NBR02_BRIDGE01_Low_Bit_Review_v0.1.md) records the bounded analysis and next candidates. The prototype demonstrates retained scripted workflow, exact-ledger checks and a frozen learned checklist advisor, with simulated SQLite effects. It does not demonstrate a language-capable companion, superiority to rules, low-bit execution or learning.

Its strongest immediate use is an inexpensive test of where precision matters. Preserve the original float64 runtime as a reference, compare float32 and bounded weight quantization, then isolate recurrent-state precision. Packed bytes, simulated quantization and native kernel performance are different findings. Low-bit adaptation must count any full-precision backbone materialization, master weights, gradients, optimizer state and activations; adapter learning is not full-parameter low-bit training. Numerical drift may be tolerable while loss of task meaning is not, so report graded usefulness and critical-effect categories separately. The exact ledger remains unchanged in these proposed neural precision comparisons. No model topology is adopted and no experiment was executed here.

## Current evidence-led direction and DIRECT01 — 28 September 2026

The user's new Evidence-Led Research Plan v0.1 is the current proposed direction. Its strongest choices are a competent language reference before memory claims, ordinary retrieval/replay controls, accumulated accepted revisions rather than repeated resets, and explicit measurement of evaluator fallibility. Support COMP01 → MEM01 → PREP01 → CYCLE01 as a decision sequence; keep resource metering and small integration checks throughout, with one conditional ADAPT01 mechanism. Earlier topology and next-pass recommendations below are historical, not a mandate to reinstate them. This review adopts no implementation or architecture.

The [DIRECT01 handoff](Research/NSS_DIRECT01_Chat_Handoff_v0.1.md) makes direct generation a narrow optional hypothesis: jointly predict structured fields from a shared frozen competent backbone, compared with a newly trained AR field readout using identical evidence, targets and serialization. Both primary arms receive no checker feedback or repair; AR keeps normal caching, and all training, encoding, decoding and checking costs count. A factorized parallel head may fail cross-field dependencies; success on a small fixture would not establish general language generation. Place it within MEM01/PREP01 only when the output question warrants it, rather than making it a new prerequisite.

The [Chat package](Research/NSS_DIRECT01_Chat_Handoff_v0.1.zip) preserves the supplied roadmap and DARP report. The roadmap reports RECOVER01 v0.2 recovery with retained corrections and residual false-DONE/numerical failure; its newer source records, including BALANCE01/TRACE01, were not located in this bounded review. Reconcile those identities in Chat before execution reliance, without rerunning completed work to fill a documentation gap. No model, device, numerical acceptance threshold or experiment budget has been chosen. The requested handoff is complete and remains protocol preparation only.

## DARP results and direct-output hypotheses — 28 September 2026

Source: [DARP01–03 consolidation and decision](NSS_DARP_Research_Results_Analysis_and_Decision_v1.0.docx), especially sections 3–5 and 12–19. This review used the supplied DOCX's body/table text; source identity and extraction method are in `.consolidation/20260928/darp_review/SOURCE_IDENTITY.json`. Its cited execution archives, checkpoint files and raw outcomes were not opened or independently recounted in this review. The following measurements are report-derived.

**Assessment:** retain AR as the current supported writer reference and park this DARP implementation as a candidate. DARP became a capable supported writer, but there is no demonstrated quality/cost reason to replace similarly supported AR. This is a result about this preparation and fixture, not a general impossibility result for diffusion output or a statistical equivalence finding.

The prospective DARP03 N comparison is close: static complete handoffs 359/384 versus AR 361/384; changed-plan handoffs 128/150 for each; equal-family macro 89.41% versus 89.67%. DARP repairs 391/431 common erroneous blocks versus AR's 386/431, but the five-block difference does not establish a general editing advantage. Median sampled episode time is 10.041 versus 9.418 ms, approximately 6.6% slower. The reported false-COMPLETE handoff outputs are 6 versus 1; these remain errors even when the supplied checker prevents publication. They are not six successfully committed false completions.

The preparation finding is more substantial: DARP N gains 21.19 macro points over same-panel U and 5.77 over the matched authored-error C branch. Real erroneous draft content helped this DARP preparation beyond merely choosing the same difficult cases. AR does not show the same consistent benefit; retain that contrary evidence. Planning, checking, editing, source binding and sequential commits are shared workflow mechanisms, so their usefulness does not establish that diffusion is required.

One constraint matters for interpreting the decoder comparison: the later wrapper supplies 13 of each block's 17 tokens. Only four fields are learned, while DARP uses four denoising steps. **Hypothesis:** that small amount of parallel work leaves limited opportunity to offset repeated refinement. This is an architectural observation, not an experimentally isolated explanation or a promise that longer blocks will win. The timing sample is small CPU execution, and AR lacks an optimized incremental KV cache. Three inherited parent pairs and a perfect task-specific checker further limit generalization.

### What output “directly from weights” could mean

Both AR and DARP already obtain predictions by applying learned weights to input-dependent activations. The weight file is not a prompt-addressable table of finished answers. The useful alternative is to change how those activations become output: predict a whole structured block or several tokens together, rather than requiring a fresh sequential prediction for each token. Existing AR weights cannot simply be switched to an unfamiliar bidirectional denoising/readout interface with an assumption of preserved competence; that interface needs training and evaluation.

My leading candidate is **shared or stable backbone → task/evidence representation → parallel block-output head → bounded optional refinement → checked commitment**. The backbone computes the context; a smaller learned head predicts the block jointly. Reuse of context representations could reduce repeated work if the architecture permits it, but those representations must be bound to the same source/model version. Joint output slots still need to agree about order, state and completion. Any gain must survive whole-handoff scoring and total-cost accounting.

Three possible future arms, not a new dispatch:

1. **Direct parallel fields as the simplest baseline.** Train a head to predict all four substantive fields together from shared context. This asks whether the fixture needs either a token-by-token loop or four denoising passes. Independent heads can disagree, so whole-record consistency remains central. [Multi-token prediction](https://arxiv.org/abs/2404.19737) provides a related shared-trunk/multiple-head precedent, not evidence that this exact NSS design works or that plain parallel decoding preserves an AR distribution.
2. **A distilled fast proposal with selective refinement.** Teach one or two proposal steps using checked teacher outputs and genuine error cases, then spend extra passes only where justified. This transfers some iterative work into training; it does not remove its cost or guarantee better correctness. [Consistency models](https://arxiv.org/abs/2303.01469) establish a one/few-step precedent in image generation. Transfer to this discrete-token task remains an untested hypothesis.
3. **DARP as a specialist editor alongside AR.** Generate a draft with the supported writer and use the denoising interface only for bounded edits or changed evidence. It must beat AR editing on the same drafts and total budget; DARP03's five additional common repairs are insufficient to establish that advantage.

[Block Diffusion](https://arxiv.org/abs/2503.09573) demonstrates the broader research family of sequential block conditioning plus parallel within-block denoising. The present tiny prototype is not a reproduction of its full training recipe, and the paper's benchmark results do not transfer to NSS. Primary abstracts/bibliographic pages were checked for these three references; no new model experiment or full literature survey was performed.

The practical decision can therefore remain unchanged while preserving the idea: the current four-step implementation is parked; a trained parallel output interface is technically plausible and scientifically distinct. HSA remains a separate evidence/execution component, and changed-weight continuation remains open. No DARP04, integration, backbone replacement or training is authorized by this review.

## HSA and segmented-context detour — 28 September 2026

**Assessment:** this is useful component-level progress and a reasonable stopping point for the present subproblem. Retain the working reader, exact versioned records, resumable execution, ordinary streaming comparators and mixed-prepared candidates. The supplied consolidation's recommendation to park the component is sensible. This review does not adopt a replacement NSS architecture or dispatch DARP, integration or another experiment.

Source: [HSA/segmented-context consolidation v1.0](NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.md), especially sections 3, 5, 8–12 and 14; its [complete evidence bundle](NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.zip) retains six original execution archives. The Markdown is the scientific review text; supplied files are preserved. Fresh checks covered the 81-member outer archive, all 80 manifest payloads and standalone Markdown/DOCX byte parity. The receipt and limits are under `.consolidation/20260928/hsa_review/`; no raw scientific-output recount was completed. Historical numerical, model-replay and training results remain reported evidence, not new Codex experimental replication.

### What the detour accomplished

Think of a small desk, a filing cabinet and a saved worksheet. The desk holds a few records at once. The cabinet holds the rest. The worksheet preserves the exact unfinished calculation, so changing which records are on the desk does not force the work to restart. The important result is that useful computations can finish this way; the records have not all been compressed into the desk.

| Finding | Evidence and meaning |
| --- | --- |
| The supplied hierarchy helped this learner. | SH01 reports 6,133/6,144 HSA decisions correct versus 5,553/6,144 for dense attention across three complete paired fits. This supports a useful task-specific structural bias under the fixed recipe. |
| Streaming enlarged executable reach. | CAP01 completed cases needing 69–755 input positions with a 32-position active tile. Its 3,904 decisions matched the full same-weight reference; some reference answers were wrong. Ordinary streaming achieved the same capacity and answers. |
| Preparation improved interpretation. | CAP02 mixed-size preparation raised HSA's selected 128-task score from 749/768 to 766/768 and its whole-job score from 80/96 to 94/96. Eight-task selected performance reached 768/768. These are different denominators, not one pooled benchmark. |
| Some added machinery was counterproductive. | SC02's intermediate neural cache avoided nearly 47% of first-layer row calculations but was slower in all 20 measured timing cells. Ordinary publication/plan reuse supplied useful improvements without that cache. |

CAP02 illustrates a useful bounded success without requiring perfection. At 128 tasks it fixed all 19 old selected errors while introducing two new ones. At 512 tasks it reached 189/192 selected answers but only 21/24 entirely correct jobs, below its declared whole-job working point. The gains and residual limitations both belong in the record. A high per-answer score is not the same as reliably finishing every job.

### What the evidence does and does not settle

The strongest transferable idea is the separation of exact evidence, current task progress, disposable model-derived calculations and advisory outputs. Source/model identity checks make it possible to reject stale work explicitly. That is useful for maintenance even without a claim that the neural model learned its own memory-management policy.

The main remaining gaps are substantive:

- **Meaning is supplied in a convenient form.** The reader consumes 37 engineered numerical channels, with task identities and dependency links supplied by software. It learns a four-way rule over immediate prerequisites. This does not yet test discovering dependencies from prose, resolving exceptions or writing reliable handoff notes. The exact software rule remains an appropriate control and, where the rule is known, an appropriate authority.
- **The attention comparison is encouraging but narrow.** There are three complete parent pairs; the dense recipe is already weaker. The result does not isolate hierarchy depth from supplied graph structure or establish an optimally trained dense ceiling. No extra comparator sweep is needed merely to retain the working component.
- **The active-tile limit is not total memory or a language context window.** Exact records, graphs, embeddings, intermediate arrays and framework allocations remain elsewhere. The 25,000-language-token maintenance idea still needs a tokenizer, workload and separate active/cumulative cost accounting. Making an attention calculation executable does not automatically make an existing language model competent at new lengths or positional arrangements.
- **Same-version resumption differs from changed-weight continuation.** CAP01 rejects stale source/model bindings. CAP02 changes weights and checks a selected fresh streaming subset; it does not migrate an unfinished old-model calculation through a learning cycle. SURFACE01's fixed-weight failure and RECOVER01's proposed acquisition/repair/state-continuation comparison remain separate questions.

For literature context, exact attention with reduced intermediate memory and tiled execution is already established in [Rabe and Staats](https://arxiv.org/abs/2112.05682) and [FlashAttention](https://arxiv.org/abs/2205.14135). My inference is that CAP01 belongs to that general engineering family; no code-equivalence or hardware-performance comparison was performed. The useful NSS evidence here is the concrete implementation, version-bound lifecycle and measured task behavior. Primary abstract/bibliographic pages were checked; this was not a new literature survey.

### My preferred next bridge

The next high-value question is **whether a model can produce a maintenance record that lets another session continue correctly**. A small prospective study could turn controlled natural-language task histories into source-linked records of unfinished obligations, corrections and unknowns. Test omissions, invented completion, stale references and successful continuation; fluent prose or valid JSON alone is insufficient. Keep an exact record-based control and ordinary retrieval/structured-output comparator so the difficult learned part is visible.

DARP can then be an optional output-method arm against direct structured generation on the same evidence and declared budget. Hold the evidence system fixed while comparing output methods. Do not change retrieval, reader, training schedule and generator together and attribute the combined difference to DARP. A later changed-weight continuity question can connect back to RECOVER01; a full end-to-end resource benchmark becomes important before deployment claims, not a requirement to keep polishing this component now.

This supports the stable-serving-weights plus external-evidence direction. It does not select a core count, establish autonomous overnight repair or replace the current frozen research architecture. The six-study consolidation and RECOVER01 should remain complementary research branches.

## Earlier architecture assessment — through 27 September 2026

Status of the earlier assessment below: design analysis of `NSS_Architecture_Learning_and_Evaluation_Handoff_v0.1.docx`, not adoption, implementation, experiment execution, or independent replication. The DOCX supplies the E00–E19 summaries below; its STATEBRIDGE account was cross-checked against the retained `source_reports/E19__NSS_NBR02_STATEBRIDGE01_Execution_v0.2__REPORT.md` in `Research/NSS_Research_Consolidation_v0.1.zip`. The other study summaries were not individually re-audited for this design review. Cited literature is documentary context; no new literature search was made. Original frozen protocols, complete study archives, and their receipts remain the authority for each scientific result. See `RESEARCH_INDEX.md` for the archive inventory and `WEIGHTS_INDEX.md` for saved parameter evidence.

## RECOVER01 proposal addendum — 27 September 2026

RECOVER01 is a prospective four-arm recovery diagnostic using all four existing SURFACE01 parents, including the imperfect parent. It compares unchanged, B learning, A-only repair, and B learning followed by matched A-only repair. It grades stable learning, full or partial recovery, tradeoffs and acquisition failure, with no retrospective change to SURFACE01 and no all-parent-perfect entry gate. This supplements master handoff v1.1 and replaces its baseline-first recommendation for this next diagnostic only. No execution or architecture replacement is authorized by the proposal.

[RECOVER01 proposal v0.1](Research/NSS_NBR02_RECOVER01_Proposal_v0.1.md). A recovery success would support bounded replay as a mechanism, not settle backbone/core topology or autonomous repair. If B is learned without old-task harm, record stable learning rather than requiring damage first.

## SURFACE01 update — 27 September 2026

SURFACE01 ended STOP_BASELINE_COMPETENCE before its main adaptation comparison. Three of four parents passed their own baseline panels; parent 4103 produced six false-DONE answers in one unchanged-checklist history, under fixed weights. Codex verified the archive and recomputed the saved admission counts/failure trace, without model execution. Reported numerical-reference, fault and fresh-process replay checks passed within SURFACE01; this does not repair STATEBRIDGE’s earlier failed numerical gate.

SURFACE01 sharpens this assessment: **stable parameters do not guarantee stable task meaning**. Three parents passed their own panels, so this is not a broad inability to learn the checklist. One connected fixed-weight failure is enough to reject the declared cohort gate, but not enough to choose capacity, optimization, representation or readout as its cause. A pending flag may remain encoded even when the head says DONE. Compare shared histories and controlled semantic variants before selecting a new topology. My strongest new candidate is auxiliary per-flag supervision plus oracle-anchored stability training, tested separately and together; an exact typed-state tracker remains a control.

The earlier baseline-first recommendation, now deferred behind RECOVER01, was baseline semantic stability: compare the same development histories across all four parents, factor pending-item burial/order/redundancy, then test auxiliary flag supervision and oracle-correct consistency training under a new protocol. Do not force hidden-coordinate equality or preserve a wrong answer merely for consistency. A learned decoder probe may test flag decodability but cannot by itself establish causation. Core count and stable-backbone topology remain unselected. The sections below retain the earlier lifecycle assessment and its conditional update-surface rationale.

## Judgment and decision map

The proposed lifecycle is a strong **candidate operating design**: accepted serving weights remain stable while task state and source-backed evidence evolve; a separate candidate learns during a bounded quiet period; the candidate is tested on new and old abilities; unfinished work is reconstructed under qualified weights before publication. This cleanly separates receiving a correction from learning it into weights, and it gives task continuity an explicit version boundary. It is more coherent than trying to make each incoming fact an immediate parameter update. The complete cycle has not been tested as an NSS system, and the currently frozen participating Primary, alternating Secondary/Tertiary, and advisory Validator remain the governing architecture.

The **functional separation** among task execution, learning, reflection, evidence review, and publication is valuable. Present results do not establish that these functions require three separately parameterized cores. Keep the frozen topology for historical comparability; test a shared or different topology only as an explicit future arm with matched capability, information access, cost, and role coverage.

| Item | Current status | Decision implication |
|---|---|---|
| Stable serving revision, live state/evidence, off-peak learning, state renewal | Owner whiteboard and proposal | Keep as a candidate; do not infer full-system effectiveness or select model topology. |
| Primary/Secondary/Tertiary/Validator roles | Existing frozen architecture boundary | Preserve them in present research; shared weights or merged functions would be a versioned alternative arm. |
| NBR-01 bounded closeout; NBR-02 active with numerical dispatch paused; `RET-MW01-FIT-001` parked | Recorded research decisions | No phase advancement or automatic return experiment. |
| `STATEBRIDGE01` readout-surface × recurrent-update diagnostic | Saved next candidate, not run | First isolate whether failure is due to the shared output surface, changed recurrence, or their interaction. |
| Experience-built practice, adaptive repair policy, evolving test library, dream/self-play, primary renewal | Proposals | Introduce each only against a fixed ordinary control and counted cost. |

## Evidence that informs the design

| Retained study | What it supports | Limit that matters here |
|---|---|---|
| CM-01/02 and TS01 | Exact reference access and, separately, learned task-state retention are useful within small tasks. | Exact index and workspace tied at 391/600 in CM-02; TS01's routing and no-op filtering were supplied. Neither establishes a general learned memory service. |
| TS02/03, CKA01 | Metadata channel use and record binding can coexist with poor derived behavior; fitting and transfer remain open. | The task/learning workspace screen failed; correct evidence binding is not task competence. |
| DC01, REV01, PROTECT01, REHEARSE01, TIMING01 | Feedback learning, faster correction, old-confidence tradeoffs, and timing-sensitive replay are real bounded mechanisms. | Some studies stop in development; later recovery does not erase earlier harm, and total native-memory efficiency is unestablished. |
| MICROMACRO01 | A small repair cycle qualified under a prospective operating tolerance, and old-record practice improved old-answer probability quality. | Qualification was tolerance-sensitive; no-repair retained old classes in this grid; the study does not establish years of cumulative maintenance. |
| TEACH01 | A frozen teacher plus recent records modestly reduced omitted-record log loss in bounded tasks. | A relative probability-loss benefit is not proof of a necessary tri-core topology or lossless knowledge preservation. |
| EVAL01/C00 | A deterministic contract and retrospective candidate evaluation can surface concrete policy and review failures. | A targeted panel can over-defer acceptable changes; no live atomic publication or long-run closed loop was shown. |
| STATEBRIDGE01 | Changed weights initially read the saved state in 1,024/1,024 cases, yet continuation degraded; carry exceeded rebuild. | Both repaired adequacy screens failed; the original whole-trajectory numerical tolerance failed on 11 arrays. Internal replay and class agreement preserve diagnostic value but do not qualify it. |

STATEBRIDGE is the sharpest constraint on the concept. A saved vector can still be readable at transition zero while the changed recurrent operator damages later work. Rebuilding through changed weights was even worse in that study. Pinning the old weights preserved the old checklist but returned the obsolete answer to the new B correction. A revision boundary is therefore a useful containment tool; it does not itself produce a competent revised model or current answers. The proposed sleep/resume cycle needs to demonstrate both task reconstruction and behavior under the revised operator.

## What is strongest in the concept

1. **Distinct lifetimes and authorities.** Parameters, recurrent state, exact evidence, resume records, repair-policy memory, optimizer state, and test cases are different objects. The proposal assigns writes and version rules to each, with the Validator advisory and publication governed separately. This is an implementable way to keep provenance and permission explicit.
2. **A whole-cycle outcome.** The objective includes accepted gain, collateral loss, disruption duration, recovery cost, rejected useful updates, future learning, and actual resumption. That is a better target than a single final accuracy score or universal refusal to update.
3. **Evaluation continuity.** Older obligations accumulate; a later test-system rebuild must pass both learner-performance and defect-detection checks. Routine exposed regression anchors are distinguished from independent confirmation. The EVAL01 false-deferral result gives a concrete reason to separate representative impact estimates from targeted risk sentinels.
4. **Honest storage economics.** Modest growth is acceptable, while retained footprint, peak migration space, compute and backlog must be measured. Exact personal facts, unique failures, and source provenance cannot be replaced by a hash, teacher, generated exercise, or fluent summary.

## Smallest improvements to the design before a lifecycle study

**Make service freshness a separate contract from weight freshness.** An old task may safely retain revision *v* while receiving a current fact or correction through retrieval/context. Define how a new correction invalidates unfinished actions, how source revisions are seen by old-version tasks, and what happens when the old model cannot act on the new information. Report correction-to-use latency and correction-to-weight latency separately. Do not call retrieval-assisted usefulness durable learned competence.

**Specify a resume transaction, not a summary format alone.** A minimal resume record should bind task identity, parameter version, source/evidence cutoff, completed and invalidated actions, external side-effect receipts, pending feedback, unresolved dependencies, and the references needed to check its completeness. Test construction and continuation while the old state/version still exist. A restart should be allowed to fail visibly; silently dropping vector-only information or replaying an external action would be worse than deferring publication.

**Keep the reviewer and repair policy narrow at first.** Use a fixed, auditable rule to choose among known repair operations and an independent evaluator with representative and targeted channels. Learn repair selection only after matched cases accumulate. Hold evaluator cases, policy version, task learner, and thresholds fixed when estimating any one improvement. This avoids attributing more data, more compute, or an easier exam to a self-improving controller.

**Put finite budgets and exposure labels on the capability library.** Keep stable known regression anchors, rotating older checks, and genuinely reserved structural variation. Record when a failed holdout enters training, when each skill was last meaningfully checked, and how many candidate generations passed since. A passing old snapshot cannot stand in for checking a materially revised model. A rebuilt suite must demonstrate defect sensitivity and coverage preservation on clean and deliberately flawed behavior, separately from current learner performance.

**Bound live versions and backlog.** Stable serving epochs trade immediate weight change for version residency and delayed skill acquisition. State a maximum number of resident weight revisions, checkpoint/candidate/rollback space, quiet-period cost, and what happens to tasks that cannot reconstruct. If deferred corrections accumulate faster than qualified cycles can process them, the lifecycle is not sustainable even when each individual cycle succeeds.

## Earlier update-surface question — deferred after SURFACE01

After baseline semantic competence is established under a new protocol, identify **which changed computation actually breaks continuation in STATEBRIDGE01**. The saved 2×2 experiment crosses shared versus copied B readout with adaptive versus frozen recurrent weights, holding B learning and all other study factors comparable. Require B to acquire its correction, score A carry/rebuild continuation and old B retention, retain the original failed numerical record, and freeze a new prospective whole-trajectory check before dispatch. If freezing recurrence prevents the loss while B still learns, the design can limit its adaptive surface. If copying the readout helps instead, the problem is more localized. If neither suffices, only then test state-anchored continuation rehearsal. These are proposals for Chat's separate protocol and execution authority, not experiments conducted in this review.

The later lifecycle comparison can then test stable-serving/off-peak consolidation against immediate serving-weight changes across continuing simulated days, with matched evidence access and full costs. It must score actual interrupted-task resumption, obsolete-answer risk on pinned versions, rejected candidates, cumulative old-ability loss against a fixed historical anchor, and correction backlog. This is the point at which the attractive operational story becomes falsifiable.

## Preserved boundaries

`NBR-01` is bounded-closed, `NBR-02` remains active with numerical execution paused, `RET-MW01-FIT-001` remains parked, and `FCR-0103-001` retains its foundation-return checkpoint. The original Q010 training, optimizer, RNG and 15 historical checkpoint bytes remain missing. G01–G22 remain in the original register, including state, depth, delayed credit, low-bit learning, evaluation, interfaces, schedule and whole-system value. No document, result, or literature precedent here establishes the final NSS architecture or authorizes local scientific execution.
