from __future__ import annotations

import json
import re
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


SCHEMA_PATH = ROOT / "schemas" / "source-ingestion-manifest.schema.json"
LEGAL_BUNDLE_PATH = ROOT / "examples" / "documents" / "legal-document.example.json"
MANIFEST_PATH = ROOT / "examples" / "documents" / "source-ingestion-manifest.example.json"
CONTENT_FIELDS = {
    "body",
    "canonical_text",
    "content",
    "exact_text",
    "full_text",
    "raw_text",
    "text",
}
STRUCTURED_IDENTIFIER_FIELDS = {
    "source_type",
    "source_system",
    "source_identifier",
    "confidentiality_class",
    "access_policy_ref",
    "steward_ref",
    "steward_role",
    "originating_repository",
    "retention_rule",
}
ACTIVE_READY_STATUSES = {"approved", "active"}
WHITESPACE_PATTERN = re.compile(r"\s")


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def collect_failures(legal_bundle: dict, manifest: dict) -> list[str]:
    failures: list[str] = []
    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema, registry=build_local_schema_registry(ROOT))

    for error in sorted(validator.iter_errors(manifest), key=lambda item: list(item.path)):
        location = ".".join(str(part) for part in error.path)
        if location:
            failures.append(f"manifest validation: {location}: {error.message}")
        else:
            failures.append(f"manifest validation: {error.message}")

    for field_name in sorted(CONTENT_FIELDS):
        require(
            field_name not in manifest,
            f"source-ingestion-manifest must remain metadata-only and may not embed '{field_name}'",
            failures,
        )

    for field_name in sorted(STRUCTURED_IDENTIFIER_FIELDS):
        value = manifest.get(field_name)
        if isinstance(value, str):
            require(
                WHITESPACE_PATTERN.search(value) is None,
                f"source-ingestion-manifest.{field_name} must remain identifier-shaped and may not embed source text",
                failures,
            )

    document = legal_bundle.get("document", {})
    source_artifact = legal_bundle.get("source_artifact", {})
    document_version = legal_bundle.get("document_version", {})

    require(
        manifest.get("document_id") == document.get("document_id"),
        "source-ingestion-manifest.document_id must resolve to the canonical document example",
        failures,
    )
    require(
        manifest.get("source_artifact_id") == source_artifact.get("source_artifact_id"),
        "source-ingestion-manifest.source_artifact_id must resolve to the canonical source artifact example",
        failures,
    )
    require(
        source_artifact.get("document_id") == manifest.get("document_id"),
        "source-ingestion-manifest must stay aligned to the source artifact document_id",
        failures,
    )
    require(
        document_version.get("source_artifact_id") == manifest.get("source_artifact_id"),
        "source-ingestion-manifest must stay aligned to the active document-version source artifact",
        failures,
    )
    require(
        manifest.get("source_system") == source_artifact.get("source_system"),
        "source-ingestion-manifest.source_system must match the source artifact source_system",
        failures,
    )
    require(
        manifest.get("source_identifier") == source_artifact.get("source_identifier"),
        "source-ingestion-manifest.source_identifier must match the source artifact source_identifier",
        failures,
    )
    require(
        manifest.get("capture_time") == source_artifact.get("capture_time"),
        "source-ingestion-manifest.capture_time must match the source artifact capture_time",
        failures,
    )
    require(
        manifest.get("checksum") == source_artifact.get("checksum"),
        "source-ingestion-manifest.checksum must match the source artifact checksum",
        failures,
    )
    require(
        manifest.get("access_policy_ref") == document.get("access_policy_ref"),
        "source-ingestion-manifest.access_policy_ref must match the canonical document access policy",
        failures,
    )

    source_systems = document.get("source_systems", [])
    if isinstance(source_systems, list) and source_systems:
        require(
            manifest.get("source_system") in source_systems,
            "source-ingestion-manifest.source_system must be listed in document.source_systems",
            failures,
        )

    document_steward_role = document.get("steward_role")
    if document_steward_role and "steward_role" in manifest:
        require(
            manifest.get("steward_role") == document_steward_role,
            "source-ingestion-manifest.steward_role must match the canonical document steward_role when both are present",
            failures,
        )
    elif document_steward_role:
        require(
            "steward_ref" in manifest,
            "source-ingestion-manifest must carry steward_ref or steward_role for governed sources",
            failures,
        )

    if document.get("canonical_status") == "active":
        require(
            manifest.get("lifecycle_status") in ACTIVE_READY_STATUSES,
            "active governed source examples require a source-ingestion-manifest with lifecycle_status approved or active",
            failures,
        )

    return failures


def main() -> int:
    failures = collect_failures(
        load_json(LEGAL_BUNDLE_PATH),
        load_json(MANIFEST_PATH),
    )

    if failures:
        print("SOURCE INGESTION MANIFEST VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Source ingestion manifest validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
