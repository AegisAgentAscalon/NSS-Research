# Q010 ExecutionValidation v1.5 — measured execution-gate checks

## Decision

The requested focused runtime pass is completed, with explicitly retained
historical-verifier limitations. The repaired fit operator can checkpoint and
continue short real training trajectories exactly; a development evaluator can
resume both an uncommitted condition group and interrupted final publication
without losing completed work. The final corrected copy reproduces the archived
v1.3 development arrays, metadata and independent scores exactly.

This is NOT completion or scientific qualification of full Q010. It is not a new
neural architecture experiment. No scientific thresholds, model layers, loss,
optimizer equations, seed derivation or scoring tolerances were changed here.

## 1. Crucial status reconciliation

The runtime contained the separately delivered
`Q010_v1.4_All15_MainWeights_Backup.zip`,60822187bytes, SHA256
`c03c1211c1ed9b2db2684d9f14bd648a0505cae1eb93eea21c838d69d278f2d3`.
All1997 manifest-covered members matched. All15 safetensors exports matched their
raw hashes, strict dtype-inclusive digests and public model fingerprints; every
model loaded into its declared architecture. Their saved numerical traces contain
6000 finite-loss rows with contiguous update counters. No such fit was retrained.

The scalar readers contain818parameters and the reconstructed attention readers
86464parameters. These are the reconstructed v1.4 models, NOT recovery of the lost
original Qualification010 attention checkpoint or its reported94728parameter model.

The backup explicitly excludes full optimizer/RNG checkpoint payloads and full
raw main-evaluation evidence. Existing reproduction/qualification JSONs survive as
prior reports, not a substitute for those raw artifacts. Verification of exports
and traces cannot establish that every historical optimizer operation occurred as
recorded or freshly reproduce full training. The exports remain useful for
inference and regeneration of evaluation evidence.

The later source-only patch's0/15 counter must not be used as the whole-project
training status. Two separate branches happened to use v1.4 labels. This package
keeps their identities separate and its STATUS.json records both.

## 2. Source preparation and one additional correction

The original159379330byte InfrastructureRepair v1.3 and62149byte SourceRepair v1.4
archives match their recorded hashes. The preparation helper successfully created
new, separate workspaces. All10525 parent members and22 source-patch members were
verified before/after; the original archives were not changed.

The first new24-test contract suite found one real path-boundary defect:
`execution_io.file_info()` resolved a supplied path BEFORE checking for symlinks.
That could hide an in-root symlink and record its target as if it had been the
supplied artifact. The v1.5 change keeps lexical components until containment and
symlink checks complete, and rejects outside-root paths explicitly.

The failed test, old source, and exact diff are retained. This correction does not
change numerical behavior. The other23 checks in that first run passed. All24
passed against the corrected source. No test threshold was relaxed.

Our validation driver also initially requested `rng_state` instead of the actual
checkpoint field `rng_states`. The failed comparison and pre-correction driver
are retained; correcting the fixture field allowed the full RNG state to be
compared. This was a test-harness mistake, not a learned-model failure.

## 3. Real fit continuation

On both the original repair and final corrected copy, all three training variants
were tested with an unchanged6000-update planned recipe:

- one invocation executing40updates;
- a separate identical trajectory executing17updates, then a fresh process
  continuing23updates to the same40-update point.

Model tensors, optimizer state, all saved RNG states, data-stream state/cursor,
identity and numerical loss/data/gradient trace fields matched exactly. Measured
wall-time trace fields were excluded from numerical identity; raw receipts remain.
These are early teacher-forced validation prefixes, not completed main fits or a
new measurement of the later free-running phase.

An additional actual process was SIGKILLed after its step20 joint commit existed.
The incomplete attempt and its missing END were retained. A separately pinned
review used the measured outer command wall as a conservative duration bound.
A new process restored step20 and reached40, exactly matching the uninterrupted
reference. Work after the last commit and before the kill is not exactly counted.

The shared comparison receipt initially reused the regular17+23 description for
that kill test. A separate erratum corrects the description to20+20; the original
receipt is preserved and the checked numerical equality is unchanged.

A real bootstrap/fit CLI invocation with a tiny soft interval retained a zero-step
checkpoint and returned an explicit pause. It did not perform an optimizer update.
The soft interval applies to the update loop, not to setup/serialization time;
that command took about6seconds in total. It is not a1ms hard execution guarantee.

## 4. Roster, source and rejection checks

All15 real zero-start factories were exercised against the operator's expected
identity checker, with zero updates. The protocol/start-lock chronology was
constructed without self-reference. These generated protocol/lock files are
explicit VALIDATION fixtures, not a main-study freeze.

The24 new contract tests include synthetic fifteen-fit roster loading and negative
cases for wrong seed, development phase, incomplete update cursor, swapped paths,
missing fits, public-versus-strict hash substitution, mutated evidence, malformed
resume reviews, no-overwrite publication, and duplicate operator leases.
Synthetic completed cursors exist ONLY inside unit-test fixtures; they are not
trained checkpoints and never contribute to a scientific result.

A rejected restore was tested against real live trainer state; model, RNG and
cursor remained unchanged. Existing producer tests also cover optimizer/restore
rejection. Five bootstrap tests check fresh-copy behavior, source drift before
numerical dispatch, wrong pins and truthful read-only status reporting.

## 5. Evaluator and final publication

The unchanged development selection was used: seed91401, four cases per ordinary
condition (from both support strata), and the declared lifecycle frames. No main
held-out conditions were scored in this pass.

Sequence tested with real numerical evaluation:

1. Commit two groups of eight conditions and return explicit pause.
2. Restart; finish a third group's capture but deliberately fail before committing
   it. Retain the uncommitted attempt.
3. Refuse continuation without a pinned failure/cost review.
4. Resume after review, complete all remaining groups, then deliberately fail
   after the first final-view copy. Preserve that partial publication.
5. Resume with both failed attempts accounted for; reuse committed groups and
   publish a new complete view.

The resumed capture matched uninterrupted execution across129frames,
10167arrays/2675104elements, and every case/query/event metadata object. The
corrected v1.5 copy independently produced the same output as the archived v1.3
successful development capture. All64condition types remained present, including
fault, lifecycle, depth and long-horizon entries. This is coverage of a small
reused development dataset, not fresh statistical evidence for competence.

The independent scorer regenerated source/event-ledger labels and checked pointer
arithmetic/decoding:2880query chains and19104logical stage audits. Its CSV was
byte-identical to the retained v1.3 development scores. No numerical contract
amendment was necessary for these development artifacts.

Invoking the completed capture again checked and returned it without adding a new
attempt or changing any existing capture artifact. Actual arbitrary-instruction
or power-loss recovery, including all final-fit publication crash points, is NOT
established by these tests.

## 6. Current test results

| Suite | Pass | Retained errors |
|---|---:|---:|
| New execution-contract suite |24|0|
| New copy/bootstrap suite |5|0|
| Existing producer suite |93|0|
| Existing batched-state/independent-scorer suite |23|0|
| Archived verifier suite |68|3|
| Total distinct passing tests |213|3|

Repeated suites and prefix comparisons are not added to the distinct test count.
The separate sequence/kill/capture/zero-start checks above are also reported in
their actual receipts, not converted into an inflated unit-test total.

The three archived verifier errors remain exactly the known categories: two
require byte equality to older Windows-generated numerical fixtures; one refers
to an unavailable historical lifecycle fixture. Logs and failures remain. They
were not overwritten, retargeted, skipped into passes or assigned looser tolerances.
Current source/event-ledger/arithmetic development checks pass on freshly generated
Linux evidence. This does not claim arbitrary cross-platform exact equality.
The original full1111-test suite and independent external replication were not run.

## 7. Execution environment and transport

Python3.13.5, PyTorch2.10.0+cpu, NumPy2.3.5; Linux; CPU quota400000/100000
(approximately4CPUs), cgroup memory cap4294967296bytes(4GiB). Math workers used one
intra-op/inter-op thread. No models, packages, private datasets or services were
downloaded or installed. This is not a Windows/GPU benchmark.

The largest monitored process-tree RSS sample in these checks was approximately
675MB, from the producer regression suite. Sampling is not an OS-enforced exact
peak. Concurrent command times are not additive elapsed wall time or a performance
comparison. Raw command starts, ends, exits and sampled resources are in logs/.

One long outer tool call timed out as its attention validation job was closing.
The child step40 commit and END survived; the supervisor's final receipt did not.
No active child remained, and its output was verified rather than retrained.
The incident is explicitly recorded. Later longer checks used a separate bounded
supervisor whose actual process and log were polled during this turn.

## 8. What is ready, and what is not

Ready within the tested local scope: exact short fit continuation, verified
checkpoint/roster rule checks, source-before-import rejection, explicit pauses,
retained failed attempts and costs, cooperative group resume, final capture-view
recovery, and unchanged numerical development outputs through independent scoring.

Not claimed: complete whole-study resource accounting/enforcement; every possible
crash point; cross-host/relocated live trainer restore; runtime acceptance of a new
main protocol; a completed full Q010 archive; new6000-update fits; integrated NSS;
NBR02; or learning-state quantization. The source-only patch's broader main-phase
budget and freeze obligations are not silently declared complete by this pass.

The next recovery job should use the surviving fifteen final weight exports to
regenerate/verify main evaluation under their ORIGINAL declared experiment, with
an explicit inference-only loader. It must not forge missing full optimizer
checkpoints or silently reinterpret those models under the validation fixture's
protocol/seed domain. The previous post-capture underflow amendment rationale is
preserved among prior documents; full main numerical verification needs its own
explicitly identified implementation and receipts, not a claim that it was run
here. Preserve all prior scientific negatives.

## Evidence index

`STATUS.json`; `results/SAVED15_AUDIT.json`; `results/SYMLINK_REPAIR.diff`;
`results/CAPTURE_RESUME_EXACT_v14.json`; `results/ARCHIVED_DEVELOPMENT_PARITY.json`;
`results/SCORE_PARITY.json`; `results/CONTROLLED_KILL.json`;
`results/KILL_RECEIPT_DESCRIPTION_ERRATUM.json`; `results/TRANSPORT_EVENT.json`;
`evidence/validation_v15/CONTINUATION_*.json`; allcommand receipts in `logs/`.
Fresh extraction is recorded in the separate delivery receipt.
