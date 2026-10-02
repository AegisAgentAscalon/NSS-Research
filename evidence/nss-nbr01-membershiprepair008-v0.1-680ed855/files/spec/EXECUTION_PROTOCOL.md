# MembershipRepair008 — execution protocol v1

This is the resolved execution contract following research plan v0.1. It is a
local preregistration, not an external preregistration or production acceptance.
See EXECUTION_LOCK.json for timestamp, source identities, fitted artifacts and
operating thresholds frozen BEFORE confirmatory episode evaluation.

## Scope and preparation
NBR-01 only. Frozen Study006 readers record_hop/gated_hop and learned binder
801–805; Study007 learned_dictionary 901–905. Protected 16-row identity reference,
17 coordinates, 16-record relationship store, protected relation-presence flags.
No runtime parameter adaptation, gradients, optimizer, or quantization. Existence
maps from Study005 are not silently imported. The current representation remains
synthetic, fixed capacity, explicitly addressed by supplied numerical identities.

One development gate fit, seed1000, 1,200 AdamW steps, batch256. Preparation caps:
max two gate recipes/2,400 dev steps; only one used. Pilot calibration 1,024/class.
A bug in preserving soft UNKNOWN outputs was found in the first development
pipeline run and corrected: the original ABI's UNKNOWN sentinel competes with
known codes even when the numerical null is not exactly e17. Failed pilot logs
are preserved; their missing-relation failure was an implementation defect, not
an architecture finding. Post-fix dry runs used disjoint development episodes.

Five main match-head fits, seeds1001–1005, 1,200 AdamW steps each, batch256,
lr0.002, weight_decay0.0001, norm clipping1. Eight invariant input features;
8→24→16→1 tanh head. Only head parameters train. Labels say whether the nearest
candidate matches a registered origin. Training covers same-family random novel
vectors, noisy knowns, near-novel and mixtures, reference counts8/12/16.

Training, calibration and confirmatory episode generators use disjoint seeds.
Calibration has 4,096/class for seven declared classes. A maximizes average
correct acceptance over exact, q05, q20, raw02 and raw08 known inputs subject to
<=0.5% observed FPR on EACH independent novel class. Search distance-squared
0.02..1.8 (180 levels) and distance margin0..0.5 (26 levels). B uses the lowest
sigmoid threshold satisfying the same FPR constraint. Both use the same data;
B also has its separately counted training data. These are operating thresholds,
not a claim of globally calibrated probabilities. No main-data refits allowed.

## Candidates
none, normalization, unconditional nearest, prior learned repair,
A gate + nearest, A gate + learned repair, B gate + nearest, B gate + learned,
and reject-all. Stage A adds distance-only and margin-only ablations using A's
selected values without extra tuning. Frozen parent weights stay pinned.
Raw pre-projection features determine admission. UNKNOWN is not an identity.
Unconditional controls still respect the explicit UNKNOWN competitor.

## State and query semantics
Inactive reference rows contain zeros, never future codes. REGISTER supplies a
canonical code through an explicit permitted event, uses the first free row, and
creates no relationship. Exact duplicates return duplicate; near duplicates get
separate rows if capacity exists (query ambiguity is not hidden by a merge).
Denied/wrong-scope/full registry events do not replace records. References have
per-stream revisions. Scoped readers reject a declared mismatching revision.

Rejected queries do not mutate records. Present fields that fail membership
remain present and retain available raw data, but become sticky-unreadable until
an explicit qualified write/clear updates that field. Independent later noise
may change the raw field but is NOT treated as new corroborating evidence.
Registration does not automatically reconsider quarantined fields. This is a
conservative tested policy, not a universally optimal reassessment policy.

All learned traversal remains the actual inherited neural matcher (and GRU for
gated_hop). Matching must survive every intermediate and final decode. A rejected
path cannot fall through into a forced final room decoder. Exact traversal is a
labelled control operating on the SAME actual store; it is not gold installation.

## Confirmatory data and design
Stage A: 1,024 independent episodes per family/pair, 18 families at count16 plus
known_q20/novel at counts8/12: 22 strata. Families include exact, q05/q20, random
novel, same-normalized noisy novel, q40, scaled knowns, erasure, explicit UNKNOWN,
near novels (0.1/0.3/0.6 additive noise then normalization), mixtures, raw storage
noise, and genuinely removed reference members. Reverse-reference permutation
interventions and 1,024 paired identical-observable origin cases per pair.
Random independent novel classes are core; near collisions/scales/severe noise
are stress. Identical observables cannot be origin-discriminated by any arm.

Stage B: batch64, half complete/half missing graphs except all-novel starts.
Depth1/2/4/8. Clean4, keys02/values02/both02 at64 ticks, both02 at1024 ticks with
8-link graphs, and separate both08 at64 stress. Each noise field receives matched
independent draws across candidates; actual maintenance cadence is independent
of query rounds. Query-only q05/q20, random novel, near novel0.1, q40. Exact
installation isolates repair; a separate live-write lifecycle uses the old binder.

Writable lifecycle starts with12 registered identities, four masked zero rows:
before REGISTER, after REGISTER with no relation, first write, correction, clear,
rewrite, full scope reset, fresh scope + registration + write.64 noise/background
event ticks/phase; valid, denied and wrong-scope events. Neighbor queries repeat
after each original-scope phase. Truth is derived independently from the explicit
events, not from what the candidate successfully managed to store. Near-collision
registration/write is a separate stress case. Checks are at declared query points,
not every possible intermediate moment. No 4,096 idle extension in this run.

Stage C: nearest, A-nearest, B-nearest, fixed schedules every8/every32/read-time
on the same 1,024-tick graphs. Every-tick reference already in Stage B. Cadence
is a registered diagnostic even if the stringent overall joint screen fails;
no winning schedule is chosen after unrestricted search.

Additional controls: remove state; erase one value; replace a value with another
valid code; common-mode key/value noise. No full-codebook tampering benchmark
beyond software integrity/version tests in this pass. Strong generic-reader
retraining remains NOT_RUN: it is not invoked automatically to repair main scores.

## Screens (retained, despite pilot showing a tradeoff)
Core known retrieval >=95% each pair at sufficient depth; core missing >=95%.
Independent-novel empirical false identity acceptance AND unsupported terminal
<=1% each pair. Known repair regression <=1 percentage point versus corresponding
unconditional arm, plus95% floor. Valid ordinary registration/write lifecycle
>=95%; software boundary tests all pass. The q20 condition remains core even
though the pilot gate lost coverage there. Do not report only the easier success.
Reference counts8/12 and near-collision/severe noise are separately reported.

Per-episode metrics, per-seed variation, paired effects, Wilson descriptive
intervals, and all false identity accepts even when final answer is UNKNOWN.
Hops are not independent trials. Lower-bound marker/readable assumptions are
reported explicitly. No external reliability probability or NBR-01 closure claim.

## Resource and reproduction
CPU only, one Torch compute thread, deterministic operators; no downloads or
network calls. Target ceiling4GiB peak resident process, 30min measured main
compute; if exceeded preserve partial work, no reducing horizons post-failure.
Costs include frozen models, working vectors/flags/masks/revisions, temporary
features/logits/projections, head training/optimizer/calibration; measured process
RSS is additional to raw array accounting. No equally matched FLOP claim.

Replay all main prediction arrays in new interpreters. Reproduce one complete
1,200-step head trajectory and calibration. Independent graph/identity scorer
must not import candidate metrics. Test scoped snapshots including active mask,
readability, reference revision, gate/model identities, RNG and partial query.
Fresh ZIP extraction: manifest, unit tests, complete rescoring, selected full
pair replay and continuation checks. Windows/third-party/long-term validation
are not performed in this environment. All input archives remain unchanged.
