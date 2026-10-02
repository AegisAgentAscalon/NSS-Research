# Execution v0.2, scientific protocol v0.1 unchanged
The v0.1 extractor stopped on an interleaved-branch identity assertion before any candidate review. Its entire work is retained under attempts/v0.1. The extractor now keys recorded states/tables by session and branch, including explicit checkpoints. No source logits, policy, tolerance, candidate selection, or old result changed. The source lock is renewed before extraction. This is a tooling correction, not an additional scientific fitting attempt.

A second pre-review source-adapter repair recognizes the actual TIMING01 dictionary-form manifest as distinct from REV01 list form. The stopped adapter and its locks/logs are in attempts/v0.2_pre_manifest. No candidate policy was evaluated before this repair.
