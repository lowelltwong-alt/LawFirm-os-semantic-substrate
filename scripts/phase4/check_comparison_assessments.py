import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schema" / "types"
DATA = ROOT / "data" / "comparisons"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> int:
    failures: list[str] = []

    comparison_type = load_yaml(SCHEMA / "comparison_object.yaml")
    optional_fields = set(comparison_type.get("optional_fields", []))
    expected_fields = {
        "alignment_assessment_id",
        "alignment_scope",
        "translation_burden",
        "evidence_sufficiency",
        "confidence_level",
        "review_status",
    }
    if not expected_fields.issubset(optional_fields):
        failures.append("comparison_object.yaml missing expected Phase 4 optional fields")

    comparison_template = load_yaml(DATA / "comparison_object.template.yaml")
    assessment_template = load_yaml(DATA / "alignment_assessment.template.yaml")

    if "alignment_assessment_id" not in comparison_template:
        failures.append("comparison_object.template.yaml missing 'alignment_assessment_id'")
    if comparison_template.get("alignment_assessment_id") != assessment_template.get("id"):
        failures.append("comparison template alignment_assessment_id does not match assessment template id")
    if assessment_template.get("comparison_object_id") != comparison_template.get("id"):
        failures.append("alignment assessment comparison_object_id does not match comparison template id")

    if failures:
        print("PHASE 4 COMPARISON ASSESSMENT FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Phase 4 comparison assessment checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
