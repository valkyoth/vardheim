# Vardheim Longitudinal Regression Strategy

Vardheim does not treat tests as disposable evidence for one release. Every
release retains enough immutable, redacted evidence for future code to prove
that earlier behavior was preserved or deliberately corrected.

## Compared Baselines

Four independent baselines are retained:

1. the normative baseline: RFCs, verified errata, IANA registries, external
   profiles, and exact draft revisions;
2. the behavioral baseline: golden vectors, adversarial corpora, model traces,
   fault schedules, normalized wire exchanges, and semantic outcomes;
3. the Vardheim release baseline: public API, feature graph, serialized state,
   migrations, configuration, CLI machine output, and support claims; and
4. the environment baseline: redacted provider observations and platform/profile
   qualification evidence.

Every evidence item has a stable ID, source or generator revision, semantic
expectation, applicability range, content hash, and first/last release metadata.
Secrets, account identifiers, private keys, tokens, and uncontrolled personal
or provider data must never enter retained evidence.

Verification capabilities are not evidence artifacts and must never be
serialized into a retained snapshot. A snapshot may retain redacted
verification audit records and the hashes/versions needed to decide that
revalidation is required. Replay after restart or a policy, trust-anchor,
status, CT-list, algorithm, provider-capability, time, or input change must
perform local verification again before deployment or activation.

## Replay Rules

Normal CI is deterministic and offline. It replays every historical evidence
set that declares itself compatible with the current release. Results are
compared semantically: incidental timestamps, nonces, ordering explicitly
defined as irrelevant, and approved redactions are normalized, but security
decisions and protocol bytes that standards define as exact are not hidden.

An unexplained difference is a release blocker. Intentional changes require all
of the following in the same version:

- the requirement, defect, security finding, or upstream change that justifies
  the difference;
- a reviewed old-versus-new semantic difference report;
- a migration or compatibility decision when externally visible behavior moves;
- a new regression case preserving the defect and the corrected expectation;
- release notes and an updated support or conformance claim; and
- the normal reviewed-implementation pentest stop and finalization-diff check.

No command may automatically bless current output as the new baseline. Baseline
updates are explicit reviewed changes. Historical evidence remains retained
even after a correction so the original failure can never silently return.

## Live Drift Versus Reproducible Evidence

Scheduled live jobs check RFC/errata status, IANA registries, external profiles,
draft revisions, tool/dependency releases, and opted-in provider behavior. They
produce advisory drift reports and never modify the pinned baseline or make an
offline build depend on the network. A maintainer reviews each difference and
assigns required work to a tactical version before it can become accepted
behavior.

## Compatibility Dimensions

The release comparison gate covers:

- Rust public API and feature resolution against the latest published release;
- normalized ACME wire behavior and typed error/security decisions;
- every supported historical persisted snapshot and migration chain, including
  proof that verification capabilities are absent and stale audit records
  trigger revalidation;
- provider observations without encoding undocumented quirks as standards;
- target/profile compile and runtime evidence;
- formal-model traces and generated adversarial cases; and
- dependency/tool manifests, where drift is reported separately from behavior.

Before `1.0.0`, an intentional breaking change is possible only when documented
and versioned, but it is never permitted to appear as an unexplained regression.
The exact compatibility promise for `1.x` is frozen during the `0.120.0` release
candidate sequence.

## Assigned Milestones

The implementation is deliberately split across `0.3.8`, `0.4.3`, `0.4.4`,
`0.33.3`, `0.33.4`, `0.39.2`, `0.69.3`, `0.92.6`, `0.97.3`, `0.119.0`, and
`0.119.1` in [the release plan](RELEASE_PLAN.md). Release binding itself is
assigned to `0.3.3`. Each boundary receives its own complete test suite and
mandatory pentest stop.
