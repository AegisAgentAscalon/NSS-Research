# Codex review handoff — NSS NBR02 SH01 v0.1

## Review requested
Audit the first working segmented-context/HSA maintenance prototype. Do not treat it as a
tri-core successor or full NSS maintenance qualification. No follow-up execution is dispatched.

## Main observations
- Three completed paired seeds: dense5553/6144, HSA6133/6144 task decisions. Whole worlds368/768
  vs758/768. Fourth dense1855/2048 retained; paired HSA unfinished at durable step200/600.
- Same exact dependency-indexed evidence for simple/segmented managers. Packets and predictions
  agree across change/restart. Cache reduces build work, not input bytes delivered to model.
- Six-job management cycle medians improve30–35%, including index+checkpoint/restart, with
  increased retained cache bytes. Timing order fixed; treat as bounded CPU evidence.
- Native selected-edge attention really avoids full score-square construction. Math/gradient
  checks pass. Yet HSA reader latency is2.33–3.49x dense at8/32/128 tasks. Large gather buffers;
  do not convert edge reductions into peak-memory or end-to-end efficiency claims.
- Dense reader's failure to meet functional targets means equal-quality comparisons remain open.
  A deterministic rule reaches2048/2048; this is a supplied-metadata learning fixture.

## Integrity and incomplete execution
Preflight initially exposed mutable snapshot aliasing, fixed before lock with old source/trace
retained. Corrected664 assertions pass;30 checkpoint hashes verified;21 endpoint files replayed
bit-exact;21 independent recounts match. Source lock is unchanged. Numeric trained-model agreement
covers only first8 confirmation worlds per HSA seed, not all records.

The runner was interrupted; initial per-update loss list was in RAM and lost. Main application
count is bounded4400–4600, plus4 preflight, below cap4800. No uncertain steps replayed. Only the
untouched scheduled8804 fits were finished. Exact first-process terminal time/RSS unavailable.
These limitations must not be silently repaired in a review or changed to an exact count.

## Questions worth reviewing
1. Is any claimed learned capability actually supplied by the compiler or dependency graph?
2. Does the data/task definition give a useful enough fixture for the intended maintenance reader?
3. How much of HSA's quality difference is explicit dependency restriction versus other graph effects?
4. What stronger dense baseline or same-graph efficient execution best isolates this?
5. Can packet/segment encoding caching reduce repeated compilation without stale revision/model reuse?
6. Add proper per-step journaling and signal-safe shutdown before another training dispatch.
7. Inspect per-seed false-ready/false-complete errors and timing scope; do not optimize a pooled scalar alone.

Suggested next candidate is engineering/controlled comparison, not more architectural ingredients:
keep the shared record contract; test grouped/block or efficient masked same-graph execution;
improve dense relational competence prospectively; only then claim equal-quality efficiency.
No DARP, giant context, or repeated overnight-repair experiment is implied.
