from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from contract_surface import compute_contract_surface, compute_contract_surface_from_git_tree


def git_ref(root: Path, ref: str = "HEAD") -> str | None:
    try:
        return subprocess.run(
            ["git", "rev-parse", "--verify", f"{ref}^{{commit}}"],
            cwd=root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
    except Exception:
        return None


def git_head(root: Path) -> str | None:
    return git_ref(root, "HEAD")


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute a LawFirm OS contract surface hash.")
    parser.add_argument("--substrate", default=".", help="Path to LawFirm-os-semantic-substrate.")
    parser.add_argument("--surface-id", default=None)
    parser.add_argument("--registry-path", default="registry/contract-surface-registry.json")
    parser.add_argument("--ref", default="HEAD", help="Committed git ref to hash; defaults to HEAD.")
    parser.add_argument("--working-tree", action="store_true", help="Hash the working tree instead of a committed git tree.")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    substrate = Path(args.substrate).resolve()
    commit_sha = git_ref(substrate, args.ref)
    if args.working_tree or commit_sha is None:
        result = compute_contract_surface(substrate, args.surface_id, Path(args.registry_path))
        result["computed_from_repo"] = substrate.name
        result["computed_from_commit"] = None
        result["provenance_mode"] = "working_tree"
        result["provenance_warning"] = (
            "This surface_sha256 was computed from mutable working-tree filesystem bytes. "
            "Do NOT use it as a contracts.lock.json contract_surface_lock.surface_sha256 with "
            "computed_from_commit / substrate_repo_commit_sha set, because consumers validate "
            "committed Git-tree blob bytes (LF semantics) which can differ from the working tree "
            "on platforms with line-ending normalisation (e.g. Windows core.autocrlf=true)."
        )
    else:
        result = compute_contract_surface_from_git_tree(substrate, commit_sha, args.surface_id, Path(args.registry_path))
        result["computed_from_repo"] = substrate.name
        result["computed_from_commit"] = commit_sha
        result["provenance_mode"] = "committed_tree"
    payload = json.dumps(result, indent=2, sort_keys=False) + "\n"
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
