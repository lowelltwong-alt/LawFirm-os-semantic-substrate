import json
import sys
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_TYPES = ROOT / "schema" / "types"
SCHEMA_INTERFACES = ROOT / "schema" / "interfaces"
INVARIANT_MAP_PATH = ROOT / "schema" / "invariants" / "first_order_invariants.yaml"
SCALE_CONTRACT_PATH = ROOT / "schema" / "contracts" / "scale_invariant_contract.yaml"
EXAMPLES_ROOT = ROOT / "examples"

INVARIANTS = [
    "identity",
    "address_placement",
    "lineage_provenance",
    "lifecycle_state",
    "trust_posture",
]

REQUIRED_SCALE_INVARIANTS = [
    "identity",
    "boundary",
    "state_transition",
    "evidence",
    "governance",
    "feedback",
]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError(f"{path.relative_to(ROOT)} must parse to a mapping")
    return data


def load_interface_fields() -> dict[str, set[str]]:
    fields: dict[str, set[str]] = {}
    for path in SCHEMA_INTERFACES.glob("*.yaml"):
        data = load_yaml(path)
        names: set[str] = set()
        for section in ("required_fields", "optional_fields"):
            for field in data.get(section, []):
                if isinstance(field, dict) and "name" in field:
                    names.add(field["name"])
        fields[data["id"]] = names
    return fields


def load_type_surface(interface_fields: dict[str, set[str]]) -> dict[str, set[str]]:
    type_surface: dict[str, set[str]] = {}
    for path in SCHEMA_TYPES.glob("*.yaml"):
        data = load_yaml(path)
        type_id = data["id"]
        names: set[str] = set()
        for section in ("required_fields", "optional_fields"):
            for field in data.get(section, []):
                if isinstance(field, str):
                    names.add(field)
                elif isinstance(field, dict) and "name" in field:
                    names.add(field["name"])

        for interface_name in data.get("implements", []):
            names.update(interface_fields.get(interface_name, set()))

        type_surface[type_id] = names
    return type_surface


def check_mapping_structure(
    type_surface: dict[str, set[str]], mapping: dict[str, Any], failures: list[str]
) -> None:
    mapped_types = mapping.get("types", {})
    if not isinstance(mapped_types, dict):
        failures.append("schema/invariants/first_order_invariants.yaml missing 'types' mapping")
        return

    for type_id in sorted(type_surface):
        if type_id not in mapped_types:
            failures.append(
                f"type '{type_id}' missing invariant mapping entry in schema/invariants/first_order_invariants.yaml"
            )
            continue

        invariant_entry = mapped_types[type_id]
        if not isinstance(invariant_entry, dict):
            failures.append(f"type '{type_id}' invariant mapping must be a mapping")
            continue

        for invariant in INVARIANTS:
            if invariant not in invariant_entry:
                failures.append(f"type '{type_id}' missing invariant '{invariant}'")
                continue

            spec = invariant_entry[invariant]
            if not isinstance(spec, dict):
                failures.append(f"type '{type_id}' invariant '{invariant}' must be a mapping")
                continue

            explicit_fields = spec.get("explicit_fields", []) or []
            linked_refs = spec.get("linked_refs", []) or []

            if not explicit_fields and not linked_refs:
                failures.append(
                    f"type '{type_id}' invariant '{invariant}' must declare explicit_fields and/or linked_refs"
                )
                continue

            for field_name in [*explicit_fields, *linked_refs]:
                if field_name not in type_surface[type_id]:
                    failures.append(
                        f"type '{type_id}' invariant '{invariant}' references unknown field '{field_name}'"
                    )


def gather_examples() -> list[tuple[Path, dict[str, Any]]]:
    examples: list[tuple[Path, dict[str, Any]]] = []
    if not EXAMPLES_ROOT.exists():
        return examples

    for path in sorted(EXAMPLES_ROOT.rglob("*.json")):
        try:
            with path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except Exception:
            continue
        if isinstance(data, dict):
            examples.append((path, data))
    return examples


def example_has_any(data: dict[str, Any], fields: list[str]) -> bool:
    for field in fields:
        value = data.get(field)
        if value is None:
            continue
        if isinstance(value, (list, dict, str)) and len(value) == 0:
            continue
        return True
    return False


def check_examples(mapping: dict[str, Any], failures: list[str]) -> None:
    mapped_types: dict[str, Any] = mapping.get("types", {})
    for path, example in gather_examples():
        object_type = example.get("object_type")
        if not isinstance(object_type, str):
            continue
        if object_type not in mapped_types:
            continue

        invariants = mapped_types[object_type]
        for invariant in INVARIANTS:
            spec = invariants.get(invariant, {})
            explicit_fields = spec.get("explicit_fields", []) or []
            linked_refs = spec.get("linked_refs", []) or []
            if not example_has_any(example, [*explicit_fields, *linked_refs]):
                failures.append(
                    f"example {path.relative_to(ROOT)} (object_type={object_type}) missing any populated field for invariant '{invariant}'"
                )


def _has_values(mapping: dict[str, Any], keys: list[str]) -> bool:
    return all(k in mapping and mapping.get(k) not in (None, "", [], {}) for k in keys)


def check_scale_contract_structure(
    type_surface: dict[str, set[str]], contract: dict[str, Any], failures: list[str]
) -> None:
    levels = contract.get("levels")
    if not isinstance(levels, dict) or not levels:
        failures.append("schema/contracts/scale_invariant_contract.yaml missing non-empty 'levels' mapping")
        return

    for level_name, spec in levels.items():
        if not isinstance(spec, dict):
            failures.append(f"level '{level_name}' must be a mapping")
            continue
        req = spec.get("required_invariants")
        if not isinstance(req, list):
            failures.append(f"level '{level_name}' must declare required_invariants list")
            continue
        missing = [item for item in REQUIRED_SCALE_INVARIANTS if item not in req]
        if missing:
            failures.append(
                f"level '{level_name}' missing required invariants: {', '.join(missing)}"
            )

    object_specs = contract.get("major_object_types")
    if not isinstance(object_specs, dict):
        failures.append("schema/contracts/scale_invariant_contract.yaml missing 'major_object_types' mapping")
        return

    known_levels = set(levels)

    for type_id in sorted(type_surface):
        type_spec = object_specs.get(type_id)
        if not isinstance(type_spec, dict):
            failures.append(
                f"major object type '{type_id}' missing mapping entry in schema/contracts/scale_invariant_contract.yaml"
            )
            continue

        scale_level = type_spec.get("scale_level")
        if scale_level not in known_levels:
            failures.append(
                f"major object type '{type_id}' scale_level must be one of: {', '.join(sorted(known_levels))}"
            )

        parent_map = type_spec.get("parent_level_mapping")
        child_map = type_spec.get("child_projection_mapping")
        if not isinstance(parent_map, dict) or not parent_map:
            failures.append(f"major object type '{type_id}' must declare parent_level_mapping")
        if not isinstance(child_map, dict) or not child_map:
            failures.append(f"major object type '{type_id}' must declare child_projection_mapping")

        rules = type_spec.get("invariant_preservation_rules")
        if not isinstance(rules, dict):
            failures.append(f"major object type '{type_id}' must declare invariant_preservation_rules")
            continue
        missing_rules = [inv for inv in REQUIRED_SCALE_INVARIANTS if inv not in rules]
        if missing_rules:
            failures.append(
                f"major object type '{type_id}' invariant_preservation_rules missing: {', '.join(missing_rules)}"
            )


def check_scale_projection_examples(contract: dict[str, Any], failures: list[str]) -> None:
    object_specs = contract.get("major_object_types", {})
    level_specs = contract.get("levels", {})

    for path, example in gather_examples():
        object_type = example.get("object_type")
        if object_type not in object_specs:
            continue

        if not _has_values(
            example,
            [
                "scale_level",
                "parent_level_mapping",
                "child_projection_mapping",
                "invariant_preservation_rules",
            ],
        ):
            failures.append(
                f"example {path.relative_to(ROOT)} (object_type={object_type}) must declare scale_level, parent_level_mapping, child_projection_mapping, and invariant_preservation_rules"
            )
            continue

        scale_level = example.get("scale_level")
        if scale_level not in level_specs:
            failures.append(
                f"example {path.relative_to(ROOT)} has unknown scale_level '{scale_level}'"
            )
            continue

        required_invariants = set(
            level_specs.get(scale_level, {}).get("required_invariants", REQUIRED_SCALE_INVARIANTS)
        )
        rules = example.get("invariant_preservation_rules", {})
        if not isinstance(rules, dict):
            failures.append(
                f"example {path.relative_to(ROOT)} invariant_preservation_rules must be a mapping"
            )
            continue

        missing_invariants = [inv for inv in required_invariants if inv not in rules]
        if missing_invariants:
            failures.append(
                f"example {path.relative_to(ROOT)} missing invariant preservation rules for: {', '.join(sorted(missing_invariants))}"
            )

        parent_map = example.get("parent_level_mapping", {})
        child_map = example.get("child_projection_mapping", {})
        if not isinstance(parent_map, dict) or not isinstance(child_map, dict):
            failures.append(
                f"example {path.relative_to(ROOT)} parent_level_mapping and child_projection_mapping must be mappings"
            )
            continue

        for target_level in [*parent_map.keys(), *child_map.keys()]:
            if target_level not in level_specs:
                failures.append(
                    f"example {path.relative_to(ROOT)} projection target '{target_level}' is not defined in contract levels"
                )


def main() -> int:
    failures: list[str] = []

    if not INVARIANT_MAP_PATH.exists():
        print("DNA INVARIANT VALIDATION FAILURES:")
        print("- missing schema/invariants/first_order_invariants.yaml")
        return 1

    if not SCALE_CONTRACT_PATH.exists():
        print("DNA INVARIANT VALIDATION FAILURES:")
        print("- missing schema/contracts/scale_invariant_contract.yaml")
        return 1

    interface_fields = load_interface_fields()
    type_surface = load_type_surface(interface_fields)
    mapping = load_yaml(INVARIANT_MAP_PATH)
    scale_contract = load_yaml(SCALE_CONTRACT_PATH)

    check_mapping_structure(type_surface, mapping, failures)
    check_examples(mapping, failures)
    check_scale_contract_structure(type_surface, scale_contract, failures)
    check_scale_projection_examples(scale_contract, failures)

    if failures:
        print("DNA INVARIANT VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("DNA invariant validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
