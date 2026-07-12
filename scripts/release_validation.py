#!/usr/bin/env python3
"""Release metadata and pentest readiness validation for Vardheim."""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from collections.abc import Callable
from datetime import date
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:  # pragma: no cover - release-host guard.
    print("Python 3.11+ is required because this script uses tomllib.", file=sys.stderr)
    raise


ROOT = Path(__file__).resolve().parents[1]
SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
COMMIT = re.compile(r"^[0-9a-f]{40}$")
REPORT_STATUSES = {"PENDING", "PASS", "FAIL"}
WORKSPACE_CRATES = (
    "vardheim-core",
    "vardheim-challenge-http",
    "vardheim-challenge-dns",
    "vardheim-challenge-tls",
    "vardheim",
)


class ValidationError(RuntimeError):
    """A fail-closed release evidence error."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def load_toml(path: Path) -> dict:
    try:
        with path.open("rb") as handle:
            return tomllib.load(handle)
    except (OSError, tomllib.TOMLDecodeError) as error:
        raise ValidationError(f"cannot load TOML {path}: {error}") from error


def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except OSError as error:
        raise ValidationError(f"cannot read {path}: {error}") from error


def exact_field(report: str, name: str) -> str:
    prefix = f"{name}:"
    matches = [line for line in report.splitlines() if line.startswith(prefix)]
    require(len(matches) == 1, f"pentest report requires exactly one {prefix} field")
    expected_prefix = f"{name}: "
    require(
        matches[0].startswith(expected_prefix),
        f"pentest field must use '{expected_prefix}<value>'",
    )
    value = matches[0][len(expected_prefix) :]
    require(bool(value.strip()), f"pentest {name} field must not be blank")
    return value


def facade_version(root: Path) -> str:
    manifest = load_toml(root / "crates/vardheim/Cargo.toml")
    version = manifest.get("package", {}).get("version")
    require(isinstance(version, str), "vardheim manifest has no explicit version")
    require(SEMVER.fullmatch(version) is not None, f"invalid facade version: {version}")
    return version


def release_gate_name(version: str) -> str:
    major, minor, patch = version.split(".")
    suffix = f"_{patch}" if patch != "0" else ""
    return f"release_{major}_{minor}{suffix}_gate.sh"


def planned_versions(root: Path) -> tuple[str, dict[str, str]]:
    plan = load_toml(root / "release-crates.toml")
    release = plan.get("release", {})
    version = release.get("version")
    require(isinstance(version, str), "release plan has no version")
    require(release.get("policy") == "independent", "release policy must be independent")
    crates = plan.get("crates", {})
    require(set(crates) == set(WORKSPACE_CRATES), "release plan crate set is incomplete")
    versions: dict[str, str] = {}
    for crate in WORKSPACE_CRATES:
        crate_version = crates[crate].get("version")
        require(isinstance(crate_version, str), f"{crate} has no planned version")
        versions[crate] = crate_version
    require(
        versions["vardheim"] == version,
        "vardheim must always match the release/tag version",
    )
    require(
        crates["vardheim"].get("publish") is True,
        "vardheim must be published for every release tag",
    )
    return version, versions


def validate_sbom(root: Path, versions: dict[str, str]) -> None:
    path = root / "sbom/vardheim.spdx.json"
    require(path.is_file(), "release SBOM is missing")
    try:
        document = json.loads(load_text(path))
    except json.JSONDecodeError as error:
        raise ValidationError(f"release SBOM is malformed: {error}") from error
    require(document.get("SPDXID") == "SPDXRef-DOCUMENT", "invalid SPDX document ID")
    packages = document.get("packages")
    require(isinstance(packages, list), "release SBOM has no package list")
    actual = {
        item.get("name"): item.get("versionInfo")
        for item in packages
        if isinstance(item, dict) and item.get("name") in versions
    }
    require(actual == versions, f"release SBOM versions differ: {actual} != {versions}")


def validate_metadata(root: Path = ROOT) -> str:
    require(not (root / "PENTEST.md").exists(), "temporary root PENTEST.md remains")
    version = facade_version(root)
    release_version, versions = planned_versions(root)
    require(version == release_version, "facade and release-plan versions differ")

    required_files = (
        "README.md",
        "CHANGELOG.md",
        "SECURITY.md",
        "docs/CRATE_RELEASES.md",
        "docs/IMPLEMENTATION_PLAN.md",
        "docs/REGISTRY_BASELINE.md",
        "docs/RFC_ERRATA.md",
        "docs/RELEASE_PLAN.md",
        "docs/VERSION_PLAN.md",
        "scripts/check-packages.sh",
        "scripts/validate-package-contents.py",
        "scripts/test-package-contents.py",
        "scripts/release_crates.py",
        "scripts/rfc_errata.py",
        "scripts/rfc_inventory.py",
        "scripts/registry_baseline.py",
        "scripts/test-registry-baseline.py",
        "scripts/lock-registries.sh",
        "registry/README.md",
        "registry/EXTERNAL_SOURCES.json",
        "registry/iana-acme.xml",
        "registry/iana-bundle.xml",
        "registry/iana-cose.xml",
        "registry/iana-smi-numbers.xml",
        "registry/SHA256SUMS",
        "registry/REGISTRY_BASELINE.json",
        "rfc/ACME_ERRATA.json",
        "rfc/SECTION_INDEX.json",
    )
    for relative in required_files:
        require((root / relative).is_file(), f"required release file is missing: {relative}")

    notes = root / f"release-notes/RELEASE_NOTES_{version}.md"
    report_path = root / f"security/pentest/v{version}.md"
    gate = root / "scripts" / release_gate_name(version)
    require(notes.is_file(), f"release notes are missing: {notes.name}")
    require(report_path.is_file(), f"pentest report is missing: {report_path.name}")
    require(gate.is_file() and os.access(gate, os.X_OK), "version release gate is missing")
    gate_text = load_text(gate)
    require(
        f"scripts/validate-release-readiness.sh v{version}" in gate_text,
        "release gate does not invoke matching readiness validation",
    )

    changelog = load_text(root / "CHANGELOG.md")
    require(f"## {version} - Unreleased" in changelog, "changelog version is missing")
    report = load_text(report_path)
    status = exact_field(report, "Status")
    require(status in REPORT_STATUSES, f"invalid pentest status: {status}")
    require(
        load_text(root / "README.md")
        == load_text(root / "crates/vardheim/README.md"),
        "root and facade README files differ",
    )
    validate_sbom(root, versions)
    return version


GitCheck = Callable[[Path, list[str]], bool]


def git_succeeds(root: Path, arguments: list[str]) -> bool:
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        check=False,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    return result.returncode == 0


def validate_readiness(
    tag: str,
    root: Path = ROOT,
    git_check: GitCheck = git_succeeds,
    *,
    require_tag_absent: bool = True,
) -> None:
    version = validate_metadata(root)
    require(tag == f"v{version}", f"expected release tag v{version}, got {tag}")
    report = load_text(root / f"security/pentest/{tag}.md")
    require(exact_field(report, "Status") == "PASS", "pentest status is not PASS")
    reviewed = exact_field(report, "Reviewed-Commit")
    require(COMMIT.fullmatch(reviewed) is not None, "Reviewed-Commit is not 40 hex")
    exact_field(report, "Tester")
    exact_field(report, "Scope")
    reviewed_date = exact_field(report, "Date")
    try:
        parsed_date = date.fromisoformat(reviewed_date)
    except ValueError as error:
        raise ValidationError("pentest Date is not YYYY-MM-DD") from error
    require(parsed_date.isoformat() == reviewed_date, "pentest Date is not canonical")

    require(
        git_check(root, ["cat-file", "-e", f"{reviewed}^{{commit}}"]),
        "Reviewed-Commit does not exist",
    )
    require(
        git_check(root, ["merge-base", "--is-ancestor", reviewed, "HEAD"]),
        "Reviewed-Commit is not an ancestor of HEAD",
    )
    if require_tag_absent:
        require(
            not git_check(root, ["rev-parse", "-q", "--verify", f"refs/tags/{tag}"]),
            f"release tag already exists: {tag}",
        )


def metadata_main() -> int:
    try:
        version = validate_metadata()
    except ValidationError as error:
        print(f"release metadata invalid: {error}", file=sys.stderr)
        return 1
    print(f"release metadata valid for v{version}")
    return 0


def readiness_main(arguments: list[str]) -> int:
    if len(arguments) != 1:
        print("usage: validate-release-readiness.sh vX.Y.Z", file=sys.stderr)
        return 2
    try:
        validate_readiness(arguments[0])
    except ValidationError as error:
        print(f"release readiness invalid: {error}", file=sys.stderr)
        return 1
    print(f"release readiness valid for {arguments[0]}")
    return 0
