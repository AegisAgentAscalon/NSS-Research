from pathlib import Path
import json,statistics
ROOT=Path(__file__).resolve().parents[1]
s=json.loads((ROOT/'SUMMARY.json').read_text())
def agg(case,method,metric='known_accuracy',d=4,reader='record_hop'):
    row=next(r for r in s['aggregates'] if (r['case'],r['method'],r['reader'],r['depth'])==(case,method,reader,d))
    x=row.get(metric);return 'not applicable' if x is None else f"{x['mean']*100:.2f} ± {x['sd']*100:.2f}%"
def cell(case,method,metric='known_accuracy',d=4):return agg(case,method,metric,d).split(' ±')[0]+'%'
lines=[]
for title,case,d in [('Keys only, .02×64','isolation/keys02_t64',4),('Values only, .02×64','isolation/values02_t64',4),('Keys + values, .02×64','isolation/both02_t64',4),('Keys + values, .02×1024; eight links','isolation/both02_t1024_h8',8)]:
    lines.append('| '+title+' | '+' | '.join(cell(case,k,d=d) for k in ('none','intrinsic_mlp','learned_dictionary','nearest'))+' |')
text=f'''# NSS NBR-01 — RepairBinding007
## Compatible restoration, relationship traversal and failure isolation

**Standalone research v0.1 · RUN · NBR-01 remains OPEN**

Place beside the prior studies inside `MegaMind_Alpha_Proto`. **Do not merge.**
This is not a new source-foundation release or a qualified serving generation.

## Decision brief

**The previous restoration principle helped once given a compatible representation
and an explicit identity reference.** A new learned restorer, used with unchanged
BindingDepth006 readers, recovered the nominal key/value corruption tests and
preserved the tested write/correction/clear/rewrite lifecycle in all five pairs.
Exact nearest-identity repair also passed and was much cheaper in the measured
implementation. An unconditioned denoiser did not work as a repeated maintainer.

**The narrowed failure has two parts.** Moderate drift can leave an identity
recoverable from the canonical dictionary while moving it outside the frozen
reader's tight matching region. Longer uncorrected drift genuinely destroys enough
identity information to defeat late restoration. Query repair helps perturbed
known identities, but wrongly maps many truly unregistered identities to existing
ones. Repair must not silently assume that every input belongs to the dictionary.

**KEEP:** compatible identity cleanup with explicit reference access as a tested
research building block; existence/content separation; frozen iterative readers;
exact cleanup as a serious baseline. **REVISE:** no-match/membership handling and
robust matching for unfamiliar identities. **DO NOT PROMOTE:** this learned cleanup
as faster/better than exact projection, the unconditioned MLP, or a general-memory
solution. The bounded combination works; full NBR-01 is not complete.

## 1. What was actually combined

Inherited, unchanged: five record-hop and five gated-hop readers, plus five binders,
from BindingDepth006801–805. Earlier StateRecovery003 contributes the idea of
restoration during maintenance, not its incompatible eight-pattern checkpoint.
The new code space is the same17-coordinate identity ABI used by Study006:16 random
identity coordinates and an UNKNOWN coordinate. Fresh identity dictionaries are
created for new episodes; the task is structured numerical chain traversal, not
natural-language reference resolution.

Protected Boolean **relation presence**, source/value field separation, full-vector
qualified writes, scope checks and explicit allocation remain engineered. This
pass does NOT transplant or retest the learned existence weights from Study005.
No proof of a combined four-core neural companion is implied.

The new learned dictionary repair receives a vector and the episode identity
codebook, scores possible canonical symbols with a225-parameter shared network,
and returns a normalized soft mixture. Its inputs contain no integer identity,
correct slot, containment edge, parent graph or room answer. It learns a cleanup
rule from fresh dictionaries and clean-symbol targets. The codebook lists valid
identities, including subjects with no known containment relation. It cannot say
whether key→pouch or pouch→drawer was ever established.

This reference information is important. Study006 already used the dictionary at
final decoding; this study deliberately expands its access to intermediate repair.
The dictionary stays protected in the main tests. That is additional access and
an assumption to test, not a hidden neural memory or free information. Both the
learned and nearest-code candidates receive the same dictionary. A wrong-dictionary
fault and unregistered-identity queries expose the assumption.

## 2. Preparation, controls and scope

Ten new fits: five intrinsic residual MLPs(2257 parameters) and five
codebook-conditioned restorers(225 parameters), seeds901–905 paired with801–805.
Each completed1800 AdamW steps of96 sequences: **18,000 steps and1,728,000 sequence
presentations** total. Three noisy repair steps plus clean consistency yield
6,912,000 supervised forward presentations of the sequence targets—not that many
independent experiences. The dictionary arm also applies cross-entropy to the same
identity target. Batches and targets match within pairs; objectives, access,
parameter counts and computation do NOT all match.

Training noise was sampled from0/.02/.05/.10/.20. Five percent of inputs were erased
and labelled UNKNOWN. Two1200-step development fits and their failures are retained.
A B128 full-development attempt hit a120-second tool timeout without producing a
result; B64 was chosen before main registration. Development inspected the task,
noise and depth settings; main seeds, identity dictionaries and episodes are fresh.
There was no main hyperparameter retuning, seed removal, model selection by main
score, download or external upload.

All learned parameters stayed fixed throughout scored evaluation. No optimizer is
used in the evaluator. Working-state writes are not parameter adaptation. This
remains NBR-01, not Titans-style online learning, delayed credit, RL or low-bit
learning-state research. Tests are synthetic numerical disturbances, not measured
hardware faults or a biological noise model.

## 3. Isolated damage: learned and exact cleanup restore chain following

The initial state here contains exact visible records, bypassing the learned
writer so maintenance can be isolated. Each main scenario has64 episodes per pair,
32 with an established chain and32 with a missing link. Table entries are known
final-destination accuracy for the primary record-hop reader, averaged across all
five pairs. Full variability and the gated reader are in SUMMARY.json.

| Damage and horizon | No repair | Intrinsic MLP | Learned dictionary repair | Exact nearest repair |
|---|---:|---:|---:|---:|
{chr(10).join(lines)}

For all these nominal cases the two dictionary-assisted mechanisms also returned
**100% correct UNKNOWN for missing links**. The gated reader independently passed
the same declared nominal screens in all five pairs. Normalization alone did not
restore the required identities. No arbitrary general-architecture comparison is
supported by these controls.

At the stronger .08×64 corruption, learned repair reached
**{agg('isolation/both08_t64','learned_dictionary')} known** and
**{agg('isolation/both08_t64','learned_dictionary','unknown_accuracy')} UNKNOWN**.
Nearest-code repair remained100%/100% on these samples. No method is established as
noise-proof or able to preserve arbitrary unlimited content.

### Moderate drift was often a matching problem before it was total information loss

With .02×64 and both fields perturbed, the unmaintained store's keys were still
nearest to their intended canonical identity **99.83%** of the time, and values
**99.96%**. Yet its four-link final accuracy was0%. Mean cosine to intended codes
had fallen to about.839. The frozen reader's learned match criterion was too strict
to reliably traverse those altered representations. Restoring a compatible input
recovered the same reader; no reader training was added.

These identity percentages average live slots, not whole-path correctness. A
single bad edge can invalidate a path, and a high slot average is not a guarantee
of retrieval. Nevertheless, the intervention and near-perfect canonical decoding
identify more than an undifferentiated claim that every record was forgotten.

When both fields were damaged, repairing keys alone gave
{agg('ablation/repair_keys_only','learned_dictionary')} known accuracy;
repairing values alone gave {agg('ablation/repair_values_only','learned_dictionary')}.
Both are needed here: the read value becomes the next query. The repair-disabled
and normalization controls establish that a maintenance call alone is insufficient.

## 4. Timing of repair, useful depth and the limits of late recovery

Eight-link chains after1024 noisy maintenance ticks still required eight read
rounds. In the successful repaired state,1/2/4 rounds did not solve the full chain;
eight did. State removal left established-chain accuracy at0%. This distinguishes
retained information, event-time restoration and query-time reasoning. The event
repair budget does not increase when query depth increases.

For the64-tick four-link test, applying64 repair calls only at the end recovered
{agg('ablation/late_equal64','learned_dictionary')} known accuracy. Thus not every
moderate disturbance requires continuous repair; the precise cadence needs its
own cost/quality study.

After1024 unmaintained ticks,1024 late repair calls recovered only
{agg('ablation/late_equal1024','learned_dictionary')} known accuracy with learned
cleanup and {agg('ablation/late_equal1024','nearest')} with nearest cleanup.
The main long periodic condition used eight links while the main long late
condition used four. **A post-main matched diagnostic** supplied the missing
four-link periodic arm with the SAME graphs/noise as the late-only condition:
periodic learned and nearest repair both recovered100% known and100% UNKNOWN.
This is exploratory paired evidence, not a retroactively changed main condition.
It supports maintaining decodable state before it drifts beyond recovery; it does
not establish an optimal maintenance cadence.

A separate post-main zero-noise1024-step check found that the dictionary-based
maintainers preserve the clean codes. The intrinsic MLP did not: even clean known
chains fell to0%. It was prepared for only three recurrent denoising steps and
its accumulated bias is unsuitable for this much deeper maintenance task. Do not
turn its failure into a theorem against all reference-free neural restoration.

## 5. Live writes, corrections and absence survive the combination

A separate stream uses the unchanged LEARNED binder, not a gold store. It includes
initial installation, correction, clear, rewrite, reset and fresh installation,
with64 intervening ticks per phase. Background observations update an unrelated
relationship, with denied and wrong-scope writes also present. Full-vector writes
and qualification remain supplied. Presence is never guessed from a repaired
content vector.

Both dictionary-repair mechanisms reached100% known/UNKNOWN at the initial,
correction and rewrite query points, and100% UNKNOWN after the necessary clear
and full reset. Fresh-installation known accuracy was
{agg('stream/new_scope','learned_dictionary')}; missing answers remained100%.
All five pairs passed the declared>=95% joint nominal screen for BOTH readers.
These are declared query points, not every possible intermediate read in the stream.

A post-main clean installation diagnostic reproduced the same99.38% fresh-scope
known score before adding noise or repair. That remaining error is already present
in the learned binding/read path. Cleanup cannot be assumed to correct a wrong
initial association merely because the values are well-formed symbols.

## 6. The new boundary: a damaged familiar identity versus a truly unfamiliar one

For query-only noise.2 with intact storage, no repair gave
{agg('query/sigma0.2','none')} known recall and100% UNKNOWN. Both dictionary cleanup
methods recovered100% known recall, but UNKNOWN became99.38%: one missing-query
sample across the five pairs was incorrectly interpreted as a supported room.
This small error must not be hidden behind the recovered known-answer score.

At query noise.4, learned cleanup reached
{agg('query/sigma0.4','learned_dictionary')} known and
{agg('query/sigma0.4','learned_dictionary','unknown_accuracy')} UNKNOWN.
Nearest cleanup traded higher known recall for worse absence preservation:
{agg('query/sigma0.4','nearest')} known and
{agg('query/sigma0.4','nearest','unknown_accuracy')} UNKNOWN.

More importantly, queries deliberately naming an identity OUTSIDE the supplied
catalogue exposed the closed-world assumption:

| Query about an unregistered identity | Correct UNKNOWN | Unsupported room answer |
|---|---:|---:|
| No repair | {cell('fault/unknown_identity','none','unknown_accuracy')} | {cell('fault/unknown_identity','none','unsupported_room_rate')} |
| Learned dictionary repair | {cell('fault/unknown_identity','learned_dictionary','unknown_accuracy')} | {cell('fault/unknown_identity','learned_dictionary','unsupported_room_rate')} |
| Nearest-code repair | {cell('fault/unknown_identity','nearest','unknown_accuracy')} | {cell('fault/unknown_identity','nearest','unsupported_room_rate')} |

The rest of the errors are unresolved nonterminal outputs, not all room claims.
These candidates assume a repairable input corresponds to an available symbol;
training did not teach open-vocabulary identity membership. Mapping it to a
familiar symbol can make an unrelated existing relationship appear relevant.

**Stable empty records do not solve this input-identity problem.** A repair service
needs an appropriate no-match/uncertain outcome or a legitimate identity-enrollment
path; it must not force every new input into the closest existing identity.
That next requirement is proposed, not implemented or measured by a tuned gate here.
Do not conflate it with factual truth, permissions or evaluation-time learning.

## 7. What a dictionary cannot recover

Corrupting the dictionary geometry while keeping records intact drove both
codebook-assisted mechanisms' known accuracy to0%. No repair stayed100% on that
intact store. The dictionary is a real dependency and needs integrity/version
handling; the test deliberately supplies bad references rather than pretending
software checks make the neural mechanism omniscient.

Replacing a relevant value with a DIFFERENT VALID identity caused0% correct known
answers for all mechanisms. Completely erasing a necessary value also gave0%
recovery; the successful missing response is not retrieval of the erased fact.
The dictionary knows possible symbols, not the previous edges. Restoring a valid
code is not proof of a true relationship. Exact evidence/archive recovery remains
separate and was not supplied as a repair oracle.

## 8. Cost: useful does not mean cheapest

Raw state per16-record stream is unchanged from the Study006 layout:
2176 bytes for keys/values +16 Boolean bytes =2192 bytes. Identity dictionary:
1156 bytes; query vector:68 bytes. The dictionary was already counted for final
readout, but its expanded intermediate ACCESS is new. The learned repair adds
900 bytes of weights; intrinsic MLP adds9028. Readers/binder weights, other buffers,
logs, snapshots, training gradients/moments and framework memory are additional.

The learned score calculation materializes per-stream feature and hidden arrays
of5440 and34816 bytes respectively in this implementation (not persistent state).
These calculated component sizes are not a measured total peak-memory guarantee.

A separate one-thread CPU timing pass measured one both-field cleanup sweep for
64 streams: learned dictionary **5.981ms**, nearest projection **0.382ms**,
intrinsic MLP **0.608ms**, and normalization **0.047ms**. The unchanged reader's
four/eight-round calls were about0.786/1.577ms per64-stream batch. This code is not
optimized; measurements are one seed on this environment, not your device, energy
cost, production latency or an asymptotic lower bound. The exact control both
worked and was substantially cheaper here.

Recorded main fit loops sum to **{s['summed_training_loop_seconds']:.2f}s** and main
evaluation loops to **{s['summed_eval_loop_seconds']:.2f}s**. Development, data
construction, engineering, verification, interpreter startup and packaging add
work. Some verification jobs overlapped. These sums are not the complete wall
clock duration or a performance comparison to previous studies.

## 9. Verification and honest status

-34 new unit tests,52 unchanged BindingDepth006 tests and68 foundation tests passed:
 **154 distinct tests**, not multiplied by reruns. Foundation used site packages
 disabled. No Windows run and no full historical1111-test qualification.
-Ten fitted checkpoints are finite, differ from initialization and match hashes.
 Main paired batch fingerprints match. Registered scientific source and inherited
 checkpoint/source hashes remained unchanged.
-All five main evaluations were replayed in fresh interpreters:525 state scenarios,
 **4200 scored rows and268,800 answer evaluations**, with all saved predictions and
 final-state hashes exactly reproduced. Those are correlated checks, not268,800
 independent experiments or external replications.
-An independent NumPy/Python graph scorer recomputed answers/metrics and decoded
 identity scores from saved records. It does not import the model/evaluator.
-One complete1800-step learned-repair fit reproduced the exact checkpoint bytes,
 learning history and sampled-batch fingerprints.
-25 complete numerical-state/RNG or mid-query snapshots resumed bit-for-bit in a
 fresh interpreter. Scope, ABI, weight, dtype and corruption checks reject invalid
 snapshots. This is not a production multi-file atomic crash-recovery service.
-Post-main diagnostic results and verification are separately labelled in
 evidence/diagnostics and DIAGNOSTICS_VERIFICATION.json. They do not replace main
 rows or turn the comparison into a registered full-lifecycle reliability trial.
-Original ten input archives preserved. Source manifests checked:974 foundation
 files,705 Study006 files and382 Study003 files. Delivery extraction checks are
 recorded in the external delivery receipt rather than assumed from source tests.

This is internal reproducibility on one Linux CPU environment, not independent
external replication or longitudinal companion reliability. The generic attention
baseline's earlier competence weakness was not repaired in this focused pass.

## 10. Decision and next work

The optimistic part is supported: compatible restoration and the existing trained
iterative readers can cooperate without reader weight changes. The less optimistic
case has also been narrowed: reference-free repair, identity membership, wrong
valid associations and destroyed information remain distinct problems.

Keep the tested combination as a bounded reference, but prefer the simple control
where its cost/quality wins. The next useful discrimination is **membership-aware
identity restoration**: separate a perturbed known identity from a truly new one,
while retaining legitimate new-record writes and UNKNOWN behavior. Also compare
cheaper repair cadence/read-time cleanup and a better-prepared robust reader at
matched information access. These are proposals, not automatic new runs.

Full NBR-01 stays OPEN: richer binding, generic-control competence, task diversity
and a useful quality/resource frontier remain. No NBR-02/03 work, broader learning,
low-bit tracing, tri-core deployment or approved architectural replacement occurred.

## Source/evidence navigation
Project basis: cognition handoff v1.0 pages7–9,13,19–21; supplied reports for
StateRecovery003, ExistenceContent005 and BindingDepth006. Original source copies
and hashes in reference/ and spec/REGISTRATION.json. No external literature claim
or biological simulation is introduced by this implementation.

Main protocol: spec/PROTOCOL.md. Aggregates: SUMMARY.json. Source events/answers:
results/. Internal verification: evidence/INDEPENDENT_RESCORING.json,
evidence/replay/VERIFIED.json, evidence/TRAINING_REPRODUCTION.json,
evidence/continuations/VERIFIED.json, evidence/PRESERVATION.json,
evidence/RESOURCES.json. Development and post-main diagnostics remain separate.
'''
(ROOT/'REPORT.md').write_text(text)
print('report words',len(text.split()))
