import json
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
EXPORT_ROOT = ROOT / "generated" / "phase3"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> int:
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)

    catalog = load_yaml(ROOT / "graphs" / "catalog.yaml")
    assertion_template = load_yaml(ROOT / "data" / "assertions" / "assertion_object.template.yaml")
    evidence_template = load_yaml(ROOT / "data" / "evidence" / "evidence_bundle.template.yaml")
    comparison_template = load_yaml(ROOT / "data" / "comparisons" / "comparison_object.template.yaml")

    export = {
        "catalog": catalog,
        "assertion_template": assertion_template,
        "evidence_template": evidence_template,
        "comparison_template": comparison_template,
    }

    output = EXPORT_ROOT / "graph_partition_manifest.json"
    output.write_text(json.dumps(export, indent=2), encoding="utf-8")
    print(f"WROTE: {output.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
