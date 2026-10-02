#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from nss_base.logic_atlas import load_atlas, flow_metrics

DOCS=ROOT/'docs'


def safe(s):
    return s.replace('"', "#quot;").replace("|", "#124;").replace('\n',' ')


def mermaid(flow):
    out=['```mermaid','flowchart TD']
    shapes={'start':('[',']'),'process':('[',']'),'decision':('{','}'),'success':('([','])'),'failure':('([','])')}
    for n in flow['nodes']:
        left,right=shapes[n['kind']]
        label=safe(n['label'])
        out.append(f'  n_{n["id"]}{left}"{label}"{right}')
    for e in flow['transitions']:
        when=e['when']
        if when=='always': out.append(f"  n_{e['from']} --> n_{e['to']}")
        else: out.append(f'  n_{e["from"]} -->|"{safe(when)}"| n_{e["to"]}')
    out.append('```')
    return '\n'.join(out)

atlas=load_atlas()
lines=[]
lines += ['# Aegis NSS pseudocode flowchart atlas','',
          '> **Status:** implementation specification framework, not executable NSS proof. The JSON source of truth is `spec/logic_atlas.json`; this document is generated from it.','',
          '## Why this exists','',
          'The purpose of this atlas is to make subsystem logic reviewable *before* implementation, so future code can be compressed without deleting contract semantics. Each flow has typed inputs/outputs, a state graph, typed failure exits, forbidden edges, invariants, pseudocode, and basic complexity metrics.','',
          '### Compression rule','',
          '**Compress repeated implementation mechanics, not decisions or invariants.** Shared guards such as validation, authorization, qualification, replay safety, hashing, and atomic publication should become common primitives only after tests prove equivalent behavior.','',
          '## Shared pseudocode primitives','']
for k,v in atlas['shared_primitives'].items():
    lines.append(f'- `{k}` — {v}')
lines += ['', '## Global rules','']
for r in atlas['global_rules']:
    lines.append(f'- {r}')

for i,flow in enumerate(atlas['flows'],1):
    m=flow_metrics(flow)
    lines += ['',f'## {i:02d}. {flow["title"]}','',
              f'**ID:** `{flow["id"]}`  ', f'**Owner:** {flow["owner"]}  ', f'**Status:** `{flow["status"]}`; implementation: `{flow["implementation"]}`  ',
              f'**Purpose:** {flow["purpose"]}','',
              f'**Inputs:** ' + '; '.join(f'`{x}`' for x in flow['inputs']) + '  ',
              f'**Outputs:** ' + '; '.join(f'`{x}`' for x in flow['outputs']) + '  ',
              f'**Logic metrics:** {m.nodes} nodes · {m.transitions} transitions · {m.decisions} decisions · normalized cyclomatic complexity {m.cyclomatic_complexity}','',
              '### Flowchart','',mermaid(flow),'','### Pseudocode','','```text']
    lines += flow['pseudocode']
    lines += ['```','','### Invariants','']
    lines += [f'- {x}' for x in flow['invariants']]
    lines += ['','### Typed failures','']
    lines += [f'- `{x}`' for x in flow['failure_codes']]
    lines += ['','### Forbidden edges','']
    lines += [f'- ✕ {x}' for x in flow['forbidden_edges']]
    lines += ['','### Optimization notes','']
    lines += [f'- {x}' for x in flow['optimization_notes']]

(DOCS/'PSEUDOCODE_FLOWCHART_ATLAS.md').write_text('\n'.join(line.rstrip() + ('<br>' if line.endswith('  ') else '') for line in lines)+'\n',encoding='utf-8')

compression='''# NSS logic compression guide

## Goal

Produce the **smallest implementation that still expresses every tested contract decision**. The objective is not minimum lines of code; it is minimum duplicated logic, minimum state ambiguity, minimum data movement, and minimum branches that do not correspond to a real contract choice.

## Optimization order

1. **Make the state machine correct and testable.** Never compress before terminal outcomes, rollback, and forbidden edges are explicit.
2. **Normalize inputs at boundaries.** Internals may reuse validation only while the bytes, scope, and authority remain unchanged. Revalidate mutable files on use, resumed checkpoints, and time-sensitive authorization.
3. **Factor repeated gates.** `VALIDATE`, `QUALIFIED`, `AUTHORIZE`, `REPLAY_SAFE`, `HASH`, and `ATOMIC_PUBLISH` should be single shared implementations when semantics are truly identical.
4. **Use immutable references rather than copied payloads.** Pass content hashes/IDs for evidence, artifacts, context, and checkpoints whenever the consumer can resolve them.
5. **Prefer tables/data over branching code.** QAPs, directed transitions, failure destinations, compatibility rules, and qualification scopes should be data-driven rather than giant `if/elif` trees.
6. **Precompute stable closures.** Dependency closure and released-generation metadata can be computed once and keyed by immutable manifest hash.
7. **Keep one publication point.** Stage work freely; mutate production identity exactly once through an atomic publish boundary.
8. **Separate replayable compute from side effects.** This eliminates special cases during recovery and keeps internal replay cheap.
9. **Measure before clever optimization.** Token count, memory movement, model passes, recurrent depth, overlay loads, and wall-clock time should be instrumented before optimization.
10. **Delete only after equivalence tests.** If two branches are merged, tests must prove identical outcomes, invariants, and failure retention for both old paths.

## Preferred implementation shape

```text
public boundary
  -> normalize / validate once
  -> lookup immutable metadata
  -> run minimal decision table
  -> call one domain operation
  -> validate result
  -> stage
  -> atomic publish OR typed failure preserving source
```

## Anti-patterns

- Treating a file path as immutable or reusing an expired authorization merely because earlier validation passed.
- Encoding transition rules in scattered `if` statements instead of one released transition table.
- Passing whole documents when a reference plus selected slice is enough.
- Generating prose to represent machine state that can remain typed/latent.
- Using exceptions for expected domain outcomes when a typed result is clearer.
- Catch-all managers that own routing, storage, policy, training, and deployment.
- Optimizing line count by merging states that have different rollback or audit meaning.

## Review metric

For every implementation pass, compare:

- behavior/tests preserved,
- number of public interfaces,
- duplicated guard implementations,
- decision count/cyclomatic complexity,
- serialized bytes moved,
- active context/tokens,
- artifact loads,
- external side-effect calls,
- number of production mutation points.

A shorter implementation that increases any ambiguity around ownership, state, or rollback is **not** an optimization.
'''
(DOCS/'LOGIC_COMPRESSION_GUIDE.md').write_text(compression,encoding='utf-8')

template='''# Subsystem implementation packet template

Use this template immediately before implementing any subsystem from `spec/logic_atlas.json`.

## 1. Identity
- Subsystem ID:
- Owner module/package:
- Atlas flow ID/version:
- Adjacent public contracts:

## 2. Typed boundary
- Input types + validation:
- Output/result types:
- Persistent state owned:
- State explicitly *not* owned:

## 3. State machine
- Start state:
- Decision table:
- Success terminal(s):
- Failure terminal(s):
- Retry/replay states:
- Atomic publication point, if any:

## 4. Dependencies
- Allowed imports/calls:
- Forbidden imports/calls:
- Events/requests emitted:

## 5. Preconditions / postconditions / invariants
Copy directly from the canonical contract/atlas, then specialize only where implementation requires more precision.

## 6. Failure and rollback
For each typed failure:
- stimulus,
- returned outcome,
- state retained,
- durable evidence written,
- replay/retry eligibility.

## 7. Tests before implementation
Write expected tests first:
- happy path,
- each decision branch,
- each typed failure,
- stale/corrupt state,
- rollback/source-retention,
- forbidden-edge regression,
- deterministic equivalence where applicable.

## 8. Compression pass
Only after tests pass:
- duplicate guards to factor,
- lookup tables to precompute,
- payloads to replace with immutable refs,
- redundant serialization/model passes to eliminate,
- branches that can be data-driven.

## 9. Definition of Done
- Atlas flow still matches implementation.
- Public API documented.
- All tests pass.
- No forbidden dependency edge.
- Failure paths retain last-known-good state.
- Version/provenance updated.
- Flowchart/pseudocode changed if code behavior changed.
'''
(DOCS/'IMPLEMENTATION_PACKET_TEMPLATE.md').write_text(template,encoding='utf-8')

metrics=['# Logic atlas metrics','', '> Generated from `spec/logic_atlas.json`. These are structural review aids, not performance measurements or implementation upper bounds. Complexity = E - N + T + 1 after joining T terminal nodes to one virtual exit. Implicit helper-failure edges are not counted.','', '| Flow | Nodes | Edges | Decisions | Terminals | Normalized cyclomatic complexity |','|---|---:|---:|---:|---:|---:|']
for fid,m in [(f['id'],flow_metrics(f)) for f in atlas['flows']]:
    metrics.append(f'| `{fid}` | {m.nodes} | {m.transitions} | {m.decisions} | {m.terminals} | {m.cyclomatic_complexity} |')
(DOCS/'LOGIC_ATLAS_METRICS.md').write_text('\n'.join(metrics)+'\n',encoding='utf-8')
print('generated docs')
