from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def main() -> int:
    failures: list[str] = []

    schema = load_json(ROOT / "schemas" / "gold-standard-asset.schema.json")
    example = load_json(ROOT / "examples" / "gold-standard" / "gold-standard-asset.example.json")["gold_standard_asset"]
    legal = load_json(ROOT / "examples" / "documents" / "legal-document.example.json")
    schema_registry = load_json(ROOT / "registry" / "schema-registry.json")
    source_of_truth = load_json(ROOT / "registry" / "source-of-truth.json")

    validator = Draft202012Validator(schema)
    for error in sorted(validator.iter_errors(example), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path)
        if location:
            failures.append(f"example validation: {location}: {error.message}")
        else:
            failures.append(f"example validation: {error.message}")

    document = legal["document"]
    source_artifact = legal["source_artifact"]
    document_version = legal["document_version"]
    components = {item["component_id"]: item for item in legal["components"]}
    span_selectors = {item["span_selector_id"]: item for item in legal["span_selectors"]}

    require(example["document_id"] == document["document_id"], "gold_standard_asset.document_id must resolve to the canonical document example", failures)
    require(example["document_version_id"] == document_version["document_version_id"], "gold_standard_asset.document_version_id must resolve to the canonical document version example", failures)
    require(example["access_policy_ref"] == document["access_policy_ref"], "gold_standard_asset.access_policy_ref must match the canonical document access policy in the example bundle", failures)
    require(source_artifact["source_artifact_id"] in example["source_artifact_refs"], "gold_standard_asset must reference the canonical source artifact used by the document version", failures)

    for component_id in example["component_ids"]:
        require(component_id in components, f"gold_standard_asset references missing component {component_id}", failures)
    for span_id in example["span_selector_ids"]:
        require(span_id in span_selectors, f"gold_standard_asset references missing span selector {span_id}", failures)
        if span_id in span_selectors:
            require(span_selectors[span_id].get("component_id") in example["component_ids"], f"gold_standard_asset span selector {span_id} must resolve to one of the asset components", failures)

    scope_refs = example.get("scope_refs", {})
    require(document["jurisdiction"] in scope_refs.get("jurisdiction_refs", []), "gold_standard_asset.scope_refs.jurisdiction_refs must include the canonical document jurisdiction in the example bundle", failures)
    for matter_ref in document.get("matter_refs", []):
        require(matter_ref in scope_refs.get("matter_refs", []), f"gold_standard_asset.scope_refs.matter_refs must include canonical document matter_ref {matter_ref}", failures)

    forbidden_derived_fields = {
        "retrieval_request_id",
        "retrieval_trace_id",
        "retrieval_response_id",
        "answer_event_id",
        "answer_evidence_ids",
        "chunk_ids",
        "index_build_id",
        "adapter_profile_id",
        "source_system",
    }
    for field_name in sorted(forbidden_derived_fields):
        require(field_name not in example, f"gold_standard_asset must not carry derived or adapter-local field {field_name}", failures)

    schemas = {entry["path"]: entry for entry in schema_registry.get("schemas", [])}
    gold_standard_entry = schemas.get("schemas/gold-standard-asset.schema.json")
    require(gold_standard_entry is not None, "schema-registry must include schemas/gold-standard-asset.schema.json", failures)
    if gold_standard_entry is not None:
        require(gold_standard_entry.get("status") == "draft", "gold-standard-asset must remain draft in schema-registry", failures)
        require(gold_standard_entry.get("layer") == "policy_and_governance", "gold-standard-asset must remain registered in the policy_and_governance layer", failures)

    layer_model = source_of_truth.get("layer_model", {})
    require("schemas/gold-standard-asset.schema.json" in layer_model.get("gold_standard_backbone", []), "source-of-truth layer_model.gold_standard_backbone must include schemas/gold-standard-asset.schema.json", failures)
    require("governance/GOLD_STANDARD_BACKBONE.md" in layer_model.get("gold_standard_backbone", []), "source-of-truth layer_model.gold_standard_backbone must include governance/GOLD_STANDARD_BACKBONE.md", failures)

    if failures:
        print("GOLD STANDARD BACKBONE VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Gold Standard backbone validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
