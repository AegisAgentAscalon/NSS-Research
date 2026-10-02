# NSS NBR-01 / ExistenceContent005
## Learned existence, frozen contents and writable absence

**Standalone research package v0.1 · main study RUN · full NBR-01 OPEN**

Place beside WritableEmpty004 in `MegaMind_Alpha_Proto`. Do not merge this into
the v0.5.0 foundation. The eight supplied ZIPs remain recovery/reference inputs;
no serving architecture, model generation or generic Forge/Runtime is updated.

## Decision brief

**A learned, noise-exposed existence state passed the complete nominal writable
memory lifecycle without adding content errors relative to protected existence.**
Both the one-coordinate and four-coordinate candidates passed all five paired
nominal screens and the extended 4,096-round empty-then-write screens. They are
not protected Boolean flags: their continuously valued existence state receives
noise, and its restoring map contains actual trained weights.

This is a scoped mechanism result, not universal reliability. Every nominal
read was correct in 319/320 streams, not 320/320; the same remaining content-error
pattern occurred with protected existence. Stronger corruption breaks these
mechanisms. The simple fixed-restoration controls matched nominal performance
and were stronger under some stresses. The finite nearest-prototype control
remains excellent. No superiority over those simpler controls is established.

**Keep learned existence/content separation as a viable research candidate. Keep
protected and fixed-rule existence as engineering references. Do not adopt the
jointly retrained content/existence map on this preparation. Do not infer that
learning is necessary where a small exact rule is already sufficient.**

## 1. What was inherited and what was learned

Five frozen 16-D representations from HorizonBinding002 (301–305) and their
2,128-parameter StateRecovery003 content-repair parents (501–505) were reused
byte-for-byte. The unsuccessful WritableEmpty004 content revisions were NOT used
as parents. Each source contains eight finite value codes and a supplied code
for no established record. These are not language-capable companion models.

New paired learning seeds701–705 produced 15 checkpoints: five 49-parameter
scalar existence maps, five 148-parameter four-coordinate maps, and five
2,257-parameter coupled17 revisions. Each took1,800 AdamW steps. Totals are
**27,000 completed optimizer steps**, **3,456,000
sequence presentations**, and **21,288,576 within-sequence
supervised presentations**. Inputs are paired/reused between arms, not independent
real-world experiences. Three separate development fits on representation141 and
seed641 totalled5,400 steps; their failures and earlier scoring are preserved.

All weights remain fixed during evaluation. Paired candidate arms receive the
same generated source episodes, labels and step budgets. Different coordinates,
objectives and trainable surfaces are used. This is NOT a matched-compute or
matched-total-parameter architecture ranking. The original content map was
prepared earlier, not obtained for free by freezing it now.

The development pair's old content map itself was weak under chronic noise.
Controls exposed that weakness. No main seed was filtered or tuned away; all
five registered seeds remain in every aggregate. Scientific source and protocol
hashes were locked before main fits and scoring; see spec/REGISTRATION.json.

## 2. Candidate state and transitions

**One-coordinate separation:** retain16 content floats and one existence float
per record. An accepted write installs the full content code and presence+1;
clear installs content0 and presence−1. A learned49-parameter map maintains the
existence coordinate. The old content-repair map is frozen. Presence is read
from the sign; that sign convention is supplied, not learned write qualification.

**Four-coordinate separation:** use the same16 content floats plus four redundant
existence coordinates. A148-parameter network maintains that four-dimensional
state. Presence is decoded from the mean sign. Four coordinates cost more state
and provide redundancy; they are not four independent facts or free capacity.

**Coupled17:** use the same17-float state budget as the scalar split candidate,
but initialize a dense17→64→17 recurrent map from the old content parent and
refit it jointly. It receives the same existence-code convention. Thus simply
adding a distinct absent code is not the sole difference: preserving versus
jointly refitting the content dynamics and the allowed cross-couplings differ.
Failure here does not prove that all joint architectures fail.

**Fixed controls:** one float restored to its sign, or four floats restored to
the sign of their mean. These have no newly learned maintenance parameters but
receive the same noise and use the same state bytes and write/read conventions
as their learned counterparts. The protected-Boolean control separately keeps
one undamaged Boolean byte per record. The nearest-prototype control projects
onto the shared nine-code catalogue and keeps its original16-D state budget.

All explicit-existence arms use a declared guard: after maintenance, a state
inferred absent clears its content vector. The guard is NOT protected by an
oracle in neural arms. A wrong existence sign can therefore erase a valid
content state; a subsequent stable sign is not evidence that the value survived.

Writes and clears remain supplied, explicit operations. Four addresses, full
value encoding, exact score≥0.5 qualification and scope checks are given. This
study does not learn which sentence is worth remembering or which entity a
pronoun refers to. A low qualification score is not multiplied into write
amplitude. No source facts, authority or permissions are inferred from a sign.

## 3. Whole lifecycle and a stricter existence check

Each configuration uses64 four-address streams. Two neighboring records start
populated; the focus and another record start empty. The focus follows:

**Empty → first write → correction → clear → rewrite.**

Each phase runs1,024 fresh noise rounds, totalling5,120 rounds per stream.
Complete legitimate writes must work immediately, including after a4,096-round
empty interval in a separate condition. Wrong-scope and just-below-threshold
writes are no-ops for content and existence. A final global clear is also tested.

Noise is additive Gaussian in the declared normalized numerical coordinates.
It affects **every neural content and existence coordinate**. The Boolean control
is explicitly exempt from existence noise; that protection is additional
information durability, not neural ability. Standard deviations0,0.15 and0.30
are tested; fresh training noise reached0.15. These are synthetic numerical
stress levels, not calibrated physiological or hardware-fault measurements.

Every read is saved, including its existence estimate. The strict whole-stream
metric requires both the answer and record-existence status to be right at
every step. An incorrect presence signal hidden behind an UNKNOWN content answer
cannot count as a perfect stream. `read_status()` distinguishes empty from
present-but-unreadable; neither status certifies truth. This explicit distinction
was added before main registration after development exposed the scoring gap.

Nominal acceptance requires all phase endpoints≥95% for known/UNKNOWN answers,
immediate valid writes≥95%, and≥95% streams correct at every read/status, in
all five seeds. Same-condition samples are paired; the five learned seeds—not
the millions of stored array positions—define replication.

## 4. Main nominal-noise results

At the final rewritten endpoint under0.15 fresh noise, means±sample standard
deviations across all five paired seeds are:

| Mechanism | Known at final endpoint | UNKNOWN at final endpoint | Correct existence status | Every read/status correct, full stream |
|---|---:|---:|---:|---:|
| Original content recurrence | 99.90 ± 0.23% | 0.00 ± 0.00% | 75.00 ± 0.00% | 0.00 ± 0.00% |
| Original + protected dynamic existence | 99.90 ± 0.23% | 100.00 ± 0.00% | 100.00 ± 0.00% | 99.69 ± 0.70% |
| Frozen content + learned 1-coordinate existence | 99.90 ± 0.23% | 100.00 ± 0.00% | 100.00 ± 0.00% | 99.69 ± 0.70% |
| Frozen content + learned 4-coordinate existence | 99.90 ± 0.23% | 100.00 ± 0.00% | 100.00 ± 0.00% | 99.69 ± 0.70% |
| Jointly retrained 17-D content/existence | 100.00 ± 0.00% | 91.88 ± 8.15% | 97.19 ± 2.25% | 0.94 ± 2.10% |
| Frozen content + fixed sign restoration | 99.90 ± 0.23% | 100.00 ± 0.00% | 100.00 ± 0.00% | 99.69 ± 0.70% |
| Frozen content + fixed mean/sign restoration (4) | 99.90 ± 0.23% | 100.00 ± 0.00% | 100.00 ± 0.00% | 99.69 ± 0.70% |
| Frozen content + unmaintained existence coordinate | 15.73 ± 1.07% | 59.38 ± 5.63% | 53.75 ± 4.87% | 0.00 ± 0.00% |
| Nearest-prototype maintenance | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% |

The learned split1 and split4 candidates matched the protected control's complete
nominal answer AND existence traces, not just rounded means. A post-analysis
bytewise array comparison records all20 pair/mode equality checks in
`evidence/NOMINAL_EQUALITY_DIAGNOSTIC.json`. The one failed stream is a content
error also present with protected existence. At the final endpoint, one of960
known-record answers is wrong, yielding99.895833%;319/320 complete streams are
correct at every read, yielding99.6875%. Neither is100%.

Both neural split mechanisms maintained all nominal empty statuses while accepting
first writes, corrections, clears and rewrites. Joint retraining reached100%
known recall at the final endpoint, but91.875% UNKNOWN and only0.9375% fully
correct streams. Its final endpoint conceals widespread earlier errors. Preserving
an answer at one time is not equivalent to preserving a usable record lifecycle.

| Mechanism | Clean joint screen | Nominal joint screen | Extended screen |
|---|---:|---:|---:|
| Original content recurrence | 5/5 | 0/5 | 0/5 |
| Original + protected dynamic existence | 5/5 | 5/5 | 5/5 |
| Frozen content + learned 1-coordinate existence | 5/5 | 5/5 | 5/5 |
| Frozen content + learned 4-coordinate existence | 5/5 | 5/5 | 5/5 |
| Jointly retrained 17-D content/existence | 5/5 | 0/5 | 0/5 |
| Frozen content + fixed sign restoration | 5/5 | 5/5 | 5/5 |
| Frozen content + fixed mean/sign restoration (4) | 5/5 | 5/5 | 5/5 |
| Frozen content + unmaintained existence coordinate | 5/5 | 0/5 | 0/5 |
| Nearest-prototype maintenance | 5/5 | 5/5 | 5/5 |

The clean screens are reported under the same95% joint thresholds; all observed
clean lifecycle scores were100%. Extended qualification also requires correct
existence estimates and the pre-write every-read criterion. No failed seed was
excluded or replaced.

## 5. What stronger noise reveals

Under0.30 noise on both content and existence, the learned scalar is no longer
reliable. Redundant learned existence retains status much better, but cannot
repair failures of the old content map:

| Mechanism | Known at final endpoint | UNKNOWN at final endpoint | Correct existence status | Every read/status correct, full stream |
|---|---:|---:|---:|---:|
| Original content recurrence | 66.88 ± 5.65% | 0.00 ± 0.00% | 75.00 ± 0.00% | 0.00 ± 0.00% |
| Original + protected dynamic existence | 66.88 ± 5.65% | 100.00 ± 0.00% | 100.00 ± 0.00% | 8.75 ± 4.50% |
| Frozen content + learned 1-coordinate existence | 6.67 ± 1.58% | 54.37 ± 1.31% | 53.12 ± 4.66% | 0.00 ± 0.00% |
| Frozen content + learned 4-coordinate existence | 66.77 ± 5.50% | 99.69 ± 0.70% | 99.77 ± 0.35% | 8.75 ± 4.50% |
| Jointly retrained 17-D content/existence | 65.00 ± 12.96% | 25.94 ± 11.72% | 71.17 ± 4.24% | 0.00 ± 0.00% |
| Frozen content + fixed sign restoration | 24.17 ± 4.11% | 51.25 ± 8.87% | 56.88 ± 2.61% | 0.00 ± 0.00% |
| Frozen content + fixed mean/sign restoration (4) | 66.88 ± 5.65% | 100.00 ± 0.00% | 100.00 ± 0.00% | 8.75 ± 4.50% |
| Frozen content + unmaintained existence coordinate | 9.69 ± 2.35% | 52.50 ± 6.50% | 53.20 ± 3.21% | 0.00 ± 0.00% |
| Nearest-prototype maintenance | 100.00 ± 0.00% | 100.00 ± 0.00% | 100.00 ± 0.00% | 99.69 ± 0.70% |

The four-coordinate learner has99.765625% final existence accuracy and99.6875%
UNKNOWN answers, but only66.770833% known recall. Protected existence itself has
only66.875% known recall. This isolates why protecting the status alone does not
solve stronger content corruption. The nearest-prototype control still passes
the declared joint screen, with99.6875% fully correct streams at this stronger
noise level—not perfect all-time behavior.

### Presence-only perturbations: redundancy is useful, not magical

A separate2,048-round condition perturbs only existence; content receives no
fresh corruption. The four-coordinate candidates are compared with equal-byte
fixed mean/sign controls. Identical-coordinate (common-mode) noise removes the
independent-noise advantage:

| Existence mechanism | 0.30 independent: correct status | 0.30 independent: every-read stream | 0.30 common-mode: correct status | 0.30 common-mode: every-read stream |
|---|---:|---:|---:|---:|
| Frozen content + learned 1-coordinate existence | 51.72 ± 2.11% | 0.00 ± 0.00% | 51.72 ± 2.11% | 0.00 ± 0.00% |
| Frozen content + learned 4-coordinate existence | 100.00 ± 0.00% | 100.00 ± 0.00% | 53.52 ± 1.66% | 0.00 ± 0.00% |
| Frozen content + fixed sign restoration | 58.59 ± 3.90% | 4.06 ± 2.84% | 58.59 ± 3.90% | 4.06 ± 2.84% |
| Frozen content + fixed mean/sign restoration (4) | 100.00 ± 0.00% | 100.00 ± 0.00% | 58.59 ± 3.90% | 4.06 ± 2.84% |
| Jointly retrained 17-D content/existence | 65.55 ± 16.09% | 0.00 ± 0.00% | 65.55 ± 16.09% | 0.00 ± 0.00% |
| Frozen content + unmaintained existence coordinate | 57.19 ± 2.04% | 0.00 ± 0.00% | 57.19 ± 2.04% | 0.00 ± 0.00% |

The learned four-coordinate and fixed four-coordinate mechanisms both achieve
100% status and whole-stream correctness under independent0.30 presence-only
noise. The learned four-coordinate mechanism falls to53.515625% status accuracy
and0% fully correct streams under common-mode0.30 noise. The fixed control also
fails, though its final status and whole-stream figures are higher. This supports
redundancy as an explanation; it does not establish a special biological circuit
or a learned advantage over the exact mean/sign rule.

At0.45 independent presence noise, the fixed four-coordinate control is markedly
stronger:95.9375% fully correct streams versus4.375% for the learned map. All
these adverse results remain in SUMMARY.json and the stored traces.

There is also a rare scalar failure at0.15 in this DIFFERENT presence-only
trajectory: one of320 streams develops false presence while the reader still
answers UNKNOWN. Its endpoint answer scores remain100%/100%, but existence
accuracy is99.921875% and full-stream success99.6875%. The revised scorer catches
this. Passing the registered primary screens is not a guarantee of no rare
errors on another sample at the same noise level.

## 6. Targeted faults and controllability

Inverting one of four existence coordinates is recovered by both four-coordinate
mechanisms on the tested clean fault cases:100% known, UNKNOWN and existence
accuracy. Inverting all coordinates is a different valid code, not a small
repairable disturbance. It changes the decoded meaning and can erase contents.
A stable resulting attractor is not proof of the original record.

Erasing all existence coordinates to zero is also NOT an explicit clear. Zero
is between the declared ±1 existence codes. The coupled model recovered the
correct tested status from still-intact content in that specific fault condition,
where split mechanisms cannot generally infer the erased status. This is a real
advantage of cross-information in this condition, retained despite coupled17's
lifecycle failures. We do not discard favorable evidence for a rejected candidate.

Erasing a populated content vector does not recover its value merely because
presence remains positive. Explicit existence can instead report present-but-
unreadable. With no exact value copy supplied to the cell, these candidates cannot
establish the erased identity. Subsequent legitimate writes/clears are evaluated
separately; they are not reported as spontaneous memory recovery.

### Partial write delivery

A separate challenge first authorizes a write, then attenuates its delivered
representation. This is NOT uncertainty about whether the observation qualified.
All candidates accept full legitimate writes and their tested16-round clean
continuations. At half CONTENT-only delivery from empty, both learned split
candidates achieve100% focus recall: the correct +1 existence code was intact.
At half delivery of the WHOLE neural state, the presence code interpolates from
−1 to+1 and arrives at0; both learned split candidates achieve60% focus recall
across five seeds. Fixed sign controls treat zero as absent and achieve0%.
The coupled arm reaches90% in this specific case, but fails the broader lifecycle.

This reinforces that a committed write must establish BOTH the new record's
existence and its value representation. A strong maintenance mechanism is not
obliged to reconstruct arbitrarily incomplete writes. The research operation is
synchronous; production power-loss atomicity for this new state format is NOT_RUN.

## 7. Resource and preparation accounting

| Mechanism | Raw state/stream | Active repair/existence parameters (bytes) | Median maintenance + read, batch64 |
|---|---:|---:|---:|
| Original content recurrence | 256 B | 8512 B | 283.7 µs |
| Original + protected dynamic existence | 260 B | 8512 B | 381.0 µs |
| Frozen content + learned 1-coordinate existence | 272 B | 8708 B | 397.2 µs |
| Frozen content + learned 4-coordinate existence | 320 B | 9104 B | 372.5 µs |
| Jointly retrained 17-D content/existence | 272 B | 9028 B | 316.7 µs |
| Frozen content + fixed sign restoration | 272 B | 8512 B | 331.2 µs |
| Frozen content + fixed mean/sign restoration (4) | 320 B | 8512 B | 346.9 µs |
| Frozen content + unmaintained existence coordinate | 272 B | 8512 B | 325.2 µs |
| Nearest-prototype maintenance | 256 B | 0 B | 172.4 µs |

All modes additionally use4,072 raw bytes of shared representation/readout
state. The convenience loader also holds the8,512-byte parent even for modes
that do not execute it; this is explicitly recorded, not silently counted as
zero process memory. The16-D baseline uses256 raw activation bytes/stream;
one existence float per address raises this to272 B, and four to320 B. Protected
existence uses260 B, with four Boolean BYTES, not four packed bits.

The49/148 new existence parameters are shared across records. They do not
replace the parent model's weights or training cost. Everything here isfloat32
except the explicitly protected Boolean and saved discrete prediction arrays.
No low-bit weights, traces, gradients or packed execution were evaluated.

Main training loops used108.84s of summed worker CPU
time and108.33s summed per-job loop wall time.
Development and exact reproduction are accounted separately. Training processes
sampled up to314.84MiB RSS
per worker;10ms sampling can miss peaks. Workers could overlap, and a full
concurrent training-phase peak was NOT measured. Microbenchmarks are descriptive
sandbox CPU timings with possible host contention, not a quality-matched latency
ranking, user-PC budget, or energy result. Source preparation receipts remain in
reference/ and are not included as newly run training.

## 8. Reproducibility and evidence status

The study contains **45 evaluation configurations**,
**9,210 summary rows**, and **308,317,440 stored answer
positions**, including overlapping snapshot reads and complete intermediate
traces. The existence arrays are separately saved and checked. This large number
is NOT a count of independent tasks, environments or subjects.

Full fresh-interpreter verification status at report generation: **PASS**,
45 configurations. It reconstructs truth from source event
semantics, independently rescores every stored answer/status trace, and
re-executes all configurations to compare every saved array and metric. It does
not merely compare final averages. See `evidence/INDEPENDENT_VERIFICATION.json`.

One full1,800-step split4 trajectory (representation303, learning seed703)
reproduced the same training-data digest, final weights and safetensors checksum.
Ninety state/two-RNG snapshots (nine modes×five pairs×two lifecycle cut points)
restored and continued exactly in a fresh interpreter. These are inference-state
continuations, not a claimed optimizer-resume feature. All15 new checkpoint
hashes and registered scientific source hashes were checked unchanged.

**44 research unit tests** cover event qualification, absence/write/correction/
clear/rewrite, neighboring records, meaningful zero symbols, corruptible existence,
separate unreadable status, read purity, state sizes, noisy coordinates and scoped
safe snapshots. **68 unchanged-foundation tests** pass with site packages disabled,
along with dependency and before/after974-file manifest checks. The historical
1,111-test qualification suite, Windows execution and target-device budget remain
NOT_RUN. ZIP-extraction checks are recorded in the external delivery receipt.

All reproduction is internal, not external independent replication. There was no
network model download, private-user-data training, repository merge or deployment.

## 9. Engineering decision and next boundary

**Keep:** the explicit existence/content distinction and the full writable
lifecycle. Both learned split candidates satisfy the primary bounded requirement
under declared conditions without changing the source content-maintenance map.
A mere extra coordinate with no restoring mechanism (hold1) fails, so the
maintenance operation matters—not just allocating space.

**Keep as equally serious controls:** protected dynamic existence, fixed sign/mean
restoration, and nearest-prototype maintenance. Learned maps have not shown a
quality/cost advantage over these simple controls. Choose an exact mechanism when
its assumptions genuinely apply; neural feasibility is not proof of necessity.

**Do not promote on this preparation:** the coupled17 refit. It fails the joint
noisy lifecycle in allfive seeds, despite good clean behavior, some excellent
endpoints and useful content-to-status recovery under a targeted fault. A future
joint candidate must earn its place rather than being ruled out categorically.

The state API must preserve three distinctions: no record established; a record
exists and the reader supplies a value; a record exists but its value cannot be
recovered. These are not factual confidence or permission levels. Changing the
state layout requires a named schema and qualified reset/migration behavior.
Equal dimensions do not imply compatible meanings.

**The next useful research boundary is broader representation/binding and
controlled state interpretation, not an indefinite series of zero-clamp variants.**
Retain these exact learned checkpoints and strong controls as the reference for
that next study. Learning which observation warrants a write, richer unknown/
uncertain content, novel entities and general relationships are still open.
A hypothetical cross-task learned existence transfer or nonzero16-D absence code
is NOT tested here. No architecture replacement or automatic model promotion is
approved by this report.

The frozen participating Primary, task/learning Secondary, reflective Tertiary,
S/T alternation and fallible advisory Validator remain the intended host. This is
a memory-cell mechanism, not an extra core. General language competence, native
reasoning depth, delayed credit, low-bit learning state and full core integration
remain separate experiments. Biological circuitry motivated separating
maintenance and updating; this package does not simulate or establish fidelity
to a human or fruit-fly brain.

**Bottom line:** the bounded writable-absence hurdle now has a trained neural
candidate as well as a strong exact implementation. Its operating limits and
remaining content failures are visible. Carry it forward as a tested building
block—not a claim that general companion memory is solved.

## Evidence index

- `spec/protocol.json`, `spec/REGISTRATION.json`: locked experiment and hashes.
- `spec/DEVELOPMENT_FINDINGS.md`, `evidence/development/`: all development trials.
- `evidence/main/`:15 main checkpoints, logs, initialization and gradient receipts.
- `evidence/results/`, `SUMMARY.json`: all conditions, predictions and statuses.
- `evidence/NOMINAL_EQUALITY_DIAGNOSTIC.json`: post-analysis nominal trace equality.
- `evidence/INDEPENDENT_VERIFICATION.json`: complete independent scoring/replay.
- `evidence/TRAINING_REPRODUCTION.json`: exact complete training reproduction.
- `evidence/RESUME_EXPECTATIONS.json`, `RESUME_VERIFICATION.json`, snapshots.
- `evidence/SOURCE_CHECKPOINT_AUDIT.json`, `RESOURCE_ACCOUNTING.json`.
- Foundation/preservation logs, `MANIFEST.sha256`, external delivery verification.
