# Security Policy

Vardheim is security-sensitive ACME and certificate-lifecycle software. Treat
all untrusted parsing, protocol transitions, JOSE, nonces, identifiers, URLs,
DNS, certificate verification, keys, storage, deployment, CI, and dependency
updates as high risk until reviewed and tested.

## Supported Versions

No production-ready version exists yet. Security fixes apply to the newest
development line until the first stable support policy is published.

## Routine Checks

Run regularly and before every release:

```bash
scripts/checks.sh
scripts/check-rust-version-matrix.sh
scripts/check_latest_tools.sh
cargo deny check
cargo audit
scripts/generate-sbom.sh
```

GitHub CodeQL default setup should be enabled in repository settings. Vardheim
does not carry an advanced CodeQL workflow while default setup is active.

## Release Gate

Every release, including patches, stops for an independent pentest before a tag
is created. The permanent report must be stored at
`security/pentest/vX.Y.Z.md`, name the exact reviewed commit, and have
`Status: PASS`. See `docs/RELEASE_PLAN.md` and `docs/release-process.md`.

## Reporting

Do not publish exploitable details before a fix is available. Use a private
GitHub security advisory after repository security channels are enabled, or
contact the maintainers directly.
