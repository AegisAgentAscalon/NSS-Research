# Maintenance — v0.4.14 / PersistentState001

## What was reused or corrected
Generations remains the single owner of current TaskRecord heads and journal commits.
State contracts/reduction are pure helpers, not competing stores. Existing EvidenceReader
and ExperienceArchive public readers own exact field, hash, size and permission checks;
state_sources composes them instead of copying them. Context remains read-only.

The existing identity-sensitive experience fixture now takes an optional sensitivity
argument instead of requiring duplicated setup. The schema and flowchart generators are
extended, not forked; no new one-off Python tool was added. Scoped lifecycle validation
shares existing handoff/completion logic. Legacy schema exports remain byte-identical.

The stale working_ar persistence-owner annotation was corrected: Generations owns managed
TaskRecord heads, RecoveryStore remains the older separate proof. The learned AR loop is
still unimplemented. Active NEXT_STEPS/AGENTS/Codex instructions now point to the new scope.

## Measured change
Physical Python lines include comments/blanks and demonstrations; generated files and
historical audit logs are excluded. Lower line count is not itself correctness or speed.

| Area | Before files / lines | After files / lines |
|---|---:|---:|
| Runtime, including demos | 75 / 10,708 | 79 / 11,238 |
| Tests and helpers | 68 / 7,700 | 71 / 8,254 |
| Build/development tools | 20 / 1,201 | 20 / 1,259 |

Four runtime modules were added (443 lines total); eleven inherited runtime files changed
(+143 / -46 lines). Total runtime growth: **530** lines. Two existing build tools changed
(+60 / -2); none added. Three test/helper files add **554** lines. No inherited Python
test/helper was changed or removed: all **68** remain byte-identical. The 48 new collected
cases share inherited neural/catalogue/archive fixtures, parameterize mutations and use
one crash driver for four commit windows. No stale behavioral regression was established
that justified deleting an old case just to lower the count.

This is net growth for a new source-authorized feature, not a claimed code-size reduction.
The 46 runtime deletions replace narrower legacy-only branches with shared version-aware
paths; they do not remove distinct behavioral protections. Repeated source checks near
publication remain intentional current-use guards, not caching targets without evidence.

Machine-readable file additions/modifications and exact before/after accounting are in
`audits/persistentstate001/CHANGE_ACCOUNTING.json`. The static dependency checker passes
but is not a proof that all dynamic calls or external integrations are safe.
