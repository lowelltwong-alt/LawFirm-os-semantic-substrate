from __future__ import annotations

from copy import deepcopy
import unittest
from pathlib import Path

from scripts.validation import validate_grounded_answer_evaluation_harness


ROOT = Path(__file__).resolve().parents[3]
EXAMPLES = ROOT / "examples"


def load_json(path: Path):
    return validate_grounded_answer_evaluation_harness.load_json(path)


class ValidateGroundedAnswerEvaluationHarnessTests(unittest.TestCase):
    def test_existing_synthetic_evaluation_run_passes(self) -> None:
        failures = validate_grounded_answer_evaluation_harness.collect_failures(
            load_json(EXAMPLES / "evaluation" / "grounded-answer-evaluation-run.example.json"),
            load_json(EXAMPLES / "documents" / "legal-document.example.json"),
            load_json(EXAMPLES / "documents" / "answer-trace.example.json"),
            load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"),
        )

        self.assertEqual(failures, [])

    def test_missing_expected_source_ref_fails(self) -> None:
        eval_run = deepcopy(load_json(EXAMPLES / "evaluation" / "grounded-answer-evaluation-run.example.json"))
        eval_run["items"][0]["expected_source_refs"] = ["SRC-missing-000001"]

        failures = validate_grounded_answer_evaluation_harness.collect_failures(
            eval_run,
            load_json(EXAMPLES / "documents" / "legal-document.example.json"),
            load_json(EXAMPLES / "documents" / "answer-trace.example.json"),
            load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"),
        )

        joined = "\n".join(failures)
        self.assertIn("expected_source_ref 'SRC-missing-000001' does not resolve", joined)

    def test_refusal_required_item_may_not_present_grounded_answer(self) -> None:
        eval_run = deepcopy(load_json(EXAMPLES / "evaluation" / "grounded-answer-evaluation-run.example.json"))
        refusal_item = eval_run["items"][1]
        refusal_item["allowed_answer_type"] = "grounded_answer"
        refusal_item["candidate_response"]["response_type"] = "grounded_answer"

        failures = validate_grounded_answer_evaluation_harness.collect_failures(
            eval_run,
            load_json(EXAMPLES / "documents" / "legal-document.example.json"),
            load_json(EXAMPLES / "documents" / "answer-trace.example.json"),
            load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"),
        )

        joined = "\n".join(failures)
        self.assertIn("refusal-required evaluation item must use refusal response_type", joined)
        self.assertIn("may not present a grounded answer", joined)

    def test_support_unavailable_item_may_not_present_grounded_answer(self) -> None:
        eval_run = deepcopy(load_json(EXAMPLES / "evaluation" / "grounded-answer-evaluation-run.example.json"))
        unavailable_item = eval_run["items"][2]
        unavailable_item["allowed_answer_type"] = "grounded_answer"
        unavailable_item["candidate_response"]["response_type"] = "grounded_answer"

        failures = validate_grounded_answer_evaluation_harness.collect_failures(
            eval_run,
            load_json(EXAMPLES / "documents" / "legal-document.example.json"),
            load_json(EXAMPLES / "documents" / "answer-trace.example.json"),
            load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"),
        )

        joined = "\n".join(failures)
        self.assertIn("support-unavailable evaluation item must use support_unavailable response_type", joined)
        self.assertIn("may not present a grounded answer", joined)

    def test_production_metric_claim_is_disallowed(self) -> None:
        eval_run = deepcopy(load_json(EXAMPLES / "evaluation" / "grounded-answer-evaluation-run.example.json"))
        eval_run["measurement_boundary"]["production_performance_not_claimed"] = False

        failures = validate_grounded_answer_evaluation_harness.collect_failures(
            eval_run,
            load_json(EXAMPLES / "documents" / "legal-document.example.json"),
            load_json(EXAMPLES / "documents" / "answer-trace.example.json"),
            load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json"),
        )

        joined = "\n".join(failures)
        self.assertIn("schema: measurement_boundary.production_performance_not_claimed: True was expected", joined)


if __name__ == "__main__":
    unittest.main()
