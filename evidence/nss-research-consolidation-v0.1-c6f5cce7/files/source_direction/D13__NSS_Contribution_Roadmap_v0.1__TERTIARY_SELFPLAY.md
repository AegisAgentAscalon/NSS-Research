# Tertiary as reviewer and curriculum generator
## CAND-NSS-TERTIARY-SELFPLAY-001 · proposed role mapping

Linked tickets: RET-DREAM-MAINT-001, RET-TRAIN-SELFPLAY-001; Contributions 08–09. The user explicitly proposes Tertiary as the other self-play model while dreaming. This is a role proposal, not an implemented mechanism or permission to run pretraining.

## Primary-paper facts (W01, checked 25 September 2026)

*Self-Play Pretraining with Zero Data*, arXiv:2609.30063v1, uses a generator of executable programs and a learner predicting their output bytes. Both are Transformers. The generator's learning signal uses learner-gradient alignment with a parameter trajectory and an AdamW preconditioner; it is not simply rewarded for high learner error. Program replay/mutation supplements fresh generation. Natural data are not used for gradient training, but natural-data validation is used for hyperparameter selection. These are the authors' reported mechanisms, not independently reproduced results here. [W01 §§2.1–2.3,3.1]

## Our proposed mapping, not a paper result

| Function | Proposed NSS responsibility | What is not being claimed |
|---|---|---|
| Retrospective review | Primary + Tertiary examine a fixed change-journal interval and unresolved older issues. | That a deep review automatically knows the causes of every failure. |
| Prospective teaching | Tertiary proposes verifiable exercises/programs addressing skills or learning opportunities. | That imagined claims about the world become true labels. |
| Learner | A separately authorized adaptive learner/candidate consumes an approved generated corpus. A Secondary-like learner is one future role mapping. | That the currently accepted Primary is fine-tuned, or that Tertiary is reduced to only this teaching role. |
| Synthetic environment | Bounded deterministic/stochastic executor plus independently specified semantic checks. | An extra personality/core or a guarantee of factual correctness outside the simulated task. |
| Training feedback | Versioned measurements from permitted learning/development records, available in a later generator phase. | Final-test leakage or self-awarded success. |
| Adoption | Existing governed qualification/runtime path, with advisory Validator input when budgeted. | Generator or reviewer self-authorization. |

This architecture would use existing experience and already trained components. It would therefore be an NSS curriculum/maintenance adaptation, not a zero-natural-data replication. It also does not require adopting Transformer-only internals for NSS.

## Two different dream products

A **retrospective finding** explains or flags something in the recorded past. A **prospective exercise** creates a new practice opportunity. A generated puzzle is not historical evidence. A correct interpreter output proves what that program produced under recorded rules/inputs, not that an analogous unobserved real event happened.

Keep three evidence lanes: actual scoped observations with revisions; executable synthetic exercises with generator/interpreter/input identities; unverified hypotheses. Only independently justified targets enter approved training. Check retention of lawful current corrections so rehearsal does not resurrect obsolete labels.

## Phased self-play rather than concurrent cores

A conservative proposed cycle is:

1. Primary participates with Tertiary; Secondary is inactive. Tertiary examines the allowed learner summary and proposes a bounded exercise manifest.
2. Freeze generator identity, program/exercise bytes, source provenance, task rules, verification outcome and allowed learning budget. Execute generated programs only in the specified limited sandbox; costs and failures are retained.
3. Pause Tertiary. Run the separately authorized learner/candidate phase. Primary continues participating; the accepted serving revision is not silently replaced.
4. End or safely pause that learner phase and record the actual outcomes at exact learner versions. Drain or explicitly handle pending feedback and state.
5. Resume Tertiary with the versioned feedback. Improve future selection, and only through a separately authorized training operation change generator weights. Old failures and rejected material remain traceable.

This phase-separated coupling is our proposed accommodation to Secondary/Tertiary mutual exclusion, not a result established by the paper. It requires explicit data/cost/feedback timing tests. Feedback may be older than the current learner; stamp the identity and do not pretend it describes a newer revision. Adopting changed weights also retains the state-migration obligation.

The paper's optimizer-specific reward cannot simply be pasted onto the present plain-SGD approximate-eligibility experiments. A future protocol must either reproduce the relevant ingredients or declare a different learning-progress signal and its information access.

## Comparisons that would make the generator useful rather than ceremonial

First select a bounded task space with an independent execution oracle and competent learner. Compare a strong fixed/heuristic generator against a frozen learned generator before adding generator adaptation. Later isolate whether adapting the generator improves future learning, holding the allowable task space and total compute accounting fixed.

The utility target is improvement on independently specified tasks and preserved old competence, not agreement between two models or endlessly raising the loss of generated exercises. Count generator inference/training, interpreter runs, mutations, rejected programs, verification, learner updates, repeated reward probes, storage and scheduling overhead. The same generator cannot create the hidden final exam after seeing the learner's errors and then claim independent transfer.

Avoid treating raw difficulty as value: a sequence can be difficult without providing useful, learnable structure. Development signals used to train/select the generator become part of its training information. Final confirmation must stay outside that loop.

## What must already be in place

The change/evidence contract, lawful target checking, ordinary curriculum control, meaningful continual-acquisition measures, and bounded candidate-training/adoption interface. A dependable selector can initially be ordinary code. The full NSS Tertiary is not needed to establish the first learning facts; do not create a circular requirement that a complete dream system must exist before testing any part.

Generator parameters may themselves forget useful exercise types or optimize a narrow score. The proposal should monitor generator coverage and later learner transfer rather than assume that adaptive teaching improves monotonically. Preservation/recovery of plasticity still needs a cumulative learner comparison.

## Status

Documented, deferred and not dispatched. No generated program, learner/generator model, training step, reward calculation, benchmark or interpreter was run for this note. Existing Primary generation rules, advisory Validator, mutual exclusion, experimental pause and FCR-0103-001 remain intact.
