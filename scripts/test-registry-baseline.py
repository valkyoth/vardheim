#!/usr/bin/env python3
"""Adversarial regression tests for the bounded registry baseline."""

from __future__ import annotations

import copy
import json
import xml.etree.ElementTree as ET

import registry_baseline


def assert_fails(fragment: str, function, *arguments, **keywords) -> None:
    try:
        function(*arguments, **keywords)
    except registry_baseline.RegistryError as error:
        assert fragment in str(error), (fragment, str(error))
    else:
        raise AssertionError(f"expected RegistryError containing {fragment!r}")


def source_tree() -> ET.Element:
    return ET.fromstring(registry_baseline.SOURCE.read_bytes())


def encoded(root: ET.Element) -> bytes:
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def registry(root: ET.Element, registry_id: str) -> ET.Element:
    for item in root.findall(f"{registry_baseline.NS}registry"):
        if item.get("id") == registry_id:
            return item
    raise AssertionError(f"missing fixture registry {registry_id}")


def test_current_baseline_is_complete_and_deterministic() -> None:
    baseline = registry_baseline.build_baseline()
    committed = json.loads(registry_baseline.OUTPUT.read_text(encoding="utf-8"))
    assert baseline == committed
    assert registry_baseline.render(baseline) == registry_baseline.render(
        registry_baseline.build_baseline()
    )
    iana = baseline["iana_acme"]
    assert iana["record_count"] == 107
    assert len(iana["registries"]) == 13
    assert len(baseline["supporting_standards"]) == 92
    assert len(baseline["external_normative_sources"]) == 11
    assert tuple(item["id"] for item in iana["registries"]) == (
        registry_baseline.EXPECTED_REGISTRIES
    )


def test_every_required_category_is_nonempty_and_bounded() -> None:
    baseline = registry_baseline.build_baseline()
    iana = baseline["iana_acme"]
    by_id = {item["id"]: item for item in iana["registries"]}
    covered: set[str] = set()
    for registry_ids in iana["required_categories"].values():
        for registry_id in registry_ids:
            assert by_id[registry_id]["records"]
            covered.add(registry_id)
    assert covered == set(registry_baseline.EXPECTED_REGISTRIES)
    limits = baseline["limits"]
    assert iana["record_count"] <= limits["records_total"]
    for item in iana["registries"]:
        assert len(item["records"]) <= limits["records_per_registry"]
        for record in item["records"]:
            assert len(record["fields"]) <= limits["fields_per_record"]
            assert len(record["references"]) <= limits["references_per_record"]


def test_known_registry_values_are_preserved() -> None:
    registries = {
        item["id"]: item for item in registry_baseline.build_baseline()["iana_acme"]["registries"]
    }
    errors = {item["fields"]["type"] for item in registries["acme-error-types"]["records"]}
    resources = {item["fields"]["name"] for item in registries["acme-resource-types"]["records"]}
    identifiers = {item["fields"]["name"] for item in registries["acme-identifier-types"]["records"]}
    validations = {
        (item["fields"]["name"], item["fields"]["type"])
        for item in registries["acme-validation-methods"]["records"]
    }
    assert {"badNonce", "alreadyReplaced", "onionCAARequired"} <= errors
    assert {"newNonce", "renewalInfo"} <= resources
    assert {"dns", "ip", "email", "TNAuthList", "bundleEID", "NfInstanceId"} == identifiers
    assert {("http-01", "dns"), ("tls-alpn-01", "ip"), ("tkauth-01", "NfInstanceId")} <= validations


def test_source_integrity_and_xml_safety_fail_closed() -> None:
    source = registry_baseline.SOURCE.read_bytes()
    assert set(registry_baseline.source_hashes()) == set(
        registry_baseline.REGISTRY_SOURCE_FILES
    )
    assert_fails("source hash differs", registry_baseline.parse_iana, source + b"\n")
    assert_fails(
        "unsafe XML declaration",
        registry_baseline.parse_iana,
        b'<!DOCTYPE x [<!ENTITY y "z">]><x>&y;</x>',
        verify_hash=False,
    )
    assert_fails(
        "source is oversized",
        registry_baseline.parse_iana,
        b"x" * (registry_baseline.LIMITS["source_bytes"] + 1),
        verify_hash=False,
    )


def test_registry_set_and_duplicate_keys_fail_closed() -> None:
    missing = source_tree()
    missing.remove(missing.findall(f"{registry_baseline.NS}registry")[-1])
    assert_fails("registry set or order differs", registry_baseline.parse_iana, encoded(missing), verify_hash=False)

    duplicate = source_tree()
    errors = registry(duplicate, "acme-error-types")
    records = errors.findall(f"{registry_baseline.NS}record")
    first_type = records[0].find(f"{registry_baseline.NS}type")
    second_type = records[1].find(f"{registry_baseline.NS}type")
    assert first_type is not None and second_type is not None
    second_type.text = first_type.text
    assert_fails("duplicate record keys", registry_baseline.parse_iana, encoded(duplicate), verify_hash=False)

    removed_record = source_tree()
    account = registry(removed_record, "acme-account-object-fields")
    account.remove(account.findall(f"{registry_baseline.NS}record")[-1])
    assert_fails("record count differs", registry_baseline.parse_iana, encoded(removed_record), verify_hash=False)


def test_record_key_field_and_reference_limits_fail_closed() -> None:
    missing_key = source_tree()
    errors = registry(missing_key, "acme-error-types")
    first = errors.find(f"{registry_baseline.NS}record")
    assert first is not None
    type_element = first.find(f"{registry_baseline.NS}type")
    assert type_element is not None
    first.remove(type_element)
    assert_fails("no primary key", registry_baseline.parse_iana, encoded(missing_key), verify_hash=False)

    too_many_fields = source_tree()
    account = registry(too_many_fields, "acme-account-object-fields")
    record = account.find(f"{registry_baseline.NS}record")
    assert record is not None
    for number in range(registry_baseline.LIMITS["fields_per_record"] + 1):
        ET.SubElement(record, f"{registry_baseline.NS}extra{number}").text = "x"
    assert_fails("too many fields", registry_baseline.parse_iana, encoded(too_many_fields), verify_hash=False)

    too_many_references = source_tree()
    account = registry(too_many_references, "acme-account-object-fields")
    record = account.find(f"{registry_baseline.NS}record")
    assert record is not None
    for number in range(registry_baseline.LIMITS["references_per_record"]):
        ET.SubElement(record, f"{registry_baseline.NS}xref", type="uri", data=f"https://example.invalid/{number}")
    assert_fails("too many references", registry_baseline.parse_iana, encoded(too_many_references), verify_hash=False)

    wrong_namespace = source_tree()
    account = registry(wrong_namespace, "acme-account-object-fields")
    record = account.find(f"{registry_baseline.NS}record")
    assert record is not None
    ET.SubElement(record, "{https://example.invalid/namespace}field").text = "x"
    assert_fails("unexpected IANA XML namespace", registry_baseline.parse_iana, encoded(wrong_namespace), verify_hash=False)


def test_record_count_and_supporting_mapping_fail_closed() -> None:
    oversized = source_tree()
    account = registry(oversized, "acme-account-object-fields")
    original = account.find(f"{registry_baseline.NS}record")
    assert original is not None
    name = original.find(f"{registry_baseline.NS}name")
    assert name is not None
    existing = len(account.findall(f"{registry_baseline.NS}record"))
    for number in range(existing, registry_baseline.LIMITS["records_per_registry"] + 1):
        clone = copy.deepcopy(original)
        clone_name = clone.find(f"{registry_baseline.NS}name")
        assert clone_name is not None
        clone_name.text = f"bounded-{number}"
        account.append(clone)
    assert_fails("too many records", registry_baseline.parse_iana, encoded(oversized), verify_hash=False)
    assert_fails("not tracked", registry_baseline.http_replacements, {9111, 9112, 9457})


def test_external_profile_revisions_are_unique_and_pinned() -> None:
    profiles = registry_baseline.build_baseline()["external_profiles"]
    assert len({item["id"] for item in profiles}) == len(profiles)
    assert {(item["id"], item["revision"]) for item in profiles} == {
        ("cabf-tls-br", "2.2.8"),
        ("cabf-smime-br", "1.0.14"),
        ("cabf-network-security", "2.0.5"),
        ("3gpp-ts-33.310", "19.5.0"),
    }
    assert all(item["source"].startswith("https://") for item in profiles)
    assert all(item["revision_source"].startswith("https://") for item in profiles)
    sources = registry_baseline.build_baseline()["external_normative_sources"]
    assert {item["reference"] for item in sources} == {
        "FIPS180-4",
        "IANA-ACME",
        "IANA-BP",
        "IANA-COSE",
        "IANA-SMI",
        "JSS15",
        "X.680",
        "X.690",
        "cabf-br",
        "tor-rend-spec-v2",
        "tor-spec",
    }


def run_tests() -> None:
    tests = (
        test_current_baseline_is_complete_and_deterministic,
        test_every_required_category_is_nonempty_and_bounded,
        test_known_registry_values_are_preserved,
        test_source_integrity_and_xml_safety_fail_closed,
        test_registry_set_and_duplicate_keys_fail_closed,
        test_record_key_field_and_reference_limits_fail_closed,
        test_record_count_and_supporting_mapping_fail_closed,
        test_external_profile_revisions_are_unique_and_pinned,
    )
    for test in tests:
        test()
    print("registry baseline tests passed")


if __name__ == "__main__":
    run_tests()
