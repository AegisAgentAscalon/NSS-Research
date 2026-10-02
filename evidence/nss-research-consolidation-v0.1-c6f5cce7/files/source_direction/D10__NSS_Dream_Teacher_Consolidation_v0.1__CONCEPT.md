# Primary-guided, retrieval-grounded dream consolidation
## CAND-NSS-DREAM-DISTILL-001 / ACP-NSS-DREAM-DISTILL-001 · concept v0.1

**Status:** User-proposed architectural extension, developed here as a concept only. No experiment, model loading, inference, gradients, training, source implementation, or numerical reanalysis occurred. Existing scientific verdicts remain unchanged. The parent Architecture Ledger is not overwritten.

## 1. What the user is proposing

Primary supplies the stable general and identity-bearing foundation. Secondary is the online/adaptive learner, with recurrent/persistent task-state ownership still to be specified. Tertiary handles dreaming: consolidation, repair, practice, review and potentially curriculum generation.

Between dreams, light maintenance permits some manageable residual deterioration. A full dream should be a richer operation than enlarging the same replay batch: Tertiary retrieves recent retained experience, obtains teaching signals from the frozen Primary, and uses that material to repair and advance a Secondary candidate.

The proposed end condition is an affordable return to an agreed operating range while retaining useful new learning, not restoration of every historical weight or probability. Near-complete recovery is a hypothesis to measure on declared capabilities, not an established property.

## 2. What the existing experiment does and does not supply

MICROMACRO01 used 674-parameter numerical learners, complete eight-record old buffers, and independent short cycles that restart from their initial checkpoints. Distributed and late replay satisfied a newly declared, bounded full-cycle requirement and survived two additional ordinary learning receipts. It did not implement a stable Primary teacher, Tertiary, retrieval over a growing experience archive, curriculum synthesis, cumulative plasticity, or state migration. [S3 §§1–3,10]

Its larger replay slot is an analogue of one maintenance operation, not a realized full dream. The result supports a useful rehearsal ingredient; it supplies neither a ceiling on what a richer consolidation phase can accomplish nor evidence that those added mechanisms will work.

## 3. Source, teacher, coordinator and student

| Component | Proposed role during the dream cycle | Important limit |
|---|---|---|
| Frozen accepted Primary | Provide stable reference behavior on relevant general tasks, identity-related constraints and demonstrations; respond to retrieved context where appropriate | Stability is not correctness on every task; an unconditioned Primary does not contain every recent personal correction |
| Tertiary | Review changes, retrieve source records, diagnose missing coverage, assemble a syllabus and propose verifiable practice | Selection and generated explanations are not independent truth or automatic permission to train |
| Secondary candidate | Receive the actual training updates and integrate current experience with retained useful capabilities | The student must execute to learn; a frozen live Secondary and a trainable copy have different roles and real resource costs |
| Exact archive / internal retrieval | Preserve current and historical evidence, revisions, targets, failures and accepted demonstrations | Retrieval does not automatically update parameters or reconstruct arbitrary lost latent state |
| Evaluation and governed adoption | Assess recovery, new learning, later acquisition, costs and compatible state before adoption | The neural Validator remains advisory; the teacher cannot certify itself merely by agreement |

The direct transfer is **Primary → candidate Secondary**, selected and organized by Tertiary. The phrase “Tertiary distills Primary” need not require first compressing Primary into Tertiary and then teaching Secondary. That two-hop design is a separate option only if it has a specific benefit worth testing. The proposal does not require Secondary to become a complete duplicate of Primary.

Primary outputs, approved old-Secondary demonstrations and public evidence are different knowledge sources. Secondary may have legitimate competencies or personalization that Primary never acquired. Preserve those through their source records and qualified behavior rather than training Secondary to imitate Primary everywhere.

## 4. Two distinct uses of retrieval

**Retrieval-assisted operation:** the model obtains evidence when producing its current answer. Success can depend on that evidence remaining available at use time.

**Retrieval-grounded consolidation:** the dream process fetches records, constructs target-bearing training examples or teacher demonstrations, and actually updates the candidate. Some resulting behavior may then be available without retrieving that exact record again.

RAG combines parametric and external memory; knowledge distillation transfers a teacher's behavior through training signals. These are different operations, not two labels for automatic copying of an archive into weights. RAFT is a relevant example of training a model to use retrieved documents, but its results concern open-book domain adaptation, not near-total repair of a recurrent learner. [P1,P2,P4]

To claim a parameter-level improvement, measure raw candidate performance with controlled retrieval access, as well as the full retrieval-assisted system. Distinguish these scores rather than treating an archive answer as proof of neural consolidation. Skills intended to use tools or retrieval should also be evaluated under their actual intended access contract; a closed-book test is not a universal definition of competence.

## 5. What must be retained before dreaming

“Temporary knowledge” must be recoverable evidence, not only an impression inside a volatile vector. Preserve the relevant observations, corrections, current target revisions, task scope, successful action/outcome records, failure descriptions and selected checkpoints under a declared retention budget.

Do not require an unlimited transcript or every tensor forever. The bounded management workspace points to detailed records and unresolved questions in the archive. Retention coverage and gaps must be explicit.

Raw recurrent state is version-specific working information. A text retriever cannot be assumed to decode all of it, and a newly trained candidate cannot automatically interpret an old hidden vector. Resuming unfinished work requires its own qualified migration/rebuild/reset procedure. The existing maintenance proposal already preserves these boundaries. [S1 lifecycle; S2 §§6,8]

## 6. A balanced dream syllabus

Proposed sources are:

1. **Stable foundations:** relevant Primary demonstrations and qualified general-capability examples.
2. **Current experience:** authoritative recent corrections, observed outcomes and current preferences, with revisions intact.
3. **Retained Secondary-specific competence:** legitimate older experiences and qualified demonstrations, selected from more than only the last dream interval.
4. **Checked practice:** variations whose answers are supplied by an independent executable rule, simulator or other legitimate evidence.

No mixture coefficients are selected here. A useful default hypothesis is continuing from the current Secondary checkpoint, not resetting it to Primary. If a later experiment tests reset/rebuild, its loss of acquired skills and additional training must be explicit.

The Primary must not overrule newer authoritative evidence by default. For example, a generic habit taught by Primary should not erase a verified user-specific correction. Teach the general rule and its legitimate scoped exception. Teacher disagreement or unsupported synthesis remains unresolved evidence rather than a new factual target.

The self-play generator idea can later improve practice selection or generation. It should not be required before testing whether teacher-plus-retrieval consolidation works at all. Unverified imagined outcomes stay hypotheses. [S1 §§3–4; S2 §8]

## 7. Scheduling without silently changing the three-core invariant

Existing design retains Primary participation and Secondary/Tertiary mutual exclusion, including learning work. The conservative compatible cycle is:

- **Prepare:** Primary + Tertiary review the fixed journal interval, retrieve evidence, obtain teacher demonstrations and freeze a rehearsal manifest. Secondary is paused.
- **Train:** pause Tertiary; run the separately authorized Secondary-candidate learning phase, with Primary participation and/or retained teacher targets. The serving checkpoint remains unchanged.
- **Review:** pause candidate learning; Primary + Tertiary inspect independent evaluation, persistent gaps and proposed adoption. Further repair, if any, must fit a predeclared finite budget rather than continue until scores pass.
- **Resume:** adopt through the governed boundary and restore task state only under the compatible version contract.

These subphases can all belong to one overall dream interval. “Secondary is not serving” is not equivalent to “training a Secondary copy uses no Secondary computation.” Concurrent candidate training while Tertiary computes would need a separate explicit scheduling change; it is not assumed here. [S1 lifecycle; S2 §§6,8]

## 8. Why substantial recovery is plausible, and where it is bounded

The frozen teacher can supply reference behavior not damaged by Secondary's online updates. Retained experience can supply newer knowledge the teacher lacks. Targeted practice can exercise a skill under varied inputs rather than merely repeat a few old answer labels. This is the proposed advantage over self-rehearsal alone.

It is not an information-complete recovery mechanism. Missing evidence, teacher errors, insufficient coverage or capacity, harmful interactions, and finite optimization can prevent full recovery. Copying every teacher response cannot guarantee preservation of new knowledge. A frozen teacher does not increase its own knowledge from Secondary experience unless a separate generation-level process is specified.

Measure functional recovery and continued new-task learning separately. A candidate can recover old answers without recovering plasticity. Distinguish repaired deficits from tolerable residual trade-offs, and assess whether repair demand grows over repeated dream cycles. [S1 “What benefit would need to be demonstrated?”]

Relevant research supports ingredients rather than the combined NSS claim: knowledge distillation [P1], active learning followed by consolidation [P3], generator/solver replay [P5], and retrieval-aware fine-tuning [P4]. Progress & Compress updates its knowledge base; that is not NSS's frozen-Primary rule. Deep Generative Replay was tested in sequential image classification; it is not evidence for a dream-driven companion.

## 9. Smallest future discriminator, not a dispatched test

Use the same adaptive learner, archive eligibility, budget and assessment process. Compare a 2×2 study of **Primary teaching on/off** and **recent source-grounded replay on/off**, while providing the same old-skill support and matched available training effort. Include a cheaper no-deep-maintenance reference and, where useful, the current ordinary-replay maintenance reference.

A record-only branch can use direct verified targets rather than teacher-generated answers. A teacher-only branch lacks the recent records intentionally; its failures on uniquely recent facts are information limits, not general defects. Cache teacher targets where lawful and count their generation, retrieval and verification. Equal training-update counts do not equal total compute.

Keep curriculum selection initially transparent and fixed. Only after this teaching/retrieval mechanism is understood compare Tertiary-selected practice against a strong ordinary selector using the same information and full budget. Do not attribute the benefit of teacher/replay information to a learned Tertiary that was not actually used.

Measure before dream, after dream and after more online learning: old-skill recovery, retained current corrections, newly acquired competence, obsolete-fact regression, source dependence, coverage, restoration of new-task learning where applicable, task-state resume, and end-to-end costs. Use real continued histories for a cumulative claim; independently restarted toy cases cannot establish it. No numerical thresholds, fit counts, source lock or execution authorization are created by this note.

## 10. Disposition

Link RET-DREAM-MAINT-001 and the existing foundation-return plan FCR-0103-001. Keep NBR-01 bounded-closed and NBR-02 active. The parked NBR-01 question, deferred self-play, and cost/compatibility gaps remain separately tracked. This proposal does not undo any failed screen or authorize a new experiment.

**Design target:** light maintenance keeps the learner usable between dreams; Primary-guided, retrieval-grounded dream consolidation seeks much fuller functional recovery and integration of recent experience, within a tested budget. Whether it can approach complete recovery across the required capabilities is an empirical target, not a promised result.

## Sources

### Project documents read for this note
- S1: NSS_NBR02_REV01_Execution_v0.4/DREAM_MAINTENANCE.md.
- S2: NSS_Layered_Review_Maintenance_v0.1/ARCHITECTURE_ADDENDUM.md.
- S3: NSS_NBR02_MICROMACRO01_Execution_v0.2/REPORT.md.
- S4: NSS_Architecture_Ledger_v0.1/ARCHITECTURE.md (role/scheduling context; older experimental-status labels remain historical).
- U1: Current user message specifying Primary general/identity, Secondary adaptive learning, and a Primary + Tertiary distillation/internal-RAG full dream.

### External primary research consulted as context, not NSS evidence
- P1: Hinton, Vinyals and Dean, *Distilling the Knowledge in a Neural Network*. https://arxiv.org/abs/1503.02531
- P2: Lewis et al., *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. https://arxiv.org/abs/2005.11401
- P3: Schwarz et al., *Progress & Compress: A scalable framework for continual learning*. https://proceedings.mlr.press/v80/schwarz18a.html
- P4: Zhang et al., *RAFT: Adapting Language Model to Domain Specific RAG*. https://arxiv.org/abs/2403.10131
- P5: Shin et al., *Continual Learning with Deep Generative Replay*. https://arxiv.org/abs/1705.08690

The external abstract/method summaries were consulted; no paper was independently reproduced. File identities are in SOURCE_IDENTITIES.json. Document byte checks do not validate the proposed architecture.
