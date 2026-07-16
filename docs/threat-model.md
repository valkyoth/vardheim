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
- JOSE algorithm confusion, nonce reuse, or malformed nested JWS;
- resource exhaustion through JSON, PEM, DER, headers, DNS, or error nesting;
- issuance for an unintended identifier or with an unintended key;
- leaked challenge, DNS, EAB, HSM, proxy, or deployment credentials;
- duplicate orders or deployments after ambiguous network outcomes;
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
  fallback, or unauthenticated RFC 2136 update responses;
- provider capability overclaim caused by inferring purpose support from a
  shared algorithm name, or platform-trust overclaim after constraint loss;
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
