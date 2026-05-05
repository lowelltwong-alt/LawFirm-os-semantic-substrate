import json
import os

import sys
import pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent))
from address_registry import validate_address_struct
from address_system import build_address, validate_address

BASE_DIR = "examples"
EXCLUDED_SUBDIRS = {
    os.path.join("examples", "talent_intelligence"),
    os.path.join("examples", "exceptions"),
}
EXCLUDED_FILES = {
    os.path.normpath(
        os.path.join("examples", "poc", "insurance-defense-budget-gold-cases.synthetic.json")
    ),
    os.path.normpath(
        os.path.join("examples", "views", "view-budget-workbook.synthetic.example.json")
    ),
}


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def validate_object(path):
    obj = load_json(path)

    if "address" not in obj:
        raise Exception(f"Missing address in {path}")

    if "address_struct" not in obj:
        raise Exception(f"Missing address_struct in {path}")

    validate_address_struct(obj["address_struct"])
    if not isinstance(obj["address"], str) or not validate_address(obj["address"]):
        raise Exception(f"Invalid canonical address in {path}")

    expected_address = build_address(
        obj["address_struct"]["environment"],
        obj["address_struct"]["authority_zone"],
        obj["address_struct"]["layer"],
        obj["address_struct"]["domain"],
        obj["address_struct"]["module"],
        obj["address_struct"]["object_type"],
        obj["address_struct"]["object_id"],
        obj["address_struct"]["version"],
    )
    if obj["address"] != expected_address:
        raise Exception(f"address and address_struct do not match in {path}")

    return True


def walk_examples():
    failures = []
    for root, _, files in os.walk(BASE_DIR):
        normalized_root = os.path.normpath(root)
        if normalized_root in EXCLUDED_SUBDIRS:
            continue
        for f in files:
            if f.endswith(".json"):
                path = os.path.join(root, f)
                if os.path.normpath(path) in EXCLUDED_FILES:
                    continue
                try:
                    validate_object(path)
                except Exception as e:
                    failures.append(str(e))

    if failures:
        print("ADDRESS VALIDATION FAILURES:")
        for f in failures:
            print(f)
        raise SystemExit(1)

    print("All objects passed address validation.")


if __name__ == "__main__":
    walk_examples()
