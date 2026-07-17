#!/usr/bin/env python3
"""Negative-path tests for the complete Vardheim release-row audit."""

from __future__ import annotations

from pathlib import Path

from audit_release_plan import AuditError, audit_release_plan


ROOT = Path(__file__).resolve().parents[1]


def valid_plan() -> str:
    return """# Test release plan

## Mandatory Exit Contract For Every Version

Every row below is a complete release boundary.

5. `vX.Y.Z implementation stop reached. Run pentest for this reviewed implementation commit.`
7. require a permanent `Status: PASS` report bound to the reviewed implementation commit before tagging.

## Tactical Milestone Size Rule

Each release contains one independently reviewable implementation boundary.

## Release Row Completeness Contract

The release-plan audit parses every row and phase table for complete contracts.

## Phase 0 - Test

| Version | Goal and required deliverables | Milestone-specific proof |
| --- | --- | --- |
| `v0.1.0` | Bounded parser boundary delivering typed output, explicit limits, and stable errors. | Malformed, boundary, and differential fixtures verify exact accepted bytes and fail-closed rejection behavior. |
"""


def assert_fails(expected: str, text: str) -> None:
    try:
        audit_release_plan(text)
    except AuditError as error:
        if expected not in str(error):
            raise AssertionError(f"expected {expected!r} in {error!r}") from error
        return
    raise AssertionError("expected release plan audit failure")


def test_valid_fixture() -> None:
    result = audit_release_plan(valid_plan())
    assert result.versions == 1
    assert result.phases == 1


def test_current_plan_audits_every_release() -> None:
    result = audit_release_plan(
        (ROOT / "docs" / "RELEASE_PLAN.md").read_text(encoding="utf-8")
    )
    assert result.versions == 481
    assert result.phases == 13


def test_missing_pentest_exit_refuses() -> None:
    text = valid_plan().replace("Run pentest", "Run security checks")
    assert_fails("missing contract text", text)


def test_malformed_or_duplicate_rows_refuse() -> None:
    assert_fails("malformed version row", valid_plan().replace(" | Bounded", " Bounded"))
    row = valid_plan().splitlines()[-1]
    assert_fails("duplicate version row", valid_plan() + row + "\n")


def test_missing_phase_schema_refuses() -> None:
    text = valid_plan().replace(
        "| Version | Goal and required deliverables | Milestone-specific proof |",
        "| Version | Scope | Proof |",
    )
    assert_fails("complete release table", text)


def test_short_or_placeholder_goal_refuses() -> None:
    text = valid_plan().replace(
        "Bounded parser boundary delivering typed output, explicit limits, and stable errors.",
        "Parser goal.",
    )
    assert_fails("not a substantive", text)
    text = valid_plan().replace(
        "Bounded parser boundary delivering typed output, explicit limits, and stable errors.",
        "TBD parser boundary delivering typed output, explicit limits, and stable errors.",
    )
    assert_fails("contains placeholder", text)


def test_weak_or_non_verifying_proof_refuses() -> None:
    text = valid_plan().replace(
        "Malformed, boundary, and differential fixtures verify exact accepted bytes and fail-closed rejection behavior.",
        "All tests pass.",
    )
    assert_fails("not a substantive", text)
    text = valid_plan().replace(
        "Malformed, boundary, and differential fixtures verify exact accepted bytes and fail-closed rejection behavior.",
        "The resulting milestone behavior remains correct under every declared condition and boundary.",
    )
    assert_fails("lacks concrete verification language", text)


def run_tests() -> None:
    tests = (
        test_valid_fixture,
        test_current_plan_audits_every_release,
        test_missing_pentest_exit_refuses,
        test_malformed_or_duplicate_rows_refuse,
        test_missing_phase_schema_refuses,
        test_short_or_placeholder_goal_refuses,
        test_weak_or_non_verifying_proof_refuses,
    )
    for test in tests:
        test()
    print("release plan audit tests passed")


if __name__ == "__main__":
    run_tests()
