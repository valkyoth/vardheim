# Unsafe Code Policy

All current crates use `#![forbid(unsafe_code)]` and inherit a workspace lint
that forbids unsafe code. Protocol, type, flow, policy, and challenge-calculation
code must remain safe Rust.

An unavoidable future FFI or operating-system adapter requires its own crate,
documented invariants, the narrowest possible unsafe module, platform tests,
Miri or sanitizer evidence where applicable, and a dedicated pentest scope.
Unsafe code must never be introduced merely for performance without measured
need and independent review.
