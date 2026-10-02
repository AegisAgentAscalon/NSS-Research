# REHEARSE01 v0.1 — newly derived workload
The old three-branch5,272 count is not used. This plan has four branches and two extra batch applications
per context. All counts below are symbolic reservations, not performed model operations or benchmarks.

## 1. Applications
One pass:
* 8 initial fits ×100 =800.
* 96 main method/fit/base contexts ×[2 common +4 tails×4 real receipts +2 extra batches] =1,920.
* Cost probes:2 methods×[10 warmups +2 full20-application contexts] =100.
* 12 clean fixture contexts×20 =240.
* 8 isolated bad batch applications =8.
Total3,068; capture plus genuine adaptive replay6,136, cap7,000 (3,500/pass).
The original PROTECT01 closed3,400 applications remain historical, not resumed unused capacity.
Any zero-gradient update still counts. A failed attempted update is charged. Rejected receipt envelopes
before the updater cause validation work but not an invented optimizer call.

## 2. Forward/gradient count
There are112 full contexts/pass:96 scientific,4 probes,12 clean.
Per context:
18 online gradient prefixes, including three fork reconstructions;
16 replay-gradient prefixes (two batches of8);
180 learned inventory prefixes (9 after18 real applications and2 batches);
60 frozen prefixes (6 cues plus54 inventory queries).
Total274 three-event/head prefixes per context.

Outside contexts/pass:800 initial training prefixes;128 initial learned/frozen inventory prefixes;
20 probe warmups plus16 warm inventories;8 derivative-only prefixes;64 fault-batch gradient prefixes plus8
post-fault queries. Total31,732 prefixes/pass.
Every prefix has3 recurrent cells and1 head; clean waits add3,360 cells/pass.
=>98,556 cells/pass;197,112 cells/capture+replay.
=>31,732 heads/pass;63,464 total.

Regular online applications/pass=2,836; batch applications/pass=232 with8 raw gradients each.
Add8 single derivative diagnostics:4,700 gradient examples/pass, exactly half each method.
=>2,350 G backwards/pass and2,350 L local-gradient examples/pass;4,700 each over replay.
This includes all8×8 fault gradients, not just the fault update count.
Rehearsal source-record fetches=232×8=1,856/pass,3,712 total; F duplicate fetches remain charged.
No QP, active-support SVD, or exact old-margin protective gradient is part of this run.

Exact X:12 main streams +6 case/delay clean streams +2 probe streams, once each rather than repeated
for fits/methods;60 raw-pre/post-inventory query rows/stream =>1,200 rows/pass. All table reads, source
receipt reconstruction, writes and byte traffic are reported separately from neural evaluations.

At3,068 apps/pass, only2,836 are single-example online updates;232 contain8 derivatives.
A claim that each application has equal cost would be wrong. N and X have no extra rehearsal.

## 3. Neural and evidence shapes
One parameter or gradient float32 vector=674×4=2,696 bytes.
Eight captured example gradients=8×674×4=21,568 bytes per replay batch.
A float64 accumulator=674×8=5,392 bytes; raw mean32=2,696 bytes.
Per forward: hidden trajectory4×16 float32=256 bytes, logits2f32=8, probabilities2f32=8.
A local eligibility trajectory3×640 float32=7,680 bytes; its essential final trace=2,560 bytes.
These arrays must not be double-counted in resident metrics merely because recorded twice. Conversely,
backing buffers cannot be omitted because a view object is small.

Illustrative full-pair components, not a complete evidence bound:
9,400 raw gradient examples×2,696 =25,342,400 bytes;
464 batch float64 accumulators×5,392 =2,501,888 bytes;
6,136 post-application vectors×2,696 =16,542,656 bytes;
63,464 hidden trajectories×256 =16,246,784 bytes.
Add initialization versions, metadata, gradients/steps, local trajectories, forward/provenance headers, logs,
fault evidence, checkpoints, alias dictionaries, costs, scorer outputs, scripts and manifests.
Do not substitute these component sums for an implementation-derived whole-schema forecast.

Exact repeated captured arrays may be keyed once by dtype/shape/content identity after byte equality.
Every referenced array must exist; a digest alone is not evidence. Restoration may reproduce redundant
captured bytes, not rerun models to fill missing original measurements. Preserve before/after state and
every example gradient even when compression is inconvenient.

## 4. Mandatory record-kind admission before initial scientific fits
The future implementation must enumerate finite counts and maximum numeric shapes for:
initial loads/checkpoints; cue/gradient frames; branch-fork and reconstruction checks; online updates;
batch-example records; batch mean/apply records; source-receipt snapshots; frozen transactions;
queries; exact controls; non-neural/fault outcomes; intention/commit/heartbeat and final receipts.
It must state bounded identifiers/header fields and actual envelopes, not copy an old209MiB allowance.
New schema fields may increase storage; that is an admission question, not permission to omit them later.

Use the clean and100-application rehearsal probes to measure all record kinds. Report separately the
logical byte ledger, physical live encoding, empirical lossless-delivery forecast, nonnumeric reserves
and a fixed safety multiplier locked before sample measurements. Proposed factors:1.35 live,1.5 delivery;
nonnumeric allowances32MiB live and18MiB delivery, including1MiB emergency log record.
If this conservative policy does not admit, stop for a new schema/encoding review with all work retained.
Do not simply reduce a margin because the sample forecast fails. Actual caps remain enforced throughout.

Fit/condition forecasts must be weighted by gradient examples, forwards and archive bytes, not only by
application count. A mean batch gradient may be cheap or expensive to store depending on correlation;
that is measured, not assumed. Check full capture+replay and packaging/restoration simultaneous footprint.
A process-tree and container monitor includes auxiliary auditors; short sampling blind spots remain disclosed.

## 5. Maximum resource and execution responsibilities
Global7,000 apps;260,000 cells;80,000 heads;6,000 G backward calls;6,000 L gradient examples.
2h active wall including post-authorization implementation, all attempts, independent audits and delivery QA.
3GiB process-tree RSS;3.5GiB container current;256MiB retained evidence;64MiB delivered ZIP.
Current metadata: Python3.13.5, NumPy2.3.5, torch2.10.0+cpu package, four CPU equivalents and4GiB cgroup.
Those observations are not measurements of this unimplemented study's numerical cost.

Logger/scorer work, exact X, NumPy derivative checks and file integrity work are outside Torch operation counts
but inside time/memory/storage. Unknown completion stops rather than a speculative replay.
Reserve is for documented failed attempts, not extra hyperparameters, favorable seed searches or more epochs.

OBS-DC01-COST-001 remains open. Count ndarray backing ownership and native autograd graph limitations
explicitly. Report components and sampled RSS; no total-memory superiority without a repaired validated counter.
