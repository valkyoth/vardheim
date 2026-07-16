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
        -> issued-certificate trust provider chosen separately from TLS roots
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

Audit records use stable invalidation reasons and retain the issued-certificate
trust snapshot identity. They never collapse trust removal, distrust, policy,
time, status, CT, algorithm/provider, or input changes into an unauditable
generic stale flag.

Caller-supplied transport, signer, verifier, clock, store, DNS, and deployment
implementations are part of the application's trusted computing base. Vardheim
types prevent accidental category/purpose misuse and validate observations at
their boundaries, but cannot make a deliberately malicious implementation
truthful.

## Existing Account Ownership

An imported directory URL, account URL, or operator assertion is not account
ownership evidence. Existing-account adoption verifies the signer handle
against its public key and requires a fresh authenticated POST-as-GET whose
effective account URL, returned object, and directory identity agree. Created,
recovered, and imported provenance remain distinct, including for non-exportable
HSM/KMS account keys.

## Public PKI Fetch Boundary

OCSP, CRL, AIA, CT-list, and related public PKI downloads use a dedicated
`PublicPkiFetch` boundary, never authenticated ACME transport. It has no ambient
credentials, cookies, ACME headers, or proxy authentication; applies explicit
scheme, address, redirect, cache, body, framing, representation, decompression,
privacy, and deadline policy; and returns only complete untrusted bytes.
Framing-invalid or partial HTTP bodies never become PKI objects, and cache keys
include method, request-body digest, tenant, purpose, policy, trust, and privacy
context. Local certificate/status/CT signature verification establishes
authenticity.

## Trust Domain Separation

ACME transport roots, issued-certificate anchors, CT log keys, DNSSEC anchors,
and signer/provider trust have distinct types and snapshot identities. A
`CertificateTrustProvider` supplies immutable, versioned, tenant/profile-bound
issued-certificate snapshots with explicit additions, removals, distrust, and
constraints. Reload failure preserves the last accepted snapshot and never
loads an empty or transport-root set. Platform snapshots preserve native
constraints and distrust or return typed unsupported; flattening roots alone
does not claim native-platform-equivalent trust.

## Certificate Transparency Version Separation

RFC 6962 CT v1 SCTs and RFC 9162 CT v2 `TransItem` objects use distinct types,
log identities, signature schemes and inputs, precertificate reconstruction,
log-list capabilities, and verified evidence. Neither version can be converted
to or used as fallback evidence for the other.

Version-specific Merkle logic verifies signed tree heads, inclusion paths, and
append-only consistency. Durable monitoring schedules each SCT after its log's
MMD, retains checkpoints, and classifies missing inclusion, rollback,
inconsistency, outage, disqualification, and closure. Optional independent
witness/gossip observations can detect conflicting views but cannot substitute
for log signatures or Merkle proof.

## PKIX Time And Name Semantics

Certificates, CRLs, OCSP, and CMS/CT share one bounded ASN.1 time parser with
RFC 5280 UTCTime/GeneralizedTime year rules, required seconds/Zulu, calendar and
interval validation, explicit leap-second policy, and checked Vardheim wall-
clock conversion. Locale, system parsers, offsets/fractions forbidden by the
profile, and lossy timestamp conversions are excluded.

Distinguished-name equality preserves RDN sequence and attribute OIDs, compares
multi-valued RDNs as sets, and applies RFC 4518 StringPrep/caseIgnoreMatch plus
domainComponent rules. Unsupported equality rules are typed rather than guessed
or reduced to display-string comparison.

## Key Disposition Evidence

Every key provider implements one disposition contract with tenant/provider/
key-version/purpose/policy/request binding. `Destroyed`, `Disabled`,
`ScheduledForDeletion`, `RetainedByPolicy`, `ProviderCannotDestroy`, `NotFound`,
`Ambiguous`, and `Unavailable` remain distinct through reconciliation. Unlink,
zeroization, handle loss, disablement, scheduled deletion, or absence cannot be
reported as physical destruction without provider evidence supporting that
exact claim.

## DNS Query Correlation

Every UDP DNS attempt binds an unpredictable transaction ID and source port (or
bounded socket rotation) to the complete local/remote tuple, server, question,
transport, and attempt. TCP retry uses a fresh ID and a bounded two-byte-framed
codec that correlates partial, coalesced, and out-of-order messages on the same
connection. Optional DNS Cookies remain server-scoped defense in depth and
cannot weaken tuple, DNSSEC, or TSIG verification.

## DNS Update Authentication

RFC 2136 updates use RFC 8945 TSIG through a dedicated `DnsUpdateMac`
capability. EAB keys and MAC purposes cannot cross this boundary. Update
success requires response authentication bound to the request MAC, server,
transaction, time, key, algorithm, and message chain.

## Stapled Status Generations

For RFC 7633 certificates, verified OCSP staple bytes and expiry join the
certificate, chain, and key in one fenced deployment generation. Deployment
adapters transport bytes and expiry but cannot fabricate verified status
evidence. Refresh and rollback preserve the last policy-valid serving
generation.

## No-Heap Validation Workspaces

The strict `no_std` tier accepts caller-provided storage for PKIX path
candidates, RFC 5280 policy trees, OCSP/CRL extensions and entries, SCT lists,
CT v2 `TransItem` collections, DNSSEC RRsets/chains, and NSEC/NSEC3 proofs.
Exhaustion is deterministic and typed. Optional `alloc` wrappers own these
workspaces without changing validation rules or capacity accounting.

## Security Invariants

- A replay nonce is consumed exactly once and never returned to a pool.
- A JWS contains exactly one of `jwk` or `kid`.
- Signed requests cannot redirect automatically or change their signed URL.
- Untrusted bytes, JSON, extension maps, headers, PEM, DER, and recursion are
  bounded before allocation or traversal.
- Account, certificate, EAB, challenge, audit, and storage keys have separate
  roles and lifecycles.
- A certificate cannot be deployed before structural and policy verification.
- An imported account cannot become active without fresh signer-proven CA
  ownership evidence bound to the exact directory and account URL.
- Verification capabilities cannot be serialized, replayed across contexts, or
  restored after restart as current proof.
- Public PKI fetch results and unauthenticated DNS AD bits are never evidence.
- A partial, ambiguously framed, wrongly typed, or cross-context cached public
  PKI body is never accepted as an object.
- Issued-certificate trust never falls back to ACME transport roots or an empty
  snapshot.
- CT v1 and CT v2 log identities, inputs, and evidence are non-interchangeable.
- CT inclusion and consistency claims require version-specific STH and Merkle
  evidence; witness observations cannot fabricate them.
- Key disablement, scheduled deletion, absence, unlink, or zeroization cannot be
  recorded as physical destruction.
- DNS responses require complete tuple/attempt correlation; TCP or Cookies do
  not reduce that requirement.
- DNS update success requires verified request-bound TSIG response evidence.
- Must-Staple certificates cannot activate or remain active with an expired or
  mismatched required staple.
- Challenge cleanup removes only the presentation owned by that workflow.
- External effects use persist-before-effect and reconciliation semantics.
- Feature unification never silently chooses a cryptographic or TLS backend.
- Account keys, nonces, trust, ToS, EAB, rate state, and issuer policy cannot
  cross directory identities without an explicit reviewed sharing/migration
  decision; alternate CAs are never silent retries.
- An adopted certificate is not considered managed until its key, identifiers,
  chain, profile, issuer/account association, deployment target, and provenance
  have been validated and durably recorded.
