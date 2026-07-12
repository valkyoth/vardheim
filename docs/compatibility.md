# Compatibility

## Rust

Supported stable compilers are Rust `1.90.0` through `1.97.0`. Rust `1.97.0`
is the pinned release toolchain. The README compatibility table is normative.

## Operating Systems And Targets

Dependency-free crates support any target capable of the required `core` APIs.
CI and later adapter milestones add explicit Linux, Windows, BSD, macOS,
Android, and iOS evidence. Platform adapters cannot reduce core portability.
The design reserves clean custom transport, clock, signer, storage, and entropy
boundaries for a future custom operating-system target.

## API And Protocol

Before 1.0, APIs may change between minor releases, but release notes and
migration notes are mandatory. Stable RFC behavior is versioned separately from
experimental Internet-Draft support. Draft behavior is never enabled by
default and never silently advances revisions.
