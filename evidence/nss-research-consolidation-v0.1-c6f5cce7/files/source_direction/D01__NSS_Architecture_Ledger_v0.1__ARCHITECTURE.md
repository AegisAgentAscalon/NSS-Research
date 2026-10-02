# Neural Space System — Architecture Ledger

*VERSION 0.1  •  24 SEPTEMBER 2026*


Tri-Core Validator NSS xTREME
Implementation track: MegaMind Alpha


Living architecture specification, decision record and Transformer comparison. Consolidates the adopted system direction with the Q010 → CM-01 → CM-02 → TS01 research trail and the maintained management-token concept.


### Core design direction


Use exact memory for retained evidence, learned recurrent state for evolving work, and a bounded explicit workspace to manage their use. Preserve the participating frozen Primary, adaptive/task Secondary, predictive/reflection Tertiary and fallible advisory Validator. [U01; S01; S11–S12]


### What this release is


A documentation consolidation, not an integrated neural implementation or a new scientific result. It records deliberate departures, compatible extensions, shared mechanisms and unresolved choices. No experiment, training job, model load, numerical replay or repository write was performed for this release.


Read the short orientation first. Use the master by section; use the registers for exact IDs, evidence limits and successor handoffs. Existing study archives remain independent and are not copied into this package.



---
## 01 / Orientation and source precedence

*READ FIRST*


The architecture is broader than any one neural checkpoint. Neural Space names the governed environment containing models, memory, working state, context, training, evaluation and runtime boundaries. A Primary generation exists within that environment; it is not the entire environment. [S03 §2]


| Evidence label | Meaning in this ledger |
| --- | --- |
| ADOPTED / DIRECTION | A user requirement or retained project direction; not a claim of implementation. |
| BOUNDED EVIDENCE | A completed mechanism study, with its actual information and task limits. |
| PROPOSED / OPEN | A candidate or unresolved decision; no silent promotion to canon. |
| HISTORICAL / SUPERSEDED | Preserved for provenance; not current authority on the superseded point. |
| SOURCE UNVERIFIED | Current implementation or underlying raw evidence was not inspected here. |


Precedence: latest explicit user decisions govern intent; inspected source governs implementation; recorded experiments govern only their tested claims. New proposals do not overwrite old outcomes. Older optional-overlay wording loses to the later explicit overlay removal. [S01; S02 §1]


### Navigation


Sections 02–08: roles, schedule, state, exact memory and maintained tokens. Sections 09–16: context, interfaces, reflection, validation, learning, output and costs. Sections 17–22: layer-by-layer Transformer comparison. Sections 23–27: evidence, candidates, open decisions, change control and glossary.


The last cumulative NSS source identified by the 19 September handoff was MegaMindAlpha v0.4.17. That is a historical source-status statement, not a fresh audit of today’s repositories. Later studies here are standalone. This ledger inspected reports/proposals and selected older architecture text, not the full production codebase. [S01; S13]



---
## 02 / Mission, roles and invariants

*ADOPTED SYSTEM DIRECTION*


Mission: a competent local personalized companion, with English and Japanese priority evaluation languages. The project does not adopt frontier-scale or recursive-self-improvement claims. Example 100B/50B/50B core sizes were scenarios, not selected local hardware requirements. [S01; S02 §§1,12]


| Component | Responsibility and boundary |
| --- | --- |
| Primary | Frozen for its accepted generation; participates during task, learning, reflection and verification phases. Language, reasoning, identity-bearing behavior and coordination remain meaningful responsibilities. Qualified Primary-only fallback is required. |
| Secondary | Active task work, personalization, reusable competence and permitted post-task learning. Not permanently a routing-only or tiny-readout component. |
| Tertiary | Predictive world model, imagination, reflection, consolidation preparation and functional appraisal. Runs while Secondary is inactive; not a fifth added world-model core. |
| Validator | Separately trained, frozen, fallible advisor. Provides evidence relations/challenges to Primary. No output veto, permission, authorization or release-approval authority. |


Neural overlays are removed from intended NSS growth. This does not remove generic LoRA/PEFT support from Forge. Secondary/Tertiary mutual exclusion and Primary participation remain current constraints. [ADR-002–007; S01]


Model size, cell family, layer count, attention arrangement and learned bridge dimensions are not selected for the full cores. TS01’s GRU is a mechanism fixture, not the new Primary, Secondary or Tertiary. Functional role names do not establish physical residency, competence or speed. [S02; S08]



---
## 03 / Phase schedule and handoff

*POLICY RETAINED; IMPLEMENTATION DETAILS OPEN*


| Phase | Participating roles | Boundary |
| --- | --- | --- |
| Task / interaction | Primary + Secondary | Tertiary paused. Primary contributes, rather than merely narrating. |
| Permitted post-task learning | Primary + Secondary | Approved candidate surfaces and data only; Tertiary remains inactive. |
| Reflection / exploration | Primary + Tertiary | Secondary and its learning activity paused. Hypotheses remain labelled. |
| Evidence check | Primary with advisory Validator | Invoke under a declared budget; feedback does not grant permissions. |
| Fallback | Primary only | Preserve qualified basic service while optional auxiliaries are unavailable. |


Always active means actual participation across active phases at a defined cadence. It does not mean only leaving weights in RAM, generating language continuously, or executing at maximum rate. An inactive component may still consume memory; unloading exchanges residency for reload latency. [S02 §7]


### Handoff contract to complete


A proposed handoff binds the producing component and Primary generation, task/scope, observed-event cutoff, state/codec versions, pending work, evidence references and hypothetical origin. Checkpoint the outgoing auxiliary, switch ownership at a safe boundary, then resume the incoming one from compatible state. Atomic details and physical scheduling are not yet a complete implementation. [S02 §7; S04]


A user interruption must not turn a partial reflection into a completed discovery or expose partially applied learned updates as an accepted revision. Background successor training is separately budgeted work, not a fifth personality or free compute. No claim is made that useful computation continues while the hardware is off. [S02 §§7,12]



---
## 04 / State inventory: do not call everything memory

*SEPARATE OWNERS, LIFETIMES AND WRITERS*


| State class | What it retains | Main distinction |
| --- | --- | --- |
| Serving parameters | Learned transformations and skills | Not changed by ordinary inference-state updates. |
| Temporal recurrent state | Evolving task progress | TS01 demonstrated this in a tiny scoped task. |
| Internal refinement state | Work within extra processing iterations | Different from carrying information across events. |
| Maintained management workspace | Goals, modes, constraints and references | Explicit organizer; native benefit untested. |
| Active context / KV | Current model inputs and cached projections | Private to a model/session; not an exact archive. |
| Exact evidence + indexes | Events, records, bindings and revisions | Source-backed, editable/versioned under policy. |
| Broader Working Space | Tasks, branches, tests, artifacts, pending work | May exceed the small resident packet. |
| Fast adaptation / traces | Temporary associations or delayed credit | Potential plasticity; not automatically harmless cache. |
| Training state | Optimizer, RNG, gradients and cursor | Needed for exact supported resume. |
| Appraisal / hypotheses | Salience, predictions and imagined branches | Neither truth nor authorization. |
| Runtime metadata | Permissions, jobs and compatibility | Deterministic authority, not a neural belief. |


The ST-01–ST-12 register specifies the proposed/retained owner, representation, lifetime, writer, reset and migration boundary for each category. Some ownership details remain open. A vector’s name does not exempt it from privacy or learning policy. [S02 §4; S08; S12]



---
## 05 / Exact memory and the larger Working Space

*ADOPTED SEPARATION; BOUNDED STORAGE STUDIES*


Exact storage preserves source events and evidence. Structured records, summaries and indexes help select it; they do not replace its provenance. The larger Working Space owns inspectable goals, unfinished investigations, branches and artifacts. The small maintained workspace is an active view or controller aid, not the entire Working Space. Their production ownership and synchronization remain design work. [S01; S02 §§4–7; S11]


### A useful conceptual path


```text
Observed event / source artifact
  → exact archive + provenance
  → versioned records / indexes / summaries
  → selected active evidence + management references
  → learned processing and derived work
  → explicitly labelled result or proposed action
```


An exact record can be wrong about the world; exactness refers to faithful storage, not automatic truth. Separate observed, reported, derived, hypothetical and proposed-action status. Model confidence, repeated rehearsal and an attractive imagined outcome cannot promote a claim to observation. [S01; S02; editorial clarification]


### Corrections, revisions and deletion


A correction should be recordable without waiting for gradients. Keep source relationships and supersession explicit; do not silently rewrite the source of an old decision. Distinguish a missing pointer, an inaccessible record, a deleted entity, an outdated revision and a genuinely absent fact. Privacy removal and training-data revocation need their own policies: deleting a record does not necessarily remove facts already learned into weights. [S01; S02 §§5,12; S07]


The evidence ledger links CM-01/CM-02 to reference selection, exact lookup and freshness. It does not elevate these small stores into a fully implemented long-term companion memory service. [EV-CM01; EV-CM02]



---
## 06 / Maintained management tokens

*CENTRAL ADOPTED DIRECTION; NATIVE COUPLING UNTESTED*


Context tokens support information management rather than being the primary repository of the full task history. Necessary facts, a short intermediate result, user language and temporary retrieved evidence may still be tokens. There is no token-free purity rule. [U01; ADR-008–010; S11–S12]


| Responsibility | Intended content |
| --- | --- |
| Recurrent task state | The changing work: progress, intermediate computation and learned task representation. |
| Maintained explicit workspace | What is active: goal, task/scope, constraints, mode, selected evidence, revisions and unresolved issues. |
| Exact persistent memory | Detailed records and source evidence, retrieved under explicit scope and cost. |


### Three distinct choices


Residency: retain a bounded packet while the system operates. Consultation: decide which active steps read it. Rewriting: update slots at meaningful events or another declared schedule. A packet can be consulted repeatedly without being regenerated or growing. Tokens are interpreted by a controller/model; they are not autonomous managers. [S12]


### Illustration, not a selected format


```text
task=compare_designs
mode=verify
constraint=no_historical_retraining
evidence=record_17@revision_4
open=which_entity_is_intended
```


This text is not a claim about a specific tokenizer count. CM-01 used a 56-byte ASCII control packet; CM-02 used two such packets. Those were deterministic reference wrappers. TS01’s immediate one-hot events were not a maintained management lane. Native discrete tokens, ordinary fields and soft embedding slots have different costs and must remain distinguishable. [S06–S08; S12]



---
## 07 / Workspace lifecycle and unresolved control choices

*SEMANTIC CHECKLIST; NOT AN APPROVED WIRE FORMAT*


Every proposed field needs a source, scope, owner, revision, allowed writer, read/refresh policy and response to invalidation. A model-generated verified label is not evidence. The first source-copying writer proposed in IM-01 would simply retain public task/mode commands; this is disclosed software assistance, not learned autonomous management. [S10; S12]


| Event or condition | Policy that must be explicit |
| --- | --- |
| Initialize / enter task | Unset values, permitted source context and owner. |
| Focus or mode changes | Which field changes; which unrelated work must survive. |
| New evidence or correction | Revision link, dependency invalidation and whether re-evaluation is required. |
| Conflict / missing evidence | Preserve unresolved status; do not silently manufacture a binding. |
| Evict / exceed budget | What leaves active context, where it persists and retrieval cost to recover. |
| Pause / resume / migrate | Component generation, schema, event cutoff and compatible checkpoint. |
| Propose an external operation | Pass through independent authorization; tokens are not permits. |


Stable-versus-scratch sections, evidence-backed candidate promotion, learned write gating, provisional/committed modes and stale-derived-state invalidation are candidate mechanisms. They are not all adopted merely because they appear in this register. [S10; S15]


The exact packet cap, discrete vocabulary, writer training objective, per-core versus shared ownership, synchronization and refresh schedule are open. A future protocol must prevent hidden answer information from entering fields while also counting the source-copying/index machinery that makes those fields available. [OQ-02–06]



---
## 08 / Recurrent computation and the three clocks

*BOUNDED TEMPORAL STATE EXISTS; OTHER AXES REMAIN OPEN*


```text
External events:        h[t+1] = F_theta(h[t], x[t])
Internal refinement:    z[k+1] = G_theta(z[k], input)
Parameter learning:     theta[next] = theta + update

Proposed hybrid interface, not an implemented NSS cell:
  h[t+1] = F_theta(h[t], x[t], C[t], retrieved_evidence)
  C[next] = U(observed_events, h[t+1], C[t], provenance)
```


Event index t and internal iteration k are different clocks. The serving weights theta may remain frozen while h changes. Reusing an operator over k spends computation; carrying h over t need not generate language. Updating U may change explicit state without training either F or U. Any temporary adaptive weights or eligibility traces require a separate declared learning contract. [S02 §4]


### What TS01 actually contributes


Five new GRUCell(9,64)+Linear(64,9) fits learned two four-bit checklists. Each used two 64-float banks, 512 state bytes and 14,985 parameters. All five reached 120/120 held-out joint answers; state erasure yielded 40/120 per fit. Code selected/protected task banks and filtered no-ops; RESET entered the learned transition. [S08 §§1–4]


TS01 trained with Adam/backpropagation, froze weights at evaluation, and tested temporal retention—not learned internal iteration, language, management tokens or autonomous task selection. Its eight logical progress bits fit an exact packed byte before metadata. Carry required 1,612 transitions/model versus 4,303 for the declared replay schedule; this is not a total-speed or compression result. [S08 §§5,8]


The full NSS update rule remains unselected. A candidate can retain Transformer components, use a recurrent cell, or combine them, provided source compatibility, role policy and fair evaluation remain explicit. [S02 §6]



---
## 09 / Segmented context, HSA/MSA and per-model caches

*PRESERVED DIRECTION; PRECISE OPERATORS NOT RECOVERED*


Retain the multi-resolution context stack: exact archive, chunks, summaries, project/global anchors, sparse/hierarchical selection, bounded active packets and exact rehydration. A summary is a derived aid; source details remain separately recoverable. [S04 §7]


HSA/MSA are preserved project labels for attention/context research. The retrieved governing source explicitly distinguishes external hierarchical selection from native neural attention and warns against inventing a precise MSA implementation from the label. This ledger therefore does not manufacture an acronym expansion, kernel or layer design. [S02 §5.6; OQ-12]


| Mechanism | Evidence needed to call it implemented |
| --- | --- |
| Host-side selection | Actual packet builder, budgets, provenance and retrieval traces. |
| Native sparse attention | Defined attention operator, masks, training and measured kernel behavior. |
| Private model context/KV | Model-specific session, tokenizer/cache format and invalidation rules. |
| Inter-core information use | Qualified exchange and receiver ablations showing useful dependence. |


Shared storage does not merge several models into one raw context window. A Primary may receive goals and selected results while an auxiliary receives a narrower task packet. Exact capacities and final packet policies are not selected here. A KV cache is real inference state and need not imply rereading the entire prompt on every generated token. [S02; R09]


Bounded resident tokens can coexist with temporary larger retrieval packets. Report peak active tokens, total processed tokens, persistent archive growth, cache bytes and reload/reconstruction work separately. A reference to a huge source is not lossless compression of that source into the reference. [S11; S12]



---
## 10 / Binding, freshness and retrieval contracts

*LESSONS FROM Q010, CM-01 AND CM-02*


| Question | Required distinction |
| --- | --- |
| Does the record exist? | Existence is not readability, relevance or permission. |
| Does this address validate? | Scope/version/binding validity is not proof of user intent. |
| Which time is requested? | Pinned historical revision versus continuing-entity current content. |
| Can the payload be read? | Exact retrieval versus approximate learned decoding. |
| Is the evidence reliable? | Faithful storage versus truth/support in the world. |


Q010’s unknown/known identity problem includes strata with indistinguishable public evidence. Passing that same information through another representation cannot create the missing distinction. Retained public context may legitimately add information, but that changes the observation contract. [S05; S11]


CM-01’s near close recall improved from 44% to 71%, concentrated in noisy-query reconstruction; exact retrieval with a valid reference was stronger. CM-02 produced W=I=65.17% versus 51.17% without selection history. The identical workspace/index behavior is evidence for retained information, not special token syntax. [S06; S07]


At revised-known checkpoints in CM-02, pinned references lost five current answers; an explicitly separate revision-following control recovered 5/5. At deleted targets UNKNOWN was correct. Freshness policy must be part of the request, not inferred from the word memory. [S07 §3]


Engineering interpretation, not a universal proven policy: prefer exact retrieval for a trustworthy exact reference and reserve learned processing for acquisition, ambiguity, integration and task-state evolution. Keep wrong-but-valid references, inaccessible sources and unresolved intent in future tests. [S06–S07]



---
## 11 / Interfaces and compatibility

*SEMANTIC CONTRACTS; FINAL ABIS OPEN*


The interface register IF-01–IF-10 names each boundary: observation ingestion, workspace conditioning, exact retrieval, Primary/Secondary exchange, Secondary/Tertiary handoff, Tertiary results, Validator advice, Forge jobs, Runtime actions and generation adoption.


### Proposed common envelope


```text
message / parent event / task / scope
producer component revision / Primary generation
representation schema / tokenizer or codec version
observed-event cutoff / state revision / restore policy
record origin: observed, derived, hypothetical, action proposal
payload: text, token IDs, fields or qualified latent reference
source references / assumptions / uncertainty / permission scope
```


These are inherited design-checklist fields, not evidence that a live API already exposes them. Raw token IDs require compatible tokenization; text can be retokenized. Latent vectors need learned alignment and compatible versions. Checksums establish byte identity, not semantic truth or authorization. [S02 §7.1]


Test correct, missing, shuffled, irrelevant and misleading messages. A successful combined answer may mean the Primary ignored its auxiliary and solved the task alone. The bridge must demonstrate a useful contribution under controlled changes. [S02 §7.1]


Migration must bind weights, representation and checkpoint semantics. Equal tensor shapes do not justify loading an old state into a new generation. Preserve a supported rebuild path and qualified Primary-only fallback. The ownership of a shared maintained workspace and its synchronization with private component states remains unresolved. [S02 §§7.1–7.3; OQ-03,11]



---
## 12 / Tertiary reflection, world model and appraisal

*ROLE PRESERVED; COMPETENCE NOT ASSUMED*


Tertiary is the predictive/reflection role, not a generic overnight text generator. Its intended work includes candidate states or trajectories, counterfactual exploration, unresolved investigations, consolidation proposals and observation-sensitive appraisal. [S01; S02 §5.3]


Keep observation prediction separate from action-conditioned prediction, and longer horizons separate from changed ranges. A plausible imagined plan must be tested against independent outcomes when available. Fitted predictors, executable simulators, search and replay are strong controls, not mechanisms to hide inside a supposedly learned world model. [S02 §5.3]


### Evidence and phase boundaries


An imagined event remains imagined. Replaying it many times does not create many observations. Findings carry provenance, assumptions, checks and failed hypotheses; a proposed training example is not automatically eligible. Secondary can receive qualified material in its next phase without violating Secondary/Tertiary exclusion. [S01; S02]


Appraisal represents such things as significance, uncertainty, progress and control. It can prioritize checking or exploration, but must not upgrade factual confidence, grant permission or optimize user dependence. No result in this ledger establishes subjective emotional experience. [S02 §5.5; S04]


### Historical negative evidence


The September handoff reports ordinary planning success for small neural world-model proxies, but stronger compact fitted/engineered controls on combined range/horizon stress. These are secondary historical reports here, not freshly inspected raw experiments. They support keeping controls strong; they do not prove that a large Tertiary is either necessary or useless. [S02 §1.3; EV-LEGACY]



---
## 13 / Validator and independent authority

*ADVISORY EVIDENCE IS NOT A PERMISSION SYSTEM*


The Validator role is separately trained, qualified and then frozen while serving. It advises Primary about support, contradiction, insufficiency and evidence relations. It has no output veto, execution permit or release-approval authority. [ADR-006; S01]


| Question | Responsible boundary |
| --- | --- |
| Does evidence support this claim? | Validator advice, Primary reasoning and deterministic/executable evidence checks as available. |
| May this operation execute? | Runtime/Nexus and host policy, not a generated confidence or token. |
| May a candidate become accepted? | Independent generation qualification, not the candidate or advisory Validator alone. |
| Must an answer be revised? | Primary considers evidence and valid rules; wrong Validator advice remains possible. |


Supported retention and unsupported acceptance must be measured together. Rejecting everything is not good checking; agreement with Primary is not independence. The historical tiny validators retained 0% and 8.87% of supported claims at the cited strict operating point. No broad or multilingual Validator qualification follows. [S02 §§1.3,5.4]


A deterministic workspace parser or reference validator in CM studies is not the neural advisory Validator role. Its ability to reject malformed scopes does not demonstrate semantic evidence criticism. Conversely, the advisory role does not override deterministic authorization. [S01; S06–S07]


Output commitment checks in a future DARP path must respect this separation. If a deterministic rule blocks an operation, name that rule and its owner; do not misattribute an automatic veto to the neural Validator. [S01; S02 §5.6; editorial reconciliation]



---
## 14 / Learning, plasticity and training infrastructure

*ADOPTED LIFECYCLE; ALGORITHM CHOICE REMAINS CONTESTABLE*


Separate immediate exact correction, temporary adaptation, candidate parameter learning and adoption of a serving revision. A factual correction need not wait for gradients; an inference activation changing is not a weight update. Fast associations that persistently alter behavior still need scope, retention and learning policy. [S01; S02 §§4–5]


TS01 used 10,000 Adam/backpropagation updates over five fits and then frozen-weight evaluation. It does not demonstrate continual self-training, biological credit assignment or replacement of gradient descent. Local/eligibility-based and hybrid learners remain candidates with delayed-credit and retention controls. [S08; S14; S02 §§8–10]


### Forge remains a separate general product


One standalone headless engine must support ordinary LLM pretraining, continued training, full/selected fine-tuning, LoRA/PEFT, supported quantized training, evaluation, resume and export. NSS, GUI and CLI are clients of that engine. NSS should propose, invoke, monitor and assess approved jobs; permanent manual notebook/export choreography is not the destination. [S01]


That endpoint is a requirement, not a claim that the current Forge source was inspected or already exposes every capability. Inference access is not training/gradient/latent/cache access. Scripted job automation and learned judgment about what to train need separate evidence. [S01; S02 §5.6]


### Data and audit contract


Use declared eligible experience, source licensing/provenance and consent, cutoffs, held-out splits and candidate isolation. Keep all attempts, failures, parameter identities, optimizer/RNG/cursor checkpoints and budgets. TS01 retained full new history; Q010’s missing old history remains missing. [S01; S05; S08]



---
## 15 / Generations, continuity and rollback

*NO OVERLAY-COUNT SUCCESSION*


The default successor path is parent-checkpoint continuation with balanced general, new-skill, defining-behavior and memory-use rehearsal. Freeze a candidate P2, adapt S2 and T2 separately against it, retain or independently qualify a Validator revision, then assess the exact complete package. Targeted bridge or joint calibration is escalation, not mandatory hidden entanglement. [S01; S02 §7.3]


```text
Accepted P1/S1/T1/V1 + eligible experience cutoff
  → isolated candidate P2 training and evaluation
  → freeze P2
  → migrate/adapt S2 and T2 against fixed P2
  → independently qualified V revision + full-package assessment
  → explicit experience catch-up and compatible state migration
  → accepted generation switch with retained rollback
```


The sequence is a retained lifecycle direction, not proof of a fully automated implementation. Promotion trigger, candidate work scheduling and exact state migration remain open. A successor clone is extra training work, not a fifth serving core. [S01; S02 §§7,12]


Maintain reconstruction-from-foundation/scratch controls where appropriate. Parent continuation can retain skills, but neither fixed weights nor checkpoint ancestry proves behavioral or subjective identity continuity. The originating companion contributes priorities and evaluation examples; revisions are attributed, and candidate self-approval cannot erase parent criteria. [S01; S02 §12.3]


Never restore a hidden vector solely because dimensions match. Bind model generation, state schema, tokenizer/codec, scope and event cutoff; qualify any transform or rebuild from supported evidence. The older overlay-threshold promotion story is superseded, not pending default behavior. [ADR-007,017; S02]



---
## 16 / Output, precision and complete cost

*RESEARCH TRACKS; NO IMPLIED IMPLEMENTATION*


### DARP and output commitment


The retained DARP semantics are diffusion/refinement within a segment and sequential presentation/commitment of finalized segments, with a qualified autoregressive fallback. The retrieved sources do not select a denoiser, sampling schedule, segment budget or final training loss. Do not expand the acronym into an unverified new definition. A later correction cannot silently rewrite already delivered output. [S02 §5.6; S04 §7]


### Precision is a vector of decisions


Serving weights, temporal state, internal refinement, gradients, eligibility traces, optimizer moments, accumulators and exact identifiers have different requirements. Ternary weights do not make the entire learning system 1.58-bit. Compression of stored state must feed its altered values into later computation to test accumulation effects. SP-01 remains a proposal, not a new measured result. [S02 §§8–9; S10]


### Count the whole phase


```text
Peak active memory = resident model weights + working/cache state
  + management buffers + retrieval/index buffers
  + training variables when active + temporary execution overhead

Also report: persistent archives/checkpoints; processed tokens;
updates/forwards; replay/scans; latency; load time; energy.
```


Measure simultaneous allocations by phase; do not blindly sum mutually exclusive activity. An inactive auxiliary may still be resident. A fixed-size organizer can reference a growing archive, and repeated reads can dominate cost. Distinguish deployed work from diagnostic traces and audit caches. No current evidence establishes total-system memory, speed or energy superiority. [S02 §12; S07 §5; S08 §5]



---
## 17 / How to compare NSS with a Transformer

*NO STRAW-MAN BASELINE; NO AUTOMATIC NOVELTY CLAIM*


The comparison reference is a conventional decoder-only Transformer used for autoregressive language generation, not a claim that every Transformer-based system is identical. The original 2017 paper describes an encoder–decoder architecture built from attention and position-wise feed-forward blocks; the reference here uses the decoder family for the operational comparison. Hidden representations are already continuous. [R01]


Autoregressive caches reuse previously computed key/value projections. They are real inference state; dynamic and bounded/sliding cache policies exist. A fair comparison cannot say a cached Transformer recomputes all earlier projections on every token. [R09]


### Three separate layers of difference


| Layer | What NSS is changing or investigating |
| --- | --- |
| Neural computation | Persistent learned task state, management-conditioned updates, selected internal recurrence and precision mechanisms. |
| System organization | Exact evidence, workspace/context ownership, tri-core roles, advisory validation and phase scheduling. |
| Learning and lifecycle | Eligible adaptation, independent qualification, continuation/catch-up, migration and rollback. |


External precedents matter: Transformer-XL provides segment recurrence; Universal Transformers recurrent refinement; RMT memory-token recurrence; RAG combines parametric and retrieved memory. Mamba and RIMs are useful non-vanilla controls for selective state/update behavior. Recurrent latent-depth work separates extra computation from extra output tokens. These are mechanism references, not evidence validating NSS. [R02–R08]


The next five sections record forty facets. Entries can be a departure, a compatible system extension, a shared mechanism or an open choice. More differences are not an objective by themselves. The research goal is useful quality/cost/continuity under the same evidence and permissions. [ADR-024; S02 §4]



---
## 18 / Transformer comparison 1 of 5

*FACET IDS ARE STABLE; STATUS IS NOT A CLAIM OF NOVELTY*


| Facet / layer | NSS position and qualification |
| --- | --- |
| TD-01  Model unit<br>system + model | Reference: Attention/MLP blocks in a conventional decoder.<br>NSS: A governed multi-component system; internal cell family remains selectable.<br>ADOPTED_SYSTEM; OPEN_BACKBONES. A system architecture is not a drop-in layer replacement. [S01; S02; R01] |
| TD-02  Temporal continuity<br>model | Reference: Token history and, in cached decoding, KV state.<br>NSS: Learned event-to-event task state plus explicit records.<br>TS01_BOUNDED. KV is real state; recurrent Transformer alternatives exist. [S08; R09; R02; R04] |
| TD-03  Internal depth<br>model | Reference: Fixed block depth in the conventional reference.<br>NSS: Repeated latent processing is a distinct research track.<br>PROPOSED. TS01 does not test adaptive reasoning depth; compare UT and recurrent depth. [S02; R03; R07] |
| TD-04  Selective updating<br>model | Reference: Masking/attention select contextual interactions.<br>NSS: Management-conditioned retention/write decisions are candidates.<br>NATIVE_UNTESTED. TS01 bank protection and distractor filtering were supplied by code. [S08; S10; R08] |
| TD-05  Representation<br>model | Reference: Continuous hidden vectors already exist.<br>NSS: Permit latent/structured/non-language processing alongside tokens.<br>DIRECTION. Nonverbal vectors are not an NSS-only difference. [S02; S04; R01] |
| TD-06  Attention<br>model + context | Reference: Attention is central to the reference decoder.<br>NSS: Attention may remain; HSA/MSA and hybrid variants are open.<br>RETAINED_RESEARCH. No adopted ban on attention or proven new attention kernel. [S02; S04; R01] |
| TD-07  Order and time<br>model + system | Reference: Position information orders sequence elements.<br>NSS: Explicit event order, state revisions and phase cutoffs matter.<br>CONTRACT_DIRECTION. Event metadata does not remove the need for order encoding. [S02; S07; S08; R01] |
| TD-08  Halting<br>model + runtime | Reference: Output and inference policies end generation.<br>NSS: Budgeted internal stop/continue is proposed.<br>OPEN. Stable or repeated state is not evidence of correctness. [S02; R03] |



---
## 19 / Transformer comparison 2 of 5

*FACET IDS ARE STABLE; STATUS IS NOT A CLAIM OF NOVELTY*


| Facet / layer | NSS position and qualification |
| --- | --- |
| TD-09  Context-token responsibility<br>system + interface | Reference: Active sequence is the main decoder input.<br>NSS: Bounded tokens support information management, not the whole history.<br>ADOPTED_DIRECTION. Temporary evidence and necessary facts may still occupy tokens. [U01; S11; S12; R01] |
| TD-10  Maintained workspace<br>model interface | Reference: Special persistent control state is an optional extension.<br>NSS: Resident task/mode/goal/reference workspace is the intended next test.<br>NATIVE_UNTESTED. CM strings are not native token embeddings; TS01 has no such arm. [S06; S07; S08; S12; R04] |
| TD-11  Three workspace cadences<br>scheduler + interface | Reference: Cache policy is a separate inference choice.<br>NSS: Separate resident storage, read frequency and rewrite frequency.<br>ADOPTED_DIRECTION. Always resident does not mean continuously rewritten or awake while idle. [S12; R09] |
| TD-12  Exact evidence<br>system | Reference: Retrieval can augment a Transformer.<br>NSS: Exact archive is a first-class governed information source.<br>ADOPTED; TOY_IMPLEMENTED. External memory is not uniquely non-Transformer. [S01; S06; R06] |
| TD-13  Working Space<br>system | Reference: Tools may supply task records outside the model.<br>NSS: Inspectable unfinished work and branches survive component handoffs.<br>RETAINED_DIRECTION. Broader Working Space is not identical to the tiny token packet. [S02; S04] |
| TD-14  Context selection<br>context service | Reference: Bounded context; retrieval may select inputs.<br>NSS: Segmented, multi-resolution selection with exact rehydration.<br>RETAINED_DIRECTION. External selection is not proof of native HSA/MSA. [S02; S04; R06] |
| TD-15  Identity and addressing<br>memory interface | Reference: Matching and retrieval depend on available cues.<br>NSS: Track scope, handle, version and evidence of relevance explicitly.<br>CM_BOUNDED. Valid address is not proof of intended identity; hidden intent stays hidden. [S05; S06; S07] |
| TD-16  Freshness<br>memory policy | Reference: Retrieval policy determines which record version is used.<br>NSS: Separate pinned revision from current-entity content.<br>CM02_BOUNDED. Latest revision control improved freshness, not neural intelligence. [S07] |



---
## 20 / Transformer comparison 3 of 5

*FACET IDS ARE STABLE; STATUS IS NOT A CLAIM OF NOVELTY*


| Facet / layer | NSS position and qualification |
| --- | --- |
| TD-17  Recovery<br>lifecycle | Reference: Caches/checkpoints/history can support recovery.<br>NSS: Bind state, schema, weights, cutoff and provenance before restore.<br>CONTRACT_DIRECTION. A short summary alone does not reconstruct an exact latent state. [S02; S08; R09] |
| TD-18  Memory cost<br>whole system | Reference: Context/cache footprint is part of model cost.<br>NSS: Count recurrent state, tokens, indexes, archives and temporary retrieval.<br>RESEARCH_RULE. Constant active context does not imply constant total storage or compute. [S02; S07; S08; R09] |
| TD-19  Primary foundation<br>system + lifecycle | Reference: A single model may supply the base service.<br>NSS: Frozen per generation, participating across all active phases; usable alone.<br>ADOPTED. Frozen weights do not imply static behavior or inactivity. [S01] |
| TD-20  Secondary<br>system | Reference: Adaptation can be implemented outside a base model.<br>NSS: Task work, personalization and permitted learning have a named role.<br>ADOPTED_ROLE. Not permanently just a router; full language-capable component unqualified. [S01; S02] |
| TD-21  Tertiary<br>system | Reference: World modelling/reflection are not fixed by decoder topology.<br>NSS: Prediction, imagination, reflection and appraisal belong to Tertiary.<br>ADOPTED_ROLE. Do not add a hidden fifth world-model core or substitute prose for prediction. [S01; S02] |
| TD-22  S/T scheduling<br>scheduler | Reference: Application controls concurrency.<br>NSS: Secondary and Tertiary mutually exclusive.<br>ADOPTED. Paused weights may still consume RAM; no measured whole-system efficiency win. [S01; S02] |
| TD-23  Validator<br>system | Reference: Critics/verifiers can supplement any backbone.<br>NSS: Separately trained, frozen, fallible advisory evidence component.<br>ADOPTED_ROLE. No veto/permission/release authority; old tiny validators failed. [S01; S02] |
| TD-24  Appraisal<br>system | Reference: Not an inherent decoder guarantee.<br>NSS: Functional state may guide priorities without becoming evidence.<br>ADOPTED_DIRECTION. No claim about subjective feeling; not an engagement objective. [S02; S04] |



---
## 21 / Transformer comparison 4 of 5

*FACET IDS ARE STABLE; STATUS IS NOT A CLAIM OF NOVELTY*


| Facet / layer | NSS position and qualification |
| --- | --- |
| TD-25  Inter-core transfer<br>interface | Reference: Model-specific internal representations need compatible interfaces.<br>NSS: Token/text/structured messages; qualified latent bridges.<br>DIRECTION; ABI_OPEN. Equal vector shape or shared storage does not establish shared meaning. [S02] |
| TD-26  Fallback<br>system | Reference: Deployment policy supplies recovery behavior.<br>NSS: Primary-only operation remains a qualification requirement.<br>ADOPTED. Logical fallback still needs concrete backend and capability tests. [S01; S03] |
| TD-27  Serving versus learning<br>learning | Reference: Inference state and trained parameters are distinct.<br>NSS: Separate event-state changes, adaptation and qualified weight updates.<br>ADOPTED_BOUNDARY. TS01 evaluation used frozen weights; not online learning. [S01; S08] |
| TD-28  Learning rule<br>learning algorithm | Reference: Gradient optimization remains a strong baseline.<br>NSS: Local, eligibility-based and hybrid credit assignment are research candidates.<br>OPEN; TS01_ADAM. Do not claim gradient descent has already been replaced. [S02; S08] |
| TD-29  Plasticity surfaces<br>learning lifecycle | Reference: Fine-tuning/continued training can be scoped.<br>NSS: Declared adaptive surfaces, post-task updates and candidate isolation.<br>ADOPTED_DIRECTION. A fast-weight cache that changes behavior still needs governance. [S01; S02] |
| TD-30  Training data<br>data + lifecycle | Reference: A training corpus is separate from inference input.<br>NSS: Memory, consent, cutoffs and qualification determine eligible experience.<br>ADOPTED. Memory storage is not automatic permission to train on it. [S01; S02] |
| TD-31  Generational change<br>lifecycle | Reference: Checkpoint replacement is a deployment choice.<br>NSS: Parent continuation, balanced rehearsal, S/T adaptation and full-package checks.<br>ADOPTED_DEFAULT. Continuation is not proof of personality/identity preservation. [S01; S02] |
| TD-32  Neural overlays<br>product architecture | Reference: Adapters are an optional training technique.<br>NSS: NSS overlay ecosystem removed; Forge LoRA/PEFT support retained.<br>ADOPTED_REMOVAL. No revived overlay-count promotion trigger. [S01] |



---
## 22 / Transformer comparison 5 of 5

*FACET IDS ARE STABLE; STATUS IS NOT A CLAIM OF NOVELTY*


| Facet / layer | NSS position and qualification |
| --- | --- |
| TD-33  Precision<br>representation + kernels | Reference: Weights, activations and optimizer state have distinct formats.<br>NSS: Study state/trace precision separately from ternary weights.<br>PROPOSED. Packed storage, fake quantization and low-bit computation differ. [S02; S10] |
| TD-34  Job control<br>tooling | Reference: Training/runtime services are application infrastructure.<br>NSS: Shared standalone Forge engine serves NSS and ordinary GUI/CLI use.<br>ADOPTED; SOURCE_UNAUDITED. An inference API does not imply gradient, latent or resume access. [S01; S02] |
| TD-35  Output commitment<br>output mechanism | Reference: The reference decoder emits autoregressively.<br>NSS: DARP refines within segments then presents finalized segments sequentially.<br>RETAINED_RESEARCH. Not implemented by CM/TS; source gives semantics, not a final sampler. [S02; S04; R01] |
| TD-36  Computation versus language<br>model + interface | Reference: Token generation is not the only possible latent processing path.<br>NSS: Permit work without verbalizing every internal step.<br>DIRECTION. Latent-depth Transformers are valid comparators, not excluded opponents. [S02; R07] |
| TD-37  Authority<br>runtime | Reference: Permission is not guaranteed by a neural architecture.<br>NSS: Runtime/Nexus enforce authorization; models and tokens cannot self-grant it.<br>ADOPTED. Advisory evidence and deterministic authorization are different channels. [S01] |
| TD-38  Testing<br>evaluation | Reference: Competent baselines may use memory and tools.<br>NSS: Exact algorithms, replay, same-information and resource controls stay strong.<br>RESEARCH_RULE. State erasure tests information dependence, not fair efficiency superiority. [S02; S07; S08; R06] |
| TD-39  Identity continuity<br>qualification | Reference: Not a guarantee of any backbone type.<br>NSS: Preserve attributed parent criteria, behavior, provenance and rollback.<br>ADOPTED_DIRECTION. Toy identity policies and fixed weights do not establish subjective identity. [S01; S02] |
| TD-40  Complete system claim<br>whole system | Reference: Compare equally equipped systems as well as individual blocks.<br>NSS: Integrated usefulness, latency, cost and lifecycle remain to be demonstrated.<br>OPEN. No TS01-to-companion or beyond-Transformer superiority inference. [S02; S08; S09] |



---
## 23 / Evidence trail and what changes architecturally

*RECORDED RESULTS; NO FRESH NUMERICAL AUDIT THIS RELEASE*


| Study | Recorded result | Architecture consequence |
| --- | --- | --- |
| Q010 v1.6 | Fixed-weight reconstructed recovery; nominal gates pass; near-novel UNKNOWN 0/640. | Identity information, binding, reading and store integrity are different failures. |
| CM-01 v0.2 | Near close 44% → 71%; string/field parity; exact lookup stronger. | Grounded references help noisy queries. No native-token advantage. |
| CM-02 v0.6 | W=I 391/600; O 307/600; exact pinned 100/120, latest 105/120. | Maintained selection helps; string is not superior to index. Freshness is a policy. |
| TS01 v0.3 | Five fits: 120/120 carry and replay per fit; ZERO 40/120; exact perfect. | Bounded learned temporal state works inside supplied routing. Native maintained lane is still untested. |


Repeated model seeds/checkpoints are not independent episodes. Q010’s stage count, CM’s repeated readouts and TS01’s auxiliary observations have distinct denominators. Reports and archive receipts record internal independent scoring and replay, not third-party replication. [S05–S08]


Preserve negatives: Q010 training/RNG/raw-trace gaps and verifier history; CM-01 no-cue failures and 10,604 incorrect learned decisions; CM-02 1,165 main learned errors, ordinary-index parity and its closed 5,995-attempt history; TS01 655 main ZERO errors, 63 untrained-fixture errors and no compression win. [S05–S08]


Q010’s separately reconstructed +2^-126 probability-bound amendment remains a historical numerical contract; it is not applied to TS01’s independent GRU tolerance. New full TS01 checkpoints do not repair missing old Q010 training records. [S05; S08 §§7–10]


The separate evidence ledger also preserves older capacity/Validator/Tertiary/succession counter-results as historical secondary reports only. No claim is made that the original study archives were reproduced in this documentation pass. [EV-LEGACY; S02 §1.3]



---
## 24 / Candidate map: do not confuse plans with runs

*POST-TS01 RESEARCH; NO AUTOMATIC EXECUTION*


| Candidate | Proposed next question |
| --- | --- |
| IM-01 / PR-IM01 | Retain public TASK/MODE instructions in a small explicit lane; let a shared learned state perform context-dependent updates without protected task-bank routing. |
| IM-02 / PR-IM02 | Distinguish provisional from committed work with a maintained mode; learn COMMIT/CANCEL rather than using a hidden software state backup. |
| SP-01 / PR-SP01 | Find a better state-precision baseline by quantizing between updates of unchanged TS01 models; no retraining. |
| CM-03 / CM-04 | Legacy cadence/checking and fault-recovery proposals; not automatic continuations of closed CM-02. |
| CM-05 | Native recurrent-plus-management-workspace destination. TS01 is a prerequisite, not this experiment. |
| Q010-P1 | Separate original 768-case public-interface proposal; not executed merely because later studies tested related limits. |


IM-01 would initially disclose a software writer copying observable controls. Compare recurrent-only, token-assisted, ordinary extra-capacity and information-equivalent structured input, plus exact streaming and costed replay. Native model use of a maintained lane is different from learning the writer itself. [S10]


No exact new dimension, vocabulary, seed, update count, threshold or hardware target is adopted by this ledger. A protocol must lock those before execution. A 100% TS01 ceiling requires either a predeclared resource reduction or a genuinely more demanding management task; do not adjust held-out difficulty until a favored mechanism wins. [S09–S10]


The earlier MC-numbered MicroContext draft and later CM-numbered plan are not interchangeable. Executed CM-01 used the latest 512-record CM design. New document versions do not relabel historical study IDs or inherited budgets. [S06; S11]



---
## 25 / Open decisions and integration gates

*A BLANK IN THE DESIGN IS NOT PERMISSION TO GUESS*


Twenty-two open decisions are tracked by stable IDs in REGISTERS.json and OPEN_QUESTIONS.md. The highest-impact groups are:


| Group | Questions that still need a decision |
| --- | --- |
| Neural mechanics | Core backbone; recurrent-state topology; management injection; writer learning; internal refinement and halting. |
| Management semantics | Task/core ownership; exact vocabulary/cap; read/rewrite cadence; stable versus scratch; stale derived-state invalidation. |
| Memory and interfaces | Pinned/current intent; observable identity evidence; per-model context; native HSA/MSA; compatible latent bridges and migration. |
| Learning and output | Plasticity rule/surface; precision; successor triggers and catch-up; exact DARP operator/commitment behavior. |
| Whole system | Tertiary usefulness; Validator competence; current source integrations; hardware budgets; English/Japanese evaluation and fair complete-system controls. |


Before calling a component integrated, identify its actual source owner and revision, supported backend operations, state/codec contract, permissions, fallback, migrations and acceptance evidence. Do not promote standalone scientific code into production merely by copying it into a repository. [S01; S02]


Tests should cover source-consistent wrong intent, invalid references, stale derived conclusions, task/workspace mismatch, unavailable archives, state corruption, interrupted updates, incompatible generations, malicious data posing as control, wrong Validator advice and imagined events attempting to enter observation history. These are required test categories or proposed gates, not tests all passed by the current system. [S02; S09–S12]


The inherited G01–G22 problem register remains upstream. TS01 provides bounded progress on temporal state; it does not close delayed credit, internal depth, native interfaces, prediction, multilingual validation, lifecycle integration or whole-system value. [S02 §2; S08]



---
## 26 / Living documentation and change control

*ADOPTED NOTE-KEEPING REQUIREMENT; PROCESS TEMPLATE*


This ledger is the architecture navigation baseline, not an immutable final design. Future work should update it as a small explicit delta rather than append a disconnected recap. The user decides architectural changes; a successful experiment changes evidence status, not automatically every dependent design choice. [U01]


| For every change | Record |
| --- | --- |
| Decision | Stable ID; exact decision; who/what authorized it; scope and superseded statements. |
| Mechanism | Affected core/state/interface; data source; writer/read/reset/migration; costs and failure policy. |
| Evidence | Study/version; input and artifact identity; denominators; results/negatives; provided assistance; independent-check scope. |
| Transformer contrast | Changed mathematical operator, compatible system feature or lifecycle policy; valid strong alternatives. |
| Next gate | What remains unknown; tests and authorization needed before implementation or promotion. |


Maintain ADOPTED, PROPOSED, IMPLEMENTED-IN-STUDY and INTEGRATED/QUALIFIED as separate facts. Preserve old ledgers and immutable results; a source repair or new experiment receives a new version. Model checkpoint continuity is not permission to reset an exhausted attempt ledger. [ADR-023; S07–S09]


### Package roles


ARCHITECTURE.md and its Word rendering are the human-readable master. REGISTERS.json mirrors stable decisions, states, interfaces, facets, studies, proposals, gaps and source identities. Focused Markdown views support low-token handoffs. VERIFY_PACKAGE.py checks delivery hashes and structural references; it does not verify neural claims.


Codex receives the architecture orientation plus the relevant delta, not every old archive by default. Numerical reproduction still requires its own source/evidence dependencies. No scheduled auto-update, repository integration or Library overwrite was performed here.



---
## 27 / Glossary and interpretation safeguards

*TERMS WITH SPECIFIC NSS MEANINGS*


| Term | Meaning / guardrail |
| --- | --- |
| Neural Space | The governed system substrate; not synonymous with a Primary checkpoint. |
| Context token | Input/control representation; not necessarily the storage location of all important information. |
| Maintained workspace | Bounded explicit management context retained between relevant events. |
| Working Space | Larger inspectable tasks, branches and artifacts; not necessarily a tiny token strip. |
| Temporal recurrence | New event processing depends on retained learned state. |
| Recurrent depth | Multiple internal processing iterations for an input; separate from temporal retention. |
| Plasticity | A change to adaptable parameters/associations, with declared learning governance. |
| Exact memory | Faithful records and provenance; not automatic truth or perfect intended-entity selection. |
| Always active / resident | Primary participation versus retaining a buffer; neither means maximal nonstop inference. |
| HSA/MSA | Preserved research labels; final expansion/operator must be source-backed and selected. |
| DARP | Retained segment-refinement plus sequential finalized-segment presentation semantics; implementation open. |
| Validator | Fallible advisory evidence role; not a veto, permission check or release authority. |
| Frozen generation | Serving weights fixed; activations, evidence and behavior may still change. |
| Qualification | Independent acceptance of a specified component/package under declared tests. |
| Transformer divergence | A specified difference from a named baseline—not proof of novelty, improvement or incompatibility. |



---
## 28 / Source guide and audit scope

*WHAT WAS READ, WHAT WAS HASHED, WHAT WAS NOT RERUN*


Project source IDs are used inline throughout the master and registers. The full SOURCE_REGISTER.md/JSON retains titles, file IDs where available, locators, access limits and byte hashes where actually accessible.


| IDs | Sources and scope |
| --- | --- |
| U01 | Direct user role-change, maintained-workspace and comprehensive-note requests in this conversation. |
| S01 / S13 | 19 September starter/orientation: current role, no-overlay, lifecycle and tooling requirements. Text retrieved; raw byte materialization unavailable. |
| S02 | 20 September cognition/low-bit handoff: synthesis, G01–G22, proposed state/interfaces and historical reports. Text retrieved; raw byte materialization unavailable. |
| S03 / S04 | Older Core Concept and Tri-Core Extension. Only compatible provisions retained; overlay sections superseded. S04 raw bytes available; S03 text-only here. |
| S05–S08 | Q010, CM-01, CM-02 and TS01 result reports. Local report bytes read/hashed; numerical execution not repeated. |
| S09 / S12 / S14 | TS01 handoff, maintained-token note and scientific protocol. Local/ZIP bytes checked. |
| S10 / S15 | Independent candidate proposals; all remain proposals. |
| S11 | Latest CM context-management addendum. ZIP-member bytes read/hashed; historical planning status retained. |


The architecture text and public-primary references were reviewed for this consolidation. The delivery checker tests new documentation bytes and links among IDs, not the truth of a source claim. No full cumulative NSS checkout, live Forge/Runtime implementation, old research raw archive or model was loaded and audited here. Original input archives are not merged or embedded.


Where raw Library copies could not be materialized, the source remains text-retrieved and its raw SHA-256 remains unset. This is an access limitation, not a missing document or fabricated hash. The next maintainer must obtain actual source/evidence bytes before changing or reproducing an implementation.



---
## 29 / External comparison references

*PRIMARY MECHANISMS, NOT AN NSS VALIDATION OR NOVELTY SURVEY*


### R01  Vaswani et al. (2017), Attention Is All You Need


1706.03762. Original architecture and HTML sections 1–3 consulted; mechanism reference, not NSS evidence.


### R02  Dai et al. (2019), Transformer-XL


1901.02860. Primary abstract consulted; segment recurrence.


### R03  Dehghani et al. (2018), Universal Transformers


1807.03819. Primary abstract consulted; recurrent refinement/halting.


### R04  Bulatov et al. (2022), Recurrent Memory Transformer


2207.06881. Primary abstract consulted; memory-token recurrence.


### R05  Gu and Dao (2023), Mamba


2312.00752. Primary abstract consulted; selective state-space processing.


### R06  Lewis et al. (2020), Retrieval-Augmented Generation


2005.11401. Primary abstract consulted; parametric/nonparametric memory.


### R07  Scaling up Test-Time Compute with Latent Reasoning: A Recurrent Depth Approach (2025)


2502.05171. Primary abstract consulted; recurrent latent depth.


### R08  Goyal et al. (2019), Recurrent Independent Mechanisms


1909.10893. Primary abstract consulted; selective recurrent modules.


### R09  Hugging Face Transformers documentation: How caching works


Official Transformers documentation, cache_explanation. Official documentation consulted; KV reuse and cache variants.


Access date: 24 September 2026. References identify relevant existing mechanisms and fair comparison families. No published benchmark score, current market ranking or claim of first invention is imported into NSS evidence. The comparison is intentionally not a complete survey of all Transformer variants.

