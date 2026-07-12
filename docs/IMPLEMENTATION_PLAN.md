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
- `vardheim-rustls`: introduced at `0.51.0` for the concrete rustls boundary.

Heavy provider SDKs, validated cryptographic distributions, hardware/remote
signers, test servers, CLI, daemon, and agents may be private workspace packages
or separately published packages when the release plan reaches them. Internal
account, order, certificate, renewal, policy, persistence, deployment, and
observation concerns remain modules unless they meet the crate-splitting rule.

## Non-Negotiable Engineering Rules

1. Every current library crate is `no_std`; `alloc` and `std` are explicit and
   localized when a milestone proves they are needed.
2. No source file exceeds 500 physical lines.
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

Versions `0.1.0` through `0.4.4` establish the workspace, release refusal
tooling, exact RFC/IANA sources, threat model, invariants, and executable state
models. Implementation must not start a parser before its resource budget and
source requirements are committed.

Required outputs:

- GitHub, supply-chain, release, pentest, documentation, and compatibility
  policies adapted from the reference projects;
- tracked, unmodified, integrity-locked RFC reference set excluded from Cargo
  packages, with a reproducible fetch/check manifest;
- conformance matrix keyed by RFC section and test fixture;
- a completeness register reviewed whenever scope changes; and
- immutable historical evidence and semantic release-to-release comparison as
  defined by [the regression strategy](REGRESSION_STRATEGY.md).

## Strict Input And JOSE Sequence

Versions `0.5.0` through `0.13.0` build the narrowest critical core:

- budgets precede all untrusted decoding;
- strict types precede protocol models;
- stable errors precede broad flows;
- JSON rejects duplicate keys and unbounded structures;
- base64url, JWK, JWA, thumbprints, JWS, EAB, and rollover use typed purpose-
  specific construction rather than arbitrary JSON values;
- nonce ownership makes reuse unrepresentable where practical.

Crypto implementations do not enter this phase. Golden tests use deterministic
test signers and verify exact signing inputs. Real providers arrive only after
the provider-neutral key roles are stable.

## RFC 8555 Sequence

Versions `0.14.0` through `0.25.0` implement the entire client side of RFC 8555
in resource order: URL/origin policy, directory, account creation and lifecycle,
rollover, orders, authorizations, polling, finalization, retrieval, revocation,
problems, and pagination.

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

Versions `0.26.0` through `0.31.0` implement HTTP-01, CSR policy, certificate
parsing, verification, and alternate chains. Challenge presentation is a
transaction: prepare, present, visibility barrier, self-check, CA acknowledgement,
poll, and owned cleanup. Cleanup obligations are persisted; async destruction
is never relied upon.

Certificate verification compares:

- order identifiers;
- CSR identifiers and public key;
- returned leaf SANs and public key;
- requested certificate profile and validity;
- chain candidates against configured roots and policy.

Non-certificate PEM objects are rejected, including server-injected private
keys.

## Durable Orchestration Sequence

Versions `0.32.0` through `0.39.0` add deterministic commands/events, snapshots,
migrations, CAS revisions, outbox effects, leases, fencing, stores, transactional
deployment, public APIs, fault injection, and Pebble integration.

Every external side effect follows:

1. validate it against current state and policy;
2. persist intended effect and revision;
3. execute with an idempotency/reconciliation classification;
4. persist the typed outcome;
5. apply it once and record cleanup obligations.

The test server must kill/restart the orchestrator after every transition and
effect boundary. A stale worker cannot present, finalize, activate, clean, or
roll back after losing its fencing authority.

## Renewal And Challenge Ecosystem

Versions `0.40.0` through `0.51.0` implement ARI, durable scheduling, complete
DNS behavior, provider adapters, the restricted DNS agent, TLS-ALPN-01, and the
rustls adapter.

DNS propagation checks query authoritative servers and distinguish secure,
insecure, bogus, and indeterminate DNSSEC outcomes. Provider record handles
preserve unrelated TXT data and enable exact cleanup. Heavy AWS and Azure SDKs
stay outside core dependency graphs.

TLS-ALPN-01 identity construction remains independent from rustls. The rustls
resolver activates only for matching identifier, exact `acme-tls/1`, and an
active unexpired owned presentation.

## Transport And Crypto Sequence

Versions `0.52.0` through `0.66.0` introduce strict transports, async/blocking/
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

Versions `0.82.0` through `0.91.0` implement SQLite, PostgreSQL HA,
multi-tenancy, deployment adapters, Kubernetes, remote deployment agents,
redacted observability, signed audit records, CLI, daemon, and hardened agents.

Secrets are never ordinary observability fields. Identifier logging defaults to
hashed or redacted. Multi-tenant stores separate encryption, quotas, leases,
accounts, intents, and audit streams.

## Platform And Assurance Sequence

Versions `0.92.0` through `0.97.2` close platform support, custom target
readiness, Kani, Loom, fuzzing, Miri, sanitizers, and model checking. Versions
`0.100.0` through `0.111.0` isolate revisioned experimental/IESG drafts. Draft
work is complete before 1.0 but remains outside stable RFC claims and disabled
by default.

## Production Qualification Sequence

The `0.120` alpha/beta/RC series freezes APIs, closes coverage, runs full
interoperability, load/chaos/disaster recovery, reproducible supply-chain
qualification, independent core and adapter audits, FIPS qualification, and a
final exact-commit pentest. `1.0.0` is tagged only after those gates pass.

## Testing Architecture

The permanent test ladder is:

```text
unit and RFC vectors
    -> compile-fail and property tests
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
