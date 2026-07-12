#!/usr/bin/env python3
"""Generate and verify Vardheim's bounded ACME registry baseline."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
import xml.parsers.expat as expat
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
REGISTRY_DIR = ROOT / "registry"
SOURCE = REGISTRY_DIR / "iana-acme.xml"
CHECKSUMS = REGISTRY_DIR / "SHA256SUMS"
OUTPUT = REGISTRY_DIR / "REGISTRY_BASELINE.json"
EXTERNAL_SOURCE_POLICY = REGISTRY_DIR / "EXTERNAL_SOURCES.json"
RFC_INDEX = ROOT / "rfc/SECTION_INDEX.json"
CHECKED_AT = "2026-07-12"
IANA_SOURCE = "https://www.iana.org/assignments/acme/acme.xml"
NAMESPACE = "http://www.iana.org/assignments"
NS = f"{{{NAMESPACE}}}"
REGISTRY_SOURCE_FILES = (
    "iana-acme.xml",
    "iana-bundle.xml",
    "iana-cose.xml",
    "iana-smi-numbers.xml",
)

LIMITS = {
    "source_bytes": 65_536,
    "registries": 32,
    "records_total": 256,
    "records_per_registry": 128,
    "fields_per_record": 16,
    "references_per_record": 8,
    "text_bytes": 4_096,
}

EXPECTED_REGISTRIES = (
    "acme-account-object-fields",
    "acme-order-object-fields",
    "acme-authorization-object-fields",
    "acme-error-types",
    "acme-resource-types",
    "acme-directory-metadata-fields",
    "acme-identifier-types",
    "acme-validation-methods",
    "acme-order-auto-renewal-fields",
    "acme-directory-metadata-auto-renewal-fields",
    "acme-star-delegation-csr-template-extensions",
    "acme-authority-token-challenge-types",
    "acme-renewalinfo-object-fields",
)

EXPECTED_RECORD_COUNTS = {
    "acme-account-object-fields": 7,
    "acme-order-object-fields": 14,
    "acme-authorization-object-fields": 6,
    "acme-error-types": 31,
    "acme-resource-types": 8,
    "acme-directory-metadata-fields": 9,
    "acme-identifier-types": 6,
    "acme-validation-methods": 12,
    "acme-order-auto-renewal-fields": 5,
    "acme-directory-metadata-auto-renewal-fields": 3,
    "acme-star-delegation-csr-template-extensions": 3,
    "acme-authority-token-challenge-types": 1,
    "acme-renewalinfo-object-fields": 2,
}

REQUIRED_CATEGORIES = {
    "fields": (
        "acme-account-object-fields",
        "acme-order-object-fields",
        "acme-authorization-object-fields",
        "acme-directory-metadata-fields",
        "acme-order-auto-renewal-fields",
        "acme-directory-metadata-auto-renewal-fields",
        "acme-renewalinfo-object-fields",
    ),
    "errors": ("acme-error-types",),
    "resources": ("acme-resource-types",),
    "identifiers": ("acme-identifier-types",),
    "validation_methods": ("acme-validation-methods",),
    "extensions": (
        "acme-star-delegation-csr-template-extensions",
        "acme-authority-token-challenge-types",
    ),
}

HTTP_REPLACEMENTS = (
    (2818, (9110,), "HTTP over TLS semantics"),
    (7230, (9110, 9112), "HTTP semantics and HTTP/1.1 messaging"),
    (7231, (9110,), "HTTP semantics"),
    (7232, (9110,), "conditional HTTP semantics"),
    (7233, (9110,), "range request semantics"),
    (7234, (9111,), "HTTP caching"),
    (7235, (9110,), "HTTP authentication semantics"),
    (7807, (9457,), "problem details for HTTP APIs"),
)

EXTERNAL_PROFILES = (
    {
        "id": "cabf-tls-br",
        "authority": "CA/Browser Forum Server Certificate Working Group",
        "title": "Baseline Requirements for TLS Server Certificates",
        "revision": "2.2.8",
        "status": "current",
        "source": "https://cabforum.org/working-groups/server/baseline-requirements/documents/",
        "revision_source": "https://github.com/cabforum/servercert/releases/tag/BRs/v2.2.8",
    },
    {
        "id": "cabf-smime-br",
        "authority": "CA/Browser Forum S/MIME Certificate Working Group",
        "title": "S/MIME Baseline Requirements",
        "revision": "1.0.14",
        "status": "current",
        "source": "https://cabforum.org/working-groups/smime/requirements/",
        "revision_source": "https://github.com/cabforum/smime/releases/tag/Ballot_SMC016",
    },
    {
        "id": "cabf-network-security",
        "authority": "CA/Browser Forum Network Security Working Group",
        "title": "Network and Certificate System Security Requirements",
        "revision": "2.0.5",
        "status": "current",
        "source": "https://cabforum.org/working-groups/netsec/requirements/",
        "revision_source": "https://github.com/cabforum/netsec/releases/tag/v2.0.5",
    },
    {
        "id": "3gpp-ts-33.310",
        "authority": "3GPP",
        "title": "Network Domain Security; Authentication Framework",
        "revision": "19.5.0",
        "status": "under-change-control",
        "source": "https://portal.3gpp.org/desktopmodules/Specifications/SpecificationDetails.aspx?specificationId=2293",
        "revision_source": "https://www.3gpp.org/ftp/Specs/archive/33_series/33.310/33310-j50.zip",
    },
)


class RegistryError(RuntimeError):
    """A malformed, unsafe, incomplete, or drifting registry baseline."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RegistryError(message)


def bounded_text(element: ET.Element, label: str) -> str:
    value = " ".join("".join(element.itertext()).split())
    require(bool(value), f"empty {label}")
    require(len(value.encode("utf-8")) <= LIMITS["text_bytes"], f"oversized {label}")
    return value


def source_hashes() -> dict[str, str]:
    lines = CHECKSUMS.read_text(encoding="ascii").splitlines()
    result: dict[str, str] = {}
    for line in lines:
        match = re.fullmatch(r"([0-9a-f]{64})  (iana-[a-z-]+\.xml)", line)
        require(match is not None, "malformed registry checksum manifest")
        name = match.group(2)
        require(name not in result, f"duplicate registry checksum: {name}")
        result[name] = match.group(1)
    require(tuple(sorted(result)) == tuple(sorted(REGISTRY_SOURCE_FILES)), "registry checksum file set differs")
    for name, expected in result.items():
        path = REGISTRY_DIR / name
        require(path.is_file(), f"missing registry source: {name}")
        content = path.read_bytes()
        require(len(content) <= 1_048_576, f"registry source is oversized: {name}")
        require(hashlib.sha256(content).hexdigest() == expected, f"registry source hash differs: {name}")
    return result


def reference(element: ET.Element) -> dict[str, str]:
    kind = element.get("type", "")
    data = element.get("data", "")
    require(bool(kind) and bool(data), "registry reference lacks type or data")
    require(len(kind.encode()) <= LIMITS["text_bytes"], "oversized reference type")
    require(len(data.encode()) <= LIMITS["text_bytes"], "oversized reference data")
    result = {"type": kind, "data": data}
    label = " ".join("".join(element.itertext()).split())
    if label:
        require(len(label.encode("utf-8")) <= LIMITS["text_bytes"], "oversized reference label")
        result["label"] = label
    return result


def reject_unsafe_xml(content: bytes) -> None:
    parser = expat.ParserCreate()

    def reject_doctype(*_arguments) -> None:
        raise RegistryError("unsafe XML DOCTYPE declaration")

    def reject_entity(*_arguments) -> None:
        raise RegistryError("unsafe XML entity declaration")

    parser.StartDoctypeDeclHandler = reject_doctype
    parser.EntityDeclHandler = reject_entity
    parser.UnparsedEntityDeclHandler = reject_entity
    parser.ExternalEntityRefHandler = reject_entity
    parser.SetParamEntityParsing(expat.XML_PARAM_ENTITY_PARSING_NEVER)
    try:
        parser.Parse(content, True)
    except RegistryError:
        raise
    except expat.ExpatError as error:
        raise RegistryError(f"malformed IANA XML: {error}") from error


def registry_key_fields(registry_id: str) -> tuple[str, ...]:
    if registry_id == "acme-error-types":
        return ("type",)
    if registry_id == "acme-validation-methods":
        return ("name", "type")
    return ("name",)


def parse_record(element: ET.Element, key_fields: tuple[str, ...]) -> dict:
    fields: dict[str, str] = {}
    for child in element:
        name = child.tag.removeprefix(NS)
        if name == "xref":
            continue
        require(name not in fields, f"duplicate record field: {name}")
        fields[name] = bounded_text(child, f"record field {name}")
    require(all(fields.get(name) for name in key_fields), "registry record has no primary key")
    require(len(fields) <= LIMITS["fields_per_record"], "record has too many fields")
    references = [reference(item) for item in element.iter(f"{NS}xref")]
    identity = "/".join(fields[name] for name in key_fields)
    require(bool(references), f"record {identity} has no source reference")
    require(
        len(references) <= LIMITS["references_per_record"],
        f"record {identity} has too many references",
    )
    result: dict[str, object] = {"fields": fields, "references": references}
    for attribute in ("date", "updated"):
        value = element.get(attribute)
        if value is not None:
            require(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", value) is not None, f"invalid record {attribute}")
            result[attribute] = value
    return result


def record_key(registry_id: str, record: dict) -> tuple[str, ...]:
    fields = record["fields"]
    require(isinstance(fields, dict), f"{registry_id} record fields are malformed")
    names = registry_key_fields(registry_id)
    values = tuple(str(fields.get(name, "")) for name in names)
    require(all(values), f"{registry_id} record has an incomplete key")
    return values


def parse_registry(element: ET.Element) -> dict:
    registry_id = element.get("id", "")
    title_element = element.find(f"{NS}title")
    rule_element = element.find(f"{NS}registration_rule")
    expert_element = element.find(f"{NS}expert")
    require(title_element is not None, f"{registry_id} has no title")
    require(rule_element is not None, f"{registry_id} has no registration rule")
    require(expert_element is not None, f"{registry_id} has no expert")
    key_fields = registry_key_fields(registry_id)
    records = [parse_record(item, key_fields) for item in element.findall(f"{NS}record")]
    require(bool(records), f"{registry_id} has no records")
    require(len(records) <= LIMITS["records_per_registry"], f"{registry_id} has too many records")
    require(
        len(records) == EXPECTED_RECORD_COUNTS.get(registry_id),
        f"{registry_id} record count differs",
    )
    keys = [record_key(registry_id, item) for item in records]
    require(len(keys) == len(set(keys)), f"{registry_id} has duplicate record keys")
    references = [reference(item) for item in element.findall(f"{NS}xref")]
    require(bool(references), f"{registry_id} has no registry reference")
    return {
        "id": registry_id,
        "title": bounded_text(title_element, f"{registry_id} title"),
        "registration_rule": bounded_text(rule_element, f"{registry_id} rule"),
        "experts": bounded_text(expert_element, f"{registry_id} experts"),
        "references": references,
        "key_fields": list(key_fields),
        "records": records,
    }


def parse_iana(content: bytes, *, verify_hash: bool = True) -> dict:
    require(len(content) <= LIMITS["source_bytes"], "IANA registry source is oversized")
    reject_unsafe_xml(content)
    digest = hashlib.sha256(content).hexdigest()
    if verify_hash:
        require(digest == source_hashes()[SOURCE.name], "IANA registry source hash differs")
    try:
        root = ET.fromstring(content)
    except ET.ParseError as error:
        raise RegistryError(f"malformed IANA XML: {error}") from error
    require(root.tag == f"{NS}registry" and root.get("id") == "acme", "unexpected IANA registry root")
    require(
        all(isinstance(item.tag, str) and item.tag.startswith(NS) for item in root.iter()),
        "unexpected IANA XML namespace",
    )
    updated = root.findtext(f"{NS}updated", default="")
    require(re.fullmatch(r"[0-9]{4}-[0-9]{2}-[0-9]{2}", updated) is not None, "invalid IANA update date")
    elements = root.findall(f"{NS}registry")
    require(len(elements) <= LIMITS["registries"], "too many IANA registries")
    actual_ids = tuple(item.get("id", "") for item in elements)
    require(actual_ids == EXPECTED_REGISTRIES, "IANA ACME registry set or order differs")
    registries = [parse_registry(item) for item in elements]
    record_count = sum(len(item["records"]) for item in registries)
    require(record_count <= LIMITS["records_total"], "too many IANA records")
    require(record_count > 0, "IANA registry baseline is empty")
    return {
        "authority": "IANA",
        "source": IANA_SOURCE,
        "source_sha256": digest,
        "source_updated": updated,
        "record_count": record_count,
        "required_categories": {
            category: list(registry_ids)
            for category, registry_ids in REQUIRED_CATEGORIES.items()
        },
        "registries": registries,
    }


def supporting_standards() -> list[dict]:
    inventory = json.loads(RFC_INDEX.read_text(encoding="utf-8"))
    documents = inventory.get("documents")
    require(isinstance(documents, list), "RFC section inventory has no documents")
    result = []
    for item in documents:
        require(isinstance(item, dict), "RFC section inventory entry is malformed")
        if item.get("role") == "acme":
            continue
        rfc = item.get("rfc")
        role = item.get("role")
        source = item.get("source")
        digest = item.get("sha256")
        require(isinstance(rfc, int) and rfc > 0, "supporting RFC number is invalid")
        require(isinstance(role, str) and bool(role), f"RFC {rfc} role is invalid")
        require(isinstance(source, str) and source.startswith("https://"), f"RFC {rfc} source is invalid")
        require(
            isinstance(digest, str) and re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
            f"RFC {rfc} hash is invalid",
        )
        result.append({"rfc": rfc, "role": role, "source": source, "sha256": digest})
    require(bool(result), "supporting-standard inventory is empty")
    require(len(result) == 92, "supporting-standard inventory count differs")
    require(len({item["rfc"] for item in result}) == len(result), "duplicate supporting RFC")
    return result


def http_replacements(tracked: set[int]) -> list[dict]:
    result = []
    for obsolete, replacements, scope in HTTP_REPLACEMENTS:
        require(set(replacements) <= tracked, f"HTTP replacement for RFC {obsolete} is not tracked")
        result.append(
            {
                "obsolete_rfc": obsolete,
                "replacement_rfcs": list(replacements),
                "scope": scope,
                "source": f"https://www.rfc-editor.org/info/rfc{replacements[0]}",
            }
        )
    return result


def external_profiles() -> list[dict[str, str]]:
    profiles = [dict(item) for item in EXTERNAL_PROFILES]
    identifiers = [item["id"] for item in profiles]
    require(len(identifiers) == len(set(identifiers)), "duplicate external profile")
    for item in profiles:
        require(all(bool(value) for value in item.values()), f"external profile {item['id']} is incomplete")
        require(item["source"].startswith("https://"), f"external profile {item['id']} source is invalid")
        require(
            item["revision_source"].startswith("https://"),
            f"external profile {item['id']} revision source is invalid",
        )
    return profiles


def external_normative_sources() -> list[dict[str, str]]:
    policy = json.loads(EXTERNAL_SOURCE_POLICY.read_text(encoding="utf-8"))
    require(policy.get("schema") == 1, "external source policy schema differs")
    sources = policy.get("sources")
    require(isinstance(sources, list), "external source policy has no sources")
    normalized: list[dict[str, str]] = []
    for item in sources:
        require(isinstance(item, dict), "external source entry is malformed")
        require(
            set(item) == {"reference", "authority", "title", "revision", "status", "source"},
            "external source fields differ",
        )
        require(all(isinstance(value, str) and bool(value) for value in item.values()), "external source entry is incomplete")
        normalized.append(dict(item))
    references = [item["reference"] for item in normalized]
    require(len(references) == len(set(references)), "duplicate external source reference")
    inventory = json.loads(RFC_INDEX.read_text(encoding="utf-8"))
    expected = inventory.get("normative_acme_external_references")
    require(isinstance(expected, list), "RFC inventory has no external reference set")
    require(set(references) == set(expected), "external normative source set differs")
    hashes = source_hashes()
    for item in normalized:
        source = item["source"]
        if source.startswith("registry/"):
            name = Path(source).name
            require(item["revision"] == f"sha256:{hashes.get(name, '')}", f"external source revision differs: {name}")
        else:
            require(source.startswith("https://"), f"external source URL is invalid: {item['reference']}")
    return normalized


def build_baseline(content: bytes | None = None, *, verify_hash: bool = True) -> dict:
    source = SOURCE.read_bytes() if content is None else content
    standards = supporting_standards()
    tracked = {item["rfc"] for item in standards}
    return {
        "schema": 1,
        "checked_at": CHECKED_AT,
        "limits": LIMITS,
        "iana_acme": parse_iana(source, verify_hash=verify_hash),
        "http_replacements": http_replacements(tracked),
        "supporting_standards": standards,
        "external_normative_sources": external_normative_sources(),
        "external_profiles": external_profiles(),
    }


def render(baseline: dict) -> str:
    return json.dumps(baseline, indent=2, ensure_ascii=False) + "\n"


def check() -> None:
    expected = render(build_baseline())
    require(OUTPUT.is_file(), "generated registry baseline is missing")
    require(OUTPUT.read_text(encoding="utf-8") == expected, "registry baseline is stale; run with --write")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--write", action="store_true", help="Regenerate the baseline")
    args = parser.parse_args()
    try:
        if args.write:
            OUTPUT.write_text(render(build_baseline()), encoding="utf-8")
            print(f"wrote {OUTPUT.relative_to(ROOT)}")
        else:
            check()
            print("ACME registry baseline is complete and current")
    except (RegistryError, OSError, UnicodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        print(f"registry baseline invalid: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
