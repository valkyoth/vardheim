# Vardheim Version Plan

The normative, deliverable-level plan is
[RELEASE_PLAN.md](RELEASE_PLAN.md). This index makes the complete sequence easy
to audit. Every entry is before `1.0.0`, including experimental draft support.

| Versions | Scope |
| --- | --- |
| `0.1.0-0.4.7` | repository, reviewed-implementation release binding, full errata/reference evidence, reproducible SBOM, cross-target CI, conformance/drift, threat and early TLA+/Quint models, immutable regression replay, pure effect/backend contract, crate/feature topology and build ergonomics |
| `0.5.0-0.13.1` | budgets and early Kani, transient evidence/trust types, errors, bounded JSON and differential fuzzing, base64url, JWK/JWA, provider-neutral digest/sign/verify/entropy/key-generation/public-key-validation/domain-separated `BoundSigner`/local exact-request admission/separate transactional asymmetric-key and symmetric-secret onboarding/typed secret-content binding/fresh live-authority reconstruction/immutable signature and MAC dispatch/mandatory returned-signature verification/verified-versus-provider-asserted-versus-cryptographically-attested MAC evidence/TSIG-MAC/key-disposition and purpose-bound legacy-hash semantics, bounded JWS, EAB, rollover, nonce/admission retry and invalidation-race safety, Kani and Loom |
| `0.14.0-0.25.2` | complete RFC 8555 client protocol including transport semantics, `newNonce`, explicit existing-account adoption, rollover/deactivation key disposition, multi-issuer isolation, and optional `newAuthz` |
| `0.26.0-0.31.3` | HTTP-01, strict DER primitives and certificate-envelope/public-key prevalidation, CSR/TLS Feature, strict PKIX time/DN equality, durable renewal key modes, private test crypto/status/CT/DNSSEC/TSIG, issued-trust snapshots, dedicated PKIX/full RFC 5280, chain-wide OCSP/CRL, distinct CT v1/v2 and Merkle auditing, hardened acquisition/AIA, alternate chains, and context evidence |
| `0.32.0-0.39.5` | deterministic reducer, capability-free snapshots and fresh authority reconstruction, lifecycle/obligation persistence, fenced stores, staple-aware deployment, APIs, conformance, hostile CA, Pebble, historical comparison, adoption, renewal bootstrap, and multi-issuer migration |
| `0.40.0-0.51.5` | ARI, compromise/lifecycle facade, honest key disposition, status/Must-Staple, durable CT inclusion/split-view monitoring, complete authoritative DNS discovery plus EDNS/source-port/TCP/Cookies and DNSSEC/NSEC/NSEC3, RFC 2136/TSIG contracts, providers/agent, TLS-ALPN-01, rustls/OpenSSL stapling, and web-server acceptance |
| `0.52.0-0.66.5` | ACME/public-PKI/CT-audit transports with framing/privacy/cache/protocol/replay isolation, explicit HTTP/1.1/2/3 profiles and disabled early data, custom/platform issued trust, transactional asymmetric-key and symmetric-secret import/generation/adoption/migration, purpose-specific crypto, signer/MAC validation/content-binding/admission/onboarding/reconstruction/immutable-dispatch/signature-verification/MAC-assertion-attestation/disposition conformance, RustCrypto EAB/RSA-PSS/legacy/DNSSEC/TSIG, production RFC 2136, ring/aws-lc/FIPS capability tables, hardware/KMS/secret-manager/remote signing and MAC providers |
| `0.67.0-0.71.2` | CAA, IP identifiers, provider profiles, provider drift replay, controlled conformance, Fluxheim acceptance and FIPS webserver integration |
| `0.72.0-0.81.0` | every published specialist ACME RFC and stable extension registry, with authority-token local signing bound to immutable dispatch and verified signatures |
| `0.82.0-0.91.6` | SQLite/PostgreSQL, tenancy, deployers, verified-signature-only signed audit, CLI, daemon, agents, Android/Apple/Windows key-store transactional onboarding/reconstruction/immutable-dispatch/output-verification/disposition, and PKCS#12 interoperability |
| `0.92.0-0.97.3` | all target families, release-to-release target comparison, custom target readiness, Kani/Loom/fuzz/model qualification closure, Miri, sanitizers, leakage evidence, and historical formal-trace replay |
| `0.100.0-0.111.0` | separately versioned active/IESG and selected related draft families |
| `0.119.0-0.119.1` | complete previous-release compatibility gate and final live-upstream drift assessment |
| `0.120.0-alpha.1-rc.5` | API freeze, split interoperability/resilience qualification, reproducibility, split audits, FIPS qualification, final candidate |
| `1.0.0` | first serious production-ready release |

There is no unversioned post-1.0 backlog. New required work receives a new
pre-1.0 milestone and pentest stop.
