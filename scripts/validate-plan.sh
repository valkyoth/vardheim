#!/usr/bin/env bash
set -euo pipefail

plan="docs/RELEASE_PLAN.md"
versions="$(sed -n 's/^| `\(v[^`]*\)` |.*/\1/p' "$plan")"

if [[ -z "$versions" ]]; then
    echo "release plan has no version rows" >&2
    exit 1
fi

while IFS= read -r version; do
    if [[ ! "$version" =~ ^v(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)(-(alpha|beta|rc)\.(0|[1-9][0-9]*))?$ ]]; then
        echo "invalid planned semantic version: $version" >&2
        exit 1
    fi
done <<< "$versions"

duplicates="$(printf '%s\n' "$versions" | sort | uniq -d)"
if [[ -n "$duplicates" ]]; then
    echo "duplicate planned versions:" >&2
    printf '%s\n' "$duplicates" >&2
    exit 1
fi

required=(
    v0.3.2
    v0.3.3
    v0.3.4
    v0.3.5
    v0.3.6
    v0.3.7
    v0.3.8
    v0.3.9
    v0.4.4
    v0.4.5
    v0.4.6
    v0.4.7
    v0.4.8
    v0.4.9
    v0.4.10
    v0.4.11
    v0.4.12
    v0.4.13
    v0.4.14
    v0.4.15
    v0.4.16
    v0.4.17
    v0.4.18
    v0.4.19
    v0.4.20
    v0.4.21
    v0.4.22
    v0.4.23
    v0.4.24
    v0.4.25
    v0.4.26
    v0.4.27
    v0.5.2
    v0.6.5
    v0.6.6
    v0.6.7
    v0.7.2
    v0.7.3
    v0.10.2
    v0.10.3
    v0.10.4
    v0.10.5
    v0.10.6
    v0.10.7
    v0.10.8
    v0.10.9
    v0.10.10
    v0.10.11
    v0.10.12
    v0.10.13
    v0.10.14
    v0.10.15
    v0.10.16
    v0.10.17
    v0.10.18
    v0.10.19
    v0.10.20
    v0.10.21
    v0.10.22
    v0.10.23
    v0.10.24
    v0.10.25
    v0.10.26
    v0.10.27
    v0.10.28
    v0.13.1
    v0.14.2
    v0.14.3
    v0.15.2
    v0.16.3
    v0.16.4
    v0.18.1
    v0.19.3
    v0.20.3
    v0.20.4
    v0.25.2
    v0.27.5
    v0.28.1
    v0.28.2
    v0.28.3
    v0.28.4
    v0.28.5
    v0.28.6
    v0.28.7
    v0.28.8
    v0.28.9
    v0.28.10
    v0.28.11
    v0.28.12
    v0.28.13
    v0.28.14
    v0.29.3
    v0.29.4
    v0.29.5
    v0.30.7
    v0.30.8
    v0.30.9
    v0.30.10
    v0.30.11
    v0.30.12
    v0.30.13
    v0.30.14
    v0.30.15
    v0.30.16
    v0.30.17
    v0.30.18
    v0.30.19
    v0.30.20
    v0.30.21
    v0.30.22
    v0.30.23
    v0.30.24
    v0.30.25
    v0.30.26
    v0.30.27
    v0.30.28
    v0.31.2
    v0.31.3
    v0.33.3
    v0.33.4
    v0.33.5
    v0.33.6
    v0.33.7
    v0.33.8
    v0.33.9
    v0.34.3
    v0.36.3
    v0.37.4
    v0.37.5
    v0.38.3
    v0.38.4
    v0.38.5
    v0.39.2
    v0.39.3
    v0.39.4
    v0.39.5
    v0.41.2
    v0.41.3
    v0.41.4
    v0.41.5
    v0.41.6
    v0.41.7
    v0.41.8
    v0.41.9
    v0.41.10
    v0.41.11
    v0.41.12
    v0.42.1
    v0.42.2
    v0.42.3
    v0.42.4
    v0.42.5
    v0.42.6
    v0.42.7
    v0.43.3
    v0.44.1
    v0.44.2
    v0.44.3
    v0.44.4
    v0.44.5
    v0.44.6
    v0.44.7
    v0.44.8
    v0.44.9
    v0.44.10
    v0.44.11
    v0.44.12
    v0.44.13
    v0.45.0
    v0.45.1
    v0.45.2
    v0.45.3
    v0.51.2
    v0.51.4
    v0.51.5
    v0.52.3
    v0.52.4
    v0.52.5
    v0.52.6
    v0.52.7
    v0.52.8
    v0.53.2
    v0.53.3
    v0.56.0
    v0.56.1
    v0.56.5
    v0.56.6
    v0.56.7
    v0.56.8
    v0.56.9
    v0.56.10
    v0.56.11
    v0.56.12
    v0.56.13
    v0.57.5
    v0.57.6
    v0.57.7
    v0.57.8
    v0.57.9
    v0.57.10
    v0.57.11
    v0.57.12
    v0.57.13
    v0.58.1
    v0.58.2
    v0.59.1
    v0.59.2
    v0.60.0
    v0.60.1
    v0.61.2
    v0.61.3
    v0.62.2
    v0.62.3
    v0.63.1
    v0.63.2
    v0.64.1
    v0.64.2
    v0.65.1
    v0.65.2
    v0.66.3
    v0.66.4
    v0.66.5
    v0.69.3
    v0.71.1
    v0.71.2
    v0.81.0
    v0.91.3
    v0.91.4
    v0.91.5
    v0.91.6
    v0.92.5
    v0.92.6
    v0.96.4
    v0.97.3
    v0.100.0
    v0.111.0
    v0.119.0
    v0.119.1
    v0.120.0-rc.5
    v1.0.0
)

for version in "${required[@]}"; do
    if ! grep -qx "$version" <<< "$versions"; then
        echo "required completeness milestone missing: $version" >&2
        exit 1
    fi
done

grep -q '^## Tactical Milestone Size Rule$' "$plan"
grep -q 'Complete offline errata evidence' "$plan"
grep -q 'Release evidence binding' "$plan"
grep -q 'Reproducible SPDX SBOM generation' "$plan"
grep -q 'Core cross-target CI baseline' "$plan"
grep -q 'Backend-boundary contract' "$plan"
grep -q 'Crate and feature topology contract' "$plan"
grep -q 'Machine-readable roadmap and requirement-work graph' "$plan"
grep -q 'Unpublished RustCrypto signer/verifier feasibility spike' "$plan"
grep -q 'Unpublished ring signer/verifier feasibility spike' "$plan"
grep -q 'Unpublished rustls resolver and ACME transport feasibility spike' "$plan"
grep -q 'Unpublished executor-mode feasibility spike' "$plan"
grep -q 'Unpublished memory-store and SQL-like transaction feasibility spike' "$plan"
grep -q 'Machine-readable crate policy tiers' "$plan"
grep -q 'Independent replay-nonce linear-authority formal model' "$plan"
grep -q 'Independent request-admission/sign/verify/finalize/commit/dispatch formal model' "$plan"
grep -q 'Independent challenge-presentation ownership formal model' "$plan"
grep -q 'Independent order/authorization aggregation formal model' "$plan"
grep -q 'Independent transactional-outbox ambiguity formal model' "$plan"
grep -q 'Independent lease, fencing, and once-only application formal model' "$plan"
grep -q 'Independent deployment formal model' "$plan"
grep -q 'Independent renewal formal model' "$plan"
grep -q 'Semantic module-invariant and complexity gate' "$plan"
grep -q 'Security mutation-testing baseline' "$plan"
grep -q 'Executable no-allocation and executor-contract proof' "$plan"
grep -q 'Unpublished safe `no_std` DER/PKIX feasibility and build-versus-adopt decision' "$plan"
grep -q 'Generic executor authority confinement' "$plan"
grep -q 'Provider-neutral `RemoteProtocolCapabilities` product' "$plan"
grep -q 'Linear replay-authority taxonomy' "$plan"
grep -q 'Sealed observation-to-evidence promotion pipeline' "$plan"
grep -q 'Optional native `SecretMemory` assurance boundary' "$plan"
grep -q 'Layered stable error envelope' "$plan"
grep -q 'Orthogonal effect-observation product shared by every backend boundary' "$plan"
grep -q 'Strict signature-evidence and multi-axis verifier-assurance invariant' "$plan"
grep -q 'Provider-neutral security-sensitive identity semantics and issuer interfaces' "$plan"
grep -q 'Core-only/no-store tests mint transient admissions' "$plan"
grep -q 'Immutable canonical `PolicySnapshot`.*`EffectDispatchPermit`' "$plan"
grep -q 'Request-identity taxonomy separating.*`LocalSigningRequestId`.*`ProtocolRequestId`' "$plan"
grep -q 'Purpose-specific effect-dispatch authority composition' "$plan"
grep -q 'Consuming two-stage protocol request identity' "$plan"
grep -q 'Sealed purpose-specific effect fingerprints replace generic byte/semantic digests' "$plan"
grep -q 'Authenticated replay-nonce admission and reservation policy' "$plan"
grep -q 'Conflict-checked challenge-method registry' "$plan"
grep -q 'Shared sealed challenge-presentation receipt envelope' "$plan"
grep -q 'System-wide rollback discontinuity and restored-store recovery model' "$plan"
grep -q 'Injected external `RollbackWitness` protocol' "$plan"
grep -q '`RollbackDetecting { maximum_window }`' "$plan"
grep -q 'witness trust root, bootstrap identity' "$plan"
grep -q 'Typed `RollbackCoverage` manifest' "$plan"
grep -q 'Transactional durable identity allocator integrated with store' "$plan"
grep -q 'Private thin real-boundary vertical slice' "$plan"
grep -q 'Reusable strict signature-evidence and multi-axis verifier-assurance conformance' "$plan"
grep -q 'four-level evidence publication' "$plan"
grep -q 'Pre-production security mutation qualification' "$plan"
grep -q 'Provider-neutral digest semantics' "$plan"
grep -q 'Narrow legacy-hash compatibility capability' "$plan"
grep -q 'Provider-neutral `DnsUpdateMac` operation semantics' "$plan"
grep -q 'Provider-neutral key-disposition request' "$plan"
grep -q 'Provider-neutral public-key validation contract' "$plan"
grep -q 'Domain-separated signer-binding ceremony producing transient non-serializable `BoundSigner`' "$plan"
grep -q 'Local request-specific signer-consumer admission contract over `&mut BoundSigner`' "$plan"
grep -q 'Provider-neutral transactional key-onboarding state model' "$plan"
grep -q 'Invalidation observed before dispatch prevents signing' "$plan"
grep -q 'Live key-authority reconstruction boundary' "$plan"
grep -q 'Provider-neutral immutable-dispatch and verified-signature commit boundary' "$plan"
grep -q 'Provider-neutral handle-backed MAC authority and positive-evidence boundary' "$plan"
grep -q 'Provider-neutral transactional symmetric-secret onboarding and content-binding state model' "$plan"
grep -q 'Live symmetric-secret authority reconstruction boundary' "$plan"
grep -q 'Narrow symmetric-secret content-binding bootstrap authority' "$plan"
grep -q 'Provider-neutral peer-binding external-effect identity and observation contract' "$plan"
grep -q 'Durable peer-binding effect orchestration and recovery' "$plan"
grep -q 'Orthogonal peer-effect outcome product and recovery matrix' "$plan"
grep -q 'Composed EAB account-creation typestate' "$plan"
grep -q 'Durable composed EAB account-creation execution and recovery' "$plan"
grep -q 'KeyLifecycleState × KeyObligationSet' "$plan"
grep -q 'Account creation with contacts.*v0.10.12' "$plan"
grep -q '`onlyReturnExisting` account recovery.*v0.10.12' "$plan"
grep -q 'Account key rollover.*v0.10.12' "$plan"
grep -q 'Complete revocation:.*v0.10.12' "$plan"
grep -q 'RFC 2986 CSR construction.*v0.10.12' "$plan"
grep -q 'TLS-ALPN-01 identity construction.*v0.10.12' "$plan"
grep -q 'RFC 2986 CSR construction.*v0.10.15.*VerifiedSignature' "$plan"
grep -q 'TLS-ALPN-01 identity construction.*v0.10.15.*VerifiedSignature' "$plan"
grep -q 'Single-use replay nonce ownership integrated with request admission and `v0.10.27`' "$plan"
grep -q '`badNonce` retry consumes the old nonce, reservation/input-bound/final-wire state' "$plan"
grep -q 'Complete `newNonce` operation' "$plan"
grep -q 'Explicit existing-account adoption' "$plan"
grep -q 'Durable old account-key lifecycle' "$plan"
grep -q 'Optional RFC 8555 `newAuthz` pre-authorization' "$plan"
grep -q 'Introduce the dependency-light `vardheim-pkix` crate' "$plan"
grep -q 'Canonical bounded DER writer' "$plan"
grep -q 'Private test-only reference crypto primitives' "$plan"
grep -q 'Private test-only PKIX evidence verifier extension' "$plan"
grep -q 'Private test-only DNSSEC verifier extension' "$plan"
grep -q 'Private test-only `DnsUpdateMac` implementation' "$plan"
grep -q 'Strict bounded ASN.1/PKIX time parser' "$plan"
grep -q 'RFC 5280 distinguished-name equality and normalization' "$plan"
grep -q 'Strict DER primitive/constructed conformance layer' "$plan"
grep -q 'X.509 certificate-envelope structural prevalidation' "$plan"
grep -q 'JWK/SPKI/CSR/certificate public-key validation integration' "$plan"
grep -q 'Durable certificate-key renewal/rotation policy' "$plan"
grep -q '`CertificateTrustProvider` load/reload contract' "$plan"
grep -q 'Complete RFC 5280 certificate-policy processing' "$plan"
grep -q 'Core-to-PKIX evidence bridge' "$plan"
grep -q 'Validation-session-bound PKIX capabilities' "$plan"
grep -q 'Bounded OCSP request encoding and response decoding' "$plan"
grep -q 'Bounded CRL and `TBSCertList` parsing' "$plan"
grep -q 'Bounded RFC 6962 CT v1 SCT-list parsing' "$plan"
grep -q 'Bounded RFC 9162 CT v2 `TransItem`' "$plan"
grep -q 'Local RFC 9162 CT v2 signature-input' "$plan"
grep -q 'Complete RFC 6960 OCSP extension' "$plan"
grep -q 'Chain-wide certificate-status policy' "$plan"
grep -q 'OCSP acquisition privacy policy' "$plan"
grep -q 'Public-PKI HTTP representation and framing policy' "$plan"
grep -q 'Purpose-specific public-PKI representation and cache contract' "$plan"
grep -q 'Optional RFC 9162 CT v2 acquisition and policy integration' "$plan"
grep -q 'RFC 6962 CT v1 Merkle audit primitives' "$plan"
grep -q 'RFC 9162 CT v2 Merkle audit primitives' "$plan"
grep -q 'Provider-neutral version-aware CT audit acquisition contract' "$plan"
grep -q 'Provider-neutral `PublicPkiFetch` contract' "$plan"
grep -q 'Snapshot restoration and capability-reconstruction boundary' "$plan"
grep -q 'BoundMacKey.*MacConsumerAdmission.*VerifiedMac.*ProviderAssertedMac.*CryptographicallyAttestedMac' "$plan"
grep -q 'Optional OCSP-staple deployment artifact contract' "$plan"
grep -q 'Existing certificate adoption' "$plan"
grep -q 'Certificate-key compromise response' "$plan"
grep -q 'Certificate generation retirement state machine' "$plan"
grep -q 'RFC 7633 TLS Feature/Must-Staple lifecycle policy' "$plan"
grep -q 'High-level lifecycle facade methods' "$plan"
grep -q 'Durable CT inclusion-monitoring state machine' "$plan"
grep -q 'Optional independent CT witness/gossip evidence' "$plan"
grep -q 'Provider-neutral bounded DNS query contract' "$plan"
grep -q 'Bounded EDNS(0) OPT construction/parsing' "$plan"
grep -q 'EDNS query-attempt policy' "$plan"
grep -q 'UDP DNS source-port and complete response-correlation policy' "$plan"
grep -q 'Bounded DNS-over-TCP codec and correlation' "$plan"
grep -q 'Optional RFC 7873/9018 DNS Cookies profile' "$plan"
grep -q 'Complete bounded authoritative discovery semantics' "$plan"
grep -q 'Production `std` wall/monotonic clock adapter' "$plan"
grep -q 'Canonical DNSSEC owner-name and RRset serialization' "$plan"
grep -q 'Local DS-to-DNSKEY digest and key-tag verification' "$plan"
grep -q 'Local RRSIG cryptographic verification' "$plan"
grep -q 'RFC 5155 NSEC3 authenticated denial' "$plan"
grep -q 'DNSSEC trust-anchor provisioning' "$plan"
grep -q 'Validating-resolver evidence policy' "$plan"
grep -q 'Production `std` `PublicPkiFetch` adapter' "$plan"
grep -q 'Provider-neutral RFC 2136 UPDATE wire/state model' "$plan"
grep -q 'RFC 8945 TSIG record and canonical MAC-input construction' "$plan"
grep -q 'TSIG secret lifecycle and rotation' "$plan"
grep -q 'Production custom issued-certificate trust provider' "$plan"
grep -q 'Production `PublicPkiFetch` HTTP framing' "$plan"
grep -q 'Production version-aware CT audit HTTP adapter' "$plan"
grep -q 'Transport protocol-version and replay-safety contract' "$plan"
grep -q 'Optional explicit RFC 9113 HTTP/2 ACME transport profile' "$plan"
grep -q 'Optional explicit RFC 9114 HTTP/3 ACME transport profile' "$plan"
grep -q 'Explicit and separate capability sets' "$plan"
grep -q 'Optional default-off migration import' "$plan"
grep -q 'Reusable key-disposition provider conformance' "$plan"
grep -q 'Reusable public-key validation, `BoundSigner`, request-admission, and provider conformance framework' "$plan"
grep -q 'Reusable transactional key-onboarding and live-authority-reconstruction provider/import conformance framework' "$plan"
grep -q 'Reusable immutable-dispatch and returned-signature verification conformance framework' "$plan"
grep -q 'Reusable handle-backed MAC authority/evidence conformance framework' "$plan"
grep -q 'Reusable transactional symmetric-secret onboarding, content-binding, and live-authority reconstruction conformance' "$plan"
grep -q 'Reusable secret-binding bootstrap and peer-effect conformance' "$plan"
grep -q 'Reusable composed-authenticated-effect conformance' "$plan"
grep -q 'PKCS#11 transactional key creation/import onboarding, fresh-session authority reconstruction' "$plan"
grep -q 'AWS KMS signer/key provider with transactional onboarding, fresh-session authority reconstruction' "$plan"
grep -q 'AWS KMS HMAC operation provider.*v0.10.16.*v0.56.10' "$plan"
grep -q 'AWS KMS HMAC key create/import/adopt onboarding and reconstruction.*v0.56.11' "$plan"
grep -q 'TPM reset/recovery, transactional persistent/transient key onboarding, fresh-session authority reconstruction' "$plan"
grep -q 'TPM 2.0 keyed-hash/HMAC operation provider.*v0.10.16.*v0.56.10' "$plan"
grep -q 'TPM keyed-hash secret creation/import/adoption onboarding and reconstruction.*v0.56.11' "$plan"
grep -q 'Azure Key Vault signer/key provider with transactional onboarding, fresh-session authority reconstruction' "$plan"
grep -q 'Azure Key Vault/Managed HSM handle-backed MAC operation capability closure.*v0.10.16.*v0.56.10' "$plan"
grep -q 'Azure Key Vault/Managed HSM symmetric-secret onboarding capability closure.*v0.56.11' "$plan"
grep -q 'OpenBao-compatible remote signer/key provider with authenticated transport, transactional onboarding, fresh-session authority reconstruction' "$plan"
grep -q 'OpenBao-compatible transit HMAC operation provider.*v0.10.16.*v0.56.10' "$plan"
grep -q 'OpenBao-compatible transit HMAC create/import/adopt onboarding and reconstruction.*v0.56.11' "$plan"
grep -q 'PKCS#11 handle-backed EAB/TSIG HMAC operation provider.*v0.10.16.*v0.56.10' "$plan"
grep -q 'PKCS#11 symmetric-secret create/import/adopt onboarding and fresh binding reconstruction.*v0.56.11' "$plan"
grep -q 'Generic authenticated remote MAC operation protocol' "$plan"
grep -q 'Reference remote MAC operation agent' "$plan"
grep -q 'Generic remote MAC protocol/agent transactional secret onboarding and fresh authority reconstruction.*v0.56.11' "$plan"
grep -q 'Android Keystore key-provider adapter with transactional generation/import/adoption, fresh-session authority reconstruction' "$plan"
grep -q 'Bounded SPKI/PKCS#8 import/export policy.*v0.10.13' "$plan"
grep -q 'Optional default-off migration import.*v0.10.13' "$plan"
grep -q 'AWS KMS signer/key provider with transactional onboarding' "$plan"
grep -q 'Android Keystore key-provider adapter with transactional generation/import/adoption, fresh-session authority reconstruction' "$plan"
grep -q 'RustCrypto DNSSEC verifier capabilities' "$plan"
grep -q 'RustCrypto `DnsUpdateMac` operation backend' "$plan"
grep -q 'Production RFC 2136 DNS provider adapter' "$plan"
grep -q 'EAB nested JWS construction through `v0.10.16`-`v0.10.21`' "$plan"
grep -q 'TSIG record and canonical MAC-input construction.*v0.10.16.*v0.10.21' "$plan"
grep -q 'RustCrypto/software symmetric-secret create/import/adopt onboarding.*v0.56.11' "$plan"
grep -q 'ring symmetric-secret onboarding/content-binding profile.*v0.56.11' "$plan"
grep -q 'aws-lc-rs non-FIPS symmetric-secret onboarding/content-binding profile.*v0.56.11' "$plan"
grep -q 'AWS-LC FIPS symmetric-secret onboarding/content-binding qualification.*v0.56.11' "$plan"
grep -q 'Signed hash-linked audit log.*v0.10.15.*VerifiedSignature' "$plan"
grep -q 'authority-token challenge framework.*v0.10.15.*VerifiedSignature' "$plan"
grep -q 'RustCrypto/software-key disposition implementation' "$plan"
grep -q 'RustCrypto public-key validation, software-signer binding, immutable dispatch, and returned-signature verification implementation' "$plan"
grep -q 'Published ring per-purpose capability, public-key-validation, signer-binding, asymmetric transactional onboarding, immutable signature dispatch/verification, handle-backed MAC operation authority/evidence, and key-disposition table' "$plan"
grep -q 'Published aws-lc-rs non-FIPS per-purpose capability, public-key-validation, signer-binding, asymmetric transactional onboarding, immutable signature dispatch/verification, handle-backed MAC operation authority/evidence, and key-disposition table' "$plan"
grep -q 'Android Keystore key-provider adapter' "$plan"
grep -q 'Reusable adapter conformance framework' "$plan"
grep -q 'qualification and coverage closure' "$plan"
grep -q 'Fluxheim integration fixture' "$plan"
grep -q 'every mandatory client requirement implemented' "$plan"
grep -q 'Longitudinal replay runner' "$plan"
grep -q 'Previous-release compatibility gate' "$plan"
grep -q 'No command may automatically bless current output' docs/REGRESSION_STRATEGY.md
grep -q 'provider assertion/attestation, and effect-authority capabilities' docs/REGRESSION_STRATEGY.md
grep -q 'artificial standards citation' docs/protocol-conformance.md
