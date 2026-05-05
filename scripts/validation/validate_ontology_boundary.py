from pathlib import Path
import sys

import yaml


ROOT = Path(__file__).resolve().parents[2]
DATA_ROOT = ROOT / "data"

FIRST_ORDER_OBJECT_TYPES = {
    "action_definition",
    "assertion_object",
    "evidence_bundle",
    "object_set_definition",
    "pilot_slice",
}

SECOND_ORDER_OBJECT_TYPES = {
    "action_log_entry",
    "alignment_assessment",
    "comparison_object",
    "property_graph_projection",
    "proposal_promotion",
    "retrieval_feedback",
}

SECOND_ORDER_FORBIDDEN_OVERRIDE_FIELDS = {
    "canonical_field_overrides",
    "first_order_field_overrides",
    "overwrite_canonical_fields",
    "proposed_canonical_updates",
}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def is_non_empty(value) -> bool:
    if value is None:
        return False
    if isinstance(value, (str, bytes)):
        return len(value) > 0
    if isinstance(value, (list, dict, tuple, set)):
        return len(value) > 0
    return True


def expected_order(object_type: str) -> str | None:
    if object_type in FIRST_ORDER_OBJECT_TYPES:
        return "first_order"
    if object_type in SECOND_ORDER_OBJECT_TYPES:
        return "second_order"
    return None


def main() -> int:
    failures: list[str] = []

    for path in sorted(DATA_ROOT.rglob("*.yaml")):
        data = load_yaml(path)
        if not isinstance(data, dict):
            continue

        object_type = data.get("object_type")
        if not object_type:
            continue

        rel_path = path.relative_to(ROOT)
        order = data.get("ontology_order")
        expected = expected_order(object_type)

        if expected:
            if order != expected:
                failures.append(
                    f"{rel_path}: object_type '{object_type}' must declare "
                    f"ontology_order '{expected}' (found '{order}')"
                )
        elif order not in (None, "first_order", "second_order"):
            failures.append(
                f"{rel_path}: ontology_order must be first_order or second_order when present"
            )

        if order == "second_order":
            for forbidden_field in sorted(SECOND_ORDER_FORBIDDEN_OVERRIDE_FIELDS):
                if forbidden_field in data and is_non_empty(data.get(forbidden_field)):
                    failures.append(
                        f"{rel_path}: second-order object must not set non-empty "
                        f"'{forbidden_field}'"
                    )

    if failures:
        print("ONTOLOGY BOUNDARY VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Ontology boundary validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
