from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from contract_surface import ContractSurfaceError, compute_contract_surface_from_git_tree


def load_json(path: Path) -> dict[str, Any]:
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


def validate_lock(lock_path: Path, substrate: Path, allow_legacy: bool) -> list[str]:
    errors: list[str] = []
    lock = load_json(lock_path)
    surface_lock = lock.get("contract_surface_lock")
    if surface_lock is None:
        if not allow_legacy:
            return [f"{lock_path} does not contain contract_surface_lock"]
        return []
    if not isinstance(surface_lock, dict):
        return [f"{lock_path} contract_surface_lock must be an object"]
    surface_id = surface_lock.get("surface_id")
    expected = surface_lock.get("surface_sha256")
    registry_path = surface_lock.get("surface_registry_path", "registry/contract-surface-registry.json")
    if not isinstance(surface_id, str) or not surface_id:
        errors.append(f"{lock_path} contract_surface_lock.surface_id missing")
    if not isinstance(expected, str) or len(expected) != 64:
        errors.append(f"{lock_path} contract_surface_lock.surface_sha256 invalid")
    if errors:
        return errors
    computed_from_commit = surface_lock.get("computed_from_commit") or lock.get("substrate_repo_commit_sha") or lock.get("contract_sha")
    if isinstance(computed_from_commit, str) and computed_from_commit:
        try:
            provenance = compute_contract_surface_from_git_tree(substrate, computed_from_commit, surface_id, Path(registry_path))
        except ContractSurfaceError as exc:
            return [f"{lock_path}: cannot verify contract_surface_lock.computed_from_commit {computed_from_commit}: {exc}"]
        if provenance["surface_sha256"] != expected:
            errors.append(
                f"{lock_path} committed tree {computed_from_commit} contract surface hash "
                f"{provenance['surface_sha256']} does not match lock {expected}"
            )
    head = git_head(substrate)
    if head:
        try:
            observed = compute_contract_surface_from_git_tree(substrate, head, surface_id, Path(registry_path))
        except ContractSurfaceError as exc:
            return [f"{lock_path}: cannot verify current committed substrate HEAD {head}: {exc}"]
        if observed["surface_sha256"] != expected:
            errors.append(
                f"{lock_path} committed substrate HEAD contract surface hash "
                f"{observed['surface_sha256']} does not match lock {expected}"
            )
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a consumer contracts.lock.json contract_surface_lock.")
    parser.add_argument("--substrate", required=True)
    parser.add_argument("--lock-path", action="append", required=True)
    parser.add_argument("--allow-legacy", action="store_true")
    args = parser.parse_args()
    substrate = Path(args.substrate).resolve()
    errors: list[str] = []
    for raw in args.lock_path:
        errors.extend(validate_lock(Path(raw).resolve(), substrate, args.allow_legacy))
    if errors:
        print("Contract surface lock validation failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 1
    print("Contract surface lock validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
