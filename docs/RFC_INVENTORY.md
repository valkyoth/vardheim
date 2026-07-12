# RFC Inventory

The tracked `rfc/` directory contains exact unmodified working copies
downloaded from the RFC Editor. SHA-256 integrity enforcement prevents silent
changes, and Cargo package inspection prevents the documents from entering
published crates. Normative implementation claims cite RFC number, section,
errata status, and conformance fixtures.

## ACME Standards

RFC 8555, 8657, 8737, 8738, 8739, 8823, 9115, 9444, 9447, 9448, 9773, 9799,
and 9891 form the published ACME family in scope.

## Required Supporting Standards

- Normative language, randomness, and time: RFC 2119, 3339, 4086, and 8174.
- JOSE and encoding: RFC 4648, 7515, 7516, 7517, 7518, 7519, 7638,
  8037, and 8725.
- HTTP and URI: RFC 3986, 7807, 8288, 9110, 9111, 9112, and 9457.
- PKIX, keys, and CSR: RFC 2986, 5280, 5480, 5958, 6125, 6960, 7468,
  8017, 8018, 8032, 8410, and 9162.
- TLS identity/presentation: RFC 6066, 7301, and 8446.
- Email/S/MIME: RFC 5321, 5322, 6531, and 8551.
- DNS and names: RFC 1034, 1035, 3596, 4033, 4034, 4035, 5890 through 5895,
  8659.

## Conformance Tiers

`Vardheim Core 1.0` requires complete RFC 8555 and its JOSE, encoding, HTTP,
CSR, PEM, and PKIX foundations. `Vardheim Web PKI 1.0` additionally requires
RFC 8657, 8737, 8738, 9773, and CAA processing from RFC 8659. Remaining
published ACME RFCs are production requirements before 1.0, delivered as
isolated optional modules after the Web PKI path is complete.

## Current ACME Work Snapshot

As checked against the official IETF ACME documents page on 2026-07-12,
active/IESG work includes certificate profiles, persistent DNS validation, DNS
account labels, authority-token JWT constraints, RATS, device attestation, and
device enrollment integrations. Selected related work includes quantum-ready
profiles, public-key challenges, and identity-controlled validation. The exact
draft revisions are intentionally fetched and pinned only at their `0.100.x`
implementation milestones because Internet-Drafts can change or expire.
