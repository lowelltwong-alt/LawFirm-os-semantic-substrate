import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schema"
DATA = ROOT / "data" / "action-types"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def enum_values(name: str) -> set[str]:
    return set(load_yaml(SCHEMA / "enums" / f"{name}.yaml").get("values", []))


def main() -> int:
    failures: list[str] = []
    template = load_yaml(DATA / "action_definition.template.yaml")

    required = {
        "id",
        "display_title",
        "action_type",
        "target_surface",
        "required_inputs",
        "required_reviewer_role",
        "required_checks",
        "lifecycle_impact",
        "outputs",
    }
    for field in required:
        if field not in template:
            failures.append(f"action definition template missing '{field}'")

    if template.get("action_type") not in enum_values("action_type"):
        failures.append("action definition template has invalid action_type")
    if template.get("required_reviewer_role") not in enum_values("reviewer_role"):
        failures.append("action definition template has invalid required_reviewer_role")

    if failures:
        print("PHASE 5 ACTION TYPE FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Phase 5 action type checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
