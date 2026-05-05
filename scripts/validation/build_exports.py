import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schema"
EXPORT_ROOT = ROOT / "generated" / "phase2"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def collect(relative_dir: str):
    base = SCHEMA_ROOT / relative_dir
    return {
        path.stem: load_yaml(path)
        for path in sorted(base.glob("*.yaml"))
    }


def main() -> int:
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

    export = {
        "manifest": load_yaml(SCHEMA_ROOT / "manifest.yaml"),
        "interfaces": collect("interfaces"),
        "types": collect("types"),
        "enums": collect("enums"),
    }

    output = EXPORT_ROOT / "enterprise_doctrinal_comparison_substrate.json"
    output.write_text(json.dumps(export, indent=2), encoding="utf-8")
    print(f"WROTE: {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
