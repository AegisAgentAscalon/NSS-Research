# NSS LB01-TERNARY — First ternary-weight trial
## Research, results, precision accounting and decision
**Execution v0.1 | 29 September 2026 | COMPLETE_BOUNDED_DIAGNOSTIC / TERNARY_STORAGE_AND_EXECUTION_WORK / WORKING_POINT_NOT_ESTABLISHED**

## 1. ELI5: the question and result
**Can our known checklist learner work with only three matrix-weight choices, and can training help it adjust?** We converted all three learned weight matrices to scaled -1, 0 or +1, implemented actual packed-code inference, and compared ordinary further training with training that uses these ternary weights during its forward computations.

**The encouraging finding:** the packed numerical model payload shrank from 72,996 bytes for float32 coefficients to 6,717 bytes including scales and floating biases. It can execute directly from that packed representation without retaining a decoded dense weight matrix. Ternary-aware preparation raised primary checklist accuracy from 19.41% after direct conversion to 96.48%.

**The limitation:** the original reference was 99.89% accurate, while the prepared ternary model completed only 610/1,024 scored continuations without any error and made 342 false-DONE predictions. No ternary parent met the declared joint working point. Training retained full-precision master weights, gradients and optimizer states, and the simple packed inference backend was slower than dense execution. This is real progress toward ternary weights, not the complete low-bit inference-and-learning solution.

Sources for every measured value: `results/SUMMARY.json`, `results/BENCHMARK.json`, `audit/AUDIT.json` and their raw files. All main work was completed; no further fit, threshold adjustment, new seed, or repair was added after confirmation. The original BRIDGE and CYCLE results remain unchanged.

## 2. What 1.58 bits means here
Three possible symbols have information capacity log2(3) = 1.5849625 bits each. Our executable storage packs five ternary symbols into one byte: roughly 1.6 bits per matrix coefficient, with negligible end padding. It does not claim physically addressable 1.58-bit scalar cells.

The three matrices contain 17,856 coefficients, or 97.85% of the model's 18,249 learned scalar parameters. The 393 biases remain float32. One derived float32 scale per matrix row adds another 393 stored values. Thus neither the complete model nor its working/training state occupies only 1.58 bits per original coefficient.

Microsoft's BitNet b1.58 paper is a precedent for ternary-weight training, but its architecture uses trained-from-scratch Transformer layers with BitLinear and quantized activations. The official BF16 release separately provides wider master weights for training/fine-tuning. Our study borrows the absmean quantization idea, not its architecture, training scale or published results. See primary-source references in section 14.

## 3. Exact task, lineage and what was held fixed
We reused the four original SURFACE01 parents 4101–4104, exported as float32 coefficients in BRIDGE01. Each is GRUCell(26,64) plus Linear(64,9), with 18,249 parameters. All four are retained regardless of performance; there are no new parent fits, language models, HSA paths, DARP blocks or pretrained downloads.

The public finite task rules are explicit. All eight items initially are unfinished. SET(i) completes i until CLEAR(i) or RESET. CLEAR(i) makes i unfinished. RESET makes every item unfinished. NOOP does nothing. After every event the required response is the smallest unfinished item; answer 8 means DONE and is valid only when every item is complete. A separate set-based interpreter checks the bitmask-derived labels. No hidden desired state is given to the neural input.

The second task contains eight reset-state cues, initially labeled 0,1,0,1,0,1,0,1. The secondary correction phase changes cue 0 to label 1 while preserving the other seven. This is association learning, not acquisition of a new procedure.

The BRIDGE01 and CYCLE01-A source ZIPs passed their original receipt hashes, CRCs, exact membership and all 719+803 = 1,522 declared payload checks. Only needed original arrays/source/receipts were copied. The source archives were not merged, rewritten or scientifically rerun. `provenance/SOURCE_VERIFICATION.json` records identities.

## 4. The comparison and training
### No-learning controls
Unchanged parent, per-row symmetric INT8 conversion, and direct ternary conversion. INT8 is an effective quantized-weight sensitivity control decoded into floating arrays for calculation; there is no native INT8 execution or compressed INT8 runtime claim in this pass.

### Matched continuing paths
Each parent branches into FLOAT and TERNARY. Both receive the same ordered 64 retained replay batches, repeated eight times, with A checklist and original-B losses added. Each batch contains 32 histories of 32 events. All original model coefficients can change.

Preparation lasts exactly 512 updates, with fresh Adam, initial learning rate .003 decayed by cosine to .0003, betas (.9,.999), epsilon 1e-8, no weight decay and clipping at 1. The ternary forward matrices are exact scaled ternary values. The backward pass uses an identity straight-through surrogate; rounding and scale derivatives are stopped. This is a declared surrogate-learning rule, not the exact derivative of a discrete quantizer.

After preparation, each path receives 64 further joint A+current-B updates with a fresh Adam at .001. This is **not** CYCLE01-A's successful B-only acquisition followed by balanced repair schedule. A failure of this different correction recipe cannot be assigned solely to precision.

There are eight paths × 576 updates = **4,608 main applications**. The disposable preflight performed six additional applications: **4,614 actual applications total**, with no repeated or unknown training tail. Saved checkpoints are 0,128,256,512,576. Intermediate checkpoints are development diagnostics, not confirmation-selected winners.

## 5. Quantizer, packed execution and precision map
For matrix row W, set s=max(mean(abs(W)),1e-8), q=clip(round(W/s),-1,1), and effective W=s*q. Rounding uses ties-to-even. Scale means accumulate in float64 then cast to float32 to produce identical training/export values. Scales are derived from the masters; they are not extra learned parameters. This is per-row rather than BitNet's cited per-tensor absmean variant.

| Surface | Representation in this pass |
|---|---|
| Matrix symbols at serving | Five trits per uint8 byte |
| Scale and bias storage | Float32 |
| Primary inference activations, gates and recurrent state | Float64; stored float32 coefficients/scales are exactly promoted |
| Packed matrix work | Direct code extraction and signed addition, then scale multiplication |
| Training masters and gradients | Float32 |
| Adam moments and counter tensors | Float32 |
| Training forward tensors and intermediate activations | Floating tensors with ternary-valued effective matrices |
| Evidence and task truth | Exact typed records, not quantized neural memory |

The packed C backend does not keep an expanded dense weight matrix. It uses double-precision accumulation and nonlinear functions, so it is **not all-integer inference**. Its scalar implementation is not an optimized BitNet kernel. The loader creates transient byte copies and checks validity; Python metadata, stack/workspace and retained output trajectories cost additional memory. The executable demo still imports the shared module containing PyTorch, so total process memory does not fall to the packed payload size.

Evaluation in float64 was declared before execution and follows the bridge's numerical interpretation. It does not establish float32/low-bit state stability, nor repair any historical float32 verification failure.

## 6. Fresh data, scoring units and state policies
The new panels have 16 development histories, 256 primary confirmation histories and 32 longer stress histories, equally distributed among mixed, idempotent, revision and reset families. Primary histories contain 24 prefix events plus 32 scored suffix events; stress contains 64 prefix plus 192 suffix events.

The primary policy REBUILD reads the whole history from empty state under each candidate's own weights. Secondary CARRY starts the scored continuation from the untouched parent's saved prefix state. Results are not exchanged after observing which is better.

Full histories and 32-event windows were checked against the retained replay subset, the prior CYCLE guard/live panels, and preceding newly generated panels. No collision occurred. Not every original historical training corpus was available for exclusion. Familiar primitive rules and shorter patterns repeat. This is bounded known-task generalization, not arbitrary novelty.

The primary denominator is 256 histories × 32 suffix events × four inherited models = 32,768 decisions. Whole-continuation denominator is 1,024. Histories repeat across model/precision paths; events and paths are not independent replications. Four parents are the model clusters.

## 7. Primary results: REBUILD
| Condition | Correct answers | Answer accuracy | Entirely correct continuations | False DONE | Current cue classes |
|---|---:|---:|---:|---:|---:|
| Unchanged float parent | 32,733/32,768 | 99.89319% | 1,020/1,024 (99.61%) | 0 | 32/32 |
| INT8 post-training control | 32,733/32,768 | 99.89319% | 1,020/1,024 (99.61%) | 0 | 32/32 |
| Direct ternary conversion | 6,361/32,768 | 19.41223% | 0/1,024 (0.00%) | 0 | 32/32 |
| Float after 512 preparation updates | 32,747/32,768 | 99.93591% | 1,022/1,024 (99.80%) | 0 | 32/32 |
| Ternary after 512 preparation updates | 31,615/32,768 | 96.48132% | 610/1,024 (59.57%) | 342 | 32/32 |
| Float after 64 correction updates | 32,749/32,768 | 99.94202% | 1,019/1,024 (99.51%) | 1 | 28/32 |
| Ternary after 64 correction updates | 31,545/32,768 | 96.26770% | 599/1,024 (58.50%) | 395 | 28/32 |

Preparation under ternary constraints reduced the converted model's errors from 26,407 to 1,153: **95.63% fewer errors**. That is a substantial learned recovery effect. The matched float continuation improved slightly, so additional training alone does not explain away the necessity of tolerating the ternary forward values; however, the QAT recipe is not shown optimal or equal-cost to an independently trained ternary model.

The INT8 control produced identical primary class decisions to the original model, not just an equal accuracy total. This supports a modest quantized-weight reference, but does not settle the requested ternary target.

### Prepared ternary results by parent
| Parent | Ternary answer accuracy | Whole continuations | False DONE | Working point |
|---|---:|---:|---:|---|
| 4101 | 7,923/8,192 (96.716%) | 147/256 | 136 | Not met |
| 4102 | 7,886/8,192 (96.265%) | 152/256 | 31 | Not met |
| 4103 | 7,809/8,192 (95.325%) | 135/256 | 91 | Not met |
| 4104 | 7,997/8,192 (97.620%) | 176/256 | 84 | Not met |

No prepared ternary parent satisfies the declared >=98% event accuracy, >=90% whole-history accuracy, <=1 percentage-point loss from its own parent, zero new false-DONE, and correct applicable B classes with minimum assigned target probability .8. All four original and INT8 parents, and all four FLOAT512 paths, satisfy this primary working point. Scores are not calibrated reliability probabilities; these are prospective engineering bands, not a population-level significance test.

### A concrete retained failure
In confirmation history 4, parent 4101's prepared ternary model correctly identified item 7 as the last unfinished item after event 52, SET(5). Event 53 was NOOP. The exact checklist therefore stayed unchanged, but the model changed its answer from item 7 to DONE. This is a contradicted completion assertion under explicit rules, not ambiguous wording. The original float parent remained correct. The eight prospectively selected history examples, including successful cases, are in `docs/TESTS_AND_ANSWERS.md`; all raw histories and model answers are retained.

Direct ternary conversion made no false-DONE claims in this panel, but almost never completed a whole sequence correctly and often returned the wrong low item. Zero false-DONE alone therefore must not be mistaken for useful retention. The prepared models became substantially more competent while acquiring a different residual error profile.

## 8. State carry and longer histories
### Secondary CARRY confirmation
| Condition | Correct answers | Answer accuracy | Entirely correct continuations | False DONE | Current cue classes |
|---|---:|---:|---:|---:|---:|
| Unchanged float parent | 32,733/32,768 | 99.89319% | 1,020/1,024 (99.61%) | 0 | 32/32 |
| INT8 post-training control | 32,733/32,768 | 99.89319% | 1,020/1,024 (99.61%) | 0 | 32/32 |
| Direct ternary conversion | 7,543/32,768 | 23.01941% | 0/1,024 (0.00%) | 0 | 32/32 |
| Float after 512 preparation updates | 32,747/32,768 | 99.93591% | 1,022/1,024 (99.80%) | 0 | 32/32 |
| Ternary after 512 preparation updates | 31,815/32,768 | 97.09167% | 650/1,024 (63.48%) | 316 | 32/32 |
| Float after 64 correction updates | 32,763/32,768 | 99.98474% | 1,019/1,024 (99.51%) | 1 | 28/32 |
| Ternary after 64 correction updates | 31,651/32,768 | 96.59119% | 611/1,024 (59.67%) | 377 | 28/32 |

Carrying old state improves the prepared ternary event aggregate modestly in this panel, but still fails the whole-continuation/critical-error requirements. This is not a substitute primary policy or a general migration guarantee.

### Separate longer stress, REBUILD
| Condition | Correct answers | Answer accuracy | Entirely correct continuations | False DONE | Current cue classes |
|---|---:|---:|---:|---:|---:|
| Unchanged float parent | 24,575/24,576 | 99.99593% | 127/128 (99.22%) | 0 | 32/32 |
| INT8 post-training control | 24,575/24,576 | 99.99593% | 127/128 (99.22%) | 0 | 32/32 |
| Direct ternary conversion | 4,871/24,576 | 19.82015% | 0/128 (0.00%) | 0 | 32/32 |
| Float after 512 preparation updates | 24,576/24,576 | 100.00000% | 128/128 (100.00%) | 0 | 32/32 |
| Ternary after 512 preparation updates | 23,599/24,576 | 96.02458% | 11/128 (8.59%) | 195 | 32/32 |
| Float after 64 correction updates | 24,575/24,576 | 99.99593% | 127/128 (99.22%) | 1 | 28/32 |
| Ternary after 64 correction updates | 23,585/24,576 | 95.96761% | 11/128 (8.59%) | 189 | 28/32 |

At 512 preparation updates, the ternary models still answer 96.02% of stress events correctly, but only 11/128 complete long continuations are error-free. Longer sequences expose the practical importance of recurring small errors. They were not used for extra tuning or to redesign a favorable primary metric.

## 9. Did the new correction enter the weights?
**No: all four FLOAT and all four TERNARY paths retained the old cue-0 class after the 64 joint correction updates.** Each answered the other seven cues correctly, giving 28/32 correct across the four parents. These are model outputs, not corrected ledger answers. The old eight associations were intact before that phase.

The float baseline's failure means this secondary test does not establish a precision-specific inability to learn. It identifies an inadequate shared acquisition recipe at this budget. No extra learning-rate adjustment, B-only rescue or repeated night was inserted. A future learning comparison needs a competent acquisition control, preferably reusing a separately declared known successful acquisition/repair recipe rather than assuming 64 joint updates are equivalent.

QAT's recovery of checklist behavior demonstrates successful learning with ternary effective forward weights. It does not qualify new-association retention, low-memory learning or a complete NSS maintenance cycle.

## 10. Actual bytes and speed
| Stored content | Numeric bytes |
|---|---:|
| Original float32 coefficients | 72,996 |
| Packed ternary matrix codes | 3,573 |
| Float32 row scales | 1,572 |
| Float32 biases | 1,572 |
| Packed model numeric payload | **6,717** |
| Complete .t3w export including header/digest | **7,556** |

The numeric payload is **10.87 times smaller** than original raw float32 coefficients, a **90.80% reduction**. Codes alone use 1.60081 bits per matrix coefficient including padding. The whole numeric body uses about **2.945 bits per original learned coefficient**, because scales and nonternary biases add cost. Full-file size and runtime arrays are separately reported; this is not a 10.87× whole-process memory saving.

Both training paths retain 72,996 master bytes, 72,996 gradient bytes and 146,016 optimizer-tensor bytes: **292,008 bytes before activations or temporary work**. Ternary preparation additionally materializes 71,424 bytes of floating effective matrices plus 1,572 scale bytes, and quantization/autograd temporaries. The counted totals are not total peak allocations, and tensor lifetimes may differ. **No training-memory reduction was demonstrated.**

### Matched-weight execution benchmark
First eight development histories, 56 events each, batch 8, one CPU thread. One warmup per method/case, then seven randomly interleaved repetitions. The comparison executes the same ternary matrices, scales, biases and float64 state either directly from packed C codes or via decoded NumPy arrays.

| Export | Packed scalar C median | Decoded NumPy median | Packed/dense ratio |
|---|---:|---:|---:|
| 4101_parent_ternary | 16.491 ms | 3.256 ms | 5.06× |
| 4101_ternary_512 | 16.920 ms | 3.123 ms | 5.42× |
| 4102_ternary_512 | 17.243 ms | 3.246 ms | 5.31× |
| 4103_ternary_512 | 16.871 ms | 3.339 ms | 5.05× |
| 4104_ternary_512 | 15.956 ms | 3.232 ms | 4.94× |

The simple packed backend is roughly five times slower. Avoiding dense weight storage does not automatically make the scalar implementation fast. The implementations also differ in loop/backend arrangement; these are full recurrence timings, not a pure hardware precision comparison or optimized language-model throughput result. Cold loading and decoding were measured separately once per case; no energy experiment was performed.

Tracked training cores sum to 56.200 seconds across overlapping processes, not the total research elapsed time. Mean per-branch training cores were 6.796 seconds for FLOAT and 7.254 for TERNARY. Maximum logged training-process RSS was 332,173,312 bytes; audit-process peak was 347,127,808 bytes. These include frameworks, model, fixtures and other arrays; they are not a per-format isolated memory comparison. The byte arithmetic, known resident arrays and sampled process maxima answer different questions.

## 11. Tests, answers and verification
The 24 preflight groups passed, including all 243 five-trit code patterns, padding, invalid symbols, nonfinite input, zero rows, rounding ties, independent recurrent arithmetic, surrogate-gradient behavior, all trainable gradients, and exact interrupted optimizer restoration on disposable copies. All 4,608 possible checklist-state/event transitions were checked under both label implementations.

The fresh-process audit independently recounted **200 output-array files containing 847,872 scored A observations** across panels/stages/state policies, and reproduced all 200 saved outputs and final states bit-for-bit. These counts include repeated development and stress material and must not be described as independent cases. It verified **40 checkpoint files** and independently decoded all **20 packed exports**.

All recorded evaluation checks covered **79,907,552 hidden/logit scalar comparisons**, with zero breaches of `1e-9 + 1e-8*abs(reference)`, no nonfinite values, and maximum absolute difference **5.4601e-13**. Checks compare implementations of the same effective weights—not a quantized candidate to its unquantized parent. This is full coverage of the declared retained evaluation checks, not verification of every training trajectory or future input.

The 20 main source/input lock objects, four fixture lock objects and separately frozen audit source remained unchanged. Audit performed zero optimizer applications. There were no unexpected training or evaluation interruptions, no unknown update tails, and no preflight failure requiring post-result repairs. Branch time/RSS was checked on update boundaries; evidence usage was checked at declared writes, not enforced by an operating-system sandbox.

The eight predeclared example histories are provided with every event and the predictions for every primary arm. Exact finite-rule checking covers all outputs. Same-author inspection of those examples is not independent semantic review, and this is not an English-comprehension benchmark. Codes have explicit public meanings. No historical scores were regraded.

## 12. Decision and next research questions
**Keep:** the honest packed ternary representation, executable packed inference, FP32/INT8 controls, full-parameter QAT implementation, checkpoint/optimizer resumption, numerical tests and all negative outcomes.

**Do not claim yet:** the accepted ternary working point, native low-bit activation arithmetic, a fast optimized kernel, reduced total training memory, learned new procedural competence, or a qualified bridge/companion.

The first next hypothesis is **learning under ternary constraints from the start versus abruptly converting an already-trained float representation**, with matched preparation and a competent float reference. The current run does not compare those routes. A small controlled gradual-transition alternative could be chosen instead, but not bundled with several other fixes or auto-run here.

A separate learning-state experiment should reduce an actual dominant cost (master/gradient/optimizer storage), after or alongside a competent ternary preparation reference. Preserve all residuals, scales and update accumulators in the resource bill. Ternary forward weights alone are not a resolution of the user's low-bit-training goal. The failed joint new-cue recipe requires an informative float control before precision comparisons.

The low-bit priority remains active until a declared useful inference **and** learning working point exists. All unrelated reader, language, HSA, DARP, longer CYCLE and bridge-expansion work stays on hold. No next model experiment is authorized merely by this report.

## 13. Evidence map and reproduction scope
`protocol/PROTOCOL.md` and `CONFIG.json`: original prospective contract. `LOCK.json`, `FIXTURE_LOCK.json`, `AUDIT_LOCK.json`: identities. `inputs/`: four exact parents and eligible old replay. `fixtures/`: fresh tests. `checkpoints/`: all states and update journals. `exports/`: effective arrays and packed models. `results/`: raw predictions, aggregate judgments and timings. `failures/`: observed first-error arrays, not hidden or repaired cases. `audit/AUDIT.json`: recount, numerical coverage and replay receipts. `docs/TESTS_AND_ANSWERS.md`: declared example panel and public-rule review.

See `README.md` for an offline packed-model demo and verification. The retained science drivers contain original absolute receipt paths, so relocating and reproducing every training/audit command requires a new path/runtime binding, not claiming that an archive copied to any operating system is byte-identical execution. Original source and binary hashes remain historical. Source is included; the compiled shared library is Linux/x86-64-specific. No universal deployment compatibility is claimed.

## 14. External primary references and boundaries
- Ma et al., *The Era of 1-bit LLMs: All Large Language Models are in 1.58 Bits*, arXiv:2402.17764v1, §2. Absmean ternary quantization and training from scratch are mechanism precedents, not our GRU results. https://arxiv.org/html/2402.17764v1
- Microsoft, official `bitnet-b1.58-2B-4T-bf16` model card. Wider master-weight/training release remains distinct from packed inference. https://huggingface.co/microsoft/bitnet-b1.58-2B-4T-bf16

Relevant primary pages were inspected; no external model weights or training code were downloaded or executed. This pass is not a reproduction of BitNet performance, a novel-method claim, or evidence that ternary works identically at all scales.
