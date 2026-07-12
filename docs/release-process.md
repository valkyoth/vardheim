# Release Process

1. Complete exactly one versioned milestone from `docs/RELEASE_PLAN.md`.
2. Update tests, RFC evidence, changelog, release notes, and known limitations.
3. Run local checks, the Rust matrix, deny, audit, and SBOM generation.
4. Stop implementation and request an independent pentest of the exact commit.
5. Fix findings, rerun all gates, and remove temporary root `PENTEST.md`.
6. Commit a permanent `security/pentest/vX.Y.Z.md` PASS report for the reviewed
   commit.
7. Run `scripts/release_X_Y_gate.sh` and validate the tag does not exist.
8. Tag or publish only when explicitly requested by the maintainer.

The GitHub release workflow is manual and metadata-only. Readiness is checked
before tag creation because a post-tag tag-existence guard necessarily fails.
