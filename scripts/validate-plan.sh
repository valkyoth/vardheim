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
    v0.13.1
    v0.14.2
    v0.15.2
    v0.19.3
    v0.20.3
    v0.25.2
    v0.28.1
    v0.30.7
    v0.30.8
    v0.30.9
    v0.33.3
    v0.37.4
    v0.38.3
    v0.39.2
    v0.39.3
    v0.39.4
    v0.39.5
    v0.41.2
    v0.41.3
    v0.42.1
    v0.42.2
    v0.51.2
    v0.60.0
    v0.69.3
    v0.71.1
    v0.71.2
    v0.81.0
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
grep -q 'Complete `newNonce` operation' "$plan"
grep -q 'Optional RFC 8555 `newAuthz` pre-authorization' "$plan"
grep -q 'Introduce the dependency-light `vardheim-pkix` crate' "$plan"
grep -q 'Existing certificate adoption' "$plan"
grep -q 'Certificate-key compromise response' "$plan"
grep -q 'Provider-neutral bounded DNS query contract' "$plan"
grep -q 'Reusable adapter conformance framework' "$plan"
grep -q 'qualification and coverage closure' "$plan"
grep -q 'Fluxheim integration fixture' "$plan"
grep -q 'every mandatory client requirement implemented' "$plan"
grep -q 'Longitudinal replay runner' "$plan"
grep -q 'Previous-release compatibility gate' "$plan"
grep -q 'No command may automatically bless current output' docs/REGRESSION_STRATEGY.md
