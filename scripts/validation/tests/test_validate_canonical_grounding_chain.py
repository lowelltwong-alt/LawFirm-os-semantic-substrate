from __future__ import annotations

from copy import deepcopy
import unittest
from pathlib import Path

from scripts.validation import validate_canonical_grounding_chain


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "examples"


def load_json(path: Path):
    return validate_canonical_grounding_chain.load_json(path)


class ValidateCanonicalGroundingChainTests(unittest.TestCase):
    def test_existing_answer_trace_bundle_is_grounded(self) -> None:
        failures = validate_canonical_grounding_chain.collect_failures(
            load_json(EXAMPLES / "documents" / "legal-document.example.json"),
            load_json(EXAMPLES / "documents" / "chunk-set.example.json"),
            load_json(EXAMPLES / "documents" / "answer-trace.example.json"),
            load_json(EXAMPLES / "gold-standard" / "gold-standard-asset.example.json"),
        )

        self.assertEqual(failures, [])

    def test_grounded_answer_without_resolvable_evidence_fails(self) -> None:
        legal = load_json(EXAMPLES / "documents" / "legal-document.example.json")
        chunks = load_json(EXAMPLES / "documents" / "chunk-set.example.json")
        answers = deepcopy(load_json(EXAMPLES / "documents" / "answer-trace.example.json"))
        gold = load_json(EXAMPLES / "gold-standard" / "gold-standard-asset.example.json")

        answers["answer_event"]["answer_evidence_ids"] = []
        answers["answer_evidence"] = []

        failures = validate_canonical_grounding_chain.collect_failures(
            legal,
            chunks,
            answers,
            gold,
        )

        joined = "\n".join(failures)
        self.assertIn("empty corpus answers must refuse", joined)

    def test_grounded_answer_without_access_basis_fails(self) -> None:
        legal = load_json(EXAMPLES / "documents" / "legal-document.example.json")
        chunks = load_json(EXAMPLES / "documents" / "chunk-set.example.json")
        answers = deepcopy(load_json(EXAMPLES / "documents" / "answer-trace.example.json"))
        gold = load_json(EXAMPLES / "gold-standard" / "gold-standard-asset.example.json")

        del answers["answer_event"]["access_basis"]

        failures = validate_canonical_grounding_chain.collect_failures(
            legal,
            chunks,
            answers,
            gold,
        )

        joined = "\n".join(failures)
        self.assertIn("must carry access_basis", joined)


if __name__ == "__main__":
    unittest.main()
