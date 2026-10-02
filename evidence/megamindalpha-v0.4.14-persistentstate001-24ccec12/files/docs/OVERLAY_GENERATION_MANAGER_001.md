# OverlayGenerationManager001 — exact local catalogue releases

## Scope and ownership
This pass accepts a WHOLE generation manifest, verifies its exact qualifications and
publishes a durable catalogue pointer. It does not replace an Aegis Runtime execution
permit, mutate a running serving process, or implement general multi-session paging.

| Module | Sole responsibility |
|---|---|
| generation_contracts | Pure bounded schemas, dependencies, permitted profiles/edges and release policy |
| generation_evidence | Live child-certificate and neural-source validation through public APIs |
| generation_state | Pure event reducer: immutable generations, grants, epochs, archive and stage pins |
| generation_store | Public lifecycle/storage owner; no neighboring private SQL |
| local_journal | Shared SQLite/hash-chain mechanics only; distinct owner files and validators |
| generation_cli | Explicit operator operations; no automatic downloads/training |
| overlaygenerationmanager001 | Opt-in synthetic demonstration and one real staged-weight forward pass |

QualificationEvidence002 still owns individual numerical claims. LocalNexusPermissions002
still grants ONLY its fixed neural replay operation. Neither contract was widened.
The new generation reviewer validates catalogue closure, not fresh scientific performance.
The separate release issuer authorizes one local catalogue transaction, not production.

## Immutable generation contract
A manifest binds generation ID/producer, exact neural evidence binding, selected
A/B checkpoint hashes, dependencies, ordered allowed profiles and profile ECIDs,
directed transitions, state-reuse policy and every evidence ID/certificate digest.
No released name or membership is overwritten. Missing evidence fails closed.

Every generation contains CORE with its actual qualification. Every selectable profile
must have a qualified directed return to CORE. Current checkers implement AB->A and
A->CORE only. B-alone evidence does NOT invent B->CORE evidence. Current-generation
families can therefore expose CORE/A/AB, but not an unsupported fallback edge.

Unused member weights and dependencies outside the released family are rejected.
The two-slot attachment order is fixed; metadata does not claim mathematical isolation.
Only Core-only, A-only and A/B family structures supported by those exact checks are
released in this experiment. A2 and generic future architectures need new evidence
adapters rather than renaming a checkpoint to evade this limitation.

## Review versus release
1. A declared PRODUCER submits a manifest; live child evidence is checked.
2. A distinct declared REVIEWER seals a generation-catalogue closure certificate.
3. An OPERATOR proposes BOOTSTRAP, UPDATE or ROLLBACK against the current epoch/hash.
4. A distinct ISSUER issues a scoped expiring, nondelegable one-use release grant.
5. The operator consumes it to enter PREPARED, then stages the exact complete weights.
6. Publication rechecks current child evidence/source permissions, expiry/revocation,
   exact source epoch, same Core package, sealed bytes, and absence of open managed work.
7. One journal transaction changes the current generation/epoch, archives its predecessor,
   and records completion. An intermediate state with only half these changes is invalid.

The new operation is `PUBLISH_LOCAL_OVERLAY_GENERATION`. A replay grant has the wrong
schema, policy, store and request binding. Catalogue grants explicitly set
`runtime_execution_permit=false` and `production_deployment_authorized=false`.

## Lifecycle, recovery and unsuccessful outcomes
`GRANTED -> PREPARED -> STAGED -> PUBLISHED` is the only successful release chain.
PREPARED consumes the grant. Local staging may resume after a crash only with fresh
live checks; it executes no external action. A PUBLISHED retry returns the original
receipt even if later releases occurred. It NEVER moves the pointer again.

An expired, revoked or otherwise invalid consumed request can be explicitly ABANDONED.
It cannot be reset to GRANTED. A new exact request and issuer approval are required.
A published operation cannot be undone by abandonment. Explicit ROLLBACK requires an
exact archived target, new grant, current evidence and the current source epoch.
No same-Core constraint is bypassed by labelling an upgrade as a rollback.

Errors retain their original codes: VALIDATION_FAILED, INCOMPATIBLE_CONFIGURATION,
INSUFFICIENT_EVIDENCE, AUTHORIZATION_DENIED, TRAINING_RESTRICTED, CONSTRAINT_CONFLICT,
CAPABILITY_UNAVAILABLE, BUDGET_EXHAUSTED or RECOVERY_REQUIRED, as applicable. A failed
release leaves the prior current pointer intact. Revoking current qualification blocks
later use; the pointer remains inspectable as history, not silently replaced by an
unqualified fallback. History inspection is not a current-use attestation.

## Managed stages and neural state
This catalogue has ONE cooperating execution worker. ALL its work registers a durable
stage ticket with store ID, generation epoch/hash, exact profile ECID, caller and stage
ID. No second stage is admitted concurrently. Publication requires no open stage.
Read returns only the selected profile's sealed artifacts, not every stored member.

A holder must finish/recover or discard its computation and preserve required portable
state BEFORE closing the ticket. Closing does not itself perform that work or claim a
successful task outcome. Source permission is rechecked on each artifact read. Closing
revoked work is allowed because it admits no new computation.

A restart can inspect outstanding tickets for explicit recovery; it never assumes
that a crash made unfinished work safe to erase. Closed tickets cannot be reopened.
Returning to identical weights creates a NEW epoch: older tickets/caches remain stale.
No cross-generation latent/KV migration is claimed. No unregistered foreign task is
covered by this quiescence barrier. This is a next-step interface, not a serving lock.

## Storage and limits
One separate generation SQLite database records an append-only bounded event log.
Immutable staged checkpoint documents are embedded in STAGE events in this tiny probe;
large content-addressed tensor storage/disk paging is deferred. Meta count/head and
hash-chain validation detect incomplete/tampered records; a semantic reducer rejects
impossible event sequences. There is no independently writable current/archive index.

Bounds: 2,000 events, 32 MiB generation history; existing JSON document limits apply.
All writes use SQLite synchronous FULL transactions. Tests terminate actual child
processes. They do not simulate power loss, adversarial disk controllers or cross-host
consensus. Current evidence and permissions reside in other stores: checks are not a
multiwriter distributed authorization lease. Roles are declared, not authenticated.
Revocation blocks subsequent supported reads; it cannot recall returned/exported bytes.

## Demonstration and interpretation
One actual tiny Core/A/B family supports both a narrower generation (CORE/A) and a
wider one (CORE/A/AB). The second adds available capability by catalogue membership;
it is NOT a new training or accuracy experiment. An AB managed-stage read supplies the
staged weights to one real PyTorch forward pass. The earlier report and mock effect
ledger are unchanged. The generation manager never invokes action execution.

See OVERLAY_GENERATION_LOGIC.md and the implementation packet for pseudocode. Concrete
failure stimuli and expected outcomes are mapped in the current audit/test index.
