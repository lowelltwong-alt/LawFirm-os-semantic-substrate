import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def check_assertion_template(path: Path, failures: list[str]) -> None:
    data = load_yaml(path)
    required = [
        "id",
        "subject_ref",
        "relation_type",
        "object_ref",
        "assertion_kind",
        "graph_partition",
        "authority_zone",
        "trust_level",
        "review_status",
        "provenance_activity_refs",
    ]
    for field in required:
        if field not in data:
            failures.append(f"{path.relative_to(ROOT)} missing '{field}'")
    if "source_refs" not in data and "evidence_refs" not in data:
        failures.append(
            f"{path.relative_to(ROOT)} should include at least one source or evidence reference"
        )


def check_evidence_template(path: Path, failures: list[str]) -> None:
    data = load_yaml(path)
    for field in ("id", "bundle_scope", "source_refs"):
        if field not in data:
            failures.append(f"{path.relative_to(ROOT)} missing '{field}'")


def main() -> int:
    failures: list[str] = []

    check_assertion_template(ROOT / "data" / "assertions" / "assertion_object.template.yaml", failures)
    check_evidence_template(ROOT / "data" / "evidence" / "evidence_bundle.template.yaml", failures)

    if failures:
        print("PHASE 3 PROVENANCE MINIMUM FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Phase 3 provenance minimum checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
