# RepairBinding007 — frozen main protocol

## Scope and question
NBR-01 only: compatible representation repair + inherited relationship traversal.
All learned parameters, including repair, remain fixed at scored evaluation.
No test-time optimizer, plasticity, RL, quantization, brain simulation, neural role
redesign, production integration, model download, repository upload, or deployment.

Can compatible maintenance restore query-dependent chain following without
inventing absent relationships or interfering with correction, clear and rewrite?
Separate key corruption, value corruption, and query-only disturbance.

## Inputs / inherited machinery
BindingDepth006 v0.1 reader and binder checkpoints801–805 are reused, not retrained.
Two readers (record_hop, gated_hop) are fixed within each pair. Main new repair seeds
901–905 map to parents801–805. Codes:16 freshly random unit identities in16 dimensions
+ UNKNOWN at coordinate17. Protected Boolean relation-presence remains in use.
StateRecovery003 contributes restoration-as-maintenance and perturbation tests,
not its incompatible eight-prototype weights. ExistenceContent005 supplies the
existence/content distinction; learned presence maps are not retested here.

## Candidates and information access
1. No repair: source reference / maintenance-disabled ablation.
2. Normalization: restore magnitude, not symbol identity; parameter-free control.
3. Intrinsic residual MLP (17→64→17): no episode-codebook input; clean consistency
   and3 noisy repair rounds during training. Additional randomly chosen zero inputs
   are labelled UNKNOWN. New episodic codes make a universal finite attractor list
   inappropriate. This is a scoped learned control, not all denoising architectures.
4. Learned dictionary-conditioned repair:5 scalar features per input/canonical-code
   pair →32 tanh units →scalar score; softmax-weighted canonical code mixture,
   normalized. No integer identity, record address, gold next link, or answer is
   supplied to the restorer. It is trained on fresh identity dictionaries and
   denoising labels. This is codebook-conditioned repair/cleanup, not free recovery.
5. Nearest identity code: exact Euclidean projection to same codebook; exactly
   erased vectors explicitly map to UNKNOWN. Strong engineered control.

The dictionary is protected from the main storage perturbation and includes ALL
known entity symbols, including subjects without a recorded relation. It contains
NO containment links and NO existence statuses. It was already available to the
old final decoder; its access at intermediate maintenance is NEW and counted.
A wrong-dictionary condition removes this protection. Out-of-dictionary queries
expose the closed-vocabulary assumption. Fixed projection need not lose to learning.

## Development versus main
Two development fits(seed900,1200 steps each) and quick/full evaluation are retained.
The initial B128 full-evaluation attempt was killed at the tool timeout; no weights
were changed or seed removed. B64 selected during development for bounded runtime.
No results were saved by the timed-out attempt. No main hyperparameters are tuned
on main outcomes. Exact 1/2/4/8-round settings and noise conditions were inspected
during development; only new main fits, dictionaries, episodes and noise draws are
held out. This is not an untouched task-family or depth-selection benchmark.

Both new learned arms:1800 AdamW steps, batch96, lr.002, no weight decay, 3 noisy
maintenance rounds plus a clean-consistency term. sigma sampled from
{0,.02,.05,.10,.20};5% of training inputs completely erased→UNKNOWN. Fresh codebook
and target per sequence. Dictionary arm has additional CE against the SAME clean
identity target; this adds an objective, not new labels. Same generated batches,
steps and target codes; NOT matched parameter count, access, objective or FLOPs.

## Main scored scenarios
B64 episodes per scenario,32 known and32 missing originally; five paired seeds.
Each read returns outputs after1/2/4/8 internal rounds, recorded separately from
maintenance. Reader is unmodified. Query-only repair happens once at query entry.

- Exact initial-visible stores: no learned-write errors before isolated damage.
  4-link clean;64 noise ticks sigma.02 on keys only, values only, both;
  both sigma.08×64;8-link both sigma.02×1024.
- Query-only: intact stores, normalized query perturbed by .05/.2/.4 in16 identity
  dimensions; no lookup of the true query index during repair.
- Late-only ablation:64/1024 calls of repair at the END of the same corruption
  process; same repair-call count, different temporal placement. Not identical
  measured runtime or guarantee of equal arithmetic shortcut behavior.
- Key-only/value-only repair under corruption of BOTH fields.
- State-off8-link ablation: all record buffers and flags removed. No wasted1024
  maintenance calls on a state immediately discarded; not an equal-evidence rival.
- Learned-writer stream: initial, correction, clear, rewrite, reset, new scope;
  64 ticks per phase with background writes, denied and wrong-scope events. Each
  tick inserts noise and one maintenance sweep. Gold graph is for scoring only.
  Valid writes install a full representation; binding mistakes are preserved.
- Boundary faults: identity absent from dictionary; wrong dictionary geometry;
  substituting a different VALID code at a relevant edge; erasing its value.
  These are information/validity boundaries, not necessarily recoverable cases.

## Criteria fixed before main
Primary reader: record_hop; gated_hop secondary confirmation, no best-seed choice.
A scoped compatible-repair candidate passes nominal screens when known and UNKNOWN
accuracy are each>=95% IN EVERY PAIR at appropriate depths for clean4, key/value/both
.02×64, both.02×1024 h8 and all lifecycle endpoints. Known/unknown categories absent
at a phase are not invented; their metrics are null and that category is not tested.
Query.2 and sigma.08 are separately reported robustness screens, not an excuse to
replace the nominal metrics. Core causal claim additionally needs paired improvement
under corruption versus no repair. Exact cleanup can win; no general-family verdict.

No pass is production qualification or full NBR-01 closure. Presence is protected;
canonical vocabulary is given; no natural language, unknown truth, or unlimited
capacity is established. Extra1/2/4/8 computation stays evaluation-weight-frozen.

## Evidence and verification
Save per-example final answers at all four depths, canonical parent graph, query,
room IDs, presence, decoded stored identities and final-buffer hashes. Independent
NumPy/Python graph scorer recomputes targets/metrics. Replay all five evaluations
fresh; reproduce one complete1800-step fit; exercise complete state/RNG snapshots
and compatibility rejection. Count actual completed training/evaluation work and
raw buffers, plus dictionary/new parameter costs and temporary allocation caveats.
Original archives hash/CRC before/after, no edits or merges of release directories.
