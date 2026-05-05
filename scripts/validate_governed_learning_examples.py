import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_directory(schema_path: Path, target_dir: Path):
    schema = load_json(schema_path)
    validator = Draft202012Validator(schema, registry=build_local_schema_registry(BASE))

    if not target_dir.exists():
        print(f"SKIP: {target_dir} does not exist")
        return 0

    failures = 0
    for file_path in sorted(target_dir.glob("*.json")):
        data = load_json(file_path)
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            failures += 1
            print(f"INVALID: {file_path}")
            for error in errors:
                path = ".".join(str(p) for p in error.path) or "<root>"
                print(f"  - {path}: {error.message}")
        else:
            print(f"VALID: {file_path}")
    return failures


def main() -> int:
    validations = [
        (
            BASE / "schemas" / "exception-event.schema.json",
            BASE / "examples" / "exceptions" / "events",
        ),
        (
            BASE / "schemas" / "pressure-vector.schema.json",
            BASE / "examples" / "exceptions" / "pressure-vectors",
        ),
        (
            BASE / "schemas" / "adaptation-proposal.schema.json",
            BASE / "examples" / "exceptions" / "adaptation-proposals",
        ),
        (
            BASE / "schemas" / "promotion-decision.schema.json",
            BASE / "examples" / "exceptions" / "promotion-decisions",
        ),
    ]

    failures = 0
    for schema_path, target_dir in validations:
        if not schema_path.exists():
            print(f"MISSING SCHEMA: {schema_path}")
            failures += 1
            continue
        failures += validate_directory(schema_path, target_dir)

    if failures:
        print(f"Governed learning validation failed with {failures} error group(s).")
        return 1

    print("Governed learning examples validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
