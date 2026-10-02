# NSS HSA + Segmented Context — Research Consolidation v1.0

Prepared 28 September 2026. Scope: **SH01, SH02, SC01, SC02, CAP01 and CAP02**.

**Disposition: working bounded component, parked for integration.** This package records completed research and does not dispatch a new experiment. It does not qualify a complete language-token maintenance architecture, a 25,000-token budget, DARP or the whole NSS lifecycle.

## Start here

Read `NSS_HSA_Segmented_Context_Research_Consolidation_v1.0.docx` for the formatted report, or `CONSOLIDATED_REPORT.md` for its portable text. The report includes research questions, each test design and comparator, results and costs, failure evidence, conclusions and a maintenance-token implications section. The DOCX has 27 rendered pages and a clickable reader's guide; pagination can vary with the local renderer.

`notes/NEXT_CHAT_HANDOFF.md` is the short continuity record. `indexes/SOURCE_REGISTER.md` maps source citations. `indexes/TEST_CATALOG.md` points to the actual test and runner implementations in the original packages. Machine-readable source, model-file, full-member, question and result indexes accompany them.

## Original evidence

The full edition includes all six original execution ZIPs **unchanged** in `original_archives/`. Their original protocols, source, fixtures, checkpoints, output arrays, failures and audits remain in their own study roots. Do not flatten these into one source tree or silently replace the historical code with a later version. The consolidated layer is documentation and indexing, not a new integrated runtime.

The smaller **review edition** omits `original_archives/`. It includes the same report, source documents, indexes, handoff and byte-audit record; it is not a standalone replacement for the full execution evidence. The edition is declared in `MANIFEST.json`.

This consolidation freshly verified the six original ZIP hashes/sizes against delivery receipts, all ZIP CRCs, and all **2,482** declared inner payloads. Standalone reports and available architecture documents match the originals. It did **not** load a model, run inference, train, rerun scientific tests, change gates, rescore data or verify outside literature. Original limitations and failed checks remain unchanged.

## Verify without running a study

Python 3.9 or later and its standard library are sufficient for these delivery tools. From the extracted package root:

```sh
python tools/verify_consolidation.py
python tools/verify_consolidation.py --deep
```

The first checks every consolidated payload. The second also verifies all original ZIP CRCs and inner manifest hashes. In the compact review edition, `--deep` exits with code 2 and explicitly reports that original archives are omitted; it does not claim to have checked absent bytes. Do not write command output inside the package tree if you want its exact manifest membership to continue matching. Hashes detect changes relative to the supplied manifest; they are not proof of publisher identity.

To extract one study **without executing it**:

```sh
python tools/extract_study.py CAP02 --destination ../CAP02_review_copy
```

The destination must not exist. The tool verifies the original archive and rejects unsafe paths before copying it. Read that study's README and protocol before considering any separate scientific reproduction. Historical operational continuation scripts are not generic new-run commands.

## Interpretation to carry forward

HSA helped learn the supplied maintenance rule. Exact segmented execution preserves source-bound jobs and extends executable input reach beyond a resident packet limit. Mixed-size preparation improves larger-layout use while retaining the tested small rule. Ordinary caching and streaming explain substantial parts of the benefits and remain valid references. The slower intermediate neural cache and other regressions remain recorded.

The 37 numerical features and active record-position budgets are **not language-token budgets**. A real token writer/reader, semantic selection and summarization, full memory/energy accounting, and an overnight learn–repair–adopt–resume lifecycle remain integration questions. DARP is primarily output generation; these studies did not implement it. Keep this component available while moving on to the next theoretical idea rather than reopening every limitation immediately.
