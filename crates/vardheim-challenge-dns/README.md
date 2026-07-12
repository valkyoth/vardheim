<p align="center">
  <b>Versioned DNS ACME challenge foundations for Vardheim.</b><br>
  Exact record ownership, authoritative visibility, DNSSEC policy, and durable cleanup boundaries.
</p>

<div align="center">
  <a href="https://crates.io/crates/vardheim">Vardheim crate</a>
  |
  <a href="https://docs.rs/vardheim-challenge-dns">Docs.rs</a>
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

# vardheim-challenge-dns

Support crate for `vardheim`: runtime-independent primitives for current and
future DNS-based ACME challenge methods.

Most users should depend on the facade crate instead:

```toml
[dependencies]
vardheim = "0.1.0"
```

Crates.io: <https://crates.io/crates/vardheim>

This package is published separately so DNS resolution, DNSSEC, provider APIs,
cloud SDKs, propagation checks, and remote validation agents do not enter the
protocol core. Protocol revisions are modules inside this crate; DNS-01 and a
future DNS revision share the same package boundary.

## Current Status

Version `0.1.0` exposes only the registered DNS-01 method name as foundation
evidence. It does not calculate TXT values or change DNS records yet.

## Security Boundary

Future implementations must preserve unrelated TXT values, identify exact
record ownership, handle CNAME/NS delegation, query authoritative servers,
represent DNSSEC results honestly, scope credentials narrowly, and persist
cleanup obligations.
