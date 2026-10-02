# Provenance catalogs

- `artifacts.json`: original ZIP identities, nested relationships and release hold.
- `archive-members.jsonl`: exact member hashes/bytes freshly read from selected source ZIPs.
- `derivations.jsonl`: original payload and public derivative SHA-256/bytes, redaction or deduplication records.
- `source-locations.json`: original relative locators mapped to browseable files.
- `omitted-evidence.jsonl`: excluded binaries, large payloads, private trees and operational material; absence from Git does not mean lost evidence.

Originals remain private and unchanged. Original manifests embedded in historical packages describe the original payloads; they do not validate redacted derivatives. A source checksum is integrity evidence, not a grant of rights or scientific replication. DOCX paragraph-text derivatives omit formatting and properties; their source container hash is separately recorded.

- `evidence-availability.json`: current per-study available-source status, reproducibility limits and exact review paths; this is the current availability authority alongside the study pages. Historical ledger statements remain attributed source claims.
