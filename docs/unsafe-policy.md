# Unsafe Code Policy

All current crates use `#![forbid(unsafe_code)]` and inherit a workspace lint
that forbids unsafe code. Protocol, type, flow, policy, and challenge-calculation
code must remain safe Rust.

An unavoidable future FFI or operating-system adapter requires its own crate,
documented invariants, the narrowest possible unsafe module, platform tests,
Miri or sanitizer evidence where applicable, and a dedicated pentest scope.
Unsafe code must never be introduced merely for performance without measured
need and independent review.

At `0.4.13`, this distinction becomes a machine-readable crate policy instead
of a repository-wide text scan. Portable crates continue to require
`#![forbid(unsafe_code)]`. A native adapter must name each permitted module,
owner, invariant, reason, target, and evidence set; unsafe elsewhere, a widened
allowlist, missing evidence, or an unclassified crate fails the gate. Safe core
semantics never move into the allowlisted module.
