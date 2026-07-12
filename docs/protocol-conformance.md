# Protocol Conformance

No RFC conformance is claimed through version 0.3.1. Version `0.3.0`
establishes immutable RFC source, section, hash, and errata evidence. Version
`0.3.1` adds bounded IANA registry, HTTP replacement, supporting-standard, and
external-profile revision evidence. Neither implements protocol behavior.

Each later claim requires:

- a section-level requirement matrix;
- positive, negative, malformed, boundary, and unknown-extension fixtures;
- errata review and an exact source-check date;
- deterministic unit and property tests;
- fault-injection coverage for ambiguous outcomes;
- integration evidence against a test CA and relevant staging services;
- pentest evidence for the exact release implementation.

Unknown identifiers, challenges, directory fields, order fields, and problem
types are retained only within explicit bounds. Recognizing a registry value is
not the same as implementing its workflow.
