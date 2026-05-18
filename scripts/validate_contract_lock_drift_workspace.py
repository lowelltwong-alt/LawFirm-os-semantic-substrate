from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from contract_surface import (
    ContractSurfaceError,
    compute_contract_surface_from_git_tree,
    is_contract_surface_path,
    load_surface_registry,
    select_surface,
)

REPO_ALIASES = {
    "LawFirm-os-semantic-substrate": ["LawFirm-os-semantic-substrate", "LawFirm-os-semantic-substrate-main"],
    "LawFirm-os-orchestrator": ["LawFirm-os-orchestrator", "LawFirm-os-orchestrator-main"],
    "LawFirm-os-exceptions-lake-runtime": ["LawFirm-os-exceptions-lake-runtime", "LawFirm-os-exceptions-lake-runtime-main"],
    "LawFirm-os-legal-knowledge-runtime": ["LawFirm-os-legal-knowledge-runtime", "LawFirm-os-legal-knowledge-runtime-main"],
    "LawFirm-os-skills-registry": ["LawFirm-os-skills-registry", "LawFirm-os-skills-registry-main"],
}

CONSUMER_REPOS = ["LawFirm-os-orchestrator", "LawFirm-os-exceptions-lake-runtime"]


def find_repo(workspace: Path, logical: str) -> Path | None:
    for name in REPO_ALIASES.get(logical, [logical]):
        p = workspace / name
        if p.exists() and p.is_dir():
            return p
    return None


def read_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RuntimeError(f"cannot read {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise RuntimeError(f"{path} must contain a JSON object")
    return data


def git_head(repo: Path) -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()
    except Exception:
        return None


def git_changed_paths(repo: Path) -> list[str]:
    try:
        raw = subprocess.run(
            ["git", "status", "--porcelain=v1", "-z", "--untracked-files=all"],
            cwd=repo,
            capture_output=True,
            check=True,
        ).stdout
    except Exception:
        return []
    entries = [entry for entry in raw.decode("utf-8", errors="replace").split("\0") if entry]
    paths: list[str] = []
    idx = 0
    while idx < len(entries):
        entry = entries[idx]
        status = entry[:2]
        path = entry[3:] if len(entry) > 3 else ""
        if path:
            paths.append(path)
        idx += 2 if status and status[0] in {"R", "C"} else 1
    return paths


def validate_lock(lock_path: Path, substrate: Path) -> list[str]:
    errors: list[str] = []
    lock = read_json(lock_path)
    if lock.get("contract_repo") != "LawFirm-os-semantic-substrate":
        errors.append(f"{lock_path}: contract_repo must be LawFirm-os-semantic-substrate")
        return errors
    surface_lock = lock.get("contract_surface_lock")
    if isinstance(surface_lock, dict):
        surface_id = surface_lock.get("surface_id")
        expected = surface_lock.get("surface_sha256")
        registry_path = surface_lock.get("surface_registry_path", "registry/contract-surface-registry.json")
        if not isinstance(surface_id, str) or not surface_id:
            errors.append(f"{lock_path}: surface_id missing")
            return errors
        if not isinstance(expected, str) or len(expected) != 64:
            errors.append(f"{lock_path}: surface_sha256 invalid")
            return errors
        computed_from_commit = surface_lock.get("computed_from_commit") or lock.get("substrate_repo_commit_sha") or lock.get("contract_sha")
        if isinstance(computed_from_commit, str) and computed_from_commit:
            try:
                provenance = compute_contract_surface_from_git_tree(substrate, computed_from_commit, surface_id, Path(str(registry_path)))
            except ContractSurfaceError as exc:
                errors.append(f"{lock_path}: cannot verify contract_surface_lock.computed_from_commit {computed_from_commit}: {exc}")
                return errors
            if provenance["surface_sha256"] != expected:
                errors.append(
                    f"{lock_path}: contract surface provenance mismatch: committed tree {computed_from_commit} has "
                    f"{provenance['surface_sha256']} expected {expected}"
                )
        head = git_head(substrate)
        if head:
            try:
                observed = compute_contract_surface_from_git_tree(substrate, head, surface_id, Path(str(registry_path)))
            except ContractSurfaceError as exc:
                errors.append(f"{lock_path}: cannot verify current committed substrate HEAD {head}: {exc}")
                return errors
            if observed["surface_sha256"] != expected:
                errors.append(
                    f"{lock_path}: committed substrate HEAD contract surface hash drift: observed "
                    f"{observed['surface_sha256']} expected {expected}"
                )
        try:
            registry = load_surface_registry(substrate, Path(str(registry_path)))
            surface = select_surface(registry, surface_id)
        except ContractSurfaceError as exc:
            errors.append(f"{lock_path}: {exc}")
            return errors
        changed_surface_paths = sorted(
            path for path in git_changed_paths(substrate) if is_contract_surface_path(path, surface)
        )
        if changed_surface_paths:
            errors.append(
                f"{lock_path}: uncommitted contract surface path(s) require a committed surface lock refresh: "
                + ", ".join(changed_surface_paths)
            )
        return errors
    # Legacy fallback: whole-repo commit lock.
    head = git_head(substrate)
    locked = lock.get("contract_sha")
    if head and locked and head != locked:
        errors.append(f"{lock_path}: legacy contract_sha drift: substrate HEAD {head} != lock {locked}")
    if not surface_lock:
        errors.append(f"{lock_path}: missing contract_surface_lock; legacy whole-repo lock is still recursive")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LawFirm OS workspace contract locks without audit-record recursion.")
    parser.add_argument("--workspace", default=".")
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    substrate = find_repo(workspace, "LawFirm-os-semantic-substrate")
    if substrate is None:
        print("Missing LawFirm-os-semantic-substrate", file=sys.stderr)
        return 1
    errors: list[str] = []
    for repo_name in CONSUMER_REPOS:
        repo = find_repo(workspace, repo_name)
        if repo is None:
            continue
        lock_path = repo / "contracts.lock.json"
        if lock_path.exists():
            errors.extend(validate_lock(lock_path, substrate))
    if errors:
        print("Workspace contract lock drift validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Workspace contract lock drift validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
