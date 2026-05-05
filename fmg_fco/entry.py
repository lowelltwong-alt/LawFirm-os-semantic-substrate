from __future__ import annotations

import argparse
import importlib.util
import os
from pathlib import Path
from typing import Sequence

REPO_MARKERS = ("registry/source-of-truth.json", "registry/design-authority.json", "README.md")


def find_repo_root(start: Path | None = None) -> Path:
    env_root = os.environ.get("FMG_REPO_ROOT")
    if env_root:
        root = Path(env_root).resolve()
        if all((root / marker).exists() for marker in REPO_MARKERS):
            return root
        raise SystemExit(f"FMG_REPO_ROOT does not point at a valid repository root: {root}")
    current = (start or Path.cwd()).resolve()
    for candidate in (current, *current.parents):
        if all((candidate / marker).exists() for marker in REPO_MARKERS):
            return candidate
    raise SystemExit("Could not find FMG repository root. Run inside the repo or set FMG_REPO_ROOT.")


def load_release_snapshot_builder(repo_root: Path):
    module_path = repo_root / "scripts" / "build_release_snapshots.py"
    if not module_path.exists():
        raise SystemExit(f"Could not find release snapshot builder at {module_path}")

    spec = importlib.util.spec_from_file_location("fmg_build_release_snapshots", module_path)
    if spec is None or spec.loader is None:
        raise SystemExit(f"Could not load release snapshot builder from {module_path}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    build_release_snapshot = getattr(module, "build_release_snapshot", None)
    if build_release_snapshot is None:
        raise SystemExit(f"Release snapshot builder did not expose build_release_snapshot: {module_path}")
    return build_release_snapshot


def audit_main(argv: Sequence[str] | None = None) -> int:
    find_repo_root()
    return 0


def claims_main(argv: Sequence[str] | None = None) -> int:
    find_repo_root()
    return 0


def shacl_main(argv: Sequence[str] | None = None) -> int:
    find_repo_root()
    return 0


def demo_main(argv: Sequence[str] | None = None) -> int:
    find_repo_root()
    return 0


def release_snapshot_main(argv: Sequence[str] | None = None) -> int:
    repo_root = find_repo_root()
    parser = argparse.ArgumentParser(prog="fmg-release-snapshot")
    parser.add_argument("--version", required=True, help="Version label for the snapshot directory.")
    args = parser.parse_args(list(argv) if argv is not None else None)
    build_release_snapshot = load_release_snapshot_builder(repo_root)
    out_dir = build_release_snapshot(args.version)
    print(f"built placeholder release snapshots in {out_dir}")
    return 0


def pitch_safe_readme_main(argv: Sequence[str] | None = None) -> int:
    find_repo_root()
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    find_repo_root()
    parser = argparse.ArgumentParser(prog="fmg")
    subparsers = parser.add_subparsers(dest="command")

    release_snapshot_parser = subparsers.add_parser(
        "release-snapshot",
        help="Build the placeholder POC release snapshot artifact.",
    )
    release_snapshot_parser.add_argument(
        "--version",
        required=True,
        help="Version label for the snapshot directory.",
    )

    args = parser.parse_args(list(argv) if argv is not None else None)

    if args.command == "release-snapshot":
        return release_snapshot_main(["--version", args.version])

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
