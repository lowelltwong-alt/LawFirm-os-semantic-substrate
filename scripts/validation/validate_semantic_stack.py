from pathlib import Path


BASE = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = [
    BASE / "schema" / "types" / "jsonld_context.yaml",
    BASE / "schema" / "types" / "named_graph_manifest.yaml",
    BASE / "shapes" / "semantic-stack.ttl",
    BASE / "shapes" / "projection.ttl",
    BASE / "docs" / "validation" / "semantic-stack-validation.md",
]


def main():
    missing = [str(path) for path in REQUIRED_PATHS if not path.exists()]
    if missing:
        print("SEMANTIC STACK VALIDATION FAILURES:")
        for path in missing:
            print(f"missing required scaffold: {path}")
        raise SystemExit(1)

    print("Semantic stack validation scaffold passed.")


if __name__ == "__main__":
    main()
