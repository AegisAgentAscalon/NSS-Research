# C00-CONTRACT01 — change/review contract conformance
## Execution specification v0.1 | 25 September 2026

## Authorization and precedence
The user instructed “All right, let's run it” following PLAN-NSS-CONTRIBUTIONS-001.
This implements only Contribution 00's minimum ordinary rule, evidence/change record,
and simulated adoption lifecycle. It does not authorize the full roadmap. Source basis:
STEP_00_CONTRACT.md §§A–G and CONTRIBUTIONS.md §§0–1. The former leaves operational
limits open; the choices below are explicitly new engineering completions, not values
inherited from the source or approved safety standards.

## Question and scope
Can the concrete rule and append-only record faithfully implement a caller-specified
old/new behavior contract, preserve unresolved cases, and distinguish review from
actual simulated adoption? This is deterministic conformance/fault testing, not a
learned-review comparison, training study, neural repair, or generalization benchmark.

All candidate behavior is AUTHOR-CONSTRUCTED SYNTHETIC EVIDENCE. A fixture artifact
contains an explicitly specified table of binary probabilities, represented as integers
0–1000. It is not a model, a model prediction, or a trained parameter checkpoint.
Labels/requirements are public fixture receipts. No historical score or threshold is
changed. No inference, gradients, optimization, random data draws, or self-play occurs.

## Selected first-domain contract
An accepted opaque parameter-revision ID, a stable epoch anchor, a candidate artifact,
current public receipt revisions, and a finite declared capability panel are represented.
Three old capabilities remain current; one focal target is legitimately corrected.
The previous focal label is historical, not a protected current target.
Binary class ties select zero. A correct-target probability is obtained directly from
p(class 1), without interpreting synthetic probabilities as calibrated uncertainty.
The reviewer has complete fixture evidence for this finite public panel only.

Only PUBLIC snapshot fields reach the reviewer. No expected decision or private extra
capability is available to the rule. The reference evaluator is separately implemented
and imports no production decision/journal/generator module.

## Caller-specified policy, not operational qualification
Each fixture supplies minimum focal target probability, per-record minimum old target
probability, per-record maximum decrease from the rolling parent, and maximum decrease
from the fixed epoch anchor. All are inclusive integer boundaries. Zero tolerance is
allowed in a fixture but is not the recommended production policy.
The default illustration is focal minimum 850, old minimum 600, parent decrease at
most 50 and epoch decrease at most 100. These mean 0.85/0.60/0.05/0.10 on the chosen
synthetic 0–1 scale. No real-world safety or confidence calibration is implied.
No average across capabilities can hide a required record's violation. Epoch reference
is not silently reset on adoption. A legitimate revision to an OLD protected target
requires explicit requalification; this pilot defers instead of inventing migration.

## Review decisions
REJECT: structurally invalid input, fabricated/untrusted artifact evidence, unsupported
authority or hypothetical-as-observed provenance, missing required permission,
wrong domain, candidate identity/content mismatch, or invalid numeric bounds.
DEFER: missing measurements, incomplete or unknown update completion, future/unreleased
or superseded evidence, stale accepted-parent/epoch/schema version, incompatible live
state, unresolved pending trace, or failure of current focal/old behavior requirements.
ADOPT_ELIGIBLE: all finite-panel integrity, current evidence, and behavior checks pass.
This is permission under the fixture's rule, not actual adoption. A separate commit
operation rechecks parent/evidence/epoch and the review fingerprint against current
public state. Direct adoption of an unreviewed candidate is not permitted.
Policy refusal is not successful neural learning. Invalid or unresolved evidence is
not a proven behavioral failure. Never-adopt and accept-all controls are reported by
separate true-failure categories, with no statistical generalization inference.

## Availability, repair, and review coverage
A clock in integer public ticks is supplied, not measured real service latency. A review
is on time when tick <= deadline. Late evidence may become eligible, but the original
overrun stays recorded. A permanent deferral becomes overdue, never success.
No repair is actually executed: a changed candidate with repaired fixture evidence is
an independent synthetic artifact. Old raw candidate data and failed decisions stay.
An accepted revision can be kept while a proposal is pending; this does not prove the
system serves the corrected answer. Simulated served revision IDs are recorded.
A contiguous dream-review accounting cursor may advance over explicitly reviewed
unresolved items, never over gaps. Accounted and resolved are distinct; no Tertiary is
instantiated. Rejected/deferred items remain accessible for later review.

## Frozen fixture inventory and primary counting
Grid: 3 parent tolerances {0,50,100} × 2 epoch tolerances {50,100} × 3 focal
probabilities {600,850,950} × 5 old probability drops {-25,0,25,75,150} × 2
parent-to-anchor gaps {0,50} × 2 old labels × 2 new focal labels × 2 completion
states {committed,unknown} = 1,440 cases. Each uses three explicitly identical old
scores; separate corner fixtures exercise unequal records, boundaries and faults.
44 named corners and 14 lifecycle scenarios are listed literally in the locked source, with
counts asserted before running. No seeded sampling, selection, tuning or held-out split.
Every fixture is an exposed contract test; agreement is not scientific holdout accuracy.
Two public-identical/private-opposite-acceptability cases illustrate incomplete panel
coverage. Their different labels never enter the operational reviewer, and no refusal
or acceptance policy can classify both from the common envelope.

## Recording and independent checks
All source/configuration files are hashed before case generation/execution. Each raw
review has an operation ID, input hash, explicit reason codes, decisions and metrics.
The journal uses canonical JSON hash chaining, fsynced intents, and commits. A commit
must name the applied immutable candidate and match its durable state. A crash after
intent before acknowledgment freezes automatic recovery as UNKNOWN_COMPLETION; both
'not applied' and 'applied but no acknowledgment' are deliberately exercised.
Hash chains detect altered content, gaps, reorder and duplicates; an externally retained
terminal count/hash is needed to detect a truncated suffix. Both limitations are tested.
These are integrity checks, not cryptographic authentication or crash-proof guarantees.
The worker is not a security sandbox; information-isolation claims are limited to the
actual public argument interface and identical-input paired probes.

## Success/stop and budget
Every mandatory conformance, independent reason/decision, ledger, current-source
recheck, integrity, and deterministic fresh-process replay check must pass. Expected
REJECT/DEFER, transient synthetic harm, invisible off-panel harm and unfinished review
are outcomes, not engineering failures. Unexpected mismatch stops that version; preserve
its attempt and do not silently tune to the case. Fixes require a new source version and
fresh execution with all failures retained. No scientific admission or statistical PASS.

Hard cap: 10,000 rule evaluations over primary/replay/technical probes; 500 lifecycle
operations; zero model loads/forwards/gradients/optimizer applications; 30 minutes from source lock (earlier document/code preparation is not continuously timed); 1 GiB worker RSS; 64 MiB output and 16 MiB delivery. Execution and
verification are charged separately; counters and elapsed time are retained. Replay
runs fresh processes from empty directories. Relocation rescoring reads retained values
only; no third model run exists. The final ZIP is tested and its payload manifest verified.

## Scope boundary
This validates a deterministic implementation of a defined policy on author-constructed
cases. It does not prove a useful harm tolerance, optimal reviewer, learned token benefit,
serving deployment, autonomy, recurrent-state migration, plasticity or training recovery.
Private candidate outcomes remain distinct from simulated accepted/served revisions.
No formula can guarantee an unobserved skill from this complete-but-tiny public panel.
NBR-01 remains bounded-closed; NBR-02 active, other experimental dispatch paused.
