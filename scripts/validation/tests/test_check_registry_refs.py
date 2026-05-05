from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts import check_registry_refs


class CheckRegistryRefsTests(unittest.TestCase):
    def test_structured_registry_with_non_string_path_fails_cleanly(self) -> None:
        registry = {
            "schemas": [
                {
                    "schema_id": "broken-schema",
                    "path": {"not": "a-string"},
                }
            ]
        }

        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            failures: list[str] = []
            with patch.object(check_registry_refs, "ROOT", root):
                check_registry_refs.check_registry_paths(registry, failures)

        self.assertEqual(len(failures), 1)
        self.assertIn("broken-schema", failures[0])
        self.assertIn("must be a string", failures[0])


if __name__ == "__main__":
    unittest.main()
