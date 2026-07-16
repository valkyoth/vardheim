# Vardheim Version Plan

The normative, deliverable-level plan is
[RELEASE_PLAN.md](RELEASE_PLAN.md). This index makes the complete sequence easy
to audit. Every entry is before `1.0.0`, including experimental draft support.

| Versions | Scope |
| --- | --- |
| `0.1.0-0.4.7` | repository, reviewed-implementation release binding, full errata/reference evidence, reproducible SBOM, cross-target CI, conformance/drift, threat and early TLA+/Quint models, immutable regression replay, pure effect/backend contract, crate/feature topology and build ergonomics |
| `0.5.0-0.13.1` | budgets and early Kani, types/evidence, errors, bounded borrowed JSON and differential fuzzing, base64url, JWK/JWA, provider-neutral digest/sign/verify/entropy/key-generation semantics, bounded JWS, EAB, rollover envelopes, nonces and early Loom |
| `0.14.0-0.25.2` | complete RFC 8555 client protocol including transport semantics, `newNonce`, multi-issuer isolation, and optional `newAuthz` |
| `0.26.0-0.31.2` | HTTP-01, DER writer/reader and algorithm identifiers before CSR, test-only real crypto, dedicated `vardheim-pkix`, full RFC 5280, OCSP/CRL/CT/AIA, alternate chains and evidence bridge |
| `0.32.0-0.39.5` | deterministic effect reducer with model/Kani replay, persistence, stores and early Loom, deployment, APIs, shared adapter conformance, hostile fault CA, test transport, Pebble, historical protocol comparison, certificate adoption, renewal bootstrap, and multi-issuer migration |
| `0.40.0-0.51.3` | ARI, compromise response, certificate retirement/inventory/status lifecycle, DNS query adapter and DNS-01/DNSSEC/providers/agent, TLS-ALPN-01, rustls, OpenSSL, and web-server acceptance |
| `0.52.0-0.66.2` | transports, purpose-specific crypto capabilities, RustCrypto including EAB HMAC/RSA-PSS, ring, aws-lc-rs, FIPS, PKCS#11, TPM2, KMS, remote signing, and offline rollover ceremony |
| `0.67.0-0.71.2` | CAA, IP identifiers, provider profiles, provider drift replay, controlled conformance, Fluxheim acceptance and FIPS webserver integration |
| `0.72.0-0.81.0` | every published specialist ACME RFC and stable extension registry |
| `0.82.0-0.91.6` | SQLite/PostgreSQL, tenancy, deployers, audit, CLI, daemon, agents, Android/Apple/Windows key stores, and PKCS#12 interoperability |
| `0.92.0-0.97.3` | all target families, release-to-release target comparison, custom target readiness, Kani/Loom/fuzz/model qualification closure, Miri, sanitizers, leakage evidence, and historical formal-trace replay |
| `0.100.0-0.111.0` | separately versioned active/IESG and selected related draft families |
| `0.119.0-0.119.1` | complete previous-release compatibility gate and final live-upstream drift assessment |
| `0.120.0-alpha.1-rc.5` | API freeze, split interoperability/resilience qualification, reproducibility, split audits, FIPS qualification, final candidate |
| `1.0.0` | first serious production-ready release |

There is no unversioned post-1.0 backlog. New required work receives a new
pre-1.0 milestone and pentest stop.
