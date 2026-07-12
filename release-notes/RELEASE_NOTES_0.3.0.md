# Vardheim 0.3.0 Release Notes

Status: release candidate; pentest and remediation retest passed, awaiting GitHub checks

## Scope

This release establishes the immutable normative-source baseline used by all
later protocol implementation. It adds no ACME wire behavior.

## Added

- Exact RFC Editor TXT source URLs and SHA-256 bindings for all 65 tracked RFCs.
- Machine-generated index of 3,071 numbered sections across those RFCs.
- Explicit implementation roles for ACME, JOSE, HTTP, PKIX, TLS, email, DNS,
  and normative-foundation sources.
- All-status RFC Editor errata snapshot covering all 13 published ACME RFCs.
- Offline source/index/errata validation in normal CI.
- Optional official live errata comparison that never changes pinned evidence
  automatically.
- Negative tests for missing roles, malformed sections, RFC-set drift,
  duplicate errata IDs, and invalid errata statuses.
- Permanent enforcement that the `vardheim` facade version and publication
  selection always match every release/tag version.

## Errata Snapshot

The 2026-07-12 official snapshot contains 24 records: 12 Verified, 5 Reported,
6 Held for Document Update, and 1 Rejected. Only Verified errata become
normative requirement inputs. All other statuses remain recorded and
drift-checked without silently overriding published RFC text.

## Publishing

Only `vardheim` advances from `0.2.0` to `0.3.0`. The four unchanged support
crates remain at `0.1.0`. The facade version is required to equal `v0.3.0` and
is always selected for publication.

## Security

- RFC text remains byte-locked, read-only locally, and excluded from crates.io
  packages.
- Generated evidence cannot be manually changed without failing deterministic
  regeneration checks.
- Live network state never affects normal offline builds or CI.
- Reported, Held, and Rejected errata cannot silently weaken or alter protocol
  requirements.
- RFC downloads have a 10-second connection timeout and 60-second total
  transfer timeout while retaining strict post-download SHA-256 verification.

## Pentest Remediation

The initial review found one low-severity availability issue: a stalled RFC
Editor connection could leave the opt-in fetch command waiting indefinitely.
The fetch now has explicit connect and total time bounds. A permanent
integration test executes the real script with a fake downloader, proves both
timeout arguments are present, and verifies the downloaded bytes through the
strict checksum gate. The maintainer-supplied remediation retest passed, and
no blocking findings remain.

## Compatibility

Rust `1.90.0` through `1.97.0` remains supported. All crates remain `no_std`
and dependency-free.

## Known Limitations

No RFC conformance is claimed yet. Section-level requirements and conformance
slots are introduced in later evidence milestones before protocol code begins.
