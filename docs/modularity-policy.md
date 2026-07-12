# Modularity And File Size Policy

No source file may exceed 500 physical lines. A file approaching the limit must
be split by responsibility before more behavior is added. Tests may be adjacent
while small, then move into focused test modules.

A new crate is justified only when it provides a real `no_std` or runtime
boundary, isolates substantial optional dependencies, integrates with an
external ecosystem, has independent users, or needs independent security and
release maintenance. Organizational separation alone uses modules.

The `vardheim` facade depends on focused crates and gives ordinary users one
coherent entry point. Core crates never gain cloud SDKs, runtimes, filesystem
clients, databases, or TLS stacks through default features.
