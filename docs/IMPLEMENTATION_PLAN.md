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
signers, test servers, CLI, daemon, and agents may be private workspace packages
or separately published packages when the release plan reaches them. Internal
account, order, certificate, renewal, policy, persistence, deployment, and
observation concerns remain modules unless they meet the crate-splitting rule.
Route 53, Azure DNS, Redis, HTTP frameworks, rustls/OpenSSL, crypto providers,
and similar ecosystems do not become features of the portable challenge or
core crates; their packages depend inward on Vardheim semantic types.

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
   adapters isolate and audit every unsafe boundary.
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
early executable TLA+/Quint state models, regression replay, and the pure
effect/backend contract. Versions `0.4.6` and `0.4.7` freeze crate/feature
topology and the build/API ergonomics gates. Implementation must not start a
parser before its resource budget and source requirements are committed.

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
- provider-neutral digest, signing, verification, entropy, and key-generation
  semantics precede their first JOSE, scheduling, CSR, PKIX, or challenge
  consumer while concrete cryptographic implementations remain later;
- nonce ownership makes reuse unrepresentable where practical; and
- Kani, differential parsing, fuzzing, and Loom begin with the primitives they
  protect rather than being postponed to final qualification.

Crypto implementations do not enter this phase. Golden tests use deterministic
test signers and verify exact signing inputs. Real providers arrive only after
the provider-neutral key roles are stable.

## RFC 8555 Sequence

Versions `0.14.0` through `0.25.2` implement the entire client side of RFC 8555
in resource order: bounded transport semantics, URL/origin policy, directory,
`newNonce`, account creation and lifecycle, rollover, multi-issuer policy,
orders, ordinary and `newAuthz` pre-authorizations, polling, finalization,
retrieval, revocation, problems, and pagination.

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

Versions `0.26.0` through `0.31.1` implement HTTP-01, introduce
`vardheim-pkix`, and complete CSR policy, certificate parsing, verification,
optional OCSP/CRL/CT acquisition, and alternate chains. Challenge presentation
is a transaction: prepare, present, visibility barrier, self-check, CA
acknowledgement, poll, and owned cleanup. Cleanup obligations are persisted;
async destruction is never relied upon.

Certificate verification compares:

- order identifiers;
- CSR identifiers and public key;
- returned leaf SANs and public key;
- requested certificate profile and validity;
- chain candidates against configured roots and policy.

Non-certificate PEM objects are rejected, including server-injected private
keys.

## Durable Orchestration Sequence

Versions `0.32.0` through `0.39.5` add the pure
command/state/policy/event reducer, typed effects and positive evidence,
snapshots, migrations, CAS revisions, outbox effects, leases, fencing, stores,
transactional deployment, public APIs, reusable adapter conformance, a
deterministic hostile CA, a test-only loopback transport, Pebble integration,
historical differential replay, existing-certificate adoption, renewal
bootstrap, and durable multi-issuer migration policy.

Every external side effect follows:

1. validate it against current state and policy;
2. persist intended effect and revision;
3. execute with an idempotency/reconciliation classification;
4. persist the typed outcome;
5. apply it once and record cleanup obligations.

The test server must kill/restart the orchestrator after every transition and
effect boundary. A stale worker cannot present, finalize, activate, clean, or
roll back after losing its fencing authority.

Executors may be async, blocking, polling, embedded, or remote, but async never
enters the reducer. Static dispatch remains available without allocation;
object-safe executor collections require an explicit `alloc` feature. Backend
features only expose constructors and never select an implementation.

## Renewal And Challenge Ecosystem

Versions `0.40.0` through `0.51.3` implement ARI, durable scheduling,
certificate/account-key compromise response, provider-neutral DNS query
semantics, complete DNS behavior, provider adapters, the restricted DNS agent,
TLS-ALPN-01, and the rustls/OpenSSL adapters.

DNS propagation checks query authoritative servers and distinguish secure,
insecure, bogus, and indeterminate DNSSEC outcomes. Provider record handles
preserve unrelated TXT data and enable exact cleanup. Heavy AWS and Azure SDKs
stay outside core dependency graphs.

TLS-ALPN-01 identity construction remains independent from rustls. The rustls
resolver activates only for matching identifier, exact `acme-tls/1`, and an
active unexpired owned presentation.

## Transport And Crypto Sequence

Versions `0.52.0` through `0.66.2` introduce strict transports, async/blocking/
embedded profiles, explicit key roles, RustCrypto, ring, aws-lc-rs, separate
AWS-LC FIPS, PKCS#11, TPM2, AWS KMS, Azure Key Vault, OpenBao-compatible, and
remote/offline signing.

Each provider implements capabilities and is explicitly selected. Provider
negotiation is:

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

Versions `0.82.0` through `0.91.2` implement SQLite, PostgreSQL HA,
multi-tenancy, deployment adapters, Kubernetes, remote deployment agents,
redacted observability, signed audit records, CLI, daemon, and hardened agents.

Secrets are never ordinary observability fields. Identifier logging defaults to
hashed or redacted. Multi-tenant stores separate encryption, quotas, leases,
accounts, intents, and audit streams.

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
