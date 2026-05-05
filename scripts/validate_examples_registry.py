import json
import os
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

BASE = os.path.dirname(os.path.dirname(__file__))
if BASE not in sys.path:
    sys.path.insert(0, BASE)

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


# Known compound examples that intentionally have no top-level registry metadata
# because they bundle multiple typed sub-objects. Each is validated by a
# dedicated validator listed here so the SKIP line stays truthful rather than
# looking like a silent coverage hole. Keep this map tight: unknown files
# without registry metadata should still print the generic SKIP message so real
# missing metadata is not masked.
COMPOUND_EXAMPLE_COVERAGE = {
    "examples/documents/legal-document.example.json": "scripts/validate_examples_canonical.py",
    "examples/documents/chunk-set.example.json": "scripts/validation/validate_canonical_grounding_chain.py",
    "examples/documents/answer-trace.example.json": "scripts/validation/validate_canonical_grounding_chain.py",
    "examples/gold-standard/gold-standard-asset.example.json": "scripts/validate_examples_canonical.py",
}


def _build_registry_lookups(reg_path):
    """Build registry lookups from registry/schema-registry.json."""
    with open(reg_path) as f:
        raw = json.load(f)
    if isinstance(raw, dict) and "schemas" not in raw:
        raise ValueError(
            "validate_examples_registry.py now expects registry/schema-registry.json "
            "to be the authoritative schema registry format."
        )

    schemas = raw.get("schemas", []) if isinstance(raw, dict) else raw
    lookup_by_key = {}
    lookup_by_id = {}
    for entry in schemas:
        path = entry.get("path")
        schema_id = entry.get("schema_id")
        major = entry.get("version", "1.0.0").split(".")[0]
        if schema_id:
            lookup_by_id[schema_id] = entry
        for applies in entry.get("applies_to", []):
            key = f"{applies}:v{major}"
            if key not in lookup_by_key:
                lookup_by_key[key] = entry
    return lookup_by_key, lookup_by_id


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_registry_entry(data, registry_by_key, registry_by_id):
    schema_type = data.get("schema_type")
    schema_version = data.get("schema_version")
    schema_id = data.get("schema_id")

    if schema_type and schema_version:
        key = f"{schema_type}:{schema_version}"
        entry = registry_by_key.get(key)
        if entry:
            return key, entry

    if schema_id:
        entry = registry_by_id.get(schema_id)
        if entry:
            return schema_id, entry

    return None, None


def classify_registry_resolution(data, registry_by_key, registry_by_id):
    registry_label, registry_entry = resolve_registry_entry(data, registry_by_key, registry_by_id)
    declared = (
        data.get("schema_id") is not None
        or (
            data.get("schema_type") is not None
            and data.get("schema_version") is not None
        )
    )
    if registry_entry is not None:
        return "resolved", registry_label, registry_entry
    if declared:
        return "declared_unresolved", None, None
    return "missing", None, None


def validate_file(path, failures, registry_by_key, registry_by_id):
    data = load_json(path)

    resolution, registry_label, registry_entry = classify_registry_resolution(
        data,
        registry_by_key,
        registry_by_id,
    )
    if resolution == "missing":
        rel = os.path.relpath(path, BASE).replace(os.sep, "/")
        covered_by = COMPOUND_EXAMPLE_COVERAGE.get(rel)
        if covered_by:
            print(
                f"SKIP (compound example; no top-level registry metadata; "
                f"validated by {covered_by}): {path}"
            )
        else:
            print(f"SKIP (no registry metadata): {path}")
        return
    if resolution == "declared_unresolved":
        failures.append(f"UNRESOLVED REGISTRY METADATA: {path}")
        failures.append(
            "  - declared schema metadata did not resolve in registry/schema-registry.json"
        )
        return

    schema_path = os.path.join(BASE, registry_entry["path"])
    schema = load_json(schema_path)

    validator = Draft202012Validator(
        schema,
        registry=build_local_schema_registry(Path(BASE)),
    )
    errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
    if errors:
        failures.append(f"INVALID ({registry_label}): {path}")
        for error in errors:
            field = ".".join(str(part) for part in error.path) or "<root>"
            failures.append(f"  - {field}: {error.message}")
        return

    print(f"VALID ({registry_label}): {path}")


def walk_and_validate(root):
    failures = []
    registry_by_key, registry_by_id = _build_registry_lookups(
        os.path.join(BASE, "registry", "schema-registry.json")
    )
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in {"legacy", "archive", "__pycache__"}]
        for filename in filenames:
            if filename.endswith(".json"):
                validate_file(
                    os.path.join(dirpath, filename),
                    failures,
                    registry_by_key,
                    registry_by_id,
                )
    return failures


def main():
    failures = walk_and_validate(os.path.join(BASE, "examples"))
    if failures:
        print("Registry-based validation failures:")
        for failure in failures:
            print(f"- {failure}")
        raise SystemExit(1)
    print("Registry-based validation complete.")


if __name__ == "__main__":
    main()
