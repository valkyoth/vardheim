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
    v0.3.3
    v0.4.4
    v0.25.2
    v0.33.3
    v0.39.2
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

rg -q '^## Tactical Milestone Size Rule$' "$plan"
rg -q 'Fluxheim integration fixture' "$plan"
rg -q 'every mandatory client requirement implemented' "$plan"
rg -q 'Longitudinal replay runner' "$plan"
rg -q 'Previous-release compatibility gate' "$plan"
rg -q 'No command may automatically bless current output' docs/REGRESSION_STRATEGY.md
