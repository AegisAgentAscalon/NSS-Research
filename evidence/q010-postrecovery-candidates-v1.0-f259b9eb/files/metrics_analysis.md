# Q010 v1.6 retained metrics analysis

This is a deterministic count-and-rate recomputation from retained CSV rows, not a new inference run. The archive and all of its members were read-only.

## Recomputed cross-checks

`ALL_QUERY_SCORES.csv` contains 449,640 reader-query outcome rows across 64 conditions, 5 seeds and six reader roles (1,920 unique condition-seed-role cells; 320 condition-seed pairs). `FROZEN_GATE_CHECKS.csv` contains 1,494 rows. The three candidate arms each have 83/83 checks in every seed and 83/83 pooled, matching `STUDY_RESULT.json`.

The 133,658 incorrect outcome rows match the study result's retained-negative count. Their evidence classes are: under_depth 32,640; unobservable_missing 19,590; observable_missing 5,225; supported 73,001; preexisting_unknown 3,202. This is an outcome-row count across readers, not a count of unique inputs or candidate-gate failures.

The result JSON reports 3,045,480 logical stage audits. That value is not re-derived from the selected score and gate tables; this review did not open stage-level captures. The result's 83-check-per-seed/pooled gate claims and 449,640 query count were checked directly against retained rows.

## Scientific signals outside the frozen gates

- Close-source supported queries: ordinary 199/320; near 229/320; attention 168/320; inherited/cap-only 198/320 each; exact-owner 320/320. Near exceeds ordinary in all five paired seeds (per-seed gains: +13, +7, +3, +4, +3 of 64). It still gets only 0/640 near-collision novel queries labeled UNKNOWN; exact-owner gets 640/640.
- At coded condition `core_assisted_l08_d01`, under_depth diagnostic accuracy is 0/320 for every role; `core_assisted_l08_d08` supported accuracy is 320/320. Each seed has the same 0/64 versus 64/64 pattern across roles.
- State-off supported queries score 0/320 for each role. With cadence 08, supported durability rows are 5440/5440; cadence 32 falls to 5414/5440. At event 1,024 without maintenance, ordinary/near/attention are 0/320, 0/320, and 0/320.
- Erased-value support is 143/320 for every role; wrong-but-valid support is 165/320 for every role. These equal marginals do not establish that the same individual queries failed. On altered-known stress, near gets 299/640, ordinary 96/640, and attention 109/640.

These denominators are query outcomes pooled over five paired seeds; the five seeds, not hundreds of query rows, are the model-level replication count. Candidate gate passage therefore does not establish broad close-identity admission, corruption tolerance or no-maintenance durability.

## Evidence boundary

The package report says no optimizer update or fresh training reproduction occurred, and `STUDY_RESULT.json` records the training audit as incomplete. Full main numerical training traces and full optimizer/RNG checkpoints are unavailable. This compact RecoveryContext package omits raw main-capture trees; the recomputation covers its retained score summaries only. It does not rederive the reported 3,045,480 logical-stage audits or constitute independent inference or third-party replication.

Primary members: `Q010_InferenceRecovery_v1.6/REPORT.md`; `Q010_InferenceRecovery_v1.6/results/analysis/STUDY_RESULT.json`; `Q010_InferenceRecovery_v1.6/results/analysis/ALL_QUERY_SCORES.csv`; `Q010_InferenceRecovery_v1.6/results/analysis/FROZEN_GATE_CHECKS.csv`; `Q010_InferenceRecovery_v1.6/results/analysis/METRICS_ALL_SEEDS_AND_POOLED.csv`; `Q010_InferenceRecovery_v1.6/results/analysis/WHOLE_MAP_DIAGNOSTICS.csv`.
