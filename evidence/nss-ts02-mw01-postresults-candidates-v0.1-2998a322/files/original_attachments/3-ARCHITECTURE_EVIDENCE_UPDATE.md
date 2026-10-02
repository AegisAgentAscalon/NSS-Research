# AER-TS02-MW01-001 — evidence update, not production adoption

Parent proposal: **ACP-TS02-MW01-001**. Parent NSS Architecture Ledger v0.1 remains byte-identical, SHA-256 `8ca191b60c8793bfd4aa8bd2e36740b3f41c1d471f19a5e0e42388db04375b43`.

## The implemented boundary

**ST-04 (maintained explicit metadata) → IF-02 (workspace-conditioned recurrent update) → ST-02 (evolving learned task state).**

Five field-typed categorical IDs per task are written by deterministic code from public goal and evidence events. A shared learned 18×4 embedding provides twenty float32 inputs alongside each admitted event. The learned GRU integrates these with its selected task bank. Query heads see state, not direct gold/progress from the writer. Software still supplies authority, task-bank selection, inactive-bank protection and no-op filtering.

Residency: ten uint8 IDs remain stored. Consultation: only actual neural updates, not every wall-clock instant or skipped event. Rewrite: accepted goal/evidence changes; physical whole-packet assignments are counted separately from changed fields. RESET of progress is learned; metadata remains resident. The core does not run merely to retain IDs.

## Evidence disposition

Native interface feasibility is implemented and numerically replayed. RW CARRY=526/600 held-out joint readouts versus R=507 and larger R+=496. Same-checkpoint slot mask drops RW to366/600, while state erasure leaves38/600. This supports channel dependence, not fair capacity-matched superiority.

**The declared scientific screen fails.** Only3/5 RW fits reach90%;75/1200 invalid revision claims and17/100 designated wrong-DONE assertions remain; the known-repair subset ties R+ at79/125. No improvement requirement is relaxed. Exact programmed S/X remain perfect.

The post-result audit identifies a dual-revision composition absent from training. All models fail E:32, and the model's right-revision claim remains stale after later progress becomes correct. The RW packet itself is accurate. This narrows a research question; it is not a proven cause or a repaired experiment.

## Canon and ownership

The user-adopted role of tokens as supporting information management remains in force. The five-field vocabulary, dimensions, update policy, and GRU are study-local choices—not default settings for all NSS cores. The writer is not learned; the common authority checker is not the advisory neural Validator. No Primary/Secondary/Tertiary role is replaced or experimentally qualified.

No learned writer, routing, cadence choice, hidden-state compression, exact-data superiority, or universal recurrent-control benefit is adopted. Parent ledger files are not edited; attach this evidence record to the existing open interface and questions. JSON companion preserves every relevant ADR/ST/IF/TD/OQ mapping from the reviewed change proposal.

## Next permitted planning question

Define a separate controlled proposal for compositional stale-derived-state repair with genuine held-out coverage, strong R/R+ and exact controls, full writer/index costs, and explicit raw binding outputs. Treat source metadata that can be copied exactly separately from derived task consequences that must be learned. Do not retrain to known E:32 labels and call that generalization. No additional experiment is authorized by this note.
