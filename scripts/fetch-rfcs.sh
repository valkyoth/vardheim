#!/usr/bin/env bash
set -euo pipefail

mapfile -t rfcs < <(
    sed -n 's/^[0-9a-f]\{64\}  rfc\([0-9][0-9]*\)\.txt$/\1/p' rfc/SHA256SUMS
)
if [[ "${#rfcs[@]}" -eq 0 ]]; then
    echo "rfc/SHA256SUMS contains no RFC sources" >&2
    exit 1
fi

mkdir -p rfc
for number in "${rfcs[@]}"; do
    if [[ -e "rfc/rfc${number}.txt" ]]; then
        continue
    fi
    curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 \
        --connect-timeout 10 --max-time 60 \
        "https://www.rfc-editor.org/rfc/rfc${number}.txt" \
        --output "rfc/rfc${number}.txt"
    test -s "rfc/rfc${number}.txt"
done

if [[ ! -f rfc/SHA256SUMS ]]; then
    echo "rfc/SHA256SUMS must be created and reviewed explicitly" >&2
    exit 1
fi

scripts/verify-rfcs.sh
printf '%s\n' "Verified ${#rfcs[@]} tracked RFC reference copies."
