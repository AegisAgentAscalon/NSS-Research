# Missing and limited evidence

This register describes the supplied NSS source tree as inventoried on 2026-10-02, including nested archives. “Not located” does not mean a file is lost everywhere. A report, delivery receipt or checksum cannot substitute for unavailable archive bytes.

## Immediate low-bit archive gaps

| Pass | Original full bundle status here | What is retained |
|---|---|---|
| 55 BRIDGE01 | Full prototype ZIP retained | Protocol, report, source, model exports, session evidence and audit |
| 56 LB01-TERNARY | Full original execution ZIP not located | Copied report, protocol, README and manifest in pass61 provenance; historical digest and lineage claims |
| 57 LB02-Q2-TRAIN | Full original execution ZIP not located | Copied report/protocol/README/manifest; selected pinned Q2_M8 starts and inherited source in pass61 |
| 58 LB02-MASTER16 | Full original execution ZIP not located | Copied report/protocol/README/manifest; inherited engine/kernel and lineage records in pass61 |
| 59 LB01-T3-TARGET | Full original execution ZIP not located | Copied report/protocol/README/manifest and historical lineage/digest records |
| 60 LB01-Q2-PACK | Full original execution ZIP not located | Copied report/protocol/README/manifest and historical lineage/digest records |
| 61 LB03-LEARNABILITY | Full execution ZIP retained | 898 declared payloads freshly matched to inventory; exact manifest digest and membership verified |

The supplied `NSS_Passes55_59_with60_Reconciliation_v0.1.md` states that six full ZIPs and a separate reconciled-records bundle were available during its earlier audit. That statement is preserved as historical evidence. Those pass56–60 full ZIPs and that separate combined bundle were not found in the current supplied source tree. Pass61 is self-contained for its selected comparison; it does not contain all historical raw arrays from those passes. Do not present the older audit as proof that those ZIP bytes are now distributed here.

## Earlier gaps and partial evidence

- **Original Q010 qualification:** original full study, training history and complete original source/checkpoint record are unavailable in the retained record. Later Q010 inference recovery, partial inherited-reader recovery and delivery receipts are separate evidence. They do not recreate the original training/optimizer/RNG history.
- **TS01, TS02-MW01, TS03-CR01, CKA01, DC01 and TEACH01:** reports, handoffs, inherited subsets and some working evidence are retained through consolidation/recovery packages. Full original execution ZIPs were not located as complete original bundles here. Use each study's locators and archive/member catalog; do not infer that every tensor, optimizer state or raw trial is included from a report-only package.
- **RECOVER01 v0.2 and TRACE01:** later findings are represented in secondary reports/ledger material. The preserved RECOVER01 v0.1 proposal is a different version and is not an execution archive.
- **DARP01–03:** the retained consolidation describes the results, but does not supply their full original execution/checkpoint bundles. A prose judgment about the writer is not a fresh checkpoint audit.
- **Reader, memory and maintenance line:** COMP01 setup, LAB01/LAB02, MEM01, PREP01, READER-SUPPORT01 and CYCLE01-A are represented by available report/ledger evidence. Their full original execution bundles were not located here. CYCLE01-A ran according to the retained report; the reserved main/CYCLE01-B did not.
- **Ancestral training data and cost:** low-bit packages retain selected parents and replay batches, not every original ancestor-training example or fitting trace. Unsaved interrupted update tails, terminal timing and memory totals remain unknown. Hashes cannot manufacture them.

## Not applicable or never run

The absence of pass60 training checkpoints is expected: it performed no training. SURFACE01's main correction/adaptation comparison was not opened after its competence stop. CYCLE01-B, BALANCE01 and other retained proposals must not acquire invented results or checkpoints. Empty failure directories do not demonstrate zero model errors; errors may be retained in raw output arrays.

## Where to verify availability

The [chronology](catalog/chronology.json) retains source-ledger wording and resolved source locators. [Archive membership](catalog/archive-members.jsonl) lists freshly read hashes/bytes for selected packages. [Omitted evidence](catalog/omitted-evidence.jsonl) distinguishes retained binaries and raw text reserved for releases from missing source bundles. Original WorkspaceSupport, RecycleRecovery and LogicAtlas preservation archives remain private because they mix historical research with operational/Git metadata; relevant scientific records are navigated separately where available.

The owner has accepted the surviving, AI-reviewable records as the publication scope. Recovering unavailable historical bundles is not a prerequisite. Publish the documented evidence boundaries accurately; do not advertise a complete runnable historical record. See [per-study availability](EVIDENCE_AVAILABILITY.md) and the [AI review guide](AI_REVIEW_GUIDE.md).

## Delivery receipts do not supply missing archives

A targeted check of both the source-file inventory and nested member locators found none of the ten named full execution/Codex Review ZIPs for passes 56–60. The separate combined complete-records package was also absent. Pass61 retains P55–P60 reports, protocols and READMEs, historical manifests and delivery JSON, plus a 2,909-row complete-record inventory. Those are retained provenance records, not the 2,909 payloads themselves. Each low-bit study page now links its historical delivery receipt separately.
