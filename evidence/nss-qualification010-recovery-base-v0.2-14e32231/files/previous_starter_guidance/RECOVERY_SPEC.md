# Qualification010 reconstruction specification

**Document type:** recovery proposal grounded in surviving sources; no new Study010 result. **Candidate name:** Qualification010_Reconstruction v0.2 (proposed). Preserve the old v0.1 label exclusively for the original bytes and historical account.

## 1. Evidence classes

**Recovered original bytes:** Study009 archive and the selected code/checkpoints in this starter; user-supplied Study010 report, status review and delivery receipt. Parent009's 501 covered files were actually hashed and its fresh-extraction 45-test suite was actually run in the recovery audit.

**Historical claims:** all Study010 training/test/metric/PASS statements in those three files. The receipt records what the old execution said it did. Its internal paths identify missing evidence; they are not currently mounted files just because the strings exist.

**Missing original Study010 artifacts:** new numerical reader/attention implementation, training code refinements, resolved acceptance table, 140-file local lock, 15 new main checkpoints, development checkpoints and six development attempts, complete 19,960-row metrics and 33,605 raw arrays, independent scorer, continuation fixtures, timing records and other verification logs. Some code can be rebuilt using parent009; that does not recover exact original bytes.

**New decisions:** any unresolved implementation choice, sampler, threshold, architecture layout, seed policy or portable runtime change made now. Record each with rationale, relation to source, impact and status. Nothing becomes historical by resembling an old description.

A hash identifies bytes; it is not a compressed backup. The archived SHA256 cannot recover an absent checkpoint, source file or result array. Reusing a stated seed with reconstructed code does not guarantee the same training data order, final weights or measurements.

## 2. Exact starting point

The original report section 2 says the source was copied from IdentityBinding009 and needed dependencies, with 128 copied files. The exact 128-file copy manifest is absent; do not claim this subset is that manifest. This starter explicitly lists its own recovered subset from verified 009.

Useful present components:
- `nbr009/state.py`: exact scoped ownership, active registry, record presence/readability, transaction and checkpoint mechanics.
- `nbr009/readout.py`: same-store exact ownership traversal and logical-map audit.
- `nbr009/stage_b.py`: state/depth/recovery isolation, candidate setup and nominal/noise cases.
- `reference/parent008/...`: match gates, earlier resolver/pipeline logic, original `nbr006` data/models, frozen record_hop/gated_hop/binder families 801–805, repair families 901–905 and matcher families 1001–1005.
- Existing tests and source-loaded checkpoints: executable recovery, not prose-only reconstruction.

Preserve these as read-only references. New instrumentation belongs in a new layer or an explicitly versioned copy, not retroactive modification of the historical releases.

## 3. Reported numerical task and information contract

Report sections 2 and 4 describe 16 identities/slots, 16 normalized random identity features plus one UNKNOWN coordinate, supplied protected symbol catalogue/active mask/ownership/scope/revision/presence/readability, and qualified registration/writes. Catalogue information is about symbols, not true graph relationships.

Only declared state changes during scoring. A numerical reader receives key/value/valid-record/query tensors, not owner integers, generator graph or correct next-row indices. An explicit assisted condition uses shared code/query cleanup between stages and on output. A direct visible-fact condition removes between-stage cleanup. Exact traversal can use the same stored owner's relationships but must not secretly consult the generator graph.

Reference internal maintenance uses true record owner to reconstruct the key and nearest-catalogue cleanup for the approximate value. Do not retain a clean destination in metadata. Scope/version/transaction/reset semantics must remain explicit. Keep truth of a relation separate from membership in the catalogue.

The cadence of eight events is a selected synthetic corruption-test operating point: Gaussian sigma .02 is deliberately added on events. It is not a measured real-world hardware or companion corruption rate.

## 4. Reported candidates to reconstruct

- Inherited 818-parameter RecordHop families801–805: original checkpoints survive in parent009.
- Cap-only: the same weights with permitted attention-scale cap changed from80 to20000. Inspect actual inherited cap implementation and declare how the new cap is represented.
- Ordinary continuation: inherited initialization, expanded cap, ordinary additional preparation.
- Close-identity continuation: same initialization/budget/base graph draws; half the examples introduce an unrelated identity close to the queried source, with sigma sampled .01–.15.
- Untied attention/pointer control: eight separate self-attention/residual/LayerNorm/MLP blocks, width32,twoheads, explicit17-coordinate entity bottleneck and learned pointer/copy outputs. The report gives94,728parameters, but not a complete layer/tensor specification. Document token layout, activation, hidden widths, normalization placement, masks, missing-record handling, output heads, initialization and stop/continuation mechanics. Parameter count alone is not an architecture specification; do not add inert weights just to match it.
- Exact ownership traversal: on the same candidate-owned store with the candidate resolver, no gold source-graph access.

The new result must not claim universal Transformer inferiority. These are structured, intermediate-supervised task readers with unequal parameter counts and lifetime histories.

## 5. Recoverable training recipe and unresolved parts

Report section3: three new recipes × five paired seeds1201–1205,6000AdamWsteps each,batch64,paths up to8,all8stages trained. Loss=row-selection cross entropy+0.5*squared-code error. Correct previous codes for first1000updates and every fourth subsequent update; otherwise free-running. Cosine LR .0015→.00015,weight decay1e-5,gradient clip5. Near-perturbation RNG kept separate to preserve base-graph pairing. Final-step checkpoints, no selection by main score.

Still resolve exact AdamW defaults/options, RNG sequencing, loss reduction/masks, precise teacher-forcing indexing and per-step interpretation, negative/missing distribution, attention implementation, and full data/job seed formulas. Inspect parent source before treating any value as missing. For each unresolved choice, use an explicit reconstruction decision; do not cite it as recovered fact.

The old15fits/90000steps and151tests are historical counts, not acceptance targets. Do not manufacture missing old development logs. New development failures are stored in their own run IDs. Equal extra examples is not equal lifetime training, compute or parameter budget.

## 6. Evaluation to rebuild and freeze

Reconstruct the documented nominal state/depth task; independently enumerate its exact supported cases before main runs. Visible-fact competence must precede delay/noise conclusions. Use stateoff/on,depth1/2/4/8,four/eight-link chains,1024sigma.02disturbanceevents,cadence8 reference and32 comparison, unrelated writes every64events. Use128streams per paired main case with known/missing counts explicit. Where original enumeration, ordering or seeds are missing, name the new design rather than imply exact replay.

Preserve ordinary registration/no-relation/write/correct/clear/rewrite/denied/wrong-scope/reset/fresh-record phases. Source events independently define the expected logical store; each candidate's actual whole map is scored as well as its queried path. Do not accept global memory integrity from a correct answer alone.

Retain close-source/destination/intermediate cases including sigma.01, near-novel and ordinary unregistered queries, altered-knownquery sigma.2, wrong-valid values, erasure, record permutation and shuffled-value controls. Report uncertainty/rejection and supported coverage together. These broader claims were not qualified historically and remain open unless new evidence changes them.

Source reports say >=95% known/missing per required condition/pair, but the full original protocol and resource ceilings are missing. Recover whatever is present in parent code, document the remaining new acceptance matrix, and freeze it before fresh confirmation. Do not tune it to reproduce the old pass list. Main candidates may pass or fail differently; neither result is a delivery defect.

## 7. Independent scoring and honest comparisons

Implement a scorer from observable source events and stored arrays rather than importing candidate scoring logic. Save per-stream actions, presence/readability, ownership, states, query/stage traces and predicted answers. Assert that the scorer's ground truth is not reachable by candidate code. Test the scorer against deliberately wrong answers/stores, missing links, altered metadata and empty-state loopholes.

For the recovery phase compare recovered inherited bytes and contracts exactly. For new floating-point results, exact reproduction within a pinned environment may be a valid test; across changed versions/hardware, predeclare numerical and behavioral tolerances. Do not weaken a failed criterion after seeing it. Internal fresh-process repetition, another agent's review, user-machine execution and external replication are different evidence categories.

Produce a historical-versus-new matrix: same/different source surface; original numbers as reported; new measured counts/intervals; divergences; cause if established; open diagnosis otherwise. Main rerun is informed by known history, not a newly blind experiment. Never select seeds or code variants to make old percentages reappear.

## 8. Workflow gates and costs

A. Fresh source audit, inherited checkpoint load,45parenttests, gap map and environment budget.
B. Reconstruct missing code and portable tests. If Unix resource telemetry is unavailable, preserve behavioral tests and mark unavailable measurements; do not equate omitted telemetry with passed resource limits.
C. Development competence and mutation tests; archive failures.
D. Freeze new source/config/criteria/main-seed list and budget; allow reviewed confirmatory execution.
E. Train declared fits, retain all checkpoints; score all scenarios and costs. Count development, replay, test, extra-agent and interrupted-run costs separately.
F. Fresh-interpreter checkpoint/evaluation replay, independent rescore, state/RNG/transaction/query-stage continuation and one full-training reproduction. New tests should check behavior rather than chase historical test counts.
G. Package/rehydrate verification, reviewed status decision and user-side receipt. NBR02 stays paused until an executable baseline and regression pack are available.

No permanent source dependence on /mnt/data paths. Output directories are distinct and never overwrite prior runs. Separate persistent state, model weights, transient activations, framework memory and archived evidence; no deployment/latency claims from historical CPU timing alone.

## 9. Deliverables and durable recovery

Use a versioned source/config/test package, a checkpoint package, evidence shards by pair/run, and a small index manifest with hashes and restore instructions. The source package must state which tests run without larger evidence and which require it. Preserve raw failures; partitioning is not permission to drop them. Deterministic archive/compression details are recorded when relevant.

Keep local/project copies of code,weights,recipe,RNG/checkpoints and reports. Put code/spec in the selected version-controlled workspace and large artifacts in the user's selected persistent artifact storage; neither destination is provisioned or uploaded by this starter. Validate the received copy by hash. Never describe a chat link as the only durable research record.

Required new release outputs: source map; reconstruction decisions; candidate config; freeze receipt; checkpoints; raw outcomes; independent scorer; replay/continuation/training receipts; resource report; historical comparison; limitations; new report/status review; archive inventory; tested restore script.

## 10. Source attribution

All reported Study010 details above come from the unchanged files in historical_qualification010/ (REPORT sections2–9, STATUS_REVIEW, DELIVERY_VERIFICATION). Parent availability, hashes and45tests are fresh recovery-audit measurements under audit/. New task/team/packaging suggestions are proposals. No new learning result or scientific qualification has occurred in preparing this starter.
