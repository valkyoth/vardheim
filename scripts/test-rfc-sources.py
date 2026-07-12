#!/usr/bin/env python3
"""Regression tests for the RFC section and errata source baselines."""

from __future__ import annotations

import copy

import rfc_errata
import rfc_inventory


def assert_fails(expected: str, function, *args) -> None:
    try:
        function(*args)
    except (rfc_inventory.InventoryError, rfc_errata.ErrataError) as error:
        if expected not in str(error):
            raise AssertionError(f"expected {expected!r} in {error!r}") from error
        return
    raise AssertionError("expected source validation failure")


def minimal_snapshot() -> dict:
    return {
        "schema": 1,
        "checked_at": "2026-07-12",
        "source": rfc_errata.ENDPOINT,
        "documents": [
            {"rfc": number, "errata": []} for number in rfc_errata.ACME_RFCS
        ],
    }


def test_current_generated_sources() -> None:
    rfc_inventory.check()
    snapshot = rfc_errata.load_snapshot()
    assert sum(len(document["errata"]) for document in snapshot["documents"]) == 24


def test_every_checksum_has_exactly_one_role() -> None:
    roles = rfc_inventory.role_map()
    checksums = rfc_inventory.checksum_manifest()
    assert len(roles) == 65
    assert set(roles) == set(checksums)
    assert set(rfc_inventory.ROLE_GROUPS["acme"]) == set(rfc_errata.ACME_RFCS)


def test_old_and_modern_section_formats() -> None:
    old = "1. Introduction\n2. Security Considerations\n"
    modern = (
        "   1. Introduction ........ 2\n"
        "      1.1. Scope ........ 3\n"
        "   2. Security Considerations ........ 4\n"
        "   200. (OK) response with a body\n"
        "   1800. Sutter St\n"
    )
    assert rfc_inventory.extract_sections(old, 1) == [
        {"id": "1", "title": "Introduction"},
        {"id": "2", "title": "Security Considerations"},
    ]
    assert rfc_inventory.extract_sections(modern, 2) == [
        {"id": "1", "title": "Introduction"},
        {"id": "1.1", "title": "Scope"},
        {"id": "2", "title": "Security Considerations"},
    ]
    assert_fails("no detected", rfc_inventory.extract_sections, "plain text", 3)


def test_errata_parser_tracks_all_status_groups() -> None:
    html = """
    <h2>Verified (1)</h2><table><tbody><tr>
    <td>RFC8555 (<a>1</a>)</td><td>7</td><td>Technical</td>
    <td>acme</td><td>A</td><td>TXT</td><td>2026-01-01</td></tr></tbody></table>
    <h2>Rejected (1)</h2><table><tbody><tr>
    <td>RFC8555 (<a>2</a>)</td><td>8</td><td>Editorial</td>
    <td>acme</td><td>B</td><td>TXT</td><td>2026-01-02</td></tr></tbody></table>
    """
    parser = rfc_errata.ErrataTableParser()
    parser.feed(html)
    assert [(record["id"], record["status"]) for record in parser.records] == [
        (1, "Verified"),
        (2, "Rejected"),
    ]


def test_errata_snapshot_refuses_set_status_and_id_drift() -> None:
    missing = minimal_snapshot()
    missing["documents"].pop()
    assert_fails("RFC set/order", rfc_errata.validate, missing)

    invalid_status = minimal_snapshot()
    invalid_status["documents"][0]["errata"] = [
        {
            "rfc": 8555,
            "id": 1,
            "source": "https://errata.rfc-editor.org/eid1/",
            "status": "Maybe",
            "section": "1",
            "type": "Technical",
            "reported": "2026-01-01",
        }
    ]
    assert_fails("invalid errata status", rfc_errata.validate, invalid_status)

    duplicate = copy.deepcopy(invalid_status)
    duplicate["documents"][0]["errata"][0]["status"] = "Verified"
    duplicate["documents"][1]["errata"] = copy.deepcopy(
        duplicate["documents"][0]["errata"]
    )
    assert_fails("duplicate or invalid", rfc_errata.validate, duplicate)


def run_tests() -> None:
    tests = (
        test_current_generated_sources,
        test_every_checksum_has_exactly_one_role,
        test_old_and_modern_section_formats,
        test_errata_parser_tracks_all_status_groups,
        test_errata_snapshot_refuses_set_status_and_id_drift,
    )
    for test in tests:
        test()
    print("RFC source baseline tests passed")


if __name__ == "__main__":
    run_tests()
