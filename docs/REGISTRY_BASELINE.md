# Registry And Profile Baseline

Vardheim `v0.3.1` pins the protocol registries and supporting profiles that
future ACME implementations must recognize. This is evidence only: it does not
add wire parsing, claim RFC conformance, or activate any external profile.

## IANA ACME Snapshot

The authoritative source is IANA's complete
[Automated Certificate Management Environment registry group](https://www.iana.org/assignments/acme/acme.xhtml).
The byte-locked XML reports a last-updated date of 2025-11-25 and was checked
on 2026-07-12. Its SHA-256 is recorded in `registry/SHA256SUMS`.

| Registry | Records |
| --- | ---: |
| ACME Account Object Fields | 7 |
| ACME Order Object Fields | 14 |
| ACME Authorization Object Fields | 6 |
| ACME Error Types | 31 |
| ACME Resource Types | 8 |
| ACME Directory Metadata Fields | 9 |
| ACME Identifier Types | 6 |
| ACME Validation Methods | 12 |
| ACME Order Auto-Renewal Fields | 5 |
| ACME Directory Metadata Auto-Renewal Fields | 3 |
| STAR Delegation CSR Template Extensions | 3 |
| ACME Authority Token Challenge Types | 1 |
| ACME RenewalInfo Object Fields | 2 |
| **Total** | **107** |

The generated fixture retains every record field, registration date, update
date, and source reference. Validation-method identity uses the composite
`(name, identifier type)` key because one method can validly occur for several
identifier types. Error identity uses its registered `type`; other registries
use `name`.

## Security Bounds

Registry input is untrusted evidence even when downloaded from an authority.
Generation therefore rejects input above 65,536 bytes, more than 32
registries, more than 256 total records, more than 128 records per registry,
more than 16 fields or eight references per record, or any individual text
value above 4,096 UTF-8 bytes. It also rejects DTD/entity declarations,
malformed namespaces, a changed registry set or order, missing primary keys,
missing references, duplicate keys, and checksum drift.

These are evidence-parser bounds, not future ACME wire limits. Wire budgets are
introduced at `v0.5.0` and `v0.5.1` before protocol parsing begins.

## Normative Non-RFC Sources

The published ACME family contains 11 normative references that are not RFCs.
The generated baseline proves every extracted label has a reviewed source:

- NIST FIPS 180-4 and the JSS15 published security paper;
- the exact 2015 ITU-T X.680 and X.690 revisions cited by RFC 8737;
- the Tor living specification pinned to commit
  `a6c90f44013f47d1c2dae8b4a5d25302e3b6e256` and the historical v2
  rendezvous revision `2437d19c` cited by RFC 9799;
- CA/Browser Forum TLS BR 2.0.6 as cited normatively by RFC 9799; and
- byte-pinned IANA ACME, Bundle Protocol, COSE, and SMI XML registries.

The normative revision and the current profile revision are deliberately
separate. For example, RFC 9799 cites TLS BR 2.0.6, while the reviewed current
profile below is 2.2.8. Future implementation must account for both rather
than silently replacing the published RFC's source.

## HTTP Replacement Map

RFC 8555 was published against the RFC 7230 HTTP family and RFC 7807 problem
details. The current implementation baseline uses the published successors:

| Obsolete RFC | Current RFC | Scope |
| ---: | --- | --- |
| 2818 | 9110 | HTTP over TLS semantics |
| 7230 | 9110 and 9112 | HTTP semantics and HTTP/1.1 messaging |
| 7231 | 9110 | HTTP semantics |
| 7232 | 9110 | conditional requests |
| 7233 | 9110 | range requests |
| 7234 | 9111 | HTTP caching |
| 7235 | 9110 | HTTP authentication semantics |
| 7807 | 9457 | problem details for HTTP APIs |

The mapping is bounded and machine-checked against the 92 supporting RFCs in
the section inventory. It does not silently rewrite RFC 8555 requirements;
future conformance requirements cite both the ACME source and applicable
replacement source.

## External Profile Revisions

The following mutable non-IETF profiles are revision-pinned for later scoped
work. Their presence does not make them normative for the current crate.

| Profile | Revision | Current use |
| --- | --- | --- |
| CA/Browser Forum TLS Baseline Requirements | 2.2.8 | future Web PKI tier |
| CA/Browser Forum S/MIME Baseline Requirements | 1.0.14 | future email ACME tier |
| CA/Browser Forum Network and Certificate System Security Requirements | 2.0.5 | future operational qualification |
| 3GPP TS 33.310 | 19.5.0 | future NfInstanceId profile |

Each record carries its authority page and immutable or revision-specific
source. The 3GPP specification remains under change control, so both its
specification number and exact release revision are required. Draft ACME work
is deliberately not pinned here; exact draft revisions begin with the isolated
experimental framework at `v0.100.0`.

## Reproduction

```bash
scripts/registry_baseline.py
python3 scripts/test-registry-baseline.py
scripts/lock-registries.sh
```

Both commands are offline and run in normal CI. Accepted baselines are never
updated from live network state. Complete reference closure is the `v0.3.4`
boundary; advisory addition/removal/status/reference/revision drift reporting
is the separate `v0.3.8` boundary.
