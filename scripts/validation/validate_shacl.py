import sys
from pathlib import Path

from rdflib import Graph


ROOT = Path(__file__).resolve().parents[2]
SHAPES_ROOT = ROOT / "shapes"


def main() -> int:
    failures: list[str] = []

    for path in sorted(SHAPES_ROOT.glob("*.ttl")):
        try:
            graph = Graph()
            graph.parse(path, format="turtle")
            print(f"PARSED: {path.relative_to(ROOT)} ({len(graph)} triples)")
        except Exception as exc:
            failures.append(f"{path.relative_to(ROOT)}: {exc}")

    if failures:
        print("SHACL SHAPE FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("SHACL seed shape parsing passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
