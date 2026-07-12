#!/usr/bin/env python3
"""Regression tests for Vardheim's per-crate release helper."""

from __future__ import annotations

import importlib.util
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "release_crates.py"


def load_release_crates():
    spec = importlib.util.spec_from_file_location("release_crates", SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("could not load release_crates.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


release_crates = load_release_crates()


def package(name: str, version: str, deps: tuple[str, ...] = ()) -> dict:
    return {
        "name": name,
        "version": version,
        "dependencies": [{"name": dependency} for dependency in deps],
    }


def base_plan() -> dict:
    return {
        "version": "0.1.0",
        "crates": {
            name: {
                "previous_version": "0.0.0",
                "version": "0.1.0",
                "change": "code",
                "publish": True,
                "reason": "test",
            }
            for name in release_crates.PUBLISH_ORDER
        },
    }


def base_packages() -> dict[str, dict]:
    packages = {
        name: package(name, "0.1.0") for name in release_crates.PUBLISH_ORDER
    }
    packages["vardheim"]["dependencies"] = [
        {"name": dependency} for dependency in release_crates.PUBLISH_ORDER[:-1]
    ]
    return packages


def assert_fails(expected: str, function, *args) -> None:
    try:
        function(*args)
    except RuntimeError as error:
        if expected not in str(error):
            raise AssertionError(f"expected {expected!r} in {error!r}") from error
        return
    raise AssertionError("expected RuntimeError")


def test_current_plan_and_order() -> None:
    plan = release_crates.release_plan(ROOT / "release-crates.toml")
    packages = release_crates.workspace_packages(release_crates.cargo_metadata())
    release_crates.verify_publish_order(packages, plan)


def test_facade_must_be_last() -> None:
    packages = base_packages()
    packages["vardheim-core"]["dependencies"] = [{"name": "vardheim"}]
    assert_fails(
        "appears later",
        release_crates.verify_publish_order,
        packages,
        base_plan(),
    )


def test_workspace_set_must_match() -> None:
    packages = base_packages()
    del packages["vardheim-core"]
    assert_fails(
        "differs from workspace packages",
        release_crates.verify_publish_order,
        packages,
        base_plan(),
    )


def test_manifest_version_must_match_plan() -> None:
    packages = base_packages()
    packages["vardheim-core"]["version"] = "0.2.0"
    assert_fails(
        "expected 0.1.0",
        release_crates.verify_publish_order,
        packages,
        base_plan(),
    )


def test_unchanged_crate_cannot_publish() -> None:
    entry = {
        "previous_version": "0.1.0",
        "version": "0.1.0",
        "change": "unchanged",
        "publish": True,
        "reason": "test",
    }
    assert_fails(
        "unchanged but publish is true",
        release_crates.validate_plan_entry,
        "vardheim-core",
        entry,
        "0.2.0",
    )


def test_support_code_requires_next_minor() -> None:
    entry = {
        "previous_version": "0.1.0",
        "version": "0.3.0",
        "change": "code",
        "publish": True,
        "reason": "test",
    }
    assert_fails(
        "version must be 0.2.0",
        release_crates.validate_plan_entry,
        "vardheim-core",
        entry,
        "0.9.0",
    )


def test_resume_requires_selected_package() -> None:
    assert_fails(
        "not selected",
        release_crates.selected_steps,
        "vardheim",
        ("vardheim-core",),
    )


def test_dirty_tree_refuses_publish() -> None:
    original_capture = release_crates.capture
    try:
        release_crates.capture = lambda _command: " M Cargo.toml"
        assert_fails(
            "dirty worktree",
            release_crates.require_clean_tagged_tree,
            "0.1.0",
        )
    finally:
        release_crates.capture = original_capture


def test_tag_must_point_at_head() -> None:
    original_capture = release_crates.capture
    original_try_capture = release_crates.try_capture

    def fake_capture(command: list[str]) -> str:
        return "" if command[1] == "status" else "current-head"

    try:
        release_crates.capture = fake_capture
        release_crates.try_capture = lambda _command: "other-commit"
        assert_fails(
            "does not point at HEAD",
            release_crates.require_clean_tagged_tree,
            "0.1.0",
        )
    finally:
        release_crates.capture = original_capture
        release_crates.try_capture = original_try_capture


def test_publish_plan_preserves_dependency_order() -> None:
    plan = base_plan()
    plan["crates"]["vardheim-challenge-http"]["publish"] = False
    assert release_crates.publish_plan(plan) == (
        "vardheim-core",
        "vardheim-challenge-dns",
        "vardheim-challenge-tls",
        "vardheim",
    )


def test_invalid_plan_entry_kinds_refuse() -> None:
    base = {
        "previous_version": "0.1.0",
        "version": "0.1.0",
        "change": "unchanged",
        "publish": False,
        "reason": "test",
    }
    cases = (
        ({**base, "change": "mystery"}, "invalid change kind"),
        ({**base, "publish": "no"}, "publish must be true or false"),
        ({**base, "version": "0.2.0"}, "differs from previous_version"),
        (
            {**base, "change": "dependency", "version": "0.2.0", "publish": True},
            "require a patch bump",
        ),
        (
            {**base, "change": "metadata", "version": "0.1.0", "publish": True},
            "metadata changes must use 0.2.0",
        ),
    )
    for entry, expected in cases:
        assert_fails(
            expected,
            release_crates.validate_plan_entry,
            "vardheim-core",
            entry,
            "0.2.0",
        )


def run_tests() -> None:
    tests = (
        test_current_plan_and_order,
        test_facade_must_be_last,
        test_workspace_set_must_match,
        test_manifest_version_must_match_plan,
        test_unchanged_crate_cannot_publish,
        test_support_code_requires_next_minor,
        test_resume_requires_selected_package,
        test_dirty_tree_refuses_publish,
        test_tag_must_point_at_head,
        test_publish_plan_preserves_dependency_order,
        test_invalid_plan_entry_kinds_refuse,
    )
    for test in tests:
        test()


if __name__ == "__main__":
    run_tests()
