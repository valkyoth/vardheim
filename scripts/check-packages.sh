#!/usr/bin/env sh
set -eu

for package in vardheim-core vardheim-challenge-http vardheim-challenge-dns vardheim-challenge-tls; do
    cargo package -p "$package" --allow-dirty --offline
done

cargo package -p vardheim --allow-dirty --offline \
    --config 'patch.crates-io.vardheim-core.path="crates/vardheim-core"' \
    --config 'patch.crates-io.vardheim-challenge-http.path="crates/vardheim-challenge-http"' \
    --config 'patch.crates-io.vardheim-challenge-dns.path="crates/vardheim-challenge-dns"' \
    --config 'patch.crates-io.vardheim-challenge-tls.path="crates/vardheim-challenge-tls"'

for archive in target/package/vardheim-*.crate; do
    if tar -tf "$archive" | grep -Eq '(^|/)(rfc/|registry/|\.github/)|\.(webp|png|jpe?g|gif|svg)$'; then
        echo "repository-only source or image asset leaked into $archive" >&2
        exit 1
    fi
done
