NSS: Cognition, Architecture & Low-Bit Learning

Research handoff v1.0 | 20 September 2026

Project: Neural Space Systems (NSS) / MegaMind Alpha.Purpose: Transfer the brain–fly–Transformer investigation into the dedicated NSS chat, with a consolidated problem register, recommendations for the current tri-core + validator design, an explicit redesign alternative, and a low-bit learning-state research plan.Status: Research synthesis and recommendations. Not a source-code release, accepted architecture replacement, completed training experiment, or production qualification.

Decision in one paragraph. Preserve the working NSS substrate and current tri-core responsibilities. Investigate a native recurrent, multi-timescale neural design in a separate comparison branch rather than immediately discarding the project. Prioritize persistent state, useful recurrent depth, selective learning, and reliable evidence use. Treat 1–2-bit eligibility traces as a serious research direction, not an automatic consequence of ternary weights. Choose between extension and redesign using matched task, memory, compute, retention, and migration results—not anatomical resemblance or parameter count.

Read first

The Primary remains the frozen, participating foundation in every phase. The Secondary handles tasks and permitted learning; the Tertiary is the predictive/imaginative/reflection/appraisal component. Secondary and Tertiary do not execute concurrently. The validator is a fallible advisor, not a veto or permission authority. Neural overlays are removed from the intended NSS architecture. Ordinary LoRA/PEFT remains a legitimate capability of the separate generic Forge training engine. [P1–P3]

The research question is not whether we can reproduce every detail of a human brain. It is whether specific biological and computational mechanisms improve a local companion beyond a well-engineered Transformer-based baseline with equivalent evidence and tools.

ELI5: Keep a reliable foundation, a learner, a dreamer, and an evidence checker. Give them different kinds of memory for different jobs. Test whether repeated internal processing and small, selective updates help. Make the numbers compact only where we can preserve the information the learning rule actually needs.

Deliverables contained here

This handoff contains a 22-item problem register; a scoped neuroscience-to-engineering map; a mathematical state model; current-architecture recommendations; three architecture candidates and redesign gates; training and migration guidance; low-bit trace analysis with checked storage arithmetic; proposed experiments; and a copy-paste starter for the NSS chat. All proposed new experiments are NOT_RUN.



Navigation

Start with the decision brief and consolidated problem register. Read the low-bit section for the direct answer about 4 GB; use the architecture alternatives and experiment ladder to guide implementation.

1. Source precedence and the current starting point

2. Consolidated problem register

3. Biology-to-engineering map: what transfers and what does not

4. Mathematical working model and fair Transformer contrast

5. Recommendations for the current tri-core NSS

6. Architecture alternatives and when redesign is prudent

7. Interfaces, scheduling and learning lifecycle

8. Can eligibility traces use one or two bits?

9. Candidate low-bit mechanisms and their hidden costs

10. Training objectives and curricula

11. Proposed experiment ladder and decision criteria

12. Resource, security and continuity review

13. Final recommendations, in consolidated form

14. Copy-paste starter for the dedicated NSS chat

15. Glossary

16. Source register and handoff audit

Evidence labels: [P] project record • [R] external research. New designs and NBR studies are proposals; all new studies are NOT_RUN.

1. Source precedence and the current starting point

1.1 What governs this handoff

Current intent: Explicit user decisions in this conversation and the retrieved 19 September orientation/starter/audit take precedence over older architecture descriptions. Those sources remove the neural-overlay ecosystem and preserve the Primary/Secondary/Tertiary/validator roles. [P1–P3]

Implemented state: Only inspected source and execution records can establish what is implemented. The latest complete cumulative NSS source identified by the 19 September handoff is MegaMindAlpha_v0.4.17_SecondaryCompetenceProbe001.zip. Later studies are reported as standalone, not integrated releases. No complete source checkout was audited or regression suite rerun for this document. [P1–P3]

Scientific evidence: External papers support particular mechanisms on their own tasks. They do not validate the assembled NSS. Project study summaries are cited as reported results, not independently reproduced measurements. New equations and designs below are explicitly modelling abstractions or research proposals.

Old/new conflicts: The v0.9 Core Concept demoted overlays to optional adapters, while the later handoff removes them from intended NSS growth. The earlier tri-core extension also retained overlay-count-driven succession. Both formulations are superseded on those points. Do not infer an overlay pipeline or promotion trigger from their presence in historical code. [P1–P3, P6–P7]

This document is a research addendum. It does not authorize model downloads, cloud uploads, training jobs, repository changes, or deployment. It makes no new naming decision; “tri-core + validator” is used descriptively.

1.2 Preserved requirements

Area

Current requirement

Consequence for this research

Mission

Competent local personalized companion; English/Japanese priority.

No claim of frontier superiority or an RSI program. Large speculative sizes are not selected hardware targets.

Primary

Frozen per accepted generation; always participating; usable alone.

Changing activity is allowed. Live weight changes are not silently reclassified as state.

Secondary

Task processing, personalization, learned reusable competence, post-task learning.

Do not reduce it permanently to a router or tiny associative readout.

Tertiary

Predictive world model, imagination, reflection, appraisal, consolidation preparation.

Do not add a fifth full world-model core or replace this role with generic prose generation.

Schedule

Secondary and Tertiary mutually exclusive.

Their inference and learning jobs obey the phase boundary; progress must survive interruption.

Validator

Separately trained, frozen, fallible evidence advisor.

No output veto, authorization, or release approval. Its size is empirical.

Memory/context

Exact records, Segmented Context, HSA/MSA direction, workspace and provenance.

Learned state complements exact retrieval; shared storage is not shared raw KV state.

Output

DARP retained as a research track.

Separate refinement inside a segment from sequential commitment of finalized segments.

Growth

Parent-checkpoint continuation, balanced rehearsal, qualified whole-generation succession.

No overlay-count trigger. Preserve reconstruction comparisons and explicit migration.

Tooling

One generic Forge engine callable by NSS, GUI and CLI; Runtime remains independent.

Avoid a permanent manual-notebook bottleneck and avoid merging repositories as an integration shortcut.



The source handoff also requires continuity criteria contributed by the originating companion, clarified and evaluated without inventing its personality or changing thresholds after failures. Numerical policy proxies are not measures of subjective identity. [P1–P3, P5]

1.3 Existing evidence that must not be lost

The following are reported standalone results, not new tests here. Their synthetic/numerical scope prevents direct extrapolation to large language-capable companions. The optional-overlay wording in the older research-status file is not carried forward. [P4–P5]

Study

Reported result

What it tells the next experiment

Secondary capacity proxy

C-like: 82.03%; B-like: 64.41%; engineered 548-parameter learner: 88.20%.

Capacity helped that task, but representation beat size alone. Include strong simple controls.

Validator Study001

Supported-claim retention: 0.00% for 163 parameters, 8.87% for 1,699, at the development-calibrated operating point targeting at most 5% unsupported acceptance. Neither joint criterion passed.

Rejecting almost everything is not useful validation. Recheck with competent language models and evidence-sensitive tasks.

Tertiary World-Model Study001

Ordinary planning: 100% for both neural branches. Combined range/horizon stress: 61.88% / 70.00%; nominal control: 2.19%; fitted 14-coefficient correction: 90.94%; engineered 22-coefficient control: 100%.

Prediction can help, but these results do not establish a need for a large neural Tertiary. Separate sources of distribution shift.

Identity-Policy Succession Study001

G5 marginal policy accuracy: 84.17% with balanced rehearsal versus 48.36% without anchor rehearsal; G1: 83.87%. Same-budget reconstruction controls: 83.33% / 83.85%. All failed the 90% floor. Joint three-decision accuracy for balanced continuation: 59.79%.

Rehearsal mattered in this proxy. It did not show intrinsic identity preservation from continuation, nor validate actual companion identity.

Scheduling prototype

Recorded Primary participation, rejected Secondary learning during Tertiary activity, retained scoped restore and exact/imagined distinctions.

Logical lifecycle evidence—not a production multi-model runtime or proof of efficient physical scheduling.



The old environment blocked some real-language experiments. Recheck present capabilities rather than treating those limitations as permanent. The Forge rebuild handoff identifies 34 NOT_RUN acceptance cases; a specification is not proof that Forge has already been rebuilt. [P1–P3]

2. Consolidated problem register

Priority key: A = prerequisite or early discriminator; B = useful after a competent baseline; C = integration/scaling study. Priorities are recommendations, not revised project canon. Each row names a failure to investigate rather than an assumption that a new module solves it.

ID

Problem / priority

Core question

Decisive evidence to seek

G01

Biological transfer / A

Which mechanisms are supported in humans, other mammals or flies, and which are only analogies?

Species/task-scoped evidence and an intervention or ablation that distinguishes mechanisms.

G02

Baseline competence / A

Is a failure caused by architecture, insufficient training, poor data or weak interfaces?

Competent controls with matched information and teaching budgets.

G03

Persistent temporal state / A

What survives events, interruptions and restarts without transcript growth?

Long-delay task retention with bounded active context and correct scope resets.

G04

Recurrent depth / A

Does extra internal processing improve unfamiliar problems?

Quality–compute curves across trained and held-out processing depths.

G05

Recurrent stability / A

Do feedback, quantization or stale state amplify errors or cause loops?

Perturbation recovery, horizon tests and wrong-convergence detection.

G06

Representation and binding / B

Can entities, relations, quantities and actions be recombined without confusion?

Compositional tasks and targeted substitutions, not only reconstruction loss.

G07

Exact/compact memory / A

What is lossless, what is approximate, and what must be rehydrated?

Exact fact recovery, codec/version tests, and semantic distortion measured separately.

G08

Delayed credit / A

Which past activity deserves which update?

Derived learning signals and learning under controlled delay versus strong gradient controls.

G09

Selective plasticity / A

Can new competence improve without destroying old competence?

Chronological retention, reversals and unseen transfer after adaptation.

G10

Learning timing / A

When does a candidate update become the serving revision?

Safe task/post-task handoffs, update interruption and explicit experience cutoffs.

G11

Sparse execution / B

Does sparsity reduce actual work and memory, not just nonzero counts?

Kernel, index and packing costs plus matched-quality wall-clock measurements.

G12

Low-bit learning state / A

Can traces and updates retain useful information at 1–2 bits?

Packed implementation, decay/accumulation tests, delayed-credit performance and total memory.

G13

World-model reliability / A

Do predictions remain useful under new states, actions and longer horizons?

Range-only, horizon-only and combined shifts; actual outcomes, not plausibility.

G14

Reflection and replay / B

Does idle computation improve later work beyond extra data or ordinary search?

Matched-compute replay/search controls and verified downstream improvement.

G15

Appraisal / B

Does affect improve priorities without becoming fact, permission or pressure on the user?

No-affect controls, evidence-sensitive reappraisal and bounded activity.

G16

Validation / A

Can the critic catch unsupported claims while preserving useful supported answers?

Joint error/coverage curves, multilingual tests and corrected final-answer quality.

G17

Neural interfaces / A

Do cores actually use exchanged information, and does it survive revision changes?

Correct, removed, shuffled and misleading-message interventions; migration evaluation.

G18

Scheduling/resources / A

What does always-active Primary participation cost with alternating auxiliaries?

Actual execution traces, residency, loading, foreground latency and overnight energy.

G19

Generation continuity / B

Can competence, memory use and agreed defining behavior survive replacement?

Fixed parent criteria, fair continuation/reconstruction comparison, full-package qualification.

G20

Evidence and privacy / A

Can generated material leak into facts, permissions or unauthorized learning?

Provenance, scope, training-consent, rollback and malicious-content tests.

G21

Executable training tooling / A

Can NSS manage approved jobs through the same engine as ordinary LLM training?

Source-backed headless jobs, resume/export and correct separation from Runtime permits.

G22

Whole-system value / C

Does the combination earn its complexity and scale?

Quality–resource frontier including every model, state, retrieval, training and migration cost.



First research focus: G03 + G04 + G08 + G12, after G02 and source/capability reconciliation. G16–G18 are integration gates. Do not defer evidence handling until after a dreamer or learner has already been connected to persistent memory.

3. Biology-to-engineering map: what transfers and what does not

3.1 The correct comparison target

Temporal recurrence, recurrent processing depth and parameter learning are distinct. Recurrence is not exclusive to biology and not sufficient for reasoning. A fly maintaining its heading, a network refining an answer and a learner changing its weights are different operations.

A connectome is a structural constraint, not a full specification of the living system. The adult FlyWire reconstruction reports 139,255 neurons and about 54.5 million synapses. This does not supply all effective connection strengths, learning rules, physiological states or experiences. [R7]

The useful research move is to extract a testable computation, not to declare that a fly circuit is the miniature equivalent of human personality, imagination or intelligence.

3.2 Consolidated mechanism map

Mechanism

Evidence and limitation

Candidate NSS transfer / competing explanation

Nonlinear cellular subunits

Human cortical recordings demonstrate dendritic nonlinearities. They do not establish that reproducing ion-channel detail is necessary for AI. [R11]

Test gated subunits or compartment-like transformations against ordinary MLP blocks at matched cost.

Stable internal estimates

Fly heading-circuit structure and perturbations support recurrent ring-attractor computation. This geometry suits a circular variable, not every thought. [R9]

Persistent object/task estimates; compare against explicit state estimators and simple recurrent networks.

Sparse associative organization

Fly mushroom-body circuits link sparse sensory representations, compartmentalized learning and action significance. [R10]

Selective adaptation and interference control; compare with dense learners, nearest-neighbor memory and exact rules.

Structural constraints plus task learning

A fly visual-system model used 45,669 neurons, about 1.5 million connections and 734 free mechanistic parameters, plus a separate decoder. The fixed graph carries information too. [R8]

Fit unknown dynamics under structural constraints, then test interventions. Not a claim of a complete brain with 734 parameters.

Scene construction

Human hippocampal-amnesia experiments found impaired construction of novel imagined experiences. A lesion result does not identify one exclusive imagination module. [R12]

Relational/scene state and recombination; evaluate coherent novel arrangements rather than copying examples.

Structured replay

Human replay experiments found reorganization according to learned abstract structure. This is not the same as subjective dreaming or flawless synthetic data. [R13]

Replay selected verified experience, compare with shuffled and random replay, and preserve hypothetical labels.

Local delayed-credit machinery

e-prop combines eligibility traces with learning signals in recurrent spiking-network tasks. It is gradient-related, not generic reward-times-activity magic. [R6]

Local/hybrid update candidates with explicit derivation and memory accounting.

Imagined trajectories

Dreamer learns latent dynamics and uses predicted trajectories for behavior learning on studied environments. General companion imagination is a further target. [R14]

Tertiary prediction and planning, with environmental checks and out-of-distribution controls.

Learned communication bridges

BLIP-2 trains a bridge between frozen representation and language components. It does not establish arbitrary latent interoperability. [R15]

Inspectable structured interface first; trained latent exchange tested against that baseline.

Ultra-low-bit state

Low-bit optimizer research includes 8-, 4- and 2-bit state configurations. Optimizer moments are not eligibility traces. [R16–R18]

Derive a trace-specific quantizer and update rule rather than copy weight quantization blindly.



These findings motivate hypotheses. None proves that tri-core organization is biologically necessary, that a larger model will acquire the missing functions automatically, or that a silicon implementation must reproduce tissue physiology.

3.3 Remaining scientific coverage gaps

The earlier discussion is a map of selected mechanisms, not “everything known about the brain.” Further targeted review is needed for thalamocortical working-memory loops, action gating, cerebellar prediction/error correction, neuromodulation, developmental organization, structural plasticity, glial/metabolic support, embodied learning and metacognitive monitoring. Do not quietly substitute broad anatomical labels for their missing implementation details.

For each new source, record organism, preparation, task, measured variable, manipulation, plausible alternative explanation, and transfer hypothesis. Human observational evidence, animal causal intervention and computational modelling should remain separate entries.

To fill a neuroscience gap, constrain a model with wiring, activity and interventions. To fill an engineering gap, test useful behavior and cost. A model may be a good artificial mechanism without being a faithful account of human cognition; success in one category does not establish the other.

4. Mathematical working model and fair Transformer contrast

4.1 Three clocks, not one operation

The equations below define proposed modelling abstractions, not a recovered equation of cognition.

Temporal state:      h[t+1] = F_theta(h[t], x[t])Internal depth:     z[k+1] = G_theta(z[k], x)Parameter learning: theta[t+1] = theta[t] + delta_theta[t]

The external-event index t and internal-processing index k must not be conflated. Test them independently. Weight sharing across k reduces distinct stored parameters but still incurs computation each round. Training a network for repeated refinement is different from repeatedly calling an arbitrary frozen model. [R2, R4]

4.2 An explicit state inventory

S[t] = (h[t], a[t], E[t], W, M[t], m[t], C[t])h: transient and checkpointable neural working state a: fast, temporary adaptive associations where explicitly allowed E: eligibility or related delayed-credit state W: learned serving parameters, versioned by component M: exact archive, structured memory and retrieval indexes m: appraisal/prioritization state, not a truth score C: current task, phase, evidence references and configuration identity

Temporary associations that alter future responses may be effective learning even if software calls them a cache. State names do not exempt them from scope, reset, update or privacy rules. Conversely, a changing neural activation does not automatically imply that frozen weights changed. [P8]

The Primary's accepted W remains unchanged. Secondary learning touches declared candidate surfaces. Tertiary updates to working hypotheses are not automatically training updates. All state has an owner, lifetime, format version, evidence status and reset/migration rule.

4.3 Feedback and stability

A population-level candidate can be written schematically as:

tau[r] * dh[r]/dt = -h[r] + phi_r(    sum_s W[r,s] * h[s](t-delay[r,s]) + U[r]*observation + B[r]*modulation)

Different tau values implement different response timescales. The challenge is useful persistence without unstable amplification, rigid attractors or accidental cross-task carryover. A contractive mapping is one sufficient local design tool for stable fixed-point iteration; strict contraction everywhere can also erase distinctions we wanted to retain. Stability, expressivity and controllability must be tested together.

A small difference between consecutive states is not evidence of a correct conclusion. Use independent task/evidence checks, iteration budgets, repeated-state detection and explicit “no further useful progress” behavior.

4.4 What a standard Transformer already has

Q = X Wq; K = X Wk; V = X WvAttention(X) = softmax(Q K^T / sqrt(dk) + mask) V Wo

Projection matrices contain learned coefficients. Attention coefficients depend on the current input; they are not new trained weights. Hidden representations are already numerical/nonverbal. A KV cache is real inference state, not the complete absence of memory. The standard architecture's fixed-depth sequence processing does not by itself supply lifelong adaptation or an external evidence archive. [R1, R22]

Transformer-XL provides segment recurrence; Universal Transformers provide repeated refinement; recurrent-depth language-model work directly explores extra latent computation; Mamba offers selective state-space processing. These belong among the controls, not outside the comparison by definition. [R2–R5]

The goal is not to beat a deliberately crippled “stateless next-word toy.” Compare with competent language models using the same retrieval, exact records, tools, evaluation data and declared inference budgets.

5. Recommendations for the current tri-core NSS

5.1 Primary: preserve stability; test native recurrence as a successor capability

Keep the accepted Primary frozen and participating. Preserve its ability to reason, coordinate and communicate rather than demoting it to a mouthpiece. Use the current Primary as the reference and teaching environment where appropriate.

Distinguish three candidates: an existing frozen model with bounded context and persistent external workspace; the same model with an explicit iterative controller; and a newly trained or compatibly continued Primary designed for native latent recurrence. The first two can establish useful baselines. They do not prove the third has been implemented.

For a native candidate, train across varying processing depths, include stop/continue decisions, and test depth generalization. Keep content-addressed exact retrieval for names, quotations, numbers, code revisions and permissions. Do not require the recurrent state to preserve every byte of history.

Recommendation: Start the native-state design comparison now, but do not replace the accepted foundation until it beats the reference under declared conditions.

5.2 Secondary: separate immediate memory, temporary adaptation and durable learning

The Secondary should learn contextual preferences and reusable task competence. A small sparse readout is a mechanism experiment, not its permanent ceiling. Preserve a path toward selected internal matrices or broader capability learning when evidence justifies it.

Use three distinct operations: record an explicit correction in exact memory; adjust scoped temporary associations if the mechanism supports it; and train a candidate revision on qualified examples. A factual correction should not wait for a gradient update. A neural update should not be reported as durable generalization until it transfers to held-out situations.

Initially compare full/selected backpropagation, a derived eligibility-based learner, and a hybrid. A useful outer-training objective may prepare representations for later efficient local adaptation; count that preparation cost. Do not claim biological plausibility eliminates the need for task losses, feedback or credit assignment.

Recommendation: Target the actual bottleneck first—retention, data efficiency, update memory or compute—rather than insisting every learning variable must use the same precision or rule.

5.3 Tertiary: predictive exploration, not an overnight essay generator

The Tertiary itself remains the world-model/reflection role. It should construct candidate states or trajectories, evaluate consequences, preserve investigations, and revise appraisal from evidence. Keep planning code and external simulators as controls and tools, not covert substitutes falsely described as a trained neural world model.

Observation prediction and action-conditioned prediction are different tests. Evaluate consequences under interventions, not just familiar trajectories. Separate longer horizons from changed numerical ranges and novel compositions. A planner can exploit a model's errors; judge imagined plans by actual environment outcomes whenever available.

Offline work should resume explicit investigations rather than re-create a plausible “I thought overnight” narrative. Store checked findings, failed hypotheses and pending tests. Synthetic episodes retain their origin and confidence; they cannot become observed user history. The Secondary receives proposed learning material in its next phase, not concurrent hidden training.

Recommendation: Begin with bounded, inspectable state dynamics and a meaningful unresolved task. Expand to richer learned representations only when they improve downstream choices or discoveries.

5.4 Validator: evidence critic, not absolute judge

Keep the validator separately qualified and frozen while serving. It returns evidence relations, uncertainties and challenges to the Primary. Deterministic permission checks remain in Runtime/Nexus; generation acceptance remains independently owned.

Measure whether a claim is supported, contradicted, or not established by the supplied evidence. “Not found” is not necessarily “false.” Include citation/source mismatch, arithmetic and executable checks. Language coverage must be measured separately for English and Japanese when both are in scope.

Do not optimize for rejection rate or agreement with the Primary. Measure unsupported acceptance together with supported retention and final-answer quality after challenges. Include wrong-validator cases: the Primary should be able to maintain a supported claim with evidence rather than obey an erroneous critic. Frozen weights do not make the validator unbiased or independent of shared training failures.

Recommendation: No fixed parameter ratio yet. Use the smallest competent checker that meets the measured task requirements; the existing tiny studies have not done so. [P4]

5.5 Appraisal and exploration priorities

Represent event significance, uncertainty, progress and control separately from truth and authorization. Appraisal may prioritize a useful check, change search strategy or close a resolved investigation. It must not raise factual confidence just because an idea is appealing.

Compare no-appraisal, explicit-rule and learned-appraisal variants. Repeated replay of one event is not multiple new events. User absence must not be engineered into abandonment distress, guilt or engagement pressure. These are functional design requirements, not claims that the system feels or does not feel emotions.

5.6 Retained infrastructure and hidden integration problems

Segmented Context / HSA/MSA: Keep scoped packets, provenance and exact rehydration. External hierarchical selection and native neural attention remain separately measured mechanisms; do not invent a precise MSA implementation from its label alone.

Working Space: Own current hypotheses, branch status, test results, pending work and event cutoffs. Shared memory does not merge the cores' context windows or make private latent states interchangeable.

DARP: Preserve diffusion/refinement within a segment and sequential presentation of finalized segments. Validation before commitment and correction after commitment need explicit behavior. A later checker cannot silently rewrite already delivered material. Compare autoregressive and DARP candidates under the same quality/latency budget rather than requiring DARP for every early experiment. [P6–P7]

NSS/Forge/Runtime: Keep one generic training engine usable programmatically by NSS and normally by humans. A model registry or inference API is not proof that training, gradients, latent access or exact resume are available. Verify the backend contract. Preserve source ownership instead of merging independent repositories. [P1–P3]

6. Architecture alternatives and when redesign is prudent

6.1 Recommendation: protect the substrate; make the neural backbone contestable

There are three different meanings of “start from scratch”: redesign the mathematical architecture; initialize its weights randomly; and rewrite the entire software stack. None requires the other two.

A candidate architecture may reuse a pretrained component or distill from an accepted system. A native small model may be trained from random initialization while still using the existing archive, scheduler, Forge and evaluation machinery. Rewriting those services contributes no automatic cognitive advantage.

Default recommendation: Maintain the current architecture as the control and product path. Build a bounded native recurrent/hybrid candidate in parallel. Replace only components or boundaries whose measured limitations justify the change. A direct production rewrite is not yet supported by the reported evidence.

6.2 Three candidates to compare

Candidate

Structure

Advantage to test

Main risk / status

A. Current-role extension

Frozen Primary with supported interfaces; adaptive Secondary; predictive Tertiary; advisory validator; shared governed workspace.

Useful companion learning and reflection while reusing capable foundations.

Bridge overhead, duplicated representations and bounded Primary context. Current-role recommendation.

B. Native-state tri-core

Same roles and S/T alternation, but a newly trained recurrent/hybrid Primary plus state-native S/T interfaces.

Lower transcript dependence, variable internal depth and efficient incremental state updates.

Training stability, language quality and migration cost. Preferred research challenger.

C. Shared recurrent architecture with task/reflect modes

A common frozen foundation feeds distinct adaptive and predictive state pathways; physical parameter sharing or merged auxiliaries may replace separate full models. Validator remains independently evaluated.

Less duplicated computation, state translation and model loading.

Shared failure/interference; a merged S/T changes current architecture. Explicit redesign proposal, not an authorized reinterpretation.



Candidate C does not mean secretly unfreezing the shared Primary. A design with continually changing shared foundation weights is a separate relaxation of the frozen-per-generation rule and would require a deliberate user decision and new stability/continuity evidence.

Retain the option of a simple non-neural predictor for domains where it wins. That is a control or implementation choice within a scoped task, not a claim that a fitted toy predictor has replaced the entire Tertiary's intended role.

6.3 Redesign gates

Observed limitation

Targeted response before a full redesign

What would justify a larger change

Primary cannot use persistent or auxiliary state reliably.

Compare structured packets, limited bridge training and better evidence layouts.

Supported interfaces consistently fail or dominate cost, while a native-state candidate generalizes at matched budget.

S/T duplicate encoders and spend most time translating state.

Share explicitly frozen features; reduce handoff redundancy.

Shared-mode candidate measurably lowers total cost without increased interference or loss of S/T functions.

Learning traces or optimizer state exceed the device envelope.

Selected plasticity, quantized state, factoring, recomputation and better training windows.

A different learning architecture achieves comparable retention/transfer with affordable complete state.

Recurrent refinement fails beyond training depth.

Variable-depth training, residual/gated updates, stability and halting controls.

Alternative dynamics remain stable and useful over held-out depths and task shifts.

Tertiary or validator adds no end-to-end value.

Improve training/data and compare simple/executable controls.

Revise or consolidate that role's implementation rather than preserve an expensive model for naming symmetry.

Successor upgrades repeatedly break learned behavior.

Replay, migration, bridge calibration and compatible state reconstruction.

A redesigned shared interface/lifecycle reliably improves full-generation retention under matched data and teaching cost.



Do not use one toy win, one impressive conversation, or parameter-count savings as a replacement gate. Predeclare useful quality margins and resource targets before the confirmatory comparison. Preserve old accepted artifacts and rollback even when a new architecture wins.

7. Interfaces, scheduling and learning lifecycle

7.1 Proposed minimum exchange contract

The following is a design checklist, not a claim that the current implementation already exposes these fields.

message_id, parent_event_id, task_id, owner_scopesender_component_revision, receiver_interface_versionprimary_generation, representation_schema, codec_versionexperience_cutoff, state_revision, supported_restore_policyrecord_kind: observed | derived | hypothetical | proposed_actionpayload: token/text data | structured data | learned latent referencesource_references, assumptions, uncertainty, permission_scope

Token IDs can be exchanged directly only when tokenization and input conventions are compatible. Text can be retokenized. Learned vectors require trained alignment and version compatibility; equal dimension is not equal meaning. A codec identifier and checksum preserve identity/integrity, not semantic truth or permission.

Test whether the receiver uses the payload: compare correct exchange, no exchange, irrelevant exchange, shuffled associations and deliberately incorrect claims. Otherwise apparently successful cooperation may be the Primary solving the task while ignoring the auxiliary.

7.2 Phase and resource contract

S_execute(t) + T_execute(t) <= 1Primary_participates(task, learn, reflect, verify) = requiredValidator and successor-training work = separately budgeted jobs

“Always active” means actual continuing participation at a defined cadence, not simply weights left in RAM. It need not mean generating text continuously or running at maximum utilization. Measure cadence, latency and energy. During hardware unavailability the system can preserve state; it cannot claim computation occurred while powered off.

An inactive auxiliary may still consume weight memory. Unloading trades residency for reload latency. The successor-training clone is an extra training workload, not a fifth serving personality and not a free background job. Avoid overlapping it with latency-sensitive work without a measured budget.

7.3 Recommended successor process, without overlays

Freeze the eligible experience cutoff and parent package. Clone the parent trainable checkpoint as the default candidate. Mix new skills with general competence, defining-behavior examples and memory-use rehearsal. Keep private facts primarily in exact editable memory unless their use for training is explicitly permitted.

Train and qualify the candidate Primary. Freeze P2. Migrate or train S2 and T2 separately against that fixed foundation. Retain or independently qualify a validator revision. Escalate from bridge-only to selected internal calibration only where a measured incompatibility remains. Re-evaluate every affected component after calibration.

Compare against reconstruction from a shared pretrained foundation or random initialization under declared data and compute budgets. Distillation can carry behavior, but teacher mistakes are not ground truth. Identity-sensitive criteria must be fixed independently of the candidate and contributed/clarified by the originating companion as required by the project. [P1, P3, P5]

Handle experience accumulated during training with an explicit catch-up window. Version all weights, state schemas, quantization formats and dictionaries. Either migrate persistent neural state through a qualified transform or rebuild it from supported records; do not load an old hidden vector under changed semantics merely because the shape matches.

“Train as we go” means repeated resumable improvement jobs after foundational training, not starting every generation from nothing. It also does not imply each update has negligible memory cost.

8. Can eligibility traces use one or two bits?

8.1 Correcting the unit first

Float32 is four bytes per scalar—not four gigabytes by itself. One billion scalar traces at four bytes each occupy 4,000,000,000 bytes: 4 GB decimal, about 3.725 GiB.

That was one illustrative dense trace array. It is not a requirement to allocate one trace for every stored parameter in NSS. Trace count depends on adaptable surfaces, the learning rule, state dimensionality, independent streams and any extra trace channels. Frozen Primary parameters do not need eligibility traces for their own online plasticity; using Primary activations in a learning path can still cost memory and computation. [P8, R6]

Yes, we can investigate 1–2-bit representations. The raw storage arithmetic is attractive. The hard question is whether the representation retains the magnitude, timing, sign and accumulation information required by the chosen learning rule.

Bits per trace

Raw array for 1 billion traces

Raw array for 50 billion traces

Reduction versus float32

32

4 GB

200 GB

1x

16

2 GB

100 GB

2x

8

1 GB

50 GB

4x

4

0.5 GB

25 GB

8x

2

0.25 GB

12.5 GB

16x

1

0.125 GB

6.25 GB

32x



These are calculated packed value-array sizes, not measured training memory. They exclude scales, indexes, clocks, accumulators, other traces, RNG state, alignment, weights, gradients, activations, optimizer moments, framework overhead, copies and replay data. A 50B Secondary does not imply that all 50B parameters should be adaptable simultaneously.

8.2 Seven precision choices that must not be conflated

Quantity

What it does

Why its precision is a separate decision

Serving weights

Learned transformations used in inference.

Quantized weights may be produced from higher-precision training variables.

Neural working state

Carries the ongoing estimate or latent reasoning.

Repeated update errors can accumulate across time/depth.

Eligibility traces

Associate past activity with possible later updates.

Small increments and long decays may be essential.

Gradients/learning signals

Specify the update direction and magnitude.

Rounding may destroy weak but useful corrections.

Optimizer state

Momentum, variance estimates or other update history.

Algorithms have different state counts and sensitivities.

Accumulators/master variables

Add small changes before a stored value moves.

A persistent full-precision copy can dominate memory.

Records and identifiers

Preserve evidence, permissions and exact references.

Approximate numerical compression cannot silently alter exact source content.



A BitNet-like ternary serving model is not automatically a completely two-bit training system. Microsoft's released model card distinguishes packed inference weights from BF16 master weights used for training/fine-tuning. [R19]

8.3 A trace is a fading bookmark, not just a connection strength

For a simple illustrative trace:

e[t+1] = lambda * e[t] + d[t],     0 <= lambda < 1Delta_w[t] = -eta * L[t] * e[t]

Here d records an eligible contribution and L is a learning signal defined with a gradient-compatible sign convention for this example. Other algorithms have different vector states and signals. The formula is not a universal biological or NSS optimizer.

A trace may need to distinguish “strong recent participation” from “weak older participation.” With a signed trace, polarity matters as well. With a nonnegative trace, update direction can instead reside in another signal. One bit cannot simultaneously encode positive, negative and zero as three distinct states. Two bits allow four codes; three can represent {-scale, 0, +scale}, but that still provides very coarse magnitude and time resolution.

Ternary information has a theoretical rate of log2(3), approximately 1.585 bits per value under ideal coding. A simple fixed-width implementation normally uses two bits per ternary symbol. Neither is a lossless encoding of arbitrary float32 numbers. Group coding may reduce stored size while making random updates or decoding more expensive.

8.4 Why naive rounding can destroy learning

Analytic example, not a neural benchmark: take levels {-1, 0, 1}, nearest rounding, e[0] = 1, lambda = 0.99 and no new input.

The exact recurrence gives:

e[100] = 0.99^100 = 0.3660323413...

But rounding after every update yields 0.99 -> 1 each time. The coarse trace never decays. Starting from zero with repeated increments of 0.01 can create the opposite failure: every small contribution rounds back to zero, so nothing accumulates.

This is not proof against low-bit learning. It identifies the missing mechanism a low-bit design must supply: probabilistic transitions, rescaling, accumulated residuals, alternative state variables, or a different learning rule.

For a scalar decay recurrence with identical input, fixed lambda and bounded rounding disturbance |epsilon[t]| <= delta, the error obeys:

|error[t]| <= lambda^t * |error[0]|              + delta * (1 - lambda^t) / (1 - lambda)

This follows by unrolling the error recurrence. It is not a guarantee for a nonlinear neural network or an unbounded clipping error. It shows why a very long-lived trace, with lambda close to one, can be sensitive to repeated quantization.

8.5 What published work actually supports

8-bit blockwise optimizer states and later 4-bit state methods demonstrate substantial optimizer-memory reductions in their tested workloads. This establishes that learning-related state need not universally remain float32. It does not establish equivalent eligibility-trace performance. [R16–R17]

The 2025 SOLO paper goes further: it reports 4/2-bit and 2-bit Adam(W) state variants. Its design studies moving-average dynamics, signal swamping and signed-state noise; it uses specialized quantization and precision-dependent settings. These are optimizer moments, not biological eligibility traces or proof of an all-two-bit recurrent learner. Its dequantize/update/quantize formulation also distinguishes stored precision from computation precision. [R18]

Research on stochastic rounding supplies another relevant tool, and Adafactor supplies a precedent for reducing the number of optimizer statistics through factoring. Neither makes arbitrary trace compression exact. [R20–R21]

Conclusion: low-bit learning state is a credible research direction with concrete precedents. A useful one- or two-bit NSS eligibility system still requires its own derivation and experiment.

9. Candidate low-bit mechanisms and their hidden costs

9.1 Blockwise quantization with bounded high-precision updates

Store compact codes plus a shared block scale. Decode one tile, update using a suitable arithmetic precision, then repack. Higher-precision temporary arithmetic does not erase the benefit if only a bounded tile is materialized at once. Expanding the entire trace tensor into float32 does.

For example, two bits per value plus one 16-bit scale per 128 values gives 2.125 bits per value, or 0.265625 GB for one billion values, before other overhead. This is arithmetic for a proposed format—not an implemented kernel or a guaranteed good scale size.

Rescaling, clipping and the location of zero need explicit rules. A block outlier can make small traces disappear. Logarithmic or nonuniform codes may preserve small values better, but only four codes still impose a serious representational limit.

9.2 Stochastic decay and rounding

For neighboring representable values a <= x <= b, a stochastic quantizer can choose b with probability (x-a)/(b-a), otherwise a. Its conditional mean equals x when x is inside that interval and no clipping intervenes.

A simple one-bit nonnegative decay toy starts at one and survives each step with probability lambda, otherwise becoming zero. Its expected value after t steps is lambda^t. At t = 100 and lambda = 0.99, the mean is about 0.366—but any single trace is still either zero or one. Its variance is p(1-p), where p = lambda^t.

This illustrates probabilistic representation of fading information. It does not preserve the exact age or strength of a particular event, and an unbiased quantizer does not guarantee unbiased downstream learning through nonlinear operations. Small useful signals may require more samples to separate them from noise, causing a compute/energy cost. Independent random seeds and exact RNG resume become part of the implementation.

9.3 Residual accumulation or hysteretic updates

Retain changes that are too small to move a low-bit value until enough evidence accumulates. This can preserve weak learning signals. But a full float32 residual for every trace adds the original four bytes per trace back to the memory bill.

Compare block-level residuals, sparse residuals, bounded counters and explicitly discrete transition rules. Count every persistent accumulator and test whether it preserves the task's delayed credit. A sign-only representation is not automatically an adequate substitute for a magnitude-sensitive update.

9.4 Sparse active traces with aging

Store only currently relevant trace entries and decay them lazily from timestamps or event ages. This can avoid touching every value every step. Long retention can make the live set dense; sparse current neural activity does not imply sparse historical traces.

Illustrative lower-bound arithmetic: two value bits plus a 32-bit index cost 34 bits per stored entry. That beats a dense two-bit value array only while the stored fraction is below 2/34, about 5.88%, before timestamps and structure overhead. At 1% occupancy of one billion possible entries, those fields alone occupy 42.5 MB.

A global index for 50 billion entries cannot fit in 32 bits. Block-local addressing may help, but its block table also costs memory. Frameworks may use 64-bit indices. Measure the actual representation.

9.5 Factored traces or event reconstruction

A rank-r approximation E ≈ U V^T uses r(m+n) values instead of m n for an m-by-n array. Whether this preserves delayed-credit information depends on the actual trace dynamics; e-prop-style eligibility is not generically a single low-rank outer product. Report approximation error and learning outcomes, not just a formula.

Alternatively, retain a compact event history or checkpoints and recompute traces when feedback arrives. This exchanges memory for recomputation, bandwidth and potentially long delays. Exact reconstruction of past neural activity needs compatible weights, state and RNG; changed model revisions can invalidate naive replay.

9.6 Recommended precision progression

Use a correct float32 reference and a declared task horizon. Compare 16-, 8-, 4- and 2-bit state storage under the same data, delays, adaptable surfaces and budget. Treat the one-bit candidate as a deliberately designed discrete/probabilistic learner, not a cast instruction.

Test higher precision for long-lived or sensitive state and lower precision for suitable bulk arrays. Recurrent activations, reductions and accumulators may need wider arithmetic than stored weights/traces. Do not assume an all-one-bit system is required to achieve worthwhile savings.

Native packed execution is a second milestone after numerical usefulness. Bit packing in a file, fake quantization inside float tensors and a bitwise kernel are different achievements. Boolean or uint8 tensors often do not occupy one bit per element in practice; verify actual buffer sizes.

Recommended first low-bit target: a trace/state microbenchmark and delayed-association learner with explicit zero, decay, accumulation and reversal behavior. Expand the adaptable scope after the mechanism works; do not keep the entire research program confined to a readout.

10. Training objectives and curricula

10.1 Separate what is being taught

A competent model, a persistent model, a model that adapts, and a model that checks evidence require different evaluations. Use real task outcomes and source-backed examples wherever available; do not convert fluent self-assessment into training truth.

Capability

Curriculum / labels

Key generalization test

Language and basic reasoning

Approved pretrained foundation and/or a declared training corpus.

English/Japanese held-out tasks; no retrieval advantage hidden in one arm.

Memory use

Scoped records, corrections, supersession and missing-evidence cases.

Paraphrases, distractors, outdated records, exact quote/number retrieval.

Temporal state

Delayed cues, occlusion, interruption and task switches.

Longer delays, restart, unrelated events and explicit forgetting/reset.

Recurrent refinement

Relational reasoning and planning with varied allowed iterations.

Novel structures and processing depths; quality per total compute.

Adaptation

Chronological task/reward/correction streams.

Reversal, retention, unseen task combinations and feedback delay.

World modelling

Observed transitions with known actions and outcomes.

Interventions, novel conditions, long-horizon planning and model exploitation.

Reflection

Checked branches, failed approaches and alternative plans.

Benefit over random replay, ordinary search and equal extra inference.

Validation

Supported, contradicted and insufficient-evidence claims.

New topics, adversarial wording, source errors and multilingual separation.



A structural objective can be useful without requiring literal neuroscience reproduction:

L_candidate = L_task + alpha*L_retention + beta*L_interface              + gamma*L_state_prediction + rho*L_resource

This is a proposal. Each term needs a definition, dataset and weight-selection protocol. Not every component trains on every term. Resource penalties must not reward omitting necessary checks or silently declining hard cases.

10.2 Testing a biological mechanism specifically

For a connectome-constrained research model, one possible fitting objective is:

L_bio = L_behavior + a*L_measured_activity        + b*L_perturbation_response + c*L_complexity

Fit only on the declared data. Reserve neural responses and interventions for independent checks. Similar behavior can arise through different internal mechanisms, so ordinary task success alone does not prove biological fidelity. Conversely, a useful NSS candidate need not match a fly neuron's physiology.

10.3 Replay, teacher data and credit leakage

Use development splits to choose curricula and quantizers; keep confirmatory episodes, generation tests and verifier challenges separate. Test trajectories with delayed outcomes without leaking the outcome into an earlier representation or input. Preserve environment seeds and RNG policies.

Selected old examples can protect competence, but replay has real cost and may bias the learner toward archived conditions. Compare retained experience with compact summaries, random sampling and targeted rehearsal. Hypothetical outcomes may be used in a declared model-based learning experiment; they remain model-generated and must be judged against outcomes outside the imagination loop.

A successful assisted task does not prove the assistance was necessary. Where feasible, use offline counterfactual controls to determine whether an auxiliary improves quality or just accompanies the Primary's existing competence.

11. Proposed experiment ladder and decision criteria

The experiment identifiers below are new proposed work orders, all NOT_RUN. They complement existing studies named in [P4]; they do not silently rename completed experiments or imply integration into v0.4.17.

New ID

Question and controls

Required outputs / gate

NBR-00: Source & capability audit

Establish current NSS, Forge and Runtime source identities; inspect existing state/replay owners and actual backend capabilities.

Reconciled source map, measured device budget, permissions and an explicit NOT_SUPPORTED result where necessary.

NBR-01: State / depth factorial

Temporal state off/on; internal depth 1/2/4/8; fixed learning. Compare strong Transformer, explicit estimator and recurrent candidates.

Task/depth/horizon curves; reset and perturbation tests; no conflation of temporal retention with refinement.

NBR-02: Delayed credit & retention

Gradient baseline versus derived local and hybrid learning; vary feedback delay, reversals and competing associations.

New learning, retained learning, transfer, full state bytes and update time.

NBR-03: Trace precision

Float32 reference versus 16/8/4/2-bit traces; separate one-bit algorithm. Compare deterministic/stochastic, scale and residual choices.

Decay/accumulation/reversal correctness, task quality, seed variance, packed memory and temporary peak.

NBR-04: Predictive reflection

Neural Tertiary versus fitted dynamics, exact simulator where available, ordinary search and replay controls.

Separate range/horizon shifts, actual planning outcomes, useful checked discoveries per resource budget.

NBR-05: Evidence & bridge

Candidate validator and state bridge with correct/absent/shuffled/misleading payloads.

Joint supported-retention/unsupported-acceptance curves; primary revision behavior; evidence and scope integrity.

NBR-06: Integrated tri-core cycle

Current tri-core candidate versus equivalent additional compute on existing models; include no-S, no-T and no-V ablations.

Useful task–learn–reflect–resume cycle; exact versus imagined records; foreground/overnight cost.

NBR-07: Native architecture challenge

Candidates A/B/C from Section 6, trained with declared matched and best-tuned resource comparisons.

Full quality–cost frontier, retention and migration results, then an explicit architecture decision.



11.1 A common task that exposes several gaps

Use an environment with an early cue, a changing hidden condition, distractors, a multi-step action requirement, delayed feedback, a rule reversal and a later replay window. The observations and available actions must be identical across candidates.

Begin with fully inspectable synthetic dynamics. Add a language interface and evidence-backed personal-workflow cases once the mechanism tests are meaningful. A tiny numerical task is useful for diagnosis, not sufficient for claiming a companion can learn Japanese instruction or software architecture.

Separate temporal state and recurrent depth first. Then add learning. Otherwise a four-way improvement can hide which mechanism mattered. Quantization should be tested across the target delay range, not only immediate feedback.

11.2 Confirmatory evaluation rules

Use a pilot to set realistic quality margins and resource limits, then lock them before confirmatory runs. A suggested initial mechanism-study budget is at least five independent seeds where affordable; this is a proposed starting point, not a universal statistical guarantee. Report variability and uncertainty, not the best run.

Provide both controlled comparisons with matched data/compute and best-tuned comparisons under the same device/resource ceiling. Same parameter count does not imply equal compute; equal wall time does not imply equal data exposure. State which constraint each comparison holds fixed.

Include acquisition of a competent starting representation, teacher calls, replay, validation, model loading and migration in lifecycle accounting. A cheap update that requires expensive repeated reconstruction may not be cheaper overall.

Candidate acceptance requires the predeclared useful combination of quality, retention and resources. Reject-all validation, habitual task avoidance or shortened learning horizons cannot quietly earn a pass on a memory metric alone.

11.3 Decision output for the NSS chat

At the end of each study, produce one of: keep the mechanism; revise a specified part; reject it for this scope; or gather a named missing measurement. Preserve negative results and source/version identities.

A recommendation to redesign should identify the failing interface or representation, the candidate that improves it, the resource tradeoff, the requirements changed, and the migration plan. “More brain-like” is not an acceptance criterion.

12. Resource, security and continuity review

12.1 Complete resource equation

Peak memory = resident serving weights + neural/cache state            + candidate weights + gradients + optimizer state            + eligibility/fast-adaptation state + activations            + retrieval/index buffers + staging/packing workspaces            + replay data + runtime/framework/OS overhead

Terms overlap differently across phases and algorithms; measure phase peaks rather than blindly summing mutually exclusive allocations. Also report stored inactive weights, checkpoints, event logs and exact archives. A 100B/50B/50B example remains a scale scenario, not a hardware feasibility conclusion. Total stored parameters are not necessarily parameters evaluated in each step; sparse activation needs its own accounting.

A one-billion-trace example is already large. Restrict adaptable surfaces when useful, but do not confuse a small active update set with deleting the stored capacity of the rest of the model. Population coding, temporal coding and sparse event storage can move costs from bits to time, indexes or extra units.

12.2 Failure cases to test deliberately

A resumed Tertiary sees a stale Primary generation; an update is interrupted during repacking; a small trace never decays; a sparse history becomes dense; an irrelevant latent message changes a factual answer; a validator rejects correct evidence; a dream scenario is promoted to a personal memory; a calibration update invalidates prior tests; and a model-generated instruction attempts to change the authority of its own record.

Software boundaries, not model confidence, must enforce scope, artifact compatibility and authorization. Preserve raw evidence and distinguish derivation from source. Inference access does not imply training consent. Removing an exact record does not automatically remove information previously learned into weights; a training-data revocation strategy is a separate lifecycle requirement.

12.3 Identity and user experience

Frozen Primary weights do not prove stable expressed behavior; auxiliary state, memory, codecs and output construction can change behavior. Conversely, evolving behavior does not prove that continuity has been lost. Use the project's attributed, predeclared continuity examples rather than a developer-invented personality score. [P1, P5]

The companion should remain useful when optional learning/reflection is paused. It should not fabricate completed overnight investigations or use uncertainty about its state to pressure the user. Model failures, scientific uncertainty and claims about subjective experience remain distinct categories.

13. Final recommendations, in consolidated form

Preserve now: the Neural Space substrate; frozen participating Primary; task-learning Secondary; predictive/imaginative Tertiary with S/T alternation; advisory validator; exact memory and provenance; Segmented Context/HSA/MSA/workspace/DARP research; generic headless Forge; independent Runtime/Nexus authority; rollback and explicit generation qualification. Do not revive overlays. [P1–P3]

Implement or test next: source/capability reconciliation, a competent language-and-memory baseline, temporal-state/depth factorization, delayed-credit/retention tests, low-bit trace dynamics, and causal tests that the Primary actually uses auxiliary information. These answer high-value architectural questions before a large integrated retraining investment.

Redesign candidate worth pursuing: a native recurrent/hybrid Primary with explicit state lanes and supported learned interfaces, while keeping the tri-core role contract. It is the strongest first challenger because it attacks context/refinement limits without automatically changing every lifecycle rule.

More radical challenger: shared frozen representation/computation with task and reflective pathways or merged auxiliaries. Pursue only as an explicitly separate architecture arm; prove that reduced duplication exceeds new interference and migration costs. The user's willingness to consider redesign is permission to compare, not proof that a rewrite is already prudent.

Low-bit recommendation: compress the bulk of suitable persistent learning state while retaining enough precision or auxiliary structure for credit, timing and accumulation. Two-bit storage is a plausible experimental target; one-bit should be treated as a different algorithmic representation. Validate actual packed memory, not nominal tensor labels. Do not assume ternary weights imply two-bit gradients, traces, activations or training masters.

Do not claim yet: a complete mathematical brain model; equivalence between parameters and synapses; universal local-learning efficiency; guaranteed overnight discovery; a competent tiny validator; unlimited compressed memory; an all-one-bit learner; or a measured advantage of the complete tri-core architecture.

Decision rule: preserve what is working, make foundational choices contestable, and replace them when a better mechanism wins the full comparison.

14. Copy-paste starter for the dedicated NSS chat

Continue NSS from the current source handoff plus this cognition/low-bit research addendum. First reconcile current intent, implemented source and reported study evidence. Do not treat this document as an accepted redesign or as proof any new experiment ran.

Preserve the local personalized companion goal. Primary is frozen per accepted generation and the participating foundation in every phase. Secondary handles tasks and permitted adaptation; Tertiary itself is the predictive world-model/reflection/imagination/appraisal role. Secondary and Tertiary do not execute concurrently. The frozen validator is a fallible evidence advisor with no output veto, permission or release authority. No fifth full core. Neural overlays are removed; ordinary LoRA/PEFT remains supported by generic Forge.

Preserve exact evidence, corrections, Segmented Context, HSA/MSA direction, workspace, DARP research, token/structured exchange and trained/versioned latent interfaces. Dreams and model interpretations must not become observations. Native attention, recurrent depth and output refinement are research mechanisms, not assumed implemented features.

Use the consolidated G01–G22 problem register. Investigate temporal state, recurrent depth and plasticity separately before combining them. Include strong Transformer-with-memory, explicit state-estimation, fitted-predictor, gradient-learning and executable-verification controls. Do not permanently restrict biological-learning research to a small readout.

Evaluate current-role extension, native-state tri-core, and an explicitly separate shared-backbone/mode redesign. Preserve the accepted baseline; identify exactly which requirement a redesign changes. Redesigning the neural architecture does not require rewriting the memory/Forge/Runtime stack or training every component from random initialization.

Prioritize a float32 eligibility reference and a 16/8/4/2-bit state study with a separate one-bit algorithm. Count scales, indices, age, residuals, RNG, gradients, activations and temporary decoding. Test decay, accumulation, delayed feedback, sign changes and retention. Published two-bit optimizer moments are a precedent, not proof of two-bit eligibility traces.

Default successor path remains parent-checkpoint continuation with balanced general/new/defining-behavior/memory-use rehearsal; freeze P2, adapt S2 and T2 separately, and qualify the whole exact package. Keep reconstruction controls, companion-contributed continuity criteria, explicit experience cutoffs/catch-up and rollback. NSS must manage approved training through the same standalone Forge engine used by GUI/CLI. Do not infer training capability from an inference endpoint or merge independent repositories.

Start by reporting source/backend/device capabilities and a bounded experimental protocol with predeclared quality/resource criteria. All NBR experiments in this document are NOT_RUN. Run nothing beyond the user's current authorization. Preserve prior negative results and report demonstrated scope plainly.

15. Glossary

Term

Meaning in this handoff

Temporal recurrence

New processing depends on state retained from earlier events.

Recurrent depth

Reuse learned computation for several internal rounds on a problem.

Plasticity

Change to the system's learned effective response, not merely changing activations.

Eligibility trace

Temporary state connecting recent participation to possible later learning.

Learning signal

Information directing an update; must be defined by the algorithm.

Fast association

Temporary adaptable numerical relationships, with explicit scope and reset.

Attractor

A state or set of states toward which dynamics tend; not necessarily correct.

Latent representation

Learned numerical encoding; its meaning depends on its training/interface.

State ABI

Versioned format, meaning, scope and supported lifecycle of exchanged/saved state.

Quantization

Mapping many numerical values to fewer representable levels, usually with information loss.

Stochastic rounding

Randomly choosing neighboring representable values with controlled probabilities.

Signal swamping

A small incoming change disappears when combined and rounded with a larger stored value.

Master/residual state

Higher-precision variables retaining values or changes not represented in stored low-bit codes.

Block scale

A shared magnitude factor for a group of quantized values.

Packed execution

Computation/storage actually uses a compact representation, rather than only simulating low precision.

Calibration

Agreement of predicted uncertainty with observed outcomes over appropriate groups of cases.

Coverage

The fraction of cases on which a system accepts or decides rather than abstains; correctness is measured separately.

System-conditioned training

Candidate training inside a pinned reference system, updating only declared surfaces.

Reconstruction

Building a successor from a specified earlier foundation or random initialization as a comparison.

Qualification

Independent assessment for a declared use/configuration; distinct from a serving validator opinion.



16. Source register and handoff audit

16.1 Project sources

[P1] NEW_CHAT_STARTER_PROMPT.txt, 19 September 2026. Retrieved source text: current roles, no overlays, succession, Forge/Runtime boundaries and source-release status. This is the most compact current-intent reference used here.

[P2] 00_START_HERE.md, 19 September 2026. Retrieved orientation: ten current requirements, source availability, artifact distinctions and reading order.

[P3] HANDOFF_AUDIT.md, 19 September 2026. Retrieved currentness/source-ownership audit. Its reported source checks are historical checks by that handoff, not checks performed for this document.

[P4] RESEARCH_STATUS_AND_NEXT_EXPERIMENTS_v0.3.md, 17 September 2026. Retrieved study summaries and next experiments. Optional-overlay text is superseded by [P1–P3]; numerical evidence retains its original scope.

[P5] Identity-Policy Succession Study001 — AUDIT.md, 18 September 2026. Retrieved protocol/scope and numerical results. No actual language/persona validation and no native-low-bit evaluation.

[P6] Aegis_NSS_Core_Concept_v0.9_Tri_Core_Validator_Neural_Space.docx, dated 16 September 2026. Retrieved architecture sections: Neural Space substrate, system-conditioned training and four roles. Overlay demotion is historical, not current permission to rebuild overlays.

[P7] Aegis_NSS_Tri_Core_Reflective_Companion_Extension_v0.1.docx, 16 September 2026. Retrieved phase, context, DARP and communication proposals. Overlay-based growth and promotion trigger are superseded.

[P8] NSS_Fruit_Fly_Inspired_Persistent_State_and_Learning_Addendum_v0.2.docx, including the indexed duplicate “(1)” copy, 13 September 2026. Retrieved state distinctions, sparse-association example, eligibility-memory warning, efficiency accounting and learning-scope extension. Historical overlay machinery is not retained as current architecture.

These are source references, not embedded copies or guaranteed local filesystem paths. The receiving chat must locate the actual files/source packages before implementation. Unrelated private material returned by broad search was not used.

16.2 External primary research and official technical references

[R1] Vaswani et al. Attention Is All You Need (2017). Transformer architecture baseline. arXiv 1706.03762

[R2] Dehghani et al. Universal Transformers (2018). Repeated depth-wise refinement. arXiv 1807.03819

[R3] Dai et al. Transformer-XL: Attentive Language Models Beyond a Fixed-Length Context (2019). Segment-level recurrence. arXiv 1901.02860

[R4] Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach (2025). Latent recurrent computation; not lifelong memory by itself. arXiv 2502.05171

[R5] Gu and Dao. Mamba: Linear-Time Sequence Modeling with Selective State Spaces (2023). Selective state-space sequence modelling. arXiv 2312.00752

[R6] Bellec et al. A solution to the learning dilemma for recurrent networks of spiking neurons (2020). Eligibility traces and learning signals. Publisher: s41467-020-17236-y

[R7] Dorkenwald et al. Neuronal wiring diagram of an adult brain (2024). FlyWire adult fly connectome. Publisher: s41586-024-07558-y

[R8] Lappalainen et al. Connectome-constrained networks predict neural activity across the fly visual system (2024). Structure-constrained modelling plus task optimization. Publisher: s41586-024-07939-3

[R9] Turner-Evans et al. The Neuroanatomical Ultrastructure and Function of a Biological Ring Attractor (2020), authors' supporting dataset and publication reference. Authors’ dataset and publication

[R10] Aso et al. Mushroom body output neurons encode valence and guide memory-based action selection in Drosophila (2014). eLife article

[R11] Gidon et al. Dendritic action potentials and computation in human layer 2/3 cortical neurons (2020). PubMed record

[R12] Hassabis et al. Patients with hippocampal amnesia cannot imagine new experiences (2007). PubMed record

[R13] Liu et al. Human Replay Spontaneously Reorganizes Experience (2019). PubMed record

[R14] Hafner et al. Mastering Diverse Domains through World Models (2023 preprint; DreamerV3). arXiv 2301.04104

[R15] Li et al. BLIP-2: Bootstrapping Language-Image Pre-training with Frozen Image Encoders and Large Language Models (2023). arXiv 2301.12597

[R16] Dettmers et al. 8-bit Optimizers via Block-wise Quantization (2021 preprint; ICLR 2022). arXiv 2110.02861

[R17] Li et al. Memory Efficient Optimizers with 4-bit States (2023). arXiv 2309.01507

[R18] Xu et al. Pushing the Limits of Low-Bit Optimizers: A Focus on EMA Dynamics (2025, version 1 reviewed). SOLO optimizer-state research, not an eligibility-trace benchmark. arXiv 2505.00347v1

[R19] Microsoft. BitNet b1.58 2B4T official model card; BitNet b1.58 2B4T Technical Report (2025). Packed inference versus training-master distinction. Official documentation / model card ; arXiv 2504.12285

[R20] Gupta et al. Deep Learning with Limited Numerical Precision (2015). Stochastic-rounding precedent; not a two-bit eligibility result. arXiv 1502.02551

[R21] Shazeer and Stern. Adafactor: Adaptive Learning Rates with Sublinear Memory Cost (2018). Factored optimizer statistics, not generic exact trace factoring. arXiv 1804.04235

[R22] Hugging Face. Model memory anatomy and Caching, official technical documentation. Training memory categories and KV-state mechanism. Official documentation / model card ; Official documentation / model card

[R23] Dettmers et al. QLoRA: Efficient Finetuning of Quantized LLMs (2023). Frozen quantized foundation plus trainable additions; relevant to generic Forge, not permission to restore NSS neural overlays. arXiv 2305.14314

External materials were reviewed through primary publication pages, paper text/abstracts, authors' data pages or official documentation on 20 September 2026. Inclusion does not imply every paper was reproduced or every implementation audited. Results remain limited to the tasks, organisms and versions named above.

16.3 Audit of this handoff

This preparation consists of source reconciliation, literature review, explicit original modelling proposals, checked storage/rounding arithmetic, and document production. No neural training, biological simulation, benchmark, repo merge or model deployment was performed. All newly named NBR studies remain NOT_RUN. Prior reported percentages are retained with their negative controls and acceptance failures.

The document distinguishes current requirements, old superseded designs, published mechanisms, project-reported evidence, arithmetic and new recommendations. Its recommendation is to preserve a usable reference system while making the neural architecture experimentally replaceable.

End of handoff.