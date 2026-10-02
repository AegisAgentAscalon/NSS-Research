# Q010 source-repair workspace v1.4

**SOURCE CHANGES ONLY — RUNTIME VALIDATION NOT RUN.**

The original `REPORT.md`, receipts and result folders describe v1.3 and earlier
work. They do not validate these changed operators. Read
`SOURCE_REPAIR_v1.4/REPAIR_REPORT.md` and its patch index first.

The v1.4 path is `tools/q010.py`, with an explicit workspace-manifest SHA256.
This bootstrap checks source/dependency bytes before importing numerical code.
Main fitting requires a separate frozen protocol and pre-main source/start lock.
No accepted protocol, main fit, held-out evaluation or scientific qualification
is created by applying this patch. Do not use older historical launch commands
as if they accepted the new source or checkpoint-publication schema.

Keep run outputs outside this directory. Use the same run-root lease for fits,
roster creation and evaluation. Main training remains three arms × five seeds
1201–1205 × 6000 updates; the small bounded invocations do not replace full fits.

Source-copy preparation performs file integrity checks only. The next stage must
validate the changed interfaces and reviewed failure recovery before main dispatch.
