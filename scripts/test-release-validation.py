#!/usr/bin/env python3
"""Negative-path tests for Vardheim release evidence validation."""

from __future__ import annotations

import json
import stat
import tempfile
from pathlib import Path

from release_validation import (
    ValidationError,
    release_gate_name,
    validate_metadata,
    validate_readiness,
)


CRATES = (
    "vardheim-core",
    "vardheim-challenge-http",
    "vardheim-challenge-dns",
    "vardheim-challenge-tls",
    "vardheim",
)
REVIEWED = "a" * 40


class FakeGit:
    def __init__(self, *, commit: bool = True, ancestor: bool = True, tag: bool = False):
        self.commit = commit
        self.ancestor = ancestor
        self.tag = tag

    def __call__(self, _root: Path, arguments: list[str]) -> bool:
        if arguments[0] == "cat-file":
            return self.commit
        if arguments[0] == "merge-base":
            return self.ancestor
        if arguments[0] == "rev-parse":
            return self.tag
        raise AssertionError(f"unexpected git arguments: {arguments}")


def write(root: Path, relative: str, content: str, *, executable: bool = False) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    if executable:
        path.chmod(path.stat().st_mode | stat.S_IXUSR)


def report(status: str = "PASS") -> str:
    return "\n".join(
        (
            "# Pentest",
            "",
            f"Status: {status}",
            f"Reviewed-Commit: {REVIEWED}",
            "Tester: test reviewer",
            "Date: 2026-07-12",
            "Scope: release enforcement",
            "",
        )
    )


def make_fixture(root: Path) -> None:
    write(
        root,
        "crates/vardheim/Cargo.toml",
        '[package]\nname = "vardheim"\nversion = "0.2.0"\n',
    )
    plan = '[release]\nversion = "0.2.0"\npolicy = "independent"\n'
    for crate in CRATES:
        version = "0.2.0" if crate == "vardheim" else "0.1.0"
        publish = "true" if crate == "vardheim" else "false"
        plan += (
            f'\n[crates."{crate}"]\nversion = "{version}"\n'
            f"publish = {publish}\n"
        )
    write(root, "release-crates.toml", plan)

    for relative in (
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
    ):
        write(root, relative, "fixture\n")
    write(root, "README.md", "same\n")
    write(root, "crates/vardheim/README.md", "same\n")
    write(root, "CHANGELOG.md", "## 0.2.0 - Unreleased\n")
    write(root, "release-notes/RELEASE_NOTES_0.2.0.md", "release notes\n")
    write(root, "security/pentest/v0.2.0.md", report())
    write(
        root,
        "scripts/release_0_2_gate.sh",
        "scripts/validate-release-readiness.sh v0.2.0\n",
        executable=True,
    )
    versions = {crate: "0.2.0" if crate == "vardheim" else "0.1.0" for crate in CRATES}
    sbom = {
        "SPDXID": "SPDXRef-DOCUMENT",
        "packages": [
            {"name": crate, "versionInfo": version}
            for crate, version in versions.items()
        ],
    }
    write(root, "sbom/vardheim.spdx.json", json.dumps(sbom))


def assert_fails(expected: str, function, *args, **kwargs) -> None:
    try:
        function(*args, **kwargs)
    except ValidationError as error:
        if expected not in str(error):
            raise AssertionError(f"expected {expected!r} in {error!r}") from error
        return
    raise AssertionError("expected ValidationError")


def with_fixture(action) -> None:
    with tempfile.TemporaryDirectory(prefix="vardheim-release-test-") as directory:
        root = Path(directory)
        make_fixture(root)
        action(root)


def test_valid_metadata_and_readiness() -> None:
    def check(root: Path) -> None:
        assert validate_metadata(root) == "0.2.0"
        validate_readiness("v0.2.0", root, FakeGit())
        validate_readiness(
            "v0.2.0",
            root,
            FakeGit(tag=True),
            require_tag_absent=False,
        )

    with_fixture(check)


def test_missing_release_files_refuse() -> None:
    paths = (
        "SECURITY.md",
        "docs/CRATE_RELEASES.md",
        "scripts/check-packages.sh",
        "scripts/validate-package-contents.py",
        "scripts/test-package-contents.py",
        "scripts/release_crates.py",
        "docs/REGISTRY_BASELINE.md",
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
        "release-notes/RELEASE_NOTES_0.2.0.md",
        "security/pentest/v0.2.0.md",
        "scripts/release_0_2_gate.sh",
        "sbom/vardheim.spdx.json",
    )
    for relative in paths:
        def check(root: Path, relative: str = relative) -> None:
            (root / relative).unlink()
            assert_fails("missing", validate_metadata, root)

        with_fixture(check)


def test_metadata_mismatches_refuse() -> None:
    def pentest_scratch(root: Path) -> None:
        write(root, "PENTEST.md", "temporary\n")
        assert_fails("PENTEST.md", validate_metadata, root)

    def version(root: Path) -> None:
        path = root / "release-crates.toml"
        path.write_text(path.read_text().replace('version = "0.2.0"', 'version = "0.3.0"', 1))
        assert_fails("must always match", validate_metadata, root)

    def readme(root: Path) -> None:
        write(root, "crates/vardheim/README.md", "different\n")
        assert_fails("README files differ", validate_metadata, root)

    def changelog(root: Path) -> None:
        write(root, "CHANGELOG.md", "## Unreleased\n")
        assert_fails("changelog version", validate_metadata, root)

    def gate(root: Path) -> None:
        write(root, "scripts/release_0_2_gate.sh", "wrong\n", executable=True)
        assert_fails("does not invoke", validate_metadata, root)

    def policy(root: Path) -> None:
        path = root / "release-crates.toml"
        path.write_text(path.read_text().replace('policy = "independent"', 'policy = "lockstep"'))
        assert_fails("policy must be independent", validate_metadata, root)

    def crate_set(root: Path) -> None:
        path = root / "release-crates.toml"
        content = path.read_text()
        content = content[: content.index('[crates."vardheim-core"]')]
        path.write_text(content)
        assert_fails("crate set is incomplete", validate_metadata, root)

    def non_executable_gate(root: Path) -> None:
        path = root / "scripts/release_0_2_gate.sh"
        path.chmod(stat.S_IRUSR | stat.S_IWUSR)
        assert_fails("release gate is missing", validate_metadata, root)

    def facade_not_selected(root: Path) -> None:
        path = root / "release-crates.toml"
        before, after = path.read_text().rsplit("publish = true", maxsplit=1)
        path.write_text(before + "publish = false" + after)
        assert_fails("must be published", validate_metadata, root)

    for action in (
        pentest_scratch,
        version,
        readme,
        changelog,
        gate,
        policy,
        crate_set,
        non_executable_gate,
        facade_not_selected,
    ):
        with_fixture(action)


def test_malformed_report_and_sbom_refuse() -> None:
    def invalid_status(root: Path) -> None:
        write(root, "security/pentest/v0.2.0.md", report("GREEN"))
        assert_fails("invalid pentest status", validate_metadata, root)

    def duplicate_status(root: Path) -> None:
        write(root, "security/pentest/v0.2.0.md", report() + "Status: PASS\n")
        assert_fails("exactly one Status", validate_metadata, root)

    def malformed_sbom(root: Path) -> None:
        write(root, "sbom/vardheim.spdx.json", "not-json\n")
        assert_fails("SBOM is malformed", validate_metadata, root)

    def stale_sbom(root: Path) -> None:
        path = root / "sbom/vardheim.spdx.json"
        path.write_text(path.read_text().replace('"0.2.0"', '"0.1.0"'))
        assert_fails("SBOM versions differ", validate_metadata, root)

    def wrong_spdx(root: Path) -> None:
        path = root / "sbom/vardheim.spdx.json"
        document = json.loads(path.read_text())
        document["SPDXID"] = "wrong"
        path.write_text(json.dumps(document))
        assert_fails("invalid SPDX", validate_metadata, root)

    def no_packages(root: Path) -> None:
        path = root / "sbom/vardheim.spdx.json"
        document = json.loads(path.read_text())
        del document["packages"]
        path.write_text(json.dumps(document))
        assert_fails("no package list", validate_metadata, root)

    for action in (
        invalid_status,
        duplicate_status,
        malformed_sbom,
        stale_sbom,
        wrong_spdx,
        no_packages,
    ):
        with_fixture(action)


def test_failed_pending_and_malformed_pentest_refuse() -> None:
    for status in ("FAIL", "PENDING"):
        def status_check(root: Path, status: str = status) -> None:
            write(root, "security/pentest/v0.2.0.md", report(status))
            assert_fails("not PASS", validate_readiness, "v0.2.0", root, FakeGit())

        with_fixture(status_check)

    mutations = (
        (f"Reviewed-Commit: {REVIEWED}", "Reviewed-Commit: bad", "not 40 hex"),
        ("Tester: test reviewer", "Tester:", "must use"),
        ("Date: 2026-07-12", "Date: yesterday", "not YYYY-MM-DD"),
        ("Scope: release enforcement", "Scope:", "must use"),
    )
    for old, new, expected in mutations:
        def malformed(root: Path, old: str = old, new: str = new, expected: str = expected) -> None:
            write(root, "security/pentest/v0.2.0.md", report().replace(old, new))
            assert_fails(expected, validate_readiness, "v0.2.0", root, FakeGit())

        with_fixture(malformed)

    def duplicate_reviewed_commit(root: Path) -> None:
        write(
            root,
            "security/pentest/v0.2.0.md",
            report() + f"Reviewed-Commit: {REVIEWED}\n",
        )
        assert_fails(
            "exactly one Reviewed-Commit",
            validate_readiness,
            "v0.2.0",
            root,
            FakeGit(),
        )

    with_fixture(duplicate_reviewed_commit)


def test_wrong_stale_and_tagged_commits_refuse() -> None:
    cases = (
        (FakeGit(commit=False), "does not exist"),
        (FakeGit(ancestor=False), "not an ancestor"),
        (FakeGit(tag=True), "tag already exists"),
    )
    for git, expected in cases:
        def check(root: Path, git: FakeGit = git, expected: str = expected) -> None:
            assert_fails(expected, validate_readiness, "v0.2.0", root, git)

        with_fixture(check)


def test_wrong_requested_tag_refuses() -> None:
    with_fixture(
        lambda root: assert_fails(
            "expected release tag",
            validate_readiness,
            "v0.3.0",
            root,
            FakeGit(),
        )
    )


def test_gate_name_policy() -> None:
    assert release_gate_name("0.2.0") == "release_0_2_gate.sh"
    assert release_gate_name("0.2.1") == "release_0_2_1_gate.sh"


def run_tests() -> None:
    tests = (
        test_valid_metadata_and_readiness,
        test_missing_release_files_refuse,
        test_metadata_mismatches_refuse,
        test_malformed_report_and_sbom_refuse,
        test_failed_pending_and_malformed_pentest_refuse,
        test_wrong_stale_and_tagged_commits_refuse,
        test_wrong_requested_tag_refuses,
        test_gate_name_policy,
    )
    for test in tests:
        test()
    print("release validation tests passed")


if __name__ == "__main__":
    run_tests()
