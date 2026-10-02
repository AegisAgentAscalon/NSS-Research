# DC01 v0.3 proposed task, split and observation contract

## Public vocabulary and roles

D=23. Coordinates0–19 are one-hot cue features. Coordinate20 primes scope0,21 primes scope1,22 is START. Global cue index is a supplied opaque-to-coordinate public mapping, never derived from labels.

| Group | Scope0 cue indices | Scope1 cue indices | Target exposure |
|---|---|---|---|
| Initial/old | 0,1,2,3 | 4,5,6,7 | Initial fit, probes, diagnostics, later retention |
| Development focal | 8,9 | 10,11 | Development receipts only |
| Held-out focal | 12,13,14,15 | 16,17,18,19 | Held-out receipts only |

For each scope and group independently, use the allocated PCG64 seed to permute that group's indices; the first half have target1, the rest0. Store labels in an isolated generator/scorer ledger. Even though the public schema lists all coordinates, a held-out focal numerical cue never occurs in earlier fitting, fillers, fixtures or development. This is novel association learning over a fixed vocabulary, not semantic or natural-language generalization.

Bases:

    DEV01: (f8,p4),(f9,p5); DEV02: (f10,p0),(f11,p1)
    EVAL01: (f12,p4),(f13,p5); EVAL02: (f14,p6),(f15,p7)
    EVAL03: (f16,p0),(f17,p1); EVAL04: (f18,p2),(f19,p3).

The protected cue is an old association in the other scope. All eight old cues remain unchanged in every condition. Focal reversal is the only mapping change. Two bases form a bookkeeping family, not an independent population sample. Cross each base with d=0,8,32 and reversal r=0,1.

## Initial fitting and cost probes

Each of four initialization pairs has its own PCG64 order stream. Twelve complete permutations of old cue0–7 produce96 transactions, then the first four entries of the next permutation produce100. Every transaction has START, PRIME, CUE and immediate receipt. G/L receive identical data and initial parameter bytes but independent objects and learning state.

The independent cost-probe pair uses six complete cycles and the first two entries of the next cycle:50 updates per method. Those weights are never copied into main fits. No probe has development/held-out focal cues. There is no adaptive choice of the 50/100 length, step size or initialization after inspecting losses.

## Main chronology

Every condition starts from a fresh clone of that arm/fit's100-update checkpoint. Only that start is cloned; subsequent legal receipts change weights persistently until the condition ends. No adaptation carries across conditions.

| Trial | Update cue | Stable label | Reversed-stream label | Primary post-receipt probe |
|---|---|---|---|---|
| 1 | f | initial f label | initial f label | None; retain raw before-feedback prediction |
| 2 | p | old p label | old p label | p |
| 3 | f | initial f label | flipped f label | f |
| 4 | f | initial f label | flipped f label | f |
| 5 | p | old p label | old p label | p |
| 6 | f | initial f label | flipped f label | f |

All six cue-time predictions are saved before their receipt. A probe after trial3's receipt is allowed to benefit from that reversal feedback. It is not scored as having predicted the surprise beforehand. For contrast, the original trial3 prediction remains a raw surprise row.

After each receipt, the worker clears live h, graph/eligibility and pending metadata. Read-only queries use zero scratch h and exactly START/PRIME/CUE. Hash parameters and the empty ephemeral state before/after to verify no query writes. At trial6 end, query each old cue0–7 and f once in that order. X uses no neural transitions but has its own counted exact query path.

One condition has6 update transactions,5 primary scratch probes and9 final inventory queries. Its four learned/frozen implementations are G,L,N_G,N_L for each of4 fits. X runs once per unique base/delay/reversal because its semantic warm table is independent of training order after all old cues have been observed. Its100-receipt initialization checks may be audited for every order, but deterministic X outputs are never multiplied into independent samples.

For each transaction, generate a32-event filler prefix from a seed indexed only by base and trial. Even filler positions use the opposite scope from the scored cue; odd positions use the same scope. Draw a local old index0–3 uniformly, giving a global old cue index0–7. d=8 is its prefix, d=0 empty. Reversal/delay/model variants share those scientific bytes. Filler labels are never supplied. Detached live-state computation is charged in all G/L/N paths.

## Readout definitions

Use stable two-class log-softmax. Decode class0 on a logit tie. Raw pre-feedback accuracy uses the outcome revealed by the current trial's receipt; the output must have been logged before release. Primary probe accuracy/log loss uses the current, already observed label after its receipt. X may output UNKNOWN before first exposure; count this as an unanswered raw query, not a secretly correct label. Primary X correctness after receipt is expected and is not an oracle claim.

Development zero-delay primary probes:4 bases×2policies×5=40 per fit/arm. Held-out primary probes:8×3×2×5=240 unique occasions; at d=0 there are80. Focal primary comparisons use3 probes per stream. Old retention uses the eight old labels, all unchanged; do not count the newly learned or reversed f as an 'unrelated old' association.

## Receipt-rejection/reordered-transaction diagnostic

For each G/L fit, fork its initial-fit checkpoint into a disposable diagnostic. Base old-cue order [0,4,1,5,2,6] is deterministically permuted by positions [1,0,3,2,5,4], yielding [4,0,5,1,6,2]. Each trial has d=8 and the normal old target. Before its legal receipt, inject a wrong-scope receipt and one old-consumed ID (unknown reserved ID on the first trial); both must be rejected before updater dispatch with no pending-state mutation. Then the correct receipt causes one legal update. Probe after trials2–6 only. This gives6 updates and5 probes per fit/arm.

This is not a shuffled-label poisoning test or a permutation among multiple valid pending cues. A correct-ID incorrect authenticated label has no generally observable invalidity under this task; it belongs to a no-detection-limit fixture, not a hidden-gold rejection gate. The disposable diagnostic never seeds main or development conditions.

## Source, seed and ID contracts

`SEED_RECIPE.json` gives120 direct seeds from SHA256(namespace+'|'+label), first8 bytes unsigned big-endian. Namespace is NSS-NBR02-DC01-INTEGRATED-v0.3. Use NumPy PCG64; freeze exact numeric package/runtime versions before generation. Never use another library's differently ordered initializer.

Opaque wire identifiers use SHA256 of UTF-8:

    'DC01-v0.3|'+format(id_seed,'016x')+'|'+phase+'|'+base+'|'+str(d)+'|'+str(r)+'|'+str(trial)+'|'+kind

Take first8 bytes unsigned big-endian. Named phase/base/kind enumerations are frozen before source lock. Zero or scoped collision stops without resampling. Delay/policy IDs can differ while the numerical sequence is paired. Validators receive only current committed messages and current pending metadata; actual future labels, seeds and templates are not worker-readable.

Before fitting: verify all120 direct seeds for in-file uniqueness and compare the declared namespaces/numeric literals with the available prior proposal/reservation scope. That audit cannot see missing historical RNG states. Independently audit legal split support and normalization; retain expected duplicate prefixes and delay/reversal commonality. Wire IDs are not semantic novelty. There are no accidental prior-feedback exposures of held-out focal cues allowed.

Held-out label/input records are instantiated only after all initial checkpoints and A0 outcomes are frozen. The symbolic held-out identities, label recipe and thresholds are already fixed; a failed gate does not authorize choosing easier labels. No source/data lock is claimed by this document.

## Numerical fixture and sandbox faults

Six clean fixture cases reset the same separate initial parameter bytes before each transaction, crossing y=0/1 with d=0/8/32. Use old cue0 for y0,old cue4 for y1, with the corresponding public scope. Fixture targets are diagnostic labels released only at receipt, not values supplied to main fitting. Each G/L case performs one update and one scratch query:12 updates per pass,24 across capture/replay.

Eight isolated deliberately invalid updater cases per pass cross G/L with two fixed diagnostic labels and two application defects: sign reversal or multiplying the prescribed SGD step by2. Their pre-update gradients are calculated normally; the mutated applications occur only in sandbox copies and must be caught by the independent update auditor. Each counts one optimizer/local attempt and one three-cell/one-head forward, including G backward. Never use their resulting weights for any experiment.

Other fault fixtures use synthetic state-machine records, copied fixture arrays or packaging stubs. A live causal-graph assertion is exercised on already-counted clean fixture operations; any additional gradient-engine call must fit an explicitly recorded reservation, not be treated as free. Four derivative-only cases per pass consume24cells/8heads and4G backward calls, with zero optimizer steps.
