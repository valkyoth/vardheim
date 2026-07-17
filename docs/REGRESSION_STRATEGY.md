# Vardheim Longitudinal Regression Strategy

Vardheim does not treat tests as disposable evidence for one release. Every
release retains enough immutable, redacted evidence for future code to prove
that earlier behavior was preserved or deliberately corrected.

## Compared Baselines

Four independent baselines are retained:

1. the normative baseline: RFCs, verified errata, IANA registries, external
   profiles, and exact draft revisions;
2. the behavioral baseline: golden vectors, adversarial corpora, model traces,
   fault schedules, normalized wire exchanges, and semantic outcomes;
3. the Vardheim release baseline: public API, feature graph, serialized state,
   migrations, configuration, CLI machine output, and support claims; and
4. the environment baseline: redacted provider observations and platform/profile
   qualification evidence.

Every evidence item has a stable ID, source or generator revision, semantic
expectation, applicability range, content hash, and first/last release metadata.
Secrets, account identifiers, private keys, tokens, and uncontrolled personal
or provider data must never enter retained evidence.

Validation, signer/secret binding, signer/MAC request-admission, signature/MAC
verification, provider assertion/attestation, and effect-authority capabilities
are not evidence artifacts and must never be serialized into a retained
snapshot. `SecretBindingAttempt`, `BoundMacKey`, `MacConsumerAdmission`,
live `EabAccountCreationAttempt` typestates, `VerifiedMac`,
`ProviderAssertedMac`, and `CryptographicallyAttestedMac` are explicitly
forbidden. A snapshot may retain lifecycle/inventory facts,
orthogonal obligation sets, redacted audit records, and the hashes/versions
needed to decide that reconstruction is required. Durable `Active` means
lifecycle eligibility, not present authority. Replay after restart or a
process, provider-session, policy, trust-anchor, status, CT-list, algorithm,
provider-capability, key-health, handle/public-key, alias/version, time, or
input change must reconstruct local authority before deployment or signing.
Audit records retain stable invalidation reasons so historical replay can
detect both changed reconstruction behavior and loss of operator-visible cause.

## Replay Rules

Normal CI is deterministic and offline. It replays every historical evidence
set that declares itself compatible with the current release. Results are
compared semantically: incidental timestamps, nonces, ordering explicitly
defined as irrelevant, and approved redactions are normalized, but security
decisions and protocol bytes that standards define as exact are not hidden.

An unexplained difference is a release blocker. Intentional changes require all
of the following in the same version:

- the requirement, defect, security finding, or upstream change that justifies
  the difference;
- a reviewed old-versus-new semantic difference report;
- a migration or compatibility decision when externally visible behavior moves;
- a new regression case preserving the defect and the corrected expectation;
- release notes and an updated support or conformance claim; and
- the normal reviewed-implementation pentest stop and finalization-diff check.

No command may automatically bless current output as the new baseline. Baseline
updates are explicit reviewed changes. Historical evidence remains retained
even after a correction so the original failure can never silently return.

## Live Drift Versus Reproducible Evidence

Scheduled live jobs check RFC/errata status, IANA registries, external profiles,
draft revisions, tool/dependency releases, and opted-in provider behavior. They
produce advisory drift reports and never modify the pinned baseline or make an
offline build depend on the network. A maintainer reviews each difference and
assigns required work to a tactical version before it can become accepted
behavior.

## Compatibility Dimensions

The release comparison gate covers:

- Rust public API and feature resolution against the latest published release;
- roadmap/requirement graph identity, prerequisite ordering, ownership,
  typed requirement-source category, evidence assignment, generated views, and
  pentest boundaries;
- external-effect observation products and assertion-to-qualified-evidence
  promotion, including adapter/session/profile/request/digest/context binding
  and residual trusted-computing-base declarations;
- security-sensitive identity issuance across entropy/counter sources, domain
  separation, collisions/exhaustion, durable ordering, fork/clone/restore and
  multi-node concurrency, with durable effect identities separated from
  no-store transient admissions/sessions and observational/caller values kept
  non-authoritative;
- local-signing versus staged durable protocol request identity, reservation,
  exact signing-input binding, verified canonical application-request-image
  binding, single-source exact URL with derived/revalidated component views and
  origin, sealed initially empty header registry/ownership projection, input-
  bound consumption into local verification, inert encoding into private unsplit
  finalized ID/image aggregate, encode-failure abandonment, malicious sink/
  partial-digest refusal, stable publication transaction/record/fence identity,
  adapter-entry consumption into `PublicationAttempt`, public store assertions,
  sealed present-record commit or fenced-absence qualification, orthogonal store
  commit observations, commit-unknown replacement blocking, contradiction
  quarantine, tombstone/outbox mutual exclusion, explicit adapter TCB limits,
  single-copy body, non-authority recovery recomputation, outbox-only admission,
  physical HTTP/TLS/QUIC framing independence, observed-effective-
  URL non-authority, middleware immutability, crash abandonment/tombstone only
  before publication or after positive non-commit, store-commit/dropped-response,
  second-worker record observation, wrong post-call assertion, unavailable
  reconciliation and cross-fence tombstone/publication races without old-
  identity re-sign/rebind, transient/partial-persistence rejection,
  request/effect substitution, and wholly new identity after `badNonce`,
  cancellation, restore, interruption, or rebuild;
- canonical effective-policy snapshots and exact-effect single-use dispatch
  authority composition, including policy schema/canonicalization/hash identity,
  defaults/inheritance/capability decisions, unresolved reloads, every cross-
  token substitution, multi-node stale workers,
  pre/racing/post-dispatch changes, `MayHaveDispatched`, forbidden-result
  activation, and fresh-work rebuilding;
- sealed signing-input/final-request/peer-effect/store-mutation/presentation/
  deployment/cleanup fingerprints, canonical-image enforcement, complete
  semantic canonicalization, schema/hash/domain separation, and cross-family/
  cross-purpose non-conversion;
- normalized ACME wire behavior and typed error/security decisions;
- existing-account adoption ownership, URL/directory binding, provenance, and
  conflicting-local-account decisions;
- account-rollover/deactivation key-control proof and disposition decisions,
  including ambiguity, legal hold, and provider reconciliation;
- normalized DNS/EDNS/source-port/TCP/Cookie/RFC 2136/TSIG behavior and
  authenticated update outcomes, plus authoritative/referral/zone-cut/SOA/
  glue/CNAME/DNAME/nameserver-address discovery decisions;
- distinct CT v1/v2 parsing, log-list, precertificate, signature, and policy
  decisions with no cross-version evidence conversion, plus STH/Merkle/MMD/
  checkpoint/witness split-view decisions;
- strict ASN.1/PKIX time and distinguished-name equality decisions across
  certificate, CRL, OCSP, and CMS/CT inputs;
- DER primitive canonicality, certificate-envelope structural rejection, and
  durable certificate renewal key-rotation decisions;
- provider/session-bound RSA/EC/EdDSA public-key validation, JWK/SPKI/algorithm
  consistency, domain-separated `BoundSigner` transcripts, narrow binding-
  operation exemption, native pairwise-consistency equivalence, locally minted
  exact-request admission, bounded concurrent identities, destructive
  consumption across signer/network/retry outcomes, pre/in/post-dispatch
  invalidation classification and positive-provider-evidence requirements,
  immutable provider-native identity/version and public-key-digest pinning,
  mutable-locator replacement at every binding/admission/dispatch/verification
  barrier, untrusted returned-signature typing, mandatory local verification
  over exact admitted bytes/algorithm/parameters/encoding/bound key,
  strict separation of unverified/provider-asserted/attested/exact-verified
  signature evidence, independent locality/trust-domain/implementation/
  validated-module/key-input assurance axes on `VerifiedSignature`, valid same-
  implementation local verification, optional diversity, remote-self-
  verification refusal, FIPS-boundary preservation,
  wrong-key/malformed/verifier-unavailable outcomes, invalidation after
  provider/session/policy/key-health change, unsupported/unavailable/ambiguous
  outcomes, no signer/verifier fallback, and issued-leaf decisions;
- handle-backed EAB/TSIG immutable secret identity/version binding,
  `BoundMacKey`, exact canonical input/purpose/request/truncation/TSIG-chain
  admission, destructive consumption across success/failure/cancellation/
  ambiguity/session change, alias/version replacement at every barrier,
  `UnverifiedMac` rejection, constant-time independent `VerifiedMac`, separately
  typed provider assertion versus genuine cryptographic attestation, complete
  signed/native attestation transcript and replay validation, default weaker-
  evidence rejection,
  wrong-valid-key/malformed/truncated/verifier-unavailable outcomes, no secret
  export, no fallback, and provider capability/assurance publication;
- transactional symmetric-secret create/import/adopt request and idempotency
  identities, definitely-not-created/created/ambiguous/unavailable outcomes,
  quarantine, `SecretLifecycleState × SecretObligationSet`, local-comparison/
  authenticated-peer/cryptographic-attestation/provider-assertion/unverified
  content-binding modes, private single-use `SecretBindingAttempt` confinement,
  exact local transcript and peer-effect binding, stable attempt/effect IDs,
  non-mutating/mutating classification, orthogonal `DispatchKnowledge ×
  OperationOutcome × BindingEvidence × ObservationStatus`, authenticated
  definitely-unsent/success/rejection/binding/mismatch evidence, persist-before-
  effect ordering, EAB account/result coupling, TSIG probe preference and
  UPDATE ownership/rollback/reconciliation, source-secret retention/destruction
  ordering, wrong-secret and cross-directory/zone import, lost/duplicate
  onboarding, lost EAB success, duplicate-account and ambiguous-DNS prevention,
  unauthenticated error handling, restored/recreated provider objects, safe
  per-session binding reconstruction without automatic mutating ceremony
  replay, one-time EAB disposition, capability-free snapshots, fencing,
  cleanup/disposition ambiguity, no absence-as-destruction, no blind retry, and
  no bare-handle activation;
- composed EAB account creation across canonical intent/contacts/ToS,
  directory/URL, account JWK and immutable signer session, EAB key/secret
  version/algorithm, exact inner JWS and positive MAC evidence, outer nonce/JWS
  input/admission/`VerifiedSignature`, attempt/request/effect IDs, local-verified
  state, unsplit finalized aggregate, store assertion, and qualified commit;
  consumed `Prepared`/`InnerMacVerified`/
  `OuterSignatureVerified`/`OutboxCommitted`/`Dispatched`/`Reconciled`
  transitions; failure between every inner/outer/durable boundary; no evidence
  stitching, old-MAC/new-nonce reuse, committed-request rebuilding, blind
  may-have-dispatched resend, binding-failure inflation from operation
  rejection, capability serialization, or repeated result application; and
  full fresh assembly after authenticated `badNonce`;
- transactional generation/import/migration/platform-adoption states, stable
  request/idempotency identities, lifecycle-state/obligation-set products,
  quarantine, active-as-eligibility semantics, fresh-session authority
  reconstruction, lost-response and eventual-visibility reconciliation,
  duplicate prevention, fencing, cleanup/disposition obligations, and no
  absence-as-destruction decisions;
- OCSP responder-extension/recursion, chain-status, privacy, and tenant/cache
  decisions;
- public-PKI HTTP framing, decompression, representation, complete-body, and
  cache-partition decisions;
- ACME HTTP-version selection, early-data refusal, retry prohibition,
  connection/session/resolver partitioning, coalescing, and
  definitely-unsent-versus-ambiguous transmission decisions;
- every supported historical persisted snapshot and migration chain, including
  proof that validation/binding/admission/verification/effect capabilities are
  absent, active snapshots grant no authority, stale audit records cannot be
  upgraded, and reconstruction obligations survive;
- whole-store rollback across outbox dispatch, leases/fences, key retirement,
  challenge ownership, deployment generations and trust/provider changes,
  including exact protected/detecting-with-maximum-window/unprotected claims,
  closed namespace/record/effect/tenant-partition/schema coverage manifests,
  unknown/new dependency downgrade,
  store/recovery epochs, an externally rooted authenticated monotonic witness,
  store/witness commit skew, restored bootstrap configuration, reset/clone/
  split-brain/key rotation, operator declaration, assurance-profile startup,
  quarantine, reconciliation, revalidation, and honest unsupported detection;
- local-only generic executor behavior and each purpose-specific remote
  protocol's exact endpoint-authentication, request/context binding,
  idempotency, replay, observation, dispatch-acknowledgement, recovery,
  attestation, and reconciliation capability cells, with full controlled-agent
  profiles separated from fixed-API unsupported cells and local compensation,
  and no serialized live authority or remote construction of local evidence;
- provider observations without encoding undocumented quirks as standards;
- issued-certificate trust snapshot/reload/distrust and Must-Staple refresh/
  deployment decisions, including typed unsupported platform constraints;
- per-purpose crypto-provider capability, public-key validation/signer-binding,
  asymmetric/symmetric onboarding and reconstruction, immutable signature/MAC
  dispatch, returned-signature verification, MAC evidence/assurance, and
  legacy-key migration decisions;
- provider-native key disposition, receipt binding, and reconciliation decisions
  without destruction-state inflation;
- target/profile compile and runtime evidence;
- allocator-free link/run, panic-on-allocation, target/compiler/optimization/
  features/linker-bound peak-stack, scratch-exhaustion, pinning, reentrancy,
  lifetime/aliasing, and `Send`/`Sync` evidence for nominal `no_alloc` profiles;
- native secret-memory page-lock/dump/swap/guard/copy/zeroization evidence and
  typed unsupported behavior without universal-erasure claims;
- formal-model traces and generated adversarial cases; and
- security mutation outcomes, including permanent named tests for removed
  verification, restored nonce/admission, parser ambiguity, certificate bypass,
  ambiguous resend, cleanup weakening, evidence promotion, and fallback; and
- dependency/tool manifests, where drift is reported separately from behavior.

Before `1.0.0`, an intentional breaking change is possible only when documented
and versioned, but it is never permitted to appear as an unexplained regression.
The exact compatibility promise for `1.x` is frozen during the `0.120.0` release
candidate sequence.

## Assigned Milestones

The implementation is deliberately split across `0.3.8`, `0.3.9`, `0.4.1`,
`0.4.3`, `0.4.4`, `0.4.14`-`0.4.27`, `0.10.23`-`0.10.33`, `0.33.3`,
`0.33.4`, `0.33.5`, `0.33.6`, `0.33.7`-`0.33.9`, `0.34.3`, `0.37.4`,
`0.37.5`, `0.38.5`, `0.39.2`, `0.56.12`, `0.69.3`, `0.92.6`,
`0.96.4`, `0.97.3`, `0.119.0`, and `0.119.1` in
[the release plan](RELEASE_PLAN.md). Release binding itself is assigned to
`0.3.3`. Each boundary receives its own complete test suite and mandatory
pentest stop.
