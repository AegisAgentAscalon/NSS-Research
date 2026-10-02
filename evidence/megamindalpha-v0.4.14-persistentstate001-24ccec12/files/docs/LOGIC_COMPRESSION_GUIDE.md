# NSS logic compression guide

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
