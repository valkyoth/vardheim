# Vardheim 0.3.1 Release Notes

Status: implementation complete; pending pentest and retest

## Scope

This release establishes the bounded registry and external-profile evidence
baseline used by later conformance and protocol milestones. It adds no ACME
wire behavior.

## Added

- Byte-pinned official IANA ACME XML snapshot with strict SHA-256 validation.
- Deterministic generated fixtures for all 107 current records in all 13 ACME
  subregistries.
- Explicit bounded categories covering every known object field, error,
  resource, identifier, validation method, and registered extension value.
- Current HTTP replacement mapping from RFC 2818, the RFC 7230 family, and RFC
  7807 to RFC 9110, 9111, 9112, and 9457.
- Generated inventory of all 92 non-ACME supporting RFCs and their exact source
  hashes, including every normative RFC reference used by the 13 published
  ACME-family RFCs.
- Forty newly integrity-pinned, unmodified RFC sources required by specialist
  ACME standards, with generated proof that no normative RFC is absent.
- Complete inventory of all 11 normative non-RFC references, including three
  additional byte-pinned IANA registry groups and exact NIST, ITU-T, Tor,
  CA/Browser Forum, and published-paper revisions.
- Revision pins for CA/Browser Forum TLS BR 2.2.8, S/MIME BR 1.0.14, Network
  Security Requirements 2.0.5, and 3GPP TS 33.310 19.5.0.
- Adversarial tests for checksum drift, unsafe XML declarations, source and
  collection limits, missing registries, duplicate composite keys, missing
  fields/references, and untracked HTTP replacements.

## Security

- Normal builds and CI remain offline and cannot mutate accepted evidence.
- IANA XML is size-limited before parsing and rejects DTD/entity declarations.
- Registry, record, field, reference, and UTF-8 text limits prevent unbounded
  evidence parsing.
- Every record retains its official references and must have a complete,
  registry-appropriate unique key.
- Mutable external profiles are pinned by exact revision without activating
  them or claiming current conformance.

## Pentest Remediation

The initial review found that the raw-byte XML declaration guard could be
bypassed by UTF-16 or UTF-32 encoded input before a future live-source path
uses the parser. XML is now pre-parsed with encoding-aware Expat handlers that
reject DOCTYPE, entity, unparsed-entity, and external-entity declarations
before ElementTree receives the document. Permanent tests cover the same
entity-expansion payload in UTF-8, UTF-16, and UTF-32, plus benign UTF-16 input.
Remediation retest is pending.

## Publishing

Only `vardheim` advances from `0.3.0` to `0.3.1`. The four unchanged support
crates remain at `0.1.0`. The facade is always selected for publication and
must exactly match the `v0.3.1` tag.

## Compatibility

Rust `1.90.0` through `1.97.0` remains supported. All crates remain `no_std`
and dependency-free.

## Known Limitations

No RFC or external-profile conformance is claimed. Machine-readable
requirements and future test slots arrive at `v0.3.2`; advisory live drift
reporting arrives at `v0.3.3`.
