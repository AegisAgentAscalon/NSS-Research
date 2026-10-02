# CM-02 v0.6: accepted results and research implications

**CM-02 establishes bounded reference continuity, with no observed task advantage over an ordinary index. The next substantive question is learned task-progress state, rather than another encoding of a selected reference.** This is analysis of returned evidence, not a fresh experiment.

## What the results say

| Held-out interface | Correct | Interpretation |
| --- | ---: | --- |
| Original query, no retained selection (O) | 307/600, 51.17% | Deliberate information-removal ablation |
| Workspace (W) | 391/600, 65.17% | Retained selection helps relative to O |
| Ordinary maintained index (I) | 391/600, 65.17% | Same information and behavior as W |
| Public exact, pinned revision | 100/120, 83.33% | Stronger referenced-payload retrieval |
| Public exact, observed current revision | 105/120, 87.50% | A separately declared freshness contract |

The learned-read denominators repeat 120 held-out query occasions across five frozen readers. There are 20 held-out sequences in five families, not 600 independent cases. Exact controls run once per occasion; their denominators must not be inflated. W and I match across all 192 main routes and 960 paired model/query decisions. A positive W–O difference occurs in all five held-out families, but no new gain threshold was defined or fitted.

The pooled gain hides an important trade-off. At low query noise W/I score 202/300 versus O's 222/300; at high noise they score 189/300 versus 85/300. Event and policy conditions are mixed, so those pools do not identify a causal noise effect by themselves. Correctly retained references also do not ensure learned recall: at the unchanged-target 64-transition endpoint, W/I get 14/25 readouts while exact lookup gets all five unique answers.

## Three different failure mechanisms

1. **Freshness policy:** at revised-known F:16, the pinned policy intentionally abstains and loses five unique current answers (0/25 learned readouts). The predeclared current-revision exact control retrieves 5/5. This is an explicit retrieval-contract difference, not a neural-memory repair. At deletion F:48, UNKNOWN is correct; W/I get 25/25 versus O's 2/25.
2. **Unobserved intent:** ten held-out occasions have a publicly consistent reference that conflicts with hidden intent. W/I accept that wrong intended binding in all 50 repeated readouts, despite ten incidental content successes; exact lookup is wrong on all ten unique main-intent cases. Identical-public-input opposite-label diagnostics expose information that the system lacks. More memory or recurrence alone cannot make those labels identifiable.
3. **Learned reading:** even a valid canonical reference leaves numerical-reader errors. Exact payload retrieval already handles the referenced facts more accurately in this task. A future learned state should therefore be tested for task progress or computation beyond simply recalling an explicitly addressed fact.

## What the cost measurements support

W's peak resident Python object graph is 24 bytes smaller than I's in each held-out family; its mean observation is 32.75 bytes smaller. That satisfies the study's narrow representation criterion. It also incurs larger parsing-transient graphs, 306 more object-shell bytes allocated per family, 50 packet decodes and extra logical byte traffic. The two 56-byte strings coexist with a much larger journal/archive/index/reader inventory. These observations establish a small implementation trade-off, not an overall efficiency win or information compression. Instrumented timing, logical wire accounting and object inventories are not deployment memory or network measurements. Experimental inference-cache memory also remains charged separately.

## Evidence acceptance and limits

All 6,664 manifest files in the 6,665-member supplied ZIP matched their recorded hashes and sizes. `archive_integrity.json` identifies the exact bytes. `METRICS.md`, `metrics_summary.json` and their small retained-table script state which primary counts and cost summaries were freshly aggregated. `SCOPE_REVIEW.md` records the static source/protocol comparison and the limits of the execution claims. We did not import the scientific implementation, run its numerical scorer, load a model or reproduce the experiment.

The completed v0.6 main capture and replay are separate from interrupted earlier attempts. A successfully completed v0.5 fixture was carried after source identity and rescoring checks. All attempts count: 5,995 attempted forwards, including two unacknowledged interrupted calls, against the unchanged 6,000 cap. The shared clock through delivery QA is reported as 2,145.57 seconds. Earlier scorer failures, transport interruptions and incomplete resource receipts remain preserved; this is not a flawless first run. The archived fresh-process replay and independent scorer are internal verification evidence, not third-party replication. Q010 training-history and reconstructed-verifier limitations remain unchanged.

## Decision

Close the deterministic reference-continuity question at this scale. Preserve the ordinary index and public exact retrieval as strong baselines. Prioritize an isolated, genuinely learned task-state candidate only if its task requires state beyond the last selected reference and it is compared with exact streaming state plus costed replay. Treat pinned/current content selection and public intent cues as explicit policy/information choices. Keep all successor work proposed, with the concrete candidate and freeze requirements in `CANDIDATES.md`; no architecture replacement or local execution follows.
