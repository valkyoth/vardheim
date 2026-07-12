#!/usr/bin/env sh
set -eu

scripts/generate-sbom.sh
scripts/checks.sh
scripts/check-rust-version-matrix.sh
cargo deny check
cargo audit
scripts/release_crates.py --check
scripts/validate-release-readiness.sh v0.3.1
