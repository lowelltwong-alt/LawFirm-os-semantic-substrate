from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

from contract_surface import compute_contract_surface


def git_head(root: Path) -> str | None:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=root, text=True, capture_output=True, check=True).stdout.strip()
    except Exception:
        return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Compute a LawFirm OS contract surface hash.")
    parser.add_argument("--substrate", default=".", help="Path to LawFirm-os-semantic-substrate.")
    parser.add_argument("--surface-id", default=None)
    parser.add_argument("--registry-path", default="registry/contract-surface-registry.json")
    parser.add_argument("--out", default=None)
    args = parser.parse_args()
    substrate = Path(args.substrate).resolve()
    result = compute_contract_surface(substrate, args.surface_id, Path(args.registry_path))
    result["computed_from_repo"] = substrate.name
    result["computed_from_commit"] = git_head(substrate)
    payload = json.dumps(result, indent=2, sort_keys=False) + "\n"
    if args.out:
        Path(args.out).write_text(payload, encoding="utf-8")
    else:
        print(payload, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
