#!/usr/bin/env sh
set -eu

failed=0
for file in scripts/*.sh; do
    IFS= read -r interpreter < "$file"
    case "$interpreter" in
        '#!/usr/bin/env bash') bash -n "$file" || failed=1 ;;
        '#!/usr/bin/env sh') sh -n "$file" || failed=1 ;;
        *)
            echo "unsupported shell interpreter in $file: $interpreter" >&2
            failed=1
            ;;
    esac
done

exit "$failed"
