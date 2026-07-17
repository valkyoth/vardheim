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

Storage adapters additionally publish whether rollback is protected, detected,
or unprotected and whether detection requires an operator restore declaration.
Nominal `no_alloc` profiles publish allocator-free link/run evidence, bounded
peak stack and caller-scratch behavior, and explicit `Send`/`Sync`, pinning,
reentrancy, and scratch-lifetime guarantees.

## API And Protocol

Before 1.0, APIs may change between minor releases, but release notes and
migration notes are mandatory. Stable RFC behavior is versioned separately from
experimental Internet-Draft support. Draft behavior is never enabled by
default and never silently advances revisions.
