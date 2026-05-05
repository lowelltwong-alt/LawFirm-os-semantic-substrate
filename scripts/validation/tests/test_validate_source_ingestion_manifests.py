from __future__ import annotations

from copy import deepcopy
import unittest
from pathlib import Path

from scripts.validation import validate_source_ingestion_manifests


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "examples"


def load_json(path: Path):
    return validate_source_ingestion_manifests.load_json(path)


class ValidateSourceIngestionManifestsTests(unittest.TestCase):
    def test_existing_manifest_example_is_metadata_complete(self) -> None:
        failures = validate_source_ingestion_manifests.collect_failures(
            load_json(EXAMPLES / "documents" / "legal-document.example.json"),
            load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"),
        )

        self.assertEqual(failures, [])

    def test_active_source_without_required_provenance_metadata_fails(self) -> None:
        legal_bundle = load_json(EXAMPLES / "documents" / "legal-document.example.json")
        manifest = deepcopy(load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"))
        del manifest["checksum"]
        manifest["lifecycle_status"] = "draft"

        failures = validate_source_ingestion_manifests.collect_failures(
            legal_bundle,
            manifest,
        )

        joined = "\n".join(failures)
        self.assertIn("manifest validation: 'checksum' is a required property", joined)
        self.assertIn(
            "active governed source examples require a source-ingestion-manifest with lifecycle_status approved or active",
            joined,
        )

    def test_obvious_forbidden_content_field_fails(self) -> None:
        legal_bundle = load_json(EXAMPLES / "documents" / "legal-document.example.json")
        manifest = deepcopy(load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"))
        manifest["content"] = "synthetic forbidden content field"

        failures = validate_source_ingestion_manifests.collect_failures(
            legal_bundle,
            manifest,
        )

        joined = "\n".join(failures)
        self.assertIn("Additional properties are not allowed", joined)

    def test_source_text_embedded_in_structured_field_fails(self) -> None:
        legal_bundle = load_json(EXAMPLES / "documents" / "legal-document.example.json")
        manifest = deepcopy(load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"))
        manifest["source_identifier"] = "The Client agrees to provide timely documentation and the Firm agrees to maintain confidentiality."

        failures = validate_source_ingestion_manifests.collect_failures(
            legal_bundle,
            manifest,
        )

        joined = "\n".join(failures)
        self.assertIn("source-ingestion-manifest.source_identifier", joined)


if __name__ == "__main__":
    unittest.main()
