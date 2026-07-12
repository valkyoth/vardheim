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

Before each implementation milestone and release, run the networked tooling and
dependency version check. Live upstream state informs updates; reproducible
release claims remain tied to committed manifests, lockfiles, and evidence.
