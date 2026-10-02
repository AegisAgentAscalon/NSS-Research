# NSS-NBR02-DC01 — reviewed direction and remaining freeze work

**Review v0.1. PROPOSAL / NOT EXECUTION-READY / NOT AUTHORIZED.** This document preserves the attached specification's question and distinguishes inherited design from this review's analysis. It deliberately does not invent a local update equation, model width or competence threshold and pretend Codex already chose them.

## 1. Source-derived proposal

Codex proposes narrow **delayed-update / trace-retention feasibility**, not unrestricted temporal credit assignment. A learner predicts at a cue, then later receives one causally identified feedback receipt after0/8/32 intervening events. The receipt must not replay the cue features. One pending scored receipt is permitted, and parameters remain at their cue-time version until that receipt. Later forward events are charged but are not ancestors of the earlier prediction in the gradient graph. [CODEX_CANDIDATES; CODEX_REVIEW_REQUEST]

- **G:** retain the actual causal graph upstream of the cue-time prediction and update once when feedback arrives.
- **L:** one explicitly derived local or hybrid trace update on the same model/observations; actual equations, information and state costs remain unspecified.
- **N:** no-update reference.
- **X:** causal exact bookkeeping updated only when feedback is observed. It can be unresolved before learning or wrong after an unannounced reversal; it is not a gold oracle.

Preserve a development-only zero-delay G competence gate before interpreting delayed failures. Score before updates; retain cue errors, interference/old-association retention, invalid updates and all costs. Shuffled receipts must be a declared control, not future-label leakage. Exact definition of that shuffle remains to be frozen.

The final CANDIDATES.md crosses every base with all three delays and both reversal schedules. Eight held-out bases ×3×2 =48 held-out condition streams; five scored probes each yield240 unique condition-occasions. Four fits repeat those occasions; they do not create960 independent tasks. Four development bases similarly give24 development condition streams.

**Source-version reconciliation:** CRITIQUE.md warns against assigning different delay conditions to separate template families. That warning describes an earlier/confounded arrangement. The included CANDIDATES.md and final CHAT_PROMPT already specify within-base crossing. Preserve the corrected crossing; do not present the issue as still unresolved or reintroduce the old design. A crossed schedule still needs exact paired cue/outcome and interference semantics frozen.

## 2. What the new checkpoint evidence adds

The Codex source receipt identifies only its TS03 compact handoff. It does not show CKA01 was reviewed. This handoff therefore adds CKA01 explicitly, without attributing its findings to Codex.

CKA01 found incomplete familiar task execution in TS03, not a hidden reliable earlier checkpoint. That makes DC01's **competent zero-delay baseline a real admission requirement**, not an optional convenience. A poorly fitted predictor cannot tell us much about damage caused specifically by delayed feedback. [CKA01 REPORT §§3,5]

Conversely, the audit does not justify resuming TS03 under this new phase or reusing its troubled task as the learning substrate by default. Choose and qualify DC01's own small association task before interpretation. No integration, new workspace fit or serving-role change follows.

## 3. Independent review: narrowness is useful, but must stay explicit

**IDs supply correspondence.** With one pending receipt and an explicit event ID, the mechanism is not discovering which of many past decisions deserved credit. It tests retaining and applying the assigned cue-time learning information. Ambiguous feedback, many simultaneous receipts and changed-parameter traces remain future questions, not implied accomplishments.

**Elapsed delay need not degrade an exact trace.** Under the proposed frozen-parameter and cue-time-graph contract, retaining an exact sufficient learning trace until feedback may preserve the same update. Later events can affect the live recurrent state and subsequent predictions, and a specified interference/decay policy can affect traces; those mechanisms must be distinguished. Do not require a local learner to outperform an undamaged exact gradient baseline merely because the receipt arrived later. Equality with lower fully counted resources could be a narrower engineering result if such a criterion is predeclared. This is a logical implication of the proposed interface, not an experimental finding.

**Define the graph at receipt boundaries.** Freezing weights while one receipt is pending does not by itself specify how a recurrent state built under earlier weights enters the next cue's graph. Freeze the carry/reset/detach and local-trace clearing rules at every receipt and condition boundary. Both arms must have the same legal truncation boundary; do not silently let one backpropagate through a longer past or reinterpret old activations at current parameters.

**Real retained learning is separate from a pending trace.** State whether recurrent state, eligibility, cue-ID queue, model weights and optimizer state persist at each scored old-association probe. An association test immediately supported by cached cue information is not automatically parameter retention. Distinguish learning reversed associations from preserving unrelated stable ones.

**A local equation is mandatory.** Specify L's parameter surface, derivative/eligibility recurrence, feedback modulation, optimizer and precision. Exact forward derivatives may reproduce the same gradient; an approximation may trade fidelity for cost. Neither is automatically a new biological mechanism, and retained backprop must not simply be renamed local. The supplied proposal has not selected which of these is intended.

## 4. Update arithmetic and an execution-readiness issue

Source proposal: two learned arms × four fits ×600 total permitted update opportunities =4,800 main; two50-opportunity probes add100, global ceiling4,900. The600 covers initial fitting, development adaptation and every held-out condition, not600 per condition.

The provisional actual schedule is:

-100 initial opportunities per arm/fit;
-72 condition streams ×6 receipts =432 online opportunities per arm/fit;
-total532 per arm/fit;68 of its600 remain unused reserve;
-8 arm/fits ×532 +100 probes =**4,356 scheduled opportunities**, **544 below the4,900 ceiling**.

Reserve is not permission for unplanned fitting or selecting an improved checkpoint. Probe and competence decisions must precede untouched held-out evaluation. Clone the same pre-condition model/optimizer/trace state for every paired condition; do not train one condition on another's outcomes.

**Review finding: exact adaptive replay is not yet costed.** Unlike earlier fixed-weight evaluation, reproducing DC01's online learning changes requires update work. A complete rerun of all initial/condition updates would add another4,256 learner opportunities; even replaying only the72×6 condition updates across8 arm/fits adds3,456. Either exceeds the544 spare opportunities under this provisional schedule.

Before dispatch, choose explicitly between a separately budgeted full adaptive reproduction, a predeclared bounded replay subset, or an independent update-arithmetic audit with a precise accounting rule. Charge audit computation and be explicit about what was not re-executed. Replaying frozen predictions alone is not reproduction of online learning. Do not reset counters, use reserve as an implicit budget extension or call update validation free learning.

## 5. Remaining freeze checklist

| ID | Must be fixed before an execution-ready protocol |
|---|---|
| DC-F01 | Model dimensions, parameter/learning surface, initialization, features and task/public observation grammar. |
| DC-F02 | Exact G gradient boundary, L update equations and all trace/optimizer/precision state. |
| DC-F03 | Carry/reset/detach rules across cue, fillers, receipt, reversal, probe and cloned-condition boundaries. |
| DC-F04 | One-pending-ID grammar; receipt provenance, malformed/shuffled semantics, cue-feature exclusion and wrong-scope behavior. |
| DC-F05 | Paired base templates, cue and outcome identities, reversal/interference schedule, scoring before updates, old/new/unresolved probes and normalized-overlap checks. |
| DC-F06 | Disjoint seed recipes and immutable split; development-only zero-delay competence floor, checkpoint policy and outcome-independent stop. |
| DC-F07 | Predeclared learning/retention/resource criteria that allow fair ties; exact X information/cost contract and valid comparison to N. |
| DC-F08 | All-attempt fit/online/probe/replay/update ledger, forward limits, independent update verification and full checkpoint/RNG receipts. Resolve4,900-cap feasibility first. |
| DC-F09 | Actual-host resource and complete-evidence estimate, measurement of traces/graph/queues/history/traffic, fixture checks and source lock. |
| DC-F10 | Explicit bounded NBR-01 closeout decision where required by the program and separate DC01 execution authorization. |

No numerical limits or source hashes have been fabricated for an unwritten implementation. The proposed two-hour,3GiB process-tree/3.5GiB container,256MiB raw/64MiB ZIP limits are ceilings awaiting a real design estimate and cost probe, not promised feasibility.

## 6. Recommendation

Advance **protocol preparation**, not another workspace run and not immediate DC01 training. Preserve the economical, causally explicit framing and the zero-delay competence gate. Resolve the adaptive-surface, trace-boundary and verification-budget choices before generating scored streams. Keep broad G08 credit attribution, G09 retention and G10 serving-update timing distinct from the small feasibility result this design could earn.
