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
    v0.4.4
    v0.4.5
    v0.4.6
    v0.4.7
    v0.5.2
    v0.10.2
    v0.10.3
    v0.10.4
    v0.10.5
    v0.10.6
    v0.10.7
    v0.13.1
    v0.14.2
    v0.15.2
    v0.19.3
    v0.20.3
    v0.25.2
    v0.28.1
    v0.28.2
    v0.28.3
    v0.28.4
    v0.28.5
    v0.28.6
    v0.28.7
    v0.28.8
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
    v0.31.2
    v0.31.3
    v0.33.3
    v0.33.4
    v0.37.4
    v0.38.3
    v0.38.4
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
    v0.42.1
    v0.42.2
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
    v0.51.2
    v0.52.3
    v0.56.0
    v0.56.1
    v0.57.5
    v0.57.6
    v0.57.7
    v0.57.8
    v0.60.0
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
grep -q 'Provider-neutral digest semantics' "$plan"
grep -q 'Narrow legacy-hash compatibility capability' "$plan"
grep -q 'Complete `newNonce` operation' "$plan"
grep -q 'Optional RFC 8555 `newAuthz` pre-authorization' "$plan"
grep -q 'Introduce the dependency-light `vardheim-pkix` crate' "$plan"
grep -q 'Canonical bounded DER writer' "$plan"
grep -q 'Private test-only reference crypto primitives' "$plan"
grep -q 'Private test-only PKIX evidence verifier extension' "$plan"
grep -q 'Private test-only DNSSEC verifier extension' "$plan"
grep -q 'Complete RFC 5280 certificate-policy processing' "$plan"
grep -q 'Core-to-PKIX evidence bridge' "$plan"
grep -q 'Validation-session-bound PKIX capabilities' "$plan"
grep -q 'Bounded OCSP request encoding and response decoding' "$plan"
grep -q 'Bounded CRL and `TBSCertList` parsing' "$plan"
grep -q 'Bounded SCT-list parsing' "$plan"
grep -q 'Provider-neutral `PublicPkiFetch` contract' "$plan"
grep -q 'Snapshot rehydration and verification-invalidation boundary' "$plan"
grep -q 'Existing certificate adoption' "$plan"
grep -q 'Certificate-key compromise response' "$plan"
grep -q 'Certificate generation retirement state machine' "$plan"
grep -q 'Provider-neutral bounded DNS query contract' "$plan"
grep -q 'Production `std` wall/monotonic clock adapter' "$plan"
grep -q 'Canonical DNSSEC owner-name and RRset serialization' "$plan"
grep -q 'Local DS-to-DNSKEY digest and key-tag verification' "$plan"
grep -q 'Local RRSIG cryptographic verification' "$plan"
grep -q 'RFC 5155 NSEC3 authenticated denial' "$plan"
grep -q 'DNSSEC trust-anchor provisioning' "$plan"
grep -q 'Validating-resolver evidence policy' "$plan"
grep -q 'Production `std` `PublicPkiFetch` adapter' "$plan"
grep -q 'Explicit and separate capability sets' "$plan"
grep -q 'RustCrypto DNSSEC verifier capabilities' "$plan"
grep -q 'Android Keystore key-provider adapter' "$plan"
grep -q 'Reusable adapter conformance framework' "$plan"
grep -q 'qualification and coverage closure' "$plan"
grep -q 'Fluxheim integration fixture' "$plan"
grep -q 'every mandatory client requirement implemented' "$plan"
grep -q 'Longitudinal replay runner' "$plan"
grep -q 'Previous-release compatibility gate' "$plan"
grep -q 'No command may automatically bless current output' docs/REGRESSION_STRATEGY.md
grep -q 'Verification capabilities are not evidence artifacts' docs/REGRESSION_STRATEGY.md
