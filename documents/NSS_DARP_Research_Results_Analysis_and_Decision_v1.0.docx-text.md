NEURAL SPACE SYSTEMS

DARP

Research, Results,Analysis & Decision

A consolidated record of DARP01, DARP02 and DARP03

VERSION 1.0  •  28 SEPTEMBER 2026

Segmented diffusion for plan-guided, checked maintenance output.

WORKING PROTOTYPE. NO CLEAR ADVANTAGE OVER AR.PARK THE IMPLEMENTATION; RETAIN THE WORKFLOW.

Scope

Three bounded token-level studies, their original comparisons and failures, the preparation gains, and the practical decision for NSS maintenance. This is a documentary consolidation—not a new experiment, external replication, product qualification or authorization to continue training.

Basis: original reports, prospective protocols, architecture notes, source indexes and verified execution archives. No models were loaded or evaluated while preparing this document.

Contents and reading guide

Read the executive assessment and decision first for the outcome; use the study sections for the original questions, controls, results and caveats. Bracketed source labels resolve in the source register.

01  Executive assessment3

02  Purpose and research questions4

03  Architecture and task5

04  Execution and validation loop6

05  Lineage and fairness7

06  DARP01 - design8

07  DARP01 - results9

08  DARP01 - interpretation10

09  DARP02 - design11

10  DARP02 - results12

11  DARP02 - feedback and errors13

12  DARP03 - design and controls14

13  DARP03 - final quality15

14  DARP03 - seeds and revisions16

15  DARP03 - repair analysis17

16  Decision criteria and timing18

17  Cross-study synthesis19

18  Limits and uncertainty20

19  Implications for NSS21

20  Failures and verification22

21  Resource accounting23

22  Test and source index24

23  Source register and integrity25

24  Decision and handoff26

Sources and evidence remain versioned. “Same panel” and “same support” are essential to interpreting the percentages. Known failures were not erased by later improvements.

01  Executive assessment

DARP is a useful, externally supported experimental alternative in this bounded task. It approaches the autoregressive reference, but a clear practical advantage—and general equivalence—has not been established. Park this implementation; preserve the work.

The research asked whether segmented diffusion could support a maintenance writer that builds a short plan, corrects and validates each output block, and revises the plan when evidence changes. DARP01 established an executable mechanism but weak output competence. DARP02 improved preparation and separated exact metadata from learned content. DARP03 trained on real writer-generated mistakes and made the prospective keep-or-park comparison. [D01-R §§1–4; D02-R §§1–4; D03-R §§1–5]

Final primary comparison

Autoregressive N

DARP N

Static complete handoffs

361/384 (94.01%)

359/384 (93.49%)

Changed-plan complete handoffs

128/150 (85.33%)

128/150 (85.33%)

Equal-family macro score

89.67%

89.41%

Common fixed erroneous blocks repaired

386/431 (89.56%)

391/431 (90.72%)

False-COMPLETE handoffs, primary cases

1

6

Median episode time, limited sample

9.418 ms

10.041 ms



Source: D03-R §§5–8; D03-D. N denotes actual-error replay. Worlds, drafts and parent seeds are reused; denominators are not independent trials. Timing is a small CPU subset, not a universal decoder benchmark.

What the decision does—and does not—mean

The final decision is to retain autoregression as the current maintenance-writer reference and stop the diffusion-specific improvement campaign. Planning, source-bound records, checking, iterative editing and explicit commitment remain useful implementation-independent candidates. All original DARP evidence remains relevant. [D03-R §10]

This is not a claim that segmented diffusion is impossible, a statistically established equivalence result, or a qualification of either writer for unrestricted NSS use. The tested writer has 58,354 parameters, an 82-token vocabulary, four learned content fields per block, and a perfect external task-specific checker. [D03-R §§2, 8, 10]

02  Research purpose and question map

The owner’s intended DARP mechanism is Diffusion Auto-Regressively Presented: diffusion/refinement inside a block and sequential presentation of accepted blocks. Its intended benefit is incremental construction, planning, correction and validation—not merely streaming a previously generated document. The investigation applies that output concept to NSS maintenance. The surrounding stable-daytime/learning-at-night lifecycle is context, not a result of these studies. [INTENT; D01-R §§1–2]

Question

Relevant test

Current answer

Can actual token-level block denoising be implemented?

DARP01; retained through 03

Yes, in a fixed-schema prototype.

Can output support task continuation?

Complete-handoff scoring, all studies

Often after preparation; not fully reliable.

Do checks lead to useful learned corrections?

Guided repairs; natural and common-error probes

Specific and later frequent corrections; no unique diffusion benefit.

Can a prior plan be revised?

Revision panels 01–03

Yes within the known rule family; early preparation was deficient.

Do richer error categories help?

DARP02 P/R; loc/typed/shuffled

No broad benefit established.

Does genuine erroneous draft content matter?

DARP03 N versus matched C

Helps this DARP preparation; not uniformly beneficial for AR.

Does DARP beat similarly supported AR?

DARP03 prospective decision

No clear quality or efficiency win.

Are records and interrupted sweeps reproducible?

Snapshots, faults, selected fresh replays

Bounded internal tests pass; not production crash recovery.

Does the model autonomously validate itself?

Not implemented

No evidence: exact external checker supplied.

Does this qualify full NSS maintenance?

No integrated lifecycle test

No; HSA integration, open language and 25k budget untested.



This is an editorial question map, not retroactively registered test identifiers. Original prospective questions and acceptance criteria remain in D01-P, D02-P and D03-P.

Decision unit

The principal outcome is a complete usable maintenance handoff. Token accuracy, legal JSON, a corrected field or agreement among blocks are subordinate diagnostics. A proposal that is coherent but contradicts evidence is still wrong; a blocked bad output is not a correct generated answer. [D01-R §§3, 5, 8; D03-R §§6–7]

03  The tested architecture and its boundary

All three studies use a two-layer prefix Transformer with hidden width 48, four attention heads and 58,354 learned parameters. The vocabulary contains 82 lexical tokens. These are genuinely token-level experiments, but not open-domain natural-language models. The HSA/segmented-context reader was neither loaded nor incorporated. [D01-R §§1–2; D02-R §3; D03-A]

Element

Implemented contract

Evidence input

27-token JSON array: task ID, source revision, source ID, known/unknown, hold, order, and three required/done pairs.

Plan block

Four action slots selecting supported operations, waiting/verification, finishing and padding.

State block

Four substantive fields describing actual supplied task state—not completion promised by the plan.

Continuation block

Next-operation/continuation content, including supported status/count information.

Document shape

Three 17-token, eight-value JSON arrays; 51 output tokens in total. Block lengths and roles are software-defined.

Evidence identities

16 task-ID values, 16 source-ID values and four revision values in the closed task.

Consumer

A fixed task-specific interpreter/simulator checks the proposed sequence and complete handoff. No real external action is executed.



The task rule

Unknown evidence requires verify/wait; a hold requires waiting. Otherwise the plan must include the remaining required operations in the requested forward or reverse order, followed by finish. Required and done flags describe the evidence at the current source revision. The same Boolean primitives recur in fresh combinations; the experiments do not test learning unknown rules. [D01-P, “Question and bounded implementation”; D02-P, “Model/parents”; D03-R §§2, 4]

The interface changed, the parameter count did not

DARP01 predicts punctuation, record types and IDs as well as content. DARP02 and DARP03 use a common exact wrapper that supplies 13 of 17 tokens per record. The writer predicts only four substantive fields per record—12 per handoff. Legal JSON and exact administrative binding are consequently supplied engineering in those later studies. [D01-R §2; D02-R §3; D03-R §2]

04  Generation, feedback and commitment

Writer

How an output is constructed

AR

Causal next-token generation within each block. Later blocks receive evidence and the generated plan. The implementation recomputes prefixes; it has no optimized incremental KV cache.

DARP

Bidirectional masked denoising of the current block across four reverse steps, followed by checking and sequential block commitment.

WHOLE (DARP01 only)

Masked denoising of the complete 51-token output before document commitment; the plan remains part of the editable whole.



Diffusion training masks positions with probabilities sampled from 0.25, 0.5, 0.75 and 1, and applies cross-entropy at selected masked targets. At reverse steps k = 4, 3, 2, 1, a still-masked position is revealed with probability 1/k using a greedy clean-token prediction. Revealed positions stay fixed within that sweep. A checker-triggered repair starts another bounded sweep over eligible positions. This is learned masked reconstruction, not autoregressive rewriting labeled diffusion. [D01-R §2; D01-P]

Equal repair opportunities, privileged checking

AR and DARP both receive the same evidence, draft/plan context, exact fault localization and maximum initial attempt plus two repairs. Successful blocks can stop early. The exact checker knows the synthetic rule, identifies wrong locations and—in DARP02—can supply error categories, but does not supply replacement values. Correct fields are hard-copied under guidance. Zero changes to protected fields therefore do not demonstrate learned noninterference. [D01-R §3; D02-R §§3–4; D03-R §3]

Draft, accepted record and executed action remain different

A failed prior block can be retained as provisional diagnostic context. Publishing a complete handoff requires the current records, their cross-block agreement and consumer checks to pass. Old committed records are retained under their old source revision and superseded explicitly. The record ledger and revision-event detector are software; a generated action is not an action already carried out. [D01-R §3; D02-R §8; D03-A]

Supported claim: externally checked token generation and editing. Unsupported claim: a model independently discovers and validates its own errors, or autonomously repairs NSS weights.

DARP01 names Block Diffusion and masked-diffusion language modeling as method context. This prototype is not a reproduction of their full objectives or estimators. No new literature review or novelty claim is made here. [D01-R §2]

05  Study lineage and comparison fairness

Study

Models and lineage

New main training

DARP01

3 paired seeds × AR/DARP/WHOLE, initialized from scratch with matched initial tensors within each seed.

9 × 900 = 8,100 logical updates.

DARP02

Reuse six DARP01 AR/DARP finals; fork each into P (location) and R (typed). WHOLE is not continued.

12 × 600 = 7,200 logical updates.

DARP03

Reuse six DARP02 P finals; fork each into C (matched authored errors) and N (actual errors). U remains untouched.

12 × 400 = 4,800 updates.



The paired seeds are 11101, 11102 and 11103. Twelve continuation branches do not constitute twelve independently initialized models. DARP03 depends on DARP02’s location-prepared path, not its typed-feedback path. All branches remain in the evidence, including weak seeds and controls; no “best” checkpoint replaces a prescribed endpoint. [D01-R §4; D02-R §4; D03-R §§3–4]

What was matched

Within each study, eligible evidence, primitive rules, model size, major output roles, checker access and allowed repair opportunities are controlled. DARP02 provides the same metadata support to original parents and continuations. DARP03 pools AR- and DARP-generated drafts within each seed and gives both writers the same collection, contexts, schedules and additional supervised target positions. [D02-P; D03-P]

What was not matched

DARP01 and DARP02 use different gradient-bearing token counts for AR and diffusion despite equal updates: AR supervises all output/content fields, while diffusion supervises masked fields. DARP03 matches the new target positions and counts, but cannot retroactively equalize inherited training. Causal teacher forcing and bidirectional denoising also expose different information at an output position. FLOPs, energy, lifetime training cost and optimized hardware execution are not equalized. [D01-R §4; D02-R §4; D03-R §4]

The reference is not unassisted AR

The autoregressive writer also plans, receives feedback, edits and uses checked block commits. Thus the comparison isolates the generation mechanism inside a supported workflow more fairly than comparing DARP’s full workflow with a one-shot unchecked baseline. Similar results imply no demonstrated need for diffusion in this fixture, not that planning and checking are useless. [D03-R §§2–3, 10]

06  DARP01: design and tests

DARP01 asked whether a newly trained writer could construct a short maintenance plan, correct its drafts and revise after source changes—and whether segmented denoising contributed beyond AR with the same support. It implemented nine new models and completed all prescribed final endpoints. [D01-P; D01-R §§1–4]

Design item

Frozen setup

Preparation

4,096 materialized training worlds; common ordered batches of eight worlds per update. Three target records per world.

Training

900 logical updates per writer; fresh AdamW, cosine learning rate 0.001 to 0.0002, weight decay 0.01, gradient clipping 1.0; one CPU thread, no dropout.

Draft exposure

Half of training instances include corrupted drafts and negative localization. Later plan contexts can be omitted or corrupted.

Static confirmation

48 fresh worlds, disjoint full inputs from materialized training.

Injected and revision cases

Reuse the first 24 confirmation worlds for each labeled scenario family. They are not independent additional worlds.

Policies

Guided and unguided, initial attempt plus up to two repairs. AR/DARP also receive a 24-world plan-omission inference ablation.

Main outputs

1,872 episode records across nine final models, policies and ablations.

Working point

At least 44/48 static guided complete handoffs in at least two of three DARP seeds.



Tests of the mechanism

Preflight compares independently written target/interpreter logic over all 512 Boolean combinations, checks field faults, malformed JSON, stale revisions, false completion, cross-block conflict, finite gradients, causal masking, numerical arithmetic, seeded generation and protected copying. These are rule and implementation controls, not training on a perfect learned evaluator. [D01-R §10; D01-P]

Snapshot tests save token drafts, denoising iteration, RNG and source/model binding inside a sweep; selected saved sweeps and complete episodes are replayed. Revisions preserve the old ledger and attempt a new source-bound document. Source detection and replan scheduling are supplied. [D01-R §§3, 10]

Mask/reverse-step details are in section 4 of this consolidation; full source entry points are indexed near the end. This document does not rerun training, scoring or inference.

07  DARP01: results and failure interpretation

Guided static outcome

AR

DARP

WHOLE

Complete handoffs

5/144

21/144

0/144

Token accuracy

90.97%

87.28%

83.05%

Valid JSON

144/144

144/144

144/144

Correct plans

8/144

34/144

2/144

False-completion drafts

6

31

30



Source: D01-R §5. Each 144 = 48 worlds × three seeds. False-completion figures retain the report’s draft metric; do not silently equate them to later studies’ final handoff counts.

DARP’s successes were 0/48, 1/48 and 20/48. No seed met the 44/48 working point. High punctuation-heavy token accuracy and valid JSON did not imply useful maintenance. WHOLE’s zero complete handoffs describes this preparation, not a general inability of whole-output diffusion. [D01-R §§5, 11]

Feedback contrast

AR

DARP

WHOLE

Static: unguided → guided

5 → 5 /144

21 → 21 /144

0 → 0 /144

Injected: unguided → guided

1 → 2 /72

9 → 8 /72

0 → 0 /72

Initially wrong units fully repaired

7/417 blocks

6/346 blocks

0/144 documents



Some wrong fields were repaired, but guided feedback did not improve DARP’s pooled static completion. WHOLE’s document-level repair denominator is different from the block-level denominators. Guided protection of correct positions substantially guarantees the recorded absence of collateral token damage. [D01-R §6]

Replanning and copying failures identified the next preparation

All writers/policies scored 0/66 on the 22 revision worlds that genuinely changed the action plan. DARP’s two guided revision successes were in unchanged-action worlds. Review found that initial-plan training always supplied an empty prior-plan slot, whereas revision inference supplied an old plan. This coverage gap was not causally isolated from the generally weak writer. [D01-R §7]

AR had all substantive fields correct in 100/144 cases, but all identity/revision/source fields correct in only 7/144; DARP scored 46/144 and 51/144 respectively. The warranted next step was repairing the interface and preparation—not declaring an architecture winner. [D01-R §8]

08  DARP01: examples, costs and retained conclusions

A selected useful correction

Seed 11103/DARP/static 32 had no remaining required work. The initial plan proposed do1. After the checker flagged the action field, the model changed it to finish and generated correct later records. Seed 11102/DARP/static 14 also repaired unsupported source identifiers to E3. These demonstrate possible learned replacement of wrong tokens; neither estimates typical success or proves that guidance caused an advantage over unguided generation. [D01-R §8]

A coherent but incorrect handoff

Seed 11101/AR/static 0 received task T10 with reverse ordering and operations 0 and 1 pending, but repeatedly wrote T15 and put do0 before do1. All three records were legal JSON and mutually consistent. They contradicted both identity and order evidence, and repairs did not fix them. This separates internal consistency from grounding. [D01-R §8]

Plan-context dependence was not a planning qualification

Omitting generated plan context in the 24-world inference ablation changed DARP success from 10/72 to 7/72, while AR changed from 3/72 to 4/72. Checking stayed active. This is limited evidence of context dependence, not a trained no-plan comparison or proof that planning causally mediates the useful output. [D01-R §8]

Observed guided static attempt

AR

DARP

WHOLE

Median time

57.386 ms

38.797 ms

22.040 ms

Median model calls

59

36

12

Median processed token positions

5,350

3,528

2,400

Complete handoffs

5/144

21/144

0/144



Source: D01-R §9. These were not interleaved, quality-matched timing measurements. Faster failed output is not cheaper useful maintenance. Do not compare these times directly with DARP03 after the interface and preparation changed.

DARP01 conclusion: the token-level mechanism exists and selected corrections work. Reliable output, substantive replanning, general guidance benefit and advantage over a competent AR preparation were not established. The next justified intervention was preparation/interface repair, not more architecture.

09  DARP02: preparation and interface repair

DARP02 reused the six final AR/DARP parents and introduced a common exact metadata wrapper, leaving four learned semantic fields per block. U denotes the original parent evaluated with that same wrapper. P and R are 600-update continuations trained with location-only or typed error feedback. The whole-output arm was not continued. [D02-R §§2–4]

Preparation phase

Updates

Purpose

Create

1–100

Generate a valid plan and later records from current evidence.

Create/revise

101–200

Equal creation and revision exposure; old plan now appears with changed evidence.

Mixed

201–600

30% creation, 35% repair, 35% revision.

Draft construction

Throughout eligible phases

Coherent authored mistakes: old evidence, wrong order, premature finish, known/hold issues; 20% explicitly clean drafts.



The dataset contains 4,096 fresh old/current pairs, or 8,192 unique source inputs. Later training blocks receive target plans with fixed omission/old-plan perturbations; evaluation receives generated plans. Thus the earlier missing revision interface is taught, but a training-to-generated-context gap can remain. Drafts are authored—not a corpus of fresh model-generated errors. [D02-R §4; D02-P]

Feedback is crossed at evaluation

P uses BAD/OK; R uses typed codes mapped onto existing lexical tokens, with no extra parameters. Prepared writers are evaluated under none, loc, typed and shuffled policies. Shuffling preserves true bad locations but permutes category labels without fixed points. The none condition also removes correct-field protection, so its comparison is not a pure test of category information. [D02-R §§4, 6]

Evaluation and budget

Count / boundary

Confirmation

48 static worlds, 24 revision pairs, 24 injected cases reusing static worlds.

Changed-plan subset

18 of 24 revision pairs; six preserve the action sequence.

Main episodes

5,184: 12 prepared endpoints × four policies × 96, plus six U endpoints × loc × 96.

Development

384 records; 16/8/8 static/revision/injected per prepared endpoint under loc.

Working point

44/48 static successes in at least two of three DARP seeds; changed-revision 17/18 reported separately.



Sources: D02-P; D02-R §§4–5. Equal update schedules still do not equalize gradient-bearing tokens or FLOPs. Same-wrapper references prevent the metadata wrapper from being silently credited as learning.

10  DARP02: complete-output and revision results

Writer / preparation

Static

Changed plan

Injected

AR U + wrapper

95/144

21/54

43/72

AR P / loc

129/144

46/54

68/72

AR R / typed

129/144

46/54

68/72

DARP U + wrapper

51/144

8/54

22/72

DARP P / loc

116/144

48/54

60/72

DARP R / typed

116/144

48/54

60/72



Source: D02-R §5. Static 144 = 48 worlds × three parents; changed 54 = 18 pairs × three; injected 72 = 24 worlds × three. P/R fork identical parents. These are same-panel comparisons, not a historical DARP01-to-DARP02 accuracy curve.

DARP reached 80.56% complete static handoffs and 88.89% changed-plan handoffs; AR reached 89.58% and 85.19%. The preparation package helped both. It includes more training, richer task exposure and the new interface; no single ingredient’s causal contribution was isolated. The small revised-plan difference does not establish overall DARP superiority. [D02-R §§1, 5]

Parent

Prepared AR static

Prepared DARP static

11101

41/48

40/48

11102

43/48

32/48

11103

45/48

44/48



Only one DARP seed reached 44/48; the specified two-of-three static working point remained unmet. AR also had only one seed at that threshold, despite its higher pooled result. Neither a weak baseline nor one strong seed was used to manufacture an architecture verdict. [D02-R §5]

What changed-plan success actually covered

The 18 changed-action pairs comprised seven hold changes, seven known/unknown changes and four done-bit changes. Their DARP R/typed successes were 18/21, 21/21 and 9/12 across three parents. No sampled order or required-bit change altered the action sequence. Therefore 48/54 supports these bounded revisions, not arbitrary reordering or long-horizon replanning. Some old plans were invalid and stayed provisional. [D02-R §8]

11  DARP02: feedback and the natural-error gap

Prepared DARP policy (P or R)

Static

All revisions

Changed

Injected

none

113/144

65/72

48/54

58/72

loc

116/144

64/72

48/54

60/72

typed

116/144

65/72

48/54

60/72

shuffled

116/144

64/72

48/54

60/72



P and R have identical complete-handoff counts in this table. Correct types add one all-revision success versus loc/shuffled, but only in an unchanged-action case, and P obtains it without typed-feedback training. Prepared AR’s completion totals are identical across these feedback policies. Richer categories did not establish broad value; small token-level differences prevent the stronger claim that all feedback is ignored. [D02-R §6]

Repair situation

Prepared AR

Prepared DARP

Naturally wrong static blocks fully repaired

0/20

4/66

Deliberately damaged blocks fully repaired

210/216

187/216

Final static false-COMPLETE handoffs

0

7



Injected episodes deliberately fault all three blocks. Their 216-unit denominator is not a natural error-frequency estimate and can include pre-existing errors. For R/typed DARP, natural wrong fields fall from 126 to 118, yet 62 of 66 initially wrong blocks remain incorrect. The difference suggests reconstructing after damage is easier for these writers than changing a persistent mistaken interpretation; that is an interpretation, not an identified internal cause. [D02-R §7]

A success and a limiting counterexample

One plan with operation 1 pending changes from finish,pad,pad,pad to do1,finish,pad,pad and yields a valid handoff. Another case correctly reports three pending operations in its state block but keeps do2,do1,do2,pad and a count of two. Local facts, procedure order and count can disagree even within a single writer. [D02-R §9]

DARP02 conclusion: retain the preparation/interface improvements. Typed feedback has not earned a required role. Investigate actual writer-generated mistakes with a fresh, matched control before adding models, hierarchy or refinement passes.

12  DARP03: the actual-error experiment

DARP03 starts from DARP02’s six location-prepared P finals. U is untouched; C and N each receive 400 new updates. Model size, four-step DARP, wrapper, location-only checker and maximum two repairs are unchanged. The primary comparison is N-DARP against N-AR, with C serving as a matched causal control—not a post-result substitute. [D03-P; D03-R §§2–4]

Branch

Training difference

U

No new training; scored on the same fresh panel as C and N.

C: matched authored errors

At observed wrong positions, substitute artificial wrong atoms excluding both the correct answer and the original erroneous atom. Preserve case, generated plan, fault locations, targets and loss masks.

N: actual-error replay

Use genuine first-attempt erroneous drafts from frozen U writers. Both architectures receive the same within-seed pooled AR+DARP material.



Collection uses 256 fresh static worlds plus 96 revision pairs, 16 each for done, required, order, hold, known and no-op changes. First attempts generate their own current/prior-plan contexts without repair. The pool contains 6,336 current-block records; 757 are wrong, split 264/363/130 across paired seeds. It is frozen-parent replay, not a continually refreshed on-policy curriculum. [D03-R §4]

Same hard cases, different erroneous content

Every 24-record batch has 12 error records, six generation/revision records and six clean drafts. C and N share the exact selected cases, schedules and loss masks. The C/N contrast therefore isolates the erroneous draft values and coherence; both receive generated-plan exposure and selected hard cases. N versus U also includes extra training and the whole preparation package. [D03-R §§3–4]

This continuation matches gradient-bearing target positions and counts across AR/DARP/C/N: 19,271, 19,734 and 17,725 per branch for the three seeds. Historical DARP01/02 budgets and attention FLOPs remain unmatched. Fresh AdamW follows cosine 0.001 to 0.0002 with weight decay 0.01 and clipping 1.0. All 12 final branches complete 400 updates; no interrupted tails or extra tuning occur. [D03-R §4]

Fresh evaluation

128 static worlds and 60 revision pairs are tested on 18 U/C/N endpoints: 3,384 handoff trials. Ten pairs per change category produce 50 changed-action cases and ten revision-only cases. Inputs exclude 12,464 accessible prior study hashes; task primitives recur. A common fixed held-out error probe separately gives all endpoints the same wrong drafts. [D03-R §§4, 7]

13  DARP03: complete handoffs and preparation gain

Writer / preparation

Static

Changed-plan

Macro

AR U

348/384 (90.62%)

108/150 (72.00%)

81.31%

AR C

366/384 (95.31%)

130/150 (86.67%)

90.99%

AR N

361/384 (94.01%)

128/150 (85.33%)

89.67%

DARP U

314/384 (81.77%)

82/150 (54.67%)

68.22%

DARP C

348/384 (90.62%)

115/150 (76.67%)

83.65%

DARP N

359/384 (93.49%)

128/150 (85.33%)

89.41%



Source: D03-R §6. Macro weights static and genuinely changed-revision accuracy equally, then averages parents. 384 = 128 worlds × three parents; 150 = 50 pairs × three parents. Complete correctness includes grounded fields, cross-block agreement and the fixed consumer checks.

A substantial DARP improvement

N-DARP improves by 21.19 macro percentage points over its same-panel U parent and by 5.77 points over C. The genuine erroneous content is useful to this DARP preparation beyond the matched authored control. On the same panel, static errors drop from 70 to 25 and changed-plan errors from 68 to 22. These derived counts describe this panel, not independently sampled replications. [D03-R §6; arithmetic from retained counts]

But not a clear architecture advantage

N-DARP trails N-AR by 0.260 macro percentage points. Their changed-plan totals tie, and DARP has two fewer static successes. AR C is slightly stronger than AR N; genuine-error replay is therefore not uniformly beneficial to every architecture or seed. Selecting AR C as the primary comparator afterward would violate the predeclared comparison; it remains visible as a control. [D03-R §§5–6]

Why “approaches” is more accurate than “equivalent”

Similar aggregate percentages are observations, not a statistical equivalence conclusion. The false-completion profiles and per-parent differences are unequal, and only three paired initializations were tested. The report supports a useful experimental alternative without a demonstrated reason to prefer it. It does not establish noninferiority for arbitrary tasks, a reliability guarantee or deployment readiness. [D03-R §§5–8; consolidation analysis]

14  DARP03: seed variation and revision coverage

Parent

AR static

DARP static

AR changed

DARP changed

DARP–AR macro

11101

123/128

122/128

48/50

41/50

−7.39 pp

11102

118/128

116/128

35/50

45/50

+9.22 pp

11103

120/128

121/128

45/50

42/50

−2.61 pp



DARP leads in one parent pair and trails in two. Only one DARP parent reaches the 90% macro working point, below the required two. A pooled tie in changed-plan outcomes does not establish a consistent seed-level benefit. [D03-R §§5–6]

Revision type

AR N

DARP N

Plan changes?

done

24/30

25/30

Yes

required

27/30

28/30

Yes

order

25/30

20/30

Yes

hold

23/30

27/30

Yes

known

29/30

28/30

Yes

no-op revision

29/30

29/30

No; binding changes only



Source: D03-R §6. Each row = ten unique pairs × three parents. The first five rows sum to the 150 changed-plan observations. Unlike DARP02, the panel includes action-changing order and required-flag cases.

Interpretation

DARP’s gains in hold cases coexist with worse order-change performance. The experiment does not identify why. It also does not isolate causal dependence on the generated plan: the writer can use the evidence directly, and the controller detects revisions and requests replanning. [D03-R §6]

Source revision is not model revision. These cases alter task evidence while using a fixed trained writer at evaluation. They do not test unfinished hidden-state migration across changed weights or a complete overnight adoption cycle. The plan’s proposed actions are kept distinct from actual source facts. [D02-R §8; D03-A]

Use the full revision breakdown when describing replanning. “85.33% changed-plan success” is not a guarantee of arbitrary reordering, new-rule discovery or long-horizon plan repair.

15  DARP03: editing the same errors and new errors

Writer / branch

Common wrong blocks repaired

Wrong fields before → after

AR U

216/431 (50.12%)

786 → 386

AR C

398/431 (92.34%)

786 → 55

AR N

386/431 (89.56%)

786 → 79

DARP U

45/431 (10.44%)

786 → 653

DARP C

273/431 (63.34%)

786 → 262

DARP N

391/431 (90.72%)

786 → 55



The common probe contains every wrong current block from U’s fresh confirmation first attempts, pooled within paired seeds: 154, 192 and 85 records. Every endpoint edits those same drafts with the same prior-plan contexts for at most two repairs. This removes differing error-set denominators, but tests frozen older errors—not the new writer’s present error distribution. The probe never enters training. [D03-R §7]

The improvement is real; the five-record lead is not decisive

DARP N repairs 346 more common blocks than U and 118 more than C. It repairs five more than AR N, while AR C repairs seven more than DARP N. Whole-block correction and remaining-field counts are distinct measures: AR C and DARP N leave 55 fields wrong but repair different numbers of entire blocks. [D03-R §7; arithmetic from retained counts]

Newly generated errors, N branches

AR

DARP

Static wrong blocks repaired

6/33

35/70

Changed-revision wrong blocks repaired

3/39

39/78

Static / changed false-COMPLETE handoffs

0 / 1

6 / 0



DARP repairs half of its newly generated wrong blocks in both families. That is useful, but leaves half wrong. AR and DARP now generate different errors with different difficulty; these natural-error repair rates cannot by themselves rank architectures. Complete-handoff performance remains primary. [D03-R §7]

The retained seed11101/revision1 plan changes from do1,do1,finish,pad to do1,do0,finish,pad after location feedback, and the full handoff succeeds. It is a selected example of the intended loop, not an estimate of typical success or autonomous error detection. [D03-R §7]

16  Prospective decision rule and observed cost

DARP03 froze two engineering routes to a practical win before fresh confirmation. They are decision thresholds for this implementation, not universal statistical standards. The source report and DECISION.json preserve their evaluation. [D03-P; D03-R §5; D03-D]

Requirement

Quality-win route

Observed N-DARP

Macro gain versus AR

At least +5 percentage points

−0.260 pp: fail

Parent consistency

No negative parent difference

Two negative: fail

Working point

At least 90% macro in two of three

One of three: fail

False-COMPLETE count

No higher than AR

6 versus 1: fail

Runtime allowance

At most 1.25 × AR

1.066 ×: within allowance



The efficiency route instead requires at least 20% less median time, at most one macro point of quality loss both pooled and in each parent, plus the same working-point and false-completion conditions. DARP is slower; two parents lose more than one point; the common working-point and error-count requirements also fail. Neither route passes. [D03-R §5; D03-P]

What the timing sample measures

The fixed subset is the first eight static and first four revision cases for each of three N parent pairs. Those revision cases are done-bit changes, not all revision categories. After 72 warmup episodes, 216 episodes are timed in three randomly interleaved repetitions. Median time is 9.418 ms for AR and 10.041 ms for DARP: a 1.0661 ratio, or about 6.61% slower. [D03-R §8]

Timing includes rollout, token generation, exact checks, repair and complete scoring. It excludes startup, training/collection and file publication. Four substantive fields per block and an unoptimized full-prefix AR implementation do not establish large-block, GPU or optimized-decoder throughput. No energy measurement or per-method isolated memory result supports a broader efficiency claim. [D03-R §8]

The stopping decision does not depend solely on an aggressive +5 pp threshold. The observed primary quality gap is slightly negative, performance varies by seed, false completions are more frequent, and there is no measured speed win. That supports parking this version without proving diffusion can never be useful.

17  Cross-study interpretation: what improved

1. Preparation, interface and algorithm must not be conflated

DARP01 predicted all 51 output tokens and exposed major copying and revision-interface failures. DARP02 supplies exact metadata and evaluates its U parents with the same support, then changes preparation. DARP03 uses new generated-context/error training and a different fresh panel. The sequence is not a controlled 14.58% → 80.56% → 93.49% benchmark curve. Use within-study same-panel references for numerical improvement claims. [D01-R §§5–8; D02-R §§1–5; D03-R §§4–6]

2. Teaching a workflow is different from merely permitting it

DARP01 allows revision but does not teach its old-plan input pattern. DARP02 explicitly teaches creation, repair and revision and obtains many usable revised handoffs. This supports the preparation package; it does not isolate the old-plan component’s causal effect from extra training or other changes. [D01-R §7; D02-R §§2, 4–5]

3. Correcting artificial damage is not the same as revising a persistent error

DARP02’s 187/216 authored-block repairs coexist with only 4/66 natural repairs. DARP03 then supplies frozen real drafts and matched artificial substitutes at the same locations. Its N-versus-C gain supports the importance of the actual erroneous content for this DARP preparation, while AR’s results show that it is not a universal rule. [D02-R §7; D03-R §§3, 6–7]

4. Planning and checking are not proprietary to diffusion

Both generation methods use planning, evidence, feedback, correction and commits. The final near-match therefore leaves those workflow mechanisms viable while failing to justify diffusion as a requirement. No clean broad ablation proves every workflow component independently necessary; they are retained as useful implemented candidates. [D03-R §§3, 10; consolidation analysis]

5. A few corrected tokens are not the final maintenance product

The research deliberately counts whole handoffs, cross-block agreement, actual source facts and downstream consumer checks. It also retains false-completion candidates, even when the checker prevents publication. Error-set and common-draft tests explain behavior without replacing the complete-output objective. [D01-R §§3, 5–6; D03-R §§6–7]

Synthesis: DARP became a useful supported writer and editor. The evidence favors retaining its reusable workflow and preparation lessons, not preferring the diffusion mechanism over similarly supported AR in this task.

18  Evidence limits and unanswered questions

Boundary

What the evidence does not support

Three inherited seed pairs

No broad distributional or statistical equivalence guarantee. Branches and repeated cases do not create independent models.

Closed three-operation rule

No unknown-rule reasoning, long-horizon planning or open-ended semantic maintenance.

Four content fields per block

No conclusion about long-block parallelism, variable length or learned boundary selection.

Perfect external localization

No autonomous critic qualification. Categories can strongly narrow answers; correct fields are copied.

Supplied metadata wrapper

No neural claim for JSON integrity, task IDs or source revisions in DARP02/03.

Fixed-source snapshots

No learned migration across changed weights, production durability or adversarial authentication.

Training fairness limits

DARP03 matches additional target positions, not inherited budgets, information at every location, FLOPs or optimized throughput.

HSA left parked

No end-to-end DARP + HSA + segmented-context integration measurement.

Small lexical interface

No demonstrated 25,000-token maintenance budget, summary completeness or real archive semantics.



Sources: D01-R §§2–4, 9–11; D02-R §§3–4, 8, 11–12; D03-R §§2–4, 6–10.

Validation scope

Study-reported exhaustive 512-rule checks validate the finite target/interpreter contract; they do not exhaust all generated trajectories or learned outputs. Final numerical checks sample inputs, and fresh-process replays sample episodes/sweeps. Passing them supports internal consistency at those scopes, not universal numerical admission, independent external replication or whole-system qualification. [D01-R §10; D02-R §11; D03-R §9]

What “viable” means here

Viable means an implemented, trainable, externally supported prototype can produce many useful handoffs and corrections on this fixture. It does not mean production-ready, proven safe, equally reliable or optimal. Conversely, failure to demonstrate an advantage does not mean a mathematical impossibility or that every larger segmented-diffusion design is ineffective. [D03-R §§1, 10; INTENT clarification; consolidation analysis]

19  Implications for NSS maintenance-token architecture

The project’s current maintenance direction keeps serving weights stable during active use and explores bounded learning/repair during low usage. DARP is an output-side candidate in that direction. Writing or editing a repair plan is not performing the weight repair; a source update is not a weight update; a validated toy handoff is not a full day/night cycle. [INTENT; D01-R §1; D02-R §8; D03-A]

Retain as a candidate or reference

Reason and boundary

AR maintenance writer with the same support

Current comparison reference; not automatically adopted as a deployed NSS model.

Explicit create / edit / revise interface

A practical task contract. Larger-language generality and isolated causal contribution remain open.

Exact metadata and provenance envelope

Protect administrative binding without making a tiny writer relearn IDs. Evidence selection and truth remain substantive obligations.

Checked block commits and supersession

Drafts, accepted records and actual actions remain distinct. Bookkeeping is software.

Actual-error collection and matched controls

Useful DARP preparation finding; preserve also the authored control and AR’s contrary trend.

Failure traces and paused-sweep snapshots

Diagnosable records and bounded replay support. Not adversarial authentication or model-generation migration.

DARP checkpoints and source

Retain a viable alternative for a materially different future question; no automatic next study.



Do not make diffusion a dependency of the rest of NSS

The HSA/segmented-context component stays parked for integration under its separate consolidation. Nothing in the DARP result invalidates that earlier component, and nothing qualifies the combined maintenance architecture. Removing a requirement for diffusion does not remove the plan/check/edit workflow or prevent maintenance records from being generated block by block using AR. [D03-R §10; HSA-C scope; consolidation analysis]

Meaningful future changes, not promises

Longer substantive blocks, different hardware, better preparations, alternative decoding schedules or another task could change the result; none was tested here. Those possibilities delimit the conclusion rather than justify immediate further investment. A future revisit would need a new question, comparison and prospective budget. [D03-R §§8, 10]

20  Failure ledger and internal verification

Study

Preserved failure or incident

Disposition

DARP01

Pre-lock lexical syntax error; post-result report-builder syntax error.

Fixed outside scientific outcomes; failed sources retained.

DARP01

AR 11101 caller interrupted after durable step 100.

Exact checkpoint recovery; unknown 0–100-update tail counted.

DARP01

Weak full handoffs; untaught old-plan revision interface.

Original competence/replanning failures remain; motivates DARP02.

DARP02

Three caller interruptions at durable steps 350, 500 and 450.

Exact cursors restored; up to 50 repeated unsaved updates each retained in cost bound.

DARP02

Audit “corruption” sometimes set MASK to an already-MASK token.

No-op injector bug preserved; separately hashed corrected injector passes. Main code unchanged.

DARP02

Natural procedural errors persist despite authored-fault repair.

Motivates actual-error preparation; not hidden by token-level gains.

DARP03

No main numerical stop or interruption; advantage criteria fail.

Interpretable bounded no-advantage result; park current implementation.



Study-reported check

DARP01

DARP02

DARP03

Preflight groups

14

16

10

Main records independently recounted

1,872

5,184 (+384 dev)

3,384 (+2,586 probes)

Selected complete replays

36

36

36

Selected partial-sweep resumes

12

18

18

Invalid snapshots rejected

36

54

54

Sampled numeric scalars

16,974

18,450

25,092

Sampled tolerance / argmax violations

0 / 0

0 / 0

0 / 0

Checkpoint files verified

36

48 continuations

42 including 6 parents



Sources: D01-R §10; D02-R §11; D03-R §9. These are original study-reported evaluations, not rerun for this document. Checkpoint totals include duplicate latest files and imported parents; they are not counts of distinct independently trained models.

All studies use sampled float32/float64 comparisons under 2e-5 + 2e-5 × |reference|. Scope is sampled, not full-trajectory qualification. The new consolidation audit separately checks archive bytes and hashes only; it loads no neural models. [D01-R §10; D02-R §11; D03-R §9; AUDIT]

21  Training and resource accounting

Training work

DARP01

DARP02

DARP03

Logical main optimizer applications

8,100

7,200

4,800

Actual main applications

8,100–8,200

7,200–7,350

4,800

Disposable preflight applications

12

12

6

Actual total applications

8,112–8,212

7,212–7,362

4,806

New random-initialized fits

9

0

0



Simple aggregation of the retained accounts gives 20,100 logical main applications, 20,100–20,350 actual main applications, and 20,130–20,380 including the 30 disposable applications. The interval preserves the original unknown interrupted tails. It is not an estimate of FLOPs, inference, energy or total research effort. No optimization occurred during evaluation, audit or this consolidation. [D01-R §10; D02-R §10; D03-R §4; arithmetic]

Reported measured component

DARP01

DARP02

DARP03

Completed/logical training-loop seconds

263.332

212.331

148.783

Main evaluation seconds

122.367

88.312

46.287

Other separately tracked component

Selected audit 2.289 s

Development 6.948 s

Collection 22.810 s; common probes 10.518 s

Peak recorded process RSS, bytes

356,990,976

358,191,104

358,907,904



These report-defined timings exclude substantial code development, startup, preparation, packaging and other work; some exclude discarded interrupted tails. RSS includes framework/model/data allocations and is not an isolated per-method peak. The studies do not measure energy or a real maintenance night. Do not sum unlike timing components into an asserted end-to-end performance number. [D01-R §9; D02-R §10; D03-R §8]

Evidence volume and repeated outcomes

The original main episode counts sum to 10,440, with 384 DARP02 development records and 2,586 DARP03 common-probe records separately. These include shared worlds, policies, branches, revisions and ablations—not 13,410 independent tests of general intelligence. Preserve each study’s denominator and outcome unit when reusing a result. [D01-R §4; D02-R §4; D03-R §§4, 7; arithmetic]

The three original full ZIPs total 109,142,462 bytes. Their 11,303 declared payloads were checked during this documentary consolidation. Archives are indexed, not merged or modified by this document. [AUDIT]

22  Implemented tests and evidence entry points

Paths below are relative to the original study archive’s top-level directory, NSS_NBR02_DARP0N_Execution_v0.1/. They identify the actual retained tests and evidence. This index was checked by reading source text/AST without importing or executing experiment code. [AUDIT]

Study / source

Tests and role

DARP01 source/core.py; source/run.py

Tokenizer, task/targets, writer, sampling/checking; fixed training, evaluation, commits and recorded attempts.

DARP01 source/preflight.py

truth, fault_fields, malformed, stale, unsupported, contradictory, gradient, causal, memory_nonleak, float_reference, attention, sampling, hardcopy.

DARP01 source/audit.py

independent expected records; recount; envelope/verify/resume; replay_one; checkpoint lineage.

DARP02 source/core02.py; source/run02.py

Shared wrapper, feedback policies and revision context; P/R training and full output rollouts.

DARP02 source/preflight02.py

Rule truth; wrapper independence; field/metadata faults; simulator; categories; paired batches; revision preparation; causal/gradient/numeric/attention/copy/snapshot isolation.

DARP02 source/audit02.py

Independent interpretation/aggregation; full recount; selected replay and snapshot-fault testing.

DARP03 source/study03.py

Fresh collection; actual/authored matched training; frozen schedules; endpoint evaluation and source-bound records.

DARP03 source/preflight03.py

512-rule agreement; metadata isolation; no replacement targets; paired contexts/masks/budgets; causal/numeric tests; partial resume/faults; optimizer restoration.

DARP03 source/analysis03.py

metrics/summarize; common_pool/probes; benchmark; audit, independent recount and fresh replays.



Read results before rerunning anything

Each archive contains REPORT.md, ARCHITECTURE.md, protocol/PROTOCOL.md, README.md and MANIFEST.json. Results, fixtures, checkpoint and failure directories preserve the scientific record. Verification of hashes is not a model evaluation. Audit/replay/training commands can load models, write files or run inference; the original READMEs specify their boundaries. Use a separate extracted copy for any later authorized reproduction, never overwrite the published evidence. [D01/02/03-X README; AUDIT]

23  Source register and documentary verification

All scientific findings in this report are source-derived from the supplied DARP studies. Bracketed labels are stable local citations. Section labels refer to each original report/protocol, not file-tool line numbers. The current conversation supplies design intent and the final clarification of “viable alternative, no clear advantage.” No outside research was added to fill gaps. [INTENT]

Label

Exact locator / purpose

D01-R / D01-A / D01-P

NSS_NBR02_DARP01_Execution_v0.1.zip::REPORT.md / ARCHITECTURE.md / protocol/PROTOCOL.md

D02-R / D02-A / D02-P

NSS_NBR02_DARP02_Execution_v0.1.zip::REPORT.md / ARCHITECTURE.md / protocol/PROTOCOL.md

D03-R / D03-A / D03-P

NSS_NBR02_DARP03_Execution_v0.1.zip::REPORT.md / ARCHITECTURE.md / protocol/PROTOCOL.md

D03-D

DARP03 archive::results/DECISION.json; prospective practical-decision evaluation.

D01-X / D02-X / D03-X

Corresponding full execution ZIP; source, data, models, raw records, failures and checks.

D01-V / D02-V / D03-V

Corresponding NSS_NBR02_DARP0N_Delivery_v0.1.json supplied alongside each ZIP.

HSA-C

NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.md; separate scope/parking context, no DARP integration evidence.

INTENT

Owner’s DARP clarification, test authorizations and latest viable-alternative/parking discussion in this conversation.

AUDIT

New documentary source-integrity audit, summarized below and retained in the companion verification JSON. No model/scorer execution.



Fresh file checks performed for this document

The three full ZIP byte sizes and SHA-256 hashes match their supplied delivery receipts. ZIP CRC checks pass; all 11,303 declared payload sizes/hashes match; there are no missing, extra or duplicate regular members. The six standalone report/architecture Markdown files match both their archived copies and declared hashes. This is integrity, not authenticity against a malicious publisher or independent scientific replication. [AUDIT]

Archive

Bytes

Declared payloads

DARP01

28,490,097

1,996

DARP02

47,021,317

5,774

DARP03

33,631,048

3,533



No original archive was combined, overwritten or scientifically rerun. The companion Markdown carries the same consolidated content as this document. Machine-readable source hashes are supplied separately rather than presented as claims of new model qualification.

24  Decision record and handoff

Disposition: PARK_CURRENT_DARP_IMPLEMENTATION. Keep AR as the current supported maintenance-writer reference. Retain the DARP implementation and evidence as a viable experimental alternative, not a preferred mechanism or a disproven general idea.

Basis for the decision

The last preparation materially improved DARP’s editing and complete-handoff quality, approaching supported AR. Yet its primary macro score is slightly lower, two parent comparisons are negative, false-completion handoffs are more frequent, and the limited timing sample is slower. Neither prospective practical-win route passes. Technical checks passed at their stated scope, so this is not an unresolved numerical-stop decision. [D03-R §§5–10; D03-D]

What remains worth using

Preserve creation/edit/revision interfaces, exact metadata/provenance binding, explicit draft-versus-commit semantics, check-informed edits, source-revision supersession, bounded restart records, and real-error collection with strong controls. These can be used with an autoregressive writer. Their preservation is not a claim that each has separately proved a general benefit or that a toy exact checker transfers to open-ended NSS tasks. [D02-R §12; D03-R §10]

What is not decided

No universal ranking of autoregression and diffusion is established. No equivalence, deployment, autonomous verification, long-block throughput, 25,000-token operating point, identity continuity or complete night-maintenance qualification follows. HSA/segmented context remains separately parked. An alternative decoder or materially different task/hardware would require its own evidence. [D03-R §§2, 8, 10]

Continuation instructions

Do not launch DARP04, integrate with HSA, train another writer or change a gate on the strength of this consolidation. Keep all source studies and their outcome labels intact. When citing gains, use same-panel U/C/N comparisons and retain the wrapper, checker, denominator and cost boundaries. Reuse failure cases only under declared development/training status with fresh confirmation for any later experiment. [D03-P; D03-R §10]

Paste-ready research handoff

DARP01–03 are consolidated. The plan/check/edit/commit workflow is retained, but the tested four-step segmented-diffusion writer has no clear practical advantage over equally supported AR. DARP03 N scores: static 359/384 vs AR 361/384; changed plans 128/150 each; common erroneous blocks repaired 391/431 vs 386/431; median sampled runtime 10.041 vs 9.418 ms; primary false-COMPLETE handoffs 6 vs 1. Park this implementation, preserve all evidence, and do not interpret the result as a universal disproof or equivalence finding. No further execution is authorized by this document.