import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA = ROOT / "schema"
DATA = ROOT / "data" / "comparisons"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def enum_values(name: str) -> set[str]:
    data = load_yaml(SCHEMA / "enums" / f"{name}.yaml")
    return set(data.get("values", []))


def main() -> int:
    failures: list[str] = []

    required_enums = {
        "alignment_scope": {
            "doctrinal_core",
            "terminology",
            "conceptual_frame",
            "anthropological_frame",
            "institutional_implication",
            "governance_translation",
            "historical_snapshot",
            "practical_ethics",
        },
        "translation_burden": {"minimal", "low", "moderate", "high", "extreme"},
        "evidence_sufficiency": {
            "direct_primary_text",
            "strong_curated_secondary",
            "mixed_support",
            "indirect_inference",
            "thin_support",
        },
    }

    for enum_name, expected in required_enums.items():
        values = enum_values(enum_name)
        if not expected.issubset(values):
            failures.append(f"{enum_name} missing expected values")

    template = load_yaml(DATA / "alignment_assessment.template.yaml")
    for field in (
        "comparison_object_id",
        "relation_type",
        "alignment_degree",
        "alignment_scope",
        "translation_burden",
        "evidence_sufficiency",
        "confidence_level",
        "review_status",
    ):
        if field not in template:
            failures.append(f"alignment assessment template missing '{field}'")

    if template.get("alignment_scope") not in enum_values("alignment_scope"):
        failures.append("alignment assessment template has invalid alignment_scope")
    if template.get("translation_burden") not in enum_values("translation_burden"):
        failures.append("alignment assessment template has invalid translation_burden")
    if template.get("evidence_sufficiency") not in enum_values("evidence_sufficiency"):
        failures.append("alignment assessment template has invalid evidence_sufficiency")

    if failures:
        print("PHASE 4 ALIGNMENT RUBRIC FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Phase 4 alignment rubric checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
