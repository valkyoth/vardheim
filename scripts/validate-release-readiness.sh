#!/usr/bin/env sh
set -eu

tag="${1:-}"
case "$tag" in
    v[0-9]*.[0-9]*.[0-9]*) ;;
    *) echo "usage: $0 vX.Y.Z" >&2; exit 2 ;;
esac

version="${tag#v}"
report="security/pentest/${tag}.md"
notes="release-notes/RELEASE_NOTES_${version}.md"

test -f "$report"
test -f "$notes"
rg -q '^Status: PASS$' "$report"
rg -q '^Tester: .+' "$report"
rg -q '^Date: [0-9]{4}-[0-9]{2}-[0-9]{2}$' "$report"
rg -q '^Scope: .+' "$report"
reviewed="$(sed -n 's/^Reviewed-Commit: \([0-9a-f]\{40\}\)$/\1/p' "$report")"
test -n "$reviewed"
git cat-file -e "${reviewed}^{commit}"

if git rev-parse -q --verify "refs/tags/$tag" >/dev/null; then
    echo "tag already exists: $tag" >&2
    exit 1
fi
