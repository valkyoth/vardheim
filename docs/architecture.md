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

Crate policy is tiered rather than pretending every future operating-system or
FFI adapter has the same build constraints as protocol code. Portable crates
remain `no_std` and safe Rust. A native adapter may use `std` and a minimal
inventoried unsafe module only after its crate, module invariants, owner,
platform evidence, and audit scope are machine declared. Native code depends
inward on safe semantic types; core never depends on it.

## Backend Observation Boundary

Core emits inert purpose-specific effects and accepts bounded observations. An
adapter never returns reducer authority directly and cannot construct sealed
positive evidence such as `VerifiedSignature`, `BoundSigner`, `DurableCommit`,
or `OwnedPresentation`. Backend state is an orthogonal product: capability
support is separate from an admitted effect; dispatch knowledge is separate
from operation outcome; observation availability/corruption is separate from
both. An adapter may be unavailable while an effect may have dispatched.
Only sealed positive evidence constructs `DefinitelyUnsent`; error codes
and bounded redacted diagnostics cannot select retry or narrow ambiguity.

External evidence promotion is explicit:

```text
adapter observation
    -> structural and context validation
    -> policy and assurance check
    -> sealed evidence constructor
    -> reducer event
```

`StoreAssertedCommit` is not `QualifiedDurableCommit`, and
`PresentationObserved` is not `OwnedPresentation`. Qualified evidence binds the
adapter implementation/session, assurance profile, request/effect identity and
digest, resource generation/owner, and validation context. The promoting
facade/policy component and residual trusted-computing-base assumption are
documented. Rust privacy prevents accidental fabrication; it cannot prove a
malicious in-process store performed media synchronization or a DNS provider
published a record. Generic tests reject structural and policy inconsistency,
not a perfectly formed semantic lie from a trusted adapter.

## Executor Process Boundary

Generic blocking, async, polling, embedded, static, and allocation-backed
executors remain local-process drivers. They may hold transient Rust authority
but cannot serialize it, create a generic remote `EffectTicket`, or delegate the
generic executor contract across a process boundary. Later remote signer, DNS,
KMS, secret-manager, deployment, and agent integrations each define a narrow
purpose-specific boundary and return observations only. Every one publishes a
`RemoteProtocolCapabilities` product covering endpoint authentication, native
request-digest and purpose/context binding, provider idempotency, replay
protection, dispatch acknowledgement, recovery-epoch binding, signed
attestation, and reconciliation. Controlled agents implement the named full
profile; fixed third-party APIs publish unsupported cells and explicit local
compensation. A remote endpoint never mints local qualified evidence or
authenticates a field its protocol did not carry.

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
`VerifiedSignature` accepted by protocol effects. `ProviderAssertedSignature`
and `AttestedSignature` are separate sealed evidence and cannot construct or be
treated as `VerifiedSignature`, which always means exact cryptographic
verification. The verified evidence separately binds execution locality,
signer/verifier trust-domain and implementation relationships, validated-module
identity, key/input binding strength, and verifier implementation/session.
Baseline production requires exact local cryptographic verification. A local
software signer may verify through its own conforming implementation; diversity
is an optional stronger profile. Remote self-verification is insufficient, and
FIPS-only profiles keep required verification inside the exact validated
boundary. Unsupported, unavailable,
malformed, or failed verification transmits nothing, consumes the admission,
invalidates or quarantines the signer according to policy, and cannot select a
fallback signer or verifier.

## Security-Sensitive Identity Issuance

Security-sensitive identities use one provider-neutral family of typed issuer
interfaces but have different guarantees. `EffectId`, `AttemptId`,
`ReconciliationId`, and `ProviderIdempotencyId` are durably allocated before
crossing a crash, process, or external-effect boundary. `AdmissionId` and
`SessionId` are transient, non-serializable, process/session-bound, and invalid
after restart. `CorrelationId` is observational only, while
`CallerIdempotencyKey` is namespace-bound untrusted input and never an internal
identity. Each issuer states transactional uniqueness within a store/recovery
epoch, cryptographic collision resistance, and bounded local duplicate
detection separately; entropy never promises absolute global collision
detection. The core-only/no-store profile can mint transient admission and
complete local signing. Durable counter/range or uniqueness-registry allocation
is integrated with the store and outbox in `0.34.3`.

Request identity is separately typed. `LocalSigningRequestId` is transient,
non-serializable, and valid only when neither the result nor any request/effect
crosses a crash, process, outbox, reconciliation, or external boundary.
Protocol identity advances only through consuming states:

```text
ReservedProtocolRequestId
    -> InputBoundRequestId<SigningInputFingerprint>
    -> VerifiedRequestId<FinalRequestFingerprint>
    -> OutboxCommittedRequest
```

The base is durably reserved first. Input binding fixes canonical signing bytes,
algorithm/parameters, nonce, purpose, policy, and signer admission before signer
dispatch. Only local `VerifiedSignature` permits deterministic final
construction of the canonical `AcmeRequestImage`. Only the final-request-bound
state enters outbox or transport. Failure, ambiguity, cancellation, `badNonce`,
invalidation, crash, or restore cannot advance or reuse partial state. If image
and verified identity were not atomically committed, recovery permanently
retires the reservation/nonce/admission/input-bound identity/fingerprints and
records non-authority `AbandonedProtocolRequest`; a later retry is a wholly new
signing operation and never re-signs, advances, or rebinds the old identity.

Invalidation before dispatch prevents signing. Invalidation racing with or
following dispatch makes the signing result ambiguous unless positive provider
evidence proves otherwise; the admission remains consumed. Replacement uses a
revalidated key, new `BoundSigner`, new request identity, and new admission.

## Policy Epoch And Dispatch Authority

Every admitted external effect binds an immutable `PolicySnapshot` containing
the policy epoch, policy schema/canonicalization version, digest algorithm
identity, and digest of the complete normalized effective policy:
explicit and defaulted values, inherited settings, trust/provider capability
snapshot identities, and unsupported-cell decisions. Raw configuration bytes
are not identity; incomplete, unresolved, invalid, or noncanonical reloads
produce no snapshot. A schema/compiler/canonicalization-version or digest-
algorithm change produces a new snapshot identity even when rendered policy is
equivalent. Immediately before adapter dispatch, the local
orchestrator proves its policy, trust, and provider epoch is current and mints a
transient non-serializable single-use `EffectDispatchPermit`. A stale worker or
pre-dispatch policy change receives no permit and operation semantics decide
whether to cancel, quarantine, or build wholly fresh work. A change racing with
dispatch preserves `MayHaveDispatched`. A result observed after a change is
recorded, but current policy must separately authorize activation or deployment.
Persisted old decisions are historical facts, not live authority, and committed
bytes are never rebuilt or re-signed under their old identity.

The permit is purpose-typed and binds effect type, `EffectId`, request state,
purpose-specific fingerprint, adapter implementation/session,
tenant/resource generation, worker lease/fence, deadline/clock epoch, and policy
snapshot. Private constructors produce one same-effect checked authority from:

- `SignerConsumerAdmission + EffectDispatchPermit<Sign>`;
- `QualifiedDurableCommit + EffectDispatchPermit<AcmeSend>`;
- `PresentationIntent + EffectDispatchPermit<Present>`;
- `VerifiedGeneration + Fence + EffectDispatchPermit<Activate>`; or
- `CleanupOwnership + Fence + EffectDispatchPermit<Cleanup>`.

Executors never receive independently mixable tokens. Any disagreement among
the components fails before adapter entry and consumes no unrelated authority.

## Purpose-Specific Effect Fingerprints

There is no generic effect digest. Signing stages use sealed
`SigningInputFingerprint` over exact serialized bytes. Final ACME application
requests use `FinalRequestFingerprint` over canonical `AcmeRequestImage`.
Protocol-specific peer effects use `PeerEffectFingerprint<Protocol, Revision>`
over their exact wire message or declared canonical image. Effects without a
wire/image representation use `StoreMutationFingerprint<Schema>`,
`PresentationFingerprint<Method, Revision>`,
`DeploymentFingerprint<Generation>`, or `CleanupFingerprint<Resource>`.
Every semantic fingerprint binds a domain separator, schema/canonicalization
version, digest algorithm, complete normalized fields, purpose, and effect type.
Wire, application-image, and semantic fingerprints, and different families,
have no implicit conversions. Changing schema/canonicalization or digest identity
changes the fingerprint identity even when display text is unchanged.

## Canonical ACME Request Image

`AcmeRequestImage` is immutable application authority, not physical transport
serialization. Its versioned canonical form contains method, a borrowed exact
verified JWS body, `SignedRequestTarget`, and closed `AcmeRequestMetadata`.

`SignedRequestTarget<'a>` owns one authoritative `ExactAcmeUrl<'a>`. Its private
validating constructor derives `UrlComponentRanges` and `OriginIdentity` from
those same bytes. Path/query and authority are borrowed views, never caller-
supplied or independently persisted values. Decoding recomputes ranges and
origin; any cached mismatch fails closed. Exact target identity never
normalizes percent encoding, dot segments, default ports, empty paths, query
ordering or duplicates, host representation, IDNA form, or IPv6 literal
spelling into equivalence. The JWS protected URL and committed target validate
together. After transport, `ObservedEffectiveUrl` is evidence compared with the
committed target and redirect/origin policy; it cannot modify the image.

`AcmeRequestMetadata` is a closed typed projection containing
`content_type: ApplicationJoseJson`, optional typed `accept`, and extensions
admitted only through a sealed registry. Each registry entry fixes canonical
name/value grammar, cardinality and combinations, HTTP/1.1/2/3 eligibility,
authority/fingerprint participation, owned-field conflicts, sensitivity, and
redaction. The registry begins empty. Host, pseudo-headers, Content-Length,
Transfer-Encoding, Connection, Authorization, cookies, proxy credentials, and
content-encoding controls can never be extensions. A normative ownership table
derives target/authority fields from `SignedRequestTarget`, Content-Length from
the exact body, and transfer/connection fields from the profile. Unknown,
duplicate, conflicting, or profile-ineligible fields fail closed.

`FinalRequestFingerprint` covers the image. `encoded_len_checked()` validates
all lengths and complete caller-buffer capacity before inert-memory encoding.
Only exact length, complete fill, and one-time fingerprint finalization create
opaque `EncodedAcmeRequestImage`; partial bytes/digest state have no authority.
The encoder cannot target storage or transport. Durable publication consumes
the completed value atomically, or uses a sealed begin/write/commit/abort sink
whose bytes are invisible before commit and which network adapters cannot
implement. Recovery recomputes URL parts, origin, header admission, length, and
fingerprint. HTTP/1.1 formatting, HTTP/2/3 frames, HPACK/QPACK state, stream IDs,
frame boundaries, TLS records, and QUIC packets remain executor-local.
`EffectDispatchPermit<AcmeSend>` binds the selected HTTP profile,
adapter/session, policy snapshot, and final request fingerprint. Middleware may
frame but cannot inject or override method, target, metadata, or body after
authority composition.

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
- `PeerConfirmed` accepts only an authenticated exact CA or DNS peer result
  produced by the narrow bootstrap and durable peer-effect boundary below.
- `CryptographicallyAttested` verifies a genuine signed/native receipt over
  the complete binding transcript and freshness.
- `ProviderAsserted` is only an opaque provider claim and is rejected by
  default.
- `Unverified` never permits activation.

The quarantine/bootstrap cycle is broken only by a private non-serializable
single-use `SecretBindingAttempt`, constructed from mutable state of the exact
quarantined onboarding transaction. It pins the provider/session, immutable
secret identity/version, tenant, directory or zone, peer, external-account or
TSIG identity, algorithm, purpose, policy, fresh transcript, onboarding
request, mode, and stable attempt identity. Its local form can MAC only the
domain-separated binding transcript. Its peer form can populate only the exact
typed confirmation-effect envelope chosen for that onboarding request. It
cannot create ordinary `BoundMacKey` or `MacConsumerAdmission`, MAC arbitrary
bytes, or service unrelated EAB/TSIG traffic. It is consumed before immutable
provider dispatch and is never cloned, serialized, restored, or reused.

Peer confirmation is an external effect, not necessarily a harmless check.
Every typed peer effect has a stable effect identity and sealed
`PeerEffectFingerprint<Protocol, Revision>`,
peer/security profile, mutation class, reconciliation key, authenticated
success/rejection evidence contract, and affected account or DNS resource.
Outcomes are the product `DispatchKnowledge × OperationOutcome ×
BindingEvidence × ObservationStatus`, not an interchangeable flat enum.
Dispatch knowledge preserves not-started, positively definitely-unsent,
committed-but-not-dispatched, may-have-dispatched, and positively dispatched
facts. Operation success/rejection is independent from purpose-specific peer
confirmation/content mismatch, and observation or reconciler unavailability
cannot erase either axis. Only authenticated request-bound, purpose-specific
peer evidence proves success, rejection, binding, or mismatch;
unauthenticated errors do not. A rate limit, contact/ToS rejection,
`badNonce`, or DNS `REFUSED` changes only the axes it proves. Any
sent-or-maybe-sent request without conclusive evidence is ambiguous and is
never blindly retried.
EAB account creation may jointly establish peer binding and durable account
state. TSIG prefers an authenticated non-mutating probe; a mutating DNS UPDATE
must carry ownership, rollback/cleanup, duplicate, and reconciliation rules.

The recovery boundary is exact:

| Boundary | Permitted recovery |
| --- | --- |
| Before provider MAC dispatch | Close with positive unsent evidence and mint a wholly new attempt. |
| MAC consumed, no outbox envelope | Prove peer dispatch was impossible, discard transient artifacts, and start fresh. |
| Exact envelope committed, dispatch not started | Send only the committed bytes; never rebuild or re-sign. |
| Dispatch started or may have started | Preserve ambiguity and reconcile; never resend blindly. |
| Authenticated `badNonce` | Record operation rejection without secret mismatch and rebuild the complete EAB attempt with fresh identities. |
| Authenticated account success | Commit account, peer binding, and obligations before disposition. |

Positive definitely-unsent evidence authorizes creation of a new capability,
never restoration or reuse of the consumed one.

EAB account creation composes both authentication layers in one consumed
typestate rather than collecting independent evidence:

```text
EabAccountCreationAttempt

Prepared
  -> InnerMacVerified
  -> OuterSignatureVerified
  -> OutboxCommitted
  -> Dispatched
  -> Reconciled
```

Every state binds the canonical account intent, contacts, ToS agreement,
directory and exact `newAccount` URL, account JWK and immutable signer/session,
EAB key ID and immutable secret version, algorithms, complete inner JWS,
outer nonce/signing input/admission, bootstrap/account/outbox identities,
canonical `AcmeRequestImage`, and `FinalRequestFingerprint`. Positive purpose-
matching MAC evidence alone advances the inner state; `VerifiedSignature` over
the exact complete outer input alone advances the outer state. The peer effect
cannot execute before that outer request is locally verified and durably
committed. Evidence, inner JWS values,
nonces, identities, and states cannot cross attempts. Authenticated `badNonce`
consumes the complete attempt and rebuilds both layers with fresh identities;
it does not prove an EAB-secret mismatch.

Durable execution commits the binding-attempt intent before privileged
provider MAC dispatch and commits the exact peer-effect envelope to the outbox
before network dispatch. Account/DNS mutation, binding evidence, lifecycle
activation, source retention/destruction, and obligations use explicit fenced
ordering. Source material cannot be destroyed before the remote result is
durably resolved and binding/account or DNS state is committed.

Durable active eligibility and historical binding receipts are not MAC
authority. Every process/provider session freshly resolves the current
immutable object and, for reusable secrets, performs a safe non-mutating local
comparison, current admitted attestation/assertion, or authenticated
non-mutating peer probe before constructing `BoundMacKey`. Restart never
automatically repeats mutating EAB account creation or DNS UPDATE. A
mutating-only peer profile requires explicit reconciliation/operator policy.
One-time EAB material proceeds to disposition after durable account success
and is not reconstructed.

Snapshots may retain lifecycle state, obligations, binding-mode/profile
identifiers, redacted receipt digests, and durable peer-effect/reconciliation
facts. They never contain or restore `SecretBindingAttempt`, `BoundMacKey`,
`MacConsumerAdmission`, live `EabAccountCreationAttempt` typestates,
`VerifiedMac`, `ProviderAssertedMac`, `CryptographicallyAttestedMac`, or any
other MAC effect capability. Restart, provider/session/policy/health change,
object restore/recreation, alias/version retargeting, peer-trust change, or assurance
profile change requires fresh reconstruction; unavailable reconstruction
leaves the secret eligible but unusable.

## Restore Discontinuity

A whole-store rollback is not an ordinary restart. Stores publish exactly
`RollbackProtected`, `RollbackDetecting { maximum_window }`, or
`RollbackUnprotected` and bind durable state to a `StoreEpoch`/`RecoveryEpoch`.
The first prevents or detects rollback for every protected committed effect;
the second detects only rollback crossing the last witnessed head and exposes
its maximum unwitnessed window; the third makes no automatic claim. A detected
change or explicit
operator `RestoreDeclared` input invalidates leases, fences, provider sessions,
caches, and live authority; quarantines restored outbox work, key eligibility,
challenge ownership, deployment generations, and retirement state; and requires
operation-specific reconciliation plus trust/signer/secret/deployment
revalidation. Without monotonic secure storage, automatic detection is typed
unsupported and operators must declare restoration.

Automatic detection requires an authenticated `RollbackWitness` outside the
store failure domain. Its trust root, bootstrap identity, and replacement
authority also live outside the restored store. The witness binds its
implementation/identity/session,
store identity and state-head digest to a monotonic counter or authenticated
journal. Its protocol models store-before-witness and witness-before-store
crashes, bounded batching windows, loss/reset/clone/rollback/split-brain,
partitions, and key rotation. High-assurance startup refuses
`RollbackUnprotected`; operator-declared restore starts recovery but cannot
protect against unnoticed rollback.

Each witness/store profile publishes a closed `RollbackCoverage` manifest that
binds the authenticated state-head construction to exact store namespaces,
record classes, effect types, tenant/partition scope, and schema version.
Protected/detecting assurance applies only when every dependency of an operation
is covered. Unknown, omitted, dynamically added, or excluded data is
`RollbackUnprotected`; it cannot inherit an aggregate store label. Changing the
coverage creates a new authenticated profile identity and requires recovery
review before authority can be reconstructed.

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

Every profile consumes the same committed `AcmeRequestImage`. HPACK/QPACK
tables, stream identity/segmentation, connection restart, TLS record layout, and
QUIC packetization cannot change `FinalRequestFingerprint`; a new connection
can frame the stored application image without rebuilding or re-signing it.
The transport returns `ObservedEffectiveUrl`, which is checked against the
immutable `SignedRequestTarget` without becoming request authority.

## No-Heap Validation Workspaces

The strict `no_std` tier accepts caller-provided storage for PKIX path
candidates, RFC 5280 policy trees, OCSP/CRL extensions and entries, SCT lists,
CT v2 `TransItem` collections, DNSSEC RRsets/chains, and NSEC/NSEC3 proofs.
Exhaustion is deterministic and typed. Optional `alloc` wrappers own these
workspaces without changing validation rules or capacity accounting.

`no_alloc` is an executable property, not a feature-name claim. Nominal paths
link without a global allocator, run under allocation traps where host harnesses
are needed, publish peak-stack evidence bound to exact target, compiler,
optimization profile, feature set, and linker plus scratch-exhaustion evidence,
and specify
`Send`/`Sync`, pinning, callback reentrancy, effect ownership, and caller-buffer
lifetime/aliasing. An allocation-backed object-safe executor is a separate
explicit tier.

## Native Secret Memory

Portable secret types promise redaction and explicit ownership, not universal
erasure. An optional outward native `SecretMemory` boundary may add page
locking, dump exclusion, guarded allocation, swap policy, copy/provenance
tracking, restricted export, and best-effort zeroization. It publishes the
exact operating-system primitives, privileges, configuration, and residual
copies it can cover. Missing support is typed unsupported and never falls back
while retaining a stronger assurance label.

## Challenge Identity Layers

Challenge evidence keeps three identities distinct: the IANA method token such
as `dns-01`, the exact RFC or draft specification revision implementing that
token, and Vardheim's internal evidence/schema revision. A future `dns-02` is a
new method token in the DNS family crate, not revision two of `dns-01`.
Compatibility or migration between specification/schema identities is explicit;
receipts never convert merely because they share a family crate.

## Security Invariants

- A replay nonce is linear authority, not a confidential secret: it is consumed
  exactly once, never cloned/restored, and never returned to a pool. A parsed
  response nonce is only an observation until authenticated TLS/origin,
  effective URL, strict framing, admitted ACME operation, grammar, directory
  context, and local duplicate/non-reuse checks within the bounded queue and
  consumed-ID window are validated; the client makes no global server-
  uniqueness claim, and authenticated `badNonce` reserves its nonce for that
  complete rebuilt retry.
- Security-sensitive internal identities are domain-separated and durably
  allocated before use; caller idempotency strings, fork/clone state, or a
  rolled-back counter cannot join unrelated evidence, outbox, admission, or
  reconciliation state.
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
  request; assertions and attestations remain distinct from
  `VerifiedSignature`, assurance axes cannot be collapsed or upgraded, remote
  self-verification is insufficient, FIPS boundary identity is preserved, and
  unavailable required verification fails closed without fallback.
- Cached, unrelated, cross-protocol, ambiguous, expired, replayed, or
  incompletely bound native signatures cannot prove a signer handle is bound.
- Signer success, failure, cancellation, ambiguity, `badNonce`, and ambiguous
  network transmission never restore or reuse a consumed request admission.
- EAB account creation cannot stitch inner MAC evidence, outer signature
  evidence, a nonce, signer session, JWK, account intent, directory, or effect
  identity from different attempts; every typestate transition consumes its
  predecessor and only exact verified outer bytes may enter the outbox.
- Peer-effect dispatch knowledge, operation outcome, binding evidence, and
  observation availability are orthogonal; operation rejection or observer
  unavailability cannot fabricate secret mismatch or definitely-unsent proof.
- A committed EAB envelope is dispatched byte-for-byte without rebuilding; a
  may-have-dispatched envelope reconciles without blind resend, while positive
  definitely-unsent evidence permits only an entirely new attempt.
- Invalidation before dispatch blocks signing; a racing or post-dispatch
  invalidation stays ambiguous without positive provider evidence and requires
  an entirely new validated/bound/request-admitted attempt.
- An imported account cannot become active without fresh signer-proven CA
  ownership evidence bound to the exact directory and account URL.
- Verification capabilities cannot be serialized, replayed across contexts, or
  restored after restart as current proof.
- A generic executor never crosses the process boundary or serializes live
  authority; a purpose-specific remote endpoint returns observations, publishes
  exact protocol capabilities, and cannot construct local qualified evidence.
- External dispatch requires a fresh current-policy `EffectDispatchPermit`;
  it composes with matching request state, purpose fingerprint, and authority
  over the same effect,
  and historical policy facts, stale workers, independently mixable tokens, or
  observed success cannot bypass current activation/deployment policy.
- Rollback detection cannot be inferred from an epoch stored only inside the
  rollback domain; high assurance requires externally rooted witness evidence
  whose exact maximum detection window and namespace/effect coverage are
  published.
- Portable secret ownership/zeroization and optional native memory controls do
  not imply universal erasure or protection from privileged software.
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
