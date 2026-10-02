from pathlib import Path
import json,statistics
r=Path('/mnt/data/NSS_NBR01_BindingDepth006_v0.1');s=json.loads((r/'SUMMARY.json').read_text());resource=json.loads((r/'evidence/RESOURCE_LEDGER.json').read_text());lookup={(x['kind'],x['case'],x['depth']):x for x in s['aggregates']}
def acc(k,case,d=4):
 a=lookup[k,case,d]['answer_accuracy'];return f"{a['mean']*100:.2f} ± {a['sample_sd']*100:.2f}%"
def get(k,case,d=4):return lookup[k,case,d]['answer_accuracy']['mean']*100
names={'record_hop':'Shared content-attention reader','gated_hop':'Gated content-attention reader','untied_hop4':'Unshared four-stage content attention','tied_attention':'Shared generic cross-attention','fixed_attention4':'Fixed four-block generic cross-attention','exact_lookup':'Exact byte-key traversal of same workspace'}
short='\n'.join(f"| {names[k]} | {acc(k,'visible/h4/missing0')} | {acc(k,'visible/h4/missing1')} |" for k in names)
stream='\n'.join(f"| {h} | {d} | {acc('record_hop',f'stream/h{h}/missing0/delay1024/on',d)} | {acc('record_hop',f'stream/h{h}/missing0/delay1024/off',d)} |" for h in [1,4,8] for d in [1,2,4,8])
life='\n'.join(f"| {phase} | {acc('record_hop','lifecycle/'+phase)} | {acc('gated_hop','lifecycle/'+phase)} | {acc('exact_lookup','lifecycle/'+phase)} |" for phase in ['initial','correction','clear','rewrite','global_reset','new_scope_fresh_records'])
report=f'''# NSS NBR-01 — BindingDepth006
## Content-based record binding and useful processing depth

**Standalone research v0.1 · Main study RUN · Full NBR-01 remains OPEN**

Place beside ExistenceContent005 inside `MegaMind_Alpha_Proto`; **do not merge**
with earlier studies or the v0.5.0 foundation. None of the nine input ZIPs was
modified. This is a research artifact, not a qualified new serving generation.

## Decision brief

**The structured, trained readers used extra internal rounds to solve longer
relationship chains with fixed evaluation weights.** Both shared record-hop and
gated record-hop reached100% on the tested eight-link known-answer problems at
eight rounds, despite gradient training using only1/2/4 rounds and paths at most
four links. Missing-link answers were100% and99.84%, respectively. The active
record store remained bounded by entity count rather than transcript length.

This is a scoped relational-retrieval result, not evidence of general reasoning
or a new algorithm. The experiment supplies identity encodings, key/value fields,
valid write operations, room/self-record semantics, a presence convention, and
intermediate path supervision. The reader must learn content matching; it is NOT
given the correct next slot or an executable path. Classical exact traversal and
an unshared attention control also solve the clean task. Extra steps help a
learned compositional procedure here; a uniquely superior neural architecture is
not established.

**Keep the factorized record layout and iterative reader as a research reference.
Revise the robustness of identity matching and stored/query representations.**
Small generic attention controls remain insufficiently competent on missing facts,
and continuous key/value noise breaks the new record representation. Do not
promote a production model or declare all NBR-01 requirements solved.

## 1. Scope, inherited design and what actually ran

The handoff's experiment ladder (page20) specifies retained state off/on × internal
depth1/2/4/8 with fixed learning. This study addresses that numerical mechanism
comparison and the adjacent binding question. It does NOT introduce Titans-style
adaptive weights, delayed-credit learning, reinforcement learning, low-bit traces,
new neural roles, or a change to the frozen serving Primary.

ExistenceContent005 supplied a tested existence/content separation. We transferred
that principle and the write/correct/clear/rewrite tests, not its checkpoint into
an incompatible representation. This pass uses new random17-coordinate codes
and protected Boolean record presence. It does **not** retest the previous learned
existence map or reuse the old content-restoration network on new codes.

Five paired seeds801–805 produced25 trained readers and five trained binders:
**30 fitted checkpoints,156,000 optimizer steps and9,984,000 example presentations.**
Each reader received6000 steps of64 examples; each binder received1200 steps.
The25 readers received22,400,000 within-example intermediate target presentations;
the five binders received384,000 match/new classification targets. These are
repeated/shared synthetic presentations, not millions of independent experiences.

All reader arms within a seed use the same generated batches, teaching targets
and optimizer-step budget. Initial/middle/final batch fingerprints match. The
binder is shared across readers within that seed and its separate preparation is
counted. This is **not a matched-compute, parameter-count or total-cost ranking**.
Every main seed is retained. No candidate was selected by its main test score.

The original development pilots and failures remain in `evidence/development/`:
12 fitted development checkpoints,33,600 steps, including failed flat-GRU and
code-space-alignment alternatives. A negative-sample bug in the development
binder and a smoke-evaluation function-name error were fixed before main
registration. Neither caused removal of a main seed. Old source snapshots and
logs preserve those attempts. Registration hashes of the fitted scientific code
and protocol still match after execution.

## 2. The task and supplied structure

Each episode has16 freshly coded entities and two rooms. Real identities are
random unit vectors in16 coordinates; coordinate17 carries a separate UNKNOWN
code. Room/self records make terminal states explicit. Observed source→destination
records represent one functional containment relation. Physical record placement,
entity names and event order vary independently of the question's path.

An illustrative question is: key→pouch→drawer→study; which room contains the key?
The actual experiment uses generated numeric identities, NOT those English words.
The room answer is not stored as a direct key→room association when multiple links
are required. Correcting a link can redirect the answer to the other room; clearing
a required relation should remove support rather than preserve an old answer.

The query path is at most four links during training and up to eight in evaluation.
Some path links and background relations are absent. A room, UNKNOWN and a
nonterminal output are distinct: at inadequate depth a nonterminal answer is
UNRESOLVED, not a correct claim that no fact exists. The final decoder compares
outputs to the full episode codebook; it does not silently restrict guesses to
the correct rooms or insert an oracle's next node.

**Scaffolding:** source/value field separation, finite allocation, qualified writes,
clear semantics, complete vector insertion, a codebook for decoding, terminal-room
records and per-round intermediate targets are supplied. This is not spontaneous
entity discovery, natural-language coreference, ambiguous-evidence learning,
multiple relation types or final-answer-only training. The original destination
is room0 in a randomly permuted internal ordering that the reader never receives;
counterfactual corrections redirect it to the other room. Shuffling values and
changing links test reliance on actual relationships rather than that generator
regularity.

Untrained depth8 and longer paths were inspected during development. Thus
“untrained/held-out depth” means **not used for gradient training**, not an
untouched architecture-selection variable. Main seeds and episodes are fresh.

## 3. Models, memory and interfaces

The shared **record-hop** reader learns query/key projections, a match scale and a
no-match threshold:818 parameters. At each round it attends over ALL live record
keys plus a null option and takes a weighted value read. That read becomes the
next query representation. No integer matching or path traversal occurs inside
this model. Its explicit key/value geometry is a strong and intentional inductive
bias. The **gated-hop** variant adds a GRU transition, totaling2654 parameters.

The **untied-hop4** control has four independently trained matching stages:
3272 parameters. It executes at most four stages by default; an8-round allowance
does not invent more work. The registered `cycled4` intervention explicitly
executes its four stages twice. This separates extra computation from claiming
that one shared block is uniquely necessary.

The **generic cross-attention controls** use multihead attention, residual updates,
normalization and feed-forward blocks. The shared version has10,850 parameters;
the fixed four-block version has36,482. These are small decoder-like mechanisms,
not pretrained language models or complete reproductions of Universal Transformers.
Their weaker missing-evidence behavior cannot establish inferiority of Transformers
as a family.

The **binder**,818 parameters, learns content-based match-versus-new decisions
before evaluation. It sees a numeric source code and live keys—not an integer ID
or gold slot. The exact allocator chooses a free slot when the learned selector
reports new; a supplied accepted write installs the complete value. On an existing
match the original key is kept and its value is updated. Clears remove the slot;
denied and wrong-scope writes leave content/presence unchanged. Full capacity
rejects a new write explicitly rather than secretly evicting another record.

The current16-record store uses **2192 raw bytes per stream**: two17-float fields
and one Boolean BYTE per slot. The external decoding codebook costs another1156
bytes/stream; query state, parameters, projected keys, attention buffers, metadata,
framework memory and evidence logs are additional. A32-record test allocates more
memory; it is not a same-budget capacity claim. This study does not pack learning
state or treat a Boolean byte as one-bit storage.

The store holds its buffers between events. It does NOT run the old learned
content-restoration procedure. Temporal event handling has the same budget for all
query depths, so more internal rounds do not secretly provide more maintenance.

The **exact read control** walks byte-equal source/value associations from the SAME
workspace. In streaming conditions it inherits the same learned binder, so it is
not an independently protected exact archive. Its perfect visible-fact results
establish answerability; its occasional streaming errors expose binding errors.
It fails exact lookup on altered query/key bytes and must not be mistaken for a
best-tuned fuzzy or symbolic identity resolver. The concept was registered; the
untuned executable implementation was added during main execution and identified
in `spec/EXACT_CONTROL_NOTE.json`.

## 4. Visible facts: competence before memory claims

Means ± sample standard deviations over all five main seeds, four-link problems
at four actual processing stages:

| Mechanism | Established chain | A required link is missing |
|---|---:|---:|
{short}

Record-hop, gated-hop, untied-hop4 and exact traversal passed the joint >=95%
known/UNKNOWN visible screen on each of h1/h2/h4 in all five seeds. The two generic
cross-attention candidates passed it in **zero of five**. Their known answers
alone would exaggerate their competence. Their failures remain in every table.

This is why later failure of those generic controls is not a clean architecture
verdict: they already struggle with evidence directly in view.

## 5. Extra processing solves a longer relation chain

On eight-link visible problems at eight actually executed rounds:

- Shared record-hop: **{acc('record_hop','visible/h8/missing0',8)} known;
  {acc('record_hop','visible/h8/missing1',8)} missing.**
- Gated-hop: **{acc('gated_hop','visible/h8/missing0',8)} known;
  {acc('gated_hop','visible/h8/missing1',8)} missing.**
- Exact traversal: **100% known and100% missing.**

The record-hop and gated-hop readers have0% final room accuracy on known eight-link
cases at one, two or four rounds, then100% at eight. Their earlier outputs are
normally intermediate entities: they are making progress, not already answering
the final question. No learned parameter changes during those extra rounds.

The standard untied-hop4 control still performs four stages under the8-round
allowance, so its0% known eight-link result is **not** an equal-compute loss.
When its four trained stages are deliberately reused a second time, it reaches
**100% known and99.06% missing** on the eight-link set. The evidence supports useful
additional execution of a learned compositional procedure, not exclusive value
of weight sharing, a novel reasoning algorithm or a general neural advantage.

A32-record visible set with eight-link paths gives100% known recall for both
shared structured readers; missing answers are99.84%/100%. This adds count and
path stress but still uses the same synthetic coding convention. Separate32-record
four-link results are retained to avoid hiding the two distribution shifts.

## 6. Retained state and internal depth are separate variables

Shared record-hop after1024 unrelated events, known-answer questions. State-off
removes the evidence at query time; it is an ablation, not a crippled rival claimed
to be an equal-evidence benchmark.

| Links required | Internal rounds | State retained | State removed |
|---:|---:|---:|---:|
{stream}

The eight-link result with retained state is99.22% for record-hop,99.38% for
gated-hop and99.38% for exact reading of that same learned-written workspace.
Most of this small gap from100% already exists at delay0: initial content binding
occasionally misplaces a record. For record-hop, eight-link accuracy moves from
99.38% at delay0 to99.22% at1024; the gated and exact readers remain99.38%.
These outcomes should not all be relabelled long-term forgetting.

The active store does not accumulate the event transcript. Distractors repeatedly
update one unrelated background relation and include denied and wrong-scope
writes. This is a bounded interference test, not a stream of unlimited new
entities. Endpoints are queried; unlike ExistenceContent005, this study does not
claim that every possible answer during every intervening event was correct.

## 7. Correction, clear, rewrite and causal interventions

Four-round lifecycle snapshots after64 distractors at each phase:

| Phase | Shared record-hop | Gated-hop | Exact reading of same workspace |
|---|---:|---:|---:|
{life}

All three structured neural reader arms passed the declared >=95% lifecycle gate
in every seed. This is not100% system reliability. Correcting one relevant edge
redirected inferred destinations; clearing it removed support; rewrites restored
support. Record absence is relation-specific—an entity can remain known while
its containment relation is missing.

A separate all-slot audit includes neighbours and absent relations. In clean
initial/corrected/cleared conditions,98.75% of sampled full stores were entirely
correct. The seeded errors are retained, not repaired by a gold record store.
After noisy storage the full-store figure fell to2.5%; see the stress limitation.

Reversing slot order preserves the structured readers' answers. A shared
orthogonal recoding retains100% on the selected four-link cases. Shuffling which
values are paired with keys reduces known-chain accuracy to11.56% for record-hop
and11.72% for gated-hop; removing evidence gives0% on these known-answer cases.
These interventions support dependence on actual associations. They do not prove
all possible bindings or invariances.

## 8. The next failure is exposed, not solved

**Continuous corruption of the NEW key/value representation breaks the pipeline.**
With Gaussian noise0.02 added per coordinate after each of64 events, four-link
known accuracy at four rounds is0% for both structured shared readers. Stronger
0.08 noise also gives0%. The generic attention controls are weak here too.
Presence remains protected, but corrupted keys alter addressing and corrupted
values spoil subsequent queries. This is combined storage/binding/readout stress,
not an isolated measurement of one of those mechanisms. No noisy-state recovery
procedure was transplanted from the previous incompatible code space.

The noise scales are coordinate-specific synthetic interventions, not a measured
hardware bit-flip rate, physiology or a directly comparable stress to Study005.
An exact archive with protected canonical identity could behave differently; this
pass's exact reader uses the same damaged neural-key workspace.

The interface matters even without corrupting storage. A one-time query disturbance
of0.05 leaves the structured shared readers at100% on the known four-link cases.
At0.2, recall falls to22.97%/26.56%. Exact byte lookup gives0% when the query bytes
change. This establishes a limited tolerance benefit of learned matching, not
superiority to a good symbolic/nearest-identity interface.

A clearly labelled **exploratory paired-query diagnostic**, added after inspecting
the main known-only query-noise results, checks missing cases too. At noise0.2 and
eight rounds on512 examples per condition/seed, record-hop has22.27% known recall
and100% correct UNKNOWN; gated-hop has25.39%/100%. Shared generic attention has
79.61% known recall but only56.41% correct UNKNOWN, with unsupported room claims
on41.52% of the missing cases. The fixed generic control has49.34% known and91.09%
UNKNOWN. No weights or thresholds were retuned. The200 diagnostic rows are NOT
main-gate evidence and do not replace main scores.

The tradeoff is specific: strict matching can reject legitimate but altered
queries; permissive matching can return unsupported associations. A high known-only
score is not overall robustness. Better identity/query alignment and robust record
representations are a named next target, while preserving absent-relation behavior.

## 9. Cost and reproducibility

Main fitted training loops summed to **{resource['main_training_loop_seconds']:.2f}s CPU**;
development loops added **{resource['development_training_loop_seconds']:.2f}s**, and a full
6000-step reproduction added **{resource['reproduction_seconds']:.2f}s**. Source engineering,
generation, process startup, testing, replays and packaging add real work. Some
training and evaluation jobs ran concurrently; these summed loop times are NOT
isolated model-speed comparisons or the complete wall time of the session.

An isolated timing pass afterward used one thread and batches of128 on this Linux
CPU environment. The shared record-hop reader's median batch query times were
0.317,0.556,1.078 and2.030ms for1/2/4/8 rounds. Extra rounds have real cost. These
measure one checkpoint, not user-device latency, energy or a large-model projection.
Exact Python lookup rebuilds a dictionary per query call; its timing is not a
fundamental algorithmic comparison or an optimized implementation benchmark.
Full timing and process-RSS ranges are in the resource evidence.

**Verification completed:**

-52 current research unit tests;68 unchanged foundation tests with site packages
 disabled;44 unchanged ExistenceContent005 tests. These are164 distinct tests,
 not multiplied by reruns.
-All30 fitted checkpoints are finite, changed from initialization, and match
 saved hashes. Registered fitted source/protocol hashes remain unchanged.
-All30 evaluation configurations—25 neural and five exact read controls—were
 regenerated in fresh interpreters, with every saved array and main metric matching.
-Independent NumPy/Python graph walks rescore **7920 rows and1,013,760 answer
 evaluations** from saved canonical relation snapshots. This is not a claim of
 independent external data collection or an independently written event generator.
-One complete6000-step training trajectory reproduces all weights, saved losses,
 sampled data fingerprints and the safetensors checksum.
-20 scoped record/RNG snapshots and100 within-query snapshots resume identically
 in a fresh interpreter. The query-step implementation also agrees bit-for-bit
 with the ordinary forward path at each tested cut. Scope, ABI and model mismatch
 tests reject incompatible snapshots. These are complete-snapshot research checks,
 not a production atomic write/crash-recovery service or optimizer-resume claim.

Fresh delivery extraction checks are recorded separately in the delivery receipt.
All verification is internal reproduction in one environment. User-machine
execution, external replication and longitudinal companion reliability remain
NOT_RUN. The full historical1111-test qualification suite was not rerun.

## 10. Decision and next boundary

**KEEP:** explicit existence/content separation; content-addressed record state;
iterative read/query updates; exact and unshared controls; evidence-dependent
corrections and UNKNOWN tests. This pass supplies a real, inspectable state/depth
factorial in which extra query computation improves an untrained chain length.

**REVISE:** robustness of stored identity/content representations and query-to-key
matching; the missing-evidence competence of the generic attention candidates.
Do not freeze the current strict threshold as a general semantic qualification
rule or infer factual truth from a successful match.

**DO NOT CLAIM:** general reasoning, biological fidelity, parameter-efficient
lifelong learning, superior Transformers or recurrent networks as entire families,
noise-proof memory, real-language companion competence, completed NBR-01 or a
production architectural upgrade. The combined representation/binding-noise case
and a stronger generic control remain open. No NBR-02/03 work was started.

The next bounded candidate should address robust identity/query alignment and
absence-preserving retrieval under the SAME fixed-weight state/depth discipline.
This is not another empty-vector clamp experiment and not a detour into online
learning. No new experiment or architecture replacement is automatically approved
by this report.

## 11. Source and artifact register

Project basis: the supplied Cognition, Architecture & Low-Bit Learning Handoff
v1.0, especially pages5,8–9,19–21; ExistenceContent005 v0.1; v0.5.0 foundation.
Input identities appear in `evidence/INPUT_BEFORE.json`; preservation is checked
again at delivery. Current user instructions defer all1–8-bit learning-state work.

External mechanism references reviewed here: Sukhbaatar et al., *End-To-End Memory
Networks*, arXiv1503.08895v5; Dehghani et al., *Universal Transformers*,
arXiv1807.03819v3. They motivate repeated attention reads and shared computation.
This experiment is an original small implementation with explicit process labels,
not a reproduction of either paper's benchmarks or a claim of novelty.

Navigation: `spec/REGISTRATION.json`, `spec/PROTOCOL.md`, `SUMMARY.json`,
`checkpoints/`, `results/`, `evidence/INDEPENDENT_RESCORING.json`,
`evidence/FULL_REPLAY.json`, `evidence/EXACT_REPLAY.json`,
`evidence/TRAINING_REPRODUCTION.json`, `evidence/continuations/VERIFIED.json`,
`evidence/RESOURCE_LEDGER.json`, `evidence/PAIRED_QUERY_DIAGNOSTIC.json`.
'''
(r/'REPORT.md').write_text(report)
print('Report words',len(report.split()))
