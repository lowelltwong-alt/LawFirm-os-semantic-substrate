import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
GRAPHS = ROOT / "graphs"
DATA_ASSERTIONS = ROOT / "data" / "assertions"
MANIFESTS = GRAPHS / "manifests"
RELATION_ENUM = ROOT / "schema" / "enums" / "relation_type.yaml"

ALLOWED_ZONES = {"asserted", "inferred", "boundary", "quarantine", "projection"}
ALLOWED_DIRECTIONALITY = {"unidirectional", "bidirectional"}
ALLOWED_CARDINALITY = {"one_to_one", "one_to_many", "many_to_one", "many_to_many"}
ALLOWED_TEMPORAL_VALIDITY = {"always_valid", "interval_bound", "event_bound", "until_revoked"}
ALLOWED_TRUST_CARRYOVER = {"inherit", "attenuate", "none", "manual_review"}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def normalized_relation_types() -> set[str]:
    if not RELATION_ENUM.exists():
        return set()
    data = load_yaml(RELATION_ENUM)
    semantics = data.get("normalized_relation_semantics", {}) if isinstance(data, dict) else {}
    if isinstance(semantics, dict):
        return set(semantics.keys())
    return set()


def validate_cross_partition_relations(path: Path, data: dict, relation_types: set[str]) -> list[str]:
    failures: list[str] = []
    relations = data.get("cross_partition_relations")
    if relations is None:
        return failures
    if not isinstance(relations, list):
        return [f"{path}: cross_partition_relations must be a list"]

    required_keys = {
        "source_zone",
        "target_zone",
        "relation_type",
        "directionality",
        "cardinality",
        "temporal_validity",
        "trust_evidence_carryover",
    }

    for idx, relation in enumerate(relations, start=1):
        if not isinstance(relation, dict):
            failures.append(f"{path}: cross_partition_relations[{idx}] must be an object")
            continue
        missing = sorted(key for key in required_keys if key not in relation or relation.get(key) in (None, ""))
        if missing:
            failures.append(f"{path}: cross_partition_relations[{idx}] missing required keys: {missing}")
            continue

        source_zone = relation.get("source_zone")
        target_zone = relation.get("target_zone")
        if source_zone not in ALLOWED_ZONES:
            failures.append(f"{path}: cross_partition_relations[{idx}] source_zone '{source_zone}' is invalid")
        if target_zone not in ALLOWED_ZONES:
            failures.append(f"{path}: cross_partition_relations[{idx}] target_zone '{target_zone}' is invalid")
        if source_zone == target_zone:
            failures.append(f"{path}: cross_partition_relations[{idx}] must be cross-zone (source_zone != target_zone)")

        if relation.get("directionality") not in ALLOWED_DIRECTIONALITY:
            failures.append(
                f"{path}: cross_partition_relations[{idx}] directionality '{relation.get('directionality')}' is invalid"
            )
        if relation.get("cardinality") not in ALLOWED_CARDINALITY:
            failures.append(f"{path}: cross_partition_relations[{idx}] cardinality '{relation.get('cardinality')}' is invalid")
        if relation.get("temporal_validity") not in ALLOWED_TEMPORAL_VALIDITY:
            failures.append(
                f"{path}: cross_partition_relations[{idx}] temporal_validity '{relation.get('temporal_validity')}' is invalid"
            )
        if relation.get("trust_evidence_carryover") not in ALLOWED_TRUST_CARRYOVER:
            failures.append(
                f"{path}: cross_partition_relations[{idx}] trust_evidence_carryover '{relation.get('trust_evidence_carryover')}' is invalid"
            )

        relation_type = relation.get("relation_type")
        if relation_types and relation_type not in relation_types:
            failures.append(
                f"{path}: cross_partition_relations[{idx}] relation_type '{relation_type}' must be normalized: {sorted(relation_types)}"
            )

    return failures


def main() -> int:
    failures: list[str] = []

    catalog_path = GRAPHS / "catalog.yaml"
    if not catalog_path.exists():
        failures.append("Missing graphs/catalog.yaml")
    else:
        catalog = load_yaml(catalog_path)
        partitions = catalog.get("partitions", []) if isinstance(catalog, dict) else []
        expected = {"asserted", "inferred", "boundary", "quarantine"}
        seen = {entry.get("id") for entry in partitions if isinstance(entry, dict)}
        if expected != seen:
            failures.append(f"Graph catalog partitions mismatch: expected {sorted(expected)}, got {sorted(seen)}")

    for partition in ("asserted", "inferred", "boundary", "quarantine"):
        partition_dir = GRAPHS / partition
        if not partition_dir.exists():
            failures.append(f"Missing graph partition directory: graphs/{partition}")
        if not (partition_dir / "README.md").exists():
            failures.append(f"Missing graph partition README: graphs/{partition}/README.md")

    template = DATA_ASSERTIONS / "assertion_object.template.yaml"
    if template.exists():
        data = load_yaml(template)
        if data.get("graph_partition") not in {"asserted", "inferred", "boundary", "quarantine"}:
            failures.append("Assertion template graph_partition is not valid")
        if data.get("assertion_kind") not in {"asserted", "inferred", "imported", "ai_extracted", "editorial"}:
            failures.append("Assertion template assertion_kind is not valid")

    relation_types = normalized_relation_types()
    if not relation_types:
        failures.append("schema/enums/relation_type.yaml is missing normalized_relation_semantics entries")
    for manifest in sorted(MANIFESTS.glob("*.yaml")):
        data = load_yaml(manifest)
        if not isinstance(data, dict):
            failures.append(f"{manifest}: manifest content must be a mapping")
            continue
        failures.extend(validate_cross_partition_relations(manifest, data, relation_types))

    if failures:
        print("PHASE 3 GRAPH PARTITION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Phase 3 graph partition checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
