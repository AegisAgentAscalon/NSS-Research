# CM-02 v0.6 retained metrics check

Recomputed from the archived main decision, exact-control, family-paired, memory/read-work and event-work CSVs. The archive was read-only; no model, scorer or source module was imported or run.

## Main and heldout scores

The main decision table has 2,880 rows. Heldout W and I each score 391/600 and O scores 307/600. The denominator is 120 heldout query occasions repeated across five frozen reader seeds: 20 sequences and five families, not 600 independent episodes. W/I decision fields match on 960/960 paired rows, with 0 mismatches.

Exact retrieval controls are run once per occasion:

X_I: 100/120; X_S: 100/120; X_W: 100/120; X_latest: 105/120.

Family-level heldout W/I/O counts and W–O differences are in `metrics_summary.json`; the W–O difference is positive in each of the five families.

## Retained failure strata

At F:16, W and I each score 0/25 and retain safe-but-lost-recall flags; at F:48, W/I score 25/25. C:32 W/I score 12/25. N:16 and N:32 together produce 10/50 correct W outcomes, while hidden-intent-wrong-binding flags remain retained. These diagnostic rows are not an overall pass/fail gate.

## Measured W/I work

The totals below combine heldout event work with query work for representative reader seed 1201. Object-graph byte observations are reported as mean/max and peak transient graph; they are not summed as simultaneous resident memory.

W: 2,800 event+query index reads, 170 event packet encodes, 250 event+query decodes, 4,420 semantic-field bytes rewritten, 9,520 ASCII bytes rewritten; I: 2,800 event+query index reads, 0 event packet encodes, 0 event+query decodes, 4,420 semantic-field bytes rewritten, 0 ASCII bytes rewritten.

Across heldout query observations, mean/max resident graph was W 117,407.72/183,508 bytes and I 117,440.47/183,532; peak transient graph was W 169,155 and I 168,945 bytes.

The archived report identifies zero training updates and describes internal exact replay; this table check is not an independent scorer rerun or third-party replication. Repeated query measurements across five fixed seeds are not independent episode samples.
