from pathlib import Path
import sys,json,statistics
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from nbr01_empty.util import write_json
s=json.loads((ROOT/'SUMMARY.json').read_text());r=json.loads((ROOT/'evidence/RESOURCE_ACCOUNTING.json').read_text())
labels={'hold':'Hold + original reader','historical':'Original recurrent maintenance','replay':'Broader rehearsal + code anchors','contract':'Same preparation + empty contraction objective',
'presence_historical':'Original recurrence + dynamic protected presence','presence_contract':'Revised recurrence + dynamic protected presence','local_empty':'Frozen original + fitted local empty gain','nearest':'Nearest-prototype maintenance'}
def f(v):return f"{100*v['mean']:.2f} ± {100*v['sample_std']:.2f}%"
def table(name,columns=('known_accuracy','unknown_accuracy','all_read_stream_success')):
 lines=['| Mechanism | '+ ' | '.join({'known_accuracy':'Known at endpoint','unknown_accuracy':'UNKNOWN at endpoint','all_read_stream_success':'Every read correct, entire stream'}[c] for c in columns)+' |', '|---|'+ '---:|'*len(columns)]
 for mode in labels:
  row=s['tables'][name][mode];lines.append('| '+labels[mode]+' | '+' | '.join(f(row[c]) for c in columns)+' |')
 return '\n'.join(lines)
crit=['| Mechanism | Clean lifecycle | Joint nominal-noise lifecycle | Extended 4,096-round screen |','|---|---:|---:|---:|']
for m,l in labels.items():
 x=s['criteria'][m];crit.append(f"| {l} | {x['clean_pass']}/5 | {x['nominal_joint_pass']}/5 | {x['extended_pass']}/5 |")
atten=['| Mechanism | 25% of intended vector delivered | 50% delivered | Full code delivered |','|---|---:|---:|---:|']
for m in ['historical','replay','contract','local_empty','presence_historical','nearest']:
 x=s['attenuated'][m]['empty'];atten.append('| '+labels[m]+' | '+' | '.join(f(x[v]) for v in ('0.25','0.5','1.0'))+' |')
resource=['| Mechanism | Raw state/stream | Additional serving weights | Median maintenance+read, batch64 |','|---|---:|---:|---:|']
for x in r['modes']:resource.append(f"| {labels[x['mode']]} | {x['raw_state_bytes_per_stream']} B | {x['extra_repair_weight_bytes']} B | {1e6*x['maintenance_and_read_seconds_median']:.1f} µs |")
report=f'''# NSS NBR-01 / WritableEmpty004
## Stable absence, legitimate writes, corrections and reuse

**Standalone research package v0.1 · main study RUN · full NBR-01 OPEN**

This is an extension of StateRecovery003, not an architecture replacement,
a cumulative foundation release, a four-core deployment, or a biological
simulation. Place it beside the earlier studies in `MegaMind_Alpha_Proto`.
Do not merge directories. The seven supplied ZIP archives and the foundation
are preserved unchanged; see the preservation and foundation receipts.

## Decision brief

**An empty record can remain protected and still accept new data.** In this
controlled environment, dynamic presence plus the original recurrent content
maintenance passed the clean, noisy lifecycle and extended screens in all five
pairs. The nearest-prototype control also passed all five and was stronger on
some stresses.

The proposed native neural changes improved empty-state behavior, but did not
produce a uniformly superior memory. Broader preparation—with or without an
additional empty-contraction loss—stabilized the empty region while weakening
long-run retention of some established values. Only one of five pairs in each
arm passed the full nominal-noise lifecycle. A highly localized, one-scalar
empty-region modification was worse than anticipated and failed even the clean
long-maintenance screen in three of five pairs. Those failures remain in every
aggregate and in the package.

**Keep the dynamic presence mechanism as an engineering reference/control;
keep native state research open. Do not adopt the revised neural maps as a
replacement for the original content-maintenance model on these results.**

## 1. What was prepared and what was held fixed

The five frozen16D code/readout representations (301–305) are reused from
HorizonBinding002. Their five original2,128-parameter recurrent repair networks
are reused from StateRecovery003 (learning seeds501–505). These are learned
finite-code representations, not language-capable Primary checkpoints.

We completed15 new fits with learning seeds601–605: five rehearsal continuations,
five otherwise identical continuations with an empty contraction objective, and
five one-parameter fits of a local empty-region gain. Each fit took1,800 AdamW
steps. This totals **{r['main_optimizer_steps']:,} completed optimizer steps**,
**{r['main_sequence_presentations']:,} sequence presentations** and
**{r['main_supervised_event_presentations']:,} supervised within-sequence event
presentations**. Examples are reused between arms. These are not independent
observations from millions of people or environments.

There are ten new full repair-network revisions and five single-scalar fits,
not15 newly trained language models. The local arm stores the unchanged parent
network plus its learned radius. Its extra parameter does not erase the parent's
training/storage costs. For each paired seed, all three arms receive identical
random inputs, labels, direct target codes and optimizer-step budgets. Their
trainable parameter sets, objectives, learning rates and computation are NOT
identical. No wall-time- or FLOP-matched architecture ranking is claimed.

Evaluation holds all weights fixed. Four addresses, eight known values and
EMPTY/UNKNOWN are supplied. Clean qualification is the explicit rule
score≥0.5 with matching scope. A qualifying write installs the full learned
code; a clear resets the designated record. The prior source's learned input
gate remains bypassed. This is **not** an unchanged end-to-end evaluation of
HorizonBinding002 and does not learn which natural-language observations should
be remembered.

## 2. Candidate mechanisms

**Original:** the same recurrent residual map as StateRecovery003,
F(z)=0.5z+0.5[N(z)−N(0)], including the existing exact-zero guard. That guard
protects exactly zero; it does not stabilize a neighborhood by itself.

**Broader rehearsal:** continue the parent using approximately half empty starts,
Gaussian initial disturbance up to0.5, fresh per-round noise up to0.15, random
qualified writes and clears, and1/2/4/8/16-round sequences. The objective combines
code reconstruction, the frozen answer head, and exact-code fixed-point
rehearsal. The eight known prototypes and empty target are directly supplied.

**Empty-contraction arm:** identical preparation plus sampled directional
penalties when ||F(ε)||²/||ε||² exceeds0.64 around the empty origin. This is a
sampled local loss, not a proof of contraction throughout the state space.

**Local empty-region arm:** retain the parent network and fit only a positive
radius r. The map becomes [1−exp(−||z||²/r²)]F_parent(z). It introduces no
presence field or hidden event history. It DOES exploit the declared EMPTY=0
coordinate convention and normalized code scale. A locally protective gain can
still disrupt established attractors.

**Dynamic presence controls:** retain one protected boolean per record. A
qualifying write changes content and presence together; a clear resets both.
Ordinary maintenance clamps only currently empty records to zero. A new write
sets presence before the next maintenance guard, so an old empty status does
not erase it. These controls add4raw bytes/stream and receive protection from
vector corruption. They are not a learned solution or a permission authority.
The implementation is one synchronous research state operation, not a claimed
production database transaction or power-loss durability guarantee.

**Nearest prototype:** project onto the closest of the supplied nine codes,
then use the same readout. The finite catalogue is strong supplied structure,
shared with the learning arms. It is not an uncounted general reasoning engine.

## 3. Full lifecycle, not merely a final recall query

Each paired mechanism receives64four-address streams. Two neighboring records
start populated; the focus record and another address start empty. The focus
record follows:

**Empty → first write → correction → clear → rewrite.**

Each of the five phases contains1,024fresh vector-noise rounds, for5,120rounds
per stream before the final global-clear check. Noise standard deviations are
0,0.15 and0.30 in RMS-normalized representation coordinates. The training
maximum for fresh repeated noise was0.15;0.30 is an extrapolation stress.

The controller reads every round. Recorded checkpoints are0/1/16/64/256/1,024.
A separate cumulative metric requires every answer at every read, over all four
addresses, to be correct. A transient false answer cannot be hidden by a correct
endpoint. Low-score0.4999 payloads and wrong-scope score1 payloads are rejected;
legitimate0.5001 writes are accepted. Their scores are not multiplied into code
amplitude: these test exact event semantics, not weak analog-signal decoding.

An extended condition starts with4,096fresh0.15-noise rounds, then supplies a
legitimate first write and256further rounds. State-shock, attenuated-write,
metadata-fault and local-dynamics conditions are separately scored. The complete
main output contains **{s['metric_rows']:,} result rows** and
**{s['saved_answer_evaluations']:,} saved answer evaluations**. Many measurements
reuse streams, assignments and trajectories; five paired seeds, not this large
row count, define the replication level.

## 4. Main nominal-noise result

At the end of the rewritten phase under0.15repeated noise, means±sample standard
deviations across all five pairs are:

{table('nominal_final_1024')}

The dynamic-presence/original-recurrence control has100% known and UNKNOWN
accuracy at every recorded phase endpoint. However, its99.6875% every-read
stream result means **319/320streams** were correct at every intermediate read;
one stream had at least one transient error. Do NOT summarize that as flawless
all-time behavior. Its protected empty records remained empty; the transient
error affected a populated record. Nearest-prototype maintenance was100% on the
entire nominal trajectory in all five pairs.

The revised neural candidate was writable: complete legitimate first writes,
corrections and rewrites were accepted immediately. Its difficulty was retaining
all established records reliably afterward. At the final endpoint, contraction
achieved94.17% known recall versus100% for the original, while correcting the
original's0% UNKNOWN endpoint behavior to100%. This is a meaningful tradeoff,
not a blanket improvement.

The broader-rehearsal control already achieved100% UNKNOWN endpoints. Adding the
empty-specific contraction objective improved some means but did not change the
1/5joint-pass count. The success cannot be attributed exclusively to that extra
loss; balanced teaching, chronic-noise exposure, variable depth and fixed-point
rehearsal were changed together relative to the historical parent.

## 5. Registered joint screens

A nominal pass requires every phase's known/UNKNOWN endpoint≥95%, immediate
legitimate writes≥95%, and≥95%streams correct at EVERY read. Clean and extended
screens are specified separately in spec/protocol.json. No failed seed is
excluded from scoring.

{chr(10).join(crit)}

The local empty-region arm is not a competent alternative on this screen. Its
later noise/shock scores remain visible, but do not turn its failed clean
baseline into an accepted candidate.

After4,096noise rounds before the first write:

{table('extended_4096')}

The protected-presence and nearest controls remained writable after that long
empty interval. This directly addresses the user's requirement: protected
absence must not become a permanently locked slot.

## 6. Why local stability is not enough

Finite-difference measurements atε=0.001give the old empty state's largest
local eigenvalue magnitude as1.045–1.524, above1in all five parents. The revised
contraction maps give0.118–0.404; the rehearsal-only maps also lie below1.
The local gain makes the empty-origin derivative numerically close to zero.

Those are genuine changes in the local dynamics, not merely external clamping.
They do not imply immunity to finite noise, preservation of all neighboring
attractors, or correctness of every decoded answer. The recorded known fixed
points can also be locally restoring while some trajectories still fail over
thousands of disturbances. This distinguishes local behavior from the full
noisy, writable lifecycle.

The local-gain arm illustrates the risk sharply: making the origin extremely
restoring did not ensure competent retention of known values, and its clean
long-horizon baseline failed in3/5pairs. No claim of a global theorem or a
faithful human/fly circuit follows from these finite-state experiments.

## 7. Writing must deliver the intended representation

The main lifecycle uses complete, explicitly qualified writes. A separate
registered stress weakens the delivered vector AFTER admission. It blends only
part of the new code into an empty or previously populated state; the presence
controls are correctly informed that a write occurred. This is a payload-delivery
fault, not a low qualification score and not an ambiguous-evidence learner.

For empty→value after16maintenance rounds:

{chr(10).join(atten)}

The revised contraction map accepted full codes, but a half-delivered code was
usually pulled back toward empty. The exact presence flag alone could not
reconstruct the missing value. Protection and writing should therefore be
separate operations, with the writer responsible for delivering an adequate
representation. The test does not establish a learned incremental writer or an
ability to reconstruct arbitrary partially erased information.

## 8. Stronger faults and imperfect metadata

At0.30noise, the final known-record accuracy was65.94% for original recurrence
with protected presence. Its UNKNOWN accuracy remained100%; the flags protected
existence, not the stored content. The revised contraction arm fell to5.83%
known with98.75%UNKNOWN. Nearest-prototype maintenance remained100%/100% in this
finite-code chronic condition. These stresses are retained, not screened out.

For a one-time Gaussian shock of1.0and four repair rounds:

{table('shock1_round4',('known_accuracy','unknown_accuracy'))}

The catalogue control is not infallible either: sufficiently large one-shot
noise can move a vector closer to a different code. Its UNKNOWN shock score is
82.66%, not100%. These mechanisms do not manufacture lost evidence.

Explicitly flipped presence fields demonstrate the protection assumption:
marking a populated address absent suppresses its content; marking an empty
address present removes its empty clamp. Subsequent valid write/clear events
can repair the corresponding status. The flags are not truth, evidence quality,
authority, or an automatically fault-tolerant storage scheme. See the complete
metadata_fault rows and saved arrays for every case.

## 9. Resources and preparation cost

{chr(10).join(resource)}

Every mode additionally uses the shared4,072-byte code/readout representation.
Raw state excludes scope/revision records, Python/tensor objects, checkpoints,
RNG, transient buffers and process overhead. The presence field is four boolean
BYTES per stream, not a claim of four packed bits. Everything here isfloat32
except explicit discrete metadata. No low-bit eligibility state was studied.

Completed main training loops totalled{r['main_training_seconds']:.2f}s on the
sandbox CPU. Sampled process RSS reached{r['sampled_training_process_peak_rss_bytes']/2**20:.2f}MiB;
10ms sampling can miss short peaks. The microbenchmarks above are descriptive
medians of five200-iteration runs at batch64, not a controlled user-PC benchmark,
energy result, or quality-matched architecture frontier. Host CPU work may overlap.
The inherited representations and original repairs were not retrained and are
not free. Exact historical preparation receipts are supplied in reference/.

Seven development fits total9,900steps and are reported separately, including
unsuccessful from-scratch and neighborhood-loss trials. One infrastructure
timeout interrupted the first local_empty301fit after its last logged step900;
no final checkpoint existed. The same seed/recipe was restarted from its parent,
not replaced by a favorable seed. Its uncompleted compute is not included in the
27,000completed-step total; the exact final interrupted step was not recorded.

## 10. Reproducibility and delivery evidence

The registered scientific core hashes are locked before main training/scoring.
All15new checkpoint identities, paired data digests, preserved local-parent
weights, source targets and scores are checked. The full fresh-interpreter
replay compares every row and saved prediction array, not just selected averages.
Its final status is recorded in evidence/INDEPENDENT_VERIFICATION.json.

One full1,800-step contract303trajectory is reproduced from the parent with the
same input digest, final tensor identity and safetensors checksum. Eighty actual
state/RNG snapshots (eight mechanisms×five pairs×two lifecycle cut points)
restore and continue identically in another interpreter, including dynamic
presence. These are internal reproducibility checks, not extra independent
training seeds or external replication.

**44research unit tests** cover writes, clears, neighbors, scope, invalid inputs,
read purity, state size, code0versusEMPTY, checksum/schema/weight compatibility,
and data-only snapshots. The unchanged foundation passes its68tests, dependency
check and974-file manifest before/after execution. The full historical1,111-test
suite, Windows execution, target-device budget and production qualification are
NOT_RUN. ZIP-level extraction and integrity results are supplied separately.

## 11. Engineering decision

**Keep:** the original content-maintenance model plus dynamic, explicit existence
state as the strongest tested engineering reference for this lifecycle. Keep the
nearest-prototype control because it is a strong competitor in this task.
Do not confuse a reliable protected metadata field with a universal learned
solution.

**Revise rather than adopt:** the broad neural empty-region training. It provides
actual local stability and writable emptiness, but damages enough established
retention to fail the joint criterion in most seeds. Empty contraction is not a
standalone success metric.

**Do not promote:** this fitted radial empty-gain candidate. It failed clean
retention in three pairs despite a locally stable origin. Its tiny parameter
count does not compensate for lost function.

A next native candidate can explicitly separate learned existence representation
from content dynamics, compared with the protected field, at a declared state
budget. Alternatively, give absence a distinct trained code instead of forcing
it into the center of a content space, with an explicitly versioned readout/reset
contract. These are next proposals, NOT_RUN and not accepted redesigns. Preserve
write/correction agility and full-lifecycle checks while testing them.

No new core is needed for these experiments. The Primary/Secondary/Tertiary/
advisory-Validator roles, S/T alternation, exact evidence, source provenance,
no-overlay direction and independent Forge/Runtime boundaries remain unchanged.
This package does not implement learned qualification, general binding, rich
uncertain beliefs, hard recurrent reasoning, delayed credit, low-bit learning,
biological fidelity, personality continuity or an integrated companion.

**Bottom line:** stable emptiness and legitimate writing are compatible. The
best engineering control demonstrated both; the tested native neural revisions
have not yet preserved the full combination as reliably.

## Evidence index

- Protocol/chronology: spec/protocol.json, spec/REGISTRATION.json,
  spec/DEVELOPMENT_FINDINGS.md; historical source reports in reference/.
- New training: evidence/main; preserved development and incomplete attempt:
  evidence/development and evidence/interrupted.
- All main rows/predictions: evidence/results; five-seed summaries: SUMMARY.json.
- Complete replay: evidence/INDEPENDENT_VERIFICATION.json; full learning replay:
  evidence/TRAINING_REPRODUCTION.json.
- Resumable state: evidence/snapshots, RESUME_EXPECTATIONS.json and
  RESUME_VERIFICATION.json.
- Resources, foundation and source preservation: evidence/RESOURCE_ACCOUNTING.json,
  FOUNDATION_REGRESSION.json and INPUT_PRESERVATION.json.
- Integrity: MANIFEST.sha256 and the external DELIVERY_VERIFICATION.json receipt.
'''
# Add spaces in a few readability-sensitive numeric phrases without touching code.
for a,b in [('five16D','five 16D'),('frozen16D','frozen 16D'),('64four','64 four'),('256four','256 four'),('15new','15 new'),('44research','44 research'),('68tests','68 tests'),('974-file','974-file'),('five200','five 200')]:report=report.replace(a,b)
for old,new in {'original2,128': 'original 2,128', 'completed15': 'completed 15', 'seeds501': 'seeds 501', 'seeds601': 'seeds 601', 'took1,800': 'took 1,800', 'not15': 'not 15', 'up to0.': 'up to 0.', 'and1/2': 'and 1/2', 'exceeds0.64': 'exceeds 0.64', 'add4raw': 'add 4 raw', 'receives64': 'receives 64', 'contains1,024fresh': 'contains 1,024 fresh', 'for5,120rounds': 'for 5,120 rounds', 'are\n0,0.15': 'are\n0, 0.15', 'and0.30': 'and 0.30', 'was0.15': 'was 0.15', '0.30 is': '0.30 is', 'score1 payloads': 'score 1 payloads', 'legitimate0.5001': 'legitimate 0.5001', 'with4,096fresh0.15': 'with 4,096 fresh 0.15', 'and256further': 'and 256 further', 'under0.15repeated': 'under 0.15 repeated', 'has100%': 'has 100%', 'its99.6875%': 'its 99.6875%', '319/320streams': '319/320 streams', 'was100%': 'was 100%', 'achieved94.17%': 'achieved 94.17%', 'versus100%': 'versus 100%', "original's0%": "original's 0%", 'to100%': 'to 100%', 'achieved100%': 'achieved 100%', '1/5joint': '1/5 joint', 'After4,096noise': 'After 4,096 noise', '0.001give': '0.001 give', 'as1.045': 'as 1.045', 'above1in': 'above 1 in', 'give0.118': 'give 0.118', 'below1.': 'below 1.', 'in3/5pairs': 'in 3/5 pairs', 'after16maintenance': 'after 16 maintenance', 'At0.30noise': 'At 0.30 noise', 'was65.94%': 'was 65.94%', 'remained100%': 'remained 100%', 'to5.83%': 'to 5.83%', 'with98.75%': 'with 98.75%', 'not100%': 'not 100%', 'of1.0and': 'of 1.0 and', 'shared4,072': 'shared 4,072', 'isfloat32': 'is float32', 'totalled150.25s': 'totalled 150.25 s', 'reached315.60MiB': 'reached 315.60 MiB', '10ms': '10 ms', 'batch64': 'batch 64', 'total9,900steps': 'total 9,900 steps', 'local_empty301fit': 'local_empty fit for representation 301', 'step900': 'step 900', '27,000completed': '27,000 completed', 'All15': 'All 15', 'full1,800': 'full 1,800', 'contract303trajectory': 'contract trajectory for representation 303', 'code0versusEMPTY': 'code 0 versus EMPTY', 'its68tests': 'its 68 tests', 'its68 tests': 'its 68 tests', 'and974-file': 'and 974-file', 'historical1,111': 'historical 1,111', '16D': '16-dimensional'}.items():report=report.replace(old,new)
(ROOT/'REPORT.md').write_text(report)
write_json(ROOT/'NEXT_WORK_ORDER.json',{'status':'PROPOSED_NOT_RUN','retain':'Dynamic protected existence + original content recurrence as a control; nearest-code control. No production adoption.',
 'next_candidate':'Separate learned existence representation/content lanes or a distinct trained absence code; pin state/readout/reset semantics and total state budget.',
 'must_test':['long noisy emptiness','legitimate first write','known retention','correction','clear and reactivation','every-read errors','payload degradation','damaged existence state'],
 'not_authorized_by_this_report':'Architecture replacement, merging repositories, general learning deployments or automatic execution of the next study.'})
print('report written',len(report.split()),'words')
