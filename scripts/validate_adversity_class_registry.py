#!/usr/bin/env python3
"""Validate the closed synthetic adversity-class candidate registry."""

from __future__ import annotations

import argparse
from hashlib import sha256
import json
import sys
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "adversity-class-registry.candidate.json"
SCHEMA = ROOT / "schemas" / "adversity-class-registry.schema.json"
SCHEMA_REGISTRY = ROOT / "registry" / "schema-registry.json"
FRONT_DOOR = ROOT / "registry" / "ai-front-door-registry.json"
DEPENDENCY_MAP = ROOT / "registry" / "governance-dependency-map.json"
EXPECTED_GRAPH_DIGEST = (
    "sha256:355b0c259de100e4000211e26e4c38b9b69c0e3c4f9a6927c8d5ff5e34b762a4"
)
EXPECTED_CASE_MANIFEST_DIGEST = (
    "sha256:6777f21c501303c56568d6fc7a506335bce625dbfac2a1a7dfa8b8bb8b7adafa"
)
EXPECTED_CLASS_IDS = (
    "synthetic-coi-class-alpha",
    "synthetic-coi-class-beta",
    "synthetic-coi-class-delta",
    "synthetic-coi-class-gamma",
)
EXPECTED_EDGES = (
    (
        "synthetic-adversity-edge-alpha-beta",
        ("synthetic-coi-class-alpha", "synthetic-coi-class-beta"),
        "synthetic_fixture_reviewed",
    ),
    (
        "synthetic-adversity-edge-delta-gamma",
        ("synthetic-coi-class-delta", "synthetic-coi-class-gamma"),
        "unreviewed_fixture",
    ),
)


class AdversityClassRegistryError(ValueError):
    """Raised when the candidate registry drifts or overclaims authority."""


def _label(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return str(path)


def _load_object(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise AdversityClassRegistryError(f"{_label(path)} unreadable: {exc}") from exc
    if not isinstance(payload, dict):
        raise AdversityClassRegistryError(f"{_label(path)} must be a JSON object")
    return payload


def _digest(payload: Any) -> str:
    canonical = json.dumps(
        payload,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )
    return "sha256:" + sha256(canonical.encode("ascii")).hexdigest()


def _validate_schema(instance: dict[str, Any], schema: dict[str, Any]) -> None:
    Draft202012Validator.check_schema(schema)
    errors = sorted(
        Draft202012Validator(schema).iter_errors(instance),
        key=lambda error: tuple(str(part) for part in error.absolute_path),
    )
    if errors:
        first = errors[0]
        location = ".".join(str(part) for part in first.absolute_path) or "<root>"
        raise AdversityClassRegistryError(
            f"candidate registry schema violation at {location}: {first.message}"
        )


def _validate_graph(registry: dict[str, Any]) -> None:
    graph = registry["synthetic_fixture_graph"]
    observed_digest = _digest(graph)
    declared_digest = registry["compatibility_anchors"][
        "synthetic_adversity_graph_digest"
    ]
    if observed_digest != EXPECTED_GRAPH_DIGEST or declared_digest != EXPECTED_GRAPH_DIGEST:
        raise AdversityClassRegistryError(
            "synthetic fixture graph must match the fixed Intake PR-LL4 digest"
        )

    case_manifest_payload = {
        "graph_digest": observed_digest,
        "cases": registry["synthetic_case_manifest"],
    }
    observed_case_digest = _digest(case_manifest_payload)
    declared_case_digest = registry["compatibility_anchors"][
        "synthetic_case_manifest_digest"
    ]
    if (
        observed_case_digest != EXPECTED_CASE_MANIFEST_DIGEST
        or declared_case_digest != EXPECTED_CASE_MANIFEST_DIGEST
    ):
        raise AdversityClassRegistryError(
            "synthetic case manifest must match the fixed Intake PR-LL4 digest"
        )

    class_ids = tuple(item["class_id"] for item in graph["conflict_classes"])
    if class_ids != EXPECTED_CLASS_IDS:
        raise AdversityClassRegistryError(
            "synthetic conflict classes must match the exact closed candidate set"
        )
    if len(class_ids) != len(set(class_ids)):
        raise AdversityClassRegistryError("synthetic conflict class IDs must be unique")

    edges = tuple(
        (
            item["edge_id"],
            tuple(item["class_ids"]),
            item["review_status"],
        )
        for item in graph["adversity_edges"]
    )
    if edges != EXPECTED_EDGES:
        raise AdversityClassRegistryError(
            "synthetic adversity edges must match the exact closed candidate set"
        )
    known = set(class_ids)
    for edge in graph["adversity_edges"]:
        class_pair = tuple(edge["class_ids"])
        if class_pair != tuple(sorted(class_pair)):
            raise AdversityClassRegistryError("adversity edge class IDs must be sorted")
        if not set(class_pair).issubset(known):
            raise AdversityClassRegistryError("adversity edge references an unknown class")


def _validate_discovery(registry: dict[str, Any]) -> None:
    schema_registry = _load_object(SCHEMA_REGISTRY)
    matching_schema_rows = [
        row
        for row in schema_registry.get("schemas", [])
        if row.get("path") == "schemas/adversity-class-registry.schema.json"
    ]
    if len(matching_schema_rows) != 1:
        raise AdversityClassRegistryError(
            "schema-registry must contain exactly one adversity registry schema row"
        )
    row = matching_schema_rows[0]
    if row.get("schema_id") != "adversity-class-registry-v0_1" or row.get(
        "status"
    ) != "draft":
        raise AdversityClassRegistryError(
            "adversity registry schema row must remain draft with the candidate schema ID"
        )

    front_door = _load_object(FRONT_DOOR)
    anchors = {
        item.get("path")
        for item in front_door.get("integration_path_anchors", [])
        if item.get("repo") == "semantic_substrate"
    }
    required_anchors = {
        "schemas/adversity-class-registry.schema.json",
        "registry/adversity-class-registry.candidate.json",
        registry["governance_doc"],
    }
    missing_anchors = sorted(required_anchors - anchors)
    if missing_anchors:
        raise AdversityClassRegistryError(
            f"AI front door missing adversity registry anchors: {missing_anchors}"
        )

    dependency_map = _load_object(DEPENDENCY_MAP)
    artifact = next(
        (
            item
            for item in dependency_map.get("artifacts", [])
            if item.get("artifact_id") == "LFGD-017"
        ),
        None,
    )
    if artifact is None:
        raise AdversityClassRegistryError(
            "governance dependency map missing LFGD-017 adversity registry coverage"
        )
    required_paths = {
        "schemas/adversity-class-registry.schema.json",
        "registry/adversity-class-registry.candidate.json",
        "governance/ADVERSITY_CLASS_REGISTRY_BOUNDARY.md",
        "scripts/validate_adversity_class_registry.py",
        "tests/test_adversity_class_registry.py",
    }
    missing_paths = sorted(required_paths - set(artifact.get("paths", [])))
    if missing_paths:
        raise AdversityClassRegistryError(
            f"LFGD-017 missing adversity registry paths: {missing_paths}"
        )


def _validate_governance_doc(registry: dict[str, Any]) -> None:
    path = ROOT / registry["governance_doc"]
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise AdversityClassRegistryError(
            f"adversity registry governance doc missing: {_label(path)}"
        ) from exc
    required_text = [
        "candidate_synthetic_only",
        "HD-4",
        "HD-7",
        "Applies when",
        "Does not apply",
        "Danger if misapplied",
        "exact digest-pinned synthetic fixture graph",
        "does not",
    ]
    missing = [value for value in required_text if value not in text]
    if missing:
        raise AdversityClassRegistryError(
            f"{_label(path)} missing required boundary text: {missing}"
        )


def validate_adversity_class_registry(
    registry_path: Path = REGISTRY,
    schema_path: Path = SCHEMA,
) -> dict[str, Any]:
    registry = _load_object(registry_path)
    schema = _load_object(schema_path)
    _validate_schema(registry, schema)
    _validate_graph(registry)
    _validate_discovery(registry)
    _validate_governance_doc(registry)
    return registry


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    parser.add_argument("--schema", type=Path, default=SCHEMA)
    args = parser.parse_args(argv)
    try:
        validate_adversity_class_registry(args.registry, args.schema)
    except AdversityClassRegistryError as exc:
        print(f"Adversity class registry validation failed: {exc}", file=sys.stderr)
        return 1
    print("Adversity class registry validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
