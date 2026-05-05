import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


BASE = Path(__file__).resolve().parents[1]
if str(BASE) not in sys.path:
    sys.path.insert(0, str(BASE))

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


ROOT = Path(__file__).resolve().parents[1]
SCHEMAS = ROOT / "schemas"
EXAMPLES = ROOT / "examples"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def validator_for(schema_name: str) -> Draft202012Validator:
    schema = load_json(SCHEMAS / schema_name)
    return Draft202012Validator(schema, registry=build_local_schema_registry(ROOT))


def validate_single(validator: Draft202012Validator, payload: dict, label: str, failures: list[str]) -> None:
    errors = sorted(validator.iter_errors(payload), key=lambda error: list(error.path))
    for error in errors:
        location = ".".join(str(part) for part in error.path)
        if location:
            failures.append(f"{label}: {location}: {error.message}")
        else:
            failures.append(f"{label}: {error.message}")


def main() -> int:
    failures: list[str] = []

    legal_bundle = load_json(EXAMPLES / "documents" / "legal-document.example.json")
    source_ingestion_manifest = load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json")
    gold_standard_bundle = load_json(EXAMPLES / "gold-standard" / "gold-standard-asset.example.json")

    validators = {
        "document": validator_for("document.schema.json"),
        "source-artifact": validator_for("source-artifact.schema.json"),
        "source-ingestion-manifest": validator_for("source-ingestion-manifest.schema.json"),
        "document-version": validator_for("document-version.schema.json"),
        "canonical-text": validator_for("canonical-text.schema.json"),
        "component": validator_for("component.schema.json"),
        "span-selector": validator_for("span-selector.schema.json"),
        "citation-target": validator_for("citation-target.schema.json"),
        "citation-mention": validator_for("citation-mention.schema.json"),
        "gold-standard-asset": validator_for("gold-standard-asset.schema.json"),
    }

    validate_single(validators["document"], legal_bundle["document"], "legal-document.example.json:document", failures)
    validate_single(validators["source-artifact"], legal_bundle["source_artifact"], "legal-document.example.json:source_artifact", failures)
    validate_single(validators["source-ingestion-manifest"], source_ingestion_manifest, "source-ingestion-manifest.example.json", failures)
    validate_single(validators["document-version"], legal_bundle["document_version"], "legal-document.example.json:document_version", failures)
    validate_single(validators["canonical-text"], legal_bundle["canonical_text"], "legal-document.example.json:canonical_text", failures)

    for index, component in enumerate(legal_bundle.get("components", []), start=1):
        validate_single(validators["component"], component, f"legal-document.example.json:components[{index}]", failures)

    for index, selector in enumerate(legal_bundle.get("span_selectors", []), start=1):
        validate_single(validators["span-selector"], selector, f"legal-document.example.json:span_selectors[{index}]", failures)

    for index, target in enumerate(legal_bundle.get("citation_targets", []), start=1):
        validate_single(validators["citation-target"], target, f"legal-document.example.json:citation_targets[{index}]", failures)

    for index, mention in enumerate(legal_bundle.get("citation_mentions", []), start=1):
        validate_single(validators["citation-mention"], mention, f"legal-document.example.json:citation_mentions[{index}]", failures)

    validate_single(
        validators["gold-standard-asset"],
        gold_standard_bundle["gold_standard_asset"],
        "gold-standard-asset.example.json:gold_standard_asset",
        failures,
    )

    if failures:
        print("CANONICAL EXAMPLE VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Canonical document, source ingestion manifest, and Gold Standard examples validated successfully.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
