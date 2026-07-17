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

An optional native `SecretMemory` implementation follows the same tier and
allowlist rules. Page locking, dump exclusion, guarded allocations, swap
controls, copy tracking, or zeroization never justify unsafe in portable secret
types and never support a universal-erasure claim. Missing operating-system
semantics or privilege produces typed unsupported behavior without fallback to
a falsely equivalent assurance profile.
