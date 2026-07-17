# Changelog

All notable changes to Vardheim will be documented here. The format follows
Keep a Changelog and the project follows Semantic Versioning.

## Unreleased

### Changed

- Split security-sensitive identity semantics into durable external-effect IDs,
  transient no-store admission/session IDs, observational correlation, and
  untrusted caller idempotency; assigned the real transactional allocator to
  `v0.34.3` and retained a core-only local-signing regression.
- Added `v0.10.24` immutable policy snapshots and single-use current-policy
  dispatch permits, including stale-worker, dispatch-race, and post-result
  activation rules.
- Added `v0.4.27` `RemoteProtocolCapabilities` so controlled agents prove a
  full protocol profile while fixed AWS KMS, Azure Key Vault, and OpenBao APIs
  publish unsupported cells and honest local compensation.
- Defined exact rollback assurance as protected, detecting with a maximum
  window, or unprotected, and required witness bootstrap trust outside the
  restored store.
- Made `VerifiedSignature` an invariant exact-cryptographic-verification type,
  distinct from provider assertions and attestations, while retaining separate
  locality, trust-domain, implementation, validated-module, and binding axes.
- Added provider-neutral security-sensitive identity issuance covering entropy/
  counters, domain separation, guarantee-specific collision handling,
  fork/clone/restore, multi-node concurrency, and caller idempotency separation.
- Confined generic executors to the local process and required later remote
  signer/DNS/KMS/deployment/agent integrations to use purpose-specific bounded,
  versioned, authenticated observation-only protocols.
- Added an external rollback-witness protocol and optional native secret-memory
  assurance; corrected nonce uniqueness to bounded local duplicate checking,
  made hostile-adapter test claims honest, and bound stack evidence to the exact
  build configuration.
- Corrected flat backend failure classification into orthogonal capability,
  dispatch-knowledge, operation-outcome, and observation-status state, and
  added an explicit adapter-assertion-to-qualified-evidence promotion boundary
  with named residual trust assumptions.
- Refined verifier assurance into independent locality, trust-domain,
  implementation, verification-basis, validated-module, and key/input axes:
  exact local verification is the baseline, implementation diversity is an
  optional stronger profile, remote self-verification remains insufficient,
  and FIPS verification stays inside its exact validated boundary.
- Tightened nonce admission to authenticated origin/effective-URL/framing/
  operation/directory evidence with a dedicated `badNonce` retry reservation;
  added whole-store rollback epochs and restored-state quarantine.
- Added executable no-allocation qualification and a private DER/PKIX
  build-versus-adopt spike, expanded roadmap requirement-source taxonomy, and
  separated IANA challenge method tokens from specification and evidence-schema
  revisions.
- Added a machine-readable roadmap/requirement DAG milestone with stable work
  IDs, ownership, prerequisites, generated views, critical-path reporting, and
  validation that cannot merge or omit the established pre-1.0 pentest stops.
- Split pre-freeze architecture qualification into separate unpublished
  RustCrypto, ring, rustls, blocking/async/embedded executor, and transactional
  store spikes; added machine portable/native crate tiers, eight independent
  formal models, semantic module/stack/reducer gates, and early plus final
  security-mutation programs.
- Added linear non-secret nonce authority, layered backend failure classes,
  verifier identity and independent-assurance evidence, conflict-checked
  versioned challenge registration, sealed presentation receipts, an early real
  HTTP/TLS/crypto/outbox vertical slice, and explicit compile/emulator/native/
  production platform evidence tiers.
- Recorded the deliberate scope decision to retain the owner-defined common
  Rust `1.90.0`-`1.97.0` range, every assigned pre-1.0 version, and a pentest at
  each stop instead of collapsing releases or moving current scope after 1.0.
- Expanded the complete pre-1.0 roadmap with explicit release boundaries for
  full errata/reference evidence, reviewed-implementation release binding,
  reproducible SBOMs, cross-target and feature-power-set gates, provider-neutral
  crypto/transport/DNS interfaces, `newNonce`, `newAuthz`, dedicated PKIX
  packaging, status/CT acquisition, certificate adoption, multi-issuer
  migration, compromise response, and early formal/fuzz/concurrency assurance.
- Corrected DER/CSR and real-crypto integration sequencing, and added full RFC
  5280 policy/AIA coverage, PKIX evidence ownership, production clock/DNS
  adapters, EAB HMAC and RSA-PSS capability milestones, certificate retirement
  and inventory reconciliation, and Android/Apple/Windows key-store plus
  PKCS#12 interoperability milestones.
- Added transient context-bound verification evidence, complete local OCSP/CRL/
  SCT verification, isolated credential-free public-PKI fetching, purpose-bound
  legacy hashing, complete DNSSEC/NSEC/NSEC3 and trust-anchor validation, and
  deterministic caller-provided no-heap validation workspaces.
- Added complete EDNS query mechanics, RFC 8945 TSIG and production sequencing,
  issued-certificate trust providers, RFC 7633 Must-Staple deployment/refresh,
  lifecycle facade coverage, stable verification invalidation reasons, OCSP
  freshness edges, and continuous DNS/PKIX parser fuzz targets.
- Added DNS source-port/full-tuple correlation, bounded DNS-over-TCP framing,
  optional DNS Cookies, separate CT v1/v2 profiles, complete OCSP responder and
  chain-status semantics, privacy-safe OCSP acquisition, hardened public-PKI
  HTTP framing/cache partitioning, legacy-key migration, and ring/aws-lc
  per-purpose capability milestones.
- Added signer-proven existing-account adoption, strict RFC 5280 time and
  distinguished-name handling, provider-neutral key-disposition semantics with
  provider-wide reconciliation, CT v1/v2 Merkle auditing, durable MMD inclusion
  monitoring, and optional independent witness/split-view evidence.
- Added strict DER/X.509 structural closure, rollover/deactivation account-key
  disposition, durable certificate renewal key modes, complete authoritative
  DNS referral/glue/DNAME discovery, and explicit replay-safe HTTP/1.1, HTTP/2,
  and HTTP/3 transport milestones with early data disabled.
- Corrected generic DER INTEGER semantics, added ENUMERATED and NULL closure,
  clarified normalized certificate signature-algorithm equivalence, and added
  provider/session-bound public-key validation and signer-binding milestones
  across PKIX, software crypto, HSM/KMS, remote, and platform providers.
- Added domain-separated signer binding and universal exact-request
  signer-consumer admission with explicit enforcement for account
  creation/recovery/adoption, both rollover signers, CSR construction,
  certificate-key revocation, TLS-ALPN ephemeral signing, future handle-backed
  effects, and every concrete provider.
- Corrected signer admission circularity by retaining `v0.10.11` for transient
  role-limited `BoundSigner` establishment and adding `v0.10.12` for locally
  minted exact-request admission, narrowly exempting only canonical
  `bind_signer`, and specifying destructive admission handling across signer
  outcomes, `badNonce`, network ambiguity, invalidation, concurrency, HSM/KMS,
  and user-presence signers.
- Added `v0.10.13` transactional key onboarding and `v0.56.8` provider/import
  conformance for generation, PKCS#8/legacy/PKCS#12 import, hardware/KMS
  creation, remote signers, and platform adoption, with quarantine,
  idempotency, lost-response/eventual-visibility reconciliation, activation
  gates, durable cleanup obligations, and no absence-as-destruction claim.
- Clarified in-flight signer invalidation: pre-dispatch invalidation blocks the
  operation, racing or post-dispatch invalidation remains ambiguous without
  positive provider evidence, admission stays consumed, and replacement uses a
  revalidated key, new binding, request identity, and admission.
- Added `v0.10.14` for fresh live key-authority reconstruction and separated
  durable lifecycle eligibility/audit history from transient validation,
  signer-binding, request-admission, and effect authority.
- Changed transactional onboarding to a
  `KeyLifecycleState × KeyObligationSet` model so reconciliation,
  revalidation, disposition, cleanup, and operator-decision work survives every
  failure and crash boundary; extended snapshot, fencing, provider, HSM, and
  KMS milestones with restart, alias/version retargeting, object replacement,
  replayed-history, and stale-worker tests.
- Added `v0.10.15` immutable signer dispatch and verified-signature commit plus
  `v0.56.9` provider conformance: mutable locators are discovery-only,
  `BoundSigner` and dispatch pin an immutable native identity/version and
  public-key digest, provider output remains untrusted, and exact local
  verification is mandatory before any protocol effect.
- Propagated fresh reconstruction and binding-to-signing TOCTOU race coverage
  to software, ring, aws-lc/FIPS, PKCS#11, TPM, AWS/Azure KMS, OpenBao, remote
  signer/agent, Android, Apple, and Windows provider milestones.
- Added `v0.10.16` and `v0.56.10` for handle-backed EAB/TSIG MAC authority:
  immutable secret-version binding, exact-input single-use admission,
  `UnverifiedMac`, constant-time independent `VerifiedMac`, distinctly typed
  provider assertions and genuine cryptographic attestations, explicit weaker-
  assurance policy, and no secret export or provider fallback.
- Added tactical MAC conformance milestones for PKCS#11, TPM, AWS KMS, Azure
  capability closure, OpenBao, and the remote protocol/agent, and propagated
  the boundary through EAB, TSIG rotation, RustCrypto, ring, aws-lc/FIPS, and
  production RFC 2136.
- Explicitly required `v0.10.15` immutable dispatch and `VerifiedSignature` for
  CSR, TLS-ALPN, locally signed authority-token effects, draft authority-token
  constraints, and signed audit checkpoints, with wrong-key, replacement,
  malformed-output, and verifier-unavailable regressions.
- Added `v0.10.17`-`v0.10.18` for transactional symmetric-secret onboarding,
  typed content binding, quarantine, source-secret destruction obligations,
  capability-free snapshots, and fresh per-session MAC authority
  reconstruction; immutable provider identity alone no longer proves intended
  EAB or TSIG secret content.
- Added `v0.56.11` shared conformance plus tactical RustCrypto, ring,
  aws-lc/FIPS, PKCS#11, TPM, AWS KMS, Azure, OpenBao, and remote-agent
  symmetric-secret onboarding milestones through `v0.66.5`.
- Added `v0.10.19`-`v0.10.20` to break the `PeerConfirmed` quarantine cycle
  with private single-use `SecretBindingAttempt`, exact local/peer ceremony
  confinement, stable peer-effect identities, authenticated observations, and
  explicit non-mutating-versus-mutating semantics.
- Added `v0.33.5` durable peer-binding outbox/reconciliation and `v0.56.12`
  provider conformance, including lost EAB account success, duplicate-account
  prevention, ambiguous TSIG DNS UPDATE ownership/rollback, source-secret
  retention, and restart rules that never automatically repeat a mutating peer
  ceremony.
- Added `v0.10.21` to replace flat peer results with orthogonal dispatch,
  operation, binding-evidence, and observation state plus an explicit recovery
  matrix that permits only wholly fresh attempts after positive unsent proof.
- Added `v0.16.4` composed EAB account-creation typestate, `v0.33.6` durable
  exact-request execution/recovery, and `v0.37.5` cross-adapter conformance to
  prevent inner/outer evidence stitching, committed-request rebuilding,
  partial crash restoration, incomplete `badNonce` rebuilds, and repeated
  success application.
- Renamed ordinary opaque MAC verification evidence to
  `ProviderAssertedMac`; reserved `CryptographicallyAttestedMac` for verified
  signed/native replay-protected receipts bound to the complete operation
  transcript, and retained `VerifiedMac` for independent verification.

## 0.3.1 - Unreleased

### Added

- Byte-pinned complete IANA ACME registry group and deterministic bounded
  fixtures for all 107 current records across 13 registries.
- Current HTTP successor mapping, 92-record supporting-standard inventory,
  exact external-profile revision pins, and complete normative-reference
  closure for all published ACME RFCs.
- Fail-closed registry generator with adversarial integrity, XML safety,
  omission, duplication, and resource-bound regression tests.
- Machine-checked closure for all normative RFC and non-RFC references used by
  the published ACME family.
- Encoding-independent XML declaration rejection backed by UTF-8, UTF-16, and
  UTF-32 entity-expansion regression tests.
- Exact crates.io archive allowlisting with traversal, entry-type, duplication,
  omission, file-count, and unpacked-size regression tests.
- Passing maintainer-supplied pentest and clean remediation retest evidence.

## 0.3.0 - 2026-07-12

### Added

- Complete checksum-bound section inventory for all 65 tracked RFCs.
- Reviewed all-status RFC Editor errata snapshot for all 13 published ACME
  RFCs, with offline validation and explicit live drift checks.
- Permanent facade/tag version equality and publication enforcement.
- Bounded RFC Editor connection and transfer timeouts with an end-to-end
  fetch-and-hash regression test.
- Passing maintainer-supplied pentest and clean remediation retest evidence.

## 0.2.0 - 2026-07-12

### Added

- Dependency-ordered workspace publication helper, independently versioned
  per-crate release plan, regression tests, and operator documentation.
- Structured release metadata and pentest-readiness validators with exhaustive
  missing, malformed, failed, stale, wrong-commit, and tag refusal tests.
- Verified package archives, matching SPDX SBOM enforcement, and the dedicated
  `v0.2.0` release gate.
- Fail-closed EOF and non-TTY publication handling plus release-state
  revalidation immediately before every irreversible crate publish.
- Passing maintainer-supplied pentest and clean remediation retest evidence.

## 0.1.0 - 2026-07-12

### Added

- Security-first Cargo workspace foundation.
- Five dependency-free `no_std` crates with a facade boundary.
- Rust `1.90.0` through `1.97.0` compatibility policy and CI matrix.
- Dual MIT and Apache-2.0 licensing.
- Initial security, RFC, implementation, release, and compatibility documents.
- Local checks, supply-chain policy, SBOM tooling, and pentest release gate.
- Application-owned panic policy and non-overridable lossy-cast lint policy.
- Tactical one-boundary release sizing with split parser, PKIX, workflow,
  persistence, deployment, operations, platform, and qualification milestones.
- ACME completeness and production web-server replacement acceptance contract.
- Sixty-five exact RFC reference copies with SHA-256 integrity enforcement,
  read-only local locking, owner review, and Cargo package exclusion.
- Passing maintainer-supplied external pentest and clean retest evidence.
- CI-portable shell syntax validation and release scripts with no undeclared
  ripgrep dependency.
