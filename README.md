<p align="center">
  <b>Security-first ACME and certificate lifecycle foundations for Rust.</b><br>
  Strict protocol boundaries, durable workflow planning, no_std portability, and security-gated release evidence.
</p>

<div align="center">
  <a href="https://crates.io/crates/vardheim">Crates.io</a>
  |
  <a href="https://docs.rs/vardheim">Docs.rs</a>
  |
  <a href="https://github.com/valkyoth/vardheim/blob/main/docs/RELEASE_PLAN.md">Release Plan</a>
  |
  <a href="https://github.com/valkyoth/vardheim/blob/main/docs/threat-model.md">Threat Model</a>
  |
  <a href="https://github.com/valkyoth/vardheim/blob/main/SECURITY.md">Security</a>
</div>

<br>

<p align="center">
  <a href="https://github.com/valkyoth/vardheim">
    <img src="https://raw.githubusercontent.com/valkyoth/vardheim/main/.github/images/vardheim.webp" alt="Vardheim Rust crate overview">
  </a>
</p>

# vardheim

`vardheim` is a `no_std`-first Rust workspace for security-focused ACME and
certificate lifecycle building blocks.

The project target is a serious production-ready certificate lifecycle
framework at `1.0.0`, reached through small releases with explicit RFC,
security, compatibility, dependency, testing, and pentest evidence. Protocol
logic remains separate from networking, runtimes, cryptographic providers,
challenge presentation, persistent storage, and certificate deployment.

## Current Status

Status: `v0.1.0` release candidate; pentest and retest passed, awaiting GitHub
checks.

Vardheim does not issue, validate, renew, revoke, or deploy certificates yet.
The current release establishes the crate boundaries and enforcement needed
before security-sensitive protocol implementation begins.

Implemented now:

- Rust workspace pinned to stable `1.97.0`.
- MSRV policy and verified checks for Rust `1.90.0` through `1.97.0`.
- Dependency-free `no_std` facade, core, and challenge-family crates.
- Future-proof HTTP, DNS, and TLS challenge crate boundaries.
- Workspace-wide `#![forbid(unsafe_code)]`.
- Maximum 500-line policy for every Rust source file.
- MIT OR Apache-2.0 licensing.
- GitHub CI, CODEOWNERS, funding, Dependabot, and SHA-pinned Actions.
- GitHub CodeQL Default setup policy.
- cargo-deny, cargo-audit, package, documentation, and SPDX SBOM gates.
- Mandatory exact-commit pentest stop before every release tag.
- Complete implementation and version plan through `1.0.0`.
- Tracked, byte-locked reference copies of all required RFC texts, excluded
  from published crates.
- Linux, Windows, BSD, macOS, Android, iOS, and future custom-target
  architecture requirements.

Not implemented yet:

- No ACME directory or account operations.
- No JOSE, JWK, JWS, EAB, or nonce implementation.
- No order, authorization, challenge, finalization, or revocation workflow.
- No CSR or certificate parsing and verification.
- No HTTP, DNS, TLS, cryptographic, storage, or deployment backend.
- No durable orchestration, CLI, daemon, or remote agent.
- No stable RFC conformance claim.

Every missing item has a concrete pre-1.0 version in the
[release plan](https://github.com/valkyoth/vardheim/blob/main/docs/RELEASE_PLAN.md).
There is no unversioned post-1.0 backlog for known requirements.

## Trust Dashboard

| Area | Status |
| --- | --- |
| License | `MIT OR Apache-2.0` |
| MSRV | Rust `1.90.0` |
| Pinned toolchain | Rust `1.97.0` |
| Default target | `no_std` |
| External dependencies | zero |
| Unsafe policy | first-party crates use `#![forbid(unsafe_code)]` |
| Default networking | none |
| Default cryptographic backend | none |
| Maximum Rust source size | 500 physical lines |
| Release evidence | checks, deny, audit, SBOM, exact-commit pentest |
| Panic policy | application-owned; expected failures use typed errors |
| Current RFC conformance | none claimed |
| 1.0 target | complete production-ready ACME lifecycle framework |

## Install

The crate is not published yet. After the first release:

```toml
[dependencies]
vardheim = "0.1.0"
```

Most users should depend only on `vardheim`. Lower-level crates exist for
applications that need direct protocol or challenge-family boundaries.

## Workspace Crates

| Crate | Responsibility |
| --- | --- |
| `vardheim` | public facade and common re-exports |
| `vardheim-core` | bounded, runtime-independent ACME protocol foundations |
| `vardheim-challenge-http` | current and future HTTP challenge methods |
| `vardheim-challenge-dns` | current and future DNS challenge methods |
| `vardheim-challenge-tls` | current and future TLS challenge methods |

The challenge crate names intentionally do not contain protocol revision
numbers. For example, `dns-01` and a future `dns-02` belong to versioned
modules inside `vardheim-challenge-dns`, not separate packages.

`vardheim-rustls` is assigned to version `0.51.0`, after the generic TLS
challenge identity boundary is complete.

## Rust Version Support

The minimum supported Rust version is `1.90.0`. New development and release
verification use pinned stable Rust `1.97.0`.

| Rust | Required evidence |
| --- | --- |
| `1.90.0` | `cargo check --workspace --all-features` |
| `1.91.0` | `cargo check --workspace --all-features` |
| `1.92.0` | `cargo check --workspace --all-features` |
| `1.93.0` | `cargo check --workspace --all-features` |
| `1.94.0` | `cargo check --workspace --all-features` |
| `1.95.0` | `cargo check --workspace --all-features` |
| `1.96.0` | `cargo check --workspace --all-features` |
| `1.96.1` | `cargo check --workspace --all-features` |
| `1.97.0` | full local and release gates |

## Platform Policy

Runtime-independent crates must remain portable across Linux, Windows, BSD,
macOS, Android, iOS, and custom `no_std` targets. Platform-specific adapters
live outside the core and fail closed on unsupported targets. Clocks, entropy,
networking, storage, signing, allocation, and deployment remain injectable so a
future custom operating system is not locked out.

## Security And Release Policy

Every release, including patches and release candidates, stops for an
independent pentest of the exact implementation commit. A tag cannot pass the
release gate without a permanent `Status: PASS` report.

Read:

- [Architecture](https://github.com/valkyoth/vardheim/blob/main/docs/architecture.md)
- [Implementation plan](https://github.com/valkyoth/vardheim/blob/main/docs/IMPLEMENTATION_PLAN.md)
- [Release plan](https://github.com/valkyoth/vardheim/blob/main/docs/RELEASE_PLAN.md)
- [Longitudinal regression strategy](https://github.com/valkyoth/vardheim/blob/main/docs/REGRESSION_STRATEGY.md)
- [ACME completeness contract](https://github.com/valkyoth/vardheim/blob/main/docs/COMPLETENESS.md)
- [RFC inventory](https://github.com/valkyoth/vardheim/blob/main/docs/RFC_INVENTORY.md)
- [Threat model](https://github.com/valkyoth/vardheim/blob/main/docs/threat-model.md)
- [Security controls](https://github.com/valkyoth/vardheim/blob/main/docs/security-controls.md)
- [Compatibility](https://github.com/valkyoth/vardheim/blob/main/docs/compatibility.md)
- [Release process](https://github.com/valkyoth/vardheim/blob/main/docs/release-process.md)

## Development

```bash
scripts/checks.sh
scripts/check-rust-version-matrix.sh
cargo deny check
cargo audit
scripts/generate-sbom.sh
```

The networked freshness check verifies pinned Cargo tools and GitHub Actions:

```bash
scripts/check_latest_tools.sh
```

## License

Licensed under either of:

- Apache License, Version 2.0
- MIT License

at your option.
