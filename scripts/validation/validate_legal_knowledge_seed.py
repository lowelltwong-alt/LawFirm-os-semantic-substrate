#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[2]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate(schema_rel: str, example_rel: str) -> list[str]:
    schema = load(ROOT / schema_rel)
    example = load(ROOT / example_rel)
    validator = Draft202012Validator(schema)
    return [error.message for error in validator.iter_errors(example)]


def main() -> int:
    checks = [
        ("schemas/legal-document-ingestion-manifest.schema.json", "examples/legal-knowledge-runtime/legal_document_ingestion_manifest.synthetic.json"),
        ("schemas/legal-context-bundle.schema.json", "examples/legal-knowledge-runtime/legal_context_bundle.synthetic.json"),
    ]
    failures: list[str] = []
    for schema_rel, example_rel in checks:
        for failure in validate(schema_rel, example_rel):
            failures.append(f"{example_rel}: {failure}")
    if failures:
        print("Legal knowledge seed validation failed:")
        for failure in failures:
            print("-", failure)
        return 1
    print("Legal knowledge seed validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
