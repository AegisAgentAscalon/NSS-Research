# Recovery finding: the selected reader weights survive

## What the reuploaded parent establishes

The available canonical Study009 ZIP is 242,997,220 bytes. Its SHA256 matches the original recorded delivery: `f35dd261c2af96058f9d3647c6345fa83d4176b426f92f3aa093861759f7632a`. All 501 manifest-covered files verified. The runtime presents the canonical filename without the attachment's `(1)` suffix; no byte comparison to a separate absent duplicate is claimed.

This is the pass immediately before Qualification010, as also stated in the historical 010 report section 2. It is the same source anchor already used in Recovery_Starter_v0.1. The new upload provides a recovery input, not new evidence that the missing 010 additions were contained in Study009.

## Exact weights, not a recollection

The five `record_hop_801.safetensors` through `record_hop_805.safetensors` files contain the actual inherited 818-parameter readers selected by the historical 010 report. Each stores:

| Tensor | Shape | Values |
|---|---:|---:|
| `match.q.weight` | 24 x 17 | 408 |
| `match.k.weight` | 24 x 17 | 408 |
| `match.log_scale` | scalar | 1 |
| `match.threshold` | scalar | 1 |
| **Total** | | **818** |

Each checkpoint contains 3,272 raw float32 tensor bytes, inside a 3,576-byte safetensors file. The inventory records every actual hash. This is why the selected inherited reader can be recovered exactly without recreating its training.

The cap-only condition changes a numerical cap, not those tensor values. This package adds a new report-derived implementation and a test that cap80 matches the original forward output exactly on a generated case. It is not claimed to be recovered original 010 source. The exact traversal control has no neural weights to regenerate.

The 35 retained checkpoints include earlier binders, gated readers, repair networks and match heads. They are not 35 Qualification010 models, and none of the missing 15 new 010 main checkpoints is silently substituted.

## What conversation memory contributes

The surviving report and receipt give detailed architecture/training/task descriptions, and earlier work notes retain general implementation intent. No missing tensor bytes or final 010 source surfaced in those notes. A preliminary attention idea cannot override the final report's stated architecture. Conversational context is useful for an annotated reconstruction map, not a numerical checkpoint backup.

The structured historical recipe preserves seeds1201-1205, three arms,6000AdamWsteps/fit,batch64,eight trained stages, row cross-entropy plus half squared code error, teacher-forcing schedule, cosine learning-rate endpoints, weight decay and clipping. Missing reductions, indexing, sampler draws, exact attention graph and acceptance-cell enumeration remain explicit nulls. Equal seeds with a different implementation do not establish identical weights.

## Fresh execution in this recovery pass

The unchanged parent suite passed45tests. The new recovery adapter/status checks passed10tests. These are55distinct tests, not the historical151.

The limited smoke exercised five inherited families, two chain lengths, horizons0/64, a state-removal intervention and three reader/control profiles. It produced25scenarios and575saved arrays. In its20state-on cases (320streams shared across profiles), all three profiles answered all supported and missing cases correctly at sufficient depth; the state-off controls did not answer supported questions. Store signatures and model hashes were unchanged by reading/evaluation. This is a small new-seed recoverability demonstration, NOT another NBR-01 qualification or a reproduction of the old performance table.

The smoke uses16streams/case and no unrelated live writes. It does not cover the old full128-stream protocol,1024horizon,21lifecyclequery checkpoints, all stresses, timing limits or all90old continuations. No new optimizer step was executed, no new 010 checkpoint was trained, and no old source lock was reconstructed.

## What we can hand off now

A working inherited foundation, actual weights, readable source locations, new limited reference checks, the historical recipe transcribed into structured records, and a precise list of missing additions. That is more complete than prose-only recovery, but is not the complete original experiment.

Next work: rebuild and review the missing010 module layer, then resolve/freeze an explicit new protocol before retraining the three arms and requalifying. Historical outcomes remain comparison evidence, never targets to manufacture.

Sources: unchanged historical010 REPORT sections2-4/9; historical receipt; exact parent009 sources and manifest; current audit files.
