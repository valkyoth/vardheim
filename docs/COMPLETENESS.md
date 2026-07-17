# ACME Completeness Contract

Status: planning audit, 2026-07-17

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
  `newNonce` acquisition/harvesting, and directory-scoped linear nonce
  authority that is distinct from secrets, cannot be cloned/restored, and
  harvests an independent response nonce before interpreting the outcome;
- account create/recover/adopt/update/orders/rollover/deactivate and EAB, with
  current validated and role-bound signers plus exact-request admission for
  every handle-backed account effect, signer-proven ownership proof for
  imported accounts, and durable old/new key disposition after rollover or
  deactivation; EAB additionally requires immutable secret-version binding,
  transactional secret onboarding/content binding, narrow quarantined
  secret-binding attempts, orthogonal dispatch/operation/binding/observation
  outcomes, a consumed composed inner-MAC/outer-signature account-creation
  typestate, durable exact-request peer-effect reconciliation, complete fresh
  assembly after `badNonce`, safe authority reconstruction without repeating
  account mutation,
  exact-input single-use MAC admission, and purpose-specific positive evidence
  with independently verified, provider-asserted, and genuinely
  cryptographically attested assurance kept distinct;
- order, optional `newAuthz` pre-authorization, authorization, challenge,
  polling, finalization, retrieval, alternate chains, revocation, and
  structured problems, with conflict-checked versioned method registration and
  sealed presentation receipts that cannot cross families or revisions;
- HTTP, DNS, TLS, IP, email, authority-token, onion, DTN, and external-profile
  identifier/challenge families assigned by published standards;
- ARI and conservative fallback renewal scheduling;
- transactional key/CSR generation, import, migration, or platform adoption
  with lifecycle-state/obligation separation, quarantine, fenced
  reconciliation, active-as-eligibility semantics, fresh per-session
  validation/binding authority reconstruction, immutable provider identity
  dispatch, mandatory local verification of returned signatures, and external/
  HSM/KMS signing without private-key export;
- provider-neutral digest/sign/verify/entropy/key-generation, public-key
  validation, domain-separated transient `BoundSigner`, locally minted
  single-use exact-request signer admission, handle-backed `BoundMacKey`,
  exact-input MAC admission, immutable signer/secret dispatch, purpose-specific
  `VerifiedMac` versus `ProviderAssertedMac` versus
  `CryptographicallyAttestedMac`, separate transactional asymmetric-key and
  symmetric-secret onboarding, typed secret-content binding, private
  single-use `SecretBindingAttempt`, orthogonal peer-effect outcome typing,
  evidence-stitching-resistant EAB composition, capability-free snapshots,
  safe signer/MAC authority reconstruction, and
  honest disposition/reconciliation contracts with explicit concrete-provider
  construction and
  per-purpose capability/validation/binding/onboarding/reconstruction/
  immutable-dispatch/signature-verification and independent-verifier-assurance/
  MAC-evidence/disposition tables,
  including narrowly purpose-bound legacy verification hashes where standards
  still require them;
- bounded strict DER primitive parsing and X.509 structural prevalidation,
  shared ASN.1/PKIX time handling and RFC 5280 DN equality, CSR/key/SAN/profile
  binding, provider/session-bound RSA/EC/EdDSA public-key validation including
  issued leaf keys plus signer-handle binding and exact-request admission,
  explicit durable renewal
  key-rotation modes, PKIX path policy, complete RFC 5280 policy processing,
  chain-wide local OCSP/CRL parsing and signature verification, distinct RFC
  6962 CT v1 and RFC 9162 CT v2 parsing/signature/Merkle verification, hardened
  credential-free optional acquisition/AIA, context-bound transient evidence,
  and server private-key injection refusal;
- distinct versioned issued-certificate trust providers for custom/platform
  anchors, additions/removals/distrust, constraints, tenant isolation, and
  reload failure without reusing ACME HTTPS/CT/DNSSEC trust;
- existing-certificate/key/chain adoption, renewal bootstrap, issuer/account
  association, and managed/replacement-required/unmanaged classification;
- multi-issuer isolation and migration without silent CA failover or
  cross-directory credential/nonce reuse;
- account-key and certificate-key compromise response, emergency replacement,
  safe revocation ordering, and honest lost-key failure modes;
- certificate supersession/retirement/revocation/destruction, deployment
  removal acknowledgement, honest provider-native disposition reconciliation,
  overlap policy, inventory reconciliation/export, orphan handling, high-level
  lifecycle APIs, and post-deployment status-driven replacement;
- durable workflow snapshots, transactional outbox, reconciliation, leases,
  fencing, cleanup, deployment activation, health verification, rollback, and
  mandatory reconstruction rather than restored validation, signer-binding,
  admission, verification, or effect-authority capabilities;
- async, blocking, embedded/custom transports and explicit crypto/TLS backends,
  with explicit HTTP protocol versions, disabled early data, no hidden retry,
  partitioned connection/session/resolver state, and definite-versus-ambiguous
  transmission evidence;
- strict public-PKI HTTP framing, decompression/work budgets, media validation,
  complete-body enforcement, OCSP POST privacy, and tenant/purpose/policy cache
  isolation;
- bounded provider-neutral transport and DNS-query interfaces before concrete
  integrations;
- complete EDNS(0) query mechanics, fresh per-attempt transaction IDs and UDP
  source ports/socket rotations, complete tuple binding, bounded framed TCP
  correlation, optional DNS Cookies, and RFC 2136 updates authenticated with
  RFC 8945 TSIG whose request, response, and chain MACs use immutable secret
  identity/version dispatch and exact positive evidence;
- complete authoritative DNS discovery across zone cuts, referrals, AA/SOA
  semantics, glue, nameserver A/AAAA resolution, CNAME/DNAME synthesis, lame
  delegations, and unreachable authorities without ambient system resolution;
- complete local DNSSEC validation including canonical RRsets, DNSKEY/DS/RRSIG,
  chain/time policy, NSEC/NSEC3 denial, trust-anchor rollover, and explicit
  authenticated-resolver evidence policy;
- optional RFC 7633 TLS Feature/Must-Staple verification, fresh OCSP activation
  gating, atomic certificate/key/staple generations, and durable refresh;
- durable CT v1/v2 inclusion and append-only consistency monitoring after MMD,
  log lifecycle/outage policy, and optional independent witness/gossip split-
  view evidence;
- bounded optional PKCS#1/SEC1 migration import into PKCS#8/opaque lifecycles,
  with no legacy export;
- memory/filesystem/SQLite/PostgreSQL storage and local/remote deployment;
- Android Keystore, Apple Keychain/Secure Enclave, Windows CNG/certificate
  store, and optional PKCS#12 interoperability profiles;
- manual, library, CLI, daemon, agent, and web-server integration surfaces;
- redacted observability, audit evidence, target compatibility, formal methods,
  fuzzing, security audits, and reviewed-implementation-bound pentests.
- a machine-checked acyclic requirement/work/version graph with ownership,
  evidence, generated plan views, critical path, and no omitted or merged
  pre-1.0 pentest boundary.

## Web-Server Acceptance Contract

A production web server must be able to use Vardheim without reimplementing
ACME protocol logic. The `0.71.1` acceptance fixture must prove:

1. map vhost/domain policy into a normalized certificate intent;
2. import or create an account, prove imported-account ownership with its
   signer and a fresh CA retrieval, and preserve an existing client migration
   path including non-exportable keys;
3. load EAB secrets through a redacted provider and destroy them after durable
   account creation according to policy;
4. serve HTTP-01 through an in-memory/distributed route store;
5. present TLS-ALPN-01 through the live TLS resolver without disturbing normal
   SNI traffic, or select DNS-01 for wildcards/policy;
6. survive process restart after every issuance transition;
7. validate the returned key, SANs, profile, validity, and chain;
8. atomically activate certificate/key generations, request live reload,
   health-check the serving endpoint, deploy/refresh a required verified OCSP
   staple in the same fenced generation, and roll back on failure;
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

Planning audits through 2026-07-17 found and corrected these weaknesses:

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
- DER writer/reader and algorithm identifiers were moved before CSR, genuine
  test-only crypto was added before interoperability, PKIX evidence ownership
  and backend trust were made explicit, full RFC 5280 policy/AIA coverage,
  concrete clock/DNS adapters, EAB HMAC/RSA-PSS, certificate retirement and
  reconciliation, and platform key-store adapters received tactical versions;
- verification evidence was made transient and context-bound, status/CT
  parsers and local signature verification were assigned, public-PKI fetching
  was separated from authenticated ACME transport, and complete DNSSEC/NSEC3/
  trust-anchor validation, genuine early verifier coverage, production
  purpose-bound legacy/DNSSEC crypto, and no-heap workspaces received tactical
  versions;
- EDNS query mechanics, source-port/full-tuple correlation, DNS TCP framing and
  Cookies, RFC 8945 TSIG sequencing, issued-certificate trust providers,
  distinct CT v1/v2 profiles, chain-wide OCSP and acquisition privacy, hardened
  public-PKI framing/cache semantics, RFC 7633 Must-Staple deployment/refresh,
  existing-account adoption, strict ASN.1 time and DN equality, CT Merkle/
  inclusion/split-view monitoring, honest provider-wide key disposition,
  DER/X.509 structural closure, rollover/deactivation account-key disposition,
  durable renewal key modes, complete authoritative DNS discovery, explicit
  HTTP version/replay/early-data policy and HTTP/2/HTTP/3 profiles,
  provider-neutral public-key validation and signer binding across every
  software, HSM, TPM, KMS, remote, and platform provider,
  nonrecursive `BoundSigner` plus local request-admission enforcement across
  account creation/recovery/adoption, both rollover signers, internal CSR
  construction, certificate-key revocation, TLS-ALPN ephemeral signing, and
  future handle-backed effects; fresh domain-separated binding transcripts,
  native-consistency equivalence, bounded concurrency, and destructive
  admission handling across retry, invalidation races, and ambiguity; immutable
  provider identity dispatch and mandatory wrong-key/malformed-output detection
  before any protocol effect; an equivalent handle-backed MAC authority
  boundary for EAB and TSIG with immutable secret-version dispatch, exact-input
  admission, constant-time independent verification where possible, distinctly
  typed provider assertion and genuine cryptographic attestation, explicit
  weaker-assurance policy, and no secret export or fallback across software,
  HSM, KMS, secret-manager, and remote providers; transactional symmetric-
  secret onboarding/content binding, quarantine, narrow local/peer bootstrap,
  persist-before-effect account/DNS confirmation, orthogonal authenticated
  dispatch/operation/binding/observation classification, composed EAB
  inner/outer typestate and exact committed-byte execution, full `badNonce`
  rebuild, no blind ambiguous retry or duplicate result application, source-
  secret destruction obligations, capability-free snapshots, and restart
  reconstruction that never automatically repeats a mutating peer ceremony;
  explicit verified-signature propagation into CSR, TLS-ALPN, authority-token,
  and signed-audit effects;
  transactional generation/import/migration/platform adoption with quarantine,
  lifecycle-state/obligation separation, active-as-eligibility semantics,
  fresh-session authority reconstruction, idempotent fenced reconciliation,
  eventual visibility, and crash-persistent cleanup obligations;
  legacy-key migration, provider capability tables, lifecycle facade methods,
  stable invalidation reasons, OCSP freshness edges, and continuous parser/
  canonicalization fuzzing received tactical versions;
- Pebble DNS/TLS integrations were moved after their primitives exist;
- active device-enrollment integrations and identity-controlled validation work
  received versions;
- the roadmap received stable machine work IDs and DAG validation; separate
  unpublished RustCrypto, ring, rustls, executor-mode, and store-model spikes;
  machine portable/native crate tiers; eight independent formal models;
  semantic module/stack/reducer gates; early and final mutation programs;
  linear non-secret nonce authority; layered adapter failure classes;
  verifier-identity/assurance evidence; versioned challenge registration and
  sealed revision receipts; an early real-boundary vertical slice; and explicit
  compile/emulator/native/production platform evidence tiers;
- recommendations to collapse planned releases, weaken adapter MSRV, or move
  current draft/provider/platform scope after `1.0.0` were reviewed but not
  adopted because they conflict with the owner-defined completion and pentest
  contract; graph/critical-path tooling is used to control that scope instead;
- the roadmap now enforces a tactical one-boundary-per-version size rule.

The remaining uncertainty is external rather than hidden scope: exact draft
revisions, CA staging availability, validated FIPS module coverage, and future
standards must be rechecked at their assigned milestones.
