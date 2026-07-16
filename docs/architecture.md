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

Caller-supplied transport, signer, verifier, MAC, clock, store, DNS, and
deployment implementations are part of the application's trusted computing
base. Vardheim types prevent accidental category/purpose misuse and validate
observations at their boundaries, but cannot make a deliberately malicious
implementation truthful.

## Existing Account Ownership

An imported directory URL, account URL, or operator assertion is not account
ownership evidence. Existing-account adoption verifies the signer handle
against its public key and requires a fresh authenticated POST-as-GET whose
effective account URL, returned object, and directory identity agree. Created,
recovered, and imported provenance remain distinct, including for non-exportable
HSM/KMS account keys.

After rollover, neither the old nor new account key is disposable until fresh
authenticated account evidence establishes the effective signer and that
decision is durably committed. Ambiguous rollover or deactivation preserves
both key records and enters provider-native disposition reconciliation,
including retention, legal hold, scheduled deletion, and unavailable-provider
states.

## DER And Certificate Structure

The PKIX boundary rejects noncanonical DER before interpreting certificate
semantics. Minimal signed INTEGER and ENUMERATED encodings, OID encodings, BIT
STRING unused bits, canonical BOOLEAN, zero-length NULL, primitive/constructed
form, SET ordering, and definite shortest lengths are shared rules. Canonical
zero, positive, and negative integers are valid DER; field schemas impose
positivity, range, and zero restrictions. Certificate-envelope prevalidation
then enforces field order, version gates, positive serial policy, normalized
inner/outer signature algorithm-and-parameter equivalence, unique-ID/extension
legality, duplicate extension OIDs, unknown critical extensions without a
profile handler, and empty-subject/critical-SAN requirements before issuer
search or path processing.

## Public-Key Validation Evidence

Decoded JWK or SPKI bytes are not a validated public key. A selected provider
checks RSA modulus/exponent policy, Weierstrass curve/point validity, and
Ed25519/Ed448 encoding plus algorithm-specific weak/small-order policy, with
exact algorithm and parameter binding. The private-constructor evidence binds
the material hash, provider/session, tenant, purpose, and policy and is
transient. It never authorizes use of a signer handle.

A transient non-serializable `BoundSigner` separately establishes that a
provider handle controls the validated public key for bounded roles and time.
A mutable alias, label, name, or persistent reference may locate a key during
discovery but is never an authority identity. Binding resolves it to an
immutable provider-native key identity/version and canonical public-key digest,
and `BoundSigner` pins those values.
A provider-native pairwise-consistency operation may establish that
relationship. Otherwise a narrowly privileged `bind_signer` operation signs a
fresh entropy-backed canonical `SignerBinding` transcript and Vardheim verifies
the exact signature locally. `bind_signer` is the only handle-backed signing
operation exempt from ordinary consumer admission and accepts only that
canonical transcript, never arbitrary bytes or JWS, CSR, revocation,
TLS-challenge, or audit requests.

Ordinary handle-backed signature effects consume a private non-serializable
single-use `SignerConsumerAdmission` minted locally from `&mut BoundSigner`.
Admission binds the exact canonical signing bytes, algorithm and parameters,
output format, protocol role, request identity, and replay nonce where
applicable; minting performs no provider signature. Admission is consumed
immediately before signer dispatch and is never restored after success,
failure, cancellation, or ambiguity. Outstanding identities are unique and
bounded. Provider/session/policy/key-health change or signer expiry invalidates
`BoundSigner` and all derived admissions. Unsupported or unavailable
validation/binding never falls back, and issued leaf public keys are validated
even when not used for signature verification.

Dispatch addresses the exact immutable identity pinned by `BoundSigner`, never
the discovery alias. Provider-returned bytes are private
`UnverifiedSignature`, still untrusted even when the provider reports success.
Vardheim verifies the exact admitted bytes, algorithm, parameters, encoding,
immutable identity, and bound public key locally. Only that check constructs
`VerifiedSignature` accepted by protocol effects. Unsupported, unavailable,
malformed, or failed verification transmits nothing, consumes the admission,
invalidates or quarantines the signer according to policy, and cannot select a
fallback signer or verifier.

Invalidation before dispatch prevents signing. Invalidation racing with or
following dispatch makes the signing result ambiguous unless positive provider
evidence proves otherwise; the admission remains consumed. Replacement uses a
revalidated key, new `BoundSigner`, new request identity, and new admission.

## Handle-Backed MAC Evidence

EAB and TSIG use a MAC authority boundary parallel to, but type-separated from,
signer authority. A transient non-serializable `BoundMacKey` pins tenant,
directory or zone, provider/session, immutable secret identity/version,
algorithm, policy, allowed EAB or TSIG purposes, health epoch, and expiry.
Mutable secret names and aliases are discovery inputs only.

Each MAC effect consumes a private single-use `MacConsumerAdmission` binding
the exact canonical input, purpose, request identity, output and truncation
policy, and TSIG request/response/chaining state where applicable. It is
consumed immediately before dispatch to the immutable secret identity and is
never restored after success, failure, cancellation, ambiguity, session
change, or invalidation. Provider output remains private `UnverifiedMac`.

For local or exportable secrets, Vardheim independently recomputes and compares
the MAC in constant time before constructing purpose-specific `VerifiedMac`.
An opaque HSM, KMS, or secret manager that cannot support independent
verification may produce only separately typed `ProviderAssertedMac`.
`CryptographicallyAttestedMac` is reserved for a verified signed or native
receipt binding provider/session, immutable secret identity/version, input and
output digests, algorithm, purpose, request/admission identity, freshness or
replay protection, and assurance-profile identity. Neither weaker type becomes
`VerifiedMac`; EAB and TSIG reject both by default unless policy explicitly
admits that exact provider, evidence class, and profile. Unavailable
verification never exports a secret, selects another provider, or makes raw
MAC bytes usable.

Secret retargeting or version replacement before admission prevents authority.
A race during or after dispatch remains ambiguous unless matching positive
evidence proves the exact outcome, while the admission stays consumed. A new
attempt resolves and binds the current immutable secret version and creates a
new request identity and admission.

## Transactional Symmetric-Secret Onboarding

An immutable provider object identity does not prove that an imported or
adopted object contains the intended EAB or TSIG secret. Symmetric-secret
create, import, and adoption therefore use their own durable transaction model
rather than asymmetric public-key validation:

```text
SecretLifecycleState × SecretObligationSet

Requested -> CreationUnknown -> CreatedQuarantined -> ActiveEligible
                                            \-> RetainedQuarantined

Obligations = {
    ReconciliationPending,
    ContentBindingRequired,
    RevalidationRequired,
    SourceDestructionPending,
    DispositionPending,
    OperatorDecisionRequired,
}
```

Stable request and provider idempotency identities bind tenant, directory or
zone, external-account or TSIG key identity, algorithm, purposes, provider,
intended immutable version, origin, exportability, persistence, policy, and
source-secret disposition. New objects remain quarantined until a typed
content-binding mode succeeds:

- `LocallyCompared` uses a fresh domain-separated transcript, computes through
  both the local source and provider object, and compares in constant time.
- `PeerConfirmed` accepts only an authenticated exact CA or DNS peer result.
- `CryptographicallyAttested` verifies a genuine signed/native receipt over
  the complete binding transcript and freshness.
- `ProviderAsserted` is only an opaque provider claim and is rejected by
  default.
- `Unverified` never permits activation.

Source material cannot be destroyed before binding and its durable receipt are
committed. Durable active eligibility and historical binding receipts are not
MAC authority. Every process/provider session freshly resolves and rebinds the
current immutable object before constructing `BoundMacKey`.

Snapshots may retain lifecycle state, obligations, binding-mode/profile
identifiers, and redacted receipt digests. They never contain or restore
`BoundMacKey`, `MacConsumerAdmission`, `VerifiedMac`,
`ProviderAssertedMac`, `CryptographicallyAttestedMac`, or any other MAC effect
capability. Restart, provider/session/policy/health change, object
restore/recreation, alias/version retargeting, peer-trust change, or assurance
profile change requires fresh reconstruction; unavailable reconstruction
leaves the secret eligible but unusable.

## Transactional Key Onboarding

Generation, PKCS#8 or PKCS#12 import, legacy-key migration, and provider or
platform key adoption share a durable product model:

```text
KeyLifecycleState × KeyObligationSet

Requested -> CreationUnknown -> CreatedQuarantined -> Active
                                            \-> RetainedQuarantined

Obligations = {
    ReconciliationPending,
    ValidationRequired,
    BindingRequired,
    RevalidationRequired,
    DispositionPending,
    OperatorDecisionRequired,
}
```

Stable request and provider idempotency identities bind tenant, role,
algorithm/parameters, provider, intended key version, origin, exportability,
persistence, attestation, and policy. The durable key record also stores the
observed immutable provider identity/version and canonical public-key digest;
mutable locators remain metadata. Provider observations distinguish definitely
not created, created, ambiguous, and unavailable. No newly created or imported
key is signable while quarantined. Obligations are orthogonal so a failure or
lifecycle transition cannot discard reconciliation, revalidation, operator-
decision, cleanup, or disposition work. `Active` is only a durable inventory
and lifecycle-policy eligibility fact. Historical validation and binding audit
records are not `ValidatedPublicKey` or `BoundSigner` values and cannot be
converted into them.

Every process and provider session reconstructs fresh live authority before
signing: validate the current public material, bind the exact current handle,
then mint request-specific admission. Restart, provider-session or policy
change, key-health epoch change, handle or public-key replacement, KMS
alias/version retargeting, or HSM object recreation invalidates live authority
and adds `RevalidationRequired`. If reconstruction is unavailable, the key may
remain lifecycle-eligible but is unusable. Lost responses, eventual visibility,
unreadable attributes, failed validation/binding, restart, and duplicate
requests retain reconciliation or disposition obligations. Object absence and
failed lookup never prove destruction.

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

## Authoritative DNS Discovery

Self-check discovery walks zone cuts using authoritative answers and downward
referrals, with AA, section placement, and SOA ownership interpreted together.
In-domain, sibling, and out-of-bailiwick glue remain untrusted routing inputs
and missing nameserver A/AAAA data is resolved iteratively. CNAME and DNAME
synthesis, alias/referral dependencies, lame delegations, address families,
servers, and total work are bounded. Ambient system resolution cannot silently
complete an authority chain.

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

## Transport Replay Boundary

Every ACME adapter declares HTTP/1.1, HTTP/2, or HTTP/3 explicitly and disables
TLS/QUIC early data and hidden retries. Only version-specific protocol evidence
can prove a request was not processed; partial writes, resets, cancellation,
response loss, and unproven stream/connection shutdown remain ambiguous and
must reconcile at the ACME operation layer. Connection pools, TLS/QUIC
sessions, DNS results, proxies, trust, directories, tenants, and policies are
partitioned. Cross-origin connection coalescing is prohibited unless a
version-specific conformance proof permits it.

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
- An old account key cannot be disposed after rollover or deactivation until
  durable signer-control evidence and policy authorize that exact disposition.
- A certificate cannot be deployed before structural and policy verification.
- Noncanonical DER or an X.509 structural defect cannot reach issuer search or
  path validation.
- Parsed JWK/SPKI material cannot become an account, CSR, certificate, or
  deployment key without current provider-bound public-key validation evidence.
- A generated, imported, migrated, or adopted key cannot become active before
  transactional reconciliation and recorded onboarding validation/binding;
  durable active eligibility alone never grants current signing authority.
- Persisted lifecycle state, validation/binding history, and audit records
  cannot construct or restore `ValidatedPublicKey`, `BoundSigner`,
  `SignerConsumerAdmission`, verification, or effect-authority capabilities.
- Each process/provider session reconstructs live signer authority, and any
  provider session, policy, key-health, handle, public-key, alias, or version
  change invalidates it without clearing durable obligations.
- No handle-backed signature effect can be constructed without current
  public-key validation, a role-permitted `BoundSigner`, and exact-request
  single-use signer-consumer admission, except the canonical `bind_signer`
  proof operation.
- Mutable aliases, labels, names, and persistent references cannot be used for
  authority dispatch; the exact immutable identity/version and public-key
  digest pinned during binding must be used.
- Provider-returned signature bytes are untrusted and cannot enter any protocol
  effect until locally verified against the bound key and exact admitted
  request; unavailable verification fails closed without fallback.
- Cached, unrelated, cross-protocol, ambiguous, expired, replayed, or
  incompletely bound native signatures cannot prove a signer handle is bound.
- Signer success, failure, cancellation, ambiguity, `badNonce`, and ambiguous
  network transmission never restore or reuse a consumed request admission.
- Invalidation before dispatch blocks signing; a racing or post-dispatch
  invalidation stays ambiguous without positive provider evidence and requires
  an entirely new validated/bound/request-admitted attempt.
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
- Authoritative DNS readiness cannot be inferred from ambient recursion,
  unvalidated glue, a bare AA bit, or an incomplete referral chain.
- DNS update success requires verified request-bound TSIG response evidence.
- ACME requests are never sent as early data or automatically retried after an
  ambiguous transmission.
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
