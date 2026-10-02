# NSS NBR02 SH01 — first working maintenance architecture, v0.1

## Dispatch and scope
User dispatch: “All right, let's do it,” accepting a shared versioned segment structure,
interchangeable dense/HSA readers, component tests and a four-configuration integration.
This is a NEW implementation/feasibility study, not RECOVER01, a tri-core implementation,
a DARP experiment, or whole-NSS qualification. Existing studies and failed gates are unchanged.

**Question:** Can an exact versioned segment manager and a genuinely sparse hierarchical
attention reader operate together on maintenance records, survive checked restart, and
provide an interpretable quality/cost comparison against competent simpler components?

## Implemented concepts and supplied information
JSON is the canonical storage/message format. Exact metadata, version resolution, scope,
cutoff, hashes and dependency links are supplied software, not learned capabilities.
The shared hierarchy has exact task records, per-task summary/query slots, region anchors
and a global maintenance constraint. The persistent manager caches version-bound packets
and invalidates them when a referenced record changes. The simple manager uses the SAME
exact dependency index and evidence selection, but rebuilds a packet on each request.
Thus this first manager comparison isolates persistence/reuse, NOT superiority over a weak
retriever. Both must return byte-identical packets. Neither gets evaluation answers.

The neural reader consumes typed numerical record vectors compiled from JSON, NOT natural
language or a standard subword tokenizer. A record-vector position is never called a language
token. Small headers and summary/region slots contain metadata, NOT a precomputed answer.
Exact task progress is explicit evidence. Dependencies are explicit IDs. The model learns
how to combine those fields into a maintenance disposition, not how to infer an undocumented
policy or learn ID registration. No claim about a 25,000-language-token workspace is possible.

Per task: query/summary, progress record, action-receipt record, and constraint record.
A random continuous address code accompanies metadata; two dependency codes are supplied.
Regional anchors summarize metadata only. A global anchor contains a freeze flag.
Targets: DEFER if global freeze; otherwise COMPLETE if own progress complete; otherwise
READY if both declared prerequisites are complete; otherwise BLOCKED. Progress/receipt
records are distinct. Receipts are used by deterministic idempotence tests, not an additional
learned target. Prediction is from each task's query position. Output serialization is fixed.

Dense and HSA readers have the same trainable architecture and paired initial parameters:
linear input projection to 32, two 2-head residual attention/FFN blocks (FFN64), layer norms,
and a 4-class head. All parameters train; no frozen-core premise.
HSA edges: dense within each task; own-region summary slots; exact two dependency tasks;
all region anchors and global anchor. A region attends its own task summaries and global;
global attends region anchors and itself. Direct dependency selection is metadata-governed,
not learned top-k. All query rows have a self edge. Sparse gather computes ONLY padded
selected-edge scores, never a full T-by-T score matrix. All valid and padded edges count.
Dense uses installed PyTorch scaled_dot_product_attention (not a deliberately slow full-score
Python baseline). Masked dense is a numerical reference only, not the dense competitor.
These graph rules are one new HSA prototype, not the only HSA or a reproduction of Longformer.

## Stages and fixed experimental settings
1. Engineering: versions, exact retrieval, current/old cutoffs, scopes, non-erasing source
   archive, stale packet detection, dependency invalidation, bounded packet refusal, digest
   corruption, idempotent action receipts, checkpoint+restart equality. Include seeded clean
   trajectories and deliberate fault injections. Technical defects may be corrected before
   source lock, with initial errors retained. No confirmation-based revisions.
2. Numerical: independent NumPy single-attention reference, sparse vs masked-dense output
   and gradients, no-full-square sparse allocation inspection. Double precision envelope
   atol1e-10+rtol1e-9*abs(reference); float32 forward envelope2e-5+2e-5*abs(reference).
   Fixed new contract; it does not requalify earlier recurrent studies. A failed numerical
   comparison is a technical finding, not a behavioral failure or permission to change tolerance.
3. Training: 4 paired fresh seeds 8801–8804, dense and HSA, 600 updates per fit (4,800 main
   applications maximum). Each update batch16 independent 8-task worlds. Same ordered
   batches for every fit. AdamW lr0.002, betas0.9/0.999, eps1e-8, weight_decay0.01;
   clipping1.0; dropout0; float32; one CPU thread; deterministic algorithms. No best-checkpoint
   selection; only final600 used for primary inference. Save steps0,200,400,600 and losses.
   Up to8 disposable preflight optimizer applications. No refit/replacement/tuning after lock.
4. Frozen confirmation: 256 fresh 8-task worlds, 2,048 task decisions per model; paired four
   seed results. Secondary stress:64 fresh 16-task worlds,1,024 decisions/model, separate
   length-transfer panel. Generator seeds train771001, development771002, confirm771003,
   stress771004. Parent/record addresses are randomly generated and worlds independent.
   Fingerprints must be disjoint. Development contains32 worlds; reports never promote it.
   Decision accuracy, macro recall, exact whole-world correctness, false COMPLETE and class
   confusion retained. Functional target >=95% task accuracy AND >=90% macro recall is a
   descriptive target per fit, not permission to suppress other valid results. A zero-error
   engineered rule is an explicit capability control, not a neural result.
5. Four-way integration: simple+dense, persistent-segmented+dense, simple+HSA,
   persistent-segmented+HSA, same eligible records and exact packets. Run seeded multi-job
   maintenance sequences with warm reuse, changed dependency, cold task, and interrupted
   restart. End-to-end status accuracy includes parser, manager and neural reader; standalone
   component timings retained. Identical reader outputs between simple/segmented are expected.
6. Bounded timing: fixed sizes8/32/128 tasks, batch1; 3 warmups and15 repetitions alternating
   reader order. Include projection/FFN; report attention cells, padding, gather buffers,
   selector/packet time, serialized traffic/cache storage. CPU medians/IQR, not energy or
   device forecasts. Stress sizes32/128 are cost profiling, NOT competence estimates.
   Paired persisted vs stateless management includes rebuild and invalidation cost and one-time
   index construction. No claim of superadditive fusion benefit from a 2x2 alone.

## Evidence, failure and resource contract
Every context and seed retained. Failures: selection/visibility, stale revision, dependency,
packet integrity, lost resume state, duplicate action, attention math, learned decision,
resource, or unknown. Store compact metadata and the first8 numeric reproducers; count
all failures without full-array duplication. Retain all raw predictions/targets and final weights.
Scientific process cap900s, peak process RSS2.5GiB, output payload cap128MiB (16MiB reserve).
Preparation, testing and packaging time recorded separately; profile memory is not training
memory. Stop with partial evidence on resource breach, never silently change budgets.
Source/config/data fingerprints locked before primary training and confirmation is scored
only after training completes. An independent recount and fresh-process saved-model replay,
archive CRC and file SHA256 checks are delivery requirements. These are internal checks,
not third-party replication. No automatic successor experiment is authorized by a finding.
