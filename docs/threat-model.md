# Threat Model

## Protected Assets

Account keys, certificate subject keys, EAB secrets, challenge material,
authorization state, DNS credentials, deployment credentials, certificate
intent, audit records, and operator policy are protected assets.

## Adversaries

Vardheim assumes hostile or compromised networks, malformed or malicious ACME
responses, malicious directory metadata, compromised challenge infrastructure,
crash/restart races, stale distributed workers, supply-chain compromise, and
accidental operator misconfiguration. A configured CA is trusted to issue but
its returned bytes are still structurally and semantically verified.

## Primary Risks

- SSRF or cross-origin credential leakage through directory-controlled URLs;
- ambient/ACME credential leakage, HTTP framing/decompression attacks, partial
  object acceptance, privacy leakage, or cross-context cache poisoning through
  public-PKI URLs;
- issued-certificate trust confused with ACME TLS/platform/CT/DNSSEC trust or
  silently emptied during reload;
- account takeover through an operator-supplied or cross-directory account URL
  without proof that the configured signer controls the CA account;
- loss of account control or evidence through premature old/new key disposition
  after ambiguous rollover or deactivation;
- JOSE algorithm confusion, nonce reuse, malformed nested JWS, or admitting a
  nonce from unauthenticated/wrong-origin/redirected/framing-invalid/unrelated
  responses; including losing the authenticated `badNonce` retry reservation
  or overclaiming global server nonce uniqueness from a bounded local window;
- collision or reuse of durable effect/attempt/reconciliation/provider-
  idempotency identities after entropy failure, counter exhaustion, process
  fork, VM clone, database restore, recovery-epoch change, multi-node race, or
  use before durable allocation; persistence of transient admission/session
  identity; or observational correlation and caller idempotency input being
  upgraded into authority;
- a transient local request identity entering an outbox or external operation;
  one durable protocol request identity naming different bytes; request/effect
  substitution; or identity reuse after `badNonce`, cancellation, restore, or
  policy-driven rebuild;
- signer dispatch before exact signing-input binding; unverified or partially
  bound request identity entering the outbox/transport; canonical application
  request fields diverging from the locally verified signature/input; physical
  HTTP/1.1, HTTP/2/3, TLS, or QUIC framing being mistaken for request authority;
  middleware mutating method, target, admitted headers, or body after image
  composition; crash recovery silently re-signing, advancing, or rebinding an
  old reservation instead of tombstoning it and creating a wholly new retry;
  or skipping/restoring a request typestate;
- resource exhaustion through JSON, PEM, DER, headers, DNS, or error nesting;
- parser/path confusion from noncanonical DER, illegal certificate-version
  fields, duplicate extensions, signature-algorithm mismatch, or structural
  constraints deferred until path validation;
- invalid or substituted RSA/EC/EdDSA public material accepted because parsing,
  signature verification, or a provider handle was mistaken for current
  provider-bound key validation and exact-role signer-consumer admission;
- account, rollover, CSR, certificate-key revocation, TLS-ALPN, or a future
  handle-backed signing effect accepting cached, unrelated, cross-protocol,
  replayed, expired, ambiguously produced, or incompletely bound native
  signatures instead of fresh exact-role signer-consumer admission;
- a mutable alias, label, name, persistent reference, or remote mapping being
  retargeted after binding but before signature dispatch; or provider-returned
  wrong-key, malformed, incorrectly encoded, or unverified signature bytes
  entering a protocol effect because local verification was optional,
  unavailable, or silently replaced by another backend;
- collapsing signature-verifier locality, trust-domain relationship,
  implementation relationship, validated-module identity, or key/input binding
  into one assurance rank; collapsing exact verification, assertion, and
  attestation into one evidence type; rejecting safe same-
  implementation local verification, promoting provider assertion/attestation
  into `VerifiedSignature`, admitting remote self-verification, or moving
  required verification outside an exact FIPS boundary;
- an EAB or TSIG secret alias/version being retargeted after discovery; a valid
  MAC from another tenant, directory, external account, zone, secret version,
  purpose, or TSIG chain entering a protocol object; raw `UnverifiedMac` being
  accepted; ordinary provider assertion being labeled cryptographic attestation
  or inflated into independent verification;
  or failure, cancellation, ambiguity, session change, or verifier
  unavailability restoring MAC admission, exporting the secret, or selecting a
  fallback provider;
- a generated, imported, or adopted symmetric provider object becoming usable
  before its content is bound to the intended EAB/TSIG secret; wrong-secret or
  cross-directory/zone import after a lost/duplicate operation; forged/replayed
  local, peer, assertion, or attestation binding evidence; source-secret
  destruction before durable binding; restored provider objects or snapshots
  recreating MAC authority; or a lifecycle failure dropping reconciliation,
  revalidation, source-destruction, disposition, or operator obligations;
- breaking secret-binding quarantine by granting ordinary MAC authority to a
  bootstrap ceremony; a binding attempt accepting arbitrary bytes, another
  onboarding request, peer, account, zone, secret version, or protocol purpose;
  treating EAB account creation or TSIG DNS UPDATE as a harmless check;
  unauthenticated peer errors proving rejection; lost success being blindly
  retried; ambiguous DNS ownership or rollback; source destruction before
  durable reconciliation; or restart automatically repeating a mutating peer
  ceremony or reconstructing live authority from historical confirmation;
- stitching an EAB MAC from one bootstrap/secret/account intent to another
  account JWK, directory, contacts/ToS payload, nonce, signer session, request,
  outbox effect, or outer JWS; executing before both inner MAC and outer
  signature have exact positive evidence and durable commit; rebuilding signed
  bytes after outbox commit; combining old MAC evidence with a fresh nonce;
  restoring a partial typestate after crash; or applying account success more
  than once;
- flattening dispatch knowledge, account/DNS operation outcome, secret-binding
  evidence, and observer availability so `badNonce`, rate/contact/ToS rejection,
  DNS `REFUSED`, or reconciliation outage fabricates secret mismatch,
  definitely-unsent proof, retry permission, or loss of may-have-dispatched
  state;
- generated, imported, migrated, or adopted keys becoming active before
  reconciliation, public-key validation, and signer binding; duplicate keys
  after lost responses or restart; or cleanup/lookup ambiguity being treated
  as deletion or destruction;
- persisted lifecycle state, `Active` eligibility, or validation/binding audit
  history being deserialized or upgraded into live signer authority; provider
  session rotation, KMS alias/version retargeting, or HSM object recreation
  leaving stale authority valid; or a generic failure state dropping
  reconciliation, revalidation, disposition, or operator-decision obligations;
- recursive signer admission, arbitrary-byte abuse of the privileged binding
  operation, per-request remote proof costs that make secure HSM/KMS or
  user-presence deployment impractical, or restoration/reuse of admission
  after signing failure, cancellation, ambiguity, `badNonce`, or reconciliation;
- signer invalidation racing with dispatch being classified as definitely
  failed and retried under the old request identity without positive provider
  evidence;
- policy, trust, or provider configuration changing after effect commit but
  before dispatch while a stale worker sends without a current single-use
  permit; or an observed success being activated/deployed despite current
  policy, rebuilt in place, or treated as proof that old policy remains valid;
- raw/partial/noncanonical configuration being hashed as policy authority;
  defaults, inheritance, trust/provider capabilities, or unsupported decisions
  omitted from the snapshot; or independently valid admission, commit,
  presentation, deployment, cleanup, fence, and dispatch-permit tokens stitched
  across different effects;
- policy schema/canonicalization or digest-algorithm changes retaining an old
  snapshot identity; a generic digest relabeled across wire, store, challenge,
  deployment, or cleanup effects; semantic fingerprint use where exact wire
  bytes exist; or omission of domain/schema/hash/normalized fields/purpose from
  a non-wire fingerprint;
- issuance for an unintended identifier or with an unintended key;
- leaked challenge, DNS, EAB, HSM, proxy, or deployment credentials;
- duplicate orders or deployments after ambiguous network outcomes;
- duplicated ACME mutations through TLS/QUIC early data, hidden middleware
  retry, incorrect HTTP/2/HTTP/3 reset/GOAWAY classification, connection
  coalescing, or cross-directory session/resolver reuse;
- one canonical ACME request image changing identity across HTTP profiles,
  compression tables, stream/frame boundaries, connection restart, TLS record
  layout, or QUIC packetization; or executor-local framing observations
  acquiring authority to rebuild signed application content;
- stale workers activating data after losing a lease;
- whole-store rollback resurrecting may-have-dispatched outbox work, old
  leases/fences, retired key eligibility, superseded challenge cleanup
  ownership, deployment generations, trust state, or live authority without a
  recovery-epoch discontinuity and complete reconciliation/revalidation;
- relying on an epoch stored inside the rolled-back database; external rollback
  witness commit skew, loss, reset, clone, rollback, split-brain, state-head or
  store-identity substitution, restored witness configuration/bootstrap trust,
  key-rotation failure, rollback inside an unpublished detection window, or
  silently starting a high-assurance profile without witness evidence;
- a witness profile overclaiming store-wide protection while omitting a
  namespace, record dependency, effect type, tenant partition, or schema
  version from its authenticated state head; or new/unknown data inheriting an
  old coverage claim;
- serializing transient authority through a generic remote executor, or a
  purpose-specific remote endpoint replaying, reordering, duplicating,
  downgrading, cross-session substituting, or falsely acknowledging an effect
  and then minting local qualified evidence; or a fixed third-party API being
  credited with authenticating local effect, policy, deadline, generation, or
  recovery fields its real protocol never carried;
- server-injected private keys or mismatched certificate chains;
- stale/replayed verification records, forged or cross-version status/CT
  evidence, forged STH/inclusion/consistency or witness evidence, CT split view,
  incomplete OCSP chain coverage, or false DNSSEC security from an
  unauthenticated resolver/AD bit;
- certificate/path errors from locale-dependent, lossy, non-profile ASN.1 time
  parsing or display-string/incorrect Unicode distinguished-name comparison;
- DNS spoofing through predictable/reused IDs or source ports, incomplete tuple
  binding, TCP framing/correlation errors, Cookie downgrade, EDNS/fragmentation
  fallback, forged referral/glue/AA/SOA/DNAME authority discovery, ambient
  resolver fallback, or unauthenticated RFC 2136 update responses;
- provider capability overclaim caused by inferring purpose support from a
  shared algorithm name, accepting stale/cross-session public-key validation
  evidence, silently falling back when validation is unavailable, or platform-
  trust overclaim after constraint loss; including an opaque MAC provider
  claiming independent verification or cryptographic attestation without a
  separate admitted verifier or genuine full-transcript signed/native receipt;
- false key destruction claims caused by confusing disablement, scheduled
  deletion, object absence, handle loss, unlink, zeroization, retention, or
  provider unavailability with evidenced physical destruction;
- activation or continued service of a Must-Staple certificate with a missing,
  stale, mismatched, or separately committed OCSP staple;
- dependency, CI action, toolchain, or release-process compromise.
- secret-memory overclaim from assuming overwrite-on-drop, page locking, dump
  exclusion, swap policy, guarded allocation, or copy tracking provides
  universal erasure or protection from a compromised kernel/hypervisor.

## Out Of Scope

Vardheim cannot make a compromised operating system, CA, HSM, DNS provider,
deployment target, or caller-supplied adapter trustworthy. Configured backend
implementations are part of the trusted computing base: typed requests,
bounded observations, evidence constructors, and self-verification reduce
accidental misuse but cannot force deliberately malicious code to report
truthfully or independently prove physical durability/external publication.
Every assertion-to-qualified-evidence promotion names that residual trust.
FIPS claims depend on a validated module and deployment profile,
not on a Cargo feature name. Availability against an unbounded adversary is not
guaranteed.

## Availability And Panic Policy

Vardheim libraries return typed errors for expected input, protocol, resource,
and operational failures and do not use panic catching as a recovery boundary.
Published libraries do not prescribe an application's panic strategy: the
final binary, target, and operator choose unwind or abort behavior and any
supervision policy. Security-sensitive arithmetic must use checked operations;
release-profile overflow checks are defense in depth, not the primary control.
Adapter failures are classified structurally rather than by diagnostic text;
unavailability cannot erase may-have-dispatched knowledge or create authority.
Provider diagnostics remain bounded and redacted, and operators must treat
native/FFI adapters as separately inventoried trusted-computing-base members.
