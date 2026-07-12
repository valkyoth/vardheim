#!/usr/bin/env python3
"""Generate and verify Vardheim's checksum-bound RFC section inventory."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RFC_DIR = ROOT / "rfc"
OUTPUT = RFC_DIR / "SECTION_INDEX.json"
SOURCE_BASE = "https://www.rfc-editor.org/rfc/"
CHECKED_AT = "2026-07-12"

ROLE_GROUPS = {
    "acme": (8555, 8657, 8737, 8738, 8739, 8823, 9115, 9444, 9447, 9448, 9773, 9799, 9891),
    "normative-foundation": (2119, 3339, 4086, 8174),
    "encoding-jose": (4648, 7515, 7516, 7517, 7518, 7519, 7638, 8037, 8725),
    "http-uri": (3986, 7807, 8288, 9110, 9111, 9112, 9457),
    "pkix-keys": (2986, 5280, 5480, 5958, 6125, 6960, 7468, 8017, 8018, 8032, 8410, 9162),
    "tls": (6066, 7301, 8446),
    "email-smime": (5321, 5322, 6531, 8551),
    "dns-names": (1034, 1035, 3596, 4033, 4034, 4035, 5890, 5891, 5892, 5893, 5894, 5895, 8659),
}

TOC_SECTION_PATTERNS = (
    re.compile(
        r"^\s{3,}(?P<id>(?:[0-9]+(?:\.[0-9]+)*|[A-Z](?:\.[0-9]+)*))\.?\s+(?P<title>\S.*?)\s+\.{3,}\s+(?:[0-9]+|[ivxlcdm]+)$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^\s{3,}Appendix\s+(?P<id>[A-Z])\.\s+(?P<title>\S.*?)\s+\.{3,}\s+(?:[0-9]+|[ivxlcdm]+)$",
        re.IGNORECASE,
    ),
)
BODY_SECTION_PATTERNS = (
    re.compile(
        r"^(?P<id>(?:[0-9]+(?:\.[0-9]+)*|[A-Z](?:\.[0-9]+)*))\.\s+(?P<title>\S.*)$"
    ),
    re.compile(r"^Appendix\s+(?P<id>[A-Z])\.\s+(?P<title>\S.*)$"),
)


class InventoryError(RuntimeError):
    """A malformed or drifting RFC inventory."""


def role_map() -> dict[int, str]:
    roles: dict[int, str] = {}
    for role, numbers in ROLE_GROUPS.items():
        for number in numbers:
            if number in roles:
                raise InventoryError(f"RFC {number} has duplicate roles")
            roles[number] = role
    return roles


def checksum_manifest() -> dict[int, str]:
    checksums: dict[int, str] = {}
    pattern = re.compile(r"^([0-9a-f]{64})  rfc([0-9]+)\.txt$")
    for line in (RFC_DIR / "SHA256SUMS").read_text(encoding="ascii").splitlines():
        match = pattern.fullmatch(line)
        if match is None:
            raise InventoryError(f"malformed SHA256SUMS line: {line!r}")
        number = int(match.group(2))
        if number in checksums:
            raise InventoryError(f"duplicate checksum for RFC {number}")
        checksums[number] = match.group(1)
    return checksums


def extract_sections(text: str, number: int) -> list[dict[str, str]]:
    lines = text.splitlines()
    sections = extract_matching_sections(lines, TOC_SECTION_PATTERNS)
    if len(sections) < 3:
        sections = extract_matching_sections(lines, BODY_SECTION_PATTERNS)
    if not sections:
        raise InventoryError(f"RFC {number} has no detected numbered sections")
    return [{"id": identifier, "title": title} for identifier, title in sections.items()]


def extract_matching_sections(
    lines: list[str], patterns: tuple[re.Pattern[str], ...]
) -> dict[str, str]:
    sections: dict[str, str] = {}
    for line in lines:
        match = next((pattern.match(line) for pattern in patterns if pattern.match(line)), None)
        if match is None:
            continue
        identifier = match.group("id")
        title = match.group("title").strip()
        if title and len(title) <= 180 and identifier not in sections:
            sections[identifier] = title
    return sections


def build_inventory() -> dict:
    roles = role_map()
    checksums = checksum_manifest()
    if set(roles) != set(checksums):
        missing_roles = sorted(set(checksums) - set(roles))
        missing_sources = sorted(set(roles) - set(checksums))
        raise InventoryError(
            f"RFC role/checksum mismatch: missing roles {missing_roles}, "
            f"missing sources {missing_sources}"
        )

    documents = []
    for number in sorted(checksums):
        path = RFC_DIR / f"rfc{number}.txt"
        if not path.is_file():
            raise InventoryError(f"missing RFC text: {path.name}")
        content = path.read_bytes()
        actual_hash = hashlib.sha256(content).hexdigest()
        if actual_hash != checksums[number]:
            raise InventoryError(f"RFC {number} differs from SHA256SUMS")
        text = content.decode("utf-8", errors="strict")
        documents.append(
            {
                "rfc": number,
                "role": roles[number],
                "source": f"{SOURCE_BASE}rfc{number}.txt",
                "sha256": actual_hash,
                "sections": extract_sections(text, number),
            }
        )
    return {
        "schema": 1,
        "checked_at": CHECKED_AT,
        "source_authority": "RFC Editor",
        "documents": documents,
    }


def render(inventory: dict) -> str:
    return json.dumps(inventory, indent=2, ensure_ascii=False) + "\n"


def check() -> None:
    expected = render(build_inventory())
    if not OUTPUT.is_file():
        raise InventoryError(f"generated inventory is missing: {OUTPUT.name}")
    actual = OUTPUT.read_text(encoding="utf-8")
    if actual != expected:
        raise InventoryError(
            "RFC section inventory is stale; run scripts/rfc_inventory.py --write"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate the index")
    args = parser.parse_args()
    try:
        if args.write:
            OUTPUT.write_text(render(build_inventory()), encoding="utf-8")
            print(f"wrote {OUTPUT.relative_to(ROOT)}")
        else:
            check()
            print("RFC section inventory is complete and current")
    except (InventoryError, OSError, UnicodeError) as error:
        print(f"RFC inventory invalid: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
