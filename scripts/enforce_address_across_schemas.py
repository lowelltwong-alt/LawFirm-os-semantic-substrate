import json
import os

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from address_registry import validate_address_struct
from address_system import validate_address


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def check_file(path):
    data = load_json(path)

    schema_type = data.get("schema_type")
    if schema_type not in ["claim", "artifact"]:
        return True, None

    if "address" not in data:
        return False, "missing address field"

    if not isinstance(data["address"], str) or not validate_address(data["address"]):
        return False, "invalid canonical address string"

    if "address_struct" not in data:
        return False, "missing address_struct field"

    try:
        validate_address_struct(data["address_struct"])
    except Exception as exc:
        return False, str(exc)

    return True, None


def main():
    root = "examples"
    failures = []

    for dirpath, _, filenames in os.walk(root):
        for filename in filenames:
            if not filename.endswith(".json"):
                continue

            path = os.path.join(dirpath, filename)
            valid, error = check_file(path)
            if valid:
                print(f"ADDRESS OK: {path}")
            else:
                print(f"ADDRESS FAIL: {path} -> {error}")
                failures.append((path, error))

    if failures:
        raise SystemExit(1)

    print("Address enforcement passed for canonical example objects.")


if __name__ == "__main__":
    main()
