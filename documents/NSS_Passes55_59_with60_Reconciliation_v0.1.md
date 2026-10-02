# NSS passes 55–59: complete-record reconciliation
## Pass 60 context and exact starting-state decision · v0.1

Prepared during LB03-LEARNABILITY. This is a new archive/lineage audit, not a rerun or requalification of the historical experiments. The user explicitly authorized a new low-bit-training study; historical holds remain part of the earlier record, not a reason to ignore this dispatch.

## Completeness finding

All five requested full execution archives and the additional pass-60 archive were present. Their complete archive SHA-256 digests match original delivery receipts. ZIP CRC, exact declared membership, manifest digest, every payload size and every payload SHA-256 passed: **2,735 payloads for passes 55–59, 174 for pass 60, 2,909 in total**. No declared payload is missing. This is integrity against supplied receipts, not cryptographic authentication of an untrusted publisher, independent replication or proof that unrecorded work never occurred.

The separate reconciled-records ZIP preserves all six original ZIPs byte-for-byte, plus the original delivery receipts and this catalog. The new experiment ZIP is self-contained for the selected comparison but does not duplicate all historical raw arrays. `COMPLETE_RECORD_INVENTORY.json` gives every historical member's locator, category, size and SHA-256. Categories are navigation aids; an empty failure directory does not mean the model made no errors.

| Pass | Study | Archive bytes | Verified payloads |
|---|---|---|---|
| 55 | BRIDGE01 | 7,732,985 | 719 |
| 56 | LB01_TERNARY | 106,822,000 | 531 |
| 57 | LB02_Q2_TRAIN | 98,307,290 | 580 |
| 58 | LB02_MASTER16 | 44,845,903 | 429 |
| 59 | LB01_T3_TARGET | 76,839,727 | 476 |
| 60 | LB01_Q2_PACK | 44,566,585 | 174 |

## What each pass contributes

### 55 — BRIDGE01
The protocol, source, four frozen model exports, 216 scripted-session journals/results, malformed/rejected proposals, restoration tests and audit are retained. The language model and tool actions were scripted simulations; the GRU advisor was real. It did no training. Its original model values establish a checked source bridge into subsequent quantization work, not trained general orchestration. Rejected proposals and output errors are principally in raw journals; no separate failed scientific run is asserted.

### 56 — LB01-TERNARY
Full protocol, original parents, 64 replay batches per parent, checkpoints, raw numerical outputs, packed ternary models, failures and audits are available. Ternary preparation recovered substantial task skill, but whole-task reliability was inadequate. A later cue-correction recipe failed both the float and ternary references. That shared failure cannot be interpreted as proof that ternary uniquely prevents learning. Full-precision masters, gradients and optimizer states remained.

### 57 — LB02-Q2-TRAIN
Full Q2/M32/M8 comparison, initial and preparation/correction checkpoints, optimizer/RNG states, replay inputs, all raw outputs, original preflight defect and two operational recoveries are preserved. Useful Q2 preparation and smaller optimizer arrays are supported; the post-correction combined retention gates failed. The original actual-main-update ceiling was exceeded. Its 205 known repeated updates and up to two additional unlogged updates remain an explicit historical cost interval. This source is not relabeled clean-budget because the present experiment ran cleanly.

### 58 — LB02-MASTER16
Full FP32/FP16 nearest/stochastic comparison with exact prepared starts, source/C kernels, master/moment/RNG snapshots, output arrays, memory probes and audit receipts are available. This tested continuation of an almost-perfect task, not early learning or new material. Its strongest unresolved question was whether small updates that are rounded away matter when learning still has work to do. A missing `failures/` directory is not missing evidence: no unexpected main numerical failure was reported; model mistakes remain in the raw arrays and readable test sheet. The declared per-write storage monitoring gap remains historical.

### 59 — LB01-T3-TARGET
Full direct/ramp ternary comparison, exact Q2_M32 starts, fixed budgets, intermediate/final states, all packed exports, output arrays and audits are present. The useful Q2 control remained strong; both ternary paths missed their whole-task target. Ramp versus direct also differs in pure-ternary exposure and learning-rate timing. This is not a controlled proof that gradual quantization can never help, nor a failure of every three-valued codebook.

### 60 — LB01-Q2-PACK (context only)
Full codec source, exact four Q2_CONTROL models from pass 59, raw results, byte/numerical comparisons, decoder timings, audit and reproduction incidents are preserved. Huffman shortened the unchanged code stream to about 1.79–1.83 bits per entry but the tested runtime was much slower. It performed no training. The encoded stream length is not the precision of masters, gradients or optimizer state. Its absent training checkpoints are **not applicable**, not missing data.

## Exact lineage resolved

Four original parent tensor hashes agree from pass 55 into passes 56 and 57, and the original-reference inputs retained by pass 59. Pass 57 Q2_M8 step1024 files match pass 58's starting files byte-for-byte. Pass 57 Q2_M32 step1024 files match pass 59's starting files byte-for-byte. Pass 59 Q2_CONTROL final packed exports match pass 60 inputs byte-for-byte. The 24 link checks are in `CHECKPOINT_LINEAGE.json`.

The new EARLY experiment uses exact pass-57 Q2_M8 step0000 files. These contain an already-trained floating ancestor, not random weights, and precede Q2 preparation. NEW uses exact pass-57 Q2_M8 step1024 preparation files, not the post-correction/repaired states. All eight files and tensor digests are in `SELECTED_STARTS.json`; no missing state was invented or approximated. Source optimizer state is retained but deliberately reset for the new matched comparison.

## Missing, unavailable or never-created material

1. **No requested declared payload was missing.** Complete protocol/report/source/starting-state/result/failure/audit coverage is available at the original recorded scope.
2. **Not all ancestral training corpora are supplied.** The low-bit packages preserve 64 replay batches per parent, not every original SURFACE01 training example and ancestor fitting trace. This limits exhaustive novelty and inherited-training-cost claims. It does not block exact continuation from the supplied pinned checkpoints.
3. **Pass 57's unlogged interrupted tails remain unknown.** Original terminal elapsed time, peak memory and up to two unjournaled updates cannot be manufactured from hashes. There is no claim of exactly 13,440 actual applications in that old study.
4. **Historical independent external replication is not supplied.** Separate scripts and fresh processes are internal checks; they are not third-party validation.
5. **A real LLM deployment in 55 and training evidence in 60 were never part of those experiments.** They are out of scope, not lost records.
6. **Current loose checklist versions were mismatched.** The mounted readable checklist was v0.28, while mounted JSON was v0.27. The exact v0.28 JSON was recovered from the verified pass-60 archive; no historical JSON version was fabricated. The new checklist preserves all 60 prior entries.

**Comparison readiness:** no missing record prevents the selected early-learning/new-association precision comparison. Full ancestral novelty, original unsaved runtime totals and independent replication remain unavailable, and the report limits its claims accordingly.

## Exact archive digests

| Pass | SHA-256 |
|---|---|
| 55 | ade14d04d64dd5fb074bff38e109d2715c24c0104b2008a5e033f22bd789ea5f |
| 56 | b373ac8af17f430af4d8b6475ed3582191631acc5065d9d0ea270fa8fa73dd0b |
| 57 | 02080e19189e74a42f5a95df3bb6042dadecfd2f9483fc0c90739b3f049f9ad7 |
| 58 | a860d41758622ecda19ec49e2ca9e25d3a30c644e7a4bc9f9d24fdadaaa6563f |
| 59 | ea02132e4e26f7927bc0177f0c980e8adda9426f8a70c6af112e9b649764ee20 |
| 60 | aae53ab1eb25e026feef29f17457112a898dd95d94e8104ac76a52708249139a |
