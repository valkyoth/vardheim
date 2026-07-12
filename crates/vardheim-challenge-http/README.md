<p align="center">
  <b>Versioned HTTP ACME challenge foundations for Vardheim.</b><br>
  Exact paths, owned presentations, bounded self-checks, and durable cleanup boundaries.
</p>

<div align="center">
  <a href="https://crates.io/crates/vardheim">Vardheim crate</a>
  |
  <a href="https://docs.rs/vardheim-challenge-http">Docs.rs</a>
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

# vardheim-challenge-http

Support crate for `vardheim`: runtime-independent primitives for current and
future HTTP-based ACME challenge methods.

Most users should depend on the facade crate instead:

```toml
[dependencies]
vardheim = "0.1.0"
```

Crates.io: <https://crates.io/crates/vardheim>

This package is published separately so HTTP route stores, webroot adapters,
framework integrations, Redis, self-check networking, and cleanup behavior do
not enter the protocol core. Protocol revisions are modules inside this crate;
HTTP-01 does not determine the permanent package name.

## Current Status

Version `0.1.0` exposes only the registered HTTP-01 method name as foundation
evidence. It does not present or validate challenges yet.

## Security Boundary

Future implementations must enforce exact token paths, identifier binding,
expiry, presentation ownership, restrictive filesystem behavior, bounded
self-checks, and cleanup that cannot remove another workflow's data.
