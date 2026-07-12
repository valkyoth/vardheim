# Vardheim Version Plan

The normative, deliverable-level plan is
[RELEASE_PLAN.md](RELEASE_PLAN.md). This index makes the complete sequence easy
to audit. Every entry is before `1.0.0`, including experimental draft support.

| Versions | Scope |
| --- | --- |
| `0.1.0-0.4.4` | repository, release enforcement, RFC/IANA evidence and drift, threat/state models, immutable regression evidence and historical replay |
| `0.5.0-0.13.0` | budgets, types, errors, JSON, base64url, JWK/JWA, JWS, EAB, rollover envelopes, nonces |
| `0.14.0-0.25.0` | complete RFC 8555 client protocol |
| `0.26.0-0.31.0` | HTTP-01, CSR, X.509/PKIX verification, alternate chains |
| `0.32.0-0.39.2` | deterministic flow, persistence, stores, deployment, APIs, fault CA, Pebble, historical state and prior-release protocol comparison |
| `0.40.0-0.51.0` | ARI, DNS-01/DNSSEC/providers/agent, TLS-ALPN-01, rustls |
| `0.52.0-0.66.0` | transports, key roles, RustCrypto, ring, aws-lc-rs, FIPS, PKCS#11, TPM2, KMS, remote signing |
| `0.67.0-0.71.2` | CAA, IP identifiers, provider profiles, provider drift replay, controlled conformance, Fluxheim acceptance and FIPS webserver integration |
| `0.72.0-0.81.0` | every published specialist ACME RFC and stable extension registry |
| `0.82.0-0.91.0` | SQLite/PostgreSQL, tenancy, deployers, audit, CLI, daemon, agents |
| `0.92.0-0.97.3` | all target families, release-to-release target comparison, custom target readiness, formal methods, fuzzing, Miri, sanitizers, leakage evidence, model checking, and historical trace replay |
| `0.100.0-0.111.0` | separately versioned active/IESG and selected related draft families |
| `0.119.0-0.119.1` | complete previous-release compatibility gate and final live-upstream drift assessment |
| `0.120.0-alpha.1-rc.5` | API freeze, split interoperability/resilience qualification, reproducibility, split audits, FIPS qualification, final candidate |
| `1.0.0` | first serious production-ready release |

There is no unversioned post-1.0 backlog. New required work receives a new
pre-1.0 milestone and pentest stop.
