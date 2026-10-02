# Git and release-asset layout

Keep the README, research map, study pages, rights notes, protocols, source, compact results/failures and provenance catalogs in Git. Keep complete execution ZIPs, raw per-case arrays, checkpoints, compiled libraries and large data outside Git history.

The proposed asset set has **50 top-level source packages totaling 1,056,556,721 bytes**. Nine additional distinct nested packages are navigated in the catalog; do not upload them a second time when their canonical parent ZIP already includes them. Each proposed original is below 2 GiB. This is a reviewed-release proposal, not an upload or a clearance finding. See [`catalog/release-assets-plan.json`](catalog/release-assets-plan.json) for exact identities and holds.

Original assets remain private at their recorded source locations. No large original ZIP was copied into this staging tree. If an original ZIP needs redaction, preserve it privately and produce a distinctly named derivative with an explicit member-level change manifest, original SHA-256 and new SHA-256. Verify the derivative independently and document omitted evidence. Do not silently replace an old archive or reuse its checksum for edited bytes.

## GitHub limits checked against official documentation

As reviewed on 2026-10-02, ordinary Git warns for files above 50 MiB and blocks files larger than 100 MiB. This draft uses a conservative 50 MiB maximum file check. [GitHub large-file documentation](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github).

GitHub also applies a separate maximum push size of 2 GB. Its large-file guidance recommends repositories ideally below 1 GB and strongly below 5 GB; the repository-limits page gives a separate on-disk Git size recommendation. These recommendations do not replace per-file limits. [Repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits).

A release can have up to 1,000 assets and each asset must be under 2 GiB. GitHub documents no aggregate release-size or release-bandwidth limit, but redistribution rights and service terms still apply. [GitHub release documentation](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases).

Pass 61 is exactly **101,813,985 bytes (97.10 MiB)**. It exceeds the warning threshold but is below the ordinary-Git 100 MiB hard cutoff; decimal MB and binary MiB must not be confused. It is still proposed as a release asset to avoid storing large evidence in Git history. IdentityBinding009 (242,997,220 bytes) and STATEBRIDGE01 (121,534,068 bytes) exceed that hard cutoff.

Git LFS is not configured. Its account-dependent limits, quotas and bandwidth billing have not been approved. Splitting ZIPs into Git-tracked chunks is not part of this plan. The owner authorized the screened Git checkout at `AegisAgentAscalon/NSS-Research`. This does not authorize the held raw assets; no GitHub Release assets are included in the publication scope.
