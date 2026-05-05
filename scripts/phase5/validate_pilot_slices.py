import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schema"
DATA = ROOT / "data" / "pilot-slices"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def enum_values(name: str) -> set[str]:
    return set(load_yaml(SCHEMA / "enums" / f"{name}.yaml").get("values", []))


def main() -> int:
    failures: list[str] = []
    pilot = load_yaml(DATA / "doctrinal_core_v1.yaml")

    required = {
        "id",
        "display_title",
        "pilot_slice_status",
        "target_thinkers",
        "target_doctrines",
        "target_concepts",
        "target_comparisons",
        "competency_questions",
        "required_artifacts",
        "exit_criteria",
    }
    for field in required:
        if field not in pilot:
            failures.append(f"pilot slice missing '{field}'")

    if pilot.get("pilot_slice_status") not in enum_values("pilot_slice_status"):
        failures.append("pilot slice has invalid pilot_slice_status")
    if len(pilot.get("target_doctrines", [])) > 2:
        failures.append("pilot slice is broader than expected for a bounded seed")

    if failures:
        print("PHASE 5 PILOT SLICE FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Phase 5 pilot slice checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
