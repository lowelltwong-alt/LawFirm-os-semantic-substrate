import json
import os

BASE = os.path.dirname(os.path.dirname(__file__))


def load_json(path):
    with open(path, "r") as f:
        return json.load(f)


def check_paths_exist(paths):
    missing = []
    for p in paths:
        full = os.path.join(BASE, p)
        if not os.path.exists(full):
            missing.append(p)
    return missing


def main():
    manifest_path = os.path.join(BASE, "governance", "canonical_spine_manifest.json")
    manifest = load_json(manifest_path)

    missing_schemas = check_paths_exist(manifest["canonical_schemas"])
    missing_scripts = check_paths_exist(manifest["validation_scripts"])

    if missing_schemas or missing_scripts:
        print("Canonical spine misalignment detected")
        if missing_schemas:
            print("Missing schemas:", missing_schemas)
        if missing_scripts:
            print("Missing validation scripts:", missing_scripts)
        raise Exception("Canonical spine validation failed")

    print("Canonical spine validation passed")


if __name__ == "__main__":
    main()
