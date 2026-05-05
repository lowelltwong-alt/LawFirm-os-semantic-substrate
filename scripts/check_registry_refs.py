from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]

FILES_TO_CHECK = [
    ROOT / "registry" / "source-of-truth.json",
    ROOT / "registry" / "design-authority.json",
    ROOT / "registry" / "ontology-registry.json",
    ROOT / "registry" / "schema-registry.json",
    ROOT / "governance" / "canonical_spine_manifest.json",
]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def require_exists(path: Path, label: str, failures: list[str]) -> None:
    if not path.exists():
        failures.append(f"Missing {label}: {path.relative_to(ROOT)}")


def check_registry_paths(registry: dict | list, failures: list[str]) -> None:
    """Check that every schema path in the registry actually exists on disk.

    Supports both the old flat-dict format ({"key": "path"}) and the new
    registry/schema-registry.json format ({"schemas": [{"schema_id": ..., "path": ...}]}).
    """
    if isinstance(registry, dict) and "schemas" in registry:
        # New nested format
        entries = registry["schemas"]
        for entry in entries:
            if not isinstance(entry, dict):
                failures.append(
                    f"Registry schema entry must be an object, found {type(entry).__name__}"
                )
                continue
            rel_path = entry.get("path")
            schema_id = entry.get("schema_id", "unknown")
            if rel_path is None:
                continue
            if not isinstance(rel_path, str):
                failures.append(
                    f"Registry target path for {schema_id} must be a string, found {type(rel_path).__name__}"
                )
                continue
            target = ROOT / rel_path
            if not target.exists():
                failures.append(f"Registry target missing for {schema_id}: {rel_path}")
    elif isinstance(registry, dict):
        # Old flat-dict format: {"key": "path"}
        for key, rel_path in sorted(registry.items()):
            if isinstance(rel_path, str):
                target = ROOT / rel_path
                if not target.exists():
                    failures.append(f"Registry target missing for {key}: {rel_path}")


def check_source_of_truth(doc: dict, failures: list[str]) -> None:
    authoritative = doc.get("authoritative_files", {})
    if isinstance(authoritative, dict):
        for key, rel_path in sorted(authoritative.items()):
            target = ROOT / rel_path
            if not target.exists():
                failures.append(f"authoritative_files target missing for {key}: {rel_path}")
    elif isinstance(authoritative, list):
        for rel_path in authoritative:
            target = ROOT / rel_path
            if not target.exists():
                failures.append(f"authoritative_files target missing: {rel_path}")

    for item in doc.get("precedence_order", []):
        if isinstance(item, str):
            target = ROOT / item
            if not target.exists():
                failures.append(f"precedence_order target missing: {item}")

    for _, paths in doc.get("layer_model", {}).items():
        if isinstance(paths, list):
            for rel_path in paths:
                target = ROOT / rel_path
                if not target.exists():
                    failures.append(f"layer_model target missing: {rel_path}")


def check_design_authority(doc: dict, failures: list[str]) -> None:
    for _, value in sorted(doc.items()):
        if isinstance(value, str) and value.endswith((".md", ".json", ".yaml", ".yml", ".ttl", ".py")):
            target = ROOT / value
            if not target.exists():
                failures.append(f"design-authority target missing: {value}")


def check_canonical_spine(doc: dict, failures: list[str]) -> None:
    for rel_path in doc.get("canonical_schemas", []):
        target = ROOT / rel_path
        if not target.exists():
            failures.append(f"canonical_schemas target missing: {rel_path}")
    for rel_path in doc.get("validation_scripts", []):
        target = ROOT / rel_path
        if not target.exists():
            failures.append(f"validation_scripts target missing: {rel_path}")


def main() -> int:
    failures: list[str] = []
    for path in FILES_TO_CHECK:
        require_exists(path, path.name, failures)
    if failures:
        print("Registry reference check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    schema_registry = load_json(ROOT / "registry" / "schema-registry.json")
    check_registry_paths(schema_registry, failures)

    source_of_truth = load_json(ROOT / "registry" / "source-of-truth.json")
    check_source_of_truth(source_of_truth, failures)

    design_authority = load_json(ROOT / "registry" / "design-authority.json")
    check_design_authority(design_authority, failures)

    canonical_spine = load_json(ROOT / "governance" / "canonical_spine_manifest.json")
    check_canonical_spine(canonical_spine, failures)

    if failures:
        print("Registry reference check failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Registry reference check passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
