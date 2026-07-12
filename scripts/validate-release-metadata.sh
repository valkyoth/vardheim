#!/usr/bin/env sh
set -eu

version="$(sed -n 's/^version = "\([0-9][0-9.]*\)"/\1/p' Cargo.toml | head -n 1)"
if [ -z "$version" ]; then
    version="$(sed -n 's/^version = "\([0-9][0-9.]*\)"/\1/p' crates/vardheim/Cargo.toml | head -n 1)"
fi
if [ -z "$version" ]; then
    version="0.1.0"
fi

notes="release-notes/RELEASE_NOTES_${version}.md"
report="security/pentest/v${version}.md"

test -f "$notes"
test -f "$report"
rg -q "^## ${version} -" CHANGELOG.md
rg -q '^Status: (PENDING|PASS|FAIL)$' "$report"
test -f docs/IMPLEMENTATION_PLAN.md
test -f docs/RELEASE_PLAN.md
test -f docs/VERSION_PLAN.md
