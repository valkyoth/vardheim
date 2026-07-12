#!/usr/bin/env sh
set -eu

ci_file=".github/workflows/ci.yml"

ci_tool_version() {
    tool="$1"
    sed -n "s/.*cargo install --locked ${tool} --version \([0-9][^ ]*\).*/\1/p" "$ci_file" | head -n 1
}

latest_crate_version() {
    crate="$1"
    cargo info "$crate" | sed -n 's/^version: //p' | head -n 1
}

check_cargo_tool() {
    tool="$1"
    pinned="$(ci_tool_version "$tool")"
    latest="$(latest_crate_version "$tool")"
    test -n "$pinned"
    test -n "$latest"
    if [ "$pinned" != "$latest" ]; then
        echo "${tool} is not latest: pinned ${pinned}, latest ${latest}" >&2
        exit 1
    fi
}

check_action_pins() {
    refs="$(sed -n 's/^[[:space:]]*uses: [^@][^@]*@\([^[:space:]]*\).*/\1/p' "$ci_file")"
    for ref in $refs; do
        if ! printf '%s\n' "$ref" | grep -Eq '^[0-9a-f]{40}$'; then
            echo "GitHub Actions ref is not a full SHA: $ref" >&2
            exit 1
        fi
    done
}

check_checkout() {
    line="$(sed -n 's/.*uses: actions\/checkout@\([0-9a-f]\{40\}\) # \(v[0-9][0-9.]*\).*/\1 \2/p' "$ci_file" | head -n 1)"
    test -n "$line"
    pinned_sha="$(printf '%s\n' "$line" | awk '{ print $1 }')"
    pinned_tag="$(printf '%s\n' "$line" | awk '{ print $2 }')"
    latest_tag="$(git ls-remote --tags --refs https://github.com/actions/checkout.git 'refs/tags/v*' | sed 's#.*refs/tags/##' | grep -E '^v[0-9]+(\.[0-9]+)*$' | sort -V | tail -n 1)"
    latest_sha="$(git ls-remote --tags --refs https://github.com/actions/checkout.git "refs/tags/${latest_tag}" | awk '{ print $1 }')"
    test "$pinned_tag" = "$latest_tag"
    test "$pinned_sha" = "$latest_sha"
}

check_cargo_tool cargo-deny
check_cargo_tool cargo-audit
check_cargo_tool cargo-sbom
check_action_pins
check_checkout
