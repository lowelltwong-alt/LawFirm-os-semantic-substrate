import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCHEMA_ROOT = ROOT / "schema"


def parse_simple_key(path: Path, key: str) -> str | None:
    prefix = f"{key}:"
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped.startswith(prefix):
            value = stripped[len(prefix):].strip()
            return value.strip("'\"")
    return None


def main() -> int:
    failures: list[str] = []

    manifest = SCHEMA_ROOT / "manifest.yaml"
    if not manifest.exists():
        failures.append("Missing schema/manifest.yaml")

    for category in ("interfaces", "types", "enums"):
        for path in sorted((SCHEMA_ROOT / category).glob("*.yaml")):
            expected = path.stem
            actual_id = parse_simple_key(path, "id")
            actual_kind = parse_simple_key(path, "kind")

            if actual_id != expected:
                failures.append(
                    f"{path.relative_to(ROOT)}: id '{actual_id}' does not match filename '{expected}'"
                )

            if actual_kind is None:
                failures.append(f"{path.relative_to(ROOT)}: missing kind")

    if failures:
        print("ID CHECK FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("ID checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
