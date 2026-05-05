#!/usr/bin/env python3
"""Schema-based validation for talent intelligence extension examples.

This validator loads the extension JSON Schemas and validates both single-object
examples and composite container examples against the appropriate schema.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas" / "extensions" / "talent_intelligence"
EXAMPLES_DIR = REPO_ROOT / "examples" / "talent_intelligence"

SCHEMA_FILES = {
    "attorney": SCHEMA_DIR / "attorney.schema.json",
    "law_firm": SCHEMA_DIR / "law_firm.schema.json",
    "employment_episode": SCHEMA_DIR / "employment_episode.schema.json",
    "external_identifier": SCHEMA_DIR / "external_identifier.schema.json",
    "source_profile": SCHEMA_DIR / "source_profile.schema.json",
    "talent_signal_claim": SCHEMA_DIR / "talent_signal_claim.schema.json",
}

EXAMPLE_PLAN = {
    "attorney_minimal_example.json": [
        ("$", "attorney"),
    ],
    "attorney_firm_change_example.json": [
        ("attorney", "attorney"),
        ("employment_episodes[0]", "employment_episode"),
        ("employment_episodes[1]", "employment_episode"),
    ],
    "common_name_collision_example.json": [
        ("attorney_candidates[0]", "attorney"),
        ("attorney_candidates[1]", "attorney"),
    ],
    "leopard_list_intake_example.json": [
        ("provisional_outputs.source_profile", "source_profile"),
        ("provisional_outputs.provisional_attorney", "attorney"),
        ("provisional_outputs.provisional_employment_episode", "employment_episode"),
    ],
    "firm_instability_claim_example.json": [
        ("$", "talent_signal_claim"),
    ],
    "portable_book_claim_example.json": [
        ("$", "talent_signal_claim"),
    ],
    "relationship_warmth_claim_example.json": [
        ("$", "talent_signal_claim"),
    ],
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def get_by_path(data, path: str):
    if path == "$":
        return data
    current = data
    for part in path.split("."):
        if "[" in part and part.endswith("]"):
            key, idx_text = part[:-1].split("[")
            current = current[key][int(idx_text)]
        else:
            current = current[part]
    return current


def load_validators():
    validators = {}
    for key, path in SCHEMA_FILES.items():
        schema = load_json(path)
        validators[key] = Draft202012Validator(schema)
    return validators


def validate_example(example_path: Path, validators: dict[str, Draft202012Validator]) -> list[str]:
    errors: list[str] = []
    try:
        data = load_json(example_path)
    except Exception as exc:
        return [f"{example_path.name}: invalid JSON: {exc}"]

    plan = EXAMPLE_PLAN.get(example_path.name)
    if plan is None:
        return [f"{example_path.name}: no schema validation plan found"]

    for obj_path, schema_key in plan:
        try:
            obj = get_by_path(data, obj_path)
        except Exception as exc:
            errors.append(f"{example_path.name}: unable to resolve path {obj_path!r}: {exc}")
            continue

        validator = validators[schema_key]
        obj_errors = sorted(validator.iter_errors(obj), key=lambda e: list(e.absolute_path))
        for err in obj_errors:
            loc = "/".join(str(p) for p in err.absolute_path) or "$"
            errors.append(
                f"{example_path.name}: schema={schema_key} path={obj_path} field={loc}: {err.message}"
            )

    return errors


def main() -> int:
    validators = load_validators()
    all_errors: list[str] = []

    for name in sorted(EXAMPLE_PLAN):
        path = EXAMPLES_DIR / name
        if not path.exists():
            all_errors.append(f"Missing example file: {name}")
            continue
        all_errors.extend(validate_example(path, validators))

    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        return 1

    print("Talent intelligence schema validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
