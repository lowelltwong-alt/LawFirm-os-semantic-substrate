import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schema"
DATA = ROOT / "data" / "object-sets"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def enum_values(name: str) -> set[str]:
    return set(load_yaml(SCHEMA / "enums" / f"{name}.yaml").get("values", []))


def main() -> int:
    failures: list[str] = []
    template = load_yaml(DATA / "object_set_definition.template.yaml")

    required = {
        "id",
        "display_title",
        "object_set_kind",
        "scope_note",
        "required_reviewer_role",
    }
    for field in required:
        if field not in template:
            failures.append(f"object set definition template missing '{field}'")

    if template.get("object_set_kind") not in enum_values("object_set_kind"):
        failures.append("object set definition template has invalid object_set_kind")
    if template.get("required_reviewer_role") not in enum_values("reviewer_role"):
        failures.append("object set definition template has invalid required_reviewer_role")

    if failures:
        print("PHASE 5 OBJECT SET FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Phase 5 object set checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
