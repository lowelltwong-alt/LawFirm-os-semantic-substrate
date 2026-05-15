from __future__ import annotations

import argparse
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from contract_surface import compute_contract_surface

REPO_ALIASES = {
    "LawFirm-os-semantic-substrate": ["LawFirm-os-semantic-substrate", "LawFirm-os-semantic-substrate-main"],
    "LawFirm-os-orchestrator": ["LawFirm-os-orchestrator", "LawFirm-os-orchestrator-main"],
    "LawFirm-os-exceptions-lake-runtime": ["LawFirm-os-exceptions-lake-runtime", "LawFirm-os-exceptions-lake-runtime-main"],
}


def find_repo(workspace: Path, logical: str) -> Path | None:
    for name in REPO_ALIASES.get(logical, [logical]):
        p = workspace / name
        if p.exists() and p.is_dir():
            return p
    return None


def git_head(repo: Path) -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, text=True, capture_output=True, check=True).stdout.strip()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: dict[str, Any]) -> None:
    path.write_text(json.dumps(data, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def update_lock(lock_path: Path, substrate: Path, surface: dict[str, Any], commit_sha: str, commit: bool) -> None:
    lock = read_json(lock_path)
    lock["contract_sha"] = commit_sha
    lock["substrate_repo_commit_sha"] = commit_sha
    lock["contract_surface_lock"] = {
        "surface_id": surface["surface_id"],
        "surface_sha256": surface["surface_sha256"],
        "surface_registry_path": surface["surface_registry_path"],
        "hash_algorithm": surface["hash_algorithm"],
        "computed_from_repo": substrate.name,
        "computed_from_commit": commit_sha,
        "included_file_count": surface["included_file_count"],
        "included_files_manifest_sha256": surface["included_files_manifest_sha256"],
        "notes": [
            "Consumer validates contract_surface_lock.surface_sha256 to avoid recursive drift from managed-patch decision/audit commits.",
            "contract_sha remains provenance for the Substrate commit used to compute this surface lock."
        ]
    }
    lock["generated_at"] = datetime.now(tz=UTC).isoformat().replace("+00:00", "Z")
    if commit:
        write_json(lock_path, lock)
        print(f"WRITE {lock_path}")
    else:
        print(f"WOULD UPDATE {lock_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Update consumer contracts.lock.json files with contract_surface_lock.")
    parser.add_argument("--workspace", default=".")
    parser.add_argument("--substrate", default=None)
    parser.add_argument("--surface-id", default=None)
    parser.add_argument("--commit", action="store_true")
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    substrate = Path(args.substrate).resolve() if args.substrate else find_repo(workspace, "LawFirm-os-semantic-substrate")
    if substrate is None:
        raise SystemExit("missing substrate repo")
    commit_sha = git_head(substrate)
    surface = compute_contract_surface(substrate, args.surface_id)
    surface["computed_from_commit"] = commit_sha
    for repo_name in ("LawFirm-os-orchestrator", "LawFirm-os-exceptions-lake-runtime"):
        repo = find_repo(workspace, repo_name)
        if repo is None:
            print(f"SKIP missing {repo_name}")
            continue
        lock_path = repo / "contracts.lock.json"
        if not lock_path.exists():
            print(f"SKIP missing {lock_path}")
            continue
        update_lock(lock_path, substrate, surface, commit_sha, args.commit)
    if not args.commit:
        print("Dry run only. Re-run with --commit to write lock files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
