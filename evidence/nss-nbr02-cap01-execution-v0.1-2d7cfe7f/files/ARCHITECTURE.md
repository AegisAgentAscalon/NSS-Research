# NSS CAP01 architecture v0.1 — A computation can outlive its active segment

## Component boundary
CAP01 extends the SC02/SH02 reader's execution lifecycle. It does not change its learned graph, parameters, task rule, feature encoding or hierarchy depth. A four-position query group may read its allowed keys in successive tiles. The task can therefore finish even when the full two-layer dependency closure cannot be simultaneously resident in the active record tile.

The same mechanism is available to the ordinary retrieval comparator. “Segmented” in the candidate means grouping queries with identical hierarchical neighborhoods; ordinary uses consecutive query groups. Both maintain exact progress. This design does not claim that ordinary algorithms cannot implement segmented execution.

## Data path
1. Bind a maintenance job to an exact source snapshot, model hash, scope, targets, graph identity and active record budget.
2. Compile the unchanged typed evidence. Source ingestion and complete graph metadata are outside the neural active-record cap and charged separately.
3. Compute required backward dependencies. Encode needed source rows in bounded tiles and write a file-backed embedding array. No desired task labels enter this operation.
4. For each first-layer query group, retrieve bounded key/value tiles. Carry the partial attention normalizer and weighted sum across tiles. Write completed first-layer rows to a separate file-backed array.
5. Once all necessary first-layer rows exist, compute the selected second-layer query outputs by the same bounded procedure. Never mix a newer layer value into an earlier simultaneous layer.
6. Apply the unchanged final normalization and head to small target groups. Record predictions, evidence/model identities, numerical comparisons and resource counters.

There remain three HSA levels: task, region, global. Segment boundaries are execution boundaries, not a fourth level. Dense readers keep all their original attention connections.

## One softmax, not one independent answer per segment
For a query, let a processed prefix have maximum m, softmax denominator l and unnormalized weighted-value numerator o. For the next score tile s and values v:

m' = max(m, max(s))

l' = exp(m - m') l + sum(exp(s - m'))

o' = exp(m - m') o + sum(exp(s - m') v)

The final attention output is o/l. Applying the same rescaling to the old and new terms preserves the joint softmax algebra. Masked keys contribute zero. Queries with no admitted keys yet retain an empty accumulator without generating NaNs. Float32 roundoff is tested against the unchanged full-reference envelope; algebraic equivalence is not represented as bitwise equality to a different execution order.

## Durable unfinished computation
A resume JSON envelope contains schema, source/model/topology identity, reader mode, manager policy, budget, targets, layer/group/key cursor, and binary-encoded exact m/l/o arrays with their shapes/dtypes/checksums. It references checksummed source/embedding/layer files in the same directory.

Resume validates the complete envelope and spool files. A source revision, changed model, wrong scope/reader/budget, malformed cursor or corrupt tensor is rejected. An unchanged snapshot resumes the unfinished attention computation, not just a high-level task description. In this prototype a source revision triggers a complete restart under the revised snapshot; it does not selectively salvage unaffected intermediate work.

This uses JSON as a record container. It is not a language model generating maintenance notes, and the binary numerical arrays are not language tokens.

## Resources
At primary cap32, no encoder call receives over32 source positions and no attention tile selects more than32 query+key positions. The retained model has18,500 parameters. The cap is NOT total memory: model weights, graph metadata, accumulators, projections, score tiles, allocator workspaces, output logs, full source archive and file-backed intermediate arrays are additional.

At512 tasks the encoded world has2,072 positions. Source plus embedding and two layer files occupy1,102,816 bytes, including NPY headers. The OS may cache those files in RAM. Main process peak RSS reached383,250,432 bytes including framework and full-reference work; it is not a32-record memory result or an isolated per-policy maximum.

## What is and is not learned
The neural model interprets the known disposition rule. The harness supplies exact IDs, two prerequisite links, record retrieval, the hierarchy, data versions, group scheduling, partial-softmax arithmetic and checksums. The harness neither learns a new rule nor infers an unknown dependency. The independent exact scorer solves the entire fixture with ordinary code; it is a ceiling/control, not neural help.

A wider input collection can now be consumed under the fixed active tile, but output quality remains limited by the trained reader. CAP01 contains no new training, autonomous night cycle, natural-language context, DARP, source summarization, identity migration or general transitive reasoning.

## Interfaces
- `graph_and_closure(world, targets, mode)`: retained dense/HSA dependencies.
- `StreamExecutor(..., cap, root)`: source binding, external spools and bounded execution.
- `advance(limit_tiles)`: progress to an interruption point or finish.
- `snapshot(path)` / `restore(...)`: exact checked continuation.
- `logits()`: selected outputs only after completion.
- `full_reference(...)`: separate full-model arithmetic for verification, outside the active cap.

The candidate is a working paged execution primitive. Further investigation of genuinely novel multi-step maintenance needs an appropriate task/learning interface rather than calling these typed records natural-language context.
