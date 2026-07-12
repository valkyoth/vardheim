#!/usr/bin/env bash
set -euo pipefail

test -f rfc/README.md
test -f rfc/SHA256SUMS

expected="$(sed -n 's/^[0-9a-f]\{64\}  \(rfc[0-9][0-9]*\.txt\)$/\1/p' rfc/SHA256SUMS | sort)"
actual="$(find rfc -maxdepth 1 -type f -name 'rfc*.txt' -printf '%f\n' | sort)"

if [[ "$expected" != "$actual" ]]; then
    echo "RFC file set does not match rfc/SHA256SUMS" >&2
    diff <(printf '%s\n' "$expected") <(printf '%s\n' "$actual") || true
    exit 1
fi

(
    cd rfc
    sha256sum --check --strict SHA256SUMS
)
