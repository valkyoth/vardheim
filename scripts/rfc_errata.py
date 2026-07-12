#!/usr/bin/env python3
"""Validate or refresh the official ACME RFC errata snapshot."""

from __future__ import annotations

import argparse
import json
import re
import sys
import urllib.parse
import urllib.request
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "rfc/ACME_ERRATA.json"
CHECKED_AT = "2026-07-12"
ACME_RFCS = (8555, 8657, 8737, 8738, 8739, 8823, 9115, 9444, 9447, 9448, 9773, 9799, 9891)
STATUSES = ("Verified", "Reported", "Held for Document Update", "Rejected")
ENDPOINT = "https://errata.rfc-editor.org/search/"


class ErrataError(RuntimeError):
    """A malformed or drifting errata snapshot."""


class ErrataTableParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.heading = False
        self.heading_text: list[str] = []
        self.status: str | None = None
        self.in_row = False
        self.in_cell = False
        self.cell_text: list[str] = []
        self.cells: list[str] = []
        self.records: list[dict] = []

    def handle_starttag(self, tag: str, _attrs) -> None:
        if tag == "h2":
            self.heading = True
            self.heading_text = []
        elif tag == "tr":
            self.in_row = True
            self.cells = []
        elif tag == "td" and self.in_row:
            self.in_cell = True
            self.cell_text = []

    def handle_data(self, data: str) -> None:
        if self.heading:
            self.heading_text.append(data)
        if self.in_cell:
            self.cell_text.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "h2" and self.heading:
            heading = "".join(self.heading_text).strip()
            self.status = next((status for status in STATUSES if heading.startswith(status)), None)
            self.heading = False
        elif tag == "td" and self.in_cell:
            self.cells.append(" ".join("".join(self.cell_text).split()))
            self.in_cell = False
        elif tag == "tr" and self.in_row:
            self.in_row = False
            if self.cells and self.status is not None:
                self._record_row()

    def _record_row(self) -> None:
        match = re.fullmatch(r"RFC([0-9]+) \(([0-9]+)\)", self.cells[0])
        if match is None or len(self.cells) != 7:
            raise ErrataError(f"unrecognized errata table row: {self.cells}")
        self.records.append(
            {
                "rfc": int(match.group(1)),
                "id": int(match.group(2)),
                "source": f"https://errata.rfc-editor.org/eid{match.group(2)}/",
                "status": self.status,
                "section": self.cells[1],
                "type": self.cells[2],
                "reported": self.cells[6],
            }
        )


def fetch_rfc(number: int) -> list[dict]:
    query = urllib.parse.urlencode(
        {"rfc_number": number, "status": "any", "presentation": "table"}
    )
    request = urllib.request.Request(
        f"{ENDPOINT}?{query}",
        headers={"User-Agent": "vardheim-rfc-baseline/0.3.0"},
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            html = response.read().decode("utf-8")
    except OSError as error:
        raise ErrataError(f"cannot fetch RFC {number} errata: {error}") from error
    parser = ErrataTableParser()
    parser.feed(html)
    records = parser.records
    if any(record["rfc"] != number for record in records):
        raise ErrataError(f"RFC {number} response contained another RFC")
    return sorted(records, key=lambda record: record["id"])


def fetch_snapshot() -> dict:
    return {
        "schema": 1,
        "checked_at": CHECKED_AT,
        "source": ENDPOINT,
        "documents": [
            {"rfc": number, "errata": fetch_rfc(number)} for number in ACME_RFCS
        ],
    }


def validate(snapshot: dict) -> None:
    if snapshot.get("schema") != 1 or snapshot.get("source") != ENDPOINT:
        raise ErrataError("errata snapshot schema or source is invalid")
    documents = snapshot.get("documents")
    if not isinstance(documents, list):
        raise ErrataError("errata snapshot has no document list")
    numbers = tuple(document.get("rfc") for document in documents)
    if numbers != ACME_RFCS:
        raise ErrataError(f"ACME RFC set/order differs: {numbers}")
    seen: set[int] = set()
    for document in documents:
        records = document.get("errata")
        if not isinstance(records, list):
            raise ErrataError(f"RFC {document['rfc']} has no errata list")
        for record in records:
            identifier = record.get("id")
            if not isinstance(identifier, int) or identifier in seen:
                raise ErrataError(f"duplicate or invalid errata ID: {identifier}")
            seen.add(identifier)
            if record.get("status") not in STATUSES:
                raise ErrataError(f"invalid errata status for {identifier}")
            if record.get("source") != f"https://errata.rfc-editor.org/eid{identifier}/":
                raise ErrataError(f"invalid errata source for {identifier}")
            if record.get("type") not in ("Technical", "Editorial"):
                raise ErrataError(f"invalid errata type for {identifier}")


def load_snapshot() -> dict:
    try:
        snapshot = json.loads(OUTPUT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        raise ErrataError(f"cannot load {OUTPUT.name}: {error}") from error
    validate(snapshot)
    return snapshot


def comparable(snapshot: dict) -> list[dict]:
    return snapshot["documents"]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--write", action="store_true", help="Fetch and write snapshot")
    mode.add_argument("--live", action="store_true", help="Compare snapshot to live data")
    args = parser.parse_args()
    try:
        if args.write:
            snapshot = fetch_snapshot()
            validate(snapshot)
            OUTPUT.write_text(json.dumps(snapshot, indent=2) + "\n", encoding="utf-8")
            print(f"wrote {OUTPUT.relative_to(ROOT)}")
        elif args.live:
            local = load_snapshot()
            current = fetch_snapshot()
            if comparable(local) != comparable(current):
                raise ErrataError("official ACME errata differ from the pinned snapshot")
            print("official ACME errata match the pinned snapshot")
        else:
            snapshot = load_snapshot()
            count = sum(len(document["errata"]) for document in snapshot["documents"])
            print(f"ACME errata snapshot is valid ({count} records)")
    except ErrataError as error:
        print(f"ACME errata invalid: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
