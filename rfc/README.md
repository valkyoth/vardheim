# RFC Reference Copies

This directory contains exact, unmodified plain-text copies downloaded from
the [RFC Editor](https://www.rfc-editor.org/). Vardheim uses them as local
normative references for conformance matrices, implementation review, test
vectors, and security analysis.

Vardheim and its maintainers claim no copyright in these RFC documents. Each
RFC retains its original copyright notices, authorship, status, disclaimers,
and legal terms. The RFC files are not licensed under Vardheim's MIT OR
Apache-2.0 project license; they remain governed by their own notices and the
[IETF Trust Legal Provisions](https://trustee.ietf.org/license-info).

The RFC Editor states that RFCs may be freely reproduced unmodified. These
copies must therefore never be edited, reformatted, annotated, have line
endings normalized, or have notices removed. Project notes belong in Vardheim
documentation, never inside an RFC text file.

## Integrity Lock

- `SHA256SUMS` pins the exact bytes of every `rfc*.txt` file.
- `scripts/verify-rfcs.sh` rejects changed, missing, extra, or corrupted RFC
  text and runs in the normal check gate.
- `SECTION_INDEX.json` binds all 105 RFC hashes and roles to a generated
  section-level inventory; it is checked offline and is not an RFC itself.
- The same generated inventory extracts the normative RFC references from all
  13 published ACME-family documents and rejects any reference without a
  checksum-bound local source.
- `ACME_ERRATA.json` records the reviewed all-status RFC Editor errata snapshot
  without modifying RFC text; it is project evidence, not an RFC itself.
- `.gitattributes` disables text/line-ending normalization for RFC text.
- `scripts/lock-rfcs.sh` makes local working copies read-only as an additional
  guard. Git cannot preserve portable read-only file permissions, so checksums
  and review remain the authoritative protection.
- `CODEOWNERS` explicitly protects this directory when repository branch rules
  require owner review.

When a new normative RFC is intentionally added, download it from the RFC
Editor, verify its provenance, add its untouched bytes, update `SHA256SUMS`,
and review both changes. Never replace an existing published RFC: RFCs are
immutable publications; later corrections are tracked as errata or new RFCs.

## crates.io Exclusion

The repository root is a virtual Cargo workspace and is not published. Every
publishable package lives below `crates/`, outside this directory.
`scripts/check-packages.sh` inspects each generated `.crate` archive and fails
if RFC text or repository image assets are included.
