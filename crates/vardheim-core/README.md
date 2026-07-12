<p align="center">
  <b>Strict no_std ACME protocol foundations for Vardheim.</b><br>
  Bounded types, deterministic protocol semantics, and security-gated conformance evidence.
</p>

<div align="center">
  <a href="https://crates.io/crates/vardheim">Vardheim crate</a>
  |
  <a href="https://docs.rs/vardheim-core">Docs.rs</a>
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

# vardheim-core

Support crate for `vardheim`: dependency-free, runtime-independent ACME
protocol foundations.

Most users should depend on the facade crate instead:

```toml
[dependencies]
vardheim = "0.1.0"
```

Crates.io: <https://crates.io/crates/vardheim>

This package is published separately so Vardheim can keep protocol types, JOSE,
bounded parsing, nonce ownership, and deterministic workflow semantics free
from networking, runtimes, databases, DNS providers, TLS implementations, and
cloud SDKs.

## Current Status

Version `0.1.0` establishes the `no_std`, dependency-free crate boundary.
It does not yet implement RFC 8555 or claim protocol conformance. Every protocol
operation is assigned to a pre-1.0 milestone in the project release plan.

## Security Boundary

This crate must keep untrusted input bounded, reject invalid state transitions,
consume replay nonces exactly once, keep signed URLs exact, and expose typed
effects rather than performing side effects. Unsafe Rust is forbidden.
