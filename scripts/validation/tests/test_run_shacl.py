from __future__ import annotations

import contextlib
import io
import unittest

from scripts.validation import run_shacl


class RunShaclTests(unittest.TestCase):
    def test_core_pair_run_pair_fails_closed_without_same_namespace_focus_nodes(self) -> None:
        data_graph = run_shacl.SHAPES / "core.ttl"
        shape_graph = run_shacl.SHAPES / "core.shacl.ttl"
        buffer = io.StringIO()

        with contextlib.redirect_stdout(buffer):
            result = run_shacl.run_pair(data_graph, shape_graph)

        output = buffer.getvalue()

        self.assertEqual(result, 1)
        self.assertIn("FAIL CLOSED", output)
        self.assertIn("same-namespace focus-node data graph", output)
        self.assertIn("Core SHACL conformance is not currently claimed", output)
        self.assertIn("A pySHACL PASS here would be vacuous", output)


if __name__ == "__main__":
    unittest.main()
