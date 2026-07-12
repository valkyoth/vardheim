# Toolchain Policy

The workspace declares Rust `1.90` as its MSRV and pins Rust `1.97.0` for
development and release verification. Every stable release from `1.90.0`
through `1.97.0`, including patch toolchains present in the matrix, is checked.

The pin moves only after the newest stable Rust release is reviewed. The MSRV
does not move before 1.0 unless a security requirement cannot be met otherwise;
such a change requires release notes and a compatibility milestone.

Nightly is allowed only for isolated fuzzing, Miri, sanitizer, or formal-proof
jobs. Published library behavior must compile on the documented stable range.
