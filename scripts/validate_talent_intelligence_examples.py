#!/usr/bin/env python3
"""Basic validation for talent intelligence extension examples.

This script is intentionally lightweight so it can run in CI without external
Python dependencies. It validates:

1. JSON parseability for all example files.
2. Presence of expected top-level object_type values.
3. Presence of key required fields for current example shapes.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
EXAMPLES_DIR = REPO_ROOT / "examples" / "talent_intelligence"

EXPECTED = {
    "attorney_minimal_example.json": {
        "type": "attorney",
        "required": ["attorney_id", "canonical_name", "status", "authority_zone", "confidence_posture"],
    },
    "attorney_firm_change_example.json": {
        "container_keys": ["attorney", "employment_episodes"],
    },
    "common_name_collision_example.json": {
        "container_keys": ["scenario", "candidate_group", "match_posture", "attorney_candidates"],
    },
    "leopard_list_intake_example.json": {
        "container_keys": ["intake_artifact", "mapped_source_row", "provisional_outputs"],
    },
    "firm_instability_claim_example.json": {
        "type": "talent_signal_claim",
        "required": ["claim_id", "signal_type", "subject_ref", "statement", "status", "authority_zone", "confidence_posture"],
    },
    "portable_book_claim_example.json": {
        "type": "talent_signal_claim",
        "required": ["claim_id", "signal_type", "subject_ref", "statement", "status", "authority_zone", "confidence_posture"],
    },
    "relationship_warmth_claim_example.json": {
        "type": "talent_signal_claim",
        "required": ["claim_id", "signal_type", "subject_ref", "statement", "status", "authority_zone", "confidence_posture"],
    },
}


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        return [f"{path.name}: invalid JSON: {exc}"]

    spec = EXPECTED.get(path.name)
    if spec is None:
        return [f"{path.name}: no validation spec found"]

    if "type" in spec:
        if not isinstance(data, dict):
            errors.append(f"{path.name}: expected top-level object")
            return errors
        if data.get("object_type") != spec["type"]:
            errors.append(
                f"{path.name}: expected object_type={spec['type']!r}, found {data.get('object_type')!r}"
            )
        for key in spec.get("required", []):
            if key not in data:
                errors.append(f"{path.name}: missing required key {key!r}")

    if "container_keys" in spec:
        if not isinstance(data, dict):
            errors.append(f"{path.name}: expected top-level object")
            return errors
        for key in spec["container_keys"]:
            if key not in data:
                errors.append(f"{path.name}: missing container key {key!r}")

    return errors


def main() -> int:
    missing = [name for name in EXPECTED if not (EXAMPLES_DIR / name).exists()]
    if missing:
        for name in missing:
            print(f"Missing example file: {name}", file=sys.stderr)
        return 1

    all_errors: list[str] = []
    for name in sorted(EXPECTED):
        all_errors.extend(validate_file(EXAMPLES_DIR / name))

    if all_errors:
        for err in all_errors:
            print(err, file=sys.stderr)
        return 1

    print("Talent intelligence example validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
