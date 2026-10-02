# LB01-Q2-PACK v0.1 — Lossless coding of the working two-bit model

## Status and question
Prospective local protocol, 1 October 2026 America/Detroit (runtime receipts UTC). Freeze this document before measuring the four model code distributions or candidate file sizes. Technical preflight may fix implementation errors before the main source lock; retain every failure. This is not a public preregistration. User authorizes one bounded next pass; no GitHub publication is authorized or performed.

ELI5: Can we put the same four-setting weights in a smaller envelope, read that envelope without expanding the whole model, and get exactly the same answers?

Broader question: low-bit model representation and executable memory economy for NSS. Model quantization is current; training-state/throughput optimization, new learning, repair, HSA, DARP, new architectures and a real transformer are excluded. No optimizer, gradients or new model fits. Retain Q2 as reference regardless of an unfavorable compression result.

## Cohort and provenance
All four final Q2_CONTROL/step1024 exports (4101–4104) from the supplied LB01-T3-TARGET v0.1 archive. Exactly 18,249 learned coefficients/model: 17,856 matrix codes, 393 FP32 scales, 393 uint8 zero points and 393 FP32 biases. Ancestral fits and tasks are unchanged. Do not select a favored seed or compress away inconvenient weights. Verify the source archive receipt, CRC, exact membership and all 476 payload hashes; copy only an explicit input/source allowlist. Do not load pickle checkpoints.

## Fixed candidate comparison
Use a common binary container and identical immutable scales/zero points/bias bytes. The baseline container RAW and candidates HUF16 and DEF16 have identical directory/header structure. Independently report the legacy 8,703-byte file and 8,001-byte numerical body so a smaller administrative header cannot masquerade as weight compression.

Matrices are divided into consecutive groups of at most 16 rows (25 total blocks per model). Original column order and values remain unchanged. Maximum packed block is 256 bytes. Each block gets an offset, encoded length, original packed length, codec flag and symbol count. Header includes original canonical-content SHA256; trailer hashes the full container.

- RAW: original four codes per byte, little-endian within each byte.
- HUF16: deterministic canonical Huffman code lengths learned from the frequencies in each entire matrix (four symbols). Encode blocks separately for row-group access. Keep a block raw when its compressed byte count is not strictly smaller. Codebook and directory bytes count. No code sorting/permutation/weight change.
- DEF16: raw DEFLATE level 9, 512-byte window (wbits=-9), separately on the packed bytes of each row group. Same raw fallback rule. No tuning, parameter sweep, codec shopping or combining methods after seeing results.
- Whole-file DEFLATE: storage-only conventional control on each complete original .q2 file. Decode it fully for byte-identity checking; explicitly not claimed to save running model RAM.

Both learned Huffman frequencies and raw-block fallback are deterministic parts of the codec, not confirmation-based model selection. Report every candidate/model, including expansion. Matrix marginal code entropy is descriptive, not a universal compression lower bound; correlations can permit further coding. A single reproducible within-matrix shuffle (seed 1400101 plus parent) and balanced/random and constant synthetic controls diagnose correlation and implementation, not model quality.

## Exactness and runtime
Keep FP32 effective weights bit-identical to original decoded Q2, and retain FP64 recurrent/gate/accumulation arithmetic. Implement a C reader that decodes only one row group into a fixed 256-byte packed buffer, then runs the same recurrence. No persistent full expanded codes or dense weights in the low-memory C path. Python verification may hold all three candidates/decoded references simultaneously; do not call its peak RSS deployment memory.

C DEFLATE allocations must be counted using zlib allocator callbacks (current/peak/live freed) plus z_stream and the 256-byte scratch. HUF16 uses canonical code lengths and local decode state. Report file bytes, code bytes, directory/codebook bytes, persistent model bytes, explicit decoder scratch, zlib allocations and shared recurrent workspace separately. Small scalar/compiler stack, Python/object/runtime, evidence and output capture are not falsely claimed to be fully measured.

Primary numerical obligations: all reconstructed matrix, scale, zero-point, bias bytes exactly match; all current RAW/HUF16/DEF16 FP64 trajectories and logits bit-identical; original C/reference and archived logits meet inherited |error| <= 1e-9+1e-8*abs(ref) and class equality. A historical non-bit-exact match is recorded separately rather than equated with a new method failure. Any current-codec value/decision mismatch stops adoption; retain outputs and do not relax tolerance.

## Evaluation panels and units
Reuse the archived 256 x (24-prefix+32-suffix) confirmation histories and 64 x (64-prefix+192-suffix) stress histories, plus eight reset B cues. These are exposed regression panels, NOT fresh confirmation of learned competence. All original events/labels and raw logits/predictions/end states stay resolvable. Independent set-based oracle checks the public eight-item checklist rule. Current predictions remain unedited; exact-preservation success includes reproducing previous mistakes. No safety guard corrects a prediction.

Eight predeclared sample indices [0,32,64,96,128,160,192,224] span the four archived primary families, with every candidate/model. Produce exact event/answer sheets and label manual coverage honestly; no independent human review is asserted. All arrays receive finite-rule checks. Additional first observed errors are retrospective illustrations.

## Timing and diagnostics
C batch=8, first eight archived development histories (56 events), single thread, original order. One warmup per parent/backend; nine randomized interleaved repetitions, permutation seed 1400102. Time inference including block decoding, nonlinearities and output tracing, excluding load/compress/validation/compilation/scoring. Report median and raw samples per parent, full range; no post-hoc best-repetition selection. Compression and whole-file decode time reported separately. Add seven interleaved whole-file encode/decode repetitions. Do not extrapolate to LLMs, GPUs, energy or 20B deployments.

Serialize and restart same-weight state at prefix boundary; bind model digest, event cursor and state checksum; reject wrong-source, corrupt, truncated and invalid headers. This is inference-only restoration, not unfinished-state migration to new weights.

## Decision rule
First report the measured effect, not just PASS/FAIL. Encoding is technically usable only if byte identity, execution parity and fault checks pass for all four models. A material storage candidate must save >=5% complete canonical file bytes vs RAW on each model; record lesser savings too. A practical streaming-memory candidate must also reduce model+explicit decoder bytes vs RAW, with no hidden full decoded model, and median inference <=1.25 x RAW for each parent. These are engineering thresholds, not statistical significance claims. Whole-file compression cannot satisfy the running-memory route merely by being small on disk. Parent is an inherited model, not an independently sampled architecture; repeated events and timing calls are not independent tasks.

A no-gain result closes this codec test. No new quantizer/codebook/sparsity/training pass follows automatically. New codec ideas require a separate protocol, not incremental search on these results.

## Resource and reproducibility boundaries
Main execution <=180 seconds per parent process, <=2 GiB process RSS, <=128 MiB generated study data before final documentation. Benchmark child <=60 seconds, complete study includes development/verification/documentation costs separately. No optimizer applications under any condition. Use synchronous bounded processes and retain partial/failure logs; never invent completed work after timeout. Enforce child timeout and check RSS/write sizes explicitly; these are not an OS memory sandbox. Do not extend a reached declared scientific budget.

Source/inputs/protocol locked after preflight and before model compression measurements. Fixing a post-lock scientific defect ends that version's attempt; any correction is a retained amendment before rerun, not a concealed edit. Separate post-result reporting/audit code from the frozen producer. Retained tests, raw results, failure ledger, command log, environment/compiler identities, manifests and independent re-decoder enable external review. Local timestamps/hashes establish a local audit trail, not tamper-proof third-party preregistration. Content checksums establish integrity, not publisher authentication.

## Publication boundary
Provide a portable repository-shaped research package: README, study protocol, source, tests, raw artifacts, report, data/model card, attribution, contribution/review guidance, licensing decision placeholder and known limitations. Do not infer licenses for historical checkpoint/code files or upload any material publicly. No raw personal conversation or secrets enter new fixtures. Original project provenance filenames are retained; sanitized public-release decisions require an owner review.
