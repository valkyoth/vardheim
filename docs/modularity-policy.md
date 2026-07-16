# Modularity And File Size Policy

No source file may exceed 500 physical lines. A file approaching the limit must
be split by responsibility before more behavior is added. Tests may be adjacent
while small, then move into focused test modules. Numbered fragments or splits
at an arbitrary line boundary are not acceptable substitutes for a documented
module responsibility and narrow export surface. Generated source and large
corpora use dedicated generated/evidence locations and their own size policy.

A new crate is justified only when it provides a real `no_std` or runtime
boundary, isolates substantial optional dependencies, integrates with an
external ecosystem, has independent users, or needs independent security and
release maintenance. Organizational separation alone uses modules.

The `vardheim` facade depends on focused crates and gives ordinary users one
coherent entry point. Core crates never gain cloud SDKs, runtimes, filesystem
clients, databases, or TLS stacks through default features.

The planned feature tiers are:

- default: core-only `no_std`, without allocation where the API permits;
- `alloc`: bounded owned values and explicitly constructed dynamic adapters;
- `std`: filesystem, threading, process, native transport, and system
  integration;
- runtime/provider features: additive and default-off, making constructors
  available without selecting a backend.

Heavy integrations use outward adapter packages rather than features in the
portable challenge/core crates. `vardheim-pkix` is the approved future
dependency-light `no_std` certificate boundary; provider SDKs, Redis, HTTP
frameworks, TLS stacks, databases, and crypto implementations remain outside
it. Dependency-cycle, feature-power-set, public API, compile-time, binary-size,
and architecture-direction checks become mandatory at their roadmap versions.
