from __future__ import annotations

import unittest
from pathlib import Path

from jsonschema import Draft202012Validator

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


class JsonschemaRegistrySupportTests(unittest.TestCase):
    def test_local_registry_resolves_relative_and_absolute_address_refs(self) -> None:
        base = Path(__file__).resolve().parents[3]
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "type": "object",
            "required": ["address", "address_struct"],
            "properties": {
                "address": {"$ref": "address.schema.json"},
                "address_struct": {
                    "$ref": "https://fmg.example/schemas/address_struct.schema.json"
                },
            },
        }

        validator = Draft202012Validator(
            schema,
            registry=build_local_schema_registry(base),
        )
        errors = sorted(
            validator.iter_errors(
                {
                    "address": "/example/public/schema/test_domain/test_module/test_object/SRC-example/v1",
                    "address_struct": {
                        "environment": "example",
                        "authority_zone": "public",
                        "layer": "schema",
                        "domain": "test_domain",
                        "module": "test_module",
                        "object_type": "source",
                        "object_id": "SRC-example",
                        "version": "v1",
                    },
                }
            ),
            key=lambda error: list(error.path),
        )

        self.assertEqual(errors, [])


if __name__ == "__main__":
    unittest.main()
