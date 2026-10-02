# Competing solution hypotheses from retained NSS evidence

These are competing explanations, not findings or an architecture choice. Metrics below are reported results, not new verification. Candidate tests require separate versioned authorization; no execution was performed. This is a local evidence analysis; external literature is outside this bounded assignment.

## 1. STATEBRIDGE continuation loss may arise in the changed recurrent transition

**Hypothesis.** Initial state survives a weight revision, but later recurrent updates progressively misinterpret it. Restricting the update surface may help more than copying only an output layer.

**Support.** STATEBRIDGE01 reports 1,024/1,024 initial changed-stage reads, then 610/1,024 CARRY reads after eight transitions and 670/1,024 after fixed repair. On a separate adequacy screen, repaired CARRY passed 9/32 and REBUILD 1/32. Aggregate B-learning scores favored CARRY, while PINNED preserved old A in 5,120/5,120 and retained an obsolete B answer. The whole-prefix numerical gate failed 11 arrays, so this remains diagnostic. [E19 §§3–7]

**Alternative.** Changed readout mapping, numerical-path error or unsuitable rebuilding may explain some failures; CARRY also exceeded REBUILD on aggregate behavior.

**Minimum test.** After freezing a passing trajectory check, cross copied/changed readout with frozen/adaptive recurrent weights. Score old A and new B on carried and rebuilt states, preserving original CARRY, REBUILD and PINNED controls.

**Falsifier.** Under valid numerics, freezing recurrence does not improve carried-state A, while copied readout alone explains recovery—or neither factor predicts failure.

**Cost.** High: paired fits, multiple state branches, full trajectory evidence and separate old/new gates are needed.

## 2. Some NBR-02 losses may be direct gradient competition

**Hypothesis.** New and old associations demand opposing updates to shared parameters; a valid correction can therefore harm old margins.

**Support.** REV01 raised first-correction accuracy to 32/32 from 17/32 G and 16/32 L, yet both exceeded old-confidence limits; L also gained five persistent old-label errors. REHEARSE01 retained-data analysis found rehearsal lowered old loss, then the next focal update raised it in every context. TIMING01’s later repair lowered final loss in 30/32 G and 29/32 L contexts, while peak old loss worsened in 25/32 and 31/32. PROTECT01’s first-order constraints did not prevent finite-step margin decline. [E09 §§3–5; E12 §§3–7; E13–E14 §§2–7; E10 §§3–5]

**Alternative.** Small synthetic tasks, different G/L prestates and narrow confidence rules may explain part of the pattern; approximation error is not isolated.

**Minimum test.** On one frozen prestate, compare focal and exact old-example gradients; apply matched-norm focal-only and prospectively defined protected/rehearsal updates. Score new and old labels, losses, margins and transient peaks after each step.

**Falsifier.** Gradient directions do not predict old-loss changes, and the matched intervention neither preserves old behavior nor predicts regressions on held-out associations.

**Cost.** Moderate to high: gradient capture, old-example accounting and multiple checkpoints add computation and storage.

## 3. TS03 fitting and transition composition should be separated from forgetting

**Hypothesis.** TS03’s low task scores mostly reflect insufficiently learned transitions or weak composition transfer; they should not be called catastrophic forgetting. A plausible alternative to placing all progress in a mutable hidden vector is exact typed task state plus a learned reusable transition policy.

**Support.** CKA01 found no competent TS03 checkpoint: C1-RW update-800 endpoint accuracy was 51/256 on sampled actual training episodes and 65/256 on new same-recipe episodes; no fit exceeded 39/80 on the stress panel. The 600-to-800 decline there was just 4/320. Yet TS03 RW binding was 144/144 while derived joint progress fell 58/144 to 51/144, and reserved asymmetric cases had 0/48 correct bindings. This differs from REV01, where previously correct old answers worsened after an update. [E05 §§2–4, 7; E06 §§2–5; E09 §4]

**Alternative.** Curriculum support, supplied writer/routing or the readout may dominate; CKA01’s sampled episodes do not represent all training. Typed state may improve fidelity but fail to generalize.

**Minimum test.** Compare hidden-vector state, explicit fields for task/revision/progress plus a learned transition policy, and an exact tracker on identical streams and budgets. Separate binding, progress and action scores across familiar transitions and reserved compositions. Require baseline fitting before a distinct new-task update arm measures forgetting.

**Falsifier.** Typed state fails to improve binding/derived-output separation, or a competent hidden-state model matches it on reserved compositions and post-update retention.

**Cost.** Medium-high: new fits, compositional splits, exact state validation and a separate retention phase.

## 4. Near-identity errors may be reader-margin failures, not damaged storage

**Hypothesis.** Approximate readers confuse close identities even when owner-keyed storage is correct; better writing or more gating alone will not fix retrieval.

**Support.** Q009 preserved maps at 0.01 separation, yet learned readers reached only about 20% joint correctness on very close families versus 100% exact traversal. Q008 gates reduced ordinary novel false acceptance to 0.43%/0.55% while altered-known accuracy fell to 70.16%/66.93% from 98.85%. Reconstructed Q010 v1.6 reports 0/640 correct UNKNOWN outcomes on near-collision novel queries. [Q008–Q010 history; E00 §§3, 5]

**Alternative.** Synthetic vector geometry, catalogue assumptions and query cleanup may drive this result; it is no general identity/language claim.

**Minimum test.** Hold exact ownership and payload fixed; stratify identity separation and corruption. Compare a learned reader, exact traversal and competent attention under matched information. Score known retrieval and novel UNKNOWN jointly.

**Falsifier.** A learned reader maintains joint known/UNKNOWN performance across held-out close identities without owner or answer labels at inference.

**Cost.** Moderate; several independent identity families and a frozen separation schedule are needed.

## 5. Exact evidence and an ordinary index may beat a learned management lane for factual continuity

**Hypothesis.** A governed archive plus index may be the useful memory layer; a compact packet may serialize the same information without adding a neural capability. One shared backbone could use retrieved evidence without three separate learned cores.

**Support.** CM01’s 56-byte reference mainly helped at high noise; at sigma .01 recall changed 71/100 to 70/100, while exact retrieval scored 40/40. CM02’s packet and ordinary index tied at 391/600 versus 307/600 with no selection history; current-revision retrieval scored 105/120. A 24-byte resident saving brought higher parsing, transient and traffic costs. These were deterministic wrappers, not learned-token trials. [E01–E02; architecture assessment, “Candidate model topologies”]

**Alternative.** Short fixed-record tasks may favor exact software and do not test native workspace writing, multilingual work or a tri-core lifecycle.

**Minimum test.** On longer held-out revision, conflict and resume tasks, compare the same backbone with exact index, compact packet and no-history controls. Match evidence and charge archive, cache, parsing, model, peak memory and resume costs; add multi-core arms only at equal total budgets.

**Falsifier.** A learned workspace or separate role repeatedly improves held-out completion and resumption over the index at equal full cost.

**Cost.** Moderate for one backbone; high for a controlled multi-role comparison.

## 6. Recurrent state may save recomputation without reducing total memory

**Hypothesis.** Carrying state trades repeated work for checkpoint size, validation and recovery burden. A practical design may combine task-local state, exact logs, periodic checkpoints and selective rebuild.

**Support.** TS01 CARRY used 1,612 recurrent transitions versus 4,303 for PREFIX_REPLAY, but carried state used 512 bytes while the exact sufficient checklist fit in one packed byte before metadata. CM02’s small resident saving did not become an overall efficiency win. STATEBRIDGE shows carried state can degrade across weight changes. These are local inventories, not deployed total-memory measures. [E03 §§3, 5; E02 §5; E19 §§4, 6]

**Alternative.** The implementations may have avoidable audit/cache overhead; larger tasks may make replay more expensive.

**Minimum test.** Compare carry, event-log replay and periodic exact checkpoints on one fixed task with interruption and revision changes. Count persistent bytes, full-process peak, recurrent work, validation and resume latency at equal answer quality.

**Falsifier.** Carry lowers complete measured cost and resumes reliably under the declared interruptions and weight revisions.

**Cost.** Medium-high; interruption points and resource sampling cost more than clean accuracy scoring.

## 7. A separate Tertiary and low-bit online traces are not prerequisites yet

**Hypothesis.** A stable serving model, exact records and bounded full-precision candidate learning may provide the needed functions before a learned Tertiary or quantized traces are justified. Test reflection as a selection policy separately from core topology and precision.

**Support.** TEACH01’s fixed teacher discriminator reduced omitted-old mean loss about 13.8% G/15.3% L versus RECENT, but replay and other deep treatments also passed; no-deep reached 29/32, and complete hard records were slightly better. This was a surrogate, not a learned Tertiary. No NSS result tests one- or two-bit traces; no tri-core/shared-backbone winner exists. [E18 §§3–7; G12; architecture assessment, “Candidate model topologies”]

**Alternative.** A trained reflective model may select useful interactions that scripted replay misses on broader tasks; a suitable low-bit update rule may also work. Neither has been tested.

**Minimum test.** First compare recent replay, old-record replay and teacher-guided selection at equal budget across held-out tasks. After selecting a trace rule, compare stored precisions against float32 on decay, accumulation, sign changes and delayed feedback, measuring packed and temporary memory.

**Falsifier.** A learned reviewer adds repeatable net value beyond equal-cost replay while preserving old skills; or low-bit traces match declared full-precision outcomes and lower measured end-to-end cost.

**Cost.** High for longitudinal role claims; moderate initially for trace mechanics, rising sharply with full training and target-device evaluation.
