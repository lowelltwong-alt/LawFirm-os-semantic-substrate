from __future__ import annotations

import unittest

from scripts import validate_examples_registry


class ValidateExamplesRegistryTests(unittest.TestCase):
    def test_resolve_registry_entry_prefers_schema_type_and_version(self) -> None:
        registry_by_key = {
            "artifact:v1": {"schema_id": "artifact-schema-v1", "path": "schemas/artifact.schema.json"}
        }
        registry_by_id = {
            "artifact-schema-v1": {"schema_id": "artifact-schema-v1", "path": "schemas/artifact.schema.json"}
        }
        payload = {"schema_type": "artifact", "schema_version": "v1"}

        label, entry = validate_examples_registry.resolve_registry_entry(
            payload,
            registry_by_key,
            registry_by_id,
        )

        self.assertEqual(label, "artifact:v1")
        self.assertEqual(entry["schema_id"], "artifact-schema-v1")

    def test_resolve_registry_entry_falls_back_to_schema_id(self) -> None:
        registry_by_key = {}
        registry_by_id = {
            "artifact-schema-v1": {"schema_id": "artifact-schema-v1", "path": "schemas/artifact.schema.json"}
        }
        payload = {"schema_id": "artifact-schema-v1", "template_id": "artifact-template-v1"}

        label, entry = validate_examples_registry.resolve_registry_entry(
            payload,
            registry_by_key,
            registry_by_id,
        )

        self.assertEqual(label, "artifact-schema-v1")
        self.assertEqual(entry["path"], "schemas/artifact.schema.json")

    def test_declared_unknown_schema_id_is_unresolved(self) -> None:
        status, label, entry = validate_examples_registry.classify_registry_resolution(
            {"schema_id": "missing-schema"},
            {},
            {},
        )

        self.assertEqual(status, "declared_unresolved")
        self.assertIsNone(label)
        self.assertIsNone(entry)

    def test_declared_unknown_schema_type_and_version_is_unresolved(self) -> None:
        status, label, entry = validate_examples_registry.classify_registry_resolution(
            {"schema_type": "artifact", "schema_version": "v9"},
            {},
            {},
        )

        self.assertEqual(status, "declared_unresolved")
        self.assertIsNone(label)
        self.assertIsNone(entry)

    def test_metadata_less_example_remains_missing(self) -> None:
        status, label, entry = validate_examples_registry.classify_registry_resolution(
            {"title": "metadata-less fixture"},
            {},
            {},
        )

        self.assertEqual(status, "missing")
        self.assertIsNone(label)
        self.assertIsNone(entry)


if __name__ == "__main__":
    unittest.main()
