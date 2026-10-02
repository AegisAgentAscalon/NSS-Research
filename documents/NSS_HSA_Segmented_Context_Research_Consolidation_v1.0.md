# NSS — HSA + Segmented Context
## Consolidated research record and maintenance-token architecture assessment

**Version 1.0 • 28 September 2026**  
**Coverage:** SH01, SH02, SC01, SC02, CAP01 and CAP02, each Execution v0.1.  
**Disposition:** Working bounded component; parked for later integration.  
**Purpose:** Preserve the research questions, implementations, comparisons, results, failures and conclusions before work moves to another theoretical component.

This is a source-grounded consolidation, not a new experiment, independent replication, literature review or whole-NSS qualification. The original six execution archives remain byte-for-byte intact. Preparing this document involved reading source records, indexing retained tests and checking file integrity; it did not load a model, run inference, train, change a scientific threshold or reevaluate held-out data.

**Reading map:** Sections 1–4 explain the objective and common design. Sections 5–10 document each study. Sections 11–13 reconcile evidence boundaries, maintenance-token implications and the integration decision. Section 14 explains the archive and reproduction entry points. The original protocols and complete retained test implementations are supplied with the archive, not replaced by this narrative.

**Source notation:** `[SH01-R, §4]` means `sources/SH01/REPORT.md`, section 4. `-P`, `-A` and `-README` mean that study's original protocol, architecture and README. `INTENT` is the clearly labeled conversation-direction record; `ORIGIN` is the original VargBot/MegaMind concept retained inside SH01. Full locators, hashes and byte counts are in `indexes/SOURCE_CATALOG.json`. Claims described as an *assessment* or *integration implication* are synthesis, not an additional measured outcome.

# 1. Executive synthesis

## 1.1 What the research achieved

The program produced an executable, three-level hierarchical maintenance reader and a versioned segmented workspace around it. Subsequent passes made its execution more efficient, enabled exact attention calculations to continue across small active tiles, and improved the reader's use of larger source layouts through a fixed, bounded preparation phase. This is a useful component-level result, not merely a collection of architectural labels. [SH01-R, §§1–5; SH02-R, §§1–3; SC01-R, §§1–4; CAP01-R, §§1–6; CAP02-R, §§3,6,8]

Four achievements should remain distinct:

| Achievement | Evidence | Scope |
|---|---|---|
| A useful hierarchical inductive bias | SH01 HSA: 6,133/6,144 correct decisions; dense: 5,553/6,144, across three complete pairs. | Same narrow rule, paired initialization and fixed training recipe; supplied dependency links. |
| Working maintenance information management | SC01 and SC02 preserved full-reader decisions while handling revisions, interruption, receipts and bounded packets. | Program-managed typed records, not a language model writing its own notes. |
| Executable input reach beyond a resident packet | CAP01 completed calculations requiring 69–755 input positions per selected HSA task using a 32-position active tile. | Exact multi-pass execution with external storage; ordinary streaming obtained the same reach. |
| Better interpretation after broader preparation | CAP02 mixed-size HSA: 766/768 selected decisions at 128 tasks, with 768/768 at eight tasks. | A fixed continuation phase, not a new rule, general reasoning result or full-night lifecycle. |

The executive values come from different experiments with different panels. They are not a single common benchmark or a combined success rate. [SH01-R, §4; SC01-R, §3; SC02-R, §4; CAP01-R, §§3–4; CAP02-R, §§2–3]

## 1.2 The capability result is not just a speed result

The central capacity finding is that an unfinished attention computation can survive between segments. The full required evidence no longer has to fit simultaneously into one active packet. CAP01 preserves the original allowed connections and one joint softmax while paging keys and storing layer results externally. Under its fixed 32-record tile, selected 32-, 128- and 512-task computations that the resident-packet control could not admit were completed with unchanged class decisions and admitted numerical agreement. [CAP01-R, §§1,4,6; CAP01-A]

This does not mean 32 positions contain the entire source collection's meaning. The system retains and rereads exact evidence and intermediate arrays outside the tile. Nor does more accessible information automatically mean competent interpretation: CAP01 exposed larger-layout errors made by both the streamed and full-reference models. CAP02 addressed that particular preparation question, with improvement and retained small-task competence. [CAP01-R, §§4–7; CAP02-R, §§3–4]

## 1.3 Efficiency improved, but not every proposed mechanism helped

SH02 reduced duplicated key/value gathering and was approximately 3.71 times faster than the original HSA at 128 tasks and 5.63 times faster at 512 in its batch-one timing session. Its smallest case became slower, and dense attention remained faster in most measured shapes. [SH02-R, §§4–5]

SC02's incremental publication and reusable plans produced material savings on changing-evidence workloads. On the contemporaneous 32-task churn fixture, SC01 took 20.939 ms and the improved scheduled path took 16.367 ms. However, generic improvements also benefited the conventional-cache reference. The additional neural intermediate cache avoided almost 47% of first-layer row computations but was slower in all 20 timing cells. It should remain available as an experimental negative, not the default. [SC02-R, §§1,5–9,12]

## 1.4 What this means for maintenance-token architecture

**Assessment:** HSA plus segmented execution is a defensible substrate to retain for a future NSS maintenance-token interface. It offers explicit evidence identity, bounded active work, checked resumption and an actual mechanism for finishing computations larger than the active packet. This supports proceeding to another component instead of demanding perfection from the current classifier. [SC01-A; CAP01-A; CAP02-R, §8]

It is not yet a tested language-token maintenance architecture. The reader consumes 37 engineered numerical features per record position, not tokenizer-produced language tokens. JSON stores records and resume envelopes; it is not generated or interpreted as free-form maintenance language by the model. No 25,000-token active or whole-night allowance, DARP output generation, learned semantic selection, reliable summarization, autonomous repair planning, identity continuity or repeated day/night adoption cycle was qualified. [SH01-R, §§2,9; CAP01-R, §9; CAP02-R, §§1,8]

## 1.5 Closeout position

Retain the three-level component, the strong ordinary comparators, original checkpoints, mixed-prepared candidates, complete protocols and failure evidence. Do not require an extra hierarchy level, tri-core topology or the slower neural cache. The current research direction is to park this subproblem for integration and move to other theoretical ideas; DARP's maintenance-output role is the previously discussed next candidate, not an experiment authorized by this consolidation. [CAP02-R, §8; INTENT]

# 2. Research intent and question map

## 2.1 Original concept and current purpose

The retained VargBot/MegaMind concept distinguishes *native context* from *effective context*: a bounded active input should be able to use a much larger exact archive through selection, metadata, summaries and provenance. Its proposed local detail, distant selected evidence and global anchors motivated the later HSA/segmented research. The older document's million-token examples and multi-level memory pyramid are aspirations, not measured outcomes or the exact three-level neural graph implemented here. [ORIGIN, §§1–5,9,20–25]

The owner's later discussion made the current objective more specific: test these ideas as **NSS maintenance architecture**, including recording, evidence use, repair support, unfinished-task handoffs and next-day continuation. Speed matters as a resource cost, but the core intention also includes expanded capability: handling information and relationships that do not fit in one ordinary active packet. The scope moved from initial feasibility, through engineering cleanup, to capacity and preparation tests. [INTENT; SH01-P; SC02-R, §1; CAP01-R, §§1,9]

The preferred surrounding lifecycle is stable serving weights during active daytime use and bounded learning/repair of candidates during low usage. Current evidence and task state may still change during the day. This is design direction from the conversation, not a lifecycle demonstrated by these six studies. Tri-core is not a required/default successor architecture. DARP remains primarily an output architecture, with maintenance records as a possible application. [INTENT]

## 2.2 Consolidated research questions

The identifiers below are an editorial cross-study map, not retroactively registered test IDs. Original prospective wording and criteria remain in each `PROTOCOL.md`.

| ID | Question | Evidence-based disposition |
|---|---|---|
| HSC-Q01 | Can the components be implemented with distinct, inspectable interfaces? | Yes, bounded: SH01 shared records; SH02 isolated graph/plan/backend; SC01–CAP01 explicit execution lifecycle. |
| HSC-Q02 | Does supplied hierarchy help learning a maintenance rule? | Yes under SH01's fixed recipe and three completed pairs; not a universal dense-attention limitation. |
| HSC-Q03 | Does fewer attention work mean lower latency or memory? | Not automatically. SH01 lost on time; SH02 packing helped at larger shapes; total-memory/energy superiority remains unestablished. |
| HSC-Q04 | Can cleanup preserve the original computation? | SH02 preserved class decisions and numerical tolerance; historical bitwise replay mismatch remains recorded. |
| HSC-Q05 | Can a bounded workspace handle revisions and interrupted jobs? | Yes on SC01/SC02 typed fixtures, with exact source/model binding and explicit deferrals. |
| HSC-Q06 | Does segmentation beat competent conventional caching? | Sometimes in time, not universally; no unique answer-quality advantage shown. |
| HSC-Q07 | Does caching intermediate neural work improve maintenance cost? | The tested SC02 cache saved computation but lost runtime in all 20 timing cells. |
| HSC-Q08 | Can required computation span packets smaller than its closure? | Yes in CAP01 through carried joint-softmax arithmetic and external layer storage. |
| HSC-Q09 | Is custom hierarchical grouping necessary for that capacity? | No in the tested implementation: ordinary multi-pass grouping matched answers and numerical agreement. |
| HSC-Q10 | Does more input reach reliably improve interpretation? | Access works; larger-layout mistakes remained. This is not new-rule or deeper transitive reasoning. |
| HSC-Q11 | Can broader preparation improve large-layout behavior without losing the small rule? | Yes, bounded in CAP02; 128-task HSA improved with eight-task retention, while 512-task stress remained imperfect. |
| HSC-Q12 | Is the proposed 25,000-language-token maintenance system established? | No. No tokenized writer/reader or active-versus-cumulative language-token budget was tested. |
| HSC-Q13 | Are three hierarchy levels optimal, and is the whole NSS lifecycle qualified? | Neither. Three is the retained working choice; depth optimization and full lifecycle remain untested. |

Sources: [SH01-R, §§1–9; SH02-R, §§1–7; SC01-R, §§2–10; SC02-R, §§1–12; CAP01-R, §§1–9; CAP02-R, §§1–8].

## 2.3 Why the sequence changed emphasis

SH01 first asked whether HSA and persistent records could function together. Its speed loss motivated SH02's backend cleanup. SC01 then tested bounded segmented job management, and SC02 removed avoidable rebuilding while testing more ambitious reuse. After the owner clarified that expanded capability mattered more than incremental timing, CAP01 changed the execution admission boundary itself. CAP02 was the single final preparation/retention check requested before moving on. [Study protocols; INTENT]

This history matters: SC01/SC02 were designed largely to preserve the same answers while changing execution. Their equal accuracy is not a negative experiment on every possible capability benefit. Conversely, CAP01's new capacity should not be reassigned to a uniquely superior custom selector, because its ordinary comparator had the same multi-pass mechanism. [SC02-R, §4; CAP01-R, §§2–4,9]

# 3. Common architecture, task and measurement rules

## 3.1 The learned task

Each source world supplies task identities, progress fields, two declared prerequisites per task, receipt/constraint distractors, regional metadata and a global freeze flag. The neural target is deliberately simple:

```text
if global_freeze:                 DEFER
elif task_is_complete:            COMPLETE
elif both_prerequisites_complete: READY
else:                             BLOCKED
```

The exact software scorer can solve this rule without a neural model. It is a ceiling/control used to isolate the learned interpretation of supplied records, not evidence that NSS should replace deterministic bookkeeping with a classifier. The tests do not teach arbitrary semantic exceptions, discover unknown prerequisites or require longer prerequisite-hop reasoning as the world grows. [SH01-P; SH01-R, §3; CAP01-R, §1; CAP02-R, §2]

## 3.2 The common reader and hierarchy

The learned reader has 37 input feature channels, projection width 32, two attention/FFN blocks, two attention heads, FFN width 64, layer normalization and a four-class readout. It has 18,500 trainable parameters. SH01 trains dense and HSA variants with paired initial tensors; subsequent engineering passes preserve the trained parameters and graph. CAP02 alone performs further learning on those exact parents. [SH01-P; SH01-R, §3; CAP02-R, §1]

| Hierarchy level | Positions and connectivity |
|---|---|
| Task | Four positions per task: query/metadata, progress, receipt and constraint. Attend to local records, declared prerequisite records, own-region task anchors, regional anchors and the global anchor. |
| Region | Metadata anchor for a region. Attends to that region's task-query anchors, itself and the global anchor. |
| Global | One anchor containing the maintenance freeze flag. Attends to regional anchors and itself. |

The exact graph is specified in the source, including self connections and original stage ordering. Region anchors are engineered metadata, not natural-language summaries or precomputed desired dispositions. HSA is native selected-edge attention, not merely an external retriever feeding an unchanged dense transformer. The dense competitor uses dense SDPA; a same-graph masked-dense path is a numerical reference, not the trained dense competitor. [SH01-P; SH01-R, §2; SH02-A]

Three levels were retained to avoid unnecessary complication, but no controlled hierarchy-depth sweep established an optimum. With bounded prerequisites and the existing square-root regional organization, SH02 identifies approximately O(N sqrt(N)) allowed-edge growth, not linear or arbitrarily recursive scaling. [SH02-R, §2; INTENT]

## 3.3 Separate the learned and supplied functions

| Supplied by program logic | Learned or numerically executed |
|---|---|
| Record identity, versions, scopes and source visibility | Interpretation of supplied evidence into the four dispositions |
| Exact dependency links and graph construction | Dense or HSA attention under the declared graph |
| Packet selection, scheduling, cache invalidation and receipts | Fixed trained projections, FFNs, normalization and readout |
| JSON checkpoints, checksums, cursor tracking and external arrays | Cross-tile accumulation of the same attention operation; this arithmetic is implemented, not learned |

The distinction is essential. A software manager preserving a source record is not a neural memory discovery. A neural output is advisory, not authorization, ground truth or proof that an external action occurred. Likewise, successful cross-tile arithmetic is valuable system capability without being new learned reasoning. [SH01-R, §§2–3; SC01-A; CAP01-A]

## 3.4 What a segment means across the versions

In SH01, persistent segments are version-bound selected packets. In SC01/SC02, a segment is a bounded exact dependency closure for a group of requested outputs, with durable maintenance progress between groups. If one task's closure is too large, it is deferred. In CAP01, even the attention calculation within a task can span successive key tiles; exact arithmetic state and layer arrays preserve the work. These are increasingly capable execution mechanisms, not interchangeable claims about a fixed language-token context. [SH01-R, §§2,5; SC01-A; CAP01-A]

The two-block reader uses simultaneous layer semantics. Selected second-layer queries need their first-layer key representations, and those require their own original input neighborhoods. Because tasks read all regional anchors, even one final task depends on task-query metadata across the world. Paging detailed evidence is possible; pretending all tasks are independent local islands would change the computation. [SC01-R, §4]

## 3.5 Numerical and evidence discipline

The SH/SC/CAP float32 comparison envelope is `abs(candidate-reference) <= 2e-5 + 2e-5*abs(reference)`. The float64 engineering reference uses `1e-10 + 1e-9*abs(reference)` where specified. These are the SH01-family contracts, not a retrospective relaxation of the earlier recurrent studies' different numerical gates. Class preservation, tolerance agreement and bitwise archival identity are distinct checks. [SH01-P; SH02-R, §3; CAP01-R, §6]

Worlds, tasks within worlds, seeds, reused snapshots, policies and repeated observations are not independent samples. Confirmation later reused for refactor checks becomes exposed regression evidence. Different studies' percentages and timing scopes must not be pooled into one score or read as a continuous benchmark improvement curve. [SH01-R, §§3–5; SC01-R, §§3,6; CAP02-R, §2]

# 4. Study sequence and model lineage

| Study | Primary purpose | Learned-weight work | Completion and result scope |
|---|---|---|---|
| SH01 | First native HSA + versioned packet prototype; learning and four-way comparison | Eight fresh fits planned; seven completed; one HSA final unavailable | Working prototype, partial training cohort; three complete pairs used |
| SH02 | Clean graph/plan/backend separation and packed execution | No optimizer steps | Same decisions, admitted numerical parity; strict historical bitwise mismatch retained |
| SC01 | Bounded segmented maintenance jobs and fair caching controls | No optimizer steps | 324 completed conditions; lifecycle and equivalence work |
| SC02 | Incremental publication/planning; scheduling and neural-cache ablations | No optimizer steps | 720 completed conditions; useful engineering gains, cache negative |
| CAP01 | Continue exact computation across tiles smaller than required resident closure | No optimizer steps | 488 completed cases; capacity gain available to both manager policies |
| CAP02 | Larger-layout preparation with small-task retention; bounded closeout | Twelve 96-update continuations from six original parents | 1,152 main + 3 preflight applications; working component parked |

SH01's complete paired seeds are 8801, 8802 and 8804. Seed 8803/dense completed, but 8803/HSA has only its durable step-200 checkpoint; it was never substituted into the complete-pair comparison. SH02/SC01/SC02 mainly reuse the three HSA finals. CAP01 carries both dense and HSA finals for the three complete pairs. CAP02 forks each of those six parents into small-only and mixed-size continuations while retaining the untouched state. [SH01-R, §§1,8; SH02-R, §1; CAP01-R, §§1–2; CAP02-R, §1]

**Update accounting:** SH01's main applications are bounded at 4,400–4,600, with four additional preflight applications. The interval reflects an interrupted process with unsaved work, not a newly estimated exact number. CAP02 has exactly 1,152 main and three preflight applications. Therefore the reported series total is 5,552–5,752 main applications, or 5,559–5,759 including the seven disposable applications. This is simple summation of the retained study accounts, not an inference/FLOP/energy total or a recomputation of missing logs. [SH01-R, §8; CAP02-R, opening and §7]

The full original archives include all retained checkpoints, not just favorable endpoints. No additional fitting, inference or model deserialization was performed for this consolidation.

# 5. SH01 — First working shared architecture

## 5.1 Question and design

SH01 asked whether an exact versioned segment manager and genuinely sparse hierarchical reader could operate together on maintenance records, survive checked restart and support interpretable quality/cost comparisons. `source/store.py` supplies the append-only versioned store, dependency-based assembly, scope/cutoff checks, invalidation and action receipts. `source/common.py` implements the compiler and dense/HSA readers; `source/demo.py` consumes and emits fixed-format JSON. [SH01-P; SH01-R, §2]

Both managers select the same evidence through the same exact index. The simple manager rebuilds packets; the persistent manager reuses valid packets. Both still decode/compile the packet and run the reader on a cache hit. This isolates packet persistence rather than advantage over an intentionally weak retriever or free reuse of neural activations. [SH01-R, §2]

## 5.2 The tests themselves

Eight 600-update fits were planned: dense/HSA for seeds 8801–8804. Every fit received the same 9,600 training worlds as 600 batches of 16 eight-task worlds. AdamW used learning rate 0.002, betas 0.9/0.999, epsilon 1e-8, weight decay 0.01, clipping 1.0, zero dropout and deterministic float32 CPU execution. Only step 600 was the primary endpoint. [SH01-P]

Confirmation used 256 new eight-task worlds, 2,048 decisions per model. A separate 64-world, sixteen-task stress panel supplied 1,024 decisions per model. Train/development/confirmation/stress fixture seeds were 771001/771002/771003/771004; content fingerprints were disjoint. The per-fit functional targets were at least 95% decision accuracy and 90% macro recall; other results were not suppressed when a target failed. [SH01-P; SH01-R, §3]

The integration used 16 additional worlds with six jobs: initial assembly, warm reuse, source revision, restart and continued reuse. Four configurations crossed simple/persistent management with dense/HSA reading. Engineering exercised lifecycle correctness, explicit faults, numerical output/gradient agreement and inspection of native sparse shapes. Timing separately measured the full neural reader and the manager-only lifecycle, with different inclusion boundaries. [SH01-R, §§5–7]

## 5.3 Learning and integration results

| Seed | Dense confirmation | HSA confirmation |
|---|---|---|
| 8801 | 1,854/2,048 (90.527%) | 2,048/2,048 (100.000%) |
| 8802 | 1,842/2,048 (89.941%) | 2,038/2,048 (99.512%) |
| 8803 | 1,855/2,048 (90.576%) | No final; saved step 200/600 |
| 8804 | 1,857/2,048 (90.674%) | 2,047/2,048 (99.951%) |

Across the three complete pairs, dense scored 5,553/6,144 decisions and 368/768 whole worlds; HSA scored 6,133/6,144 and 758/768. False COMPLETE counts were ten versus one. HSA's sixteen-task stress score was 3,063/3,072 (99.707%). The supplied graph clearly helped in this recipe, but the dense reader was not exhaustively optimized. [SH01-R, §4]

The integration produced 2,187/2,304 correct decisions for each dense-management combination and 2,304/2,304 for each HSA-management combination. Simple and persistent managers produced identical packets and decisions. Persistent management recorded 64 hits and 32 packet builds across each 96-job reader/seed workload; simple management rebuilt 96 times. This does not demonstrate an additional accuracy interaction between custom segmentation and HSA. [SH01-R, §5]

## 5.4 Cost results and limits

| Tasks | Dense reader ms | Initial HSA ms | HSA relative result |
|---|---:|---:|---|
| 8 | 0.237 | 0.591 | 2.50 times slower |
| 32 | 0.588 | 1.371 | 2.33 times slower |
| 128 | 2.320 | 8.092 | 3.49 times slower |

These single-thread, batch-one neural timings include projection, both blocks and the readout, but not the source/manager lifecycle. At 128 tasks the HSA path used about 93.13% fewer padded score cells, yet selected K/V gathering materialized 4,829,184 bytes per layer. Fewer edges did not establish lower elapsed time or total memory. [SH01-R, §6]

The separate six-job manager-only cycle fell from 1.417 to 0.970 ms at eight tasks, 5.653 to 3.677 ms at 32, and 20.079 to 14.009 ms at 128. It included construction, updates and restart but excluded the neural reader and record-vector compilation. At 128 tasks both managers still delivered 359,268 serialized packet bytes to the reader. Source rereading fell; neural input traffic did not. [SH01-R, §6]

## 5.5 Failures and conclusion

A snapshot-aliasing bug contaminated a supposedly independent preflight copy. It was fixed by deep-copy isolation before scientific lock, with the original source/traceback preserved. The corrected suite passed 664 assertions, including seeded lifecycle and 11 deliberate fault checks. Numerical comparisons included 32,640 attention-output and 97,920 gradient scalars. All 21 saved final-output files replayed bit-exactly in the study's fresh process; all 30 retained checkpoint model hashes matched. [SH01-R, §7]

The initial runner interruption left the HSA 8803 fit incomplete and lost the initial in-memory per-update loss list. It also left the first process's terminal time/RSS unavailable. Only the untouched 8804 fits were later completed; no uncertain training prefix was replayed. These evidence gaps remain inside the archive and constrain any complete-cost assertion. [SH01-R, §8]

**Conclusion:** The shared interface works and HSA helps learn the controlled rule, while packet persistence saves assembly. Initial sparse execution is slower. This justified implementation cleanup, not a claim of full maintenance efficiency. [SH01-R, §9]

# 6. SH02 — A clean hierarchical reader

## 6.1 Question and implementation

SH02 isolated immutable topology, feature encoding, plan compilation, bounded topology cache, numerical backend and learned reader. It preserved every original graph edge, one joint softmax, the 37-feature adapter and all learned parameters. The four positions belonging to a task share a neighborhood; packing them together gathers the neighborhood once rather than four times. Regional/global singleton queries use a separate bucket. [SH02-R, §§1–2; SH02-A]

The cache stores graph plans only. A value change permits topology reuse but requires renewed feature/reader computation. A dependency, layout or scope change requires a new plan. The planner accepts variable prerequisites, but the trained feature adapter deliberately retains exactly two. No context policy, DARP or new neural ability was added. [SH02-R, §2]

## 6.2 Tests and preservation result

The 92-case engineering suite covers graph/feature equivalence, native versus reference output and gradients, full-reader gradients, invalid layouts/dependencies, cache eviction, forbidden-edge noninterference, stale/corrupt/mutated plans and nonfinite inputs. It reported 623,800 scalar comparisons with no tolerance violation. Full-model regression compared both blocks and logits across 2,918,400 stage scalars, also within the original envelope. [SH02-R, §3]

All 9,984 retained HSA development/confirmation/stress decisions stayed unchanged. Exposed confirmation remained 6,133/6,144, including its old mistakes. This is successful refactoring on an exposed regression panel, not fresh confirmation of new learning. [SH02-R, §§1,3]

## 6.3 Runtime, storage and preparation

| Tasks, batch one | Old HSA ms | Packed HSA ms | Dense ms |
|---|---:|---:|---:|
| 8 | 0.6226 | 0.7934 | 0.2663 |
| 32 | 1.7751 | 1.2772 | 0.5324 |
| 128 | 9.5426 | 2.5691 | 1.9619 |
| 512 | 71.2465 | 12.6545 | 19.5640 |

All timing backends used identical weights and inputs, five warmups and 31 interleaved samples. Full dense has different connectivity, so this is not an equal-quality trained-model comparison. Packed HSA is slower at the smallest batch-one case and beats dense only at the largest batch-one case in this grid. At batch 16 it improves on old HSA at all tested sizes, but dense is still faster. [SH02-R, §4]

Known gathered K/V payload shrank by roughly 75%; at 128 tasks it fell from 4,829,184 to 1,189,888 bytes per layer. That is not a total-memory reduction. Graph preparation is separately charged: 128-task plan build about 1.036 ms and complete cold packed path about 4.505 ms. Profiling identifies old indexing, multiplication and reduction costs; indexing/copying remain material in the new path. [SH02-R, §§4–5]

## 6.4 The retained historical replay discrepancy

All nine historical logit files differed in low-order values even under unchanged SH01 source in the current runtime, making the strict regression driver return exit 1. The largest legacy/archive difference was at most 2.38418579e-6; classes and numerical tolerances matched. The cause remains unresolved and is not automatically attributed to hardware or rounding. Current fresh processes reproduced all nine new cleaned files bit-exactly. These are different outcomes, all retained. [SH02-R, §3]

The cost sweep was interrupted after six conditions; only the missing seventh was completed, with the earlier samples preserved. The first process's terminal resource totals remain unavailable. [SH02-R, §6]

**Conclusion:** Retain the clean three-level graph and packed backend. Neither hierarchy-depth optimality nor universal latency/total-memory advantage was established. [SH02-R, §7]

# 7. SC01 — Segmented maintenance workspace

## 7.1 Question and comparisons

SC01 asked whether bounded maintenance work can use the unchanged HSA reader without dropping dependencies, while handling revisions, repeated requests, interruption and resume. The planner computes the exact two-layer backward closure for requested outputs, preserving original global row identities and stage semantics. A complete closure must fit or the task explicitly defers. [SC01-P; SC01-R, §1; SC01-A]

Three policies share durable jobs/receipts and a bounded plan cache. INDEX retrieves and processes without source/result memoization. CACHE adds bounded source-row and final-task-result LRU reuse, validating complete dependency-version fingerprints. SEGMENT has the same capacities, event-based invalidation and greedy dependency-overlap grouping. Ordinary caching is not denied progress or correct retrieval. [SC01-R, §2]

## 7.2 Test design and results

There are 36 fresh episodes: three sizes (8/32/128), two initial seeds and six families (reuse, sweep, churn, revisions, resume, undersized). Three HSA models and three policies yield 324 executions. Main input caps are 40/128/384 typed rows; the deliberate insufficient caps are 16/32/128. The result cache has 32 entries. Normal episodes make 12 requests of up to eight tasks; resume adds interrupted work and changed evidence. [SC01-R, §3]

| Functional measure | Recorded outcome |
|---|---|
| Available answer observations | 26,604; zero changed classes versus full SH02 |
| Score comparisons | 106,416; zero breaches of original tolerance |
| Full request occasions | 3,294 completed |
| Deliberate partial requests | 54, with unfinished work preserved |
| Undersized requests | 648 request occasions; 5,184 task-answer attempts explicitly deferred |
| Duplicate version-bound advisory receipts | Zero |
| Peak active input rows | 36 / 126 / 383 within the respective caps |

Equivalence is not perfect model accuracy. Per policy, learned accuracy was 2,903/2,940 at eight tasks, 2,964/2,964 at 32, and 2,955/2,964 at 128. The same errors remained across policies. [SC01-R, §3]

The exact single-task closure spans 24–36 of 36 source positions at eight tasks, 66–96 of 135 at 32, and 209–254 of 524 at 128, across the two initial layouts. All task-query metadata remains necessary because of the global regional-anchor path. The archive is RAM-resident; active-row limits exclude several other allocations. [SC01-R, §4]

## 7.3 Timing and attribution

| Tasks / episode | INDEX ms | CACHE ms | SEGMENT ms |
|---|---:|---:|---:|
| 8 / reuse | 19.229 | 5.103 | 4.142 |
| 8 / resume | 25.976 | 11.225 | 9.990 |
| 32 / churn | 76.823 | 40.636 | 38.477 |
| 32 / resume | 90.515 | 22.548 | 24.195 |
| 128 / reuse | 126.644 | 23.312 | 20.852 |
| 128 / sweep | 75.015 | 72.593 | 71.985 |
| 128 / churn | 156.717 | 78.592 | 74.583 |
| 128 / resume | 184.679 | 47.335 | 44.987 |

These are selected rows from the complete 12-cell table in the original report, not per-workload chosen winners. One model, one timing seed, one CPU thread, one warmup and nine interleaved samples define the scope. The whole-episode core includes ingestion, retrieval, planning, reading, revisions, receipts and JSON restart; it excludes model/process startup, full-reference scoring and actual disk durability. SEGMENT had a lower median in 11/12 cells but was 7.31% slower in 32-task resume. Small differences are not a general superiority claim. [SC01-R, §6]

Most savings come from ordinary caching. Greedy segmentation sometimes increases reader calls: at 128 tasks, reuse was three versus CACHE's two, churn 14 versus 13, and resume five versus four. The smallest sweep repeats its eight tasks; only the 128-task sweep supplies 96 distinct targets with little answer reuse. [SC01-R, §§5–6]

## 7.4 Verification and outcome

Engineering passed 34 explicit cases, including ten faults, plus 12 pipeline preflights. A pre-lock verifier incorrectly selected float64 tolerance from JSON containers holding float32-computed values; the precision selection was fixed before main lock, not by changing the numerical envelope. Two timing interruptions were retained, with only missing resume families completed. [SC01-R, §8]

Independent recount covered all 324 result files; 216 policy/status comparisons agreed, 54 selected episodes replayed bit-exactly and 36 saved workspaces resumed to matching traces. These are source-reported internal checks, not a fresh consolidation rerun. [SC01-R, §9]

**Conclusion:** A working bounded workspace and HSA integration, with modest, workload-dependent incremental value beyond a strong cache. It is not yet multi-pass execution of an individually over-budget task. [SC01-R, §10]

# 8. SC02 — Incremental execution and useful negative results

## 8.1 Question and five arms

SC02 tested avoidable publication/planning work, a better grouping choice and intermediate neural reuse while preserving the existing graph, labels, weights and information. It is an efficiency study of the same capability, not a new capability-learning experiment. [SC02-P; SC02-R, §§1–2]

| Arm | Mechanism |
|---|---|
| C | Unchanged SC01 conventional cache and request order |
| S | Unchanged SC01 event invalidation and greedy overlap grouping |
| F | Incremental/vectorized compilation, reusable graph plans, exact-signature reuse; conventional order |
| P | F engineering plus choose between ordinary and overlap packings by group count, closure rows and first-block rows |
| I | P plus a bounded, model/source-version-checked first-layer output cache |

F receives the same generic engineering improvements as P/I. Ordinary source changes patch affected detail rows, freeze patches the global row, and dependency changes rebuild validated topology/features. Restored caches are cold; no cross-weight activation migration is claimed. [SC02-R, §2]

## 8.2 Test design and preservation

Forty-eight fresh episodes combine three sizes, two new seeds and eight families: reuse, sweep, churn, revisions, resume, oversize, eviction and global change. Three HSA checkpoints and five arms yield 720 executions. Eviction uses four result entries; other result capacities and input budgets match. [SC02-R, §4]

All 61,620 available observations preserved full-reader classes. All 246,480 numerical comparisons stayed within the original envelope; duplicate receipts were zero. Each arm had the same 12,199/12,324 correct answers (98.9857%), not perfect learned behavior. Undersized attempts were explicitly deferred, while intentional interrupted positions remained separately unresolved. [SC02-R, §4]

## 8.3 Contemporaneous timing, not historical subtraction

| Workload | Old cache C | SC01 S | Fast cache F | Scheduled P | Neural cache I |
|---|---:|---:|---:|---:|---:|
| 8 / resume | 6.712 | 6.029 | 7.222 | 6.998 | 7.241 |
| 32 / churn | 23.632 | 20.939 | 16.849 | 16.367 | 18.310 |
| 32 / resume | 14.863 | 13.144 | 13.757 | 12.939 | 14.959 |
| 128 / sweep | 47.335 | 47.788 | 35.073 | 37.414 | 44.213 |
| 128 / churn | 52.360 | 49.490 | 26.532 | 28.925 | 30.791 |
| 128 / resume | 36.427 | 33.819 | 27.451 | 26.884 | 30.763 |

All values are median milliseconds from selected rows of the original 12-cell retained-workload grid. Eleven interleaved repetitions follow a prescribed warmup. Crucially, unchanged SC01 already ran the historical 24.195 ms resume case in 13.144 ms in this session. P's 12.939 ms is only a 1.6% contemporaneous improvement; claiming 24-to-13 from code changes would be unsupported. [SC02-R, §§1,5]

P beat S in 9/12 retained cells, but was slower in all three non-churn eight-task cells. Its equal-cell geometric time ratio to S was 0.88585; P versus F was almost tied at 0.99581. These are descriptive grid summaries, not deployment-weighted means. [SC02-R, §5]

Fresh seed 942203 supplied eight 32/128-task timing cases after source freeze, each with seven interleaved repetitions. P beat S in six and C in all eight. Fresh 128-task churn fell from 55.691 ms (S) to 32.029 ms (P), but fresh 32-task resume rose from 13.833 to 14.155 ms and sweep also worsened. All 20 timing cells, including losses, remain in the original report and raw files. [SC02-R, §6]

## 8.4 What saved work, and what did not

On retained 128-task churn, median publication fell from 12.782 ms to 0.298 ms. Encoded material over initial publication plus 12 changes fell from 1,008,176 to 79,328 bytes, because unchanged records were not repeatedly rebuilt. This is avoided rematerialization, not compression of source truth. F obtains the same publication benefit, so it is not unique to segmentation. [SC02-R, §7]

I reused 28,800 of 61,344 first-layer output-row demands, avoiding 46.95% of those computations. Nevertheless it was slower than P in all 20 timing cells, with geometric slowdowns about 14.7% on retained and 15.0% on fresh grids. It added up to 49,152 bytes of neural tensors, with additional validity and plan metadata. Their separately measured maxima are not a summed simultaneous peak. Validation, copying and partial planning are plausible overheads, not independently isolated causes. [SC02-R, §§8–9]

## 8.5 Verification and conclusion

All 34 engineering checks passed, including source mutation/revision, scope/model replacement, stale intermediates, corruption, budget and eviction controls. One caller timeout left 713/720 conditions durable; a separately identified driver evaluated only the seven missing conditions. No completed outputs or frozen scientific source were replaced. [SC02-R, §10]

Recount covered all 720 files with no discrepancy, 576 semantic comparisons agreed, 36 selected episodes replayed bit-exactly and 24 workspaces resumed to matching traces. Model and source locks remained intact. [SC02-R, §11]

**Conclusion:** Retain incremental publication, graph-plan reuse and validated signature reuse. Keep F and P as alternatives; leave I disabled by default. This materially improves a first implementation but does not establish unique segmentation superiority or lower cost for every workload. [SC02-R, §12]

# 9. CAP01 — Expanded execution capacity across segments

## 9.1 The new research question

CAP01 directly tested the owner's capability intention: can the reader finish work when its required input closure exceeds the active packet allowance? SC01/SC02 deferred such work. CAP01 carries exact unfinished attention arithmetic across key tiles, writes layer results externally and preserves every original graph edge and learned parameter. Ordinary and hierarchical grouping both receive this ability. [CAP01-P; CAP01-R, §§1–2]

The ordinary manager groups consecutive queries; the segmented policy groups queries with identical HSA neighborhoods. Both can retrieve repeatedly, preserve progress, serialize a pause and restart on current evidence. This fair control prevents attributing ordinary streaming's general capacity to an exclusive architectural name. [CAP01-R, §1]

## 9.2 How one attention calculation survives its segments

For each query, retain the running score maximum `m`, denominator `l` and unnormalized value numerator `o`. For the next score tile `s` and values `v`, the original architecture specifies:

```text
m_new = max(m, max(s))
l_new = exp(m - m_new) * l + sum(exp(s - m_new))
o_new = exp(m - m_new) * o + sum(exp(s - m_new) * v)
final_attention = o / l
```

Both old and new terms are rescaled consistently, retaining one joint softmax rather than averaging independent segment answers. Empty admitted prefixes are handled without NaNs. Layer-one rows are completed before their values are used in layer two; execution does not mix simultaneous stages. Numerical equality is checked within the original envelope, not asserted bitwise across accumulation orders. [CAP01-A]

A JSON resume envelope records source/model/topology identity, manager mode, target IDs, budget and layer/group/key cursors. Binary-encoded exact accumulators with shapes/dtypes/checksums and referenced source/embedding/layer files preserve actual numerical computation. A changed source or model rejects the old state. A revised source triggers conservative restart, not selective migration. [CAP01-A; CAP01-R, §6]

## 9.3 Test matrix

Primary: 432 cases at 8/32/128 tasks, two worlds per size, three scenarios, two snapshots, three paired seeds, dense/HSA and two manager policies. The scenarios concern dispersed prerequisites, a global override and a revised dependency after interruption. Six base worlds underlie these repeated comparisons, not 432 independent random problems. [CAP01-R, §2]

Separate stress: 24 cases at 512 tasks using only pair 8801 and one world. Tile-size sensitivity: 32 cases at 128/512 on two additional worlds, capacities 16 and 64, also pair 8801. Total: 488 cases. The primary cap of 32 counts active query plus key **record positions**, not language tokens or total memory. [CAP01-R, §§2,4,7]

## 9.4 The capacity boundary moved

| Source tasks | Full positions | Selected task's old HSA input closure | New active tile |
|---|---:|---:|---:|
| 8 | 36 | 30–36 | 32 |
| 32 | 135 | 69–96 | 32 |
| 128 | 524 | 218–260 | 32 |
| 512 | 2,072 | 602–755 | 32 |

At 32 tasks and above, the listed complete closures cannot fit into 32 positions, yet both streamed policies finish with unchanged decisions. That is a demonstrated expansion of executable reach relative to the same-budget resident control. It is not information compression into a 32-position hidden state; the source and intermediate files remain available outside the active tile. [CAP01-R, §4]

## 9.5 Learned quality on accessible evidence

| Source tasks | Dense correct | HSA correct | Dense whole jobs | HSA whole jobs |
|---|---|---|---|---|
| 8 | 204/240 | 240/240 | 6/30 | 30/30 |
| 32 | 225/240 | 240/240 | 15/30 | 30/30 |
| 128 | 188/240 | 235/240 | 3/30 | 25/30 |
| 512, separate stress | 16/40 | 35/40 | 0/5 | 0/5 |

The table excludes easy all-DEFER frozen snapshots. Each job has eight selected decisions, not every task in its archive. Custom and ordinary grouping have identical answers, so these denominators are for one policy, not doubled evidence. HSA meets the declared accuracy/macro-recall/whole-job working points at 8/32; the 128 whole-job target and 512 stress points remain unmet. The dense parents were already weaker under the source training recipe. [CAP01-R, §§2–3]

The five HSA errors at 128 are the same parent 8802/task 124 false-READY defect repeated across scenarios. The five stress failures repeat parent 8801/task 386. Full resident models make the same errors, so these are not missing-evidence failures introduced by streaming. A different 512 sensitivity world scored 16/16 at both tile sizes; this prevents claiming a universal monotone failure threshold at 512. [CAP01-R, §5]

## 9.6 Lifecycle, numerical agreement and cost

All 488 cases completed. All 3,904 repeated decisions matched full reference; 4,078,784 block/logit comparisons had zero tolerance violations. All 244 policy pairs agreed. There were 152 partial-attention pauses and 76 explicitly rejected attempts to reuse old-snapshot state after a revision. All revised cases restarted with new binding. Engineering passed 29 cases; the study reports independent recount of all 488 files, 40 bit-exact fresh-process final replays and 14 exact partial resumes. [CAP01-R, §6]

Capacity costs passes and storage. At 512 tasks, source plus embedding/two-layer arrays used 1,102,816 bytes, while recorded process RSS peaked at 383,250,432 bytes including full-reference/framework work. The cap excludes the archive, graph, model, accumulators, allocator workspaces and OS caching; ingestion itself is not a 32-row-total-memory operation. The 17,936-byte named tensor observation is a partial accounting point, not total memory. [CAP01-R, §7]

Representative case timings are single observations, not a repeated speed benchmark. At 128 tasks the report records 0.5097 seconds for dense versus 0.0821 for HSA; at 512, 6.4958 versus 0.1558, with different allowed graphs. These illustrate paid capacity and reduced connections in this executor, not an overall equal-quality efficiency ratio. Main cores totaled 211.841 seconds, distinct from complete study cost. [CAP01-R, §7]

**Conclusion:** Expanded executable input reach is demonstrated; unique custom grouping superiority and general new reasoning are not. Larger-layout interpretation remained the bounded next question. [CAP01-R, §9]

# 10. CAP02 — Preparation, retention and bounded closeout

## 10.1 Question and fixed recipe

The owner accepted one final preparation check, with an explicit preference not to linger after a working concept was established. CAP02 therefore asks whether a modest multi-size continuation can improve use of larger evidence while retaining the eight-task rule. It is not another search over architectures, thresholds or training budgets. [INTENT; CAP02-P; CAP02-R, §8]

Each of six original dense/HSA parents has U (untouched), S (96 additional eight-task updates) and M (96 updates cycling 8/32/128 tasks). Each update uses four worlds and supervises eight selected decisions per world: 32 labels/update, 3,072 per continuation. Corresponding eight-task batches match. Fresh AdamW uses learning rate 0.0005, weight decay 0.01, betas 0.9/0.999, epsilon 1e-8 and clipping 1.0. All parameters can change. Checkpoints are saved at 0/24/48/72/96, with only step 96 evaluated. [CAP02-R, §1]

This creates 12 trained continuations and 18 total endpoints. Main applications are exactly 1,152, with three disposable preflight updates. No random-initialized refits, early stopping, endpoint selection or extra tuning occurred. Mixed-size training uses more source information and computation; equal updates and labels are not equal FLOPs, time or training memory. Training itself is resident, not limited to the 32-record inference tile. [CAP02-R, opening and §1]

## 10.2 Fresh tests

The 130-world panel includes 32 nonfrozen and eight frozen worlds at each of 8/32/128 tasks, plus eight nonfrozen and two frozen worlds for independent 512-task stress. Worlds are common across parents and branches. Selected jobs contain eight random targets; all-task outputs are also retained to expose errors outside those targets. Exact overlap checks against training and 9,952 retained SH01 fingerprints found none. [CAP02-R, §2]

Each primary reader/arm/size has 768 selected observations and 96 jobs. The 512 stress has 192 observations and 24 jobs. These include repeated models on common worlds; they are not 768 or 192 independent random layouts. The rule still concerns immediate supplied prerequisites, not novel transitive reasoning. [CAP02-R, §2]

## 10.3 HSA result and retention

| Tasks | Untouched U | Small-only S | Mixed M | Whole jobs U to M |
|---|---|---|---|---|
| 8 | 767/768 | 768/768 | 768/768 | 95/96 to 96/96 |
| 32 | 762/768 | 767/768 | 767/768 | 91/96 to 95/96 |
| 128 | 749/768 | 730/768 | 766/768 | 80/96 to 94/96 |
| 512, separate stress | 175/192 | 177/192 | 189/192 | 11/24 to 21/24 |

At 128, M reaches 99.740% selected accuracy and 97.917% whole-job accuracy. At eight tasks every M parent has perfect selected/all-task answers and jobs. M meets the prospective descriptive working points at 8/32/128; 512 has 98.438% selected accuracy but 87.5% whole-job accuracy, below its 90% job point. It remains a recorded stress limitation, not a prompt for further tuning. [CAP02-R, §3]

| Parent at 128 tasks | U | S | M |
|---|---|---|---|
| 8801 | 242/256 | 220/256 | 256/256 |
| 8802 | 252/256 | 254/256 | 255/256 |
| 8804 | 255/256 | 256/256 | 255/256 |

Mixed preparation improves on U in two parents and ties one. It beats S in two but is one answer worse in the third. This is a strong pooled bounded result, not a uniformly positive change at every seed or position. [CAP02-R, §3]

## 10.4 Collateral errors and dense comparison

At 128, M fixes all 19 U errors but introduces two new errors: one false BLOCKED on an already complete task and one false COMPLETE on a blocked task. At 32 one pre-existing false COMPLETE remains. At 512 it repairs 14/17 old selected errors, introduces no new selected errors and retains three false READY outputs. All error evidence includes exact sources, prerequisite progress and logits. [CAP02-R, §4]

All-task secondary checks support improvement without substituting denominators: HSA at 128 moves from 11,962/12,288 to 12,275/12,288; at 512 from 11,178/12,288 to 12,083/12,288. These are not the selected-job counts above. [CAP02-R, §4]

Dense M scores 692/768 at eight tasks, 654/768 at 32, 624/768 at 128 and 136/192 at 512. It improves some larger-layout scores but remains weaker under this recipe. Because the inherited dense model was already less competent, these comparisons do not establish an optimally prepared dense ceiling. [CAP02-R, §5]

## 10.5 Post-learning stream compatibility and closeout

All six M endpoints were checked with unchanged CAP01 32-record streaming on the first nonfrozen 32- and 128-task worlds: 12 declared checks. Across 89,952 stage/logit comparisons there were no tolerance violations or class differences. This is a subset compatibility test after learning, not streaming evaluation of the entire 130-world panel or proof of bounded-memory training. [CAP02-R, §6]

All 18 endpoints were evaluated on 130 worlds: 2,340 endpoint/world records, 18,720 selected observations and 213,120 all-task observations. The study's independent recount found no discrepancy; all 60 checkpoint hashes/parent links matched; a fresh process reproduced all 18 endpoint files bit-exactly. Preflight passed 12 named checks. A pre-lock syntax error was preserved and repaired before model work; no main interruption occurred. [CAP02-R, §7]

Tracked command cores totaled 22.073 seconds, not complete research time. Peak process RSS was 399,749,120 bytes and included resident training/evaluation and framework allocations. No per-method speed or energy study was conducted. [CAP02-R, §7]

**Conclusion:** Broader preparation can improve use of the expanded evidence on this known task while preserving the tested small skill. The component is now parked for integration, not adopted as an NSS serving model or held for endless perfection. [CAP02-R, §8]

# 11. Cross-study interpretation and failure ledger

## 11.1 Four meanings of “works”

| Meaning | What is supported | What must not be inferred |
|---|---|---|
| Functional architecture | Exact record/graph interfaces, lifecycle checks and cross-segment arithmetic execute. | An entire autonomous companion or day/night service exists. |
| Learned competence | HSA learned the specified rule better than the retained dense recipe; CAP02 broadened preparation. | Unknown policies, semantic exceptions or general reasoning were learned. |
| Capacity | Exact source-dependent computations exceeding the active tile can finish through multiple passes. | All evidence is compressed into the tile or total memory is capped at the tile size. |
| Efficiency | Several implementations reduce measured work/time in specific CPU workloads. | Universal latency, energy, total-memory or unique custom-selector superiority. |

These distinctions allow the measured success to remain meaningful without extending it beyond the task and implementation. [SH01-R, §9; SC02-R, §12; CAP01-R, §9; CAP02-R, §8]

## 11.2 Retained failures and why they matter

| Study / issue | Observed consequence | Disposition |
|---|---|---|
| SH01 snapshot aliasing | A corrupt test copy contaminated shared data. | Fixed pre-lock; failed source and traceback retained. |
| SH01 interrupted HSA fit | 8803 HSA final absent; some initial losses/resource totals unavailable. | No replacement or best-checkpoint substitution; update count remains an interval. |
| SH01 sparse runtime | Fewer attention cells but slower reader. | Motivated packed execution, not denial of HSA learning benefit. |
| SH02 historical bitwise mismatch | Strict driver exit 1 despite admitted tolerance and unchanged classes. | Unresolved cause; failure preserved separately from current replay success. |
| SC01 grouping/invalidation overhead | Some extra reader calls and a slower resumption case. | Strong cache retained; no universal policy adoption. |
| SC01 precision-selection bug | Float32 outputs restored in JSON judged as float64. | Comparator fixed before main lock, envelope unchanged. |
| SC02 intermediate cache | Less neural work but slower in every timing cell. | Experimental path retained; not recommended by default. |
| SC02 timing comparison hazard | Same historical code ran much faster in the later session. | Only contemporaneous C/S/F/P/I differences support optimization claims. |
| CAP01 interpretation failures | Some false READY answers on larger layouts, also in full reference. | Capacity preserved; learner weakness not mistaken for missing evidence. |
| CAP01 revised-source resume | Old numerical checkpoint rejected after source changes. | Correct conservative restart, not migration qualification. |
| CAP02 collateral errors/stress | Two new 128-task selected errors; three residual 512 false READY outputs. | Net improvement retained alongside remaining mistakes; no extra tuning. |

Caller interruptions in SH02, SC01 and SC02 were handled by separately documented completion of missing inference/timing work. They do not imply all original terminal resource records survived. CAP01's attempted unsupported interactive invocation failed before work; CAP02's parse error also preceded model execution. Each original incident remains in its own archive. [Original reports, failure/operational sections]

## 11.3 Verification is not one interchangeable “pass”

| Study | Engineering report | Numerical / behavior-preservation report | Replay / recount report |
|---|---|---|---|
| SH01 | 664 assertions; seeded lifecycle and fault cases | Native/reference attention and gradients; trained subset checked | 21 output files and 30 checkpoint hashes |
| SH02 | 92 cases | 623,800 engineering + 2,918,400 stage scalars within envelope; 9,984 decisions unchanged | Historical nine-file bitwise failure retained; new nine-file replay exact |
| SC01 | 34 cases + 12 pipeline episodes | 106,416 score scalars, 26,604 decisions; no violations | 324 recounts, 54 selected replays, 36 resumes |
| SC02 | 34 checks | 246,480 score scalars, 61,620 decisions; no violations | 720 recounts, 36 selected replays, 24 resumes |
| CAP01 | 29 cases | 4,078,784 stage/logit scalars, 3,904 decisions; no violations | 488 recounts, 40 selected replays, 14 partial resumes |
| CAP02 | 12 checks | 89,952 streaming comparison scalars on 12 checks | 2,340 endpoint/world recounts, 18 output-file replays, 60 checkpoint hashes |

The columns describe different units and coverage. Do not add assertion counts, output positions, worlds and repeated replays to manufacture a larger independent sample. These are historical study-reported internal checks. The current consolidation reran only archive/hash integrity checks, documented separately in section 14. [All six reports]

## 11.4 Conclusions that are not supported

No result establishes the most efficient general “AI language,” JSON token efficiency, 25,000-token adequacy, a million-token semantic memory, language-model summarization fidelity, autonomous choice of maintenance objectives, trustworthy self-diagnosis, privacy/security against hostile data, lossless identity migration or indefinite learning stability. The checksums detect accidental corruption, not an adversary replacing both data and digest. The synthetic receipts describe advisory outputs, not real external side effects. [SH01-R, §§2,9; SC01-R, §§2,9; SC02-R, §10; CAP01-R, §§6–9; CAP02-R, §8]

Neither an isolated high answer percentage nor a numerical mismatch should erase the complementary evidence. Harmless admitted arithmetic drift differs from wrong outputs; a new false COMPLETE remains visible even alongside a large aggregate improvement. Identity continuity itself was not measured by the four-class task. [SH02-R, §3; CAP02-R, §§3–4; INTENT]

# 12. Implications for NSS maintenance-token architecture

## 12.1 What transfers as an architectural principle

**Assessment, not a new test:** The demonstrated component supports a maintenance design in which exact records live outside the active workspace, selected evidence is organized through a shared hierarchy, and unfinished computation can be checkpointed rather than discarded at a packet boundary. Maintenance outputs can be tied to source versions and rejected when their premises change. These functions are relevant to task handoffs, consolidation bookkeeping, candidate-evaluation records and repair support. [SC01-A; SC02-A; CAP01-A]

The working division is therefore:

```text
exact versioned evidence + explicit job/receipt records
                    |
       segmented work selection / retrieval
                    |
   dense or three-level HSA learned interpretation
                    |
  bounded execution, with exact multi-pass carry when needed
                    |
        source-bound advisory result + continuation record
```

This is a conceptual summary of the implemented functions, not a newly delivered single production runtime. SH02, SC02 and CAP01 are versioned components with different execution paths. Their source compatibility is useful, but it does not make every optional optimization and every later candidate checkpoint automatically validated in every combination. [SH02-A; SC02-A; CAP01-A; CAP02-R, §6]

## 12.2 The bridge from typed records to tokens

| Desired maintenance use | Tested precursor | Remaining gap |
|---|---|---|
| Explicit JSON maintenance messages | Exact serialized records, source IDs, result and resume envelopes | A language-capable model that writes and reads them correctly |
| Bounded active maintenance context | SC packet budgets and CAP query/key tiles | Actual tokenizer counts, positional/context semantics and language-task adequacy |
| Large exact archive with selective access | RAM-backed records and CAP file-backed intermediates | Real document retrieval, disk/network costs, semantic relevance and long-lived archive management |
| Short handoffs that preserve needed information | Program-authored progress/receipt state and exact arithmetic checkpoints | Learned summary completeness, task reconstruction from text and correction of omitted obligations |
| Repair/consolidation support | Maintained evidence and simple learned dispositions | Useful generated curricula, actual repair selection and full acquisition/retention/adoption evaluation |
| Safe overnight continuation | Same-model/source restore and rejection of stale bindings | Task/identity continuity across changed serving weights; tested fallback or migration |
| DARP maintenance outputs | An input/context substrate and fixed-format advisory outputs | Actual within-segment diffusion/refinement, output commitment and quality/cost tests |

The matrix intentionally separates relevance from demonstrated implementation. No row permits calling an engineered record a language token or treating a software-written receipt as an autonomously generated maintenance plan. [SH01-R, §2; SC01-A; CAP01-A; CAP02-R, §§1,6,8]

## 12.3 JSON, tokens and numerical state should not be conflated

The conversation prefers JSON for explicit internal records and wants tokens used where helpful for maintenance rather than avoided on principle. The tests substantiate JSON's use as a checked serialization format in this prototype. They do not compare serialization formats with a tokenizer or show that JSON is universally the shortest/most efficient model representation. [INTENT; SH01-R, §2; CAP01-A]

The CAP01 envelope can contain binary-encoded numerical accumulators. That makes the checkpoint exact as a record but does not make the accumulators natural language or ordinary context tokens. Numerical state, tokenized notes and exact evidence references have different lifetimes and compatibility rules. Holding a model revision fixed is part of cache validity; nightly weight changes cannot silently reuse those learned activations. [CAP01-A; SC02-R, §2]

## 12.4 The 25,000-token idea remains a testable budget hypothesis

The owner proposed approximately 25,000 maintenance tokens as a plausible starting scale rather than assuming a million-token active context. The active-at-once budget and cumulative overnight traffic were distinguished in the discussion but never implemented as a language experiment. No exact tokenizer, token allocation, maintenance workload distribution or generation policy has been fixed by these studies. [INTENT; SH01-R, §2; CAP02-R, §8]

A later evaluation would have to report active language tokens, cumulative reads and generated tokens, repeated refinement work, total memory, storage and elapsed cost separately. That is an implication for eventual integration, not a newly authorized protocol. Fitting an active tile does not bound all resource use; CAP01 is direct evidence of why external arrays, graph state, ingestion and OS caches must remain visible. [CAP01-R, §7]

## 12.5 Expanded capacity versus expanded reasoning

CAP01 demonstrates an execution constraint being lifted. CAP02 shows a prepared reader using the wider evidence more reliably on the same known rule. Together they support the narrower maintenance hypothesis: a small active workspace need not prevent a model from consulting and computing over a larger information collection. [CAP01-R, §§4,9; CAP02-R, §§3,8]

They do not establish that the model can understand natural-language exceptions, discover cross-record relationships, perform an unfamiliar multistep repair, or safely compress every necessary fact into a summary. Increasing world size changes the source/dependency population, not the number of logical prerequisite hops. Expanded input reach is valuable on its own, but cannot substitute for a task and learning interface suited to those harder maintenance questions. [CAP01-R, §§1,3,9; CAP02-R, §2]

## 12.6 Stable-day / learning-night compatibility

**Integration implication:** The tested same-version caches and checkpoints are naturally useful while serving weights are stable. They can record daytime obligations and manage an overnight job's exact work state. But these experiments do not execute a complete night in which a model learns, repairs, is evaluated, is published and resumes real unfinished tasks the next morning. CAP02 teaches the narrow rule on broader layouts, then checks selected streaming compatibility; that is not the full lifecycle. [SC02-A; CAP01-A; CAP02-R, §§1,6,8; INTENT]

The older accepted checkpoint and exact records remain conceptually different fallbacks. Neither retaining a numerical checkpoint nor writing JSON proves a changed model can continue the user's work. That boundary remains for later system integration, without reinstating tri-core or demanding that harmless expression/numerical changes be eliminated. [INTENT]

# 13. Consolidated conclusions and handoff decision

## 13.1 What should be retained

Retain the explicit task/region/global graph, the separated record/topology/plan/backend interfaces, the packed HSA execution, exact dependency-aware segmented work and the multi-pass attention accumulator. Retain incremental record publication and plan/signature reuse as measured engineering improvements. Keep ordinary caching and ordinary streaming as first-class comparators rather than obstacles to an architectural narrative. [SH02-R, §7; SC02-R, §12; CAP01-R, §9]

Retain the original six complete-pair model parents and CAP02's fixed mixed-preparation candidates. Preserve the incomplete SH01 8803 HSA checkpoint and all unwanted endpoints/errors. The mixed-prepared weights are research candidates, not a newly adopted NSS serving model. [SH01-R, §8; CAP02-R, §8]

## 13.2 What should remain optional or open

The tested first-layer neural cache should be off by default on this evidence. Scheduled grouping can be useful, but conventional request order can also win. No automatic workload selector was validated, and no per-row collection of favorable choices should be described as an already working adaptive policy. [SC02-R, §§5–8,12]

Open integration limits include a stronger dense baseline, layout-sensitive residual errors, recursive/depth alternatives, cold archive costs, total-memory and energy accounting, model-generated maintenance records, language-token budgets and complete maintenance/adoption cycles. These are recorded boundaries, not an instruction to reopen every topic before moving on. [SH02-R, §§2,7; CAP01-R, §9; CAP02-R, §8]

## 13.3 Overall assessment

**HSA plus segmented context is a working bounded maintenance component.** The hierarchy has a positive learning result in this task; lifecycle execution preserves source-bound work; multi-pass calculation demonstrably exceeds a resident active-packet constraint; broader preparation improves larger-layout use while retaining the tested small skill. [SH01-R, §4; SC01-R, §3; CAP01-R, §4; CAP02-R, §3]

**Unique superiority of the custom segmented policy is not established.** Much of the efficiency comes from conventional caching/incremental engineering, and ordinary multi-pass computation matches the capacity/answer results. This does not negate the underlying mechanism; it locates the contribution accurately. [SC02-R, §§5–8; CAP01-R, §§3–4,9]

**The maintenance-token architecture remains a next-stage application, not a completed result.** These components provide a credible base for that application, but typed inputs, program-authored JSON and exact numerical state do not qualify language generation, semantic maintenance or a 25,000-token night. [CAP01-R, §9; CAP02-R, §8]

The appropriate status is **PARKED FOR INTEGRATION**. Continue to another theoretical component, with this archive as the preserved reference. DARP is primarily output generation and can be investigated for maintenance outputs next, but no DARP training, experiment or full-system construction is authorized by the consolidation. [CAP02-R, §8; INTENT]

# 14. Archive, verification and reproduction guide

## 14.1 What the consolidated archive contains

`original_archives/` contains exactly the six complete original execution ZIPs, unchanged. Each retains its prospective protocol, source/test implementations, fixtures, checkpoints, raw outcomes, failures, audits and original manifest. Keeping them intact preserves original hashes and avoids silently synthesizing a new experimental codebase.

`sources/<STUDY>/` supplies convenient exact copies of each report, protocol, README, review note, original manifest, available architecture and source/fixture locks, plus the original delivery receipt. `sources/context/` contains the original VargBot context concept and the clearly labeled current conversation-direction record. Missing standalone architecture documents for SH01 and CAP02 are not invented; their protocol/report and inherited architecture define their scope.

`indexes/` contains the source catalog, per-study full member inventories, a test/implementation entry-point catalog, model/checkpoint lineage index and a machine-readable question/results summary. These indexes point back to original members; they do not claim the tests were rerun during consolidation.

`verification/INPUT_AUDIT.json` records this consolidation's fresh byte audit. `MANIFEST.json` covers the consolidated payloads, and the external delivery receipt identifies the final downloadable files. `tools/verify_consolidation.py` verifies integrity without loading model files. `tools/extract_study.py` extracts one chosen original archive to a separate working directory with path checks.

The compact review ZIP, when supplied, omits the original execution ZIP payloads but includes the same report and documentary/index layer. It is convenient for reading and review; the full archive is the self-contained evidence delivery.

## 14.2 Fresh byte-integrity audit

All six original archive hashes and sizes matched their original delivery receipts. ZIP CRC checks passed. Every declared member's size and SHA-256 matched its original manifest, with no missing or unlisted regular payloads. The six standalone reports, and all four available standalone architecture files, match their original archive members byte-for-byte. [verification/INPUT_AUDIT.json]

| Original study ZIP | Original ZIP bytes | Manifest payloads checked |
|---|---:|---:|
| SH01 | 15,700,634 | 140 |
| SH02 | 1,352,829 | 87 |
| SC01 | 3,494,844 | 522 |
| SC02 | 7,176,459 | 906 |
| CAP01 | 3,125,818 | 652 |
| CAP02 | 20,326,303 | 175 |
| **Total** | **51,176,887** | **2,482** |

This fresh verification is an archive-integrity result. It does not turn the original reported numerical checks, model evaluations or replay claims into new scientific replication. The original SH01 missing final/loss history and SH02 archival bitwise discrepancy remain unresolved historical limitations.

## 14.3 Where the actual tests are

| Study | Main source / test entry points inside its original root |
|---|---|
| SH01 | `source/common.py`, `source/store.py`, `source/preflight.py`; original protocol, fixtures, predictions and failure examples |
| SH02 | `nss_hsa/`, `tests/validate.py`, `scripts/regression.py`, `scripts/benchmark.py`, `scripts/post_audit.py` |
| SC01 | `source/sc01.py`, `tests/preflight.py`, `tests/pipeline_preflight.py`, `scripts/run.py`, `scripts/audit.py` |
| SC02 | `source/sc02.py`, `tests/preflight.py`, `scripts/runner.py`, `scripts/main.py`, `scripts/benchmark.py`, `postrun/audit.py` |
| CAP01 | `source/cap01.py`, `tests/preflight.py`, `scripts/run.py`, `scripts/audit.py`, `CASES.json` |
| CAP02 | `source/cap02.py`, `audit/recount_and_replay.py`, original schedule/fixtures, retained parents and continuation checkpoints |

The fuller `indexes/TEST_CATALOG.md` records test and runner locations, declared coverage and reproduction cautions. An inventory of files is not a statement that every historical script is a general-purpose CLI: operational continuation scripts refer to specific interrupted runs and must not be used as fresh experiments.

## 14.4 Safe use and future continuity

Verify first; preserve the delivery ZIP as immutable evidence; unpack one study into a separate directory for any reproduction. Read its original README and protocol. Some scripts write results or assume an existing source layout. Do not execute training commands, regenerate locks or overwrite historical outputs as part of merely reviewing this consolidation. The recorded studies used a CPU Python/NumPy/PyTorch environment; where specified, the receipts identify Python 3.13.5, NumPy 2.3.5 and PyTorch 2.10.0+cpu. No current package-version research was performed here. [Study READMEs]

The six complete archives are provided, so their retained source and model payloads need not be reconstructed from the conversation. Conversely, full successful intermediate arrays were not retained for every CAP01 case; its source, fixtures and checkpoints are supplied for separately authorized recomputation. The source reports explain those retention boundaries. [CAP01-R, §8]

**Handoff instruction:** Treat this record as completed bounded research. Preserve the distinction between capability, efficiency, numerical equivalence and evidence integrity. Keep the component parked unless a new integration or replication question is explicitly authorized. Move to the next theoretical idea without retroactively converting these studies into a full maintenance-token or whole-NSS qualification.
