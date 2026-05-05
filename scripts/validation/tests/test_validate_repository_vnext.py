from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts import validate_repository_vnext


class ValidateRepositoryVNextTests(unittest.TestCase):
    def test_matches_expected_schema_accepts_schema_type_and_version(self) -> None:
        payload = {"schema_type": "artifact", "schema_version": "v1"}

        self.assertTrue(
            validate_repository_vnext.matches_expected_schema(
                payload,
                "artifact",
                "v1",
                "artifact-schema-v1",
            )
        )

    def test_matches_expected_schema_accepts_authoritative_schema_id(self) -> None:
        payload = {"schema_id": "artifact-schema-v1", "template_id": "artifact-template-v1"}

        self.assertTrue(
            validate_repository_vnext.matches_expected_schema(
                payload,
                "artifact",
                "v1",
                "artifact-schema-v1",
            )
        )

    def test_matches_expected_schema_rejects_unrelated_schema_id(self) -> None:
        payload = {"schema_id": "claim-schema-v3"}

        self.assertFalse(
            validate_repository_vnext.matches_expected_schema(
                payload,
                "artifact",
                "v1",
                "artifact-schema-v1",
            )
        )

    def test_active_executive_brief_example_matches_registered_view_schema(self) -> None:
        repo_root = Path(__file__).resolve().parents[3]
        payload = json.loads(
            (repo_root / "examples" / "innovation-os" / "executive-brief-object.example.json").read_text(
                encoding="utf-8"
            )
        )

        self.assertTrue(
            validate_repository_vnext.matches_expected_schema(
                payload,
                "view-executive-brief",
                "draft-v1",
                "view-executive-brief-v1",
            )
        )


if __name__ == "__main__":
    unittest.main()
