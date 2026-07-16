# ACME Completeness Contract

Status: planning audit, 2026-07-12

Completeness claims are preserved across releases through the immutable
evidence and replay rules in [the regression strategy](REGRESSION_STRATEGY.md).

Vardheim may call itself a complete ACME client at `1.0.0` only when this
contract and the release plan are fully satisfied. “100%” means complete
client-side implementation of the published ACME standards and declared
profiles; it does not mean implementing an ACME server, predicting future
standards, or overriding a CA's product restrictions.

## Normative Scope

The published-family baseline is the thirteen RFCs listed by the
[IETF ACME working group](https://datatracker.ietf.org/group/acme/documents/):
RFC 8555, 8657, 8737, 8738, 8739, 8823, 9115, 9444, 9447, 9448, 9773, 9799,
and 9891. RFC 9891 is Experimental, so Vardheim must implement and label it
accurately rather than presenting it as a Proposed Standard.

The implementation must also track every field/value in the
[IANA ACME registries](https://www.iana.org/assignments/acme/acme.xhtml),
including account/order/authorization fields, errors, resources, directory
metadata, identifiers, validation methods, STAR fields, authority-token types,
and ARI fields. Registry recognition is separate from semantic support: an
unknown or not-yet-implemented value is retained within bounds and returns a
typed capability result.

The reviewed current assignments, HTTP successor mapping, supporting RFCs,
and mutable profile revisions are pinned in the
[registry baseline](REGISTRY_BASELINE.md).

## Draft Scope

The official snapshot contains active work for profiles, persistent DNS,
DNS account labels, authority-token JWT constraints, RATS, device attestation,
and device enrollment integrations. Selected related work covers quantum-ready
TLS/JWS profiles, post-quantum agility, public-key challenges, and
identity-controlled validation. Each is assigned independently in `0.100.0`
through `0.111.0`.

Drafts are revisioned, disabled by default, and never counted toward stable RFC
conformance. Expired/replaced drafts are recorded but not implemented unless a
real interoperability requirement justifies a separately versioned revival.
If a draft becomes an RFC before its milestone, the roadmap must move it into
the published phase and rerun the standards/security review.

## Complete Client Capabilities

At `1.0.0`, all of these must work without placeholder success paths:

- strict directory discovery, refresh, origin policy, ToS changes, complete
  `newNonce` acquisition/harvesting, and directory-scoped nonce ownership;
- account create/recover/update/orders/rollover/deactivate and EAB;
- order, optional `newAuthz` pre-authorization, authorization, challenge,
  polling, finalization, retrieval, alternate chains, revocation, and
  structured problems;
- HTTP, DNS, TLS, IP, email, authority-token, onion, DTN, and external-profile
  identifier/challenge families assigned by published standards;
- ARI and conservative fallback renewal scheduling;
- key/CSR generation or external/HSM/KMS signing without private-key export;
- provider-neutral digest/sign/verify/entropy/key-generation contracts and
  explicit concrete-provider construction;
- bounded certificate parsing, CSR/key/SAN/profile binding, PKIX path policy,
  optional OCSP/CRL/CT acquisition and evidence policy, and server private-key
  injection refusal;
- existing-certificate/key/chain adoption, renewal bootstrap, issuer/account
  association, and managed/replacement-required/unmanaged classification;
- multi-issuer isolation and migration without silent CA failover or
  cross-directory credential/nonce reuse;
- account-key and certificate-key compromise response, emergency replacement,
  safe revocation ordering, and honest lost-key failure modes;
- durable workflow snapshots, transactional outbox, reconciliation, leases,
  fencing, cleanup, deployment activation, health verification, and rollback;
- async, blocking, embedded/custom transports and explicit crypto/TLS backends;
- bounded provider-neutral transport and DNS-query interfaces before concrete
  integrations;
- memory/filesystem/SQLite/PostgreSQL storage and local/remote deployment;
- manual, library, CLI, daemon, agent, and web-server integration surfaces;
- redacted observability, audit evidence, target compatibility, formal methods,
  fuzzing, security audits, and reviewed-implementation-bound pentests.

## Web-Server Acceptance Contract

A production web server must be able to use Vardheim without reimplementing
ACME protocol logic. The `0.71.1` acceptance fixture must prove:

1. map vhost/domain policy into a normalized certificate intent;
2. import or create an account and preserve an existing client migration path;
3. load EAB secrets through a redacted provider and destroy them after durable
   account creation according to policy;
4. serve HTTP-01 through an in-memory/distributed route store;
5. present TLS-ALPN-01 through the live TLS resolver without disturbing normal
   SNI traffic, or select DNS-01 for wildcards/policy;
6. survive process restart after every issuance transition;
7. validate the returned key, SANs, profile, validity, and chain;
8. atomically activate certificate/key generations, request live reload,
   health-check the serving endpoint, and roll back on failure;
9. calculate due renewals through ARI/fallback, renew one/all targets, expose
   status, rollover accounts, and revoke certificates;
10. keep existing certificates serving during failed first issuance/renewal;
11. emit bounded redacted pending/renewed/failed/reload outcomes;
12. support a fail-closed AWS-LC FIPS profile where every ACME cryptographic
    operation is inside the documented validated boundary.

The concrete fixture targets Fluxheim's current account, EAB, HTTP-01,
TLS-ALPN-01, renewal queue, atomic installation, revocation, live reload, and
metrics needs while keeping the Vardheim APIs generic for other servers.

## Honest Limitations

No static plan can permanently guarantee “all ACME” because IANA registries,
drafts, CA behavior, cryptographic modules, and platform APIs evolve. Vardheim
therefore guarantees a checked snapshot plus bounded extension handling and an
upstream-monitoring obligation. A new published RFC or registered value blocks
a subsequent conformance claim until it is classified and versioned.

A CA can still refuse an operation or product. FIPS is a property of an exact
validated module and deployment configuration. Certificate Transparency and
revocation-status availability depend on external ecosystems. These conditions
must produce precise capability/evidence results rather than inflated support
claims.

## Audit Result

The 2026-07-12 plan audit found and corrected these weaknesses:

- overloaded JSON, type, PKIX, workflow, persistence, deployment, operations,
  platform, formal-assurance, and qualification milestones were split;
- account-key persistence/import, OCSP/CRL evidence policy, CT evidence policy,
  OpenSSL TLS challenge presentation, and web-server migration acceptance were
  added explicitly;
- full errata text, release binding, reproducible SBOM, cross-target CI,
  provider-neutral crypto/transport/DNS semantics, `newNonce`, `newAuthz`,
  dedicated PKIX packaging, OCSP/CRL/CT acquisition, certificate adoption,
  renewal bootstrap, multi-issuer migration, compromise response, feature
  powersets, and early formal/fuzz/concurrency assurance were assigned to
  tactical pre-1.0 versions;
- Pebble DNS/TLS integrations were moved after their primitives exist;
- active device-enrollment integrations and identity-controlled validation work
  received versions;
- the roadmap now enforces a tactical one-boundary-per-version size rule.

The remaining uncertainty is external rather than hidden scope: exact draft
revisions, CA staging availability, validated FIPS module coverage, and future
standards must be rechecked at their assigned milestones.
