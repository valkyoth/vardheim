# Vardheim 0.1.0 Release Notes

Status: release candidate; pentest and retest passed, awaiting GitHub checks

## Scope

This foundation release establishes repository policy, `no_std` crate
boundaries, security tooling, documentation, and the Rust compatibility matrix.
It intentionally implements no ACME wire behavior.

## Security

- Unsafe Rust is forbidden in every current crate.
- The dependency graph contains no external crates.
- Every later release requires a pentest before tagging.
- GitHub Actions dependencies are pinned to full commit SHAs.
- RFC reference texts retain their original notices and are integrity-locked,
  owner-reviewed, and excluded from published crate archives.
- Expected failures use typed errors; published libraries leave panic strategy
  and process supervision to the consuming application.
- Potentially truncating and sign-losing cast lints are non-overridable within
  the workspace, while checked arithmetic remains the primary parser control.

## Compatibility

Rust `1.90.0` through `1.97.0` is supported. The current pinned stable
toolchain is Rust `1.97.0`.

## Known Limitations

Vardheim cannot yet discover a directory, manage an account, create an order,
answer a challenge, retrieve a certificate, or deploy a certificate.

The release plan has been tactically split through `0.120.0-rc.5`; each
milestone introduces one reviewable boundary and stops for pentest.

## Pentest

The foundation review raised two low-severity hardening observations covering
release-profile panic blast radius and locally overridable lossy-cast lints.
The panic policy is now application-owned and documented, the cast lints are
forbidden workspace-wide, and the maintainer-supplied retest passed. Permanent
evidence is recorded in `security/pentest/v0.1.0.md`.

The first GitHub run exposed two CI portability defects: Bash scripts were
syntax-checked as POSIX `sh`, and release scripts assumed `rg` was installed.
The syntax gate now selects the interpreter declared by each shebang and fails
if any check fails. Release scripts now use baseline `grep` and `find`, so the
local gate has no undeclared ripgrep dependency.
