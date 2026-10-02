# NSS TS03-CR01 — controlled composition exposure and raw-output fidelity
## Completed execution v0.4 / reviewed scientific protocol v0.2

**The experiment completed; D1 coverage-effect, D2 workspace-configuration interaction, and D3 absolute-reliability screens all FAILED.** The additional final-level advantage criterion also failed. Engineering, independent semantic/numerical scoring and fresh evaluation replay passed. This is not an omnibus PASS.

The controlled C1 curriculum helped the recurrent-only controls on the primary repair set, but did not improve RW: its joint repair score decreased and its already-perfect binding score stayed perfect. Correctly reporting current metadata was not sufficient to report correct derived work. The prior TS02-MW01 failed screen remains failed; these are new fits, curricula, evaluation streams and budgets, not a repair or re-score of its checkpoints.

Execution clock began 2026-09-25T02:06:04.139038+00:00; date is the measured host UTC, not an assumed user-local date.

## 1. What changed, and what did not

Two curricula were crossed with R, larger R+, and native maintained-workspace RW. Four paired fits per cell produced **24 new main models**, each trained for exactly 800 updates. Six new, discarded 50-update cost probes bring total optimization to **19,500 updates**. No main checkpoint was selected for performance: only step800 was evaluated. Within each architecture/fit pair, C0 and C1 initial parameter tensors and fresh optimizer states were identical. Historical Q010, TS01 and TS02 models were not loaded, forwarded, trained or modified.

C0 included separate source revisions but not jointly valid (1,1). C1 re-paired whole right-source histories in an eight-slot block, adding (1,1) and compensating (0,0) exposure while preserving each source's marginal history, revisions/status, receipts and group targets at every absolute prefix. It is a controlled joint-support redistribution, not a literal single added tuple with nothing else changed. C0 is not a rerun of the old TS02 curriculum.

Both excluded (1,2)/(2,1) in training and probes; development and the fixture also avoided them. The reserved asymmetric family is therefore a genuine unseen-combination stress test under this support contract. Neither metadata support nor equal marginal counts guarantees adequate training of every ordered progress transition.

R has14,620 parameters /384 recurrent bytes; R+20,428 /480 bytes; RW17,572 /384 bytes plus ten uint8 IDs and an18×4 learned embedding already included in its parameter count. RW uses five field-typed metadata slots per task. Its recurrent update consumes their embeddings; **heads read h only**. The packet contains no completion stamps or correct next action. Public authority checking, legal metadata writing, protected bank routing and no-op filtering are supplied code. Public RESET is learned; episode initialization clears state. No direct metadata-to-head bypass or output repair was added.

The models and event/authority rules are the pinned TS02 implementation, copied as source and verified by hash. Exact structured S and packed X controls track completion stamps and metadata directly. Their perfect performance does not qualify the neural solution or demonstrate compression.

## 2. Held-out task and binding results

| Architecture | C0 joint J | C1 joint J | C1 − C0 J | C0 both bindings B | C1 both bindings B |
|---|---|---|---|---|---|
| R | 124/320 (38.75%) | 139/320 (43.44%) | +4.69 pp | 152/320 (47.50%) | 194/320 (60.62%) |
| R+ | 95/320 (29.69%) | 119/320 (37.19%) | +7.50 pp | 137/320 (42.81%) | 193/320 (60.31%) |
| RW | 144/320 (45.00%) | 139/320 (43.44%) | -1.56 pp | 236/320 (73.75%) | 224/320 (70.00%) |

Each cell is **80 held-out occasions × four fits =320 readouts**, not320 independent tasks. There are16 held-out sequences in four stress categories, plus8 development sequences/40 occasions. Every sequence has65 events after an11-message prelude; readouts follow events0,8,16,32,64. The stress categories are not IID samples from a broad task population. J requires all four milestone categories and next action correct. B requires both raw evidence-binding categories correct; J alone does not certify provenance.

These figures must not be compared directly with TS02's87.67% as a degradation of the same models: all models, training recipes, split, duration and chronological tests here are new. The controlled causal comparisons are C0 versus C1 within this study.

## 3. Primary repair contrast and frozen decisions

P comprises the three non-asymmetric held-out families at events16,32,64:36 unique occasions,144 readouts per cell.

| Architecture | Joint repair | Change | Both bindings | Change |
|---|---|---|---|---|
| R | 37/144 → 49/144 | +8.33 pp | 82/144 → 128/144 | +31.94 pp |
| R+ | 20/144 → 35/144 | +10.42 pp | 53/144 → 113/144 | +41.67 pp |
| RW | 58/144 → 51/144 | -4.86 pp | 144/144 → 144/144 | +0.00 pp |

**D1 FAILED:** RW loses7/144 joint successes (−4.86points); its binding score is144/144 in both curricula. No paired fit or contributing family improves both metrics. The binding-gain requirement has a ceiling in this realized baseline, but the joint score also declines, so the negative result is not only an unattainable binding margin.

**D2 FAILED:** relative to R, the RW coverage response is−19 joint successes and−46 binding successes; relative to R+, −22 and−60, respectively, on the common144 denominator. This does not support a workspace-specific benefit from this curriculum intervention.

**D3 FAILED:** C1-RW fits achieve34,36,34,35 out of80; zero of four reach the required72/80 floor. They make96 invalid raw USE revision claims across640 group predictions, and6 designated wrong-DONE assertions out of128 designated readouts. There are102 total binding errors when erroneous UNRESOLVED predictions are also counted. Across all320 held-out readouts, wrong-DONE occurs60 times, including unresolved-evidence contexts outside the designated subset. No raw mistake was removed by the shadow filter.

**Additional final-level advantage FAILED:** C1-RW gains only2 joint successes over C1-R on P (51 versus49/144), below the required8. It does outperform C1-R+ on P, but the rule required both controls. Its final pooled joint level ties R at139/320. A relative score advantage over only one opponent is not qualification.

## 4. Where the combined system still fails

On P, **both RW curricula report current evidence bindings correctly on144/144**, yet C1-RW reports correct progress and action on only51/144. Milestone-vector correctness declines75→67/144 and action correctness91→86/144. Thus the organizer's current metadata can be reflected in one head without reliable derived-work outputs. This does not prove that only a particular hidden transition or decoder is defective; jointly trained state and heads remain confounded.

At the initial held-out checkpoint, C1-RW gets64/64 readouts correct. At event64 it gets0/64 joint readouts correct, although48/64 binding pairs are correct. This is a chronology-and-state stress result, not an isolated measurement of time decay. The two recurrent controls also encounter major failures. A toy exact algorithm handles every tested prefix correctly.

On the reserved asymmetric repair positions, C1-RW obtains16/48 joint successes, **0/48 correct binding pairs and0/48 all-head successes**. On all asymmetric occasions it obtains32/80 J and19/80 B. Learning the individually observed revision values did not provide the desired transfer to their unseen combinations. Both evidence-order orientations and all fits remain in `ASYMMETRIC_TRANSFER.csv`.

A post-result, non-neural support audit found that every C1 primary repair query/fit pair had its metadata-plus-gold-milestone state represented somewhere in that fit's own training prefixes (minimum21, maximum4,439 prefix occurrences). This is not a causal explanation: matching a target state does not match the required transition or ordering history. It does make the simple claim “that target combination never appeared anywhere in C1” inaccurate. The diagnostic is labelled exploratory and did not change data, targets, models or gates.

## 5. Channel removal, replay and exact controls

C1-RW CARRY and PREFIX_REPLAY are139/320; SLOT_MASK is105/320; ZERO_EVERY_EVENT is0/320. C0-RW gives144,101 and0/320 for carry, slot mask and state removal respectively. These are same-checkpoint information removals, potentially out of training distribution—not equal-resource superiority experiments.

Both exact S and X controls achieve **80/80 held-out and120/120 all-main occasions**, including bindings. Do not multiply those deterministic observations by the four model seeds. Each model/condition pays for the archive, controller, indices, transitions and readouts; R+ is not an exact FLOP/optimization match. No overall efficiency or compression qualification is claimed.

The shadow check uses public metadata and consistency among the model's own output categories, not hidden progress. For C1-RW it accepts179/320 readouts:121 correct joint outputs and58 remaining joint errors. It blocks all96 occurrences with an invalid USE claim, but still permits10 wrong-DONE outputs. It rejects16 otherwise-correct known-answer outputs (18 correct joint outputs in total, including two UNKNOWN cases). Its121 accepted successes must not replace the raw139/320 score or be described as a learned repair. The check does not influence future state.

## 6. Corpus identity, support and independence

The complete study retains52,000 allocated main/probe wire streams:51,200 main streams shared across architectures and800 cost-probe streams. The corresponding156,000 episode presentations comprise153,600 main and2,400 probe presentations. Independent reconstruction checked **1,878,400 unique allocated-stream prefix targets**, including recreated PCG64 component draws and their saved RNG states. No optimization was independently repeated.

All52,000 full wire streams are unique. After removing opaque IDs and ignored distractor payloads, only12,846 normalized streams are distinct; **39,154 duplicate excess presentations are retained**. Most duplication follows the intentionally weighted/re-paired block. It is not52,000 independent semantic tasks. All24 main normalized streams are distinct and have no full-stream training match; supplemental audits also compare28/44-message prefixes and retained TS02 identities. Different IDs or lengths alone are not evidence of generalization.

The generated-data checker verified469,600 per-component prefix multisets before training; the separate prefit oracle audit reconstructed all event semantics, labels and numerical features. A redundant, independently written exact-byte-prefix multiset audit repeated all469,600 comparisons after main fitting had begun; its timing is explicit. It used no model results or data selection. All support, marginal and authority checks passed. Reserved asymmetric combinations are absent from training/probes/development/fixture.

## 7. Training history and retained failures

All24 main fits and six probes completed their first optimizer schedules. Full checkpoints are retained at0,200,400,600,800 for each main fit and0/50 for each probe: **132 model/Adam/runtime-RNG/dedicated-generator/data-cursor checkpoints**, plus untrained fixture initialization artifacts. Every update records loss, unclipped gradient norm, input identity and parameter digest. Paired initial bytes, checkpoints, cursors and RNG fields were independently checked; this is not a second training reproduction.

Completed main scoring retains **7,155 incorrect joint rows**,3,064 invalid USE claims and their all-head-negative union of7,543 rows, out of9,600 learned-interface rows across all arms and splits. The completed untrained fixture has200 incorrect joint/all-head rows and302 invalid USE claims; poor untrained accuracy is not a fixture failure. All204,288 main and4,256 fixture auxiliary event/bank observations are retained losslessly, with negative-row indices. Repeated seeds, duplicate representations and replay are not new scientific samples.

Execution v0.3 completed an untrained fixture and exact replay, then stopped before optimization when the storage codec incorrectly tried to share identity-dependent lookup-byte costs with otherwise identical numerical histories. Its logs, source lock and fixture evidence are preserved in `attempts/v0.3`. The failed in-memory probe batch had not been written before the exception; its later deterministic reconstruction is explicitly labelled post-stop, not original captured evidence.

Execution v0.4 separated the per-wire lookup-cost lane. Generator, public semantics, oracle, models, training, inference worker and scoring source were unchanged; the new source lock and storage bound were fixed before this version's generation. The fixture was run again and every extra attempted cell/head counted. **No training fit was retried and no held-out result was tuned away.** Original clock and hard limits were retained.

## 8. Numerical verification and resources

Main fresh-process evaluation replay matched **20,544 arrays / 12,916,064 elements**. The v0.4 fixture matched428 arrays / 270,046 elements. Each split's18 independent score files matched byte-for-byte between capture and replay. Public event/route/metadata receipts and deterministic costs also matched; measured timing is not required to be identical. Array aliases are written only after genuine fresh recomputation and exact verification; they restore retained data, not newly invented evidence.

The independent NumPy scorer imports no producer/generator/controller/model code, reconstructs the public history, and checks GRU/head operations in float64 under the frozen empirical tolerance `2e-6 + 2e-5*abs(reference)`. Main checked7,459,584 scalars, maximum tolerance ratio0.143784, with no near-tied query winners. This tolerance is not a proof of a numerical error bound. Q010's +2^-126 softmax amendment is historical and was not repurposed.

| Charged quantity | All attempts | Unchanged cap |
|---|---:|---:|
| Potential cell examples reserved/completed |6,064,000|6,500,000|
| Head vectors reserved/completed |11,708,000|12,500,000|
| Backward updates |19,500|19,500|
| Optimizer updates |19,500|19,500|

Actual dispatched cell examples are4,080,964; the reservation also covers skipped no-ops. Actual head vectors are11,708,000. All extra work from v0.3 is included. Independent NumPy checks and data audits are additional measured work, not neural inference counts.

The shared clock through numerical completion and full training audit was1875.12seconds, including implementation, preparation and the stopped version. Sampled supervisor/process-tree RSS peaked at620,281,856bytes; sampled container memory at1,723,162,624bytes. Both remain below3GiB/3.5GiB limits. Sampling was0.1seconds; brief peaks and the initial pre-supervisor inspection are not fully covered. Supplemental audit processes are covered by the container measurement, not necessarily the main child-tree subtotal. These are not deployment-speed measurements. Final packaging/relocation QA is separately receipted against the same two-hour clock.

## 9. Codex program context and architecture disposition

The handoff explicitly includes **ACP-NBR-CLOSEOUT-001 and the full original G01–G22 revived research-question register**, because Codex had not received that context. The user called the latter “NVR questions”; the recovered source names them G01–G22 under NSS, with the NBR experiment ladder. No separate program is invented.

The closeout is **still proposed, not automatically adopted**. NBR-01's bounded state/depth reference can be considered for explicit recovered-evidence acceptance without waiting for every workspace candidate to pass. TS01 remains a separate successful small learned-state reference; TS02 and TS03 negatives remain negatives. NBR-02 means delayed credit/retention under specified feedback timing and adaptive surfaces—not merely changing an offline curriculum. No NBR-02 experiment or role replacement was authorized here.

`AER-TS03-CR01-001` records the negative coverage/interaction/reliability findings at the existing ST-04 → IF-02 → ST-02 interface. The parent's Architecture Ledger v0.1 bytes are unchanged. Native slots, protected banks and h-only readout remain study-local mechanisms, not production defaults. Learned writing/routing, constrained or metadata-aware readout, factorized state, precision, cadence and scale-up remain separately proposed research.

## 10. Evidence boundary and next interpretation

This result rejects the proposed coverage fix **for RW under this recipe, optimizer, capacity, budget and stress set**. It does not prove that maintained context can never help, nor that training coverage is irrelevant: the recurrent-only controls improved, particularly their binding heads. It does not uniquely locate an internal state-versus-decoder fault.

A next proposal should first separate current-metadata fidelity from derived-progress maintenance and transition/ordering generalization. Direct public metadata readout could remove some provenance mistakes but would not establish repaired work; a filter cannot mask raw errors. Do not simply retrain on these now-known held-out answers or run additional fits under this closed ledger.

Historical Q010 missing full optimizer/RNG/raw training traces, old verifier errors and absent original underflow source/row remain missing. No new records retroactively fill them. The old models are not numerical dependencies for scoring this new study. Internal independent scoring and fresh replay are not third-party replication or independent optimization reproduction.

The delivered archive contains complete completed-run evidence plus retained failed-preparation records, including the explicitly reconstructed—not original—failed batch. Read `README.md`; run `RESTORE_EVIDENCE.py`, then `VERIFY_STUDY.py`. Delivery integrity and relocated rescoring are documented in the external delivery receipt; this scientific report is not a substitute for those checks.
