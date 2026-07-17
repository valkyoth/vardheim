# Vardheim Implementation Plan

Status: architecture and execution plan

Crate name: `vardheim`

Production target: `1.0.0`, after every version in
[the release plan](RELEASE_PLAN.md) has stopped for pentest and passed its own
release boundary.

## Product Boundary

Vardheim is a security-first ACME and certificate lifecycle framework, not a
single happy-path HTTP client. It supports two equally maintained interfaces:

- a high-level durable API that manages account, order, challenge, certificate,
  deployment, cleanup, and renewal lifecycles;
- a low-level deterministic command/event engine for custom runtimes, kernels,
  proxies, embedded systems, HSM-controlled systems, and unusual transports.

The protocol engine does not parse raw HTTP streams. It consumes bounded typed
response envelopes and emits typed effects. HTTP framing, TLS, sleeping,
storage, signing, DNS, and deployment belong to injected adapters.

## Workspace Shape

The public crate family is intentionally small:

- `vardheim`: complete facade, high-level orchestration, policy, certificate
  verification, storage/deployment traits, and common implementations;
- `vardheim-core`: dependency-light `no_std` ACME types, JSON/JOSE, protocol,
  and deterministic state machines;
- `vardheim-challenge-http`: versioned HTTP challenge calculations,
  presentation traits, generic handler,
  memory/filesystem stores, self-check, and cleanup receipts;
- `vardheim-challenge-dns`: versioned DNS challenge calculations, provider
  traits, authoritative checks,
  DNSSEC, and lightweight providers;
- `vardheim-challenge-tls`: versioned TLS challenge validation certificate
  construction, identity store,
  expiry, self-verification, and cleanup;
- `vardheim-pkix`: introduced at `0.28.1` as the independently auditable
  dependency-light `no_std` DER, PEM, CSR, X.509, path-policy, status/CT
  evidence, and certificate-binding boundary;
- `vardheim-rustls`: introduced at `0.51.0` for the concrete rustls boundary.

Heavy provider SDKs, validated cryptographic distributions, hardware/remote
signers, public-PKI fetch implementations, test servers, CLI, daemon, and agents
may be private workspace packages or separately published packages when the
release plan reaches them. Internal account, order, certificate, renewal,
policy, persistence, deployment, and observation concerns remain modules
unless they meet the crate-splitting rule. Route 53, Azure DNS, Redis, HTTP
frameworks, rustls/OpenSSL, crypto providers, and similar ecosystems do not
become features of the portable challenge or core crates; their packages depend
inward on Vardheim semantic types.

## Non-Negotiable Engineering Rules

1. Every current library crate is `no_std`; `alloc` and `std` are explicit and
   localized when a milestone proves they are needed.
2. No source file exceeds 500 physical lines. Modules split by semantic
   responsibility and invariant ownership, never merely at a line boundary;
   large corpora, compile-fail cases, and generated evidence stay outside
   production modules.
3. Public behavior is total over its documented inputs: success or a typed
   bounded error, never a panic.
4. Unsafe code remains forbidden in protocol and policy code. Future FFI/native
   adapters use a machine-declared native tier, isolate and audit every unsafe
   boundary, and cannot weaken the portable crate policy.
5. Every function, branch, state, parser limit, retry path, feature profile, and
   supported target behavior is testable through injected dependencies.
6. Features are additive. The caller explicitly constructs crypto, TLS,
   transport, storage, solver, and deployment implementations.
7. The newest stable crate/tool versions are checked before a dependency or
   implementation milestone and before release; changes are never made without
   compatibility and security review.
8. RFC text, errata, IANA registries, and provider observations are evidence,
   not assumptions. Stable claims cite exact sections and fixtures.
9. A completed milestone stops. It does not absorb the next milestone merely
   because code is convenient to add.
10. The default feature tier is core-only `no_std` without allocation where
    feasible; `alloc` and `std` are additive, heavy adapters are default-off,
    and multiple available providers never imply automatic selection.

## Core Data And Trust Flow

```text
operator certificate intent
    -> normalization and policy
    -> deterministic issuance machine
    -> persist intended effect and revision
    -> explicit executor performs one authorized side effect
    -> bounded typed event is persisted and applied
    -> returned certificate is parsed and verified
    -> deployment is staged, activated, health-checked, and fenced
    -> ARI/fallback renewal state is durably scheduled
```

At no point may receipt of bytes from the CA bypass local key, SAN, profile,
validity, chain, or deployment policy.

## Foundation Sequence

Versions `0.1.0` through `0.4.5` establish the workspace, release refusal and
reviewed-implementation binding, full offline RFC/errata/IANA/reference
evidence, reproducible SBOMs, cross-target compile CI, threat model, invariants,
the formal trace contract, regression replay, and the candidate pure
effect/backend contract. Versions `0.4.6` and `0.4.7` establish crate/feature
topology and build/API ergonomics. Versions `0.4.8` through `0.4.12` challenge
that candidate boundary with separate unpublished RustCrypto, ring, rustls,
executor-mode, and transactional-store spikes; `0.4.13` replaces the temporary
all-crates policy with machine-readable portable/native tiers. Versions
`0.4.14` through `0.4.21` build eight small independent models rather than one
model that appears to prove unrelated lifecycles, `0.4.22`-`0.4.23` close
semantic module and mutation baselines, `0.4.24` proves the nominal
no-allocation executor contract, and `0.4.25` records an evidence-backed
DER/PKIX build-versus-adopt decision. `0.4.26` confines generic executors to the
local process and reserves cross-process behavior for later purpose-specific
authenticated protocols. `0.4.27` gives those protocols an explicit capability
product so controlled agents and fixed third-party APIs cannot claim the same
endpoint guarantees by implication. The public boundary freezes only after
these empirical and formal checks. Implementation must not start a parser
before its resource budget and source requirements are committed.

Required outputs:

- GitHub, supply-chain, release, pentest, documentation, and compatibility
  policies adapted from the reference projects;
- tracked, unmodified, integrity-locked RFC reference set excluded from Cargo
  packages, with a reproducible fetch/check manifest;
- conformance matrix keyed by source hash, section/paragraph, errata,
  applicability, implementation symbol, and test fixture;
- strict pre-tag and post-tag validation that permits only mechanically
  allowlisted release-evidence finalization after the reviewed implementation
  commit;
- feature-power-set, dependency-direction, public API, compile-time, and
  binary-size regression gates;
- a machine-readable work/requirement DAG with typed RFC, errata, registry,
  threat-control, architecture, compatibility, platform, and security-finding
  sources whose generated views cannot omit, merge, reorder, or silently detach
  a pentest boundary;
- real private adapter/store and DER/PKIX feasibility evidence before their
  public traits freeze, without publishing those spikes as production support;
- executable allocator-free, configuration-bound stack, scratch-lifetime,
  pinning, reentrancy, and
  `Send`/`Sync` evidence for every nominal `no_alloc` executor claim;
- machine-readable crate tiers that keep portable semantics `no_std` and safe
  while allowing later native adapters only narrowly inventoried unsafe FFI;
- a completeness register reviewed whenever scope changes; and
- immutable historical evidence and semantic release-to-release comparison as
  defined by [the regression strategy](REGRESSION_STRATEGY.md).

## Strict Input And JOSE Sequence

Versions `0.5.0` through `0.13.1` build the narrowest critical core:

- budgets precede all untrusted decoding;
- strict types precede protocol models;
- stable errors precede broad flows;
- JSON rejects duplicate keys and unbounded structures;
- borrowed views, caller-provided scratch, bounded sinks, and small capacity
  policies keep the strict core usable without `alloc`;
- base64url, JWK, JWA, thumbprints, JWS, EAB, and rollover use typed purpose-
  specific construction rather than arbitrary JSON values;
- provider-neutral digest, signing, verification, entropy, key-generation,
  security-sensitive transient/durable identity semantics, local/protocol
  staged request identities, versioned canonical policy snapshots, current-
  policy permits, effect-bound authority composition, sealed purpose-specific
  fingerprints, public-key-validation,
  domain-separated `BoundSigner`, and local
  exact-request admission, separate transactional asymmetric-key and symmetric-
  secret onboarding/content binding, narrow quarantined secret-binding
  bootstrap, orthogonal peer-effect outcomes/reconciliation, safe live signer/
  MAC-authority reconstruction, immutable dispatch, and verified signature/MAC
  evidence semantics precede their first JOSE, scheduling, account-adoption,
  CSR, PKIX, DNS update, or challenge consumer while concrete cryptographic
  implementations remain later;
- standards-required SHA-1 is exposed only through purpose-bound OCSP/DNSSEC/
  NSEC3 verification capabilities and cannot become a general or JOSE digest;
- DNS update authentication uses a separate `DnsUpdateMac` capability and
  secret domain that cannot be reused for EAB, and neither a bare secret handle
  nor immutable provider identity proves intended secret content;
- portable secret types never overclaim erasure; an optional native
  `SecretMemory` boundary publishes exact page-locking, dump/swap, guarded-
  allocation, copy-tracking, zeroization, privilege, and platform assurance or
  returns typed unsupported without fallback;
- key disposition uses a shared typed request/receipt/reconciliation contract
  that distinguishes destruction from disablement, scheduled deletion,
  retention, absence, ambiguity, and provider unavailability;
- ACME HTTPS roots, issued-certificate roots, CT log keys, and DNSSEC anchors
  are distinct trust types rather than interchangeable byte collections;
- nonce ownership uses linear, non-restorable authority distinct from secret
  material; a parsed nonce remains an observation until authenticated origin,
  effective-URL, framing, operation, grammar, directory, and bounded local
  duplicate/consumed-window checks promote it; the client never claims global
  server uniqueness, and authenticated `badNonce` reserves its nonce for the
  complete rebuilt retry; and
- Kani, differential parsing, fuzzing, and Loom begin with the primitives they
  protect rather than being postponed to final qualification.

Crypto implementations do not enter this phase. Golden tests use deterministic
test signers and verify exact signing inputs. Real providers arrive only after
the provider-neutral key roles are stable.

Public-material validation, signer-handle binding, and per-request authority
are separate capabilities. Current `ValidatedPublicKey` evidence feeds a
transient non-serializable `BoundSigner`, established once per bounded
provider/session/key-health context by native pairwise consistency or a fresh
entropy-backed canonical `SignerBinding` transcript. The narrowly privileged
`bind_signer` provider operation is explicitly exempt from ordinary admission,
accepts only that transcript, cannot sign arbitrary bytes or protocol requests,
and yields no binding after failure or ambiguity.

Mutable aliases, labels, names, and persistent references are discovery inputs,
not authority identities. Binding resolves them to an immutable provider-native
key identity/version and canonical public-key digest. `BoundSigner`, admission,
and provider dispatch all pin that same identity.

Each ordinary handle-backed signature effect then consumes a private,
single-use `SignerConsumerAdmission` minted locally from `&mut BoundSigner` for
the exact canonical signing bytes, algorithm/parameters, output format, role,
request identity, and replay nonce where applicable. Minting performs no
provider signature, so rate-limited, costly, remote, HSM, and user-presence
signers pay the binding proof once per bounded signer session rather than once
per request. Admissions have unique bounded outstanding identities, are
consumed immediately before signer dispatch, and are never restored after
success, failure, cancellation, ambiguity, `badNonce`, or ambiguous network
transmission. Provider/session/policy/key-health change or expiry invalidates
the signer and every derived admission.

Provider output is private untrusted `UnverifiedSignature`. Before any JWS,
CSR, revocation, TLS-ALPN, audit, or other effect can use it, Vardheim locally
verifies the exact admitted bytes, algorithm, parameters, output encoding,
immutable provider identity/version, and bound public key. Only successful
verification constructs `VerifiedSignature`. `ProviderAssertedSignature` and
`AttestedSignature` remain separate evidence and cannot construct it.
`VerifiedSignature` always means exact cryptographic verification and records
independent axes for execution locality, signer/verifier trust-domain and
implementation relationships, validated-module identity, key/input binding,
and verifier implementation/session. Baseline production requires
exact local cryptographic verification. A local software signer may use its own
conforming implementation; diversity is an optional stronger profile. Remote
self-verification remains insufficient, and a FIPS-only profile keeps required
verification inside its exact validated boundary. Unsupported, unavailable,
malformed, wrong-key, or failed verification sends nothing, consumes the
admission, invalidates or quarantines authority by policy, and never selects an
implicit signer or verifier fallback.

Security-sensitive identities come only from the `0.10.23` typed issuer
interfaces. `EffectId`, `AttemptId`, `ReconciliationId`, and
`ProviderIdempotencyId` are durable before crossing a crash, process, or
external-effect boundary. `AdmissionId` and `SessionId` are transient,
non-serializable, and process/session-bound; `CorrelationId` is observational
only; `CallerIdempotencyKey` is namespace-bound untrusted input. Each issuer
states transactional uniqueness within a store/recovery epoch, cryptographic
collision resistance, and bounded local duplicate detection independently.
The early release supplies fake durable issuers and fully local no-store signing;
the real store/outbox allocator arrives in `0.34.3`.

`0.10.25` separates transient `LocalSigningRequestId` from the durably reserved
protocol identity base. `0.10.27` then makes protocol identity a consuming
sequence: `ReservedProtocolRequestId` ->
`InputBoundRequestId<SigningInputFingerprint>` ->
`LocallyVerifiedRequest` ->
`FinalizedProtocolRequest<FinalRequestFingerprint>` ->
`OutboxCommittedRequest`. Signer dispatch consumes input-bound state. Exact local
verification creates the local-verified state owning signature/image inputs;
successful inert encoding privately creates one unsplit finalized aggregate of
verified ID and encoded image. Encoding failure abandons rather than restoring
input-bound authority. Public store transactions return assertions; only sealed
core qualification plus the same aggregate commits. Failure, ambiguity,
cancellation, `badNonce`, invalidation, or restore never advances/reuses a
predecessor. `0.10.30` tombstones interrupted work; retry is wholly new.

Every admitted effect binds an immutable canonical `PolicySnapshot`. Its
identity includes policy schema/canonicalization version and digest algorithm;
its digest covers the complete normalized effective policy, including defaults,
inheritance, trust/provider capability snapshot identities, and unsupported-
cell decisions. Schema/compiler/normalization or hash changes create a new
identity even when displayed policy is equivalent; raw text, partial reloads,
and unresolved policy produce no snapshot. Immediately before dispatch, `0.10.24`
requires a transient single-use
`EffectDispatchPermit` proving the worker's policy, trust, and provider epoch is
still current. Pre-dispatch changes block the effect; racing changes preserve
`MayHaveDispatched`; a result observed after a change is recorded but cannot
activate or deploy a now-forbidden artifact. Persisted policy decisions are
facts, not authority, and old committed bytes are never rebuilt or re-signed.

`0.10.26` binds that permit to exact purpose, effect/request state, the
`0.10.28` purpose fingerprint, adapter/session, tenant/resource generation,
lease/fence, deadline/clock epoch, and policy snapshot. Private
purpose-specific constructors consume the permit together with the matching
signer admission, durable commit, presentation intent, verified generation, or
cleanup ownership. Executors receive one checked same-effect authority, never a
bag of independently valid tokens that can be stitched together.

`0.10.28` forbids generic effect digests. Exact signing/protocol wire effects
use `SigningInputFingerprint` or `PeerEffectFingerprint<Protocol, Revision>`.
Final ACME requests use `FinalRequestFingerprint` over the `0.10.29` canonical
`AcmeRequestImage`; physical HTTP/TLS/QUIC framing is never authority. Non-wire
effects use only sealed `StoreMutationFingerprint<Schema>`,
`PresentationFingerprint<Method, Revision>`,
`DeploymentFingerprint<Generation>`, or `CleanupFingerprint<Resource>`, each
binding domain separator, schema/canonicalization version, digest algorithm,
complete normalized fields, purpose, and effect type. There is no semantic-to-
wire or cross-purpose conversion.

The canonical ACME image contains method, a borrowed exact verified JWS body,
single-source `SignedRequestTarget<'a>` over one `ExactAcmeUrl<'a>`, and closed
`AcmeRequestMetadata`. One private target constructor derives component ranges
and origin; path/query is only a borrowed view, and decoding recomputes all
derived values. Normalization is origin-policy-only. Metadata extensions come
only from a sealed registry defining grammar, cardinality/combination, profile
eligibility, fingerprint participation, owned-field conflicts, sensitivity,
and redaction; it starts empty, and raw authority/framing/auth/cookie/proxy/
content-encoding fields are forbidden. A closed table derives transport fields
from target/body/profile. Middleware cannot inject or override them.

`0.10.31` is transactionally inert: length/capacity preflight, complete fill,
and one-time fingerprint finalization atomically consume `LocallyVerifiedRequest`
into private `FinalizedProtocolRequest { id, image }`. Its fields cannot split,
and errors abandon the attempt. Encoding into storage/network/observable sinks
is not an API. Published bounds retain `no_std`/`no_alloc`.

`0.10.32` defines the single-copy stored representation and decoder. Recovery
recomputes URL ranges/origin, sealed-header admission, length, and fingerprint
into bounded non-authority `ValidatedStoredRequest`; persisted derived values
are absent or checked caches and cannot reconstruct live authority.

`0.10.33` exposes publicly implementable general store transactions receiving
a core-created read-only finalized-request view and returning untrusted
`StoreAssertedCommit`. The `0.6.6` sealed promoter checks adapter/session,
transaction, request/fingerprint, assurance, policy, and atomicity/durability
profile before `QualifiedDurableCommit`; only it plus the same unsplit aggregate
commits live work. Restart instead joins non-authority `ValidatedStoredRequest`
with qualified evidence for its exact record/fingerprint and never recreates
finalized authority. Built-in streaming is private. Third-party atomicity/pre-
commit visibility/durability remain explicit TCB claims, never Rust guarantees.

Invalidation has an explicit dispatch boundary. If observed before signer
dispatch, the operation is prevented. If it races with or follows dispatch,
the outcome is ambiguous unless positive provider evidence proves a narrower
result. The admission stays consumed. A replacement attempt revalidates the
key, establishes a new `BoundSigner`, constructs a new request identity, and
mints a new admission; it never retries under the old identity.

Handle-backed EAB and TSIG MAC authority follows a separate shared boundary.
Discovery aliases resolve to a transient `BoundMacKey` that pins the immutable
secret identity/version, tenant, directory or zone, provider/session,
algorithm, policy, purpose, health epoch, and expiry. A single-use
`MacConsumerAdmission` binds the exact canonical input, request identity,
output/truncation policy, and TSIG request/response/chaining state and is
consumed before immutable-identity dispatch. Provider bytes remain
`UnverifiedMac`.

Software or exportable-secret backends independently recompute and compare the
MAC in constant time before constructing purpose-specific `VerifiedMac`.
Opaque HSM, KMS, secret-manager, remote, and platform adapters may instead
return only separately typed `ProviderAssertedMac` evidence with an explicit
assurance profile when independent verification is impossible.
`CryptographicallyAttestedMac` requires a verified signed/native replay-
protected receipt over the complete provider/session/secret/input/output/
algorithm/purpose/request/profile transcript. Neither type can be promoted to
`VerifiedMac`; EAB and TSIG reject both by default unless policy explicitly
admits the exact provider, evidence class, and profile. No unavailable
verification path exports the secret, changes providers, exposes raw usable MAC
bytes, or restores a consumed admission.

Symmetric-secret creation, import, and adoption has a separate transactional
model because public-key validation cannot prove secret content. Stable request
and provider idempotency identities drive a
`SecretLifecycleState × SecretObligationSet` product with typed
definitely-not-created, created, ambiguous, and unavailable observations.
Created objects stay quarantined while reconciliation, content binding,
revalidation, source destruction, disposition, or operator obligations remain.
Binding is explicitly `LocallyCompared`, `PeerConfirmed`,
`CryptographicallyAttested`, `ProviderAsserted`, or `Unverified`, in descending
assurance; provider assertion is rejected by default and unverified is never
usable. Source material remains retained until binding and its durable receipt
commit.

A private single-use non-serializable `SecretBindingAttempt`, minted only from
the exact mutable quarantined onboarding transaction, breaks the binding cycle.
It pins provider/session, immutable secret identity/version, tenant, peer and
directory/zone scope, external-account or TSIG identity, algorithm, purpose,
policy, fresh transcript, onboarding request, binding mode, and stable attempt
identity. Its local variant permits only the domain-separated binding
transcript. Its peer variant permits only the exact typed confirmation effect.
It cannot create normal `BoundMacKey`/`MacConsumerAdmission`, MAC arbitrary
bytes, or service unrelated EAB/TSIG requests, and it is consumed before
provider dispatch without restoration after any outcome.

Peer confirmation uses a stable external-effect identity and sealed
`PeerEffectFingerprint<Protocol, Revision>`, peer/security profile, mutation
class, reconciliation key, affected account or DNS resource, and authenticated
evidence contract. State is `DispatchKnowledge × OperationOutcome ×
BindingEvidence × ObservationStatus`, not a flat result enum. Dispatch knowledge, operation
success/rejection, purpose-specific peer confirmation/content mismatch, and
observation availability change independently. Unauthenticated errors prove
none of those security facts; `badNonce`, rate/contact/ToS rejection, and DNS
`REFUSED` do not imply secret mismatch; observation unavailability cannot turn
a may-have-dispatched effect into a definitely-unsent one. Ambiguous effects
are never blindly retried. EAB account success can jointly commit peer binding
and durable account state. TSIG prefers authenticated non-mutating probes; a
mutating UPDATE must define ownership, duplicate behavior, rollback/cleanup,
and reconciliation.

Recovery follows one table. Before provider MAC dispatch, close with positive
unsent evidence and mint a wholly new attempt. After MAC consumption but before
any outbox envelope, prove network dispatch was impossible, discard transient
artifacts, and start fresh. Dispatch a committed envelope exactly as stored
without rebuilding or re-signing. Once dispatch starts or may have started,
reconcile and do not resend. A new attempt after positive definitely-unsent
evidence is not restoration or reconstruction of the consumed capability.

EAB uses one consumed `EabAccountCreationAttempt` typestate:

```text
Prepared -> InnerMacVerified -> OuterSignatureVerified
         -> OutboxCommitted -> Dispatched -> Reconciled
```

It immutably joins account intent/contacts/ToS, directory and exact
`newAccount` URL, account JWK and signer identity/session, EAB key ID and
secret identity/version/algorithm, inner protected header/payload/positive MAC
evidence, outer nonce/signing input/admission/verified signature,
bootstrap/account/outbox identities, `LocallyVerifiedRequest`, unsplit
`FinalizedProtocolRequest`, store assertion, and qualified durable commit. Each
transition consumes its predecessor. Only purpose-matching positive MAC
evidence completes the inner JWS; only `VerifiedSignature` over the exact
complete outer input completes the outer JWS; only a durable commit makes the
effect executable. No field or evidence can be stitched across attempts.
Authenticated `badNonce` consumes the whole attempt and rebuilds both layers
with fresh nonce, bootstrap, MAC, admission, request, effect, and outbox
identities.

Durable orchestration commits binding-attempt intent before privileged provider
MAC dispatch and the exact peer-effect envelope before network dispatch.
Attempt consumption, outbox/transmission state, account or DNS mutation,
binding evidence, source-secret retention/destruction, lifecycle, and
obligations are ordered and fenced. Live EAB typestates and evidence are never
serialized; before outbox commit only redacted phase facts/digests persist,
then the complete verified request bytes become the immutable outbox payload.
Result application is once-only.

Every process/provider session reconstructs reusable MAC authority by resolving
the exact immutable secret identity/version and performing a fresh safe
non-mutating comparison, admitted current attestation/assertion, or
authenticated non-mutating peer probe. Persisted lifecycle state, historical
peer/attestation receipts, and audit history cannot become `BoundMacKey`,
`MacConsumerAdmission`, `VerifiedMac`, `ProviderAssertedMac`, or
`CryptographicallyAttestedMac`. Restart never automatically repeats mutating
EAB account creation or DNS UPDATE. Mutating-only peer profiles require
explicit reconciliation/operator policy; one-time EAB material proceeds to
disposition after durable account success. Object restore/recreation, alias
retargeting, or provider/policy/peer/assurance change leaves a reusable secret
eligible but unusable until safe reconstruction.

Key creation, import, migration, and platform adoption are transactions, not
handle-returning shortcuts. A stable request ID and provider idempotency token
drives a durable `KeyLifecycleState × KeyObligationSet` model, with direct
typed observations for definitely-not-created, created, ambiguous, and
unavailable outcomes. Lifecycle values cover requested, creation-unknown,
created-quarantined, active eligibility, retained quarantine, and retirement;
orthogonal obligations cover reconciliation, validation, binding,
revalidation, disposition, and operator decision. Tenant, role,
algorithm/parameters, provider, intended key version, origin, exportability,
persistence, attestation, policy, observed immutable provider identity/version,
and canonical public-key digest remain bound throughout. Mutable locators are
metadata only. Created or imported keys are unusable while quarantined. A
durable active value is only inventory/policy eligibility, never present
signing authority.

Persisted validation/binding history cannot become `ValidatedPublicKey`,
`BoundSigner`, request admission, or an effect capability. Every process and
provider session reconstructs fresh validation and binding before signing.
Restart, provider-session or policy change, key-health epoch change, handle or
public-key replacement, KMS alias/version retargeting, or HSM object recreation
invalidates live authority and adds a revalidation obligation. Lost responses,
eventual provider visibility, unreadable attributes, validation/binding
failure, restart, and duplicate requests retain durable reconciliation or
key-disposition obligations. Concurrent reconstruction/reconciliation is
fenced, and stale workers cannot publish authority or clear obligations.
Lookup failure or object absence never proves destruction.

## RFC 8555 Sequence

Versions `0.14.0` through `0.25.2` implement the entire client side of RFC 8555
in resource order: bounded transport semantics, URL/origin policy, directory,
`newNonce`, account creation, recovery and explicit adoption, lifecycle,
rollover, multi-issuer policy, orders, ordinary and `newAuthz`
pre-authorizations, polling, finalization, retrieval, revocation, problems, and
pagination.

Existing-account adoption accepts a directory URL, account URL, and signer/key
handle only as inputs. Ownership is established by local signer/public-key
validation plus role-specific `BoundSigner`, exact-request admission, and a fresh
authenticated POST-as-GET whose effective URL and account object bind to the
same directory. Account creation and recovery require the same current
validation, binding, and admission before their first signed effect. Operator assertions,
parsed public material, cached or unrelated signatures, and possession of an
account URL are never proof. Imported, created, and recovered provenance remain
distinct and non-exportable HSM/KMS signers are first-class.

Account rollover does not end at a successful response parser. Both old and new
signers require their own current validation, role-specific binding, and
exact-request admission before the nested rollover signatures are constructed,
and both keys remain protected
until a fresh authenticated account observation proves which signer controls
the account and that evidence is durable. Ambiguous rollover or deactivation
keeps disposition pending; disablement, retention, scheduled deletion,
destruction, legal hold, and provider unavailability use the shared
disposition/reconciliation contract.

Each operation has:

- a pure request constructor;
- a bounded response parser;
- state preconditions and postconditions;
- nonce handling and retry classification;
- unknown-outcome reconciliation rules;
- positive, negative, malformed, and limit fixtures;
- section-level conformance evidence.

No generic “retry request” helper may hide whether an operation is safe to
repeat. `newOrder` and other ambiguous outcomes enter reconciliation first.

## Challenge And Certificate Sequence

Versions `0.26.0` through `0.31.3` implement HTTP-01, introduce
`vardheim-pkix`, place canonical DER writing/reading and shared algorithm
identifiers before CSR, add isolated test-only real crypto for genuine early
interoperability, and complete CSR policy, full RFC 5280 path/policy behavior,
bounded local OCSP/CRL/CT parsing and cryptographic verification, credential-
free public-PKI acquisition, alternate chains, and transient context-bound PKIX
evidence. RFC 6962 CT v1 SCTs and RFC 9162 CT v2 `TransItem` evidence use
separate bounded types, log identities, signature inputs, precertificate
reconstruction, log-list capabilities, and verification results; no conversion
or fallback crosses versions. Challenge presentation is a transaction: prepare,
present, visibility barrier, self-check, CA acknowledgement, poll, and owned
cleanup. Cleanup obligations are persisted; async destruction is never relied
upon.

Separate private test verifiers supply genuine pinned status/CT and DNSSEC
algorithm coverage before production providers exist; neither is shipped or
presented as a supported backend.

DER primitive conformance is complete before certificate semantics. Canonical
zero, positive, and negative INTEGER/ENUMERATED values are accepted while
nonminimal encodings fail; OID, BIT STRING, BOOLEAN, zero-length NULL,
constructed/primitive form, SET ordering, and length encodings are canonical
and bounded. Context schemas impose positivity, range, and zero restrictions.
Certificate envelopes then enforce field ordering and version legality,
positive serial policy, normalized inner/outer algorithm-and-parameter
equivalence through the shared algorithm model, unique-ID and extension version
gates, duplicate extension rejection, unknown-critical rejection unless a
profile assigns a handler, and empty-subject/critical-SAN rules before issuer
search or path validation begins.

Public-key parsing is not public-key validation. JWK and SPKI material passes
through a provider/session-bound validation capability covering RSA integer and
size/exponent policy, exact Weierstrass curve binding and point validity, and
Ed25519/Ed448 encoding plus algorithm-specific weak/small-order policy.
Algorithm/parameter identities must agree across JWK, SPKI, CSR, certificate,
and provider capability. `ValidatedPublicKey` evidence is transient and cannot
be restored, crossed between providers/policies, or promoted into signer-handle
authority. Handle-backed account, rollover, CSR, certificate-key revocation,
and TLS-ALPN certificate-signing consumers separately require current
`BoundSigner` established through the domain-separated ceremony or native
pairwise consistency, followed by locally minted single-use
`SignerConsumerAdmission` for the exact request.
Issued leaf keys are validated even when no signature is verified with them.

Certificate verification compares:

- order identifiers;
- CSR identifiers and public key;
- returned leaf SANs and public key;
- requested certificate profile, TLS Feature requirements, and validity;
- chain candidates against a versioned immutable issued-certificate trust
  snapshot and policy, never implicitly against ACME transport roots.

Non-certificate PEM objects are rejected, including server-injected private
keys.

The no-allocation validation tier receives caller-provided path candidates,
policy-tree arenas, OCSP/CRL extensions and entries, CT v1 SCT lists, CT v2
`TransItem` collections, DNSSEC RRsets, chains, and denial-proof workspaces.
Capacity exhaustion is a deterministic typed result. The `alloc` tier may
provide owned convenience wrappers but cannot change validation semantics or
budgets.

OCSP verification classifies `nocheck`, archive-cutoff, extended-revoke, and
other RFC 6960 extensions explicitly. Leaf and intermediate status requirements
are independently configurable, delegated-responder recursion is bounded, and
an uncheckable responder certificate cannot silently satisfy a required status
policy. OCSP acquisition can require POST and partitions caches by request body,
tenant, purpose, privacy policy, and policy version.

One shared strict ASN.1/PKIX time layer parses certificate, CRL, OCSP, and
CMS/CT fields. It enforces RFC 5280 UTCTime/GeneralizedTime year selection,
Zulu and seconds requirements, profile-specific fraction/offset rejection,
calendar and interval validity, explicit leap-second policy, and checked
conversion into Vardheim wall time without locale/system parser behavior or
lossy timestamps.

Distinguished-name equality is also a first-class primitive rather than a path
builder detail. It preserves RDN sequence, treats attributes within an RDN as a
set, compares exact attribute OIDs, applies RFC 4518 StringPrep/caseIgnoreMatch
and domainComponent rules, and returns typed unsupported results when an
attribute's required equality rule cannot be implemented safely.

Certificate renewal selects a durable key mode: always rotate, reuse only
within explicit count/time limits, provider-managed rotation, or forced
rotation after compromise or relevant policy/provider/attestation change. The
chosen key generation and reason are part of renewal intent and cannot change
implicitly after restart or retry.

## Durable Orchestration Sequence

Versions `0.32.0` through `0.39.5` add the pure
command/state/policy/event reducer, typed effects and positive evidence,
snapshots, migrations, CAS revisions, outbox effects, leases, fencing, stores,
durable peer-binding effect/reconciliation orchestration, transactional
composed-EAB execution, system-wide restored-store recovery epochs,
externally rooted rollback assurance and explicit coverage manifests,
store-backed durable protocol-request reservation/unsplit finalization/public
store assertion/sealed commit qualification/non-authority recovery validation
and interrupted-request abandonment tombstones, transactional deployment,
current-policy dispatch
authorization, public APIs,
reusable adapter
and composed-effect conformance, a deterministic hostile CA, a test-only
loopback transport, a production wall/monotonic clock adapter, Pebble
integration, historical differential replay, existing-certificate adoption,
renewal bootstrap, and durable multi-issuer migration policy.

Snapshots contain lifecycle/inventory facts, orthogonal obligation sets, audit
records, durable peer-effect state, and invalidation inputs, never live
validation, signer/secret binding, `SecretBindingAttempt`, request-admission,
verification, or effect-authority capabilities. Restart, migration,
process/provider-session change, issued-trust/policy/status/CT/algorithm/key-
or-secret-health change, handle/public-key or alias/version replacement, and
renewed verification time create mandatory safe reconstruction obligations
before deployment, signing, EAB, or TSIG use. Reconstruction never
automatically repeats a mutating peer effect. Durable `Active` is lifecycle
eligibility only.

A whole-store rollback is a discontinuity, not an ordinary restart. Stores
publish exact `RollbackProtected`, `RollbackDetecting { maximum_window }`, or
`RollbackUnprotected` capability; a changed `StoreEpoch`/`RecoveryEpoch`,
detected restoration, or
operator declaration invalidates leases, fences, sessions, caches, and all live
authority. Restored outbox work, key eligibility, challenge ownership,
deployment generations, retirement, trust, and provider state remain
quarantined until operation-specific reconciliation and revalidation complete.
Where monotonic secure state is unavailable, restoration must be declared by
the operator or rollback detection remains explicitly unsupported.

`RollbackProtected` prevents or detects rollback for every protected committed
effect. `RollbackDetecting { maximum_window }` detects only rollback crossing
the last witnessed head and exposes the bounded unwitnessed window.
`RollbackUnprotected` makes no automatic claim. Automatic detection requires
an injected authenticated `RollbackWitness` outside the store failure domain;
its trust root, bootstrap identity, and replacement authority also live outside
the restored store. It binds store identity and state-head digest to a monotonic
counter or journal and defines recovery for store-before-witness and witness-
before-store crashes, partitions, reset/clone/split-brain, loss, and key
rotation. High-assurance startup rejects rollback-unprotected storage; a named
operator-selected reduced profile is required to proceed.

Every store/witness profile also publishes a closed `RollbackCoverage` manifest
binding its state-head construction to store namespaces, record/effect types,
tenant/partition scope, and schema version. Protection and detection claims
apply only to that set. Unknown, omitted, or uncovered dependencies are
unprotected and block higher-assurance authority rather than inheriting a store-
wide label. A coverage change creates a new authenticated profile identity and
enters recovery review.

Audit records retain stable invalidation reasons so operators and future
regression replay can distinguish trust removal, explicit distrust, policy
change, expiry, clock rollback, status/CT change, algorithm/provider-session or
key-health change, handle/public-key or alias/version replacement, and input
mutation.

Every external side effect follows:

1. validate it against current state and policy;
2. bind an immutable policy snapshot and persist intended effect and revision;
3. prove the policy/trust/provider epoch is still current and consume an
   exact-effect checked authority that composes `EffectDispatchPermit` with the
   matching request typestate, purpose fingerprint, admission/commit/ownership/
   fence immediately before execution;
4. execute with an idempotency/reconciliation classification;
5. receive a bounded adapter observation with independent dispatch, outcome,
   and observation-status axes;
6. structurally/contextually validate it and apply current policy before
   constructing sealed qualified evidence or activating/deploying the result;
7. persist the typed outcome;
8. apply it once and record cleanup obligations.

`Unsupported`, operation rejection, observation corruption/unavailability, and
dispatch knowledge are never flattened into one error. An adapter can be
unavailable while an operation may have dispatched. Only sealed positive
evidence constructs `DefinitelyUnsent`; provider diagnostics never do.

The test server must kill/restart the orchestrator after every transition and
effect boundary. A stale worker cannot present, finalize, activate, clean, or
roll back after losing its fencing authority.

Generic executors may be async, blocking, polling, or embedded, but remain in
the local process and async never enters the reducer. Static dispatch remains
available without allocation; object-safe executor collections require an
explicit `alloc` feature. Live Rust capabilities are never serialized. Later
remote signer, DNS, KMS, deployment, and agent protocols are purpose-specific
adapter boundaries that return observations only and cannot mint local
evidence. Every boundary publishes `RemoteProtocolCapabilities` for endpoint
authentication, native request-digest and purpose/context binding, provider
idempotency, replay protection, dispatch acknowledgement, recovery-epoch
binding, signed attestation, and reconciliation. Vardheim-controlled agents
must meet the named full profile; fixed APIs such as AWS KMS, Azure Key Vault,
and OpenBao expose unsupported cells and only explicit local compensation.
Backend features only expose constructors and never select an implementation.

## Renewal And Challenge Ecosystem

Versions `0.40.0` through `0.51.5` implement ARI, durable scheduling,
certificate/account-key compromise response, certificate retirement,
key/artifact destruction, inventory reconciliation, post-deployment status
response, high-level lifecycle methods, provider-neutral DNS/EDNS query
behavior, provider adapters, the restricted DNS agent, complete local DNSSEC
validation, TLS-ALPN-01, RFC 7633 Must-Staple lifecycle, and rustls/OpenSSL
staple consumers. It also schedules CT inclusion audits for every accepted
v1/v2 SCT and can consume independent witness/gossip evidence without treating
it as log proof.

DNS propagation checks query authoritative servers and derive secure, insecure,
bogus, and indeterminate results from canonical RRsets, DNSKEY/DS/RRSIG
verification, root-to-leaf chains, NSEC/NSEC3 denial, time policy, and explicit
trust anchors. An unauthenticated AD bit is never evidence; authenticated
validating-resolver evidence is an explicit policy alternative. Provider record
handles preserve unrelated TXT data and enable exact cleanup. Heavy AWS and
Azure SDKs stay outside core dependency graphs.

Authoritative discovery distinguishes answers, downward referrals, partial
answer/referrals, and lame or upward responses using AA, section placement,
zone cuts, and SOA ownership. It validates in-domain, sibling, and
out-of-bailiwick glue; resolves missing nameserver A/AAAA records iteratively;
processes CNAME and DNAME synthesis; and bounds aliases, referrals, nameserver
dependencies, addresses, servers, and total work without ambient system
resolution.

DNS queries construct and parse bounded EDNS(0), request DNSSEC material with
DO, use fresh unpredictable transaction IDs and UDP source ports/socket
rotations for every attempt, and bind responses to the complete local/remote
tuple, server, transport, question, and attempt. Truncated responses retry with
a fresh ID over a bounded RFC 7766 two-byte-framed TCP codec that handles
partial and out-of-order frames. Optional RFC 7873/9018 DNS Cookies are
server-scoped defense in depth and never replace tuple correlation, DNSSEC, or
TSIG. EDNS fallback cannot silently remove semantics required by local DNSSEC
validation.

RFC 2136 UPDATE and RFC 8945 TSIG are first implemented against provider-neutral
contracts and genuine private test cryptography. The production adapter is
deliberately later, after the dedicated RustCrypto `DnsUpdateMac` backend; an
unauthenticated or incorrectly chained TSIG response can never confirm success.
Request and response MAC construction uses the shared `BoundMacKey`,
single-use exact-input admission, immutable secret-version dispatch, and
positive evidence boundary. Secret aliases cannot authorize an UPDATE,
provider-returned bytes cannot directly form TSIG, and independently verified
MAC evidence remains distinct from explicitly policy-admitted provider
attestation.

TLS-ALPN-01 identity construction remains independent from rustls. The rustls
resolver activates only for matching identifier, exact `acme-tls/1`, and an
active unexpired owned presentation. Its ephemeral certificate signature is
constructed only after current validation, TLS-challenge-role binding, and
exact-request admission; an account, CSR, revocation, normal-certificate, or
cached signature cannot satisfy that admission.

Certificates requiring `status_request` are not activated without fresh locally
verified OCSP evidence. Certificate, key, chain, and staple form one fenced
deployment generation; refresh failure follows explicit hard-fail, rollback,
and last-serving-generation policy.

CT monitoring verifies version-specific STH signatures, Merkle inclusion, and
append-only consistency after each log's MMD, retains durable checkpoints, and
classifies outage, disqualification, closure, missing inclusion, rollback, and
split view. Optional witness quorum/diversity policy can escalate conflicting
views but cannot construct SCT, STH, inclusion, or consistency evidence.

## Transport And Crypto Sequence

Versions `0.52.0` through `0.66.5` introduce strict ACME transports, a separate
credential-free `PublicPkiFetch` implementation, async/blocking/embedded
profiles, purpose-specific key/MAC/sign/verify/generation capabilities,
RustCrypto including EAB HMAC and RSA-PSS, ring, aws-lc-rs, separate AWS-LC
FIPS, purpose-bound legacy verification hashes, DNSSEC algorithms, and TSIG
HMAC, custom/platform issued-certificate trust providers, PKCS#11, TPM2, AWS
KMS, Azure Key Vault, OpenBao-compatible, and remote/offline signing.

Every production transport explicitly selects HTTP/1.1, HTTP/2, or HTTP/3 and
implements one replay-safety contract. TLS/QUIC early data is disabled, adapter
and middleware retries are disabled, and only protocol evidence can classify a
request as definitely unsent. Partial writes, resets, cancellation, response
loss, and unproven GOAWAY/stream outcomes are ambiguous and enter ACME
reconciliation. Connection, TLS/QUIC session, resolver, proxy, directory,
tenant, trust, and policy state are partitioned; cross-origin coalescing is off
unless a version-specific proof permits it. HTTP/1.1 is the initial mandatory
profile, with RFC 9113 HTTP/2 and RFC 9114 HTTP/3 admitted separately.

Public PKI fetching may use HTTP or HTTPS according to explicit policy but has
dedicated configuration and pools, no ACME/cookie/proxy/ambient credentials,
strict SSRF and cache bounds, and returns only untrusted bytes. Decompression is
disabled by default or has independent encoded/decoded/work budgets; HTTP
framing rejects CL/TE ambiguity, incomplete bodies, excessive chunks/trailers/
informational responses, and wrong purpose-specific media types. Cache identity
includes URL, method, request-body digest, tenant, purpose, policy, trust, and
privacy context. OCSP, CRL, AIA, certificate, and CT signatures—not delivery
authentication—establish object authenticity.

Platform issued-trust adapters preserve platform constraints, distrust, and
scope or return typed unsupported; flattening roots into DER never implies
native-equivalent trust. Optional migration import accepts bounded PKCS#1 RSA
and SEC1 EC keys only to validate and convert them into PKCS#8 or an opaque
provider lifecycle through transactional quarantined onboarding, and never
exports legacy formats. PKCS#8, PKCS#12, software generation/import, hardware
creation, KMS creation/import, and platform-key adoption use the same staged
activation contract.

Each provider implements capabilities and is explicitly selected. ring,
aws-lc-rs, and AWS-LC FIPS publish per-purpose capability tables covering JOSE,
CSR, X.509, OCSP, CRL, CT v1/v2, TLS-ALPN, DNSSEC, TSIG, key import/generation,
public-key validation, signer binding, immutable signature/MAC dispatch,
returned-signature verification, independent, provider-asserted, or
cryptographically attested MAC evidence, legacy verification hashes, and key
disposition. Every software, HSM, TPM,
KMS, remote, and platform key provider implements the shared validation,
`BoundSigner`, request-admission, and verified-signature conformance boundaries
and maps native states through the shared disposition contract. Every provider
offering EAB or TSIG MAC operations also implements the shared `BoundMacKey`,
exact-input admission, immutable secret dispatch, purpose-specific evidence,
assurance publication, and no-secret-export/no-fallback conformance boundary;
providers without those semantics publish typed unsupported capability cells.
Every symmetric-secret create/import/adopt path additionally implements stable
idempotency, quarantine, typed content binding, lifecycle/obligation
separation, narrow single-use binding attempts, peer mutation/result
classification, persist-before-effect and operation-specific reconciliation,
source-secret disposition, fencing, capability-free snapshots, and safe per-
session reconstruction without mutating-effect replay. A provider that
supports MAC operations but no admitted onboarding/binding/bootstrap mode
remains unusable for new or adopted secrets rather than accepting a bare
handle.
Every EAB-capable signer/MAC/transport/store/executor combination passes the
shared composed-effect suite: exact identity/digest binding across both JWS
layers, consumed typestates, positive evidence at each transition, orthogonal
outcome preservation, committed-byte dispatch, complete `badNonce` rebuild,
fenced reconciliation, once-only application, capability-free persistence,
and no provider or transport fallback.
Native pairwise consistency or the narrow canonical `bind_signer` operation
establishes binding; all request admissions are then minted locally and
consumed before immutable-identity signer dispatch and local output
verification. Every key creation/import path
also implements transactional onboarding, idempotent reconciliation,
lifecycle/obligation separation, quarantine, fresh-session authority
reconstruction, immutable dispatch, mandatory returned-signature verification,
fencing, and cleanup obligations. Invalid keys, wrong handles, stale provider
sessions, replayed history, mutable alias retargeting, wrong-key or malformed
signature output, unavailable verification, failed or ambiguous binding,
ambiguous creation/import, or provider unavailability cannot fall back to
another backend. Scheduled
deletion, disablement, object absence, handle loss, unlink, or zeroization is
never inflated into physical destruction. Unsupported purposes, validations,
bindings, or dispositions are typed and never inferred from an algorithm name.
Unsupported MAC verification, a provider assertion, or a cryptographic
attestation profile is likewise typed and cannot be upgraded into independent
verification or a stronger content-binding mode.
Provider negotiation is:

```text
local key capabilities
    intersect CA protocol capabilities
    intersect operator algorithm policy
    -> one explicit algorithm or a typed failure
```

FIPS is a deployment profile tied to the exact validated module, build,
platform, runtime status, and approved algorithms. It never falls back to a
non-FIPS backend and never claims compliance based only on a feature flag.

## Extensions And Provider Capability Sequence

Versions `0.67.0` through `0.81.0` implement CAA binding/preflight, IP
identifiers, data-driven provider profiles, provider staging conformance, STAR,
S/MIME, delegated STAR, subdomain authorization, authority tokens, TNAuthList,
`.onion`, DTN, NfInstanceId, and stable extension registration.

Unsupported results distinguish standard, client, cryptographic provider, CA,
operator policy, and product restrictions. Protocol code never branches on a
provider name. Observations expire and cannot override operator security policy.

## Production Operations Sequence

Versions `0.82.0` through `0.91.6` implement SQLite, PostgreSQL HA,
multi-tenancy, deployment adapters, Kubernetes, remote deployment agents,
redacted observability, signed audit records, CLI, daemon, hardened agents,
Android Keystore, Apple Keychain/Secure Enclave, Windows CNG/certificate
stores, and optional PKCS#12 interoperability.

Secrets are never ordinary observability fields. Identifier logging defaults to
hashed or redacted. Multi-tenant stores separate encryption, quotas, leases,
accounts, intents, and audit streams.
Handle-backed signed audit checkpoints use immutable signer dispatch and
`VerifiedSignature` before durable commit or export. Authority-token extensions
apply the same rule to any locally signed request/effect, while externally
issued tokens remain verification evidence and cannot manufacture local signer
authority.

## Platform And Assurance Sequence

Versions `0.92.0` through `0.97.3` close platform support, custom target
readiness, and qualification coverage for the Kani, Loom, fuzzing, and formal
models already introduced beside their code, plus Miri, sanitizers, leakage
evidence, and historical trace replay. Versions `0.100.0` through `0.111.0`
isolate revisioned experimental/IESG drafts. Draft work is complete before 1.0
but remains outside stable RFC claims and disabled by default.

## Production Qualification Sequence

The `0.120` alpha/beta/RC series freezes APIs, closes coverage, runs full
interoperability, load/chaos/disaster recovery, reproducible supply-chain
qualification, attributable independent core and adapter audits, FIPS
qualification, and a final signed pentest bound to the reviewed implementation
with zero unapproved finalization changes. `1.0.0` is tagged only after those
gates pass.

## Testing Architecture

The permanent test ladder is:

```text
unit and RFC vectors
    -> compile-fail, property, feature-power-set, API, and size-budget tests
    -> deterministic state-model traces
    -> fuzzing, Miri, Kani, Loom, sanitizers
    -> in-house hostile test CA
    -> Pebble and Boulder subset
    -> staging and controlled provider integrations
    -> opt-in production smoke
    -> independent pentest and audit
```

Coverage numbers are supporting evidence, not permission to leave behavior
untested. Every public function and meaningful private branch must have direct
behavioral tests. Generated code and structurally unreachable defensive lines
need documented exclusions reviewed at the release gate.

Parser and canonicalization fuzzing begins with each boundary, including OCSP,
CRL, SCT, EDNS, TSIG, and DNSSEC RRset processing; `0.96.0` qualifies and
closes those continuously retained corpora rather than introducing them late.

## Dependency Maintenance

Before each milestone:

1. run `scripts/check_latest_tools.sh` and the dependency-current checker;
2. inspect upstream release notes, MSRV, advisories, ownership, features, unsafe
   and native code, and transitive changes;
3. update one boundary at a time;
4. rerun the full compatibility and conformance evidence;
5. record the check date and decision.

Dependabot is a prompt for review, never authority to merge. Cryptographic,
PKIX, JSON, DNS, HTTP, TLS, database, SDK, and CI changes require explicit
security review.

## Completion Rule

If implementation exposes missing security, interoperability, operational, or
standards work, do not mark it out of scope and do not defer it beyond 1.0. Add
a new pre-1.0 version or split the active milestone, update the completeness
register, and stop at the newly created pentest boundary.
