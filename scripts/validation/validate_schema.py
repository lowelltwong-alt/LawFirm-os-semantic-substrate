import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schema"


def load_yaml(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def main() -> int:
    failures: list[str] = []

    manifest_path = SCHEMA_ROOT / "manifest.yaml"
    manifest = load_yaml(manifest_path)
    if not isinstance(manifest, dict):
        failures.append("schema/manifest.yaml must parse to a mapping")
    else:
        for field in ("schema_set_id", "version", "status", "phase", "files"):
            if field not in manifest:
                failures.append(f"schema/manifest.yaml missing '{field}'")

        for file_ref in manifest.get("files", []):
            target = ROOT / file_ref
            if not target.exists():
                failures.append(f"manifest references missing file: {file_ref}")

    interfaces = {path.stem for path in (SCHEMA_ROOT / "interfaces").glob("*.yaml")}
    enums = {path.stem for path in (SCHEMA_ROOT / "enums").glob("*.yaml")}

    for category in ("interfaces", "types", "enums"):
        for path in sorted((SCHEMA_ROOT / category).glob("*.yaml")):
            data = load_yaml(path)
            if not isinstance(data, dict):
                failures.append(f"{path.relative_to(ROOT)} must parse to a mapping")
                continue

            for field in ("kind", "id", "version", "status"):
                if field not in data:
                    failures.append(f"{path.relative_to(ROOT)} missing '{field}'")

            if category == "types":
                for field in ("implements", "description"):
                    if field not in data:
                        failures.append(f"{path.relative_to(ROOT)} missing '{field}'")
                for interface_name in data.get("implements", []):
                    if interface_name not in interfaces:
                        failures.append(
                            f"{path.relative_to(ROOT)} implements unknown interface '{interface_name}'"
                        )

            if category == "interfaces":
                if "required_fields" not in data:
                    failures.append(f"{path.relative_to(ROOT)} missing 'required_fields'")

            if category == "enums" and "values" not in data:
                failures.append(f"{path.relative_to(ROOT)} missing 'values'")

    if "trust_zone" not in enums:
        failures.append("schema/enums/trust_zone.yaml is required")
    if "confidence_level" not in enums:
        failures.append("schema/enums/confidence_level.yaml is required")

    if failures:
        print("SCHEMA VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Schema validation scaffolding checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
