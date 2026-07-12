# Vardheim 0.2.0 Release Notes

Status: implementation complete; pending pentest and retest

## Scope

This release enforces the repository's release discipline. It adds no ACME
wire behavior and does not change any support-crate API.

## Added

- Independently versioned workspace crate manifests and a machine-readable
  per-crate release plan.
- Dependency-ordered publication helper with clean-tree, exact-tag, preflight,
  version-confirmation, index-propagation, and safe-resume controls.
- Structured release metadata and exact pentest-evidence validators.
- Version-specific `v0.2.0` release gate.
- Negative tests for missing, malformed, failed, stale, wrong-commit, and
  existing-tag release evidence.
- SPDX SBOM presence and workspace-version validation.

## Publishing

Only `vardheim` advances to `0.2.0`, including its public version marker and
version regression test. The four support crates remain at `0.1.0` because
their published package contents and APIs are unchanged. The facade continues
to depend on those compatible `0.1.0` support releases.

## Security

- A temporary root `PENTEST.md` fails closed.
- Pentest fields must be unique, well-formed, and non-empty.
- `Reviewed-Commit` must be a real 40-hex commit and an ancestor of the release
  candidate.
- `PENDING` and `FAIL` reports cannot pass readiness.
- An existing release tag prevents accidental reuse.
- Real publication has no dirty-tree, untagged, skipped-check, or
  `--no-verify` bypass.
- Multi-package publication refuses non-interactive stdin before the first
  irreversible operation and handles unexpected EOF as a clean failure.
- Clean-tree, tag, and passing review evidence are revalidated immediately
  before every individual crate publication, closing operator-wait TOCTOU
  windows.

## Pentest Remediation

The initial review found one low-severity unattended-EOF failure mode and one
medium TOCTOU window between crate publications. Both are remediated. Permanent
regression tests prove EOF/non-TTY refusal and the exact check/publish/wait/check
ordering for multi-crate releases. A remediation retest is pending.

## Compatibility

Rust `1.90.0` through `1.97.0` remains supported. All crates remain
dependency-free and `no_std`.

## Known Limitations

Vardheim still implements no ACME protocol operation. Protocol work begins
only after the specification and evidence milestones that follow this release.
