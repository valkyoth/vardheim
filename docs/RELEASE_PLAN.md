# Vardheim Release Plan To 1.0

Status: complete scope plan

This plan assigns every currently known Vardheim requirement to a version
before `1.0.0`. Nothing listed here is an unversioned deferral. If new required
work is discovered, add or split a version before implementation crosses the
affected boundary.

## Mandatory Exit Contract For Every Version

Every row below is a complete release boundary. A version is not implemented
until all of its public functions, error paths, state transitions, parsers,
feature combinations, and platform branches have unit and adversarial tests.
Where relevant it also needs vectors, property tests, fuzz targets, integration
tests, crash/fault injection, and conformance evidence.

For **every** `v0.N.0`, patch, RC, and `v1.0.0`:

1. update RFC/source evidence, changelog, release notes, compatibility, and
   known limitations;
2. run `scripts/checks.sh`, the Rust `1.90.0` through `1.97.0` matrix,
   `cargo deny check`, `cargo audit`, package checks, and SBOM generation;
3. after `v0.4.4`, replay every applicable historical evidence set and review
   the semantic difference report; after `v0.119.0`, also compare against the
   latest released public compatibility baseline;
4. meet milestone-specific proof in the table;
5. stop and print:
   `vX.Y.Z implementation stop reached. Run pentest for this exact commit.`;
6. fix all findings and rerun all evidence;
7. require a permanent exact-commit `Status: PASS` report before tagging.

Passing one version never authorizes implementation to skip the next version's
stop. A security fix receives its own patch version and pentest.

## Release Principles

- Rust stable `1.97.0` is pinned; Rust `1.90.0` remains the MSRV through 1.0.
- Core and challenge-calculation crates remain `no_std`; `alloc` and `std` are
  explicit local features only where their behavior is unavoidable.
- Backend features make implementations available but never select one.
- Protocol behavior is first-party and strictly follows published RFCs and
  verified errata. Third-party crates enter through reviewed narrow boundaries.
- No source file may exceed 500 physical lines.
- No certificate is production-safe until verified and transactionally
  activated; receipt from a CA is not trust evidence by itself.
- Experimental drafts use exact revisions, remain disabled by default, and do
  not count toward stable RFC conformance.

## Tactical Milestone Size Rule

One version may introduce only one independently reviewable boundary: one
parser layer, one protocol resource or transition family, one persistence
primitive, one backend/provider, one deployment target, or one assurance
technique. A version must be split before implementation when it would require
more than one new external dependency family, more than one independently
deployable adapter, or more than one unrelated state-machine slice. Integration
releases may connect already completed boundaries but may not introduce their
missing primitives. Patch-numbered roadmap releases below are planned feature
releases, not afterthoughts; each receives the same pentest stop as a minor.

## Phase 0 - Repository, Evidence, And Specification

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.1.0` | Repository foundation: five dependency-free `no_std` crates, facade re-exports, dual license, Rust matrix, CI, CodeQL Default policy, deny/audit/SBOM policy, docs, file-size rule, release notes, and pentest template. | Clean full checks on Rust 1.97.0 and compatibility checks on every stable line from 1.90.0. |
| `v0.2.0` | Enforce release discipline: release metadata validator, exact-commit pentest validator, tag guard, publish order, independent crate versions, package checks, SBOM presence, and negative tests of every refusal path. | Release-readiness test suite proves missing, malformed, stale, wrong-commit, and failed pentest evidence cannot pass. |
| `v0.3.0` | Normative source baseline: complete section-level published RFC inventory, local RFC fetch/check script, source hashes, and verified errata log. | Machine-check every claimed RFC and accepted/rejected erratum against the pinned local snapshot. |
| `v0.3.1` | Registry baseline: pinned IANA ACME registries, current HTTP replacement mapping, supporting-standard inventory, and external profile revisions. | Every known field, error, resource, identifier, validation method, and extension value has a generated bounded registry fixture. |
| `v0.3.2` | Conformance system: machine-readable requirement IDs, conformance tiers, capability schema, fixture provenance, and coverage/report format. | Every planned behavior maps to a source requirement and future test slot; no implementation starts with an unassigned requirement. |
| `v0.3.3` | Upstream drift monitor for RFC status/errata, IANA ACME registries, referenced profiles, and pinned draft revisions, producing a machine-readable difference report without mutating accepted baselines. | Offline fixtures prove additions, removals, status changes, errata, and draft replacement are detected; live checks are advisory until reviewed and assigned to a version. |
| `v0.4.0` | Threat model: assets, adversaries, trust boundaries, abuse cases, security invariants, and non-guarantees. | Independent review finds no unowned trust boundary or secret lifecycle. |
| `v0.4.1` | State-model baseline for account, issuance, challenge, certificate verification, deployment, renewal, and cancellation lifecycles. | Model traces reach every state and reject every enumerated invalid transition. |
| `v0.4.2` | Test and evidence architecture: vectors, properties, fuzzing, fault injection, integration tiers, coverage policy, and completeness register. | Every invariant has at least one assigned evidence technique and release owner. |
| `v0.4.3` | Immutable regression-evidence manifest for vectors, corpora, model traces, interoperability captures, expected semantic outcomes, provenance, and content hashes. | Tamper, omission, duplicate-ID, provenance, and accidental-baseline-replacement negatives pass; evidence remains addressable across releases. |
| `v0.4.4` | Longitudinal replay runner that executes every compatible historical evidence set against current code and emits a semantic difference report. | Seeded old/current fixture simulations detect missing behavior and changed results; an expected change cannot pass without a reviewed replacement vector, reason, requirement link, and release note. |

## Phase 1 - Bounded Types, Encoding, And JOSE

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.5.0` | Core resource budgets for bytes, strings, collections, nesting, and cumulative allocation/work accounting. | Boundary, overflow, exhaustion, and exact-limit properties for every constructor and decrement path. |
| `v0.5.1` | Protocol-operation budgets for headers, identifiers, challenges, subproblems, links, redirects, retries, polling, and elapsed time. | Composed budgets cannot reset or bypass a parent ceiling across nested operations. |
| `v0.6.0` | Strict URI, origin, directory, and resource URL newtypes with normalization and cross-type isolation. | Constructors reject user-info, fragments, unsafe schemes, ambiguity, and cross-domain substitutions. |
| `v0.6.1` | Account, order, authorization, challenge, certificate, request, effect, revision, tenant, and key-handle domains. | Cross-resource misuse is prevented by types and compile-fail tests. |
| `v0.6.2` | Identifier domains: DNS A-label normalization, IDNA 2008 policy, wildcard representation, canonical IP bytes, email/TNAuthList/bundleEID/NfInstanceId extension shells, and sorted identifier sets. | Unicode, public-suffix-policy boundary, wildcard, equivalence, duplicate, and canonicalization corpora pass. |
| `v0.6.3` | Secret-bearing nonce/token/key-authorization/EAB types, wall/monotonic time domains, deadlines, correlation IDs, and redacted handles. | Required secrets are non-Copy/non-Clone, always redact, and cannot cross clock or purpose domains. |
| `v0.7.0` | Stable protocol and server-problem errors, all registered problem types, bounded subproblems, identifier association, instance URI, and unknown problem retention. | Every problem mapping and bounded round trip is tested without flattening to strings. |
| `v0.7.1` | Retry/operator advice, error provenance, correlation, source-category conversion, and secret-safe Display/Debug policy. | Every error class has an explicit retry decision; snapshots prove no secret-bearing formatting. |
| `v0.8.0` | Bounded UTF-8 JSON tokenizer with string escape, scalar, number grammar, depth, token-count, and byte limits. | Differential lexical corpus and fuzzing never panic or exceed budgets. |
| `v0.8.1` | Strict object/array decoder with duplicate-key rejection, null/missing/empty distinction, and exact consumption. | Duplicate, recursive, trailing, ambiguous, and oversized inputs fail deterministically. |
| `v0.8.2` | Typed ACME JSON schema decoding with exact timestamps/numeric ranges, known-field validation, and bounded unknown-field preservation. | Known fields cannot be overridden by extensions; typed fixture and mutation corpus passes. |
| `v0.9.0` | RFC 4648 base64url without padding, exact-length decoded buffers, and canonical rejection. | RFC vectors, exhaustive short-input tests, round trips, noncanonical padding/alphabet rejection, and fuzzing. |
| `v0.10.0` | RFC 7518 algorithm and capability models with explicit policy intersection and no server-selected local algorithm. | Algorithm/key/purpose mismatch and downgrade matrices fail closed. |
| `v0.10.1` | RFC 7517 bounded JWK models and canonical public-key member encoding for required key families. | Leading-zero, coordinate, exponent, curve, duplicate-member, and private-member rejection fixtures pass. |
| `v0.10.2` | RFC 7638 canonical JWK thumbprints and account-key authorization digest inputs. | Published vectors and cross-implementation differential evidence pass byte-for-byte. |
| `v0.11.0` | RFC 7515 flattened JWS construction with typed protected headers, exactly one of `jwk`/`kid`, exact signed URL, typed payloads, and signing-purpose separation. | Golden signing-input vectors and properties proving header exclusivity, deterministic bytes, no arbitrary JSON signing, and no algorithm confusion. |
| `v0.12.0` | EAB nested JWS construction, HMAC purpose separation, EAB algorithm policy, and secret destruction lifecycle. | EAB vectors plus wrong key/URL/algorithm and retained-secret negatives pass. |
| `v0.12.1` | Account-key rollover inner/outer JWS envelopes with old/new key and purpose separation. | Swapped inner/outer keys, URLs, accounts, algorithms, and payloads are rejected. |
| `v0.13.0` | Single-use replay nonce ownership, per-directory bounded queues, duplicate rejection, cancellation consumption, and bounded `badNonce` retry semantics. | Property and concurrency tests prove no consumed nonce can be emitted or reinserted and all retries re-sign with a fresh nonce. |

## Phase 2 - RFC 8555 Protocol Core

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.14.0` | Typed request/response envelopes, bounded ACME headers/body, status/content type, effective URL, and exact signed-request URL binding. | Header/body/content-type/status and mismatched URL adversarial matrix passes. |
| `v0.14.1` | Origin authorization and SSRF policy: HTTPS, directory identity, endpoint/link allowlists, IP classification, proxies, and no automatic signed-request redirects. | Cross-origin, redirect, user-info, DNS rebinding, local/link-local/private network, and normalization matrix passes. |
| `v0.15.0` | Directory discovery parsing for all base resources, metadata, CAA identities, EAB-required, and bounded unknown fields. | Missing, duplicate, malformed, unsupported, and hostile endpoint fixtures fail closed. |
| `v0.15.1` | Directory refresh/change detection, trust re-evaluation, ToS change workflow, cached identity, and capability invalidation. | Endpoint/origin/ToS changes require the correct policy or operator action and cannot reuse stale trust. |
| `v0.16.0` | Account creation with contacts, ToS agreement, Location binding, status, and successful state persistence event. | Positive/negative flows and malformed account responses pass. |
| `v0.16.1` | `onlyReturnExisting` account recovery and lost-account-creation response reconciliation. | Existing, absent, ambiguous, duplicated, and wrong-Location cases cannot corrupt account identity. |
| `v0.16.2` | EAB-required account creation integration and deletion of EAB material only after durable success. | Required/optional EAB and crash-at-every-boundary cases pass. |
| `v0.17.0` | Account retrieval, contact update, status handling, and replay/stale response policy. | Every account state and update precondition is tested. |
| `v0.17.1` | Account order enumeration and pagination semantics with bounded link traversal. | Empty, multi-page, cyclic, cross-origin, repeated, and oversized collections pass. |
| `v0.17.2` | Account deactivation and recovery reconciliation. | Ambiguous response, retry, already-deactivated, stale key, and illegal transition cases pass. |
| `v0.18.0` | Account key rollover with nested JWS, recovery checkpoints, old/new signer purpose control, and offline ceremony boundary. | Golden vectors, crash at every rollover step, rejection of swapped keys or URLs, and old/new recovery tests. |
| `v0.19.0` | Normalized certificate intent, stable intent digest, sorted identifiers, validity/profile/key/challenge/deployment policy, and local single-flight identity. | Intent equivalence, duplicate, tenant, ordering, and policy mutation properties pass. |
| `v0.19.1` | `newOrder` construction and response parsing with identifiers, validity, Location, expiry, error, extension fields, and authorization/finalize URLs. | Multi-identifier and malformed order fixtures pass. |
| `v0.19.2` | Unknown `newOrder` outcome reconciliation through account orders and normalized intent evidence. | Lost-response simulation never blindly duplicates an order without policy authorization. |
| `v0.20.0` | Authorization models and transitions: status, expiry, identifier, wildcard metadata, reuse, deactivation, and bounded extensions. | Exhaustive authorization transition and stale/reuse matrix passes. |
| `v0.20.1` | Challenge offer/status/error models, unknown challenge retention, selection inputs, and acknowledgement request semantics. | Mixed known/unknown offers and impossible challenge transitions fail correctly. |
| `v0.20.2` | Multi-authorization aggregation, readiness, mixed terminal outcomes, and cleanup ownership assignment. | Permutation/property tests prove order-independent correct aggregation. |
| `v0.21.0` | POST-as-GET request semantics and typed retrieval for account, order, authorization, challenge, and certificate resources. | Empty-payload/signature and resource-type confusion fixtures pass. |
| `v0.21.1` | Retry-After HTTP-date/delta parsing, wall/monotonic clock conversion, bounded backoff, jitter inputs, and clock-skew reporting. | Date/delta/overflow/skew vectors and deterministic injected-clock tests pass. |
| `v0.21.2` | Polling controller, status reconciliation, cancellation, deadlines, retry budgets, and endless/contradictory server behavior. | Cancellation races, endless polling, stale response, and contradictory state fault injection pass. |
| `v0.22.0` | CSR finalization request/response semantics, order-ready enforcement, CSR digest binding, processing polling, and certificate URL acceptance. | Impossible finalization transitions fail; lost finalization responses reconcile without blind unsafe retries. |
| `v0.23.0` | Certificate POST-as-GET retrieval, media-type policy, bounded RFC 7468 PEM tokenization, and strict certificates-only bundles. | Private-key injection, malformed label, oversized bundle, wrong first object, and non-certificate object tests pass. |
| `v0.23.1` | RFC 8288 Link parsing and bounded alternate-chain discovery with origin policy and relation filtering. | Hostile, cyclic, cross-origin, malformed, duplicated, and excessive alternate links fail safely. |
| `v0.24.0` | Complete revocation: account-key and certificate-key signing, reason validation, already-revoked behavior, and signer-purpose isolation. | Every RFC reason and signer path plus wrong-key, wrong-cert, replay, ambiguous outcome, and idempotency tests. |
| `v0.25.0` | Complete structured problem/subproblem decoding, registered/unknown extension problems, operator-action links, and sanitized server detail. | Complete problem fixture and recursive/resource-limit suite passes. |
| `v0.25.1` | RFC 8555 pagination and collection conformance closure across account orders and extension collections. | Cyclic, repeated, cross-origin, malformed, and budget-exhausting pagination tests pass. |
| `v0.25.2` | RFC 8555 section-by-section client conformance closure with no catch-all implementation work. | The machine-readable matrix reports every mandatory client requirement implemented and every optional behavior explicitly classified. |

## Phase 3 - Challenge And Certificate Foundation

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.26.0` | HTTP-01 core: exact token/path/key-authorization construction, DNS/IP identifier binding, wildcard prohibition, and expiry. | RFC vectors; traversal, ambiguous path, Unicode, host mismatch, stale token, and token-bound tests. |
| `v0.27.0` | HTTP challenge presentation trait, in-memory store, generic route helper, expiry, and ownership receipts. | Concurrent presentations never overwrite or expose unrelated data; exact lookup/expiry properties pass. |
| `v0.27.1` | HTTP-01 local/external self-check interface, IPv4/IPv6 policy, multi-vantage evidence, and cluster visibility barrier. | Resolver/routing disagreement, partial visibility, timeout, and false-positive simulations pass. |
| `v0.27.2` | Durable HTTP challenge cleanup obligations, compare-and-delete ownership, retry classification, and crash recovery. | Cleanup never removes another workflow's data and resumes after every injected crash. |
| `v0.27.3` | Axum and Actix HTTP-01 integration examples and tested adapter helpers built on the generic route/store API, without framework dependencies in core crates. | Framework integration suites prove exact routing, host binding, concurrency, expiry, response body, and cleanup behavior. |
| `v0.27.4` | Redis-backed distributed HTTP-01 presentation store with namespacing, TTL, compare-and-delete ownership, cluster visibility, and credential redaction. | Real Redis integration covers failover, stale TTL, duplicate token, lost acknowledgement, wrong owner, partition, and cleanup. |
| `v0.28.0` | HTTP-01 filesystem webroot adapter with restrictive permissions, atomic creation, exact cleanup, Nginx/Apache integration examples, and no arbitrary CA-controlled path. | Platform filesystem tests, symlink/race/traversal attacks, crash cleanup, and permission verification. |
| `v0.29.0` | Certificate key policy, key-handle role binding, algorithm/export/reuse/storage/attestation choices, and account-key separation. | API/type tests prevent account/leaf reuse and silent algorithm/exportability fallback. |
| `v0.29.1` | RFC 2986 CSR construction with exact SANs, wildcard/subject/KU/EKU/profile policy, deterministic extension ordering, and signature request boundary. | Published/generated vectors and exact order/CSR identifier-set equality pass. |
| `v0.29.2` | External CSR bounded parsing, signature verification, public-key capability checks, and policy validation before finalization. | Duplicate SAN, unauthorized subject, wrong signature/key/algorithm, malformed DER, and profile mismatch tests pass. |
| `v0.30.0` | Bounded canonical DER length/tag/value parser with depth/element/byte budgets and exact consumption. | Hostile DER corpus, mutation fuzzing, and differential structural fixtures pass. |
| `v0.30.1` | X.509 leaf/intermediate structural models for SPKI, names, validity, SAN, KU/EKU, basic/name constraints, critical extensions, signatures, and algorithm identifiers. | Certificate parsing corpus passes without making path-trust claims. |
| `v0.30.2` | Issued-leaf binding: CSR public key, exact authorized identifiers, requested profile, validity bounds, required/prohibited extensions, and no extra SANs. | Key/SAN/profile/validity/extension substitution corpus fails closed. |
| `v0.30.3` | RFC 5280 path construction and validation with explicit trust anchors, constraints, name constraints, signature algorithms, depth/time budgets, and no network fetching. | Official/independent valid and broken path fixtures plus differential evidence pass. |
| `v0.30.4` | RFC 6125 service identity policy for DNS/IP/email/profile-specific identities, wildcard rules, IDNA binding, and caller-selected service context. | Identity, wildcard, Unicode, IP-type, and cross-service confusion corpus passes. |
| `v0.30.5` | Certificate-status evidence policy: stapled/caller-provided OCSP and CRL evidence interfaces, freshness/failure modes, and explicit offline/soft/hard-fail policy without hidden network I/O. | Revoked, stale, unknown, unavailable, mismatched issuer, and policy-mode fixtures pass. |
| `v0.30.6` | Certificate Transparency/SCT evidence interface and operator policy for public Web PKI deployments, without claiming CT-log operation in core. | Valid/invalid/unknown-log/stale-list and disabled-policy behavior is explicit and tested. |
| `v0.31.0` | Alternate-chain candidate parsing and bounded evaluation against completed PKIX policy. | Broken, looping, ambiguous, expired, and cross-signed candidate fixtures pass. |
| `v0.31.1` | Explicit chain selection policy: server default, root fingerprint, issuer, shortest valid, compatibility metadata, and bounded custom selector. | Deterministic selection/property tests prove no hardcoded CA names or order-dependent result. |

## Phase 4 - Deterministic And Durable Lifecycle

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.32.0` | Deterministic account/directory/order command-event machine through order creation and recovery. | Exhaustive transitions and replayed-event properties pass with no I/O. |
| `v0.32.1` | Authorization/challenge presentation, validation, polling, cleanup, retry, and operator-action state slices. | Every challenge lifecycle and terminal transition is covered by generated traces. |
| `v0.32.2` | CSR/finalization/certificate download/verification state slices including unknown outcomes. | Certificate cannot advance to verified without all prior evidence; reconciliation traces pass. |
| `v0.32.3` | Deployment/renewal/completion, cancellation, recoverable/terminal failure, and cleanup-required state slices. | Terminal-state and cancellation/cleanup precedence properties pass. |
| `v0.33.0` | Canonical serializable snapshots, revisions, schema identifiers, forward migration contract, and unknown-field policy. | Round-trip, version skew, corrupt snapshot, and migration fixture suite passes. |
| `v0.33.1` | Effect IDs and persist-before-effect transactional outbox with once-only result application. | Crash/restart after every persist/execute/result boundary is safe. |
| `v0.33.2` | Operation-specific unknown-outcome reconciliation and policy decision records. | Lost response simulations never convert uncertainty into false success or blind retry. |
| `v0.33.3` | Cross-version snapshot compatibility and migration harness using retained snapshots from every released schema revision. | Current readers replay every supported historical snapshot; incompatible, corrupt, downgrade, forward-version, and migration-chain cases fail according to the published policy. |
| `v0.34.0` | Store transaction/load/commit/compare-and-swap traits and in-memory reference implementation. | Stale/replayed writes and atomicity model tests pass. |
| `v0.34.1` | Lease, fencing-token, challenge-ownership, and single-flight store traits. | Lease theft, expiry, stale owner, and fencing interleavings fail safely. |
| `v0.34.2` | Encrypted-field/key-reference boundary and tenant/intent/account namespace isolation. | Ciphertext/key-reference substitution and cross-namespace access tests pass. |
| `v0.35.0` | Complete in-memory store, outbox, leases, cleanup queue, deterministic clock behavior, and fault hooks. | Reference-store conformance suite covers every store trait and fault. |
| `v0.35.1` | Durable filesystem snapshot/journal store with restrictive permissions and symlink/reparse-point-safe paths. | Cross-platform path/race/permission and corrupt/truncated journal tests pass. |
| `v0.35.2` | Filesystem store fsync/atomicity, crash recovery, backup/restore, and schema migration. | Power-loss injection at every write/rename/fsync/migration stage passes. |
| `v0.36.0` | Filesystem deployment staging with bounded files, ownership/mode/ACL policy, safe paths, fsync, and atomic certificate/key generation layout. | No crash/race exposes partial or mismatched active material. |
| `v0.36.1` | Deployment generation activation, stale-worker fencing, previous-generation retention, and deterministic rollback. | Stale activation and rollback-after-failure matrices pass. |
| `v0.36.2` | Service reload callback/control-channel interface and post-activation certificate/key/TLS health evidence. | Failed/hung/replayed reload and health checks trigger correct rollback without losing the serving generation. |
| `v0.37.0` | Stable low-level workflow loop, typed effects/events, executor traits, and checkpoint contract. | Fake executor covers every effect/result and rejects unauthorized effects. |
| `v0.37.1` | High-level `ensure_certificate`, begin/resume/status/cancel, idempotent intent, and result APIs. | End-to-end fake platform covers success, recovery, cancellation, and every typed terminal outcome. |
| `v0.37.2` | Manual challenge workflow, operator instructions/evidence, confirmation, cleanup, and resume. | Manual-flow misuse, stale confirmation, restart, and cleanup tests pass. |
| `v0.37.3` | High-level account/contact/rollover/deactivation, revoke, renew-now, and ARI inspection API shells over completed protocol operations. | Compile/API misuse and behavior tests cover every public method without placeholder success. |
| `v0.38.0` | Minimal deterministic in-house ACME test server implementing successful RFC 8555 directory/account/order/HTTP-01/finalization/retrieval/revocation paths. | Full local happy-path lifecycle is reproducible with no external service. |
| `v0.38.1` | Fault-injection response catalog: malformed/bounded HTTP/JSON/PEM/DER, nonce, URL, content-type, header, state, clock, and chain failures. | Every catalog fault has a client assertion and cannot panic. |
| `v0.38.2` | Ambiguous-outcome/crash/distributed fault server: lost responses, delayed effects, repeated operations, worker death, and lease theft. | Restart after every transition/effect produces the modeled safe outcome. |
| `v0.39.0` | Pinned Pebble integration for directory, account, order, HTTP-01, finalization, retrieval, revocation, and pagination. | Zero skipped mandatory RFC 8555 happy-path cases supported by Pebble. |
| `v0.39.1` | Pebble randomized-state, badNonce, alternate behavior, retry, and order-list robustness suite. | Repeated seeded runs are reproducible and all expected variants pass. |
| `v0.39.2` | Prior-release differential protocol harness comparing normalized requests, responses, state transitions, errors, and security decisions with retained Vardheim release evidence. | Every unexplained wire or semantic difference blocks release; approved corrections preserve both the old regression case and the newly required result. |

## Phase 5 - Renewal, DNS, And TLS-ALPN

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.40.0` | RFC 9773 ARI identifiers, unauthenticated renewal-info GET, suggested-window validation, explanation URL handling without auto-fetch, Retry-After, and replacement links. | RFC vectors and malformed AKI/serial/window/URL/server-response tests. |
| `v0.41.0` | Durable ARI renewal state and cryptographically random time selection persisted within a validated suggested window. | Injectable RNG/clock properties prove selected times remain stable across restart and within the window. |
| `v0.41.1` | Non-ARI fallback scheduling, jitter, emergency threshold, clock-skew detection, retry checks, replacement/expiry/revocation stop conditions. | Failure/skew/restart properties prove no missed emergency renewal or renewal storm. |
| `v0.42.0` | DNS-01 calculation and provider trait with exact TXT value, normalized owner, record handle/lease, concurrent-value preservation, and exact cleanup. | RFC vectors and properties proving concurrent workflows cannot remove unrelated TXT values. |
| `v0.43.0` | Authoritative zone and server discovery with label walking, CNAME/NS delegation representation, and bounded loop detection. | Delegation loops, lame/missing zones, split authority, and malformed response fixtures pass. |
| `v0.43.1` | DNS-01 propagation checks against every authoritative server over IPv4/IPv6 with explicit partial/complete visibility evidence. | Partial propagation, inconsistent answers, timeout, truncation/TCP fallback, and unreachable-family matrix passes. |
| `v0.43.2` | TTL, negative-caching, bounded wait/backoff, recursive comparison, and self-check deadline policy. | NXDOMAIN/NODATA cache and stale/early visibility simulations cannot report false global readiness. |
| `v0.44.0` | DNSSEC-aware self-check with explicit secure/insecure/bogus/indeterminate results and operator policy. | Signed, unsigned, broken-chain, rollover, denial-of-existence, downgrade, and clock-skew fixtures. |
| `v0.44.1` | Pinned Pebble/challtestsrv DNS-01 integration over the completed DNS presentation and propagation boundaries. | Complete DNS-01 issuance, concurrent TXT, delegation, cleanup, and failure paths pass. |
| `v0.45.0` | RFC 2136 DNS provider adapter with TSIG/key boundary, zone restrictions, prerequisites, exact update/delete, and retry classification. | Authoritative integration suite plus wrong-zone, privilege, replay, partial update, and cleanup recovery tests. |
| `v0.46.0` | Cloudflare DNS adapter with narrowly scoped credentials, pagination, exact record IDs, rate limits, and redacted errors. | Mock and controlled integration tests for duplicate values, partial failures, revoked credentials, quotas, and cleanup. |
| `v0.47.0` | AWS Route 53 adapter isolated from core, including hosted-zone resolution, change polling, credential-provider boundary, and exact cleanup. | Local/mocked AWS protocol suite and opt-in controlled integration; dependency and SDK admission report. |
| `v0.48.0` | Azure DNS adapter isolated from core, including zone/resource IDs, identity boundary, ETags/concurrency, and exact cleanup. | Mock Azure protocol suite and opt-in controlled integration; dependency and SDK admission report. |
| `v0.49.0` | Remote least-privilege DNS validation agent wire protocol with authenticated capability requests, restricted names/values, expiry, replay defense, and audit receipts. | Protocol properties prove requests cannot authorize account access, issuance, or unrelated DNS edits. |
| `v0.49.1` | Reference DNS agent executor, enrollment/credential rotation boundary, provider mapping, recovery, and hostile-network integration. | Compromise scenarios prove least privilege; disconnect/replay/expiry and cleanup recovery pass. |
| `v0.50.0` | TLS-ALPN-01 identity construction per RFC 8737: dedicated ephemeral key handle, one SAN, critical `acmeIdentifier`, SHA-256 digest, and exact certificate profile. | RFC vectors plus wrong SAN/extension/criticality/digest/key negatives pass. |
| `v0.50.1` | TLS challenge identity store, expiry, presentation ownership, self-verification, and durable cleanup. | Concurrent/expired/stale-owner/crash cleanup cases cannot affect normal certificate identities. |
| `v0.51.0` | `vardheim-rustls` exact `acme-tls/1` SNI/ALPN challenge resolver with no normal-certificate fallback. | Handshake, concurrency, SNI confusion, ALPN downgrade, expired identity, and normal-traffic isolation tests pass. |
| `v0.51.1` | Pinned Pebble/challtestsrv TLS-ALPN-01 end-to-end integration through `vardheim-rustls`. | Successful issuance, invalid identity, cleanup, restart, and concurrent normal TLS traffic pass. |
| `v0.51.2` | rustls live certificate generation/reload consumer interface, SNI table update, activation health evidence, and rollback integration. | First issuance and renewal activate without process restart; failure leaves the prior SNI certificate serving. |
| `v0.51.3` | OpenSSL TLS-ALPN presentation adapter behind the same challenge identity contract, isolated from core. | OpenSSL handshake/SNI/ALPN/cleanup and normal-certificate isolation suite passes. |

## Phase 6 - Transport And Cryptographic Backends

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.52.0` | Transport request/response traits, body/header budgets, connect/write/read/total deadlines, cancellation, and deterministic fake transport. | Slowloris, oversized response, timeout phase, cancellation, and budget tests pass. |
| `v0.52.1` | HTTPS/TLS trust policy, custom roots, platform roots, minimum protocol, certificate/SPKI pinning, and peer identity evidence. | Wrong root/name/pin/version and trust-store failure matrices pass. |
| `v0.52.2` | Proxy authentication boundary, origin authorization enforcement, disabled bounded decompression policy, redirect prohibition, correlation, and credential-leak prevention. | Malicious proxy, redirect, decompression bomb, SSRF, cross-origin, and proxy credential tests pass. |
| `v0.53.0` | Tokio + hyper + rustls asynchronous transport with explicit executor construction and cancellation semantics. | Loopback and hostile-server integration on Linux, Windows, BSD, macOS, Android, and iOS-capable CI tiers. |
| `v0.53.1` | Reqwest asynchronous transport adapter with strict redirect/decompression/proxy policy parity and explicit rustls/native TLS construction. | Differential transport suite proves policy-equivalent requests, errors, limits, cancellation, and origin enforcement against hyper. |
| `v0.54.0` | Blocking ureq-compatible transport with strict policy parity and explicit rustls construction. | Blocking timeout/cancellation/resource/redirect/origin tests pass. |
| `v0.54.1` | Native TLS blocking transport option isolated outside core, with platform roots and identity-policy parity. | Native-root/hostname/proxy/timeout behavior passes across supported desktop operating systems. |
| `v0.55.0` | Embedded/custom transport adapter and allocation-bounded response handoff for kernels, firmware, and future custom operating-system targets. | Host-free compile profiles, caller-buffer exhaustion tests, deterministic fake transport, and no hidden runtime assumptions. |
| `v0.56.0` | Explicit account signer, certificate key factory, ephemeral challenge key, EAB MAC, authority-token, audit, and storage-encryption roles. | Type/API tests prevent account/leaf/key-purpose reuse; all handles redact. |
| `v0.56.1` | Key/signer capability negotiation across local provider, CA support, operator policy, certificate profile, and signature purpose. | Server-driven algorithm choice and downgrade matrices fail closed. |
| `v0.56.2` | Entropy interface and key-generation request semantics with purpose, algorithm, exportability, attestation, and failure provenance. | Deterministic entropy/exhaustion/reuse/failure tests pass without hidden global RNG assumptions. |
| `v0.56.3` | Bounded SPKI/PKCS#8 import/export policy, key/algorithm verification, redacted errors, and format-version handling. | Malformed/wrong algorithm/private-public mismatch/unsupported-format corpus passes. |
| `v0.56.4` | Encrypted software-key envelope, password/key-provider boundary, atomic account-key persistence, key versioning/rotation, backup, and recovery. | Wrong password/purpose/version, crash, permission, rollback, backup, and key substitution cases pass. |
| `v0.57.0` | RustCrypto baseline ES256 account/CSR backend with entropy, key import/generation, JOSE raw signature conversion, and zeroization integration. | Official ES256/JWK/JWS/CSR vectors, malformed signature/key rejection, leakage review, and dependency admission pass. |
| `v0.57.1` | RustCrypto RSA/RS256 backend and bounded key-size/exponent policy. | RSA vectors, weak/oversized key, padding, algorithm-confusion, and resource tests pass. |
| `v0.57.2` | RustCrypto Ed25519/EdDSA backend where supported by ACME provider policy. | Official/differential vectors and unsupported-combination tests pass. |
| `v0.57.3` | RustCrypto P-384/ES384 backend where supported by ACME provider policy. | Official/differential vectors and coordinate/signature conversion tests pass. |
| `v0.57.4` | RustCrypto P-521/ES512 backend where supported by ACME provider policy. | Official/differential vectors, unusual bit-width, and conversion tests pass. |
| `v0.58.0` | ring backend in its own implementation boundary with explicit selection and no feature-unification ambiguity. | Cross-backend JWK/JWS/CSR vectors, unsupported algorithm fail-closed behavior, platform matrix, and dependency review. |
| `v0.59.0` | aws-lc-rs non-FIPS backend with explicit provider health, approved local policy set, and no silent fallback. | Cross-backend vectors, platform/native build matrix, provider failure tests, SBOM/native dependency evidence, and audit. |
| `v0.60.0` | Separate AWS-LC FIPS deployment package/profile with exact module line, runtime `fips_status`, compliance manifest, approved algorithms, supported environments, and fail-closed startup. | Dedicated supported-target CI proves provider status and negative fallback; independent FIPS configuration review. |
| `v0.61.0` | PKCS#11 module/session/object discovery, key-handle identity, PIN/credential policy, and mechanism capabilities. | SoftHSM wrong module/slot/object/PIN and mechanism confusion tests pass. |
| `v0.61.1` | PKCS#11 signing, concurrency/session pooling, unavailable-token recovery, non-exportability, and lifecycle integration. | Session loss/login races/token removal/retry/redaction integration passes. |
| `v0.62.0` | TPM 2.0 persistent handle, key creation/loading, policy session, signing, and non-exportability. | Software TPM wrong handle/policy/algorithm/lockout tests pass. |
| `v0.62.1` | TPM reset/recovery, attestation evidence boundary, interrupted operations, key rotation, and lifecycle integration. | Reset/lockout/attestation/recovery integration passes. |
| `v0.63.0` | AWS KMS signer/key provider with algorithm mapping, public-key verification, grant/identity policy, retry/reconciliation, and no private export. | Mock and controlled AWS integration, throttling, ambiguous signing, revoked grant, region/account confusion, and SDK review. |
| `v0.64.0` | Azure Key Vault signer/key provider with versioned key IDs, algorithm mapping, identity policy, retry/reconciliation, and no private export. | Mock and controlled Azure integration, version rollover, throttling, revoked identity, tenant confusion, and SDK review. |
| `v0.65.0` | OpenBao-compatible remote signer/key provider with authenticated transport, mount/key/version binding, capability policy, and secret-safe errors. | Dev-server integration, wrong mount/version, token expiry, replay, network ambiguity, and authorization tests. |
| `v0.66.0` | Generic authenticated remote signer protocol, request purpose authorization, key capabilities, replay defense, and signed audit receipts. | Compromised-client scenarios prove forbidden purposes/keys fail; disconnect/replay/reordering tests pass. |
| `v0.66.1` | Reference remote signer agent, enrollment/rotation/revocation, availability/reconciliation, and least-privilege deployment. | Hostile-network and compromised-agent/client integration passes. |
| `v0.66.2` | Offline account-key rollover ceremony package, human-verifiable transcript, dual authorization, resume/abort, and recovery. | Interrupted/swapped/replayed/partially approved ceremony fixtures fail safely. |

## Phase 7 - Web PKI Extensions And Provider Profiles

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.67.0` | RFC 8657 account-URI and validation-method parameter syntax, normalization, account binding, and policy model. | Published vectors and malformed/duplicate/unknown parameter tests pass. |
| `v0.67.1` | RFC 8659 advisory CAA preflight for `issue`/`issuewild`, aliases, DNSSEC states, and CA advertised identities. | Deny/allow/indeterminate vectors pass without claiming CA-equivalent validation. |
| `v0.68.0` | RFC 8738 IP identifier orders for IPv4/IPv6 with HTTP-01 and TLS-ALPN-01, canonical bytes, CSR/certificate binding, and DNS-01 prohibition. | RFC vectors and cross-family, textual alias, SAN type, wildcard, forbidden challenge, and route-policy tests. |
| `v0.69.0` | Advertised capability extraction and versioned signed provider-profile schema for documented product behavior. | Schema fuzzing/signature/version and no-provider-name-branching checks pass. |
| `v0.69.1` | Expiring observed-capability cache with provenance, confidence, invalidation, and no security-policy override. | Stale/conflicting/spoofed observations cannot weaken policy. |
| `v0.69.2` | Operator capability/product policy precedence and typed unsupported taxonomy across standard/client/crypto/CA/operator/product causes. | Full precedence matrix returns stable exact reasons. |
| `v0.69.3` | Provider-observation record/replay corpus for directory metadata, advertised/observed capabilities, quirks, rate behavior, and redacted failure shapes. | Current code replays every retained provider observation; drift reports distinguish provider change, standard change, deliberate client correction, and regression. |
| `v0.70.0` | Let's Encrypt staging profile and conformance: directory changes, challenge behavior, ARI, rate-limit handling, alternate chains, and controlled production opt-in smoke. | Pinned staging suite, account/order lifecycle, all supported challenges, ARI, revocation, and no default production traffic. |
| `v0.71.0` | EAB-required commercial-CA profile and controlled conformance for product restrictions, quotas/payment/operator actions, challenge availability, and wildcard policy. | Controlled integration evidence, profile-vs-advertised conflict tests, and no embedded provider special cases. |
| `v0.71.1` | Production web-server adoption contract and reference migration from an existing `instant-acme`-style client: issuer/account import, EAB, HTTP-01/TLS-ALPN-01/DNS-01 selection, renewal queue/status, atomic install, live reload, rollback, and redacted metrics. | A Fluxheim integration fixture replaces its client boundary and proves first issuance, due renewal, account rollover, revocation, failure continuity, and zero-restart SNI activation. |
| `v0.71.2` | Regulated web-server profile using the AWS-LC FIPS signer/CSR/TLS challenge/transport path with machine-readable boundary evidence. | FIPS-required configuration fails closed on any non-validated ACME crypto path and passes the web-server lifecycle fixture on supported environments. |

## Phase 8 - Every Published Specialist ACME RFC

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.72.0` | RFC 8739 STAR directory/order fields, lifetime/date policy, recurrent certificate retrieval model, and strict separation from ordinary orders. | Section-level encoding/parsing and invalid lifetime/date fixtures pass. |
| `v0.72.1` | STAR recurrent retrieval, cancellation, expiry, renewal scheduling, persistence, and crash recovery. | Timing/restart/cancellation/expiry fault suite passes. |
| `v0.73.0` | RFC 8823 email identifier normalization, S/MIME CSR/certificate profile, address binding, and capability model. | Address/canonicalization/profile/identifier substitution fixtures pass. |
| `v0.73.1` | `email-reply-00` presentation/evidence, MIME/message validation, replay/spoofing defense, manual workflow, and cleanup. | RFC fixtures and malformed/replayed/spoofed message recovery suite passes. |
| `v0.74.0` | RFC 9115 delegation metadata, credentials, CSR templates/extensions, order fields, and authorization boundaries. | Encoding/profile/confused-deputy and scope fixtures pass. |
| `v0.74.1` | Delegated STAR issuance, recurrent retrieval, termination/revocation, duplicate handling, persistence, and crash recovery. | Expired/unknown delegation, duplicate request, revocation, and restart suite passes. |
| `v0.75.0` | RFC 9444 subdomain authorization and policy integration, including delegation limits and identifier-set binding. | RFC vectors, parent/child confusion, scope escalation, wildcard interaction, expiry, and revocation tests. |
| `v0.76.0` | RFC 9447 authority-token challenge framework, token-type registry, typed request/evidence, issuer/purpose policy, and extension API. | RFC encoding and unknown/unsupported token-type fixtures pass. |
| `v0.76.1` | JWT authority-token profile using RFC 7519/8725 algorithm/audience/expiry/issuer/subject constraints and replay defense. | JWT algorithm, audience, expiry, substitution, nested-token, and replay corpus passes. |
| `v0.77.0` | RFC 9448 TNAuthList authority-token profile, identifier normalization, certificate profile, and `tkauth-01`. | RFC fixtures, range/canonicalization, token binding, profile mismatch, and authorization aggregation tests. |
| `v0.78.0` | RFC 9799 `.onion` identifier parsing, version/checksum/key binding, in-band CAA fields/policy, and CSR/certificate profile. | RFC identifier/CAA/profile and key mismatch fixtures pass. |
| `v0.78.1` | `onion-csr-01` challenge construction, CSR evidence, replay/expiry handling, workflow persistence, and cleanup. | CSR substitution/replay/expiry/restart/cleanup suite passes. |
| `v0.79.0` | RFC 9891 DTN `bundleEID` identifier normalization, certificate SAN/profile rules, and capability model. | RFC endpoint/profile and malformed identifier fixtures pass. |
| `v0.79.1` | `bp-nodeid-00` presentation/evidence, validation workflow, replay/timeout policy, persistence, and cleanup. | Evidence binding/replay/timeout/restart/cleanup suite passes. |
| `v0.80.0` | NfInstanceId registry/profile support with `tkauth-01`, isolated external-profile mapping, typed capability result, and certificate checks. | Registry fixtures, profile revision pin, identifier/token mismatch, unsupported-profile, and extension round-trip tests. |
| `v0.81.0` | Stable extension registration API for directory, identifier, challenge, order, and problem values with bounded unknown retention and conflict prevention. | All published extensions register concurrently; duplicates, known-field override, unstable ordering, and resource attacks fail. |

## Phase 9 - Production Stores, Deployment, And Operations

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.82.0` | SQLite schema, migrations, account/job/certificate/audit persistence, transactions, and CAS revisions. | Real database transaction/lock/migration and store-conformance suites pass. |
| `v0.82.1` | SQLite outbox, leases/fencing, encrypted-field references, single-node scheduling, and cleanup queue. | Lease/outbox/crash and ciphertext-reference fault injection passes. |
| `v0.82.2` | SQLite corruption detection, online backup, restore, migration rollback, and disaster recovery runbook. | Corrupt/truncated/locked database and backup/restore drills pass. |
| `v0.83.0` | PostgreSQL schema/migrations, transactions, CAS revisions, and store-conformance baseline. | Isolation-level, lock, migration, and compatibility suite passes. |
| `v0.83.1` | PostgreSQL transactional outbox, leases, fencing, account/intent concurrency, and cleanup queues. | Multi-worker stale leader and exactly-once-application interleavings pass. |
| `v0.83.2` | PostgreSQL HA failover, network partitions, connection recovery, migration rollback, backup/restore, and bounded load. | Multi-node failover/partition/restore/load suite passes without duplicate activation. |
| `v0.84.0` | Tenant identity/authorization boundaries and row/key namespace isolation across accounts, jobs, keys, deployments, and audit events. | Cross-tenant access/property and confused-deputy tests pass. |
| `v0.84.1` | Per-tenant encryption-key references, rotation, deletion/crypto-shredding policy, and backup implications. | Key rotation/wrong-key/deleted-key/restore cases are explicit and safe. |
| `v0.84.2` | Tenant quotas, account concurrency/rate policy, intent single-flight, noisy-neighbor backpressure, and fair scheduling. | Quota races, starvation, overload, and duplicate intent properties pass. |
| `v0.85.0` | Nginx filesystem/config-test/reload/health/rollback deployment adapter. | Real Nginx failed reload, stale generation, permission, and rollback tests pass. |
| `v0.85.1` | Apache filesystem/config-test/reload/health/rollback deployment adapter. | Real Apache failed reload, stale generation, permission, and rollback tests pass. |
| `v0.85.2` | HAProxy runtime/file activation, health verification, generation fencing, and rollback deployment adapter. | Real HAProxy reload/runtime failure and rollback tests pass. |
| `v0.85.3` | systemd credentials/path/timer/service notification deployment adapter with atomic generations and rollback. | Real systemd credential permission, reload, restart, stale generation, and rollback tests pass. |
| `v0.86.0` | Kubernetes Secret deployment with resource versions, server-side conflict policy, immutable options, rollout verification, rollback, and least-privilege RBAC. | Kind integration, conflict/partition/watch loss, namespace isolation, RBAC denial, stale worker, and rollback tests. |
| `v0.87.0` | Generic in-process deployment callback contract with generation fencing, health evidence, timeout/cancellation, and rollback. | Failed/hung/replayed callbacks and stale generation tests pass. |
| `v0.87.1` | Authenticated remote deployment agent protocol with target-scoped capabilities, replay defense, generation fencing, and key-material policy. | Protocol and compromised-client scope tests pass. |
| `v0.87.2` | Reference remote deployer, partition recovery, health evidence, rollback, and hostile-network integration. | Compromised/partitioned agent tests prove containment and correct rollback. |
| `v0.88.0` | Redacted structured lifecycle event model and identifier privacy modes with stable event schemas. | Snapshot/redaction tests prove no secret fields leak. |
| `v0.88.1` | Tracing and metrics traits, bounded labels/cardinality, queue/renewal/deployment health, and exporter failure isolation. | Cardinality, backpressure, exporter failure, and redaction tests pass. |
| `v0.88.2` | Audit records and canonical serialization with actor/tenant/effect/deployment provenance. | Complete event provenance and secret-exclusion tests pass. |
| `v0.88.3` | Signed hash-linked audit log, key rotation, checkpoints, verification, export, and retention. | Tamper/deletion/reordering/truncation/rotation/signature tests pass. |
| `v0.89.0` | Read-only CLI for directory/account/order/certificate/ARI/policy/status inspection and safe human/machine output. | Golden output, schema, corruption, and redaction tests pass. |
| `v0.89.1` | Mutating CLI for account operations, begin/resume/cancel/manual challenge, renew-now, revocation, and confirmation gates. | Command misuse, confirmation, cancellation, resume, and interrupted mutation tests pass. |
| `v0.89.2` | CLI configuration/profile validation, shell completion, exit-code contract, signal handling, and automation compatibility. | Cross-platform invocation and stable exit/output contract tests pass. |
| `v0.90.0` | Single-node daemon process, configuration, worker supervision, health/readiness, graceful shutdown, and SQLite profile. | Restart/kill/config failure and long-running single-node soak tests pass. |
| `v0.90.1` | Durable renewal scheduling, cleanup workers, backpressure, live safe configuration reload, and operational controls. | Clock/queue/reload/overload and shutdown drain tests pass. |
| `v0.90.2` | PostgreSQL HA daemon profile, leader/lease behavior, rolling upgrades, partitions, and multi-replica observability. | Leader changes, network partition, stale replica, rolling upgrade, and soak tests pass. |
| `v0.91.0` | Remote validation/deployment agent enrollment and least-privilege reference packaging. | Enrollment, expired credential, target scope, and package permission tests pass. |
| `v0.91.1` | Agent credential/key rotation, revocation, re-enrollment, lost-state recovery, and operator audit. | Rotation/revocation/recovery and hostile-network tests pass. |
| `v0.91.2` | Agent protocol-version compatibility, signed upgrades, rollback, system packages/containers, and deployment hardening. | Upgrade/rollback/tamper/old-new compatibility and compromised-node exercises pass. |

## Phase 10 - Platform, Formal Assurance, And Draft Isolation

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.92.0` | Linux target qualification for core, transports, filesystems, rustls/OpenSSL, stores, agents, clocks, entropy, permissions, services, and packages. | Native Linux CI and target-specific security evidence passes. |
| `v0.92.1` | Android target qualification for core and supported adapters, Keystore integration boundary, roots, clocks, entropy, storage, and lifecycle constraints. | Device/emulator CI and explicit unsupported-profile evidence passes. |
| `v0.92.2` | Windows target qualification including reparse-safe paths, ACLs, atomic replacement, certificate roots, services, clocks, entropy, and process behavior. | Native Windows integration and security evidence passes. |
| `v0.92.3` | macOS and iOS target qualification including APFS/symlink/ACL behavior, Keychain/key-provider boundaries, roots, clocks, entropy, launch/runtime integration. | Native macOS plus documented device/simulator iOS evidence passes. |
| `v0.92.4` | FreeBSD, OpenBSD, NetBSD, and DragonFly BSD qualification for core and supported std adapters. | Native/cross CI and explicit unsupported-adapter failure evidence passes for each BSD. |
| `v0.92.5` | Cross-target feature/profile parity audit and support-tier publication for every crate/backend/adapter combination. | Machine-readable target matrix matches CI and unsupported profiles fail at compile/config time. |
| `v0.92.6` | Release-to-release target/profile regression matrix covering compile support, feature resolution, runtime probes, filesystem semantics, and platform security decisions. | Every previously supported cell is compared with the prior release; removals or weaker evidence block release unless explicitly approved as a documented breaking change. |
| `v0.93.0` | Future custom-operating-system readiness: no_std low-level API audit, caller-provided alloc/clock/entropy/transport/signer/storage interfaces, C ABI exclusion policy, and porting guide. | A freestanding reference target compiles core/challenge crates and replays a complete deterministic issuance trace with fake effects. |
| `v0.94.0` | Kani proofs for budgets, identifier/intent normalization, JWS exclusivity, and nonce ownership. | Harnesses pass at published bounds with assumptions/non-proven properties documented. |
| `v0.94.1` | Kani proofs for protocol/workflow transition legality, retry termination, authorization aggregation, and terminal states. | Harnesses pass at published bounds and replay generated counterexamples as Rust tests. |
| `v0.94.2` | Kani proofs for cleanup ownership, leases/fencing, deployment activation, and chain selection invariants. | Harnesses pass at published bounds with environmental assumptions explicit. |
| `v0.95.0` | Loom models for nonce queues, challenge presentation stores, and cancellation races. | All modeled interleavings pass without reuse, deadlock, or lost cleanup. |
| `v0.95.1` | Loom models for job/account leases, fencing, outbox application, and rate limiting. | All interleavings pass without stale activation or duplicate result application. |
| `v0.95.2` | Loom models for deployment reload/rollback, scheduler/cleanup queues, and shutdown races. | All interleavings pass without mismatched generations or abandoned cleanup. |
| `v0.96.0` | Full parser/protocol fuzz program for JSON, JOSE/JWK, PEM/DER/CSR, links, Retry-After, URLs, IDNA, extensions, and profiles with seed/reproduction policy. | Minimum fuzz durations complete with zero unresolved crashes and every crash becomes a regression. |
| `v0.96.1` | Miri program for every applicable safe crate, store model, and challenge ownership path. | Miri matrix is clean or has documented tool limitations with alternate evidence. |
| `v0.96.2` | Native/FFI sanitizer program for crypto, PKCS#11, TPM, OpenSSL, database, and platform adapters. | ASan/UBSan/TSan profiles are clean on supported targets. |
| `v0.96.3` | Timing/leakage evidence program for secret comparisons, software signers, key parsing, and redaction boundaries. | Published methodology/results meet defined thresholds without overstating constant-time guarantees. |
| `v0.97.0` | TLA+/Quint issuance/finalization/certificate verification/cancellation model with Rust trace replay. | Model checking and valid/invalid trace parity pass. |
| `v0.97.1` | Account rollover and challenge presentation/cleanup model with Rust trace replay. | Model checking and crash/retry trace parity pass. |
| `v0.97.2` | Lease/outbox/deployment activation/rollback/renewal model with Rust trace replay. | Partition/stale-worker/crash trace parity passes. |
| `v0.97.3` | Historical formal-model and generated-trace replay across all retained model revisions. | Current Rust behavior accepts every still-valid historical trace and rejects every retained invalid trace; model changes produce reviewed trace-level diffs. |
| `v0.100.0` | Experimental standards framework: exact draft-revision metadata/naming, default-off registration, fixture isolation, API instability policy, compatibility rules, active/expired/replaced classification, and promotion/retirement process. | Tests prove drafts cannot activate implicitly, override stable registrations, advance revision without an explicit package/API change, or remain claimed after expiry/replacement unnoticed. |
| `v0.101.0` | Exact-revision ACME certificate profiles draft implementation, including directory metadata, order selection, capability policy, and certificate verification binding. | Revision-specific fixtures, unknown profile behavior, downgrade/mismatch tests, and no stable API leakage. |
| `v0.102.0` | Exact-revision persistent DNS validation draft implementation with authorization lifetime, reuse, revocation, and cleanup policy. | Revision-specific lifecycle, stale authorization, takeover, policy downgrade, and crash-recovery tests. |
| `v0.103.0` | Exact-revision DNS account-label draft implementation with account binding, label derivation, delegation, rotation, and cleanup. | Revision-specific vectors plus collision, cross-account, rollover, downgrade, and DNS delegation attacks. |
| `v0.104.0` | Exact-revision device-attestation draft implementation with attestation format/provider boundary, challenge binding, freshness, and privacy policy. | Revision-specific fixtures plus replay, substituted device/key, untrusted root, malformed evidence, and privacy tests. |
| `v0.105.0` | Exact-revision RATS draft implementation with evidence/appraisal interfaces, nonce binding, endorsements, reference values, and result policy. | Revision-specific fixtures plus replay, stale endorsement, verifier confusion, ambiguous appraisal, and resource limits. |
| `v0.106.0` | Exact-revision authority-token constraints draft implementation extending the stable authority-token model without weakening RFC 9447/9448 behavior. | Revision-specific token vectors, constraint precedence, downgrade, audience/scope escalation, and stable/draft coexistence tests. |
| `v0.107.0` | Exact-revision quantum-ready ACME TLS/JWS profile draft with hybrid/PQ algorithm identifiers, key-provider capabilities, transport/signing policy, and size budgets. | Revision-specific vectors, downgrade, oversized key/signature, provider mismatch, hybrid binding, and interoperability tests. |
| `v0.108.0` | Exact-revision public-key challenge draft implementation with proof construction, key/identifier/account binding, replay defense, and cleanup lifecycle. | Revision-specific vectors plus substituted key/account/identifier, replay, downgrade, unsupported algorithm, and state recovery tests. |
| `v0.109.0` | Exact-revision ACME integrations for device certificate enrollment, including EST/BRSKI integration roles, challenge delegation, CSR attributes, trust boundaries, and operational flow. Promote to the published-RFC phase if it exits the RFC Editor queue first. | Revision-specific interop diagrams/fixtures, confused-deputy, delegated validation, wrong RA/CA, and enrollment recovery tests pass. |
| `v0.110.0` | Exact-revision identity-controlled validation draft with identity-provider trust/configuration, identifier binding, token/privacy policy, replay defense, and failure semantics. | Revision-specific issuer/audience/identifier/account binding, substitution, replay, privacy, and outage tests pass. |
| `v0.111.0` | Exact-revision post-quantum cryptographic-agility profile with negotiation, downgrade resistance, algorithm lifecycle, CSR/certificate binding, and migration policy. | Revision-specific agility/downgrade/hybrid/classical transition and interoperability tests pass. |

## Phase 10.5 - Release-To-Release Regression Freeze

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.119.0` | Previous-release compatibility gate for public Rust API, feature graph, wire semantics, serialized state/migrations, configuration, CLI machine output, and documented support claims. | The candidate is mechanically compared with the latest release and every retained historical corpus; all differences are either absent or linked to an approved requirement, migration, regression test, and release note. |
| `v0.119.1` | Final live-upstream drift assessment against the pinned RFC/IANA/profile/draft and provider-observation baselines. | A signed review classifies every live difference and assigns required work to a pre-1.0 version; no drift is silently accepted or allowed to make offline release tests non-reproducible. |

## Phase 11 - Production Qualification

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.120.0-alpha.1` | Full API completeness and freeze candidate: no unversioned TODOs, no placeholder functions, complete docs/examples, stable error taxonomy, feature matrix, migration guide, and performance budgets. | Public API review, documentation tests, semver checks, zero uncovered public functions/branches under the documented coverage policy. |
| `v0.120.0-alpha.2` | Core interoperability matrix: in-house CA, Pebble, Boulder subset, RFC 8555, Web PKI extensions, staging providers, and controlled commercial provider. | Reproducible reports have no skipped mandatory core/Web PKI cases and classify provider limitations. |
| `v0.120.0-alpha.3` | Specialist RFC/draft and challenge-method interoperability matrix. | Every published extension and enabled exact draft revision has pinned reproducible evidence. |
| `v0.120.0-alpha.4` | Backend/store/deployer/web-server interoperability matrix across crypto, transports, DNS providers, databases, HSM/KMS, agents, and target profiles. | Pairwise profile reports have no unexplained skips or configuration-dependent backend choice. |
| `v0.120.0-beta.1` | Resource-exhaustion qualification: CPU/memory/body/header/identifier/queue budgets, backpressure, rate control, and bounded concurrency. | Load/soak tests meet published budgets without secret leakage or unbounded growth. |
| `v0.120.0-beta.2` | Resilience/disaster qualification: DNS/CA/KMS/database outages, partitions, clock faults, process/host loss, backup restore, and incident runbooks. | Chaos/restore exercises preserve safe state and serving certificate continuity. |
| `v0.120.0-beta.3` | Supply-chain and release qualification: cargo-vet policy, reproducible builds, signed provenance/tags, SBOM verification, tool/action freshness, packaging, and dependency freeze review. | Two clean builders reproduce artifacts; vet/deny/audit/provenance/SBOM gates pass. |
| `v0.120.0-rc.1` | Independent parser/JOSE/nonce/protocol-core security audit and remediation. | Exact-commit PASS report and permanent regression tests exist. |
| `v0.120.0-rc.2` | Independent workflow/policy/PKIX/storage/deployment security audit and remediation. | Exact-commit PASS report and permanent regression tests exist. |
| `v0.120.0-rc.3` | Independent crypto/FIPS/transport/DNS/TLS/KMS/agent/platform adapter audit and remediation. | Exact-commit PASS report and permanent native/remote regression tests exist. |
| `v0.120.0-rc.4` | FIPS production-profile qualification on supported environments, exact validated-module documentation, operator evidence bundle, and no-fallback verification. | Independent compliance review and automated runtime/configuration evidence precisely match validated boundaries. |
| `v0.120.0-rc.5` | Final release candidate: frozen APIs, complete manuals, upgrade/rollback rehearsal, all target profiles/RFC tiers/artifacts, and no known critical/high findings. | Full release gate twice from clean environments plus final independent pentest of the exact candidate commit. |
| `v1.0.0` | First serious production-ready Vardheim release: complete RFC 8555, Web PKI tier, every published specialist ACME RFC, all planned runtime/crypto/FIPS/store/deployment/operations/platform boundaries, and isolated experimental drafts. | Final 1.0 audit and pentest PASS, all matrices green, reproducible signed artifacts, verified SBOM/provenance, and maintainer authorization to tag/publish. |

## Completeness Register

The following requirements are deliberately assigned and may not disappear
from the plan:

| Requirement | Assigned versions |
| --- | --- |
| `no_std`, Rust 1.90-1.97, OS portability, future custom target | 0.1, 0.52-0.55, 0.92-0.93 |
| Strict JSON, JOSE/JWK/JWA, EAB, rollover, nonces | 0.5-0.13 |
| Complete RFC 8555 operations | 0.14-0.25 |
| HTTP-01, DNS-01, TLS-ALPN-01 | 0.26-0.28, 0.42-0.51 |
| CSR, certificate parsing/verification, alternate chains | 0.29-0.31 |
| Durable workflow, stores, crash recovery, deployment | 0.32-0.39, 0.82-0.87 |
| Historical evidence replay, prior-release comparison, state/API/platform/provider drift | 0.3.3-0.4.4, 0.33.3, 0.39.2, 0.69.3, 0.92.6, 0.97.3, 0.119.0-0.119.1 |
| ARI | 0.40-0.41 |
| rustls, ring, RustCrypto, aws-lc-rs, AWS-LC FIPS | 0.51, 0.57-0.60 |
| PKCS#11, TPM2, AWS KMS, Azure Key Vault, OpenBao, remote signer | 0.61-0.66 |
| CAA, IP, provider profiles and staging conformance | 0.67-0.71 |
| Every published specialist ACME RFC and registry extension | 0.72-0.81 |
| SQLite, PostgreSQL HA, tenancy, deployers, CLI, daemon, agents | 0.82-0.91 |
| Kani, Loom, fuzzing, Miri, sanitizers, state models | 0.94-0.97 |
| All active/IESG and selected related draft families in the 2026-07-12 official snapshot | 0.100.0-0.111.0 |
| Production web-server replacement and regulated ACME acceptance | 0.51.2, 0.71.1-0.71.2 |
| API freeze, interoperability, resilience, supply chain, audits, RCs | 0.120 series |

There is no “post-1.0 someday” bucket in this plan. Newly discovered required
work must receive a new pre-1.0 version or split an existing milestone.
