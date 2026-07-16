# Security Controls

| Boundary | Required control |
| --- | --- |
| Input | explicit size, count, depth, time, and retry budgets |
| JSON | duplicate-key rejection and bounded unknown-field retention |
| JOSE | typed payloads, explicit algorithms, exact `jwk`/`kid` exclusivity |
| Nonces | per-directory bounded queues and destructive take semantics |
| URLs | trusted origins, no signed-request redirect, SSRF policy |
| Issuers | explicit directory identity and selection; no credential crossover or silent failover |
| Secrets | redacted formatting, role separation, minimum retention |
| Workflow | valid transitions only, persisted effects, reconciliation |
| Challenges | ownership receipts, self-check, durable cleanup |
| Certificates | key/SAN/profile/chain checks before deployment |
| PKIX evidence | private constructors in PKIX; facade-only reducer translation |
| Adoption | validate key/chain/issuer/account/provenance before managed status |
| Compromise | suspend affected key roles, explicit emergency replacement and revocation |
| Retirement | acknowledged target removal, fenced overlap, evidenced key/artifact disposition |
| Deployment | atomic activation, health verification, rollback |
| Concurrency | compare-and-swap revisions, leases, fencing tokens |
| Supply chain | pinned CI actions, deny policy, audit, SBOM, review |
| Release | pentest bound to reviewed implementation; allowlisted evidence-only finalization |

Controls become executable tests in the milestone that introduces their
boundary. A control without evidence is not considered implemented.
