# Vardheim 0.1.0 Release Notes

Status: implementation complete; pending exact-commit pentest

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

## Compatibility

Rust `1.90.0` through `1.97.0` is supported. The current pinned stable
toolchain is Rust `1.97.0`.

## Known Limitations

Vardheim cannot yet discover a directory, manage an account, create an order,
answer a challenge, retrieve a certificate, or deploy a certificate.

The release plan has been tactically split through `0.120.0-rc.5`; each
milestone introduces one reviewable boundary and stops for pentest.
