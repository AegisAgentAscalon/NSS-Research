# NSS recovery flowcharts

Editable Mermaid sources for the Recovery 001A/001B contract simulator. For the comprehensive build-level subsystem logic, see `PSEUDOCODE_FLOWCHART_ATLAS.md`, generated from `spec/logic_atlas.json`. Render in a Mermaid-capable Markdown viewer. These diagrams include planned systems. 001A implements serialized profile/ECID checks, integer computation/replay, and a single-runner local mock action ledger. 001B adds a durable single-runner recovery-attempt/checkpoint publication boundary. Other system boxes remain planned. External executors, neural operations, multi-runner coordination, and production deployment remain design only.

## System overview

```mermaid
flowchart TD
 Input[User input and source evidence] --> Context[Context manager]
 Context --> Core[Frozen Core under ECID]
 Core --> Intent[Generation intent]
 Intent --> Output[Qualified output and validation]
 Core --> Request[Capability request]
 Request --> Registry[Qualified profiles and transitions]
 Registry --> Loader[Authorized transition simulator]
 Loader --> Core
 Core -. curated gap evidence .-> Builder[External Builder]
 Builder --> Qualifier[Independent qualification]
 Qualifier --> Nexus[Nexus authorization]
 Nexus --> Release[Atomic release]
 Release --> Registry
```

## Core package and runtime

```mermaid
flowchart LR
 subgraph Package[Versioned Core generation package]
 Weights[Immutable weights]
 Specs[Tokenizer and context specifications]
 ABI[Context and Overlay ABIs]
 end
 Package --> Runtime[Compatible runtime services]
 Runtime --> Load[Loader and state management]
 Runtime --> Train[Isolated training executor]
 Train --> Qualify[Independent qualification]
 Qualify --> Authorize[Nexus authorization]
 Authorize --> Deploy[Deployment]
 Weights -. learned request .-> Runtime
```

## Profiles and transitions

```mermaid
flowchart TD
 Request[Requested target profile] --> Check{Qualified profile and directed edge?}
 Check -->|No| Reject[Reject and retain original state]
 Check -->|Yes| Auth{Authorized?}
 Auth -->|No| Reject
 Auth -->|Yes| Mode{Declared transition mode}
 Mode -->|Compatible reuse| Keep[Preserve compatible state]
 Mode -->|Replay| Actions{Uncertain external action?}
 Actions -->|Yes| Reconcile[Stop and reconcile]
 Actions -->|No| Inputs{Portable replay inputs available?}
 Inputs -->|No| Stop[Recovery required]
 Inputs -->|Yes| Clear[Recompute target from hashed portable inputs; discard old cache and draft]
 Keep --> Load{Target load succeeds?}
 Clear --> Load
 Load -->|No| Reject
 Load -->|Yes| Commit[Publish target ECID and tagged state]
 Commit --> Replay[Return rebuilt target state; tests compare with clean execution]
 Replay --> Execute[Continue under pinned ECID]
```

## Context and cognition

```mermaid
flowchart TD
 Budget[Compute budget governs all stages] -.-> Select
 Budget -.-> Think
 Budget -.-> Generate
 Input[Intent and clarification] --> Select[Select typed evidence]
 Select --> Fits{Mandatory context fits?}
 Fits -->|No| Recover[Decompose and rehydrate references]
 Recover --> Valid{Meaning preserved within budget?}
 Valid -->|No| Fail[Typed failure]
 Valid -->|Yes| Packet[Context packet with ECID]
 Fits -->|Yes| Packet
 Packet --> Think[AR cognitive step]
 Think --> Next{Next operation}
 Next -->|Retrieve| Select
 Next -->|Clarify| Input
 Next -->|Ready| Generate[Generation intent]
 Generate --> Output[Output engine and validation]
 Output --> Carry[Carry forward essential state]
```

## Memory and learning eligibility

```mermaid
flowchart TD
 Evidence[Source evidence with provenance] --> Memory[Structured memory candidate]
 Memory --> Review[Interpretation and review revisions]
 Review --> Stored[Stored memory]
 Review --> Archive[Curated experience archive]
 Evidence --> Retention[Auditable retention and deletion policy]
 Archive --> Eligible{Training eligibility}
 Eligible -->|Approved| Dataset[Curated dataset]
 Eligible -->|Restricted| Policy[Check permitted use before inclusion]
 Eligible -->|Denied| Exclude[Exclude from training]
 Dataset --> Builder[Builder input]
```

## Training and deployment

```mermaid
flowchart TD
 Gap[Capability gap evidence] --> Need{Training necessary?}
 Need -->|No| Existing[Retrieval routing clarification or existing skill]
 Need -->|Yes| Permit[Nexus training authorization]
 Permit --> Data[Approved dataset and frozen target Core]
 Data --> Train[Isolated candidate training]
 Train --> Qualify{Independent qualification passes?}
 Qualify -->|No| Reject[Reject and archive]
 Reject -. new candidate only .-> Data
 Qualify -->|Yes| Package[Immutable candidate and evidence]
 Package --> Authorize{Nexus deployment authorization?}
 Authorize -->|No| Hold[Remain non-production]
 Authorize -->|Yes| Release[Atomic generation publication]
 Release --> Preserve[Preserve prior qualified configuration]
```

## Output and external action boundaries

```mermaid
flowchart TD
 Intent[Intent with explicit positive and negative constraints] --> Engine{Qualified output engine}
 Engine --> AR[Baseline AR]
 Engine --> DARP[Optional qualified DARP]
 AR --> Validate{Shared applicable validation}
 DARP --> Validate
 Validate -->|Fail| Retry[Bounded retry or typed failure]
 Validate -->|Pass| Kind{Output kind}
 Kind -->|Content| Final[Finalize and record presented segment]
 Kind -->|External action| Permit[Nexus action authorization]
 Permit --> Ledger[PENDING intent with idempotency key]
 Ledger --> Claim[Persist UNCERTAIN before effect]
 Claim --> Executor[001A local mock effect store]
 Executor --> Receipt[Persist COMMITTED receipt]
 Claim -. crash or unknown outcome .-> Block[Block automatic replay]
 Block --> Reconcile[Explicit receipt reconciliation]
 Reconcile -->|Receipt found| Receipt
 Reconcile -->|Proven absent in local mock| Ledger
 Receipt --> Duplicate[Repeated key returns receipt without execution]
 Final --> Carry[Authoritative continuity state]
 Receipt --> Carry
```

## Rare Core generation upgrade

```mermaid
flowchart TD
 Justify[Foundational change justification] --> Permit[Explicit Nexus approval]
 Permit --> Train[Train new Core package]
 Train --> Qualify[Independent qualification including Core-only]
 Qualify --> Plan[Explicit overlay memory and state migration plan]
 Plan --> Authorize[Deployment authorization]
 Authorize --> Switch[Atomic new generation activation]
 Switch --> ECID[New ECID compatibility boundary]
 Switch --> Old[Prior generation remains recoverable]
 Old --> Rollback[Qualified rollback with state and action reconciliation]
```

## Plain language overview

```mermaid
flowchart TD
 Ask[Understand the request] --> Find[Find relevant evidence]
 Find --> Think[Use the stable Core]
 Think --> Skills[Load only a tested skill configuration]
 Skills --> Answer[Create and check the answer]
 Answer --> Remember[Review useful memories separately]
 Remember --> Learn[Train future candidates only when justified]
 Learn --> Test[Independently test candidates]
 Test --> Approve[Authorize a qualified replacement]
 Approve --> Recover[Keep a valid recovery path]
```

## 001A crash and restart boundary

```mermaid
flowchart TD
 Pending[PENDING persisted] --> Claim[UNCERTAIN persisted]
 Claim --> Effect[Idempotent mock effect and receipt persisted]
 Effect --> Commit[COMMITTED ledger receipt persisted]
 Pending -. process exits .-> Restart[Restart converts abandoned PENDING to UNCERTAIN]
 Claim -. process exits .-> Restart
 Effect -. process exits .-> Restart
 Restart --> Stop[Automatic replay blocked]
 Stop --> Check{Explicit reconciliation finds receipt?}
 Check -->|Yes| Commit
 Check -->|Authoritative absence in local mock| Retry[PENDING; explicit retry required]
 Retry --> Claim
 Commit --> Skip[Replay skips committed action]
```

## 001B durable recovery publication boundary

```mermaid
flowchart TD
 Current[Published source checkpoint AB] --> Prepare[Persist PREPARED attempt
source hash + target ECID + inputs + action keys]
 Prepare --> Compute[Recompute target A from portable inputs]
 Prepare -. crash .-> Restart1[Restart: source AB still current; resume PREPARED]
 Compute -. crash before stage .-> Restart1
 Compute --> Stage[Persist content-addressed target checkpoint
mark attempt STAGED]
 Stage -. crash .-> Restart2[Restart: source AB still current; validate STAGED target]
 Restart1 --> Compute
 Restart2 --> Guard{Source hash, target ECID,
action set, directed edge, authorization
and target load still valid?}
 Stage --> Guard
 Guard -->|No| Fail[FAILED attempt; keep source current]
 Guard -->|Yes| Publish[Single SQLite transaction:
current pointer -> A + attempt -> PUBLISHED]
 Publish -. process exits after commit .-> Restart3[Restart sees A current and PUBLISHED together]
 Publish --> Done[Continue under published target ECID]
 Restart3 --> Done
```

A resumed PUBLISHED attempt reads its historical result without moving the current pointer. Failed or corrupt reads return a typed modeled error and current state when readable. See the schema-v2 `checkpoint_recovery` atlas for the full status graph.
