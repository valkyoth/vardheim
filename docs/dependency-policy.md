# Dependency Policy

Vardheim starts with zero external dependencies. Third-party crates may be
admitted only when reimplementing a mature cryptographic, PKIX, HTTP, TLS, DNS,
or platform primitive would increase risk.

Every admission records:

- latest stable version and date checked;
- license, MSRV, maintenance, ownership, audit, and advisory status;
- default and enabled features;
- `std`, allocation, unsafe, build-script, native, and network impact;
- transitive graph and duplicate-version impact;
- why a Vardheim boundary cannot remain dependency-free;
- conformance, negative, differential, and replacement evidence.

Git dependencies are denied unless pinned to an exact revision with an explicit
temporary exception. Backends are constructed explicitly; Cargo features may
make implementations available but may not silently select one.

Portable core, challenge, and PKIX crates do not admit cloud SDKs, runtimes,
databases, Redis, HTTP frameworks, or concrete TLS/crypto stacks as optional
features. Those dependencies live in outward adapter packages so enabling
`--all-features` on a portable crate cannot collapse unrelated ecosystems into
its graph. After the feature-topology milestone, dependency admission includes
minimal/additive/maximal and intentional multi-provider power-set checks plus
compile-time and binary-size impact.

Before each implementation milestone and release, run the networked tooling and
dependency version check. Live upstream state informs updates; reproducible
release claims remain tied to committed manifests, lockfiles, and evidence.

Before a public adapter trait freezes, private pinned API spikes validate each
materially different dependency/runtime family independently. Spike code and
dependencies remain unpublished evidence, carry no production support claim,
and may force the candidate boundary to change. A successful spike for one
provider cannot stand in for another provider's message/digest, buffer,
cancellation, identity, verification, or ambiguity semantics.

The first-party DER/PKIX boundary receives the same treatment before public API
freeze. Safe `no_std` ASN.1/X.509 candidates and independent parser oracles are
compared against exact semantic, MSRV, allocation, unsafe, maintenance, and
replacement requirements. The resulting build-versus-adopt decision is
reviewed evidence; an oracle or spike dependency is not automatically admitted
to production.

Native secret-memory primitives and purpose-specific remote protocols follow
the outward-adapter rule. OS bindings, transport stacks, authentication, schema
codecs, and witness implementations cannot enter portable core or create local
authority. Each admission records its exact platform/security semantics,
protocol/version surface, recovery behavior, and typed unsupported cells; a
dependency's claim of page locking, secure memory, delivery, or monotonic state
is not accepted without Vardheim conformance evidence.
For fixed third-party services, the adapter's `RemoteProtocolCapabilities`
record is derived from the actual authenticated API surface. Local correlation,
outbox state, or reconciliation may compensate for a missing native facility
where sound, but never turns that facility into a provider-authenticated claim.

Store and witness dependencies additionally map their actual transaction,
namespace, partition, schema, and authenticated-head behavior into a closed
`RollbackCoverage` manifest. A library-level durability or backup claim cannot
grant protection to omitted or newly introduced Vardheim records/effects.
