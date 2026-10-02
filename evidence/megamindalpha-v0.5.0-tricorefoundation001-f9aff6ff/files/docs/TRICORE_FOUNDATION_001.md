# TriCoreFoundation001 — implementation and migration boundary

Version 0.5.0, 20 September 2026. Current-role foundation; not a full neural architecture acceptance.

## Source precedence

The supplied cognition/low-bit handoff v1.0 (§§1, 5–7 and 11) and the user-approved foundation-first plan determine current intent. The recovered v0.4.14 source determines what was available to reuse. Later handoff-referenced versions and standalone studies are not manufactured into this checkout. This implementation makes no new model-size, learning-rule or native-backbone selection.

Historical root documents and the exact original source manifest are in `docs/history/`. All inherited diagrams/overlay docs remain historical unless explicitly superseded by a new document. The default CLI routes to current roles; direct legacy demo modules remain diagnostic controls.

## Source-to-target map

| Owner / seam | Implementation in this release |
|---|---|
| `generation_store.py::Generations` | Same SQLite journal owner, explicit current-role store format, manifest/reducer dispatch. No parallel task database and no automatic legacy conversion. |
| `foundation_store.py` / `foundation_events.py` | Current-role operations/pure replay for scoped admission, reviewed changes, pending ticks, checkpoints, completion, interruption, close and test-configuration boundaries. |
| `state_contracts.py` / `state_updates.py` | Shared reviewed state logic accepts neutral v3 configuration binding. Legacy v2 source tickets still use their original path. |
| `context_service.py` / `context_plan.py` / `context_contracts.py` | Same deterministic selection/evidence/revalidation logic; neutral v3 requests/packets use `FoundationContextSource`, not a fake `CatalogController` or empty overlay catalogue. |
| `experience_store.py` / `state_sources.py` | Original immutable evidence and purpose-aware permission checks reused. No new interpretation or consent owner. |
| `foundation_contracts.py` | Exact component/generation identities, scope, codecs, message/state envelopes, execution budgets and explicit test-only admission. |
| `foundation_adapters.py` | Replaceable role protocol and declared non-neural test adapters. |
| `foundation_runner.py` / `foundation_lock.py` | Synchronous bounded callbacks, actual Primary pre/post calls, OS cooperative exclusion, durable reservation and atomic complete-step publication. |
| `foundation_ports.py` | Unconnected generic Forge and independent Runtime seams. Unsupported capability is a result, not an invisible fallback. |
| `research/nbr01.py` | NOT_RUN study protocol and a hand-engineered harness self-test; no neural comparison or learning rule implemented. |
| Existing qualification/learning/dataset orchestration | Preserved historical owner code; remaining overlay-specific product integration is not reported as migrated. |

## Configuration and store identity

`Generations.create_foundation(...)` creates a new, explicitly empty local store with format `NSS.TriCoreFoundation001`. The old format remains `MegaMindAlpha.OverlayGenerationManager001`. A legacy store does not become current-role by changing a label or invoking a modern reader.

Each component descriptor pins role, component identity, revision, parameter digest, Primary generation, interface, state schema, codec, tokenizer/input ABI, frozen serving revision and capabilities. The configuration pins the complete role set, including explicit absent auxiliaries. The Primary must exist; two roles cannot share one component identity as a disguised merged-auxiliary redesign.

All active configurations in this first release are `TEST_ADAPTERS_ONLY`. A future real-model path must establish source-backed backend capabilities and independent qualification; changing an evidence-class string is not sufficient.

## One owner, separate state kinds

The Generations journal owns symbolic task revisions, temporal adapter state, candidate-job state and execution reservations. These are different lanes in one owner, not one undifferentiated memory:

- Exact source content stays in admitted immutable files / ExperienceArchive; it is not reconstructed from a hidden vector.
- Scoped symbolic changes use the existing reviewed delta engine and preserve historical revisions.
- Each component's temporal checkpoint is bound to its task, scope, exact configuration, owner revision, schema, codec, event and cutoff.
- The Secondary candidate-step checkpoint is separate from the serving state. The test adapter only increments a job counter; it is not an optimizer or parameter update.

Eligibility state, fast adaptable associations and richer appraisal state remain future declared lanes, not features inferred from the presence of a JSON checkpoint. No cached variable is exempt from scope/learning controls merely because it is called state.

New task admission is explicit. Importing an already-running legacy task, its mock-execution receipts, hidden-state migration across revisions, or a previously accepted production generation is NOT_SUPPORTED in this release. State restoration is exact, not a shape-only compatibility guess.

## Bounded phase scheduling

Each successful tick reserves the single local execution slot, then invokes:

```text
PRIMARY_ONLY: Primary -> Primary
TASK:         Primary -> Secondary inference -> Primary
LEARN:        Primary -> Secondary candidate-step interface -> Primary
REFLECT:      Primary -> Tertiary -> Primary
VERIFY:       Primary -> Validator advice -> Primary
```

Primary state changes are activations/checkpoints, not accepted-parameter changes. Each adapter's serving-parameter digest is compared with the pinned descriptor before and after callbacks. The test adapter hashes its actual deterministic parameter dictionary; this is not a claim that large-model parameter hashing has been integrated or is cheap. A real adapter must correctly cover its actual serving parameters and may require backend-supported freeze enforcement.

The controller does not continuously run while paused, powered off, or outside a requested tick. Its declared cadence is two actual Primary calls around a bounded step. Duration is measured and budget overruns are rejected **after return**. This is not hard preemption or a production power/latency measurement. Real long jobs need independent Runtime resource control and checkpoints between bounded slices.

Secondary and Tertiary never execute together through this controller. Candidate-step work uses the same exclusion. On supported cooperative workers, the OS file lock prevents a second process/thread from starting a callback or recovering a still-running job. It is not a sandbox against hostile Python, direct database rewriting, manually bypassed private APIs or independently spawned backend threads.

## Crash and retry semantics

`F_BEGIN` is durable before callbacks. Complete role states, messages, receipts and final output enter one `F_COMPLETE` transaction. A process exit before commit leaves the last complete state and a pending reservation; partial callbacks are not reported as completed. Recovery requires the OS lock to be available, an authorized local operator declaration and an explicit reason.

After interruption, retry with a **new operation ID** and the last committed state. An already-committed exact retry returns a historical receipt without rerunning callbacks or redisclosing a cached output. A changed request under an old ID is rejected. No external action is replayed; the installed role protocol prohibits such side effects in this release. Exact resume of generic training jobs is not implemented by these rules alone.

The test suite exercises real subprocess exits after reservation, after Primary, after Secondary candidate work, before complete commit, and after commit, as well as live cross-process lock contention.

## Evidence and communication

The exchange envelope carries the handoff's task/scope, sender/receiver interface, configuration and Primary generation, representation/codec, cutoff/state revision, origin kind, payload, source references and restoration binding. Its permission scope is empty; its authority is data only.

Generated exchanges may be derived, hypothetical or proposed actions, not observations. Initial Tertiary outputs remain hypothetical. Checked discoveries require a separate evidence-backed event; a Tertiary assertion is not itself an observed user memory. The Validator gives evidence advice to the Primary and has no permission/release API. Deterministic wrong-advice tests establish software separation, not neural checking skill or calibrated confidence.

Text/structured transport is available. Token IDs require matching tokenizer/input ABI; otherwise retokenization would need an explicit implementation. Latent references remain NOT_SUPPORTED without trained, qualified alignment. Equal vector sizes are never treated as equal meaning.

The existing context selector is still byte-budgeted, not a model tokenizer or native HSA/MSA implementation. All mandatory state remains present or the packet fails; no hidden truncation. Exact source slices retain their provenance and purpose-aware archive checks. Revocation is checked again after callbacks, but these are point-in-time checks across separate owners, not an atomic multi-store authorization lease.

## Configuration succession and boundaries

The test-only whole-configuration switch requires no pending job or open task, exact expected-current identity, independent local reviewer/issuer declarations and an evidence digest. Historical configurations remain available for rollback; closed tasks and states remain history and are not silently reopened under new semantics. A Primary generation cannot be rebound to different Primary parameters/interfaces.

The qualification label is explicitly `STRUCTURAL_TEST_ATTESTATION_NOT_MODEL_QUALIFICATION`. It neither replaces the existing Qualifications owner nor establishes neural performance. Future P2/S2/T2 migration, actual companion-contributed continuity criteria, experience catch-up windows and model qualification remain separate required product work.

## NBR-01 entry and limits

The hand-engineered `ClockEstimator` retains an optional cue over events and runs a separate query-refinement loop. Its checkpoints have eight raw numerical bytes plus integrity/scope metadata. Its 24 smoke cases check clocks, state-off behavior, delay, reset and exact restart. They do not demonstrate useful learned recurrence, low-bit learning, Transformer superiority/inferiority or reduced companion memory cost.

The full preflight reports missing competent task-matched Transformer and trained recurrent candidates, a measured target-device budget, and pilot-selected confirmatory criteria. The framework is sufficient to host separately identified studies; it does not decide their winners. NBR-00 is still partial overall; the language-and-memory G02 baseline and full NBR-01–07 studies are not completed.
