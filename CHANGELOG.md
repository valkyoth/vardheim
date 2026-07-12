# Changelog

All notable changes to Vardheim will be documented here. The format follows
Keep a Changelog and the project follows Semantic Versioning.

## Unreleased

## 0.3.0 - Unreleased

### Added

- Complete checksum-bound section inventory for all 65 tracked RFCs.
- Reviewed all-status RFC Editor errata snapshot for all 13 published ACME
  RFCs, with offline validation and explicit live drift checks.
- Permanent facade/tag version equality and publication enforcement.
- Bounded RFC Editor connection and transfer timeouts with an end-to-end
  fetch-and-hash regression test.
- Passing maintainer-supplied pentest and clean remediation retest evidence.

## 0.2.0 - 2026-07-12

### Added

- Dependency-ordered workspace publication helper, independently versioned
  per-crate release plan, regression tests, and operator documentation.
- Structured release metadata and pentest-readiness validators with exhaustive
  missing, malformed, failed, stale, wrong-commit, and tag refusal tests.
- Verified package archives, matching SPDX SBOM enforcement, and the dedicated
  `v0.2.0` release gate.
- Fail-closed EOF and non-TTY publication handling plus release-state
  revalidation immediately before every irreversible crate publish.
- Passing maintainer-supplied pentest and clean remediation retest evidence.

## 0.1.0 - 2026-07-12

### Added

- Security-first Cargo workspace foundation.
- Five dependency-free `no_std` crates with a facade boundary.
- Rust `1.90.0` through `1.97.0` compatibility policy and CI matrix.
- Dual MIT and Apache-2.0 licensing.
- Initial security, RFC, implementation, release, and compatibility documents.
- Local checks, supply-chain policy, SBOM tooling, and pentest release gate.
- Application-owned panic policy and non-overridable lossy-cast lint policy.
- Tactical one-boundary release sizing with split parser, PKIX, workflow,
  persistence, deployment, operations, platform, and qualification milestones.
- ACME completeness and production web-server replacement acceptance contract.
- Sixty-five exact RFC reference copies with SHA-256 integrity enforcement,
  read-only local locking, owner review, and Cargo package exclusion.
- Passing maintainer-supplied external pentest and clean retest evidence.
- CI-portable shell syntax validation and release scripts with no undeclared
  ripgrep dependency.
