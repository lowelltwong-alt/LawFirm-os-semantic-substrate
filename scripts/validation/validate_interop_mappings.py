from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[2]
INTEROP_PROFILES_DIR = ROOT / "interop" / "profiles"
SCHEMA_MANIFEST = ROOT / "schema" / "manifest.yaml"
SCHEMA_TYPES_DIR = ROOT / "schema" / "types"

ALLOWED_MAPPING_MODES = {"exact", "transformed", "unsupported"}


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def build_core_type_versions() -> dict[str, str]:
    versions: dict[str, str] = {}
    for path in sorted(SCHEMA_TYPES_DIR.glob("*.yaml")):
        data = load_yaml(path)
        if isinstance(data, dict) and isinstance(data.get("id"), str):
            versions[data["id"]] = str(data.get("version", ""))
    return versions


def validate_mapping_rules(
    profile_name: str, context: str, rules: list[dict], failures: list[str]
) -> None:
    for index, rule in enumerate(rules, start=1):
        if not isinstance(rule, dict):
            failures.append(f"{profile_name} {context} rule #{index} must be a mapping")
            continue

        mode = rule.get("mapping_mode")
        confidence = rule.get("confidence")
        lossiness = rule.get("lossiness")
        target_path = rule.get("target_path")

        if mode not in ALLOWED_MAPPING_MODES:
            failures.append(
                f"{profile_name} {context} rule #{index} has invalid mapping_mode '{mode}'"
            )

        if not isinstance(confidence, (int, float)) or not (0.0 <= float(confidence) <= 1.0):
            failures.append(
                f"{profile_name} {context} rule #{index} confidence must be between 0.0 and 1.0"
            )

        if not isinstance(lossiness, str) or not lossiness.strip():
            failures.append(f"{profile_name} {context} rule #{index} must include a lossiness note")

        if mode in {"exact", "transformed"} and not target_path:
            failures.append(
                f"{profile_name} {context} rule #{index} with mode '{mode}' must include target_path"
            )

        if mode == "unsupported" and target_path not in (None, ""):
            failures.append(
                f"{profile_name} {context} rule #{index} with mode 'unsupported' must not declare target_path"
            )


def main() -> int:
    failures: list[str] = []

    if not SCHEMA_MANIFEST.exists():
        print("INTEROP MAPPING VALIDATION FAILURES:")
        print("- missing schema manifest")
        return 1

    manifest = load_yaml(SCHEMA_MANIFEST)
    if not isinstance(manifest, dict):
        print("INTEROP MAPPING VALIDATION FAILURES:")
        print("- schema/manifest.yaml must parse to a mapping")
        return 1

    manifest_schema_set_id = manifest.get("schema_set_id")
    manifest_version = str(manifest.get("version"))
    core_type_versions = build_core_type_versions()

    profile_paths = sorted(INTEROP_PROFILES_DIR.glob("*.yaml"))
    if not profile_paths:
        failures.append("interop/profiles must contain at least one mapping profile")

    for profile_path in profile_paths:
        profile = load_yaml(profile_path)
        rel = profile_path.relative_to(ROOT)

        if not isinstance(profile, dict):
            failures.append(f"{rel} must parse to a mapping")
            continue

        for field in ("profile_id", "profile_version", "core_schema", "mapping_metadata_contract"):
            if field not in profile:
                failures.append(f"{rel} missing required field '{field}'")

        core_schema = profile.get("core_schema", {})
        if not isinstance(core_schema, dict):
            failures.append(f"{rel} core_schema must be a mapping")
            continue

        if core_schema.get("schema_set_id") != manifest_schema_set_id:
            failures.append(
                f"{rel} core_schema.schema_set_id '{core_schema.get('schema_set_id')}' "
                f"does not match schema/manifest.yaml '{manifest_schema_set_id}'"
            )

        if str(core_schema.get("schema_set_version")) != manifest_version:
            failures.append(
                f"{rel} core_schema.schema_set_version '{core_schema.get('schema_set_version')}' "
                f"does not match schema/manifest.yaml '{manifest_version}'"
            )

        declared_type_versions = core_schema.get("core_type_versions", {})
        if not isinstance(declared_type_versions, dict):
            failures.append(f"{rel} core_schema.core_type_versions must be a mapping")
            declared_type_versions = {}

        mapped_types: set[str] = set()

        for section_name in ("core_entity_mappings", "provenance_mappings"):
            section = profile.get(section_name, [])
            if section and not isinstance(section, list):
                failures.append(f"{rel} {section_name} must be a list")
                continue
            for entry in section:
                if not isinstance(entry, dict):
                    failures.append(f"{rel} has non-mapping entry in {section_name}")
                    continue
                core_entity = entry.get("core_entity")
                if isinstance(core_entity, str):
                    mapped_types.add(core_entity)
                rules = entry.get("mapping_rules", [])
                if not isinstance(rules, list):
                    failures.append(f"{rel} {section_name} entry for {core_entity} has non-list mapping_rules")
                    continue
                validate_mapping_rules(str(rel), f"{section_name}:{core_entity}", rules, failures)

        relation_mappings = profile.get("core_relation_mappings", [])
        if relation_mappings and not isinstance(relation_mappings, list):
            failures.append(f"{rel} core_relation_mappings must be a list")
            relation_mappings = []

        for relation_entry in relation_mappings:
            if not isinstance(relation_entry, dict):
                failures.append(f"{rel} has non-mapping entry in core_relation_mappings")
                continue
            core_relation = relation_entry.get("core_relation")
            if isinstance(core_relation, str):
                mapped_types.add(core_relation)
            strategy = relation_entry.get("target_predicate_strategy", {})
            if not isinstance(strategy, dict):
                failures.append(
                    f"{rel} core_relation_mappings entry for {core_relation} must include mapping target_predicate_strategy"
                )
                continue
            validate_mapping_rules(
                str(rel),
                f"core_relation_mappings:{core_relation}",
                [strategy],
                failures,
            )

        for mapped_type in sorted(mapped_types):
            if mapped_type not in core_type_versions:
                failures.append(f"{rel} maps unknown core type '{mapped_type}'")
                continue
            declared_version = declared_type_versions.get(mapped_type)
            actual_version = core_type_versions[mapped_type]
            if str(declared_version) != actual_version:
                failures.append(
                    f"{rel} core type version mismatch for '{mapped_type}': "
                    f"declared={declared_version}, actual={actual_version}"
                )

        for sample_output in profile.get("sample_outputs", []):
            sample_path = ROOT / str(sample_output)
            if not sample_path.exists():
                failures.append(f"{rel} references missing sample output: {sample_output}")

    if failures:
        print("INTEROP MAPPING VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Interop mapping validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
