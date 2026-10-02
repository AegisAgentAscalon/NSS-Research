# Codex handoff — TS02-MW01 completed; scientific screen failed

Review **NSS_TS02_MW01_Execution_v0.2**, beginning with REPORT.md, STATUS.json, ARCHITECTURE_EVIDENCE_UPDATE.md, and the untouched scientific protocol/source lock. This asks for analysis and one narrowly specified next proposal, **not another training run**. Keep earlier Q010/TS01 models and closed ledgers untouched.

## Actual results

Fifteen new main fits (R/R+/RW × five, 1,000 updates each), plus three fixed 100-update cost probes completed: 15,300 total updates. No sweep, selected checkpoint, extra fit, or retry. All terminal hashes were locked before concrete main evaluation streams were generated. The 120 held-out occasions across 20 sequences/five families were repeated with five fits; these are not 600 independent tasks.

| CARRY configuration | Held-out joint correct |
|---|---:|
| R | 507/600 — 84.50% |
| Larger R+ | 496/600 — 82.67% |
| RW | 526/600 — 87.67% |

RW is +3.17 points over R and +5 points over R+ pooled. Its per-fit counts are **96, 113, 112, 108, 97 / 120**: only three fits reach 90%, versus four required. RW−R reaches five points in only one family; RW−R+ does so in four. The known-repair subset gives R=76/125, R+=79/125, RW=79/125. There is no repair gain over R+.

RW made **75 invalid/stale revision claims out of 1,200 group predictions** and **17 wrong-DONE assertions at 100 designated assessments**. Both targets required zero. Exact structured S and packed X each score 120/120 unique held-out occasions with correct bindings. The scientific screen **FAILED**, despite completed engineering checks. Do not rename the pooled gain a pass.

RW slot masking gives 366/600 (61%); erasing learned state before every event gives 38/600 (6.33%); prefix replay gives 526/600 with exact carried states/logits. Masking supports dependence on the maintained embeddings, not fair capacity-matched superiority. R+ has greater state and parameters, but is not exactly matched for compute or optimization difficulty.

## Most informative post-result finding

Retained training and probe labels never have **both evidence groups valid at revision 1 together**. Held-out E:32/E:48/E:64 do. All 75 RW invalid claims occur at those 15 unique occasions × five fits: predicted bindings (1,0) versus gold (1,1), despite correct resident metadata.

All configurations score 0/25 at E:32. At E:48 and E:64, progress plus next action is 25/25, but the raw revision claim remains wrong. This is a verified coverage pattern and post-result association, **not proof of causality or permission to repair this run**. The no-model `post_analysis/analyze_retained.py` reproduces the analysis from retained arrays.

A focused next proposal should separate compositional coverage, copying legitimate exact metadata, learned derived-state repair, and raw claim fidelity. A future exact revision-output path may be good engineering, but does not retrospectively qualify these learned heads. Do not add updates until known held-out cases pass. Require fresh splits/seeds, predeclared rules, and strong exact/R/R+ controls; keep the intervention bounded.

## Maintained management tokens and architecture

Preserve the user's direction: **bounded resident context supports information management alongside richer recurrent state and exact evidence**, reducing transcript reliance rather than eliminating tokens. Residency, consultation and rewriting are distinct.

This experiment realizes **ST-04 → IF-02 → ST-02** with five categorical fields per task (goal, left revision/status, right revision/status), ten uint8 IDs and an 18×4 learned embedding. A deterministic lawful-event writer supplies these fields, never completed milestones or gold actions. Query heads read recurrent state only. The contribution under test is native learned conditioning, not an autonomous writer or another string/index comparison.

Attach **AER-TS02-MW01-001** to proposed **ACP-TS02-MW01-001**. The parent Architecture Ledger v0.1 is unchanged. Do not adopt the study's exact dimensions/vocabulary as production canon, or confuse the software authority checker with the fallible advisory neural Validator. Preserve frozen Primary, alternating Secondary/Tertiary, overlay removal, Segmented Context/HSA/MSA, DARP, Forge/Runtime and generation policies. No shared-state routing, learned writer, soft-slot, precision, or consultation-cadence study ran.

## Evidence and limits

All 40,800 separately allocated main/probe public streams are retained, with 120,000 main and 2,400 probe presentations. There are 75 main and six probe full model/Adam/RNG/cursor checkpoints. Independent input/target/route/checkpoint auditing did not repeat optimization or stochastic generation. Two excess normalized duplicates remain. Lack of complete-stream overlap does not establish broad distribution independence.

The 9,600 main learned rows retain 4,108 joint errors and 963 invalid group claims; their union contains 4,717 negative rows. The 240 fixture rows retain 238 joint errors and 239 invalid group claims. All auxiliary scores, raw states/logits, and negatives are retained.

Fresh main replay matched 17,120 arrays / 10,019,920 elements; fixture matched 428 / 250,498. Fifteen score files per split match. This is internal, same-runtime verification, not third-party or cross-device replication. The empirical NumPy tolerance is `2e-6 + 2e-5*abs(reference)`, not Q010's underflow amendment. Evidence aliases are created only after actual recomputation/equality checks, never used as inference caches.

Reservations: 4,836,256 cells; 9,212,000 heads; 15,300 backward and optimizer attempts. Actual dispatched cells: 3,681,666. Historical archives remain byte-identical. One upstream aggregate seed digest has unspecified serialization and was not matched; all 216 direct and 40,800 episode label-derived numeric seeds were verified. Do not claim the opaque aggregate was verified. Historical Q010 optimizer/RNG/raw-trace and reconstructed-underflow limitations remain unchanged.

After extraction, run `RESTORE_EVIDENCE.py`, then `VERIFY_STUDY.py`. A rejected 80 MB per-file ZIP is documented; the final whole-payload compression format restores every canonical file, with no dropped evidence. `RESCORE.py --output /new/external/path` independently scores without model calls. Old archives are provenance, not numerical dependencies. `REPLAY_EVALUATION.py` is an optional, explicitly requested future reproduction and must not reset this closed ledger. Preserve all scientific failures and source identities.
