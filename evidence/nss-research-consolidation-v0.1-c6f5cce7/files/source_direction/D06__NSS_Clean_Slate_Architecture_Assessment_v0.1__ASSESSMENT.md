# NSS clean-slate architecture assessment
## Hypothetical challenger design v0.1

**Status:** design assessment requested by the user, not an adopted architecture replacement or experiment. The accepted tri-core specification, historical verdicts, NBR-01 bounded closure, active NBR-02 work, deferred tickets and foundation-return plan remain unchanged. No models, gradients, training, numerical reanalysis, source deletion, or live migration were performed for this assessment.

## Recommendation

Preserve stable general/identity-bearing cognition, adaptable competence, recurrent task continuity, explicit evidence, compact management context, and dreaming. Do not assume these functions must reside in three independently trained full-scale models. The preferred new challenger is a **shared-backbone, multi-timescale NSS** with bounded learned memory and phase-separated consolidation. A native-state tri-core variant remains a serious competitor, not a rejected architecture.

This is a hypothesis about implementation boundaries. Sharing foundational computation could reduce duplicated representation and inter-model transfer work, but costs, correlated errors, interference and capacity limits must be measured. It is not an efficiency claim or evidence that a three-core design failed.

## What the current results establish

TEACH01 uses a 674-parameter frozen teacher surrogate, adaptive student surrogates and a programmed curriculum coordinator. Teacher access improves final loss on old associations omitted from direct replay. Ordinary replay and every deep branch also meet the primary feasibility screen; the cheaper light-maintenance-only branch qualifies, and direct full records slightly outperform teacher-plus-recent replay. No learned Tertiary, general identity model, cumulative plasticity test or integrated tri-core comparison occurred.

MICROMACRO01 establishes a bounded learning-and-repair cycle under explicit investigator-selected allowances. Distributed and equal-work late rehearsal both qualify; distributed maintenance improves the middle, late rehearsal slightly improves the end. Conditions restart from initial checkpoints; results do not establish lifelong plasticity or the necessity of three separate networks.

The earlier CM studies favor exact lookup for addressed payloads and show a deterministic string/index tie. TS01 supports bounded learned task-state retention. Neither result means neural computation is unnecessary; they help assign exact records and unfinished computation different responsibilities.

Sources: TEACH01 REPORT.md §§2–6,9; MICROMACRO01 REPORT.md §§1,4–7,10; CM-02 review §§results/decision; TS01 report and its scope review. Reports were read; their numerical executions were not reproduced in this assessment.

## Proposed organization

### 1. One competent, participating general backbone

A stable accepted backbone handles interpretation, general reasoning, language and identity-bearing behavior in both task and reflection phases. A native recurrent/attention hybrid is the research preference, not an already-selected implementation. Reuse an existing competent foundation for a practical prototype; a new native interface needs training or verified transfer, not attachment of an untrained memory block.

The foundation is not merely an output narrator. It reads task state, selected memory and evidence, and participates in ongoing computation. It remains frozen within an accepted generation. Stable parameters are not by themselves a guarantee of stable behavior: changing context and memory still changes outputs.

### 2. Distinct state and memory contracts

| Component | Purpose | Lifetime/change rule |
|---|---|---|
| Working recurrent state | Unfinished computation and task progress | Evolves across events; task-scoped checkpoint/rebuild |
| Bounded learned adaptive memory | Acquired associations, preferences and reusable patterns | Declared fast update surface; repair and consolidation |
| Compact management context | Goals, scope, constraints, evidence/version references and pending work | Observable-event updates; bounded slots |
| Exact/structured evidence store | Current facts, corrections, important episodes and provenance | Explicit source and retention policy |
| Accepted foundational parameters | Broad general competence and slowly consolidated capabilities | Qualified generation changes |

No channel is an unlimited archive. The task state and the fast adaptive memory are distinct even if a chosen architecture represents both with tensors. A fast-weight memory is not automatically exact or immune to interference.

### 3. Control where learning happens

Do not send every newly observed fact through a broad weight update. Record a unique factual correction exactly, update task state for current progress, and use the fast learned surface for the adaptation it is designed to support. Promote durable, evidence-supported generalizations into a candidate slow foundation during consolidation.

The main architectural hypothesis is that a smaller, explicitly bounded adaptation surface can reduce the scope and cost of harmful changes compared with adapting all of a second general-purpose model. This is not proved. Even frozen foundational weights can produce bad answers when conditioned on corrupt learned memory; all output effects remain scored.

This proposal does not silently reintroduce the removed specialist-overlay system. It proposes one defined native adaptive-memory interface rather than an unbounded collection of interchangeable LoRA-like specialists.

### 4. Dreaming as a real computation mode, not necessarily a separate full backbone

Maintain separate task and reflection states. The reflection state may hold counterfactual branches, appraisal, unresolved investigations and curriculum progress. The same foundational computation can be used at a different time with this different state and access policy. Distinct state does not supply independent reasoning errors or prove a shared network is adequate at world modeling.

A dream uses a frozen journal interval, current evidence, retained exemplars and accepted teacher snapshots to prepare practice, train authorized candidates in separate subphases, evaluate them and propose adoption. The learner must actually execute to train. Hypothetical outputs stay distinct from observations. No final confirmation labels enter curriculum selection.

A dedicated Tertiary model is warranted if it adds useful world-modeling, curriculum generation, reflection or error diversity beyond shared-mode cognition at a justified resource cost. It is not removed from the project by this hypothetical assessment. Its functional role survives regardless of eventual physical placement.

### 5. Identity, review and adoption

Keep behavioral identity grounded in the trained foundation, versioned commitments and autobiographical/source records. This is not a claim that a personality is merely a configuration file. Use evidence-grounded behavioral checks across updates.

Evaluator functions measure effects; review interprets them; deterministic authorized policy governs adoption. The neural Validator remains advisory. Do not train a new general evaluator before identifying a judgment a cheaper ordinary check cannot provide.

Preserve raw candidate outcomes, repaired outcomes, served outcomes, deferral costs and new-learning latency separately. A reject-all policy cannot qualify as continual improvement. Share no final test answers with either the candidate or its reviewer.

### 6. Resource and version boundaries from the start

Budget model residency, adaptive state, task state, archive/indexes, candidate/optimizer copies, replay examples, generator work and rollback. Shared weights remove duplicate weight storage only where actually shared; they do not eliminate additional calls, activations, private states or training copies.

Bind task state and credit traces to their parameter/memory versions. A fast-memory update can also invalidate derived state even when the backbone is frozen. Consolidation and foundation changes need explicit migration/rebuild boundaries. Exact archive retirement remains separately authorized.

Increase capacity only where a measured bottleneck warrants it: state, learned memory, foundation, or a dedicated reflection model. No fixed-size design can preserve unlimited independent exact facts.

## Research influences, not NSS evidence

- **Griffin** (arXiv:2402.19427): combines recurrent sequence processing with local attention. Motivates a hybrid rather than an anti-attention requirement.
- **Learning to (Learn at Test Time): RNNs with Expressive Hidden States** (arXiv:2407.04620; ICML 2025): investigates a learned model as sequence state, updated through learning. Does not establish autonomous lifelong companion memory.
- **Titans: Learning to Memorize at Test Time** (arXiv:2501.00663): integrates learned memory with attention. Its memory mechanisms are precedents, not an exact implementation plan or a guarantee of retention.
- **Progress & Compress** (ICML 2018): separates active learning from consolidation into a knowledge base. Its topology and adaptation rules differ from both current NSS and this challenger.
- **Loss of plasticity in deep continual learning** (Nature 2024, DOI 10.1038/s41586-024-07711-7): distinguishes continued learning capacity from old-task retention, and studies selective feature replacement. It is not a general retention solution or authorization to reset NSS units.

Primary abstract/method pages were consulted; no external implementation was run. The proposed NSS combination is not claimed novel or empirically qualified by these papers.

## The next architectural discriminator, not a dispatch

Keep three contenders available: (A) a strong stable-backbone plus explicit memory/task-state baseline; (B) the proposed shared-backbone plus learned adaptive memory and consolidation; (C) a native-state tri-core design with a genuinely learned reflection/curriculum function. Do not call a programmed selector a trained Tertiary or replace the current tri-core design with a deliberately weak approximation of it.

Define a continuing task stream containing arbitrary facts, related procedural skills, scoped corrections, interference, interruptions, retention pressure and genuinely new tasks after maintenance. Keep future test information unavailable to learning. Do not reset to the original checkpoint after every opportunity when claiming accumulated progress or plasticity.

Compare retained useful capability, later acquisition, repair/reconstruction work, activation of legitimate corrections, archive growth and whole-system cost. Components may share budgets rather than exactly equal parameter counts; report the trade-off explicitly. Start with one model-partition question while keeping information access, task requirements and ordinary controls as comparable as feasible. A short pilot is not an instruction to build every layer at once.

A bounded result may favor the simpler system. Evidence for a valuable separate Tertiary would also justify retaining it. The design choice is the physical division of cognition and learning, not whether reflection and maintenance should exist.

## Bottom line

Keep NSS's stable/adaptive/consolidating functions. Rebuild the challenger around explicit memory lifetimes, controlled plasticity and one coherent computation path. Make three independent full models an empirical option rather than the starting axiom. Current canon and study verdicts stay unchanged until an explicit architecture decision.
