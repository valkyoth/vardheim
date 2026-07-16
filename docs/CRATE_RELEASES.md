# Crate Release Policy

Vardheim crates use independent versions and are published in validated Cargo
dependency order. The facade is always last.

The `vardheim` facade always uses the exact `vX.Y.Z` tag version and is
published for every release, including metadata-only milestones. Support
crates retain independent versions and publish only when their own package
contents require it. This prevents facade versions from drifting behind the
repository release sequence.

## crates.io Content Boundary

Published archives contain only Cargo-generated package metadata,
`README.md`, and regular `.rs` files below `src/`. RFC and registry snapshots,
project-wide documentation, release notes, pentest evidence, scripts, GitHub
configuration, images, downloads, vectors, and other repository evidence stay
on GitHub.

`scripts/validate-package-contents.py` applies this as an allowlist to the
actual `.crate` archives after `cargo package`. It also rejects absolute or
parent-traversal paths, unexpected package roots, links and special entries,
duplicate paths, missing Cargo metadata or Rust sources, more than 512 files,
individual files above 1 MiB, and archives above 5 MiB unpacked. Adding a new
publishable content class therefore requires an explicit reviewed policy
change; placing a file in a crate directory cannot silently publish it.

The adversarial package suite exercises repository evidence, downloads,
path traversal, wrong roots, symlinks, duplicates, omissions, and size limits.

## Publish Order

1. `vardheim-core`
2. `vardheim-challenge-http`
3. `vardheim-challenge-dns`
4. `vardheim-challenge-tls`
5. `vardheim`

The first four crates are currently independent of one another. The order is
kept stable for reproducible release evidence. `vardheim` depends on all four
and therefore must be published only after crates.io resolves their versions.
When roadmap versions introduce `vardheim-pkix` or outward adapter packages,
the release manifest and dependency-derived publish order must add them in the
same milestone; this current five-crate list is not permission to hide heavy
ecosystem dependencies inside an existing portable crate.

## Version Rules

| Change | Version rule | Publish |
| --- | --- | --- |
| `code` | The facade follows the Vardheim milestone; a support crate advances to its next independent minor version. | Yes |
| `dependency` | Patch-bump the support crate's current minor line. | Yes |
| `metadata` | Use the milestone version for corrected immutable package metadata. | Yes |
| `unchanged` | Retain the published version. | No |

`release-crates.toml` records the exact plan. Package versions in Cargo metadata
must match it, and its crate set must exactly match the workspace.

## Commands

Validate the plan without network access or publishing:

```bash
scripts/release_crates.py --check
python3 scripts/test-release-crates.py
scripts/validate-package-contents.py
python3 scripts/test-package-contents.py
```

Preview the exact preflight and publish sequence without executing commands:

```bash
scripts/release_crates.py --dry-run --yes
```

Publish only from a clean worktree whose `vX.Y.Z` tag points at `HEAD`:

```bash
scripts/release_crates.py
```

After a partial crates.io release, resume at the first package that did not
publish:

```bash
scripts/release_crates.py --start-at vardheim-challenge-dns
```

The script deliberately has no `--no-verify`, dirty-tree, untagged, or
skip-preflight escape hatch. It pauses between packages so the operator can
confirm crates.io index propagation before publishing a dependent crate.

## Current `v0.3.1` Plan

| Crate | Published | Planned | Change | Publish |
| --- | --- | --- | --- | --- |
| `vardheim-core` | `0.1.0` | `0.1.0` | unchanged | No |
| `vardheim-challenge-http` | `0.1.0` | `0.1.0` | unchanged | No |
| `vardheim-challenge-dns` | `0.1.0` | `0.1.0` | unchanged | No |
| `vardheim-challenge-tls` | `0.1.0` | `0.1.0` | unchanged | No |
| `vardheim` | `0.3.0` | `0.3.1` | code | Yes |

All five crates were first published manually at `0.1.0`. The rolling
`release-crates.toml` now captures the next release decision and must be updated
with this table before every later milestone.
