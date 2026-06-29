#!/usr/bin/env python3
"""Validate the LawFirm OS governance dependency map."""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
MAP = ROOT / "registry" / "governance-dependency-map.json"

WATCHED_PREFIXES = (
    ".github/ISSUE_TEMPLATE/",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/pull_request_template.md",
    ".github/workflows/",
    "AGENTS.md",
    "AI_FRONT_DOOR.md",
    "AI_START_HERE.md",
    "AI_TABLE_OF_CONTENTS.md",
    "AI_WORK_START_HERE.md",
    "DATA_FLOW_MAP.md",
    "ENDPOINTS_AND_COMMANDS.md",
    "GOVERNANCE_BOUNDARY.md",
    "README.md",
    "REPO_ROLE.md",
    "contracts.lock.json",
    "docs/governance/",
    "governance/",
    "manifests/",
    "registry/",
    "repo_topology.yaml",
    "schemas/",
    "scripts/check_",
    "scripts/validate_",
    "skill-agent-manifest.json",
)

REQUIRED_TOP_LEVEL = {
    "schema_version",
    "map_id",
    "status",
    "source_repo",
    "owner",
    "provenance_note",
    "reason_for_inclusion",
    "map_authority",
    "update_policy",
    "repo_authority",
    "artifacts",
    "child_mirror_contract",
    "open_questions",
}

REQUIRED_ARTIFACT_FIELDS = {
    "artifact_id",
    "title",
    "repo",
    "paths",
    "object_type",
    "trust_zone",
    "lifecycle_status",
    "authorized_by",
    "owner_decision_ref",
    "depends_on",
    "downstream_controls",
    "mirrored_by",
    "validators",
    "update_triggers",
    "provenance_note",
    "reason_for_inclusion",
}

REQUIRED_ARTIFACT_IDS = {
    "LFGD-001",
    "LFGD-002",
    "LFGD-003",
    "LFGD-004",
    "LFGD-005",
    "LFGD-006",
    "LFGD-007",
    "LFGD-008",
    "LFGD-009",
    "LFGD-010",
    "LFGD-011",
    "LFGD-012",
    "LFGD-013",
}

REQUIRED_COVERED_PATHS = {
    ".github/workflows/governance-dependency-map.yml",
    ".github/workflows/pr-description-governance-checks.yml",
    "AI_TABLE_OF_CONTENTS.md",
    "AI_WORK_START_HERE.md",
    "governance/CROSS_REPO_MAP.md",
    "governance/GOVERNANCE_DEPENDENCY_MAP.md",
    "registry/governance-dependency-map.json",
    "registry/governance-full-manifest.json",
    "registry/lawfirm-os-repo-registry.json",
    "registry/registry-full-manifest.json",
    "scripts/validate_governance_dependency_map.py",
    "scripts/validation/tests/test_validate_governance_dependency_map.py",
    "templates/governance-dependency-map-mirror.template.json",
}

REQUIRED_CHILD_MIRRORS = {
    "LawFirm-os-orchestrator/.ai/control/governance-dependency-map-mirror.json",
    "LawFirm-os-exceptions-lake-runtime/.ai/control/governance-dependency-map-mirror.json",
    "LawFirm-os-legal-knowledge-runtime/.ai/control/governance-dependency-map-mirror.json",
    "LawFirm-os-skills-registry/.ai/control/governance-dependency-map-mirror.json",
    "LawFirm-os-intake/.ai/control/governance-dependency-map-mirror.json",
}


class DependencyMapError(ValueError):
    """Raised when the governance dependency map is invalid."""


def _rel(path: Path) -> str:
    try:
        return path.relative_to(ROOT).as_posix()
    except ValueError:
        return path.as_posix()


def _read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DependencyMapError(f"{_rel(path)} unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise DependencyMapError(f"{_rel(path)} must be a JSON object")
    return data


def _require_string(container: dict[str, Any], key: str, label: str) -> None:
    value = container.get(key)
    if not isinstance(value, str) or not value.strip():
        raise DependencyMapError(f"{label}: {key} must be a non-empty string")


def _require_string_list(
    container: dict[str, Any], key: str, label: str, *, allow_empty: bool = False
) -> list[str]:
    value = container.get(key)
    if not isinstance(value, list) or (not allow_empty and not value):
        raise DependencyMapError(f"{label}: {key} must be a {'possibly empty ' if allow_empty else ''}list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise DependencyMapError(f"{label}: {key} must contain only non-empty strings")
    return value


def _normalize_path(path: str) -> str:
    normalized = path.replace("\\", "/")
    if normalized.startswith("./"):
        return normalized[2:]
    return normalized


def _matches_path_rule(path: str, rule: str) -> bool:
    path = _normalize_path(path)
    rule = _normalize_path(rule)
    if rule.endswith("/") or rule.endswith("_"):
        return path.startswith(rule)
    return path == rule


def _artifact_coverage(data: dict[str, Any]) -> set[str]:
    coverage: set[str] = set()
    for artifact in data.get("artifacts", []):
        if not isinstance(artifact, dict):
            continue
        for key in ("paths", "validators", "update_triggers", "mirrored_by"):
            value = artifact.get(key)
            if isinstance(value, list):
                coverage.update(_normalize_path(str(item)) for item in value if str(item).strip())
    return coverage


def _git_changed_files(base_ref: str) -> list[str]:
    try:
        result = subprocess.run(
            ["git", "diff", "--name-only", f"{base_ref}...HEAD"],
            cwd=ROOT,
            check=True,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except subprocess.CalledProcessError as exc:
        raise DependencyMapError(f"could not compute changed files against {base_ref}: {exc.stderr.strip()}") from exc
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def validate_dependency_map(path: Path = MAP) -> dict[str, Any]:
    data = _read_json(path)
    missing = sorted(REQUIRED_TOP_LEVEL - set(data))
    if missing:
        raise DependencyMapError(f"{_rel(path)} missing top-level keys: {missing}")
    if data["schema_version"] != "governance_dependency_map.v1":
        raise DependencyMapError(f"{_rel(path)} schema_version must be governance_dependency_map.v1")
    if data["source_repo"] != "LawFirm-os-semantic-substrate":
        raise DependencyMapError(f"{_rel(path)} source_repo must be LawFirm-os-semantic-substrate")

    authority = data["map_authority"]
    if not isinstance(authority, dict):
        raise DependencyMapError("map_authority must be an object")
    if authority.get("records_governance_dependencies") is not True:
        raise DependencyMapError("map_authority.records_governance_dependencies must be true")
    for key in (
        "authorizes_child_repo_override",
        "authorizes_ai_generated_governance_authority",
        "authorizes_client_or_matter_data_change",
        "authorizes_legal_advice",
        "authorizes_external_write_or_production_automation",
    ):
        if authority.get(key) is not False:
            raise DependencyMapError(f"map_authority.{key} must be false")

    update_policy = data["update_policy"]
    if not isinstance(update_policy, dict):
        raise DependencyMapError("update_policy must be an object")
    if update_policy.get("changed_path_gate_enabled") is not True:
        raise DependencyMapError("update_policy.changed_path_gate_enabled must be true")
    if update_policy.get("changed_governance_path_must_be_registered_in_map_coverage") is not True:
        raise DependencyMapError(
            "update_policy.changed_governance_path_must_be_registered_in_map_coverage must be true"
        )
    configured_watch = set(_require_string_list(update_policy, "map_update_required_when_paths_change", "update_policy"))
    missing_watch = sorted(set(WATCHED_PREFIXES) - configured_watch)
    if missing_watch:
        raise DependencyMapError(f"update_policy missing watched path rules: {missing_watch}")

    coverage = _artifact_coverage(data)
    missing_covered = sorted(path for path in REQUIRED_COVERED_PATHS if path not in coverage)
    if missing_covered:
        raise DependencyMapError(f"required paths missing map coverage: {missing_covered}")
    missing_mirrors = sorted(path for path in REQUIRED_CHILD_MIRRORS if path not in coverage)
    if missing_mirrors:
        raise DependencyMapError(f"required child mirrors missing map coverage: {missing_mirrors}")

    artifact_ids: set[str] = set()
    for idx, artifact in enumerate(data["artifacts"]):
        if not isinstance(artifact, dict):
            raise DependencyMapError(f"artifacts[{idx}] must be an object")
        label = artifact.get("artifact_id", f"artifacts[{idx}]")
        missing_fields = sorted(REQUIRED_ARTIFACT_FIELDS - set(artifact))
        if missing_fields:
            raise DependencyMapError(f"{label}: missing fields {missing_fields}")
        artifact_id = artifact["artifact_id"]
        if artifact_id in artifact_ids:
            raise DependencyMapError(f"duplicate artifact_id {artifact_id}")
        artifact_ids.add(artifact_id)
        for key in (
            "artifact_id",
            "title",
            "repo",
            "object_type",
            "trust_zone",
            "lifecycle_status",
            "authorized_by",
            "owner_decision_ref",
            "provenance_note",
            "reason_for_inclusion",
        ):
            _require_string(artifact, key, label)
        for key in ("paths", "downstream_controls", "mirrored_by", "validators", "update_triggers"):
            _require_string_list(artifact, key, label, allow_empty=(key == "mirrored_by"))
        dependencies = _require_string_list(artifact, "depends_on", label, allow_empty=True)
        for dependency in dependencies:
            if dependency not in artifact_ids and dependency not in REQUIRED_ARTIFACT_IDS:
                raise DependencyMapError(f"{label}: unknown dependency {dependency}")

    missing_artifacts = sorted(REQUIRED_ARTIFACT_IDS - artifact_ids)
    if missing_artifacts:
        raise DependencyMapError(f"{_rel(path)} missing required artifact ids: {missing_artifacts}")

    mirror_contract = data["child_mirror_contract"]
    if not isinstance(mirror_contract, dict):
        raise DependencyMapError("child_mirror_contract must be an object")
    for key in (
        "local_repo_may_override_upstream_dependency_map",
        "local_repo_may_weaken_upstream_governance",
        "local_repo_may_treat_local_convenience_as_governance_authority",
    ):
        if mirror_contract.get(key) is not False:
            raise DependencyMapError(f"child_mirror_contract.{key} must be false")
    if mirror_contract.get("local_repo_must_stop_if_upstream_map_conflicts") is not True:
        raise DependencyMapError("child_mirror_contract.local_repo_must_stop_if_upstream_map_conflicts must be true")

    return data


def validate_changed_path_gate(
    *,
    changed_files: list[str],
    map_path: Path = MAP,
    map_updated: bool | None = None,
) -> None:
    normalized = [_normalize_path(path) for path in changed_files]
    watched_changed = [
        path for path in normalized if any(_matches_path_rule(path, prefix) for prefix in WATCHED_PREFIXES)
    ]
    if map_updated is None:
        map_updated = _rel(map_path) in normalized
    if watched_changed and not map_updated:
        raise DependencyMapError(
            "governance dependency map must be updated when watched paths change: "
            + ", ".join(watched_changed)
        )
    if watched_changed:
        data = validate_dependency_map(map_path)
        coverage = _artifact_coverage(data)
        uncovered = [
            path for path in watched_changed if not any(_matches_path_rule(path, rule) for rule in coverage)
        ]
        if uncovered:
            raise DependencyMapError(
                "changed governance paths must be registered in dependency map coverage: " + ", ".join(uncovered)
            )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--map", type=Path, default=MAP)
    parser.add_argument("--base-ref", default="origin/main")
    parser.add_argument("--changed-file", action="append", default=[])
    parser.add_argument("--map-updated", choices=["true", "false"], default=None)
    args = parser.parse_args(argv)

    try:
        validate_dependency_map(args.map)
        map_updated = None if args.map_updated is None else args.map_updated == "true"
        if args.changed_file:
            changed_files = args.changed_file
        elif map_updated is True:
            changed_files = [_rel(args.map)]
        else:
            changed_files = _git_changed_files(args.base_ref)
        validate_changed_path_gate(changed_files=changed_files, map_path=args.map, map_updated=map_updated)
    except DependencyMapError as exc:
        print(f"Governance dependency map validation failed: {exc}", file=sys.stderr)
        return 1

    print("Governance dependency map validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
