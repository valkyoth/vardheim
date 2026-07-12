#!/usr/bin/env bash
set -euo pipefail

rfcs=(
    1034 1035 2119 2986 3339 3596 3986 4033 4034 4035 4086
    4648 5280 5321 5322 5480 5890 5891 5892 5893 5894 5895
    5958 6066 6125 6531 6960 7301 7468 7515 7516 7517 7518
    7519 7638 7807 8017 8018 8032 8037 8174 8288 8410 8446
    8551 8555 8657 8659 8725 8737 8738 8739 8823 9110 9111
    9112 9115 9162 9444 9447 9448 9457 9773 9799 9891
)

mkdir -p rfc
for number in "${rfcs[@]}"; do
    if [[ -e "rfc/rfc${number}.txt" ]]; then
        continue
    fi
    curl --fail --location --silent --show-error --proto '=https' --tlsv1.2 \
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
