# Compatibility

## Rust

Supported stable compilers are Rust `1.90.0` through `1.97.0`. Rust `1.97.0`
is the pinned release toolchain. The README compatibility table is normative.
Outward adapter crates keep the same range through `1.0.0`; using a newer SDK
does not silently grant an adapter a weaker MSRV.

## Operating Systems And Targets

Dependency-free crates support any target capable of the required `core` APIs.
CI and later adapter milestones add explicit Linux, Windows, BSD, macOS,
Android, and iOS evidence. Platform adapters cannot reduce core portability.
The design reserves clean custom transport, clock, signer, storage, and entropy
boundaries for a future custom operating-system target.

Support claims distinguish compile-checked, emulator/simulator-tested,
native-tested, and production-qualified evidence. A compile-only target is
never described as runtime-supported. Relevant adapters also publish evidence
for durability/atomic replacement and symlink semantics, wall and monotonic
clocks, entropy failure, mutable alias replacement, endian/width assumptions,
and required atomics.

Storage adapters additionally publish exactly `RollbackProtected`,
`RollbackDetecting { maximum_window }`, or `RollbackUnprotected`, the external
witness profile and externally rooted bootstrap identity, the closed namespace/
record/effect/tenant-partition/schema coverage of its authenticated state head,
and whether an operator restore declaration or reduced-assurance selection is
required. New or unknown store data never inherits a prior coverage claim.
Nominal `no_alloc` profiles publish allocator-free link/run evidence, peak stack
bound to exact target/compiler/optimization/features/linker, caller-scratch
behavior, and explicit `Send`/`Sync`, pinning, reentrancy, and scratch-lifetime
guarantees. Optional native secret-memory profiles publish exact page-lock,
dump/swap, guarded-allocation, copy-tracking, zeroization, privilege, and target
limitations; portable targets remain explicitly unsupported where necessary.

Cross-process adapters publish a `RemoteProtocolCapabilities` product rather
than inheriting generic guarantees. Controlled agents can advertise the full
authenticated protocol profile; fixed third-party APIs mark unsupported native
binding, replay, acknowledgement, recovery, attestation, or reconciliation
cells and separately document any sound local compensation.

## API And Protocol

Before 1.0, APIs may change between minor releases, but release notes and
migration notes are mandatory. Stable RFC behavior is versioned separately from
experimental Internet-Draft support. Draft behavior is never enabled by
default and never silently advances revisions.

Persisted and wire compatibility distinguishes transient
`LocalSigningRequestId` from the durable protocol reservation and its consuming
input-bound, final-request-bound, outbox-committed, and abandoned states. The
versioned canonical `AcmeRequestImage`, not HTTP/1.1 serialization, HTTP/2/3
frames, compression state, streams, TLS records, or QUIC packets, defines ACME
request compatibility. Partial/live states have no serialized authority
representation; persisted phase facts and abandonment tombstones cannot be
upgraded into one. Policy snapshot compatibility includes normalized effective
semantics, schema/canonicalization version, and digest-algorithm identity, not
source formatting. Fingerprint compatibility is purpose-specific and
cross-family conversion is forbidden; schema/canonicalization/hash changes
produce a new identity.
