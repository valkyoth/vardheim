<p align="center">
  <b>Versioned TLS ACME challenge foundations for Vardheim.</b><br>
  Ephemeral identities, exact ALPN routing, strict certificate construction, and durable cleanup boundaries.
</p>

<div align="center">
  <a href="https://crates.io/crates/vardheim">Vardheim crate</a>
  |
  <a href="https://docs.rs/vardheim-challenge-tls">Docs.rs</a>
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

# vardheim-challenge-tls

Support crate for `vardheim`: runtime-independent primitives for current and
future TLS-based ACME challenge methods.

Most users should depend on the facade crate instead:

```toml
[dependencies]
vardheim = "0.1.0"
```

Crates.io: <https://crates.io/crates/vardheim>

This package is published separately so ephemeral validation certificates,
identity stores, and future TLS validation methods remain independent from a
specific TLS stack. Concrete rustls integration belongs in `vardheim-rustls`.

## Current Status

Version `0.1.0` exposes only the registered TLS-ALPN-01 method name as
foundation evidence. It does not construct certificates or terminate TLS yet.

## Security Boundary

Future implementations must use dedicated ephemeral keys, exact `acme-tls/1`
ALPN routing, one matching SAN, a critical `acmeIdentifier`, automatic expiry,
and cleanup isolated from normal website certificates.
