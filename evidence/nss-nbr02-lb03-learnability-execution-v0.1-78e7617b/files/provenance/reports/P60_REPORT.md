# NSS LB01-Q2-PACK
## Lossless coding of useful two-bit weights: research, results and publication handoff
**Execution v0.1 | 1 October 2026, America/Detroit**  
Runtime receipts use 2 October 2026 UTC.  
**Disposition: COMPLETE — LOSSLESS STORAGE GAIN; NO PRACTICAL RUNTIME ADOPTION.**

## 1. Executive answer — the small-number model stayed unchanged
**Question:** Can we store the four-setting model more tightly without turning it ternary, pruning it, retraining it, or changing its answers?

**Answer:** Yes, for storage. A deterministic Huffman representation reduced the matrix-code stream from 2.0000 to 1.7890–1.8297 bits per matrix entry. Including the common header, block directory, source digest, scales, zero points and biases, complete files were 4.46–5.53% smaller than the same-format raw baseline. Every reconstructed coefficient and every tested output remained exact.

**The cost:** the simple bit-by-bit decoder made the tested inference workload 7.56–8.23 times slower. Independent DEFLATE blocks saved less than 1% of complete file bytes and their decoder needed more memory than the saved model bytes. Neither candidate earns replacement of the direct Q2 runtime. Whole-file compression saved about 13% of the legacy file for transport/archiving, but that control expands the file before use and does not establish smaller inference RAM. [E01–E04]

This is a positive mechanism result and a negative practical-default decision, not a failed neural-training study. There were **zero optimizer updates, no new model fits, no new lesson, no post-learning repair, no model-download dependency, and no external publication**.

The new contribution is a source-pinned, runnable coding/execution comparison with explicit overheads. Huffman coding after quantization is established prior work; no novel compression algorithm or large-model claim is made. [R1]

## 2. Where this fits the NSS research
The retained 59-pass record ends with useful two-bit model quantization and underqualified ternary routes. The current owner's sequence remains model quantization first, training efficiency later, post-learning repair separately afterward. The last conversation proposed inspecting lossless redundancy in the existing Q2 codes. This study is the 60th documented pass and answers that narrower proposal. [S01–S03]

The broader NSS goal is a controllable local companion using exact evidence, persistent work state and bounded maintenance. This tiny GRU is a research instrument, not that companion or a 20B language model. No model-change result, hardware-scalability conclusion or full NSS qualification follows.

**Retain:** the existing Q2 model as the default bounded reference. **Preserve but do not adopt:** this HUF16 decoder and the DEFLATE-block alternative. Training-state compression, training throughput, the longer day/night study, reader curricula, HSA, DARP and other architectures stay on hold.

## 3. Questions and predeclared comparison
| Question | Test | Answer in this pass |
|---|---|---|
| Is there losslessly exploitable redundancy in Q2 codes? | Fixed canonical Huffman per matrix, with fixed row blocks | Yes; all four models' code streams shrink. |
| Does the saving survive metadata accounting? | Common RAW/HUF16/DEF16 container; every byte charged | Some saving for HUF16; 4.46–5.53% of complete same-format files. |
| Can a calculation consume it without keeping a fully expanded model? | C block decoder plus unchanged GRU arithmetic | Yes during execution, with a 256-byte packed block buffer. Loader validation is a separate transient full-body operation. |
| Is it a practical drop-in runtime improvement? | Named decoder allocations plus interleaved inference timing | No at this implementation/workload. |
| Are model values, current outputs and known errors preserved? | Canonical byte comparison, native trajectories, independent equations, exact task scorer | Yes throughout the executed regression panels. |
| Is this evidence for training acceleration or sub-two-bit arithmetic? | Not tested | No: unchanged forward numbers and FP64 arithmetic. |

The prospective engineering rule required exactness in every model; a material storage candidate needed at least 5% full-container reduction in every model. The runtime route additionally required lower model-plus-explicit-decoder storage and inference no more than 1.25 times the matched raw version in every parent. Those are project decision thresholds, not statistical confidence or a universal usefulness definition. Smaller real gains remain reported. [P01]

## 4. Systems, lineage and information boundaries
Four exact final **Q2_CONTROL/step1024** exports from LB01-T3-TARGET were used: source parent IDs 4101, 4102, 4103 and 4104. They share an inherited training history family; this pass does not create four new independent experiments about all neural architectures. All four were included without selection.

Each model is **GRUCell(26,64) + Linear(64,9)**, containing 18,249 original learned coefficients. The three matrices contain 17,856 quantized entries. Metadata comprises 393 FP32 row scales, 393 uint8 zero points, and 393 FP32 biases. The Q2 quantizer itself is unchanged. The effective value is the exact FP32 product `(code - zero_point) * scale`, promoted to FP64 for the recurrent computation. Four settings remain available per row; the code stream's average length is not the number of allowed values. [S01]

The legacy file is 8,703 bytes: an 8,001-byte numerical body plus its header/integrity envelope. The new uncompressed container is 8,517 bytes, with the **same** 8,001 numerical bytes plus a different envelope. That 186-byte administrative difference is not credited to Huffman coding.

No compression code sees an answer key or uses task scores. Fitting a Huffman codebook to a stored matrix is a declared lossless file-encoding operation, not learning from test labels. The primary fixtures are deliberately reused regression inputs; no fresh-generalization claim is made.

## 5. Actual methods
### 5.1 Common block format
Each matrix is divided into consecutive groups of at most 16 rows: 12 input-matrix blocks, 12 recurrent-matrix blocks, one output-matrix block. The largest decoded block is 1,024 four-valued entries, still packed into **256 bytes**. Original row, column and numerical values are not permuted.

The common container stores matrix shapes, offsets, exact metadata, a 12-byte directory entry per block, a canonical-content SHA-256 and a file trailer digest. RAW, HUF16 and DEF16 have the same directory/header structure, so their file-size difference comes only from code-stream encoding. A stored raw block is used whenever a candidate's block is not strictly shorter. This fallback is part of the frozen codec, not a post-result choice of favorable models. Full binary offsets and validation rules are specified in `docs/FORMAT.md`. [P01, C01]

### 5.2 RAW reference
Four codes per byte, least-significant pair first, identical to the original code order. Native inference reads codes directly. This is a strong packed baseline, not byte-per-weight storage.

### 5.3 HUF16
Count the four symbols across each matrix; derive deterministic canonical Huffman code lengths with fixed tie-breaking; encode each row group independently. Store the four code lengths in each matrix descriptor. Prefix strings are decoded into one packed 256-byte scratch block. No persistent full decoded code array or dense weight array is retained in the C inference path.

### 5.4 DEF16
Use raw DEFLATE level 9 with a 512-byte window separately for each packed row group. The native decoder reuses an initialized zlib state across blocks within one rollout and frees it afterward. Allocation callbacks count both library requests and the small allocation headers used by the tracker. This conventional library route is not a newly invented codec. [R2, R3]

### 5.5 Whole-file and shuffled controls
A separate `zlib.compress(original_file, 9)` control compresses the **entire legacy file**, including header and metadata. Its output is decompressed completely for an exact-file check; no low-RAM inference claim is assigned to that route.

One fixed within-matrix shuffle preserves symbol counts but removes much of their original ordering. It is a coding diagnostic only: shuffled weights are not assessed or promoted as trained models. HUF16 sizes were unchanged or differed by one byte from padding; DEF16 then selected raw blocks everywhere. This suggests its tiny gains depend on local ordering, whereas Huffman exploits frequencies. One shuffle cannot prove absence of other exploitable patterns. [E01]

## 6. Test data, raw answers and units
The archived primary panel contains 256 histories, each with 24 prefix events and 32 scored suffix events. The long panel contains 64 histories, each with 64 prefix and 192 scored suffix events. Eight original cue associations use zero starting state. The source labels, events, family identities and prefix boundaries are preserved byte-for-byte.

The public checklist rule is explicit: all eight items begin unfinished; SET completes an item until CLEAR or RESET; CLEAR reopens it; RESET reopens all; NOOP changes nothing. After each event the answer is the smallest unfinished index, or 8/DONE only when all are complete. A second implementation uses sets, while the post-result recount uses bit masks. The 4,608 possible immediate state/event combinations agree.

Across three formats and four models, **36 output arrays** contain **368,736 total event/cue observations**, including prefixes, and **245,856 scored suffix/cue observations**. Those are repeated observations of the same 320 source histories and eight cue conditions, not independent tasks or new fits.

`docs/ALL_TESTS.jsonl` identifies every public test. Every raw input token, target, unedited prediction, output score, final recurrent state, source/model identity and exact locator is available. The readable example sheet retains the eight prospectively selected primary indices. Post-result inspection found that all eight belong to family 0 (mixed), contrary to the protocol’s expectation of four-family coverage. They were not replaced after seeing outcomes. Retrospective first errors are labeled separately; full automated checks cover all four families. Automated finite-rule review covers all arrays. No model identity-blind human panel or independent semantic reviewer was used.

## 7. Storage results — all four models
| Parent | RAW file bytes | HUF16 file bytes | HUF16 saving vs RAW | HUF16 code bits/entry | DEF16 file bytes |
|---|---:|---:|---:|---:|---:|
| 4101 | 8,517 | 8,137 | 4.46% | 1.8297 | 8,491 |
| 4102 | 8,517 | 8,088 | 5.04% | 1.8078 | 8,464 |
| 4103 | 8,517 | 8,046 | 5.53% | 1.7890 | 8,454 |
| 4104 | 8,517 | 8,058 | 5.39% | 1.7944 | 8,480 |

RAW code streams are 4,464 bytes. HUF16 streams are 3,993–4,084 bytes: **8.51–10.55% fewer code bytes**, with all four values retained. Scales, zero points and biases remain 3,537 bytes per model. The new common layout contributes 516 other bytes, including directory/codebook slots and digests. Thus the complete model is not a 1.8-bit-per-parameter runtime; 1.79–1.83 describes only its encoded matrix-code stream.

HUF16 meets the at-least-5% storage threshold in three of four models, not all four. Its smallest observed gain is still a real gain. DEF16's full-container saving is only 0.31–0.74%, with most blocks stored raw. No compression-size failure was repaired by trying another block size or level.

### Whole legacy-file compression — storage-only control
| Parent | Original file | Compressed file | Reduction |
|---|---:|---:|---:|
| 4101 | 8,703 | 7,607 | 12.59% |
| 4102 | 8,703 | 7,602 | 12.65% |
| 4103 | 8,703 | 7,579 | 12.92% |
| 4104 | 8,703 | 7,583 | 12.87% |

This saves 12.59–12.92% of the complete original file and preserves every original byte. It is appropriate evidence for a smaller archive/transfer representation. It is not evidence that all those bytes remain compressed while the neural computation runs.

## 8. Exactness and retained task quality
All twelve native model-format combinations reconstructed the **same 8,001-byte canonical numerical body** as their respective source. The independent audit decoded **214,272 matrix entries across those repeated format checks**, preserving scales and biases too. These checks cover every stored coefficient, not a random sample.

Current RAW, HUF16 and DEF16 trajectories and logits were bit-identical across **26,917,728 repeated hidden-state/logit comparisons**. The original C implementation versus independent NumPy equations, plus comparisons to the archived source logits, covered **10,078,784 scalar comparisons**, with zero violations of `1e-9 + 1e-8*abs(reference)`; the largest absolute difference was **1.16351e-13**. This compares execution methods for identical weights, not quantized and unquantized model quality.

| Reused task panel | Every format, current execution | Interpretation |
|---|---|---|
| Primary checklist suffixes | 32,764/32,768 correct; 1,023/1,024 whole; 0 false DONE | Exactly the source model's task result. |
| Long checklist suffixes | 49,147/49,152 correct; 253/256 whole; 2 false DONE | Existing long-run failures are retained, not corrected. |
| Original cue associations | 32/32 correct | No new association was introduced. |

The report does not pool old numerical failures from other studies into a new qualification, or call bit-exact compression a new learning ability. Semantic correctness still follows the same explicit task rule; matching an incorrect reference answer is a fidelity success but a task failure.

## 9. Runtime and memory — why neither decoder is the default
### Fixed, interleaved execution timing
Each sample processes the first eight archived development histories, 56 events each, with a single CPU thread. One warmup per model/format precedes nine randomized repetitions. Timers include Python call/output allocation, C decoding, recurrent arithmetic and output tracing; exclude model load, checksum/decode validation, encoding, compilation and scoring. Same values, events, arithmetic precision and output requirements are used.

| Parent | RAW ms | HUF16 ms | HUF16 / RAW | DEF16 ms | DEF16 / RAW |
|---|---:|---:|---:|---:|---:|
| 4101 | 7.327 | 60.274 | 8.23x | 9.142 | 1.25x |
| 4102 | 7.309 | 57.318 | 7.84x | 12.108 | 1.66x |
| 4103 | 7.250 | 56.674 | 7.82x | 11.009 | 1.52x |
| 4104 | 7.389 | 55.871 | 7.56x | 10.916 | 1.48x |

HUF16 is **7.56–8.23x slower**. Its simple decoder reads variable-length bits repeatedly for each event/example; it has no optimized lookup table, SIMD path or cross-example block reuse. That is a specific implementation cost, not a proof that all compressed inference must be slow. DEF16 is 1.25–1.66x slower and does very little compression here. These are tiny-model CPU results, not GPU/LLM, energy or optimized-production throughput claims.

### Explicit execution-storage accounting
| Parent | RAW model + named decoder bytes | HUF16 | DEF16 |
|---|---:|---:|---:|
| 4101 | 8,901 | 8,521 | 16,043 |
| 4102 | 8,901 | 8,472 | 16,016 |
| 4103 | 8,901 | 8,430 | 16,006 |
| 4104 | 8,901 | 8,442 | 16,032 |

All paths have the same identified 384 bytes of decoder-side structures: 256-byte packed scratch, 112-byte z_stream structure and 16-byte allocation tracker. The C implementation also uses 4,096 bytes of common recurrent arrays per rollout, outside this table. DEF16 adds **7,168 bytes of tracked zlib allocations**, including tracker allocation headers. They are freed at the end of each call; peak use still matters. Small scalar/compiler stack, alignment, library/OS pages, Python objects, model loader, tests and output arrays are not included in these named-byte totals.

**Baseline caveat:** the common container carries 300 bytes of block directory for a fair codec comparison. The original direct Q2 representation does not need that directory. Consequently, this table establishes a saving against the matched new layout, not a proven lower footprint than the best-engineered legacy packed runtime. The HUF16 complete containers alone are slightly larger than the old 8,001-byte bare numerical body. We do not equate body-only bytes with a complete executable model either.

**Loader caveat:** the Python wrapper performs a full exact decode for validation before a run and discards it afterward. During native execution there is no persistent full decoded model, but initial validation has a transient full-body/Python-symbol cost. Therefore no bounded cold-start peak claim is made.

## 10. What the frequencies explain
Matrix marginal entropy is 1.73–1.84 bits per symbol on these inputs. This is a descriptive single-symbol statistic. It is not a lower bound against every possible lossless coder, since correlations and shared structure can permit other compression.

| Parent | Matrix | Counts of codes 0,1,2,3 | Marginal entropy (bits) |
|---|---|---|---:|
| 4101 | cell.weight_ih | 545, 1472, 2096, 879 | 1.8352 |
| 4101 | cell.weight_hh | 1395, 5040, 4540, 1313 | 1.7592 |
| 4101 | head.weight | 109, 278, 144, 45 | 1.7491 |
| 4102 | cell.weight_ih | 482, 1388, 2258, 864 | 1.7948 |
| 4102 | cell.weight_hh | 1263, 5039, 4712, 1274 | 1.7340 |
| 4102 | head.weight | 46, 198, 238, 94 | 1.7744 |
| 4103 | cell.weight_ih | 508, 1448, 2240, 796 | 1.7945 |
| 4103 | cell.weight_hh | 1430, 5352, 4366, 1140 | 1.7320 |
| 4103 | head.weight | 61, 204, 251, 60 | 1.7355 |
| 4104 | cell.weight_ih | 460, 1451, 2252, 829 | 1.7833 |
| 4104 | cell.weight_hh | 1376, 5186, 4592, 1134 | 1.7269 |
| 4104 | head.weight | 81, 260, 191, 44 | 1.7275 |

The middle settings recur much more often than the extreme settings. HUF16 exploits that imbalance without deleting the extremes. A 1.79-bit average stream therefore does **not** mean the trained model has become binary or ternary. Nor can this tiny model's symbol frequencies be assumed for a 20B checkpoint.

## 11. Verification, incidents and cost accounting
The synthetic preflight passed **11 groups**: all 256 four-code byte patterns; partial lengths; 255 small Huffman histograms; three complete synthetic container distributions; corrupted/truncated/trailing-file rejection; digest-valid malformed layouts; bounded DEFLATE; three native/legacy/NumPy comparisons and split resumes; and 4,608 task state/event pairs. Native synthetic parity covered 42,048 scalar values. No cohort code histogram or compression score was used to tune the codec before the main lock.

The separately frozen post-result audit checked all 36 result files, replayed all 36 exactly, restored all 12 saved prefix states across the primary panel, and rejected 48 deliberately invalid state bindings. Full replay compared **3,318,624 saved logits** and **251,904 final-state values**. This is an internal fresh-process audit, not independent external replication.

Source receipt, archive CRC, membership and all **476 source payload hashes** passed. Thirty-seven protocol/source/input objects remain unchanged under the pre-main lock. Audit/report scripts are separately identified post-result code. Local hashes/timestamps are an audit trail, not proof of independently witnessed preregistration.

**Incident:** before protocol freezing, the first source-copy attempt requested `REPORT.md`; the archived member was actually `docs/REPORT.md`. It stopped with KeyError before compression or inference. The locator was corrected, source acquisition repeated, and the incident retained. No scientific source change, discarded learning, replacement model, post-result codec tuning or unplanned main-run interruption occurred. The failure is an operational source-location error, not evidence against a model. A separate post-result review found a coverage error in the protocol’s description of its eight illustrative indices: all are mixed-family histories, not a four-family sample. The protocol and indices remain unchanged; `failures/002_example_coverage.json` records the correction. This limits the rendered sample’s coverage, not the complete automatic recount.

Main per-parent processing totals **33.907 seconds**; the dedicated timing process used **3.181 seconds**; the full fresh-process audit used **26.294 seconds**. Those are measured script cores, not complete research wall time: source checks, code authoring, compilation, preflight, review, report rendering and packaging are additional. Main maximum recorded process RSS was **167,374,848 bytes**, with multiple candidates, reference arrays and outputs resident; this is explicitly not deployment memory. There was no energy measurement.

Guards sampled RSS/time at stages and checked anticipated output sizes; container calls also imposed timeouts. All completed workloads stayed within their declared ceilings. The C decoder has a fixed block buffer, but the overall process is not an OS-enforced memory sandbox. There were **0 training updates, 0 backward passes, 0 new models fitted, 0 pretrained downloads, and 0 external tool actions**.

## 12. Research decision and next boundary
**Keep the original direct two-bit model as the default.** HUF16 demonstrates that lossless sub-two-bit *code storage* is possible without removing the fourth value. That is worth preserving. It does not meet the all-parent 5% storage screen, and its current decoder fails the latency criterion in every parent. DEF16 does not meet material storage or execution-memory criteria. Neither achieves the complete practical adoption rule.

Whole-file DEFLATE is a useful conventional archive candidate, but its benefit must not be relabeled an inference-memory improvement. A future same-format lookup-table or cross-example decoder experiment could investigate the measured decoding cost; a new representation or larger model would answer a different question. Such work is **not automatically dispatched**. No training-efficiency or repair phase is reopened by this result.

The immediate publication contribution is a faithful self-contained example: question, fixed method, source identities, exact positive result, unfavorable cost tradeoff, raw evidence and explicit decision. That can help another group reproduce, critique or replace the codec without trusting an attractive summary.

## 13. Reproduction, publication and research etiquette
The package includes CPU source, four exact Q2 inputs, both exposed fixture panels, the original selected reference outputs, all new compressed formats, raw current arrays, logs, protocol/locks, tests and an audit script. No Torch installation or untrusted pickle loading is needed. Linux x86-64 was tested; a C compiler and zlib headers/library plus NumPy are required. Other platforms are not yet validated.

See `README.md` for commands. `tools/reproduce.py` runs in a fresh directory rather than overwriting the retained experiment. Full regeneration can produce different wall times or binary compiler hashes, and NPZ container metadata may differ; compare decoded arrays and canonical model bytes. The archived main files remain immutable.

See `docs/RESEARCH_PRACTICES.md` and `CONTRIBUTING.md` for precise claim scope, unit-of-analysis rules, fair controls, negative-result retention, pre/post-result separation, dual review, cost accounting and reviewer independence. Review is not complete simply because a hash matches.

**Publication is not yet performed.** The owner has not selected an open-source license for all historical code/checkpoints. `LICENSE_DECISION_REQUIRED.md` and `ATTRIBUTION.md` record that boundary. The package is a repository-shaped publication candidate, not proof that every inherited artifact may be relicensed. No GitHub repository was created or modified. No private conversational training data or online inference was used in this study; source/provenance documents still deserve human review before public release.

## 14. Evidence and reference register
- **P01:** `protocol/PROTOCOL.md`, `PROTOCOL_RECEIPT.json`, `MAIN_LOCK.json` — prospective local design and frozen bytes.
- **S01:** `provenance/original_REPORT.md` — original LB01-T3-TARGET report and its limitations.
- **S02:** `provenance/CHECKLIST_v0.27.md/.json` — inherited priority and 59-pass inventory.
- **S03:** NSS Collective Research Master Record v1.0, supplied separately — broader history; not re-audited in this pass.
- **C01:** `source/codec.py`, `source/stream.c`, `source/runtime.py`, `source/run_study.py` — actual codecs, execution and scoring.
- **E01:** `results/PARENT_4101.json` through `PARENT_4104.json` — every format size, entropy, shuffled control, comparison and panel result.
- **E02:** `results/BENCHMARK.json` — all timed samples, not only favorable medians.
- **E03:** `results/AUDIT.json`, `PREFLIGHT.json` — actual checks and their scope.
- **E04:** `results/SUMMARY.json` — predeclared screening decisions applied to retained data.
- **E05:** `docs/ALL_TESTS.jsonl`, `docs/TESTS_AND_ANSWERS.md`, `results/*_*.npz`, `FIRST_ERRORS.json` — exact tests, raw answers and failure locators.
- **R1:** Han, Mao and Dally, *Deep Compression: Compressing Deep Neural Networks with Pruning, Trained Quantization and Huffman Coding*, arXiv:1510.00149v5. https://arxiv.org/abs/1510.00149v5. Abstract-level precedent; its AlexNet/VGG results are not NSS results.
- **R2:** Deutsch, *DEFLATE Compressed Data Format Specification version 1.3*, RFC 1951. https://www.rfc-editor.org/rfc/rfc1951. Format/library background, not a learned-model result.
- **R3:** Python Software Foundation, *zlib — Compression compatible with gzip*. https://docs.python.org/3/library/zlib.html. Interface documentation; runtime versions recorded separately.

**Final status:** lossless compression is demonstrated; practical runtime advantage is not. Preserve the work and the useful Q2 reference. This study changes neither the old learned answers nor the current research scope.
