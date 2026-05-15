from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from contract_surface import ContractSurfaceError, compute_contract_surface

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
        try:
            observed = compute_contract_surface(substrate, surface_id, Path(str(registry_path)))
        except ContractSurfaceError as exc:
            errors.append(f"{lock_path}: {exc}")
            return errors
        if observed["surface_sha256"] != expected:
            errors.append(
                f"{lock_path}: contract surface hash drift: observed {observed['surface_sha256']} expected {expected}"
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
