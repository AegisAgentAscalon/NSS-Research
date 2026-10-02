# NBR-02: recurrent state, online learning, and repair
## DEC-NBR02-MECHANISM-FOCUS-001 / CAND-NBR02-STATEBRIDGE-001

**Version:** 0.1. **Date:** 25 September 2026 (conversation system date; source execution reports retain their own measured dates).

**Status:** Research-direction update and proposed next discriminator. Not an experiment, execution protocol, architecture replacement, or claim of newly verified numerical performance. No model, stimulus, gradient, parameter update, state migration, or numerical re-scoring was executed for this document.

## 1. User direction

The user asks how the researched recurrent-state architecture interacts with continual learning, especially maintenance and repair, and asks to continue NBR-02 without the idealized NSS conception determining the result.

Working interpretation: keep investigating mechanisms that can earn a place in a later system. Do not require three separate models, or the proposed shared-backbone challenger, to win. Preserve the broader architectural ideas as design alternatives; do not silently replace the accepted architecture. The objective remains retained useful improvement with manageable degradation and affordable repair, not perfect statistics or acceptance of every beneficial change.

This message continues the research direction. No particular new numerical protocol, training budget, or candidate was selected by the user. This note prepares one question rather than dispatching an unspecified combined experiment.

## 2. Source-derived boundary: the two halves have largely been tested separately

**TS01:** learned temporal task progress with fixed weights during evaluation. The small GRU maintained two four-bit checklists; task-bank routing, protection of the inactive bank, and distractor filtering were supplied by code. Carry and full-prefix inference replay succeeded on the bounded test. State erasure was an information-removal control, not an equal-information efficiency competitor. [S1 §§1–4]

**MICROMACRO01:** real weight adaptation and repair with a recurrent tanh model, but every cue/query starts from reset temporary state. Its protocol explicitly says no retained recurrent state crosses weight revisions. Each association condition also restarts from an initial model checkpoint. Therefore it tests short learning-and-repair cycles, not concurrent persistent task memory or lifetime learning. [S2 §§1–2; S3 Model and lawful inputs]

**TEACH01:** actual frozen teacher and adaptive student computations with a fixed curriculum coordinator. It demonstrates a modest teacher contribution when some direct old records are omitted. All deep branches also meet the bounded feasibility screen; the evidence does not establish tri-core necessity, live-state migration, or plasticity recovery. [S4 §§2–6]

**Clean-slate assessment:** hypothetical alternative, not an adopted replacement. It already identifies state/parameter version compatibility as unresolved. [S5 Distinct state and memory contracts; Resource and version boundaries]

These statements are from the inspected source documents. Their training, scoring, replay, and delivery claims were not numerically reproduced in this planning pass.

## 3. Three stores with different jobs

- **Working recurrent state h:** current unfinished information computed from a history of events.
- **Learned parameters theta:** the transformations used to update and read that state.
- **Evidence/history M:** the permitted source records from which state or learning examples may be reconstructed.

A fourth object, the **learning trace or retained computation graph**, is not interchangeable with h. It supports a particular delayed derivative calculation and binds to a parameter version. The first bridge pilot should drain any pending receipt before switching versions rather than also study stale-gradient learning.

For illustration, at an interruption:

    h_old = Run(theta_old, initial_state, public_prefix)
    theta_new = a lawfully updated or repaired parameter snapshot

Two different resumption states are then possible:

    CARRY:   h_old, interpreted by theta_new
    REBUILD: Run(theta_new, initial_state, the same public_prefix)

There is no construction here that requires those states to agree. Whether either produces correct continued behavior is an empirical question. State-vector distance is a diagnostic, not the definition of preserved meaning. Rebuilt state is not a correctness oracle.

## 4. Maintenance has two responsibilities that must not be merged

**Parameter repair:** improve or restore task behavior when the updated learner starts from a valid fresh state. This is closest to the existing NBR-02 repair evidence.

**Continuation repair:** preserve or reconstruct the useful meaning of an unfinished state when the transformation reading/updating it has changed.

A rehearsal batch that repairs fresh-start behavior might leave a pre-existing working state unsuitable for the revised model. Conversely, recomputing state might fix a mixed-version continuation without repairing any learned parameters. Neither possibility is an observed result here.

Training itself must not use the active task buffer as scratch space. In the proposed pilot, the carried task state is copied/checksummed, candidate learning uses separate scratch state, and any mutation of the saved buffer is an engineering failure. Perfect preservation of its bytes still does not prove semantic compatibility.

## 5. Proposed next question

> When a model learns and then performs a bounded repair, does unfinished recurrent work remain usable under its new weights? If not, does a costed inference-only reconstruction from the same public history restore correct continuation?

This is a state–learning interface question within NBR-02. It does not reopen NBR-01's accepted bounded results or qualify the parked workspace-fitting candidate. No core labels are required.

### Minimal meaningful task

Use one small model with a genuinely trained state-dependent task and a declared adaptive parameter surface. A fixed-semantics unfinished task A must coexist with learning a different association/task B through the same chosen parameter surface. The intervention must not legitimately change A's target semantics; otherwise a correct revised answer could be mistaken for lost progress.

A short, context-dependent procedural task is a candidate. Different legal prefixes should have the same final input/suffix but require different continuation answers. That prevents the last cue from already revealing everything. The existing DC01/MICROMACRO cue IDs encode substantial identity information and their reset-three-step interface must not be renamed long-horizon memory.

Before main work, demonstrate held-out fixed-weight task competence, genuine dependence on the earlier prefix, and consistency of carry versus full-prefix replay when weights have not changed. Use an independently computed task oracle for scoring, never as a hidden-state input. RESET without history is a diagnostic information-removal control, not a stronger or equally informed competitor.

The TS01 GRU and DC01-family dense tanh model have different dimensions, output heads, training tasks, and update mechanisms. Do not load a state from one into the other or describe a software adapter as a learned compatible interface. A compatible task/interface must be specified and trained or validly transferred before this experiment is executable.

### Paired causal comparison

1. Process the permitted task-A prefix at theta0 and retain h0 and the reconstructible public history.
2. Complete or lawfully drain unrelated pending credit records; pause task-A progression at a defined event boundary.
3. In a separate scratch context, use legitimate feedback for task B to produce theta1 under the selected ordinary update rule.
4. Apply one separately fixed, paid repair schedule to obtain theta2. No new teacher, learned selector, token lane, or repair-coefficient sweep is introduced.
5. At theta0, theta1, and theta2, branch into CARRY, REBUILD, and RESET. Each branch at a given parameter version receives exactly the same weights, public history, and future task-A inputs. Continuation readouts do not execute new optimizer updates.
6. Score unfinished task-A continuation, fresh-start old behavior, new task-B acquisition, and required costs separately. Repair that restores A while deleting B is not success.

| Parameter stage | Carry saved h0 | Rebuild h from prefix at that stage's weights | Reset h without prefix |
|---|---|---|---|
| theta0, unchanged | Ordinary continuation reference | Implementation/reference equivalence check | Information-removal diagnostic |
| theta1, after online learning | Direct state-reuse candidate | Weight-matched reconstruction reference | No-history diagnostic |
| theta2, after fixed repair | Does parameter repair also preserve old working state? | Does repair plus reconstruction restore correct work? | No-history diagnostic |

Repeated branches and readouts are paired measurements, not independent tasks. G/L, if both are retained, need separate results. Choosing one exact-gradient reference first is a possible scope reduction, not a decided algorithmic winner or an authorized omission.

## 6. Interpretation fixed before running

- **Carry remains adequate:** state repair is unnecessary at this bounded scale; do not invent a migration problem.
- **Rebuild improves continuation at identical theta:** state reuse/reconstruction contributes to the outcome. This is evidence of an interface effect, not proof of a unique internal representational cause.
- **Both carry and rebuild are poor, and fresh-start checks are poor:** learning/retention competence is inadequate. A state mapper alone has not been shown sufficient.
- **Repair restores fresh-start behavior but carry remains poor while rebuild succeeds:** weight repair and continuation repair are empirically separable under this task.
- **All continuation branches are correct but reconstruction costs much more:** carry may be the better engineering choice; count the actual difference without inferring general efficiency.
- **A gain is obtained only by retaining unbounded history:** report the reconstruction trade-off. A bounded-window or learned migration alternative becomes a separate future question.
- **Task B fails or is erased by repair:** preserving A does not qualify overall learning.

The task oracle, not resemblance to old outputs or closeness of hidden vectors, determines correctness. If new evidence legitimately changes a target in a later study, its temporal semantics must be specified separately.

## 7. Costs and failure-first records

State reconstruction is inference over the already observed prefix; it must not reapply the historical training receipts. Retaining the history and rereading it have real storage, bandwidth, and transition costs. Full learning replay for experimental verification is a separate charged operation.

Record parameter IDs, state-producing parameter ID, scope, event cutoff, prefix identity, readout version, scratch-buffer isolation, receipt/trace state, repair work, reconstructed-state identity, continuation outputs and exact target provenance. Keep first observable divergence distinct from root-cause hypotheses.

Measure task accuracy/loss, lost progress, new-task retention, tolerable temporary deficits, recovery latency, model/working/history storage, reconstruction transitions and all update/derivative costs. Report both improvement and cost; a slower safe boundary may be adequate, and no-update/no-learning controls must not masquerade as successful adaptation.

Do not invent numerical margins, seed counts or pass thresholds in the report after seeing results. Before dispatch, complete a versioned protocol with exact task inputs/semantics, chosen compatible model and adaptive surface, fixed updates/repair schedule, independent scorer, competence gate, legitimate data split, operational allowances, all-attempt resource ledger, and reproducible packaged source. Export the executable package before long computation. The current note is not that executable lock.

## 8. Program disposition

NBR-01 stays CLOSED_BOUNDED_RECOVERED_EVIDENCE. NBR-02 continues as mechanism-led research. MICROMACRO01 and TEACH01 remain bounded references with their limitations; no result is erased. The broad tri-core design and hypothetical shared-backbone alternative remain design possibilities, not required explanations or selected implementations.

Retain the user's manageable-loss/affordable-repair/retained-improvement objective. RET-MW01-FIT-001 is parked; the separate Q010 identity question is not conflated with it. Dream maintenance, self-play, teacher-guided full-core consolidation, capacity growth, source retirement, and live deployment are not dispatched. Preserve FCR-0103-001 (return to 01–03 foundations after 03 and before 04) and the existing conditional earlier return, whose precise skipped ticket still needs identification.

This proposed interaction study is not automatically a new stage-closeout requirement. It is the preferred next preparation because the user asked about the state/learning boundary. No broader experiment has been selected or run here.

## Sources

S1: NSS_TS01_Execution_v0.3/REPORT.md, sections 1–4.
S2: NSS_NBR02_MICROMACRO01_Execution_v0.2/REPORT.md, sections 1–2 and 10.
S3: NSS_NBR02_MICROMACRO01_Execution_v0.2/protocol/PROTOCOL.md, Model and lawful inputs.
S4: NSS_NBR02_TEACH01_Execution_v0.1/REPORT.md, sections 2–6 and 9.
S5: NSS_Clean_Slate_Architecture_Assessment_v0.1/ASSESSMENT.md, status and state/version boundaries.

SOURCE_IDENTITIES.json identifies the locally present source bytes. Hashing is not numerical replication. No prior file was rewritten.
