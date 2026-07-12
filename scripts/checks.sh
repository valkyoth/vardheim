#!/usr/bin/env sh
set -eu

cargo fmt --all --check
scripts/check_shell_syntax.sh
scripts/check_doc_links.sh
scripts/verify-rfcs.sh
scripts/validate-plan.sh
scripts/validate-release-metadata.sh
scripts/validate-modularity-policy.sh
scripts/validate-security-policy.sh
scripts/release_crates.py --check
python3 scripts/test-release-crates.py
python3 scripts/test-release-validation.py
scripts/check-packages.sh
cargo check --workspace --all-targets --all-features
cargo clippy --workspace --all-targets --all-features -- -D warnings
cargo test --workspace --all-features
cargo doc --workspace --all-features --no-deps
