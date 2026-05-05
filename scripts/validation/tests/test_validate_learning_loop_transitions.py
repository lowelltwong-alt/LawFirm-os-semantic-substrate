from __future__ import annotations

import json
import unittest
from pathlib import Path

from scripts.validation.validate_learning_loop_transitions import (
    load_enum,
    load_yaml,
    validate_innovation_payloads,
    validate_transition_policy,
)


class ValidateTransitionPolicyTests(unittest.TestCase):
    def test_invalid_policy_fixture_reports_enum_failures(self) -> None:
        fixture = Path("scripts/validation/test_fixtures/invalid_learning_transition_policy.yaml")
        data = load_yaml(fixture)
        self.assertIsInstance(data, dict)

        failures: list[str] = []
        validate_transition_policy(
            fixture,
            data,
            failures,
            load_enum("action_type"),
            load_enum("confidence_level"),
            load_enum("evidence_sufficiency"),
            load_enum("allocation_decision_state"),
        )

        joined = "\n".join(failures)
        self.assertIn("not_a_real_action", joined)
        self.assertIn("very_high", joined)
        self.assertIn("mythic_source", joined)
        self.assertIn("invalid_state", joined)

    def load_active_innovation_payloads(self) -> tuple[dict[str, dict], dict[str, Path]]:
        repo_root = Path(__file__).resolve().parents[3]
        paths = {
            "exc": repo_root / "examples" / "exceptions" / "events" / "EXC-000101.json",
            "pv": repo_root / "examples" / "exceptions" / "pressure-vectors" / "PV-000101.json",
            "ap": repo_root / "examples" / "exceptions" / "adaptation-proposals" / "AP-000001.json",
            "pd": repo_root / "examples" / "exceptions" / "promotion-decisions" / "PD-000001.json",
            "opp": repo_root / "examples" / "innovation-os" / "opportunity-object.example.json",
            "spr": repo_root / "examples" / "innovation-os" / "sprint-object.example.json",
            "pil": repo_root / "examples" / "innovation-os" / "pilot-object.example.json",
            "gate": repo_root / "examples" / "innovation-os" / "validation-gate-record.example.json",
            "scale": repo_root / "examples" / "innovation-os" / "scale-package-object.example.json",
            "brief": repo_root / "examples" / "innovation-os" / "executive-brief-object.example.json",
        }
        payloads = {
            key: json.loads(path.read_text(encoding="utf-8")) for key, path in paths.items()
        }
        rel_paths = {key: path.relative_to(repo_root) for key, path in paths.items()}
        return payloads, rel_paths

    def test_opportunity_refs_must_include_linked_exception_and_pressure_vector(self) -> None:
        payloads, rel_paths = self.load_active_innovation_payloads()
        payloads["opp"]["source_refs"]["pressure_vector_ids"] = ["PV-999999"]
        payloads["opp"]["source_refs"]["exception_event_ids"] = ["EXC-999999"]

        failures: list[str] = []
        validate_innovation_payloads(payloads, rel_paths, failures)

        joined = "\n".join(failures)
        self.assertIn("source_refs.pressure_vector_ids' must include 'PV-000101'", joined)
        self.assertIn("source_refs.exception_event_ids' must include 'EXC-000101'", joined)

    def test_active_executive_brief_example_participates_in_validation(self) -> None:
        payloads, rel_paths = self.load_active_innovation_payloads()

        failures: list[str] = []
        validate_innovation_payloads(payloads, rel_paths, failures)

        self.assertEqual(failures, [])

    def test_sprint_refs_must_match_active_pressure_vector(self) -> None:
        payloads, rel_paths = self.load_active_innovation_payloads()
        payloads["spr"]["source_refs"]["pressure_vector_ids"] = ["PV-999999"]

        failures: list[str] = []
        validate_innovation_payloads(payloads, rel_paths, failures)

        joined = "\n".join(failures)
        self.assertIn(
            "source_refs.pressure_vector_ids' value 'PV-999999' must resolve to one of ['PV-000101']",
            joined,
        )

    def test_executive_brief_dangling_refs_fail(self) -> None:
        payloads, rel_paths = self.load_active_innovation_payloads()
        payloads["brief"]["evidence_refs"] = [
            "EXC-999999",
            "PV-999999",
            "OPP-000001",
            "SPR-999999",
        ]

        failures: list[str] = []
        validate_innovation_payloads(payloads, rel_paths, failures)

        joined = "\n".join(failures)
        self.assertIn(
            "evidence_refs' value 'EXC-999999' must resolve to one of ['EXC-000101', 'OPP-000001', 'PV-000101', 'SPR-000001']",
            joined,
        )
        self.assertIn(
            "evidence_refs' value 'SPR-999999' must resolve to one of ['EXC-000101', 'OPP-000001', 'PV-000101', 'SPR-000001']",
            joined,
        )

    def test_incomplete_chain_missing_adaptation_proposal_fails(self) -> None:
        payloads, rel_paths = self.load_active_innovation_payloads()
        fixture = Path("scripts/validation/test_fixtures/incomplete_governed_learning_chain.synthetic.json")
        data = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertTrue(data.get("synthetic_test_only"))
        payloads["exc"] = data["objects"]["examples/exceptions/events/EXC-900002.json"]
        payloads["pv"] = data["objects"]["examples/exceptions/pressure-vectors/PV-900002.json"]
        payloads["pd"] = data["objects"]["examples/exceptions/promotion-decisions/PD-900002.json"]
        rel_paths["exc"] = Path("scripts/validation/test_fixtures/incomplete_governed_learning_chain.synthetic.json")
        rel_paths["pv"] = Path("scripts/validation/test_fixtures/incomplete_governed_learning_chain.synthetic.json")
        rel_paths["pd"] = Path("scripts/validation/test_fixtures/incomplete_governed_learning_chain.synthetic.json")
        del payloads["ap"]
        rel_paths["ap"] = Path("scripts/validation/test_fixtures/incomplete_governed_learning_chain.synthetic.json")

        failures: list[str] = []
        validate_innovation_payloads(payloads, rel_paths, failures)

        joined = "\n".join(failures)
        self.assertIn("required Innovation OS example is missing", joined)
        self.assertIn("incomplete_governed_learning_chain.synthetic.json", joined)

    def test_promotion_decision_must_reference_active_adaptation_proposal(self) -> None:
        payloads, rel_paths = self.load_active_innovation_payloads()
        payloads["pd"]["proposal_id"] = "AP-999999"

        failures: list[str] = []
        validate_innovation_payloads(payloads, rel_paths, failures)

        joined = "\n".join(failures)
        self.assertIn("proposal_id must reference the active adaptation-proposal example", joined)


if __name__ == "__main__":
    unittest.main()
