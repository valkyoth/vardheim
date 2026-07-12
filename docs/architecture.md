# Architecture

Vardheim separates protocol decisions from side effects. The low-level engine
consumes bounded typed inputs, validates state transitions, and emits typed
effects. It does not own networking, sleeping, storage, DNS credentials,
private keys, system clocks, or certificate installation.

```text
application
    -> vardheim orchestration, policy, verification, and durable workflow
        -> vardheim-core typed ACME, JOSE, and deterministic state machines
        -> signer and certificate-key provider chosen explicitly by caller
        -> transport, challenge, storage, and deployment adapters
```

## Public Crate Boundaries

- `vardheim-core` is the strict dependency-light `no_std` protocol boundary.
- `vardheim` is the complete public SDK facade and high-level orchestration.
- challenge crates isolate independently useful challenge behavior and heavy
  provider or runtime dependencies from the facade's core graph.
- `vardheim-rustls` is admitted only when the generic TLS-ALPN boundary exists.

Internal account, order, authorization, renewal, policy, storage, deployment,
certificate, error, and observation concerns remain modules. A new public crate
requires a meaningful portability, dependency, ecosystem, or security boundary.

## Security Invariants

- A replay nonce is consumed exactly once and never returned to a pool.
- A JWS contains exactly one of `jwk` or `kid`.
- Signed requests cannot redirect automatically or change their signed URL.
- Untrusted bytes, JSON, extension maps, headers, PEM, DER, and recursion are
  bounded before allocation or traversal.
- Account, certificate, EAB, challenge, audit, and storage keys have separate
  roles and lifecycles.
- A certificate cannot be deployed before structural and policy verification.
- Challenge cleanup removes only the presentation owned by that workflow.
- External effects use persist-before-effect and reconciliation semantics.
- Feature unification never silently chooses a cryptographic or TLS backend.
