# REHEARSE01: preserve the admission stop and development signal

Start with REPORT.md, STATUS.json, analysis/DEVELOPMENT_SUMMARY.csv, analysis/DEVELOPMENT_CONFIDENCE_DIAGNOSTIC.csv, and raw/primary/A0_AND_GUARDS_LOCK.json. This packet is a review handoff, not authority for a new run. The compact packet is not the full raw archive.

## Actual disposition

Execution v0.2 / scientific protocol v0.1 stopped at A0. All eight G/L fits met 8/8 old inventory and B1≥16/20, but G met the normalized learning-gain condition in only 2/4 fits; L met it in 4/4. Each group required three fits. G's B1_K/N_K counts were (10,9), (8,6), (10,6), and (8,0) on twelve fixed focal opportunities. H was 3,6,6,12. The first two recovered one-third of available frozen errors, below one-half. Unlike PROTECT01, no fit had zero headroom or an impossible threshold. No held-out map or stream was generated. Do not waive the gate, select different seeds, or train longer under this closed run.

## Development findings, not confirmation

Each first-correction cell is four bases × four fits. G B1/U/F/R scored 4/16,16/16,16/16,16/16; L scored 5/16,16/16,16/16,16/16. U/F/R had identical parameters before the extra step.

Old-record rehearsal R reduced immediate mean old loss from .022229 to .013178 for G and .049394 to .016503 for L. Extra focal practice F increased it to .070237 and .072631. R retained all 512 repeated old-class observations per method over four tail checkpoints. G-U retained 509/512 and G-F 507/512; L retained 512/512 in every branch. No old class was wrong immediately before the extra update, so this is probability-quality recovery and later retention, not resurrection of an already-lost class label.

R still exceeded the calibrated old-confidence envelope in 2/16 G and 5/16 L development base/checkpoint cells. Keep those deviations visible; do not convert the favorable average or perfect class count into a held-out pass.

## Mechanism and evidence

Every batch recomputed eight examples at the same post-clip2 weights, took the ordered float64 mean of captured float32 gradients, cast once, clipped once, and applied once. F's repetitions average to one gradient; all eight computations were charged. L used its own local derivative for old examples. The buffer contained the complete fixed set of eight old records. Each environmental receipt was consumed once; replay had its own application/version record.

All preflight, cost probes, eight fresh 100-update initial fits, and all 32 development contexts were executed and then repeated in a fresh adaptive replay. Total: 3,576 updates/commits, 91,896 cells, 28,392 heads, 2,524 G backwards and 2,524 local gradient examples. Replay matched 19,428 frames, 61,150 arrays, 14,577,108 elements, and thirteen final audit/score files. All 2,046 incorrect rows among 13,220 primary query/diagnostic rows remain. No old model was loaded, no fit retried, and no scientific source or gate changed after results. Native/backing-memory accounting remains limited; no efficiency claim.

## Program and next review

The user wants to return to the skipped NBR-01 question after a qualifying pass instead of advancing stages without Codex. The exact ticket was not named; RET-MW01-FIT-001 is the explicitly parked derived-progress line, distinct from the original Q010 public-input identity proposal. No subsequent experiment was dispatched. NBR-01 stays bounded-closed; NBR-02 active; dream maintenance deferred; FCR-0103-001 and all G01–G22 remain attached.

The next design review should separate baseline competence from the first-reversal recovery that the intervention is intended to improve. Is A0 measuring a necessary prerequisite, or demanding too much of the deliberately slower reference? Preserve this real shortfall either way. Separately address the remaining confidence deviations. Return a single justified prospective plan, not retrospective qualification or another blind fit campaign.
