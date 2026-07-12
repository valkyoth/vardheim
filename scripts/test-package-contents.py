#!/usr/bin/env python3
"""Adversarial tests for crates.io package-content enforcement."""

from __future__ import annotations

import importlib.util
import io
import tarfile
import tempfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/validate-package-contents.py"


def load_validator():
    spec = importlib.util.spec_from_file_location("validate_package_contents", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load package-content validator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


validator = load_validator()
PACKAGE = "vardheim"
VERSION = "0.3.1"
ARCHIVE_ROOT = f"{PACKAGE}-{VERSION}"


def valid_files() -> dict[str, bytes]:
    return {
        ".cargo_vcs_info.json": b"{}\n",
        "Cargo.lock": b"version = 4\n",
        "Cargo.toml": b"[package]\n",
        "Cargo.toml.orig": b"[package]\n",
        "README.md": b"# fixture\n",
        "src/lib.rs": b"#![no_std]\n",
    }


def assert_fails(fragment: str, path: Path) -> None:
    try:
        validator.validate_archive(path, PACKAGE, VERSION)
    except validator.PackageContentError as error:
        assert fragment in str(error), (fragment, str(error))
    else:
        raise AssertionError(f"expected package rejection containing {fragment!r}")


def write_archive(path: Path, files: dict[str, bytes]) -> None:
    validator.fixture_archive(path, ARCHIVE_ROOT, files)


def test_valid_archive_and_current_packages() -> None:
    with tempfile.TemporaryDirectory(prefix="vardheim-package-test-") as directory:
        path = Path(directory) / "valid.crate"
        write_archive(path, valid_files())
        validator.validate_archive(path, PACKAGE, VERSION)
    validator.validate_current_archives()


def test_repository_evidence_and_downloads_refuse() -> None:
    cases = (
        "rfc/rfc8555.txt",
        "registry/iana-acme.xml",
        "docs/RELEASE_PLAN.md",
        "scripts/fetch-rfcs.sh",
        ".github/images/vardheim.webp",
        "downloads/profile.zip",
        "src/vector.json",
    )
    with tempfile.TemporaryDirectory(prefix="vardheim-package-test-") as directory:
        for number, unexpected in enumerate(cases):
            path = Path(directory) / f"unexpected-{number}.crate"
            files = valid_files()
            files[unexpected] = b"not publishable\n"
            write_archive(path, files)
            assert_fails("unexpected content", path)


def test_traversal_root_and_entry_types_refuse() -> None:
    with tempfile.TemporaryDirectory(prefix="vardheim-package-test-") as directory:
        root = Path(directory)
        traversal = root / "traversal.crate"
        with tarfile.open(traversal, mode="w:gz") as archive:
            info = tarfile.TarInfo(f"{ARCHIVE_ROOT}/../secret")
            info.size = 1
            archive.addfile(info, io.BytesIO(b"x"))
        assert_fails("parent traversal", traversal)

        wrong_root = root / "wrong-root.crate"
        validator.fixture_archive(wrong_root, "other-0.3.1", valid_files())
        assert_fails("unexpected package root", wrong_root)

        symlink = root / "symlink.crate"
        write_archive(symlink, valid_files())
        with tarfile.open(symlink, mode="w:gz") as archive:
            info = tarfile.TarInfo(f"{ARCHIVE_ROOT}/src/lib.rs")
            info.type = tarfile.SYMTYPE
            info.linkname = "/etc/passwd"
            archive.addfile(info)
        assert_fails("non-regular entry", symlink)


def test_duplicates_missing_metadata_and_size_refuse() -> None:
    with tempfile.TemporaryDirectory(prefix="vardheim-package-test-") as directory:
        root = Path(directory)
        duplicate = root / "duplicate.crate"
        with tarfile.open(duplicate, mode="w:gz") as archive:
            for _ in range(2):
                info = tarfile.TarInfo(f"{ARCHIVE_ROOT}/README.md")
                info.size = 1
                archive.addfile(info, io.BytesIO(b"x"))
        assert_fails("duplicate path", duplicate)

        missing = root / "missing.crate"
        files = valid_files()
        del files["README.md"]
        write_archive(missing, files)
        assert_fails("lacks required", missing)

        oversized = root / "oversized.crate"
        files = valid_files()
        files["src/large.rs"] = b"x" * (validator.MAX_FILE_BYTES + 1)
        write_archive(oversized, files)
        assert_fails("oversized file", oversized)

        too_many = root / "too-many.crate"
        files = valid_files()
        for number in range(validator.MAX_FILES):
            files[f"src/generated/item_{number}.rs"] = b"pub const VALUE: u8 = 1;\n"
        write_archive(too_many, files)
        assert_fails("too many files", too_many)

        excessive_total = root / "excessive-total.crate"
        files = valid_files()
        for number in range(5):
            files[f"src/large_{number}.rs"] = b"x" * validator.MAX_FILE_BYTES
        write_archive(excessive_total, files)
        assert_fails("unpacked size is excessive", excessive_total)


def run_tests() -> None:
    tests = (
        test_valid_archive_and_current_packages,
        test_repository_evidence_and_downloads_refuse,
        test_traversal_root_and_entry_types_refuse,
        test_duplicates_missing_metadata_and_size_refuse,
    )
    for test in tests:
        test()
    print("crate package-content tests passed")


if __name__ == "__main__":
    run_tests()
