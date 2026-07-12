# Release Process

1. Complete exactly one versioned milestone from `docs/RELEASE_PLAN.md`.
2. Update tests, RFC evidence, changelog, release notes, and known limitations.
3. Run local checks, the Rust matrix, deny, audit, and SBOM generation.
4. Stop implementation and request a pentest. The maintainer supplies findings
   in temporary, ignored root `PENTEST.md`.
5. Fix findings, remove `PENTEST.md`, and request another retest. Repeat these
   two steps until the maintainer reports a green retest.
6. Commit the permanent `security/pentest/vX.Y.Z.md` PASS report, update the
   README and release notes, and run `scripts/release_X_Y_gate.sh`.
7. Wait for required GitHub checks. If CodeQL or CI finds an issue, fix it and
   repeat the GitHub-check step.
8. Tag or publish only after GitHub is green and the maintainer explicitly
   requests it.

The GitHub release workflow is manual and metadata-only. Readiness is checked
before tag creation because a post-tag tag-existence guard necessarily fails.

Before each release, update `release-crates.toml` with every workspace crate's
independent version, change kind, publication decision, and reason. After the
signed tag points at the clean release commit, `scripts/release_crates.py`
validates the Cargo dependency graph, reruns preflight checks, and publishes in
the order documented in [CRATE_RELEASES.md](CRATE_RELEASES.md).
