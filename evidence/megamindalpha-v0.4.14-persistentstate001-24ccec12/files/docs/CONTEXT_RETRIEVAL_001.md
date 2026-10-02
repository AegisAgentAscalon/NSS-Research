# ContextRetrieval001 — public contract

This is the implemented external/software context baseline, not HSA/MSA or a complete
neural Context ABI. See `implementation_packets/contextretrieval001/DECISIONS.md`
and `ACCEPTANCE.md` for ownership, failure semantics, limits and concrete stimuli.

## Interfaces
- `ContextService(controller: CatalogController, archive: ExperienceArchive | None)`
- `build(ContextRequest) -> Outcome[ContextPacket]`
- `consume(ContextPacket, caller_id, expected_packet_sha256) -> Outcome[Payload]`
- `rehydrate(ContextPacket, caller_id, expected_packet_sha256, exact_selector) -> Outcome[ContextPacket]`

All outcomes have status, data, detail and recovery. A failed operation returns no
partial payload. These are synchronous local reads. No result authorizes execution,
training, generation adoption or external actions. No time-bound grant is issued.

## Public field map
| Structure | Exact fields / validation |
|---|---|
| Request | schema/format/policy; declared operator; entire ticket; exact record hash; task-state identity; archive location binding when used; budget; selectors |
| Budget | explicit canonical-JSON UTF-8 byte unit; 1..131072 payload bytes; 0..2097152 accepted evidence bytes |
| Task selectors | sorted unique required/optional fact IDs, assumption/result IDs, exact source fields |
| Experience shortlist | <=32 exact current refs with revision+hash, required flag and declared priority; optional casefolded lexical query terms |
| Source slices | <=32 exact selected experience/source/digest, nonempty byte bounds; valid UTF-8 boundaries |
| Payload | profile/ECID/generation identity; mandatory task spine; selected facts, assumptions and checked results; exact source fields; permission-checked interpretations and provenance; selected exact evidence slices |
| Packet metadata | exact request/payload digest; source/selection omissions; measured bytes; no-authority flags |

The task-state identity additionally binds the portable record and input pairs; ECID
alone does not distinguish changed records. Request defaults select no optional content.
Stage-required fields are always mandatory even when a caller leaves selectors empty.

Original facts, assumptions, unresolved questions, source classes, interpretation author
and uncertainty remain explicit. Local source file metadata is the upstream operator's
attribution, not an authenticated instruction hierarchy or semantic fact verification.

## Preconditions / postconditions / invariants
Before building: a RUNNING exact ticket/revision, current qualification and matching
source/ledger owners must be valid. Experience refs must target the pinned archive.
On success: the complete mandatory payload and selected optional material fit the
explicit budget and pass current-owner checks. On failure: status identifies why and
owners remain unchanged. Every consume performs fresh checks; every rehydrate produces
a new packet value or failure. No stale packet, historical receipt or digest renews
permission. The original TaskRecord is never modified by hydration.

Optional inaccessible experiences are omitted with a reason, without exposing their
text. Integrity failures are not silently treated as mere irrelevance. A previously
valid packet whose selection would now differ is rejected, not silently rewritten.

## Recovery and limitations
Required overflow returns a measured required-prefix byte count at the failure point
(not a complete estimate of every future mandatory item), plus explicit budget-change
or authorized-stage-decomposition choices. This implementation does not automatically
split tasks or update clarifications. Exact selected-source rehydration is implemented;
unknown meaning and semantic contradictions remain outside this deterministic selector.

Consume rebuilds from exact current inputs. Interrupted reads publish nothing. Existing
owner transactions and their tests still govern task/archive durability. A cooperating
single-worker process model is assumed; rechecks are not a distributed lease. Raw source
exports and already-used model context cannot be recalled through this API.

## Tools and reproducible views
Schemas are generated with the existing `tools/generate_generation_schemas.py`.
The three JSON logic graphs generate Markdown/Mermaid and DOT through the shared
`tools/generate_subsystem_logic.py --view context` command. Add `--render` only for
optional Graphviz SVG/PNG output. Static dependency checks forbid unreviewed import
edges; they are not a general malicious-code sandbox.
