from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def path_exists(path_text: str) -> bool:
    normalized = path_text.rstrip("/")
    if not normalized:
        return False
    return (ROOT / normalized).exists()


def main() -> int:
    failures: list[str] = []

    source_of_truth = load_json(ROOT / "registry" / "source-of-truth.json")
    schema_registry = load_json(ROOT / "registry" / "schema-registry.json")

    system_map = load_text(ROOT / "governance" / "SYSTEM_MAP.md")
    canonical_document_model = load_text(ROOT / "governance" / "CANONICAL_DOCUMENT_MODEL.md")
    retrieval_architecture = load_text(ROOT / "governance" / "RETRIEVAL_ARCHITECTURE.md")
    gold_standard_backbone = load_text(ROOT / "governance" / "GOLD_STANDARD_BACKBONE.md")
    project_system_map = load_text(ROOT / "docs" / "architecture" / "PROJECT_SYSTEM_MAP.md")

    for key, rel_path in source_of_truth.get("authoritative_files", {}).items():
        require(path_exists(rel_path), f"authoritative_files.{key} references missing path {rel_path}", failures)

    precedence = source_of_truth.get("precedence_order", [])
    require(precedence[:4] == [
        "registry/source-of-truth.json",
        "registry/design-authority.json",
        "registry/ontology-registry.json",
        "registry/schema-registry.json",
    ], "precedence_order must begin with source-of-truth, design-authority, ontology-registry, and schema-registry", failures)
    for rel_path in precedence:
        if rel_path in source_of_truth.get("deprecated_paths", []):
            continue
        require(path_exists(rel_path), f"precedence_order references missing path {rel_path}", failures)

    layer_model = source_of_truth.get("layer_model", {})
    expected_layers = {
        "canonical_document_family",
        "gold_standard_backbone",
        "derived_document_and_evidence",
        "retrieval_and_access",
        "policy_and_governance",
        "action_and_runtime",
    }
    require(expected_layers.issubset(layer_model.keys()), "source-of-truth layer_model is missing one or more required boundary layers", failures)

    expected_paths = {
        "canonical_document_family": {
            "governance/CANONICAL_DOCUMENT_MODEL.md",
            "schemas/document.schema.json",
            "schemas/source-artifact.schema.json",
            "schemas/source-ingestion-manifest.schema.json",
            "schemas/document-version.schema.json",
            "schemas/canonical-text.schema.json",
            "schemas/component.schema.json",
            "schemas/span-selector.schema.json",
            "schemas/citation-mention.schema.json",
            "schemas/citation-target.schema.json",
        },
        "gold_standard_backbone": {
            "governance/GOLD_STANDARD_BACKBONE.md",
            "schemas/gold-standard-asset.schema.json",
        },
        "derived_document_and_evidence": {
            "schemas/chunk-set.schema.json",
            "schemas/chunk.schema.json",
            "schemas/embedding-set.schema.json",
            "schemas/index-build.schema.json",
            "schemas/answer-evidence.schema.json",
            "schemas/answer-event.schema.json",
        },
        "retrieval_and_access": {
            "governance/RETRIEVAL_ARCHITECTURE.md",
            "governance/PRIVILEGE_AWARE_RETRIEVAL.md",
            "schemas/retrieval-request.schema.json",
            "schemas/retrieval-trace.schema.json",
            "schemas/retrieval-response.schema.json",
            "schemas/access-decision.schema.json",
            "schemas/index-migration-plan.schema.json",
        },
    }
    for layer_name, paths in expected_paths.items():
        actual_paths = set(layer_model.get(layer_name, []))
        missing = sorted(paths - actual_paths)
        for rel_path in missing:
            failures.append(f"layer_model.{layer_name} is missing expected path {rel_path}")

    schemas = {entry["path"]: entry for entry in schema_registry.get("schemas", [])}
    for rel_path in expected_paths["canonical_document_family"] | expected_paths["derived_document_and_evidence"] | expected_paths["retrieval_and_access"] | expected_paths["gold_standard_backbone"]:
        if rel_path.startswith("schemas/"):
            require(rel_path in schemas, f"schema-registry is missing schema path {rel_path}", failures)

    gold_standard_entry = schemas.get("schemas/gold-standard-asset.schema.json")
    if gold_standard_entry:
        require(gold_standard_entry.get("status") == "draft", "gold-standard-asset must remain draft in schema-registry", failures)
    retrieval_request_entry = schemas.get("schemas/retrieval-request.schema.json")
    retrieval_response_entry = schemas.get("schemas/retrieval-response.schema.json")
    retrieval_trace_entry = schemas.get("schemas/retrieval-trace.schema.json")
    access_decision_entry = schemas.get("schemas/access-decision.schema.json")
    index_migration_entry = schemas.get("schemas/index-migration-plan.schema.json")
    for name, entry in (
        ("retrieval-request", retrieval_request_entry),
        ("retrieval-response", retrieval_response_entry),
        ("retrieval-trace", retrieval_trace_entry),
        ("access-decision", access_decision_entry),
        ("index-migration-plan", index_migration_entry),
    ):
        require(entry is not None and entry.get("status") == "active", f"{name} must be present and active in schema-registry", failures)

    require("retrieval-response does not supersede `retrieval-trace`".replace("`", "") in retrieval_architecture.replace("`", ""), "RETRIEVAL_ARCHITECTURE.md must state that retrieval-response does not supersede retrieval-trace", failures)
    require("Treat Gold Standard assets as thin canonical KM designations".lower() in " ".join(source_of_truth.get("interpretation_rules", [])).lower(), "source-of-truth interpretation_rules must include the Gold Standard canonical-boundary rule", failures)
    require("Treat source-ingestion-manifest as a metadata-only provenance gate".lower() in " ".join(source_of_truth.get("interpretation_rules", [])).lower(), "source-of-truth interpretation_rules must include the source-ingestion metadata gate rule", failures)
    require("Treat retrieval, answer, and index-migration contracts as derived control surfaces".lower() in " ".join(source_of_truth.get("interpretation_rules", [])).lower(), "source-of-truth interpretation_rules must include the retrieval/access derived-surface rule", failures)

    require("canonical document structure plus derived document and evidence artifacts" in system_map, "SYSTEM_MAP.md must distinguish canonical document structure from derived document and evidence artifacts", failures)
    require(
        "retrieval and access contracts" in system_map.lower()
        or "retrieval and access control contracts" in system_map.lower(),
        "SYSTEM_MAP.md must explicitly name retrieval and access contracts",
        failures,
    )
    require("derived document and evidence artifacts" in project_system_map.lower(), "PROJECT_SYSTEM_MAP.md must explicitly separate derived document and evidence artifacts", failures)
    require("retrieval and access control contracts" in project_system_map.lower(), "PROJECT_SYSTEM_MAP.md must explicitly separate retrieval and access control contracts", failures)
    require("The following are derived and rebuildable:" in canonical_document_model, "CANONICAL_DOCUMENT_MODEL.md must explicitly identify derived artifacts", failures)
    require("source-ingestion-manifest" in canonical_document_model, "CANONICAL_DOCUMENT_MODEL.md must document the source-ingestion-manifest ingestion gate", failures)
    require("retrieval, ranking, answer generation, and telemetry remain derived".lower() in gold_standard_backbone.lower(), "GOLD_STANDARD_BACKBONE.md must keep retrieval and answer artifacts derived", failures)

    if failures:
        print("SOURCE-OF-TRUTH COHERENCE VALIDATION FAILURES:")
        for failure in failures:
            if failure:
                print(f"- {failure}")
        return 1

    print("Source-of-truth, schema-registry, and doctrine coherence validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
