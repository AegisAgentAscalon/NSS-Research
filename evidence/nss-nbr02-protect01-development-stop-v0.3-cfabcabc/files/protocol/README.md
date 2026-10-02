# PROTECT01 — focused final design review v0.2

**Status: PROPOSED_FOR_FINAL_REVIEW. No execution authorized by this packet.**

The user has limited remaining Codex usage. The recommended use is one bounded adversarial review of a single candidate, not another portfolio of ideas. Read `CHAT_PROMPT.md`, then only the cited sections needed to challenge the design. Return concrete corrections and a disposition. Do not spend the pass reproducing REV01 or revisiting all program history.

## Read order
1. `CHAT_PROMPT.md`: the requested deliverable and the few consequential decisions.
2. `PROTOCOL.md`: intervention, observations, scoring, stop behavior.
3. `SOLVER_AND_FLOAT32.md`: proposed finite active-support search, exact sign convention, numerical admission and the actual-step control.
4. `WORK_AND_STORAGE.md` plus JSON ledger: all-attempt work, finite solver work, and honest unmeasured storage/host gates.
5. `REVIEW_DISPOSITION.md`: what Codex supplied, what this reviewer completed, and what remains unvalidated.

The earlier technical companion is present verbatim in `sources/ORIGINAL_PROTECT01_TECHNICAL.md`. Codex's previous receipt correctly did not list it. Its absence was a handoff gap, not evidence that the document never existed. The current packet includes it so the last review need not reconstruct it.

The full REV01 archive is NOT copied here. Its exact identity and selected source excerpts are provided. Codex's existing retained copy is the historical numerical dependency for a future run. Do not request the old package again unless its bytes are actually missing or fail the identity check.

All new equations, tolerances, probe schedules, seed values and caps are proposals. Document hashes are not an executable source lock. No task examples, initialization tensors, model outputs, QP runs, derivatives, training, replay, fault injection or parameter updates were generated in this review.

`python VERIFY_PACKAGE.py` checks the delivered documents and static arithmetic only. It is not a scientific test. No DOCX or duplicate models are needed for this focused handoff.
