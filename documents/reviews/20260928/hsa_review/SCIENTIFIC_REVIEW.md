# Scientific review: HSA + Segmented Context consolidation

**Scope:** Independent scientific and architecture assessment of `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.md`. The consolidation is a record of six component studies, not a new experiment or independent replication. This note comments on its scientific meaning and fit for NSS maintenance architecture. It does not adopt an architecture, supersede RECOVER01, or dispatch work.

## Plain-language account

The studies built a small classifier that reads hand-structured maintenance records and labels each selected task BLOCKED, READY, COMPLETE or DEFER. A program supplies the records, task identities, prerequisite links, selection and exact graph; the neural reader learns the label rule. Later implementations could pause and resume the calculation, process inputs in tiles smaller than the full attention closure, and prepare on mixed-size examples.

The clearest capability result is computational: CAP01 completes an exact attention calculation when the active tile is only 32 record positions but the needed closure can span 69–755 positions. It retains the rest of the inputs and partial calculation in external arrays and resumes the same joint softmax. Ordinary multi-pass grouping obtains the same answers, so this demonstrates useful bounded-active-work execution, not exclusive power from HSA segmentation. CAP02 then improves the fixed known task on larger layouts: mixed-prepared HSA reaches 766/768 selected answers at 128 tasks and retains 768/768 at eight tasks. It still makes errors at 128 and misses its 512-task whole-job working point. [Consolidation §§1, 9–10]

## What is genuinely established

SH01 provides positive, bounded evidence for HSA as an inductive bias in this task and recipe. Across three complete paired fits, HSA scored 6,133/6,144 decisions versus 5,553/6,144 for dense attention, with one versus ten false COMPLETE outputs. The task, paired initial weights, training recipe and confirmation panels make that a meaningful comparison. It is not a general result about dense models: one HSA parent fit was incomplete, only three pairs contribute, and the dense learner was not an exhaustively tuned or same-graph trained comparator. [Consolidation §§5.2–5.5]

The strongest architecture idea is the surrounding evidence-and-execution discipline: keep exact, versioned records outside the active neural packet; bind work and cached results to their source/model versions; and preserve unfinished numerical computation across pauses. These are practical maintenance-system primitives. CAP01’s active-tile bound is not a bound on total memory: the program still retains/rereads source, graph, embeddings, layer arrays and online-softmax accumulators outside the tile. [Consolidation §§3.3–3.4, 9]

## Main limits

1. **The “reasoning” task is engineered and closed-world.** The program supplies the task fields, prerequisite graph, region/global anchors and freeze flag. The target is a known rule over immediate supplied prerequisites. The model learns to interpret engineered numerical features; it does not discover dependencies, retrieve relevant evidence from prose, resolve unknown exceptions, or demonstrate deeper transitive reasoning. The deterministic scorer can solve the rule exactly and is a useful ceiling/control. [Consolidation §§3.1–3.3, 11.4]

2. **HSA attribution is encouraging but underdetermined.** HSA beats dense on the narrow SH01 outcome, but three complete seed pairs do not establish broad generalization. Dense’s weaker result may reflect this recipe. SH02’s masked-dense implementation is a numerical reference, not a separately trained competitor. The data support “this supplied hierarchy helped these fits,” not “hierarchy is necessary,” “three levels are optimal,” or “dense attention cannot learn this.” [Consolidation §§2.2, 3.2, 5, 6]

3. **Segmentation and capacity are not unique HSA advantages.** SC01/SC02 show most savings from ordinary caching, incremental publication and plan reuse; the neural intermediate cache was slower in every timing cell. In CAP01, ordinary streaming and HSA grouping preserve the same outputs. The custom policy may help some workloads, but unique accuracy or cost superiority is not demonstrated. [Consolidation §§7–9]

4. **Input reach is not language-memory competence.** The 37 engineered channels, JSON receipts and numerical checkpoints are not tokenizer-produced maintenance language or model-written summaries. The studies do not measure a 25,000-token active or cumulative night budget, semantic retrieval from real records, generated handoffs, identity continuity, autonomous repair, or a full day/night learning cycle. Reported process RSS and named tensor sizes are not total-system memory, energy, or deployment costs. [Consolidation §§1.4, 2.1, 3.3, 12]

5. **Preparation results are bounded, not a durable-learning result.** CAP02 adds a fixed 96 updates and tests selected jobs on shared synthetic worlds. It improves HSA on 128-task cases but introduces two new selected errors there; 512-task stress retains three false READY outputs and misses the whole-job point. Reused worlds and checkpoints are not independent replications. The consolidation’s archive verification confirms preserved bytes, not its historical model outputs through new execution. [Consolidation §§10–11, 14]

## Relationship to the other current NSS questions

SURFACE01 and RECOVER01 concern a separate recurrent checklist learner. SURFACE01 stopped before its correction comparison because parent 4103 violated the zero-false-DONE baseline gate; it exposed a fixed-weight idempotent-event semantic failure. The current RECOVER01 proposal preserves that historical stop while proposing U/L/R/LR acquisition-and-replay branches on the four retained parents. It remains planning only. Neither result measures HSA, and CAP02’s HSA continuation does not resolve RECOVER01’s GRU state/update-retention question. [`RESEARCH_STATE.md`, “Current position”; `Research/NSS_NBR02_RECOVER01_Proposal_v0.1.md`]

The HSA consolidation recommends moving to another theoretical component and mentions DARP as a possible maintenance-output direction. That is source-recorded direction, not authorization or adoption of a replacement architecture. DARP should remain optional and, if considered, be compared with direct structured generation; it does not follow from the HSA classifier results.

## Ranked next questions

1. **Can this evidence/execution substrate support real maintenance language?** The smallest bridge is tokenizer-counted, source-bound maintenance records and a constrained handoff/summary task, while task selection, provenance and permissions remain deterministic. Score omissions, stale-source use and continuation, not fluent style alone. This tests the missing semantic interface without pretending CAP01 tiles are language tokens.

2. **What learned capability remains beyond supplied bookkeeping?** Use held-out task layouts and carefully varied evidence; compare the neural reader with the exact scorer and a competent, matched learned comparator. Include cases where record meaning or evidence is not reducible to prefilled dependency channels before claiming semantic reasoning. This would sharpen HSA’s contribution without another broad architecture search.

3. **What does the bounded execution cost end to end?** Compare resident execution, ordinary exact streaming and HSA grouping on the same outputs while measuring peak process and system memory, temporary storage, cold-start, preparation and elapsed time. This is needed before turning “32 active positions” into a resource or deployment claim.

4. **Does DARP add value as an output mechanism?** If pursued after the language bridge, compare DARP-generated maintenance artifacts with direct constrained structured output on the same evidence, correctness checks and token/compute budget. Keep this distinct from the reader and from RECOVER01’s changed-weight recovery question.
