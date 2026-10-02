# DatasetSnapshot001 fixtures

Self-authored synthetic software-test data only. `capture_validation.json` is an
unreviewed capture request; the demo separately creates scripted HUMAN approval
and training-permission events. None is evidence of actual human review.

`tokenizer_identity.json` is an identity-only byte fixture. It is deliberately not
a real tokenizer or model. DatasetSnapshot verifies its digest and never executes it.

Run `python -m nss_base.datasetsnapshot001` for the connected in-memory lifecycle,
or add `--directory ./snapshot-demo` to retain its local SQLite demo files.
No private conversations, downloads, network services or training are involved.
