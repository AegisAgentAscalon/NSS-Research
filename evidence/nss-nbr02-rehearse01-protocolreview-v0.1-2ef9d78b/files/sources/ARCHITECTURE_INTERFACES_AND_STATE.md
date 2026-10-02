# State inventory

Version 0.1 | 2026-09-24 | Documentation view; not execution authorization.

## ST-01 — Serving parameters

**Owner:** Each neural component

**Representation:** Versioned learned tensors

**Lifetime:** Accepted component generation/revision

**Writer:** Approved candidate training; frozen P/V while serving

**Reset / migration:** Replace only through qualification; retain rollback

**Status:** ROLE_POLICY_ADOPTED; TOY_WEIGHTS_IMPLEMENTED

**Sources:** S01; S08

## ST-02 — Temporal task state

**Owner:** Active neural component; full NSS ownership unresolved

**Representation:** Learned recurrent tensors

**Lifetime:** Across events within a declared scope

**Writer:** Learned transition

**Reset / migration:** Episode/task reset, compatible checkpoint or qualified replay

**Status:** TS01_LOCAL_IMPLEMENTATION

**Sources:** S08; S14

## ST-03 — Internal refinement state

**Owner:** Active component

**Representation:** Latent iteration state

**Lifetime:** Within one processing episode

**Writer:** Proposed recurrent-depth operator

**Reset / migration:** Stop/continue and iteration limits unresolved

**Status:** PROPOSED

**Sources:** S02

## ST-04 — Maintained management workspace

**Owner:** Writer/owner per scope not yet selected

**Representation:** Discrete fields/tokens; soft slots separate candidate

**Lifetime:** Bounded resident task/phase context

**Writer:** Source-copying or learned writer, explicitly declared

**Reset / migration:** Preserve provenance; stale/evicted fields need declared handling

**Status:** DIRECTION_ADOPTED; NATIVE_UNTESTED

**Sources:** S09; S10; S12

## ST-05 — Active context and KV

**Owner:** Each active model privately

**Representation:** Token packet; optional KV caches

**Lifetime:** Model session or supported segment window

**Writer:** Tokenizer/context constructor/model

**Reset / migration:** Version-specific cache invalidation

**Status:** RETAINED_INTERFACE_DIRECTION

**Sources:** S02; S04; R09

## ST-06 — Exact event/evidence archive

**Owner:** Governed memory service

**Representation:** Source records plus provenance and permissions

**Lifetime:** Persistent within retention/consent rules

**Writer:** Observed events and explicitly labelled derivations

**Reset / migration:** Correction/supersession; qualified recovery; no source falsification

**Status:** SYNTHETIC_ARCHIVES_IMPLEMENTED

**Sources:** S01; S06; S07

## ST-07 — Indexes and record bindings

**Owner:** Memory/context service

**Representation:** Exact keys, scopes, revisions, retrieval structures

**Lifetime:** Persistent or rebuildable

**Writer:** Declared deterministic/learned indexing policy

**Reset / migration:** Rebuild from authoritative records; identify unresolved bindings

**Status:** CM_WRAPPERS_IMPLEMENTED

**Sources:** S06; S07

## ST-08 — Broader Working Space

**Owner:** Task/investigation owner

**Representation:** Inspectable tasks, branches, tests, artifacts, references

**Lifetime:** Across interruptions and core handoffs

**Writer:** Declared component/host changes

**Reset / migration:** Cutoff and revision-bound restore

**Status:** RETAINED_DIRECTION

**Sources:** S02; S04

## ST-09 — Fast adaptation/eligibility

**Owner:** Declared adaptive surface

**Representation:** Temporary associations or delayed-credit traces

**Lifetime:** Algorithm-specific

**Writer:** Proposed update/decay rule

**Reset / migration:** Explicit scope, decay, clearing and resume

**Status:** PROPOSED; NOT_TS01_ONLINE_LEARNING

**Sources:** S02

## ST-10 — Optimizer, gradients and cursor

**Owner:** Training job / Forge

**Representation:** Optimizer history, RNG, dataset cursor, transient gradients

**Lifetime:** During candidate training; checkpointed for resume

**Writer:** Approved training engine

**Reset / migration:** Exact compatible resume or explicitly new run

**Status:** TS01_HISTORY_RETAINED

**Sources:** S08

## ST-11 — Appraisal and hypothetical state

**Owner:** Tertiary with Primary handoff

**Representation:** Unselected representation

**Lifetime:** Across a bounded investigation/phase

**Writer:** Observation-sensitive appraisal/prediction

**Reset / migration:** Keep imagined origin; do not reinterpret as observation

**Status:** ROLE_DIRECTION; UNINTEGRATED

**Sources:** S01; S02

## ST-12 — Runtime and authority metadata

**Owner:** Host/Runtime/Nexus

**Representation:** Permissions, jobs, schemas, leases, generation IDs

**Lifetime:** Operational lifetime

**Writer:** Authorized deterministic control

**Reset / migration:** Fail closed for unauthorized operation; preserve valid fallback

**Status:** POLICY_ADOPTED; CURRENT_SOURCE_UNAUDITED

**Sources:** S01; S02

# Interface register

## IF-01 — Observation → context/state

**Payload:** Committed observable event; origin, scope, order, permissions

**Boundary:** No hidden evaluator labels or future suffix

**Status:** Semantic policy retained; binary/schema details open

**Sources:** S02; S09

## IF-02 — Workspace → recurrent transition

**Payload:** Bounded management fields plus representation/version

**Boundary:** Tokens are data; they neither execute themselves nor grant authority

**Status:** IM-01 proposed; no native implemented NSS bridge

**Sources:** S10; S12

## IF-03 — Component → exact memory

**Payload:** Retrieval intent, record/scope/revision and allowed operation

**Boundary:** Address validity, task relevance and truth are separate

**Status:** CM wrappers only; production service not audited

**Sources:** S06; S07

## IF-04 — Secondary ↔ Primary

**Payload:** Task state/results, evidence, uncertainty, compatible learned features

**Boundary:** Primary remains participating and usable alone

**Status:** Retained direction; trained bridge dimensions open

**Sources:** S01; S02

## IF-05 — Secondary → Tertiary handoff

**Payload:** Checkpoint/cutoff, pending work, experience references, appraisal origin

**Boundary:** S/T mutual exclusion; imagined/observed provenance preserved

**Status:** Role contract retained; atomic implementation open

**Sources:** S02; S04

## IF-06 — Tertiary → Primary/Secondary

**Payload:** Hypotheses, predictions, tests, discoveries with source status

**Boundary:** Exploration result is not observation or approved training data

**Status:** Role contract retained; native schema open

**Sources:** S01; S02

## IF-07 — Validator → Primary

**Payload:** Claim support/contradiction/insufficiency, evidence and uncertainty

**Boundary:** Advisory only; no veto or permit

**Status:** Role contract retained; no competent integrated validator shown

**Sources:** S01; S02

## IF-08 — NSS → Forge

**Payload:** Approved training job, dataset cutoff, surfaces, budget, checkpoints and assessment

**Boundary:** Shared headless engine; normal standalone LLM product retained

**Status:** Required endpoint; current source not inspected

**Sources:** S01

## IF-09 — NSS → Runtime/Nexus

**Payload:** Explicit operation request under host and runtime policy

**Boundary:** Approval layers independent; model text cannot grant permits

**Status:** Policy retained; current exact adapters open

**Sources:** S01

## IF-10 — Candidate → serving generation

**Payload:** Qualified weights, interface/state versions, codec and rollback package

**Boundary:** Acceptance independent of candidate and advisory Validator

**Status:** Lifecycle retained; trigger and migrations open

**Sources:** S01; S02

