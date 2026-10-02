# NBR02-EVAL01 — completed retrospective evaluator/reviewer comparison
No model, gradient or optimizer execution. Actual prior neural outputs are the data. This is NBR-02 research, not deployment or proof of transferred NSS capability.

Read REPORT.md and CHAT_PROMPT.md. The scientific contract is protocol/PROTOCOL.md, fixed before new policy outcomes. Execution v0.2 preserves earlier source-adapter failures under attempts/. Recorded candidates are all exposed historical examples; old qualifications remain unchanged.

Files: inputs/CANDIDATES.json supplies the self-contained new review input. inputs/REV01 and inputs/TIMING01 retain selected raw proofs, provenance, original score tables and reports. Larger auxiliary inputs are gzip-compressed; inputs/ENCODINGS.json supplies decoded and encoded identities. No restoration is required for review or scoring. Original neural archives are only needed to rerun source extraction, not policy evaluation.

Commands after extraction:
    python VERIFY_STUDY.py
    python RESCORE.py --output /a/new/output/directory
    python REPRODUCE_REVIEW.py --output /a/new/reproduction/directory

RESCORE runs independent reference adjudication only. REPRODUCE_REVIEW is explicitly a new ordinary review replay over unchanged stored outputs and then scoring; it does not repeat training or old adaptive replay. Do not overwrite archived outputs or call it another scientific sample. All scripts require standard Python; the independent scorer/provenance diagnostics additionally use NumPy. No neural-library dependency.

Do not use probabilities as calibrated operational safety guarantees. Partial panels cover only selected members of the eight-record inventory; the full reference still says nothing about unobserved skills. No real credentials, live serving publication, recurrent-state migration, new repair scheduling, or dreaming is implemented.
