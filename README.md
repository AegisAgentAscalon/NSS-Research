# NSS Research

A research archive about persistent neural state, memory, learning, evaluation and low-bit computation. This repository preserves the surviving NSS research record, with explicit evidence availability and reproducibility limits.

For AI review, start with the [AI reading guide](AI_REVIEW_GUIDE.md) and [per-study evidence availability](EVIDENCE_AVAILABILITY.md).

Start with the [research map](RESEARCH_MAP.md), [chronological study index](studies/README.md), or [retained evidence packages](evidence/README.md). The [historical compendium](documents/NSS_Research_Compendium_v1.0.md) organizes the earlier work by research question. [Reproducibility](REPRODUCIBILITY.md), [evidence limits](EVIDENCE_LIMITS.md), [release layout](RELEASE_LAYOUT.md) and [license scope](LICENSE_SCOPE.md) explain what can be checked and what remains open.

The chronology now contains **61 records**. The earlier **59-pass** endpoint ends at LB01-T3-TARGET; pass 60 is LB01-Q2-PACK and pass 61 is LB03-LEARNABILITY. These records include diagnostics, analysis, engineering and planning; they are not 61 successful experiments. The older compendium contains **67 thematic entries**, including proposals, recovery work and audits. Its count is a different index, not a competing pass count.

The latest retained execution package, LB03-LEARNABILITY, reports a bounded mixed-precision learning result. FP16 stochastic master rounding met the frozen cohort screen separately in EARLY and NEW, but only two of four identical parents passed both regimes. Old-task retention remained mixed. The 19.45% saving applies to named learning arrays; the broader saved-tensor union saving was about 1.41%, with slower measured training. Wide precision remained elsewhere. Sigmoid overflow warnings and large gate inputs remain a robustness limit. This is not all-two-bit training, a scaled language-model result, independent replication or system qualification.

## Find the material

| Location | Contents |
|---|---|
| `studies/` | One page for each chronological record, with evidence tiers and locators |
| `evidence/` | Historical protocols, reports, source, compact results, failures and receipts from retained packages |
| `documents/` | Master records, architecture discussion and historical compendium; Word documents have explicit text derivatives |
| `catalog/` | Archive/member identities, original-to-public checksums, omissions and release holds |
| `tools/` | Safe local hash verifier; it does not execute research code |

Original archives remain private and unchanged. Public derivatives document path redactions and have separate hashes. Large evidence is not committed to Git; see the [release plan](RELEASE_LAYOUT.md). Missing execution archives are listed explicitly, even where a report or a historical delivery receipt exists. Original code is licensed under [MIT](LICENSES/MIT.txt); original research documents, data and model artifacts published here are licensed under [CC BY 4.0](LICENSES/CC-BY-4.0.txt). See the [exact scope and attribution](LICENSE_SCOPE.md) and [third-party exceptions](THIRD_PARTY_NOTICES.md). Raw model/checkpoint/array payloads are not included.

The owner accepts the surviving, reviewable records as the publication scope and attests that the research code and data were created within this project. Unavailable historical ZIPs remain disclosed limitations; their recovery is not a prerequisite for this documentary scope. The owner authorized the [license split](LICENSE_SCOPE.md) and publication of this screened checkout. Raw assets remain outside the [publication scope](PUBLICATION_STATUS.md).
