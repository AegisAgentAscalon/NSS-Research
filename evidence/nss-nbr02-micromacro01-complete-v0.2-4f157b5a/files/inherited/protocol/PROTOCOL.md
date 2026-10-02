# NSS-NBR02-TIMING01 — fixed-work early versus late rehearsal
## Scientific protocol v0.1 / execution v0.1; prospectively locked under current user authorization

Selected candidate: CAND-NBR02-REPLAY-TIMING-001 from the post-REHEARSE retained-data analysis.
This is one new study, not a reopening of any failed gate. No CONTINUATION-MIX or CONFIDENCE-CAP arm.
Concrete choices below complete the candidate's previously unresolved admission/work items. They are
reviewer choices fixed before any newly generated task, model operation or score. No second Codex
review is required by the user-authorized workflow. No historical model is an initialization.

## Mechanism and observations
Retain the DC01/REHEARSE 674-parameter dense tanh model (H16,D23, two logits), all five adaptive
float32 tensors, eta1 SGD, global norm clipping1 except first authenticated changed label at clip2 for
U/E/LATE. G uses exact reverse-mode gradients; L uses its unchanged diagonal-local sensitivities for
all examples including replay. Forward prefix START22, PRIME20+scope, CUE0..19 from zero state.
Parameter order W16x23,U16x16,b16,V2x16,a2. Zero temporary state after receipt; learned weights persist
within the condition. Exact formulas/implementation boundary recorded in copied source identities.
The ordinary writer/detector, fixed complete old buffer, task scope and valid receipt identity remain
supplied software. This is not learned memory selection, dream maintenance, unbuffered skill retention,
plasticity restoration, or a long-lived cumulative learner.

Each condition uses f,p,f,f,p,f, with p an old cue of the other scope. The first two updates are shared.
At the first public validated label disagreement, before applying the update, clone state into B1,U,E,LATE.
B1 keeps clip1; the other three use clip2. Later real receipts use clip1 everywhere.
E applies exactly one old-record batch after that correction. LATE applies exactly one after the next
VALID NEW receipt for the same cue/scope and same changed label. The worker—not the scorer—tracks this
from public receipt fields, not trial index or correctness. Intervening unrelated receipts do not trigger
replay. A repeated consumed receipt is rejected; another contradictory focal label before the promised
follow-up stops as EXPECTED_FOLLOWUP_CHANGED_AGAIN, with evidence. In the declared main grammar the
follow-up is present at trial4. A missing follow-up in the pure-policy fixture leaves the slot unspent;
no batch is moved elsewhere or counted as performed. No score-driven trigger/retry/rollback.

Both timing branches revisit the same eight lawful current old records in coordinate order0..7. Their
labels, source receipts and release chronology match exactly; gradients are recomputed at each branch's
own batch-entry state. Each example resets h; all8 raw float32 gradients are captured before any mutation,
serially summed in float64 from +0, divided8, cast once32, clipped once1 and applied once. No individual
clipping or sequential per-example optimizer steps. Batch use is a new REHEARSAL application, not another
environment receipt. Cost each fetch and derivative. No focal-repeat arm is included. E/LATE equal
extra examples/applications, not equal step norms or wall runtime; B1/U are deliberately cheaper.

## Data and initialization
Eight fresh initial fits G/L x4 paired seeds,100 updates each on8 balanced old associations. W uniform
+-sqrt(6/39),U uniform+-.05 plus.25I,b0,V uniform+-.02,a0 in fixed PCG64 row order, cast32. Twelve random
cycles of8 plus first4 of a thirteenth give the100 initial examples. Four development focal cues8..11,
eight heldout12..19, two scopes; within-scope label balance is fixed. Old coords0..3 scope0,4..7scope1;
focal8,9 and12..15scope0,10,11and16..19scope1. Protected cues bybase[4,5,0,1,4,5,6,7,0,1,2,3].
New 33 direct seeds derive first8 SHA256 bytes bigendian from ASCII NSS-NBR02-TIMING01-v0.1/{label}.
No stimulus drawn before source lock. All datasets and fits remain, no favorable seed search. Old and
small binary-grammar overlap is explicitly allowed and audited; new IDs do not mean unseen tasks.
Heldout labels generated only after prospective A0/calibration/source/checkpoint lock.
All ordinary main delays0. Fixture crosses0/8/32 using inherited detached filler contract.

## A0: basic competence, separate from speed and relative scores
Per fit require: initial old8/8; original B1 mixed development>=16/20; all4 focal acquisitions correct
after first teaching receipt; all4 reversals recovered after TWO corrective receipts (trial4); all4 final
focal answers correct (trial6). EACH G/L group needs>=3/4 qualifying fits; retain all4 if group passes.
Failure is ELEMENTARY_ACQUISITION_RECOVERY_DEFICIT, stop before heldout, replay completed prefix.
Justification: a viable baseline must demonstrate the elementary task with bounded extra feedback;
first-correction speed is the intervention's question, not a prerequisite that assumes its solution.
These are pragmatic small-task floors, not statistical confidence bounds. Own frozen N remains strong,
with mixed/focal counts and normalized gain fully reported; relative gain is not an admission gate.
No prior results relabelled. This prospective change is informed by known analysis, not independently
validated by it. Existing REHEARSE STOPPED_AT_A0 remains frozen.

Only B1 development calibrates confidence: absolute mean8-old change from common trial2 at trials3/4,
all4bases x4fits, medians q. tau_loss=min(.01,max(.002,q_loss)); tau_margin=min(.02,max(.005,q_margin)).
Lock before heldout; E/LATE/U scores cannot change tolerances or data. No checkpoint/model selection.

## Shared scoring grid and decisions
Score original before-feedback predictions separately. Read focal+all8old after EVERY real update and
after each extra batch. Common grid: T3_PRE_EXTRA,T3_POST_EXTRA,T4_PRE_EXTRA,T4_POST_EXTRA,T5,T6.
For no-extra branches the same saved post-real inventory is reused at aligned POST_EXTRA; mark its
source frame and reuse. Reuse is not another model call/sample. LATE cannot delay its first score.
Pre-fork old reference is common trial2. All raw class/loss/logit/probability margins retained.
N_G/N_L no-learning paths and causal exact last-label X remain; exact targets only from released labels.

For EACH E/LATE and learner, a FULL_TRAJECTORY screen requires:
1) At T3_POST_EXTRA gain at least1 class overB1 in>=3/4fits and positive in>=6/8bases, pooled focal loss
   no worse; no paired first-correction class regression where U correct.
2) Every old class correct at prefork remains correct at ALL SIX boundaries, no extra error versusB1.
3) Every base/boundary mean(old loss)-B1<=tau_loss and B1-minus-mean(prob margin)<=tau_margin, plus each
   pooled boundary. Later recovery never erases early failure. Report each loss/guard failure separately.
4) No paired focal class loss versusU at any common boundary.
If B1 is saturated, the efficacy improvement claim may fail without implying incompetence.
Timing E/LATE contrasts (perfit/base, final loss, worst sampled excursion, discrete boundary counts,
post-next-update tail) are predeclared DESCRIPTIVE/EXPLORATORY, not a new significance or superiority
threshold. A later improvement with earlier harm is a trade-off, not a pass. Worst/discrete averages
are schedule metrics, not elapsed-time damage. No hidden delay-based scoring window or removal of fits.

## Engineering and costs
Same-prestate fork equality; own exact/local gradient math; immutable public receipt/trace; independent
NumPy same-source reconstruction; ordered mean/cast/clip/application; early/late public timing tests;
identical retained old source lists; pending/missing/conflicting/rejected feedback; read-only probes;
no hidden task score in worker. Numerical tolerance2e-6+2e-5abs(reference) remains empirical, not proved.
All actual stored application bytes separately checked. Natural poor scores complete admitted evaluation;
engineering/resource failures stop incomplete. Preserve errors, all attempted updates and unknown
completions. Eight bad-sign/double sandbox batches perpass never enter scientific weights.
Full fresh adaptive replay repeats completed updates/initial fits from empty state, no retained-output
substitution. Independent scoring imports no model/driver/controller. Replay is not another sample.

Eight initialfits800 +96 contexts20=1920 +100fixed costupdates +240cleanfixture +8sandbox =3068/pass;
capture+freshreplay6136. ALL-ATTEMPT CAPS7000updates,260000cells,80000heads,6000G backwards,6000local
example gradients,4800fetches; per-pass halfcaps. No unused historical budget transfer. Full schedule
independently enumerated inWORK_LEDGER.json including reconstruction, inventories, probes/derivatives.
Two-hour shared clock starts with current first shell check including implementation. CPUone thread,
3GiBprocess-tree/3.5GiBcontainer abort,256MiBnew encoded retained evidence,64MiBsingleZIP; actual host
must pass fixed probe forecast. Per-kind numeric ceilings and measured headers/compression, not copied
209MiB proof. Forecasts empirical; actual caps monitored. Native/backing memory gap remains open; no
whole-memory efficiency claim. Retain all40main checkpoints0,25,50,75,100 plus other checkpointrecords,
all gradients/prepost weights, input/RNG/cursor identities, states/logits/costs, raw truth separately,
source/seed locks, chronological flags, faults, full adaptive replay and relocated no-model re-scoring.

## Scope disposition
NBR01 bounded closure unchanged; NBR02 active. Historical failed gates/screens unchanged. Workspace
RET-MW01-FIT-001 parked, dream RET-DREAM-MAINT-001 deferred, OBS-DC01-COST-001 open. FCR0103 return
beforeNBR04 preserved. No skipped NBR01 study dispatched; identify the specific ticket before return.
The user-supplied self-play paper is a deferred literature item, no synthetic curriculum or third core
implemented here. Parent architecture ledger not overwritten. G01-G22 carried verbatim.
