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
- JOSE algorithm confusion, nonce reuse, or malformed nested JWS;
- resource exhaustion through JSON, PEM, DER, headers, DNS, or error nesting;
- issuance for an unintended identifier or with an unintended key;
- leaked challenge, DNS, EAB, HSM, proxy, or deployment credentials;
- duplicate orders or deployments after ambiguous network outcomes;
- stale workers activating data after losing a lease;
- server-injected private keys or mismatched certificate chains;
- dependency, CI action, toolchain, or release-process compromise.

## Out Of Scope

Vardheim cannot make a compromised operating system, CA, HSM, DNS provider, or
deployment target trustworthy. FIPS claims depend on a validated module and
deployment profile, not on a Cargo feature name. Availability against an
unbounded adversary is not guaranteed.
