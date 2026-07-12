#!/usr/bin/env python3
"""Fail closed unless every current Vardheim crate archive is code-focused."""

from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
import tarfile
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
MAX_FILES = 512
MAX_FILE_BYTES = 1_048_576
MAX_TOTAL_BYTES = 5_242_880
REQUIRED_FILES = {
    ".cargo_vcs_info.json",
    "Cargo.lock",
    "Cargo.toml",
    "Cargo.toml.orig",
    "README.md",
}


class PackageContentError(RuntimeError):
    """An unsafe, unexpected, incomplete, or oversized crate archive."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise PackageContentError(message)


def workspace_archives() -> list[tuple[str, str, Path]]:
    result = subprocess.run(
        ["cargo", "metadata", "--format-version", "1", "--no-deps"],
        cwd=ROOT,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    metadata = json.loads(result.stdout)
    workspace_ids = set(metadata["workspace_members"])
    packages = [
        item
        for item in metadata["packages"]
        if item["id"] in workspace_ids and item["name"].startswith("vardheim")
    ]
    require(len(packages) == 5, "workspace crate set differs")
    return [
        (
            item["name"],
            item["version"],
            ROOT / "target/package" / f"{item['name']}-{item['version']}.crate",
        )
        for item in packages
    ]


def allowed_relative_path(path: PurePosixPath) -> bool:
    rendered = path.as_posix()
    if rendered in REQUIRED_FILES:
        return True
    return len(path.parts) >= 2 and path.parts[0] == "src" and path.suffix == ".rs"


def validate_archive(path: Path, package: str, version: str) -> None:
    require(path.is_file(), f"package archive is missing: {path.name}")
    expected_root = f"{package}-{version}"
    try:
        archive = tarfile.open(path, mode="r:gz")
    except (OSError, tarfile.TarError) as error:
        raise PackageContentError(f"cannot read {path.name}: {error}") from error
    with archive:
        members = archive.getmembers()
        require(bool(members), f"{path.name} is empty")
        require(len(members) <= MAX_FILES, f"{path.name} has too many files")
        seen: set[str] = set()
        relative_files: set[str] = set()
        total_bytes = 0
        for member in members:
            require(member.isfile(), f"{path.name} contains a non-regular entry: {member.name}")
            member_path = PurePosixPath(member.name)
            require(not member_path.is_absolute(), f"{path.name} contains an absolute path")
            require(".." not in member_path.parts, f"{path.name} contains parent traversal")
            require(len(member_path.parts) >= 2, f"{path.name} has no package root")
            require(member_path.parts[0] == expected_root, f"{path.name} has an unexpected package root")
            relative = PurePosixPath(*member_path.parts[1:])
            rendered = relative.as_posix()
            require(rendered not in seen, f"{path.name} contains a duplicate path: {rendered}")
            seen.add(rendered)
            require(allowed_relative_path(relative), f"{path.name} contains unexpected content: {rendered}")
            require(member.size <= MAX_FILE_BYTES, f"{path.name} contains an oversized file: {rendered}")
            total_bytes += member.size
            require(total_bytes <= MAX_TOTAL_BYTES, f"{path.name} unpacked size is excessive")
            relative_files.add(rendered)
        require(REQUIRED_FILES <= relative_files, f"{path.name} lacks required package metadata")
        require(any(name.startswith("src/") for name in relative_files), f"{path.name} contains no Rust source")


def validate_current_archives() -> None:
    for package, version, path in workspace_archives():
        validate_archive(path, package, version)


def fixture_archive(path: Path, root: str, files: dict[str, bytes]) -> None:
    with tarfile.open(path, mode="w:gz") as archive:
        for relative, content in files.items():
            info = tarfile.TarInfo(f"{root}/{relative}")
            info.size = len(content)
            info.mode = 0o644
            archive.addfile(info, io.BytesIO(content))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        validate_current_archives()
        print("crate archives contain only code-focused package files")
    except (PackageContentError, OSError, json.JSONDecodeError, subprocess.SubprocessError) as error:
        print(f"crate package content invalid: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
