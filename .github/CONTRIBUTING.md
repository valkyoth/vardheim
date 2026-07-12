# Contributing To Vardheim

Vardheim is security-sensitive ACME and certificate-lifecycle infrastructure.
Contributions must keep the workspace explicit, testable, `no_std`-first, and
honest about implemented conformance.

## License

Vardheim is licensed under either MIT or Apache-2.0, at your option. Unless you
state otherwise, contributions intentionally submitted for inclusion are dual
licensed under those terms.

## Development Setup

Use the pinned Rust toolchain from `rust-toolchain.toml`.

```bash
cargo check --workspace --all-features
cargo test --workspace --all-features
scripts/checks.sh
```

## Security-Sensitive Changes

Treat protocol parsing, JOSE, nonces, URLs, state transitions, identifiers,
certificate verification, challenge cleanup, persistence, deployment, key
handling, CI, release scripts, and dependencies as high risk.

Do not post exploitable details in public issues. Follow
[SECURITY.md](../SECURITY.md).

## Dependency Policy

Before adding or updating a crate, verify its latest stable version, MSRV,
license, maintenance, features, `no_std` impact, unsafe code, and transitive
graph. Run `cargo deny check` and `cargo audit`, and record the admission
rationale in `docs/dependency-policy.md`.
