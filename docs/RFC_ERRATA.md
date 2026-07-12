# ACME RFC Errata Baseline

Status: official RFC Editor snapshot checked 2026-07-12

Published RFC text is immutable. Vardheim stores exact RFC Editor TXT files
and separately records every erratum status so corrections are never silently
inserted into those files.

The machine-readable snapshot is [`rfc/ACME_ERRATA.json`](../rfc/ACME_ERRATA.json).
It was obtained from the official [RFC Editor errata service](https://errata.rfc-editor.org/search/)
with all statuses selected.

## Interpretation Policy

- **Verified** errata are reviewed corrections and become normative inputs to
  the requirement and conformance work for the affected section.
- **Reported** errata are tracked as unresolved observations. They do not
  change implementation requirements until their status changes or an
  independent published standard requires the behavior.
- **Held for Document Update** errata remain visible design evidence but do not
  silently override published normative text.
- **Rejected** errata are retained to prevent repeatedly treating a rejected
  proposal as a correction.

Any status, ID, section, type, or record-set change detected by the optional
live comparison requires maintainer review and an explicit snapshot update.
Normal CI validates the pinned snapshot offline and never depends on the live
service.

## Snapshot Summary

| RFC | Verified | Reported | Held | Rejected |
| --- | ---: | ---: | ---: | ---: |
| 8555 | 11 | 4 | 6 | 1 |
| 8823 | 0 | 1 | 0 | 0 |
| 9115 | 1 | 0 | 0 | 0 |
| 8657, 8737, 8738, 8739, 9444, 9447, 9448, 9773, 9799, 9891 | 0 | 0 | 0 | 0 |
| **Total** | **12** | **5** | **6** | **1** |

## Verified Errata Applied To Future Requirements

| RFC | Errata IDs |
| --- | --- |
| 8555 | 5729, 5732, 5733, 5734, 5735, 5983, 6016, 6103, 6104, 6364, 7565 |
| 9115 | 7336 |

The snapshot also retains Reported IDs 5861, 7826, 8381, 8883, and 7508;
Held IDs 5979, 6030, 6276, 6317, 6843, and 6950; and Rejected ID 5771.

## Commands

Validate the committed snapshot offline:

```bash
scripts/rfc_errata.py
python3 scripts/test-rfc-sources.py
```

Compare it with the official live service during source review:

```bash
scripts/rfc_errata.py --live
```

After reviewing a legitimate upstream change, regenerate and inspect the full
diff before committing:

```bash
scripts/rfc_errata.py --write
```
