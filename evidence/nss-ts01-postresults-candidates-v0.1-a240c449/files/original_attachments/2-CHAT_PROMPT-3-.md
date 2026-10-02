# Codex handoff — TS01 completed; maintained management-token concept preserved

Review NSS_TS01_Execution_v0.3, beginning with REPORT.md, STATUS.json, MAINTAINED_MANAGEMENT_TOKENS.md, the frozen v0.2 scientific protocol, execution source lock, and complete scores. This handoff requests analysis and the next proposed specification, **not another training run**.

## Completed evidence

Five new 14,985-parameter GRU+head fits each completed exactly 2,000 prescribed Adam updates. The fifteen historical Q010 exports were untouched and received zero TS01 forwards. TS01's 10,000-update/4,099,712-cell-reservation ledger is separate from CM-02's closed 5,995-attempt history.

CARRY and PREFIX_REPLAY each scored 120/120 held-out joint successes for each of all five fits: 600/600 readouts across 120 unique query occasions. ZERO_EVERY_EVENT scored 40/120 per fit, 200/600 overall. EXACT_STREAM scored 120/120 unique occasions. All five family CARRY-minus-ZERO differences were positive. CARRY had zero raw wrong-DONE assertions at all 75 forced-revocation assessments and no held-out auxiliary errors across 13,000 related bank/event observations. These are repeated observations on five small procedural families, not hundreds of independent tasks or a broad safety guarantee.

Carry/prefix states and logits are bit-identical. Main fresh-process replay matched 2,144 arrays / 12,888,000 elements; the separate untrained fixture matched 60 arrays / 322,616 elements. Independent scoring uses Boolean-list truth and float64 NumPy GRU/head reconstruction, not producer/model logic. The empirical rounding tolerance is the unchanged 2e-6 + 2e-5*abs(reference); it is not Q010's underflow verifier. Fresh evaluation replay is not repeated optimization or third-party replication.

Every training event and batch trace is retained, along with 45 full model/optimizer/RNG/cursor checkpoints. An independent audit reconstructed all 160,000 episodes and 4,000,000 targets from their frozen recipes and checked checkpoint/input hashes, but did not repeat the 10,000 updates. The 12 duplicate excess normalized training streams remain retained. Full main/fixture rows, 655 main ZERO query errors, 63 untrained-fixture query errors, and all auxiliary negatives remain available.

## Interpret the result narrowly

This is learned progress maintenance inside supplied exact routing: two protected task banks, public task addressing, labeled distraction/no-op filtering, and read-only query behavior are provided by software. RESET is genuinely a learned input, not an external hard zero for CARRY. The task contains only eight completion bits; exact streaming is perfect with one packed progress byte plus ordinary metadata/archive costs. The learned state uses 512 bytes and 59,940 weight bytes. This is not storage compression or an efficiency win over the exact algorithm.

For the specified query schedule, one main-model CARRY pass uses 1,612 actual recurrent transitions versus 4,303 for PREFIX_REPLAY. Keep that recurrence/reconstruction trade-off distinct from a wall-clock speedup claim and count auxiliary heads, archive construction/scans, weights, state, training and verification work honestly.

## Explicit user direction: maintained management tokens

The intended NSS architecture shifts context tokens from primary information storage to a **supporting role in information management**. The goal is less dependence on a growing transcript, **not zero tokens**.

Preserve the proposal for a small, bounded, **always-resident management workspace** alongside richer recurrent state and exact persistent evidence. Reuse its slots rather than append a history. Candidate contents include current goal/task/scope, constraints, candidate/confirmed references, evidence revisions, unresolved issues, and update/recovery instructions. Necessary short facts or intermediate results may also be present. Retrieved evidence can temporarily exceed this resident budget if its traffic and compute are counted.

Distinguish residency from consultation and rewriting. A workspace can remain available at every active recurrent step while changing only at appropriate observed events. Its symbols are interpreted by a controller/model; the symbols are not autonomous processes. Native discrete tokens, a fixed byte/control grammar, and soft embedding slots are different representations with different costs.

**TS01 has NOT tested that maintained workspace.** Immediate event one-hots are not the persistent management channel. Neither the CM-02 string/index tie nor the TS01 state-only success settles whether token-conditioned recurrent updates will help.

## Next proposed specification, without automatic execution

Develop one bounded, resource-matched recurrent-plus-maintained-workspace candidate. Define a real native interface/update rule, vocabulary or tokenizer and embedding cost, state budgets, workspace acquisition/update policy, and permitted observations. The manager must not receive hidden correct progress, future events, evaluator labels or a gold binding. A self-generated “verified” marker is not a grounding test.

Use the successful TS01 fits as retained baselines, not permission to silently tune them. Compare recurrence alone, the same added capacity allocated as ordinary state, the same information in structured fields, and meaningful state/workspace removal. Keep exact streaming and equal-information replay as strong controls. Relevant hypotheses include selective writes, stable/scratch workspace sections, correcting derived progress when evidence changes, and smaller recurrent state at matched total working memory. An eight-bit toy alone cannot justify broad efficiency claims; any task expansion must be predeclared and bounded rather than chosen after inspecting held-out scores.

Freeze the next source/task/split/seed/training/resource/scoring protocol before seeking a separate execution instruction. No automatic scale-up, additional fits, CM-03–05 launch, role replacement, or Forge/Runtime integration. Preserve the Primary, Secondary, Tertiary and Validator architectural roles and all Q010 historical evidence gaps.

## Package use

The archive may losslessly deduplicate identical files and two redundant hash-count tables. Run `python RESTORE_EVIDENCE.py` and then `python VERIFY_STUDY.py`. Restoration recreates retained bytes, not neural data. `python RESCORE.py --output /new/audit/path` recomputes independent scores without neural forwards. Old Q010/CM archives are not required for this new numerical scoring; they are only historical provenance references. Do not reset or extend archived execution ledgers.
