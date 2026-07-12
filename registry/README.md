# Registry Reference Snapshot

This directory contains byte-pinned XML snapshots of the official
[IANA ACME registry group](https://www.iana.org/assignments/acme/acme.xhtml)
and the Bundle Protocol, COSE, and SMI registry groups normatively referenced
by RFC 9891, plus Vardheim-generated evidence derived from them. The snapshots
were checked on 2026-07-12. The ACME source reports an IANA last-updated date
of 2025-11-25.

The `iana-*.xml` files remain IANA source material. Vardheim claims no
copyright in them and does not apply the project's MIT OR Apache-2.0 license
to those files.
The generated JSON and explanatory documentation are Vardheim project files.

## Integrity And Bounds

- `SHA256SUMS` locks the exact bytes of all four IANA XML sources.
- `EXTERNAL_SOURCES.json` maps every non-RFC normative reference in the
  published ACME family to an exact revision, content hash, DOI, or reviewed
  authority URL.
- `REGISTRY_BASELINE.json` is generated deterministically from those bytes,
  the RFC section inventory, reviewed HTTP replacement mappings, and pinned
  external profile revisions.
- `scripts/registry_baseline.py` rejects oversized input, XML declarations
  capable of entity expansion, unknown or missing registries, duplicate
  record keys, excessive records/fields/references, missing primary names, and
  stale generated output.
- The normal offline check gate regenerates the semantic model in memory and
  compares it byte-for-byte with the committed JSON.
- `scripts/lock-registries.sh` makes the raw XML and checksum manifest
  read-only locally as an additional guard; hashes and review remain the
  portable authority because Git does not preserve read-only permissions.

Baseline updates are deliberate review events. Network state never rewrites an
accepted snapshot during builds or CI. The advisory upstream drift machinery
arrives at the separately reviewed `v0.3.3` milestone.

## crates.io Exclusion

This directory is repository evidence, not crate payload. Publishable crates
live below `crates/`, and package checks reject leaked registry or image assets.
