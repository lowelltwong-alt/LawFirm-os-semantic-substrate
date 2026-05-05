import json
import os
import pathlib
import sys

from jsonschema import Draft202012Validator

_ROOT = pathlib.Path(__file__).parent.parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


def _load(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


schema = _load(_ROOT / "schemas" / "claim_v3.schema.json")
validator = Draft202012Validator(schema, registry=build_local_schema_registry(_ROOT))

for root, dirs, files in os.walk(str(_ROOT / "examples")):
    # Skip legacy/archive directories
    dirs[:] = [d for d in dirs if d not in {"legacy", "archive", "__pycache__"}]
    for f in files:
        if not f.endswith(".json"):
            continue
        data = _load(os.path.join(root, f))
        # Only validate files that declare themselves as claim:v3 against the v3 schema.
        if data.get("schema_type") != "claim" or data.get("schema_version") != "v3":
            continue
        errors = sorted(validator.iter_errors(data), key=lambda e: list(e.path))
        if errors:
            raise SystemExit(
                f"Validation failed for {os.path.join(root, f)}: {errors[0].message}"
            )

print("Validation passed")
