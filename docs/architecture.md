# Architecture

Vardheim separates protocol decisions from side effects. The low-level engine
consumes bounded typed inputs, validates state transitions, and emits typed
effects. It does not own networking, sleeping, storage, DNS credentials,
private keys, system clocks, or certificate installation.

```text
application
    -> vardheim orchestration, policy, verification, and durable workflow
        -> vardheim-core typed ACME, JOSE, and deterministic state machines
        -> vardheim-pkix bounded certificate and policy verification
        -> signer and certificate-key provider chosen explicitly by caller
        -> transport, challenge, storage, and deployment adapters
```

## Public Crate Boundaries

- `vardheim-core` is the strict dependency-light `no_std` protocol boundary.
- `vardheim` is the complete public SDK facade and high-level orchestration.
- challenge crates isolate independently useful challenge behavior and heavy
  provider or runtime dependencies from the facade's core graph; provider SDKs,
  web frameworks, Redis, and TLS stacks live in separate adapter packages.
- `vardheim-pkix` is introduced before certificate parsing as an independently
  auditable dependency-light `no_std` boundary; `vardheim-core` does not depend
  on it.
- `vardheim-rustls` is admitted only when the generic TLS-ALPN boundary exists.

Internal account, order, authorization, renewal, policy, storage, deployment,
certificate, error, and observation concerns remain modules. A new public crate
requires a meaningful portability, dependency, ecosystem, or security boundary.

## PKIX Evidence Ownership

`vardheim-pkix` owns private-field `VerifiedLeaf`, `VerifiedPath`, and
`CertificateBinding` evidence. The facade invokes PKIX validation and converts
that evidence into crate-private reducer events; public custom adapters return
bounded observations and cannot construct verified workflow events directly.
Core therefore remains independent from PKIX while deployment still requires
positive certificate evidence.

Verification evidence is validation-session-bound and transient. It binds the
input hashes, intent/CSR, policy and trust-anchor identities, verification time,
validity deadline and clock epoch, status/CT inputs, and crypto-provider
capabilities. It is never deserialized or restored from workflow state.
Persisted verification records are audit facts; restart or any bound-context
change requires local revalidation before deployment or activation.

Caller-supplied transport, signer, verifier, clock, store, DNS, and deployment
implementations are part of the application's trusted computing base. Vardheim
types prevent accidental category/purpose misuse and validate observations at
their boundaries, but cannot make a deliberately malicious implementation
truthful.

## Public PKI Fetch Boundary

OCSP, CRL, AIA, CT-list, and related public PKI downloads use a dedicated
`PublicPkiFetch` boundary, never authenticated ACME transport. It has no ambient
credentials, cookies, ACME headers, or proxy authentication; applies explicit
scheme, address, redirect, cache, body, and deadline policy; and returns only
untrusted bytes. Local certificate/status/CT signature verification establishes
authenticity.

## No-Heap Validation Workspaces

The strict `no_std` tier accepts caller-provided storage for PKIX path
candidates, RFC 5280 policy trees, OCSP/CRL extensions and entries, SCT lists,
DNSSEC RRsets/chains, and NSEC/NSEC3 proofs. Exhaustion is deterministic and
typed. Optional `alloc` wrappers own these workspaces without changing
validation rules or capacity accounting.

## Security Invariants

- A replay nonce is consumed exactly once and never returned to a pool.
- A JWS contains exactly one of `jwk` or `kid`.
- Signed requests cannot redirect automatically or change their signed URL.
- Untrusted bytes, JSON, extension maps, headers, PEM, DER, and recursion are
  bounded before allocation or traversal.
- Account, certificate, EAB, challenge, audit, and storage keys have separate
  roles and lifecycles.
- A certificate cannot be deployed before structural and policy verification.
- Verification capabilities cannot be serialized, replayed across contexts, or
  restored after restart as current proof.
- Public PKI fetch results and unauthenticated DNS AD bits are never evidence.
- Challenge cleanup removes only the presentation owned by that workflow.
- External effects use persist-before-effect and reconciliation semantics.
- Feature unification never silently chooses a cryptographic or TLS backend.
- Account keys, nonces, trust, ToS, EAB, rate state, and issuer policy cannot
  cross directory identities without an explicit reviewed sharing/migration
  decision; alternate CAs are never silent retries.
- An adopted certificate is not considered managed until its key, identifiers,
  chain, profile, issuer/account association, deployment target, and provenance
  have been validated and durably recorded.
