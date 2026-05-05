from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def load_primary_schema_ids() -> dict[str, str]:
    registry = load_json(BASE / "registry" / "schema-registry.json")
    mapping: dict[str, str] = {}
    for entry in registry.get("schemas", []):
        path = entry.get("path")
        schema_id = entry.get("schema_id")
        if path and schema_id:
            mapping[path] = schema_id
    return mapping


PRIMARY_SCHEMA_IDS = load_primary_schema_ids()


def matches_expected_schema(
    data: dict,
    expected_type: str,
    expected_version: str,
    expected_schema_id: str | None = None,
) -> bool:
    if data.get("schema_type") == expected_type and data.get("schema_version") == expected_version:
        return True
    return expected_schema_id is not None and data.get("schema_id") == expected_schema_id


def should_validate(
    file_path: Path,
    expected_type: str,
    expected_version: str,
    expected_schema_id: str | None = None,
) -> bool:
    try:
        data = load_json(file_path)
    except Exception:
        return False
    return matches_expected_schema(data, expected_type, expected_version, expected_schema_id)


def validate_directory(
    schema_path: Path,
    target_dir: Path,
    expected_type: str,
    expected_version: str,
    expected_schema_id: str | None = None,
):
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, registry=build_local_schema_registry(BASE))

    if not target_dir.exists():
        print(f"SKIP: {target_dir} does not exist")
        return 0

    failures = 0
    matched = 0
    for file_path in sorted(target_dir.rglob("*.json")):
        if "legacy" in file_path.parts:
            print(f"SKIP LEGACY: {file_path}")
            continue
        if not should_validate(file_path, expected_type, expected_version, expected_schema_id):
            print(f"SKIP SCHEMA MISMATCH: {file_path}")
            continue
        matched += 1
        data = load_json(file_path)
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            failures += 1
            print(f"INVALID: {file_path}")
            for error in errors:
                path = ".".join(str(p) for p in error.path) or "<root>"
                print(f"  - {path}: {error.message}")
        else:
            print(f"VALID: {file_path}")

    if matched == 0:
        print(f"SKIP: no {expected_type}:{expected_version} examples found in {target_dir}")
    return failures


def main() -> int:
    validations = [
        (
            BASE / "schemas" / "claim_v3.schema.json",
            BASE / "examples" / "claims",
            "claim",
            "v3",
            PRIMARY_SCHEMA_IDS.get("schemas/claim_v3.schema.json"),
        ),
        (
            BASE / "schemas" / "artifact.schema.json",
            BASE / "examples" / "artifacts",
            "artifact",
            "v1",
            PRIMARY_SCHEMA_IDS.get("schemas/artifact.schema.json"),
        ),
        (
            BASE / "schemas" / "exception-event.schema.json",
            BASE / "examples" / "exceptions" / "events",
            "exception-event",
            "v1",
            PRIMARY_SCHEMA_IDS.get("schemas/exception-event.schema.json"),
        ),
        (
            BASE / "schemas" / "pressure-vector.schema.json",
            BASE / "examples" / "exceptions" / "pressure-vectors",
            "pressure-vector",
            "v1",
            PRIMARY_SCHEMA_IDS.get("schemas/pressure-vector.schema.json"),
        ),
        (
            BASE / "schemas" / "adaptation-proposal.schema.json",
            BASE / "examples" / "exceptions" / "adaptation-proposals",
            "adaptation-proposal",
            "v1",
            PRIMARY_SCHEMA_IDS.get("schemas/adaptation-proposal.schema.json"),
        ),
        (
            BASE / "schemas" / "promotion-decision.schema.json",
            BASE / "examples" / "exceptions" / "promotion-decisions",
            "promotion-decision",
            "v1",
            PRIMARY_SCHEMA_IDS.get("schemas/promotion-decision.schema.json"),
        ),
        (
            BASE / "schemas" / "view-executive-brief.schema.json",
            BASE / "examples" / "innovation-os",
            "view-executive-brief",
            "draft-v1",
            PRIMARY_SCHEMA_IDS.get("schemas/view-executive-brief.schema.json"),
        ),
    ]

    failures = 0
    for schema_path, target_dir, expected_type, expected_version, expected_schema_id in validations:
        if not schema_path.exists():
            print(f"MISSING SCHEMA: {schema_path}")
            failures += 1
            continue
        failures += validate_directory(
            schema_path,
            target_dir,
            expected_type,
            expected_version,
            expected_schema_id,
        )

    if failures:
        print(f"Repository vNext validation failed with {failures} error group(s).")
        return 1

    print("Repository vNext validation completed successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
