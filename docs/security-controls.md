# Security Controls

| Boundary | Required control |
| --- | --- |
| Input | explicit size, count, depth, time, and retry budgets |
| JSON | duplicate-key rejection and bounded unknown-field retention |
| JOSE | typed payloads, explicit algorithms, exact `jwk`/`kid` exclusivity |
| Nonces | linear non-secret `FreshNonce` authority, per-directory/account/tenant bounded caller-backed queues, destructive take with no restore, independent response harvesting before outcome handling, and persistable consumed IDs without live authority |
| URLs | trusted origins, no signed-request redirect, SSRF policy |
| Public PKI fetch | isolated credential-free transport; strict framing/media/complete-body checks and context-partitioned cache; untrusted bytes require local verification |
| Trust domains | ACME, issued-certificate, CT, DNSSEC, and provider trust are non-interchangeable |
| Issuers | explicit directory identity and selection; no credential crossover or silent failover |
| Account adoption | signer/public-key self-check plus fresh CA-authenticated account retrieval bound to directory and account URL |
| EAB account creation | one consumed typestate binds account intent/contacts/ToS, directory/URL, JWK/signer session, EAB secret version/algorithm, exact inner positive MAC evidence, outer nonce/admission/`VerifiedSignature`, attempt/request/effect IDs, and final bytes/digest; executable only after verified outer request and durable outbox commit; `badNonce` rebuilds everything; no evidence stitching, committed-byte rebuilding, blind ambiguous resend, or repeated success application |
| Account rollover | retain old/new keys until durable effective-signer proof; ambiguous rollover/deactivation blocks disposition |
| Secrets | redacted formatting, role separation, minimum retention |
| Workflow | valid transitions only, persisted effects, reconciliation |
| Challenges | conflict-checked method/revision registry; sealed receipts bind exact method revision, identifier, account/key authorization, resource IDs, generation, expiry, backend, observed value and cleanup owner; no cross-family/revision conversion; self-check and durable cleanup |
| DER/X.509 structure | canonical primitive/length encoding and version-gated certificate fields rejected before path validation |
| Public keys and signer handles | provider/session-bound RSA/EC/EdDSA validation; transient role-limited `BoundSigner` pins immutable native identity/version and public-key digest, never mutable aliases; ordinary signature effects consume exact-request admission, dispatch only to that identity, treat provider output as untrusted, and locally verify exact bytes/algorithm/parameters/encoding/key before use; `VerifiedSignature` binds verifier implementation/execution/trust identity and assurance, same-provider verification is not independent, and default production acceptance requires an independent local software verifier; binding operation alone is narrowly exempt; no signer/verifier fallback |
| MAC secrets and handles | create/import/adopt is transactional and quarantined until an admitted typed content-binding mode succeeds; a private single-use `SecretBindingAttempt` permits only the exact domain-separated local transcript or request-bound peer ceremony and never ordinary EAB/TSIG authority; peer confirmation has stable attempt/effect IDs, persist-before-effect ordering, orthogonal dispatch/operation/binding/observation state, authenticated purpose-specific evidence, no blind ambiguous retry, operation-specific EAB/DNS reconciliation, and no automatic mutating ceremony replay on restart; stable idempotency and durable lifecycle/obligations protect reconciliation, revalidation, source destruction, and disposition; transient purpose-limited `BoundMacKey` pins tenant, directory/zone, provider/session, immutable secret identity/version, algorithm, policy, health, and expiry; exact-input single-use admission is consumed before immutable dispatch; raw provider output remains `UnverifiedMac`; local/exportable secrets require constant-time independent `VerifiedMac`; ordinary opaque results are `ProviderAssertedMac`, while `CryptographicallyAttestedMac` requires a signed/native replay-protected full-transcript receipt; weaker evidence is rejected by default; no capability restoration, secret export, or provider fallback |
| Key onboarding | stable idempotent create/import identity; durable lifecycle state is separate from orthogonal obligations and live authority; `Active` means eligible, not signable; every process/provider session freshly validates and binds; ambiguous/lost/eventually visible outcomes reconcile with fencing; failures retain obligations; absence never proves destruction |
| Certificates | key/SAN/profile/chain checks and explicit durable renewal key-rotation mode before deployment |
| PKIX evidence | private, context-bound, non-serializable capabilities; facade-only reducer translation |
| Certificate Transparency | distinct RFC 6962 v1 and RFC 9162 v2 types, log lists, signatures, STH/Merkle evidence and MMD monitoring; no conversion/fallback |
| PKIX time/names | strict RFC 5280 ASN.1 time and RFC 4518 DN equality; no locale/lossy conversion/display-string matching |
| OCSP | explicit responder recursion/extensions, chain-wide status policy, POST privacy option, tenant/request cache isolation |
| DNSSEC | local chain/signature/denial validation; no unauthenticated AD trust |
| DNS query | fresh IDs and source ports, complete tuple/attempt binding, bounded EDNS/UDP and framed TCP correlation, optional non-authoritative Cookies |
| DNS authority discovery | AA/section/zone-cut/SOA/referral/glue/CNAME/DNAME semantics with bounded iterative nameserver address resolution and no ambient resolver fallback |
| DNS update | RFC 8945 request/response/chaining-bound TSIG through immutable secret-version dispatch and purpose-specific positive MAC evidence; dedicated MAC purpose, no raw provider MAC, authenticated response, non-mutating binding probe preference, and explicit ownership/rollback/reconciliation with no blind retry for ambiguous mutating confirmation UPDATEs |
| Adoption | validate key/chain/issuer/account/provenance before managed status |
| Compromise | suspend affected key roles, explicit emergency replacement and revocation |
| Retirement | acknowledged target removal, fenced overlap, typed provider-native disposition and reconciliation; destruction never inferred |
| Must-Staple | verified fresh OCSP required; staple and certificate activate atomically |
| Deployment | atomic activation, health verification, rollback |
| Concurrency | compare-and-swap revisions, leases, fencing tokens |
| ACME transport replay | explicit HTTP version, early data and implicit retries disabled, partitioned connection/session/resolver state, only proven-unsent requests retryable |
| Adapter failures | stable protocol/security/resource/backend/reconciliation/unsupported envelope; bounded diagnostics never drive authority; backend classes preserve unsupported/unavailable/rejected/corrupt/definitely-not-dispatched/may-have-dispatched distinctions |
| Crate tiers | portable crates remain `no_std` and safe Rust; native/FFI adapters require machine inventory, narrow audited unsafe modules, invariant owners, platform evidence, and inward-only dependencies |
| Supply chain | pinned CI actions, deny policy, audit, SBOM, review |
| Crypto capabilities | per-purpose provider tables; unsupported purposes typed rather than inferred from algorithm names |
| Release | pentest bound to reviewed implementation; allowlisted evidence-only finalization |

Controls become executable tests in the milestone that introduces their
boundary. A control without evidence is not considered implemented.
