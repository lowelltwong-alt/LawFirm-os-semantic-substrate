from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from scripts import check_repo_drift


class CheckRepoDriftTests(unittest.TestCase):
    def test_missing_flat_schema_registry_passes(self) -> None:
        root = Path("repo-root")

        def fake_exists(path: Path) -> bool:
            return path != root / "schemas" / "schema_registry.json"

        with patch("pathlib.Path.exists", autospec=True, side_effect=fake_exists):
            passed, note = check_repo_drift.check_flat_schema_registry_state(root)

        self.assertTrue(passed)
        self.assertIn("has been removed", note)

    def test_flat_schema_registry_with_missing_target_fails(self) -> None:
        root = Path("repo-root")

        def fake_exists(path: Path) -> bool:
            return path == root / "schemas" / "schema_registry.json"

        with (
            patch("pathlib.Path.exists", autospec=True, side_effect=fake_exists),
            patch(
                "scripts.check_repo_drift.load_json",
                return_value={"claim:v2": "schemas/claim_stub_v2.schema.json"},
            ),
        ):
            passed, note = check_repo_drift.check_flat_schema_registry_state(root)

        self.assertFalse(passed)
        self.assertIn("claim_stub_v2.schema.json", note)

    def test_flat_schema_registry_with_non_string_entry_fails_cleanly(self) -> None:
        root = Path("repo-root")

        def fake_exists(path: Path) -> bool:
            return path == root / "schemas" / "schema_registry.json"

        with (
            patch("pathlib.Path.exists", autospec=True, side_effect=fake_exists),
            patch(
                "scripts.check_repo_drift.load_json",
                return_value={"schemas": ["not-a-flat-path-entry"]},
            ),
        ):
            passed, note = check_repo_drift.check_flat_schema_registry_state(root)

        self.assertFalse(passed)
        self.assertIn("non-string flat-registry entries", note)


if __name__ == "__main__":
    unittest.main()
