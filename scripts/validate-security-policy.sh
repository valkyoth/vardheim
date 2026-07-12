#!/usr/bin/env sh
set -eu

for file in crates/*/src/lib.rs; do
    if ! grep -Eq '^#!\[no_std\]$' "$file"; then
        echo "missing no_std at crate root: $file" >&2
        exit 1
    fi
    if ! grep -Eq '^#!\[forbid\(unsafe_code\)\]$' "$file"; then
        echo "missing unsafe prohibition at crate root: $file" >&2
        exit 1
    fi
done

if find crates -type f -name '*.rs' \
    -exec grep -nHE '(^|[^[:alnum:]_])unsafe([^[:alnum:]_]|$)' {} + \
    | grep -Ev 'forbid\(unsafe_code\)'; then
    echo "unsafe Rust found outside the prohibition attributes" >&2
    exit 1
fi

test -f SECURITY.md
test -f docs/threat-model.md
test -f docs/security-controls.md
test -f docs/unsafe-policy.md
test -f deny.toml
