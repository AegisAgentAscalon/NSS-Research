# ContextRetrieval001 — implementation decisions / v0.4.11

## Scope and owners
Provide ordinary software context assembly for one current catalogue-managed stage.
This is not native HSA/MSA, language-model tokenization, latent memory, semantic search,
new Core/overlay training, a serving permit or authenticated permissions.

- `Generations` remains the one task/ticket/current-generation owner.
- `CatalogController.read` is the public live stage/artifact/qualification gate.
- `ExperienceArchive` owns review, revision, permission, revocation and evidence bytes.
- `ContextService` owns NO persistent store. It returns immutable-by-value proposals
  and revalidates them before use. A copied packet is not a permission token.
- `EvidenceReader` caches only within one call. Raw archive evidence uses the new
  `read_evidence_for_use` public method, never administrative `inspect_source`.
- Existing relative-root, exact-hash TASK fixture files remain locally admitted task
  sources. They are not globally licensed knowledge. Their permission domain is
  separate from the archive; relabelling archive content as a task fixture is outside
  the trusted-local threat model, not an implemented revocation bypass guarantee.

## Typed boundaries
`context_request.schema.json` pins the entire generation ticket, caller, TaskRecord
hash, task-state identity, optional archive-owner binding, explicit selectors and
resource budget. Identifiers are unique and canonically ordered. Exact source
selectors may request a task field or an explicit UTF-8 byte range from reviewed
experience evidence.

`context_packet.schema.json` binds the request, profile ECID, task identity, payload,
byte accounting, source metadata and omission reasons. `build`, `consume`, and
`rehydrate` return `{status, data, detail, recovery}`. Only SUCCESS has data. A current
read never authorizes training, generation publication or an external effect.

## Budget definition
`max_context_bytes` measures ALL of `encoded(payload)` (the inherited canonical JSON
encoder, sorted keys and ASCII-escaped text, then UTF-8), including the task spine,
provenance refs, selected text and evidence. It is NOT token count, native context
length, VRAM, total JSON-envelope bytes, total I/O, latency or energy. Hard cap 128 KiB.

`max_evidence_bytes` caps material admitted by this assembler: distinct local file
payloads, each permission-checked shortlisted experience view and distinct retrieved
archive source payloads (2 MiB hard cap). Rejected oversized items and owner-internal
lineage/qualification reads are not counted as accepted evidence bytes. Owner reads
have their own bounds; this is not a process-memory or global-I/O limit. Requests have
at most 32 experience candidates and 32 slices. Integrity rechecks may reread bytes.

## Selection and precedence
Always retain goal, original request, complete current stage, constraints,
clarifications, unresolved questions and action receipts. No automatic summary.
Stage-required facts and explicitly required selectors are mandatory. Exact missing
value/unit fields may be hydrated in the packet, with `rehydrated_fields`; the original
TaskRecord is NOT silently changed. An absent fact, unknown required source field,
contradiction, or unresolved blocking question returns a typed inability.

Optional record IDs are deliberate selectors. Experience candidates are an explicit
shortlist with declared priority and optional literal casefolded term matching.
Required experiences bypass lexical filtering. Remaining optional experiences sort
by declared priority, matched-term count and stable ID. This is deterministic greedy
selection, NOT proven minimal context, optimized knapsack, semantic relevance, truth
checking or learned routing. Required content is never displaced by optional content.

Retrieved statements retain author, uncertainty, source class, review and permission;
they are marked reviewed interpretations, not controlling instructions. Source slices
are marked source data, not instructions. This typing does not prove a future neural
model immune to prompt injection or able to detect semantic contradictions.

## Overflow, rehydration, and missing information
Required content too large -> BUDGET_EXHAUSTED with the measured failing required-prefix
size (not a complete remaining-task estimate) and explicit
options to increase the byte budget within the cap or decompose at an authorized
stage boundary. Optional content that does not fit -> an omission record. No partial
success for failed required content. A source reference is not a substitute for
required inline information. `rehydrate` expands only a reference already selected in
a currently valid packet; exact slices must align with UTF-8 characters and fit the
original packet/evidence budgets. No inferred units, summaries, silent truncation or
unbounded retry loop.

General TaskRecord amendments (new clarification/correction during a running stage)
remain deferred: they require owner-controlled CAS, revision history and cache
invalidation. This read-only pass returns NEEDS_CLARIFICATION; it does not create a
second task head or write a patch. Existing finish/move/cancel paths remain available.

## Freshness and failure
Before output, selected experience refs are rechecked together through the archive,
local files are rechecked, then the task owner is reread. `consume` repeats assembly
and demands the same packet plus the caller's expected digest; hashing alone is not
acceptance. A previous stage/revision/epoch is rejected. Optional eligibility changes
may yield a different new packet but cannot silently validate the old packet.

Checks are point-in-time in the existing single-cooperating-worker model. There is
NO distributed lease, global multi-store transaction, hostile-local-user protection,
authenticated caller, or recall of already exported text. A process interruption
cannot partially publish context state because this service has no publication.

## Forbidden edges
Context -> direct SQL in task/archive stores; Context -> task record mutation;
Context -> action execution; Context -> training dataset admission; Context -> model
optimizer; archived inspection -> retrieval permission; byte limit -> token claim;
source text -> runtime authorization. No new package dependency or network path.

## Compatibility
New context ABI `MegaMindAlpha.ContextRetrieval001`, schema 1, fixed selection policy.
Existing task/archive storage schemas and commands remain unchanged. The archive's
source-read method is additive; the old batch interface delegates its existing use
check to a shared helper. Existing stage sources delegate to a shared bounded reader.
