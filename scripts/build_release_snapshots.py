from __future__ import annotations

import argparse
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "release-snapshots"


def build_release_snapshot(version: str) -> Path:
    target = OUT / version
    target.mkdir(parents=True, exist_ok=True)

    (target / "graph.ttl").write_text("# placeholder graph snapshot\n", encoding="utf-8")
    (target / "graph.jsonld").write_text(
        json.dumps({"@context": {}, "@graph": []}, indent=2),
        encoding="utf-8",
    )
    (target / "nodes.ndjson").write_text("", encoding="utf-8")
    (target / "synthis-export.json").write_text(
        json.dumps({"version": version, "objects": []}, indent=2),
        encoding="utf-8",
    )
    return target


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", required=True, help="Version label for the snapshot directory.")
    args = parser.parse_args()
    target = build_release_snapshot(args.version)
    print(f"built placeholder release snapshots in {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
