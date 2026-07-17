#!/usr/bin/env python3
"""Audit every Vardheim release-plan row for a complete release contract."""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from pathlib import Path


TABLE_HEADER = "| Version | Goal and required deliverables | Milestone-specific proof |"
TABLE_SEPARATOR = "| --- | --- | --- |"
VERSION_ROW_PREFIX = "| `v"
VERSION_RE = r"v(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-(?:alpha|beta|rc)\.(?:0|[1-9][0-9]*))?"
ROW_RE = re.compile(
    rf"^\| `(?P<version>{VERSION_RE})` \| (?P<goal>[^|]+) \| (?P<proof>[^|]+) \|$"
)
WORD_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_./+-]*")
PLACEHOLDER_RE = re.compile(
    r"\b(?:TBD|TBC|TODO|FIXME)\b|\bas needed\b|\bdetails later\b|"
    r"\bto be decided\b|\bfuture work\b",
    re.IGNORECASE,
)
VERIFICATION_RE = re.compile(
    r"\b(?:test|tests|tested|fixture|fixtures|vector|vectors|fuzz|property|properties|"
    r"proof|prove|proves|check|checks|compile|matrix|matrices|audit|review|"
    r"evidence|report|reports|replay|benchmark|exercise|attestation|model|"
    r"trace|traces|simulation|simulations|suite|corpus|conformance|differential|integration|"
    r"inspection|validation|verify|verifies|verified|fail|fails|reject|rejects|rejected|"
    r"detect|detects|detected|pass|passes|safe|cannot|reproducible|reproduce|"
    r"reproduces|generate|generates|compare|compares|compared|cover|covers)\b",
    re.IGNORECASE,
)
GENERIC_PROOF_RE = re.compile(
    r"^(?:all )?(?:tests?|checks?|fixtures?) (?:pass|passes)[.]?$",
    re.IGNORECASE,
)
REQUIRED_CONTRACT_TEXT = (
    "## Mandatory Exit Contract For Every Version",
    "Every row below is a complete release boundary.",
    "vX.Y.Z implementation stop reached. Run pentest for this reviewed implementation commit.",
    "require a permanent `Status: PASS` report bound to the reviewed implementation commit before tagging",
    "## Tactical Milestone Size Rule",
    "## Release Row Completeness Contract",
    "The release-plan audit parses every row and phase table",
)


class AuditError(RuntimeError):
    """Raised when any release row or inherited exit contract is incomplete."""


@dataclass(frozen=True)
class AuditResult:
    versions: int
    phases: int


def normalized_text(text: str) -> str:
    return " ".join(text.split())


def words(value: str) -> list[str]:
    return WORD_RE.findall(value)


def validate_cell(version: str, field: str, value: str, minimum_words: int) -> None:
    if len(value) < 40:
        raise AuditError(f"{version} {field} is not a substantive release contract")
    if len(words(value)) < minimum_words:
        raise AuditError(f"{version} {field} is too terse")
    if not value.endswith("."):
        raise AuditError(f"{version} {field} must end with a complete sentence")
    match = PLACEHOLDER_RE.search(value)
    if match is not None:
        raise AuditError(f"{version} {field} contains placeholder {match.group(0)!r}")


def audit_release_plan(text: str) -> AuditResult:
    normalized = normalized_text(text)
    for required in REQUIRED_CONTRACT_TEXT:
        if required not in normalized:
            raise AuditError(f"release plan is missing contract text: {required}")

    lines = text.splitlines()
    phase_lines = [index for index, line in enumerate(lines) if line.startswith("## Phase")]
    header_count = lines.count(TABLE_HEADER)
    separator_count = lines.count(TABLE_SEPARATOR)
    if not phase_lines or header_count != len(phase_lines) or separator_count != header_count:
        raise AuditError("every phase must have exactly one complete release table")
    for index in phase_lines:
        following = [line for line in lines[index + 1 :] if line.strip()][:2]
        if following != [TABLE_HEADER, TABLE_SEPARATOR]:
            raise AuditError(f"phase at line {index + 1} lacks the required table schema")

    versions: set[str] = set()
    row_count = 0
    for line_number, line in enumerate(lines, start=1):
        if not line.startswith(VERSION_ROW_PREFIX):
            continue
        match = ROW_RE.fullmatch(line)
        if match is None:
            raise AuditError(f"malformed version row at line {line_number}")
        version = match.group("version")
        if version in versions:
            raise AuditError(f"duplicate version row: {version}")
        versions.add(version)
        row_count += 1

        goal = match.group("goal").strip()
        proof = match.group("proof").strip()
        validate_cell(version, "goal/deliverables", goal, 5)
        validate_cell(version, "milestone proof", proof, 6)
        if VERIFICATION_RE.search(proof) is None:
            raise AuditError(f"{version} milestone proof lacks concrete verification language")
        if GENERIC_PROOF_RE.fullmatch(proof) is not None:
            raise AuditError(f"{version} milestone proof is generic")

    if row_count == 0:
        raise AuditError("release plan has no version rows")
    return AuditResult(versions=row_count, phases=len(phase_lines))


def main(arguments: list[str]) -> int:
    path = Path(arguments[1]) if len(arguments) == 2 else Path("docs/RELEASE_PLAN.md")
    if len(arguments) > 2:
        print(f"usage: {arguments[0]} [RELEASE_PLAN.md]", file=sys.stderr)
        return 2
    try:
        result = audit_release_plan(path.read_text(encoding="utf-8"))
    except (AuditError, OSError) as error:
        print(f"release plan audit failed: {error}", file=sys.stderr)
        return 1
    print(f"release plan row audit passed ({result.versions} versions, {result.phases} phases)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
