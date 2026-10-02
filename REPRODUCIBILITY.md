# Reproducibility

This checkout supports document/source inspection and hash verification. Complete study execution requires its exact reviewed evidence bundle, environment and inputs. Assets have not been uploaded; no working download URL is implied.

1. Choose a record in [the study index](studies/README.md). Read its original report, frozen protocol, source lock, failures and evidence limits before selecting an executable entry point.
2. Resolve the original archive and nested member identities through `catalog/artifacts.json` and `catalog/archive-members.jsonl`. A receipt without the corresponding bytes cannot provide a runnable dependency.
3. Verify the Git candidate with `python tools/verify_catalog.py`. It reads files and hashes only. Public derivative hashes differ from original hashes when redaction or document-text extraction occurred.
4. For future independently authorized reproduction, obtain cleared original assets and verify their checksums before extraction. Reject traversal paths; inspect NPZ keys as container members rather than extracting them to Windows filenames. Do not unpickle untrusted checkpoint files.
5. Read the study's own environment record and dependency/source locks. This collection has heterogeneous Python, NumPy, PyTorch and C-based studies; there is no verified single global environment. No packages were installed during preparation.
6. Review hard-coded historical paths. Public path placeholders are redactions, not runnable locations. Reproducing from a redacted source tree requires explicit path configuration and new run provenance; original source locks validate originals, not edited files.
7. Preserve each historical start, training/evaluation split, seed, budget, threshold and stop condition. Record training, preparation, evaluation, storage and runtime costs separately. Put any future run under a new identity and retain failures.

## Checkpoint lineage

Pass 55 floating parents are reported as the ancestors for passes 56/57 and pass 59's reference inputs. Pass 57 Q2_M8 step1024 starts feed pass 58; Q2_M32 step1024 starts feed pass 59; pass 59 Q2_CONTROL packed final exports feed pass 60. Pass 61 retains selected Q2_M8 step0000 and step1024 starts and lineage receipts. Its 24 historical link checks are retained claims; this preparation does not have every historical full ZIP needed to freshly repeat all links. See each study's availability and the retained `CHECKPOINT_LINEAGE.json` / `SELECTED_STARTS.json`.

Pass 61 historical counts (336 output arrays, 120 checkpoints and 120 exports) are report claims backed by its retained package, not outputs of this packaging task. A successful checksum check proves byte identity, not statistical validity or external replication.
