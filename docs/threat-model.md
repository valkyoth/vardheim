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
- JOSE algorithm confusion, nonce reuse, or malformed nested JWS;
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
- issuance for an unintended identifier or with an unintended key;
- leaked challenge, DNS, EAB, HSM, proxy, or deployment credentials;
- duplicate orders or deployments after ambiguous network outcomes;
- duplicated ACME mutations through TLS/QUIC early data, hidden middleware
  retry, incorrect HTTP/2/HTTP/3 reset/GOAWAY classification, connection
  coalescing, or cross-directory session/resolver reuse;
- stale workers activating data after losing a lease;
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

## Out Of Scope

Vardheim cannot make a compromised operating system, CA, HSM, DNS provider,
deployment target, or caller-supplied adapter trustworthy. Configured backend
implementations are part of the trusted computing base: typed requests,
bounded observations, evidence constructors, and self-verification reduce
accidental misuse but cannot force deliberately malicious code to report
truthfully. FIPS claims depend on a validated module and deployment profile,
not on a Cargo feature name. Availability against an unbounded adversary is not
guaranteed.

## Availability And Panic Policy

Vardheim libraries return typed errors for expected input, protocol, resource,
and operational failures and do not use panic catching as a recovery boundary.
Published libraries do not prescribe an application's panic strategy: the
final binary, target, and operator choose unwind or abort behavior and any
supervision policy. Security-sensitive arithmetic must use checked operations;
release-profile overflow checks are defense in depth, not the primary control.
