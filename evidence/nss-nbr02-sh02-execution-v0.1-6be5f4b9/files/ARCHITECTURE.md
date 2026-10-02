# NSS hierarchical maintenance reader — clean reference v0.1

**Component:** NSS NBR02 SH02. **Purpose:** a clean executable hierarchical-attention component for later NSS maintenance architecture experiments. It is not an overnight learner, an autonomous repair agent, a language model, or the old tri-core design.

## 1. The design in one paragraph

Exact typed maintenance evidence enters a feature adapter. A separate, immutable topology description states which task records and prerequisite records may interact. A compiler groups queries with identical allowed neighborhoods and prepares a bounded reusable execution plan. The reader projects the evidence into learned representations, applies two hierarchical attention/FFN blocks, and produces an advisory disposition per task. Graph construction, numerical attention, task interpretation, and upstream record ownership are separate responsibilities.

The cleanup preserves SH01's graph, feature encoding and all learned weights. It changes execution and software boundaries, not what evidence the model receives or the learned task.

## 2. Explicit three-level hierarchy

| Level | Contents | Outgoing attention: keys available to that query |
|---|---|---|
| Task records | Four positions per task: query/identity, progress, receipt, constraint | Its four local records; all four records of each declared prerequisite; query positions of tasks in its own region; all regional anchors; the global anchor. |
| Regional anchors | Mean address metadata for a group of tasks | Query positions in that region, that regional anchor, and the global anchor. |
| Global anchor | Global maintenance freeze flag | Regional anchors and the global anchor itself. |

Region width is ceil(sqrt(number of tasks)) for SH01-compatible inputs. The final region may be smaller. Region anchors are metadata, not natural-language summaries or ground-truth dispositions. Dependencies are supplied record metadata, not inferred by the model.

Every layer computes these queries simultaneously. There is no newly introduced serial bottom-up summarization pass followed by a top-down pass. Such a change would define a different model and would need separate learning evidence. All available keys for a query participate in ONE joint softmax; normalizing each level separately and averaging would not preserve SH01.

Multiple routes to the same key are deduplicated before computation. Cycles between distinct task dependencies are not rejected: SH01 supports them. Self-dependencies and duplicate entries within a dependency list are rejected by the topology API.

## 3. Software boundaries

| Module | Owns | Must not silently do |
|---|---|---|
| `records.py` | Validate and encode the 37-channel typed evidence; preserve exact SH01 features | Inject oracle labels, select convenient evidence, or call the model's predictions ground truth. |
| `hierarchy.py: Hierarchy` | Immutable dependency/region/scope specification and canonical graph | Inspect progress labels or learned activations to choose edges. |
| `hierarchy.py: compile_plan` | Group identical query neighborhoods, produce padded index/mask buckets, topology identity and accounting | Drop a valid edge to improve speed or hide padding/plan costs. |
| `hierarchy.py: PlanCache` | Bounded LRU of weight-independent topology plans | Cache neural K/V, weights, source facts, or past answers. |
| `attention.py` | Packed attention execution plus explicit numerical references | Treat a full dense competitor as an equivalent graph or claim sparse storage equals low total memory. |
| `reader.py` | SH01-compatible trainable projections, two blocks, output head | Update weights during inference or execute output dispositions. |
| `scripts/demo.py` | Load a trusted source-pinned inference checkpoint, validate a typed input, emit JSON | Publish an NSS candidate or execute an external action. |

The core package imports neither the old experiment runner nor its record store. SH01 code exists under `reference/` for verification only. The feature adapter intentionally remains narrow: it requires two prerequisites per task, matching the trained interface. The topology planner itself permits variable dependency counts, tested only as attention engineering cases.

## 4. Shared-neighborhood execution

SH01 gathered K and V separately for every query position. Four queries belonging to one task have the same allowed neighborhood. SH02 packs them together:

- Task bucket: `Q = [batch*tasks, heads, 4, head_dim]`; one gathered K/V neighborhood per task.
- Anchor bucket: region and global queries have `Q = [batch*(regions+1), heads, 1, head_dim]`; a smaller separately padded K/V layout.
- Each bucket uses PyTorch SDPA with its explicit allowed-key mask; the results are restored to original record order.

This removes repeated K/V gathering within each four-query task block. It is batched packed-neighborhood attention, not a new handwritten GPU kernel, not shared attention heads (GQA), and not approximate/top-k attention. Gather, layout-conversion and concatenation costs remain.

The packed path never constructs a global T×T score/mask array. The numerical reference deliberately does. Dispatcher shape tracing covers the sampled 135-position case; source inspection establishes the intended layout generally, not every native kernel's hidden memory allocation.

## 5. Plan identity, changes, and restart

A plan is identified by topology schema, ordered dependencies, task count, region width and scope. Its serialization includes a SHA-256 content checksum. Loading validates the checksum and rebuilds device tensors from authoritative topology rather than deserializing a device-specific cache. A checksum detects accidental corruption; it is NOT authentication against an attacker who can replace both payload and checksum.

A dependency, task ordering, region width or scope change creates a different plan. `assert_matches()` rejects explicit stale-plan reuse. The LRU capacity bounds retained plans and reports hits, misses and evictions. Scope prevents mixing different scopes in one batch; source permission and visibility checks remain the upstream record store's responsibility.

Evidence-only changes (progress, receipts, freeze) do not change the topology: reuse the plan, but recompile current evidence and recompute all neural representations. Weight revisions also do not invalidate this graph plan; they DO invalidate any future neural activation cache, which is deliberately absent here.

Materialized plan tensors are a trusted read-only object by contract, not magically immutable Python objects. `validate_tensors()` detects mutation at ingestion/restart/debug boundaries. `checked=True` validates the plan and finite inputs before a forward; steady-state timing uses a previously validated plan, with checked-entry costs reported separately. Code holding arbitrary mutable tensors remains responsible for not racing writes against inference.

## 6. Normal call sequence

```python
import torch
from nss_hsa import MaintenanceReader, PlanCache, prepare_worlds

# world: SH01 typed input; see examples/world.json
features, specs = prepare_worlds([world])
plan = PlanCache(capacity=8).get(specs)
plan.assert_matches(specs)
reader = MaintenanceReader()
reader.load_state_dict(checkpoint["model"])
reader.eval()
with torch.no_grad():
    logits = reader(features, plan, checked=True)
```

The weights loaded here are existing SH01 weights, not newly trained. Instantiating `MaintenanceReader()` alone creates random weights and is not a competent maintenance system. Reuse a cache instance across calls; the one-line example merely illustrates the API.

## 7. Scaling and boundaries

With a bounded number of prerequisites and the square-root regional layout, task queries see O(sqrt(N)) region/task anchors. The allowed-edge count is O(N sqrt(N)), NOT a linear-time guarantee. Unbounded dependency counts can approach quadratic cost. Recursive hierarchy, bounded learned routing, or a different regional connectivity rule would change the architecture and require separate evidence.

The current backend's small-input overhead and batch copies can outweigh sparse savings. A future backend may execute the SAME graph using dense masked kernels for small inputs or optimized sparse kernels for larger inputs. That requires a prospectively measured same-graph dispatch rule; SH02 does not implement an automatic crossover selector.

No 25,000-language-token budget is tested. The positions are fixed engineered records. No semantic segmentation, DARP, generated text, nighttime learning, candidate adoption, or unfinished neural-state migration is added in this component pass. The eventual criterion remains NSS maintenance value and full cost, not a sparse operation count.

## 8. Failure interpretation

A graph mismatch is a topology/compiler defect. A graph-equivalent numerical mismatch is an execution/verifier issue. A preserved wrong disposition is an existing learned-model error, not a refactor regression. A slower small shape is a cost result, not a functional failure. Replaying an old archive within tolerance but not bit-for-bit is recorded separately from class parity and within-environment reproducibility.

See REPORT.md and retained raw receipts for all observed outcomes, including a historical bitwise-replay mismatch and one cost-runner interruption.

## Implementation references

External guidance, not NSS result evidence:
- PyTorch 2.10 SDPA semantics: https://docs.pytorch.org/docs/2.10/generated/torch.nn.functional.scaled_dot_product_attention.html
- PyTorch 2.10 profiler scope and overhead: https://docs.pytorch.org/docs/2.10/profiler.html
- FlexAttention block-mask reuse is a future backend lead, not used here: https://pytorch.org/blog/flexattention/
