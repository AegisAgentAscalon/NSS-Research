# NBR-01 BindingDepth006 — locked main protocol

Status before main fits: NOT_RUN. Standalone v0.1 research, not companion release.
The governing handoff's p20 requires temporal state off/on × depth1/2/4/8 with
fixed evaluation learning. This protocol implements a bounded relationship task
for G02/G03/G04/G05/G06, not NBR-02 or low-bit state. Evaluation weights NEVER
change. Working record buffers do change. No Titans/optimizer/eligibility/RL
update, integration, model download, private-data training or deployment occurs.

## Inheritance and changed representation
ExistenceContent005 establishes a finite-slot writable-absence reference. We
transfer existence/content separation and lifecycle tests, NOT its learned
content or existence checkpoints to incompatible 17-D representations. Source
archives remain unmodified. New presence fields are explicitly protected Boolean
metadata in this pass. Learned noise-resilient existence is not silently claimed.

## Task, inputs and scaffolding
16 entities have fresh random unit codes in16 real coordinates; coordinate17 is
a separate UNKNOWN code. Two room identities have supplied self-records. One
functional containment relation exists per source when established. Randomized
acyclic graphs contain query paths1..4 in training,1/2/4/6/8 in evaluation. Some
required relationships are absent; background relations can also be absent.
Room names and object names are randomly coded on every generated episode.
Physical record positions and observation order are randomized. No integer
entity IDs, oracle path, correct next-slot choice or target answer enter neural
reader functions. The final answer decoder compares the output to the episode's
identity codebook. Query-code representation, source/value field structure,
qualified write/clear operations, finite slot allocation, and intermediate
training targets are explicit supplied structure. This is NOT language,
pronoun resolution, open-domain entity resolution or discovered decomposition.

Each known query has a generated path to one of the room/self records. Training
uses intermediate next-entity labels for every executed round. Loss = CE on
normalized output/candidate-code similarities +0.25 squared code error. This
strong process supervision must be counted; final-answer-only learning is NOT_RUN.
Room index0 in randomized topological order is the original query destination;
corrections redirect it to the other room. The neural inputs never expose that
order. Counterfactual corrections and value-shuffle interventions test dependence
on the presented links, not a room-frequency shortcut.

## Main candidates and budgets
Five paired seeds801..805. Each reader receives the same6000 generated batches
of64 examples, the same labels, AdamW lr0.002 weight_decay0.0001, clipped gradient
norm1, and cyclic allowed training depths1,2,4. Common data, step and supervision
budgets; NOT matched FLOPs, wall time, parameters or exact state representation.
Data fingerprint checks at initial/middle/final batches are recorded.

Readers:
- record_hop: learned normalized query/key matching, learned null threshold/scale,
  attention-weighted supplied value fields, reused per internal round.
- gated_hop: same memory read plus trained GRU transition.
- untied_hop4: four independently trained matching blocks. Standard read caps at4;
  depth8 allowance is NOT fabricated8-block work. A named cycled4 intervention
  reuses the four trained blocks a second time, without new training.
- tied_attention: standard multihead cross-attention + residual/normalization/FFN
  with shared block and latent query state. Small decoder-like control, NOT a
  language model or a complete Universal Transformer reproduction.
- fixed_attention4: four independently trained versions of that block, capped4.

A separate per-seed matcher (1200 steps×64, same optimizer) learns whether an
incoming numeric source matches a live slot or is new. Negative entities use the
same16-D code distribution as existing entities. This writer is shared by all
readers within a seed and frozen during evaluation. The allocator and full-value
write are exact; keys remain fixed on matched update. No matching ID oracle is
called. Capacity exhaustion is explicit rejection, not secret eviction.

Flat snapshot-GRU and code-space-aligned attention variants failed development
competence; their checkpoints remain archived, but they are not promoted to main
competent controls. All original raw generic-attention main seeds are retained,
including failures; they cannot justify a broad Transformer inferiority claim.

## Staged evaluation
A: visible current records, separate known/missing cases, hops1/2/4/6/8 ×depths.
B/C: learned store with query paths1/4/8, known/missing, delay0/64/1024 accepted
background updates plus denied/wrong-scope events, retained state on/off ×depths.
State-off removes records but keeps the same query; it is an information-removal
ablation, NOT an equal-evidence rival. Current visible-fact controls have all
records, avoiding a deliberately impoverished conventional control.
D: initial→correction→clear→rewrite,64 intervening distractor events each;
global clear and fresh installation in a new state object. Existing relation
keys, neighbouring information, and missing relationships are checked separately.
E: query noise0.05/0.2; actual per-event key/value state noise0.02/0.08 for64
rounds;32-record visible sets at4 and8 links; slot reversal, shuffled values,
removed evidence and shared orthogonal recoding. No hypothesis/fiction treated
as actual records. No stochastic numerical corruption is calibrated to hardware.
F: source-event binding audit, finite capacity, continuation snapshots with scope,
ABI, model fingerprint, arrays and RNG. Separate measured query-depth timing.

## Metrics and gates, fixed before main runs
Visible task competence: >=95% known AND >=95% UNKNOWN on each h1/2/4 condition
at4 rounds, for every main seed. The gate is joint, not reject-all accuracy.
Structural progress: compare trained4 rounds to held-out8 on8-link queries;
8-link accuracy>=95% is a declared transfer target for each recurrent seed.
Lifecycle target: >=95% answer accuracy for each lifecycle phase and correct
first write after absence; targeted neighbour/missing checks scored separately.
Same-evidence structural interventions and state-off distinguish causal reliance.
At insufficient depth a nonterminal output is UNRESOLVED, distinct from UNKNOWN;
no credit for avoiding supported answers. Report unsupported room claims on missing
cases. Report means/sample SD across five seeds, all failures and raw predictions.

Longer state and extra query rounds are independent clocks: maintenance/stream
processing does NOT increase when query depth increases. Main state uses bounded
hold between writes (not old content restoration); horizon success cannot prove
noise-resilient compressed memory. Stronger state-noise tests are separate.
Weights before/after evaluation must hash identically. All final arrays are
rescored by an independently implemented graph oracle; fresh-interpreter replay
must match. Reproduce at least one full training trajectory. User-device execution,
external replication, full1111 historical suite, larger language baseline,
full-model fairness, online learning and low-bit work remain NOT_RUN.

A result may keep a mechanism, revise a named part, reject a bounded candidate,
or request a missing measurement. No forced positive architecture verdict and
no declaration that this one task completes all of NBR-01.
