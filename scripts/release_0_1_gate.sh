#!/usr/bin/env sh
set -eu

scripts/checks.sh
scripts/check-rust-version-matrix.sh
cargo deny check
cargo audit
scripts/generate-sbom.sh
scripts/validate-release-readiness.sh v0.1.0
