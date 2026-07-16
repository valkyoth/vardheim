# Security Controls

| Boundary | Required control |
| --- | --- |
| Input | explicit size, count, depth, time, and retry budgets |
| JSON | duplicate-key rejection and bounded unknown-field retention |
| JOSE | typed payloads, explicit algorithms, exact `jwk`/`kid` exclusivity |
| Nonces | per-directory bounded queues and destructive take semantics |
| URLs | trusted origins, no signed-request redirect, SSRF policy |
| Public PKI fetch | isolated credential-free transport; strict framing/media/complete-body checks and context-partitioned cache; untrusted bytes require local verification |
| Trust domains | ACME, issued-certificate, CT, DNSSEC, and provider trust are non-interchangeable |
| Issuers | explicit directory identity and selection; no credential crossover or silent failover |
| Secrets | redacted formatting, role separation, minimum retention |
| Workflow | valid transitions only, persisted effects, reconciliation |
| Challenges | ownership receipts, self-check, durable cleanup |
| Certificates | key/SAN/profile/chain checks before deployment |
| PKIX evidence | private, context-bound, non-serializable capabilities; facade-only reducer translation |
| Certificate Transparency | distinct RFC 6962 v1 and RFC 9162 v2 types, log lists, signature inputs, and evidence; no conversion/fallback |
| OCSP | explicit responder recursion/extensions, chain-wide status policy, POST privacy option, tenant/request cache isolation |
| DNSSEC | local chain/signature/denial validation; no unauthenticated AD trust |
| DNS query | fresh IDs and source ports, complete tuple/attempt binding, bounded EDNS/UDP and framed TCP correlation, optional non-authoritative Cookies |
| DNS update | RFC 8945 request-bound TSIG; dedicated MAC purpose and authenticated response |
| Adoption | validate key/chain/issuer/account/provenance before managed status |
| Compromise | suspend affected key roles, explicit emergency replacement and revocation |
| Retirement | acknowledged target removal, fenced overlap, evidenced key/artifact disposition |
| Must-Staple | verified fresh OCSP required; staple and certificate activate atomically |
| Deployment | atomic activation, health verification, rollback |
| Concurrency | compare-and-swap revisions, leases, fencing tokens |
| Supply chain | pinned CI actions, deny policy, audit, SBOM, review |
| Crypto capabilities | per-purpose provider tables; unsupported purposes typed rather than inferred from algorithm names |
| Release | pentest bound to reviewed implementation; allowlisted evidence-only finalization |

Controls become executable tests in the milestone that introduces their
boundary. A control without evidence is not considered implemented.
