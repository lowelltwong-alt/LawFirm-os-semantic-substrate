from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from scripts.validation import validate_source_of_truth_coherence


class ValidateSourceOfTruthCoherenceTests(unittest.TestCase):
    def test_directory_paths_must_exist(self) -> None:
        with TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "present").mkdir()

            with patch.object(validate_source_of_truth_coherence, "ROOT", root):
                self.assertTrue(validate_source_of_truth_coherence.path_exists("present/"))
                self.assertFalse(validate_source_of_truth_coherence.path_exists("missing/"))


if __name__ == "__main__":
    unittest.main()
