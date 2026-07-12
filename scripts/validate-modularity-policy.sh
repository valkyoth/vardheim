#!/usr/bin/env sh
set -eu

failed=0
find crates -type f -name '*.rs' -print | while IFS= read -r file; do
    lines="$(wc -l < "$file")"
    if [ "$lines" -gt 500 ]; then
        echo "Rust source exceeds 500 lines: $file ($lines)" >&2
        exit 1
    fi
done || failed=1

obsolete_pattern='acme''-ng|acme''_ng'
if find . -type f \
    ! -path './.git/*' \
    ! -path './target/*' \
    ! -path './rfc/*' \
    ! -name IDEA.md \
    -exec grep -nHE "$obsolete_pattern" {} +; then
    echo "obsolete design placeholder name found; use vardheim naming" >&2
    failed=1
fi

for crate in vardheim vardheim-core vardheim-challenge-http vardheim-challenge-dns vardheim-challenge-tls; do
    test -f "crates/$crate/Cargo.toml" || failed=1
    test -f "crates/$crate/src/lib.rs" || failed=1
done

exit "$failed"
