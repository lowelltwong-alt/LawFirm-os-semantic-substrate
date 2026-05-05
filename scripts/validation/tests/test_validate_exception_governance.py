from __future__ import annotations

import json
import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validation import validate_exception_governance

FIXTURES = Path("scripts/validation/test_fixtures")
ROUTE_REGISTRY = {
    "routes": [
        {
            "route_id": "route.retrieval_miss.v1",
            "event_class": "retrieval_miss",
            "prohibited_direct_actions": [
                "canonical_ontology_write",
                "taxonomy_rewrite",
                "schema_mutation",
                "policy_overwrite",
                "address_system_mutation",
            ],
        }
    ]
}


def load_fixture_payloads(name: str) -> dict[Path, dict]:
    fixture = json.loads((FIXTURES / name).read_text(encoding="utf-8"))
    assert fixture["synthetic_test_only"] is True
    return {Path(path): payload for path, payload in fixture["objects"].items()}


class ValidateExceptionGovernanceTests(unittest.TestCase):
    def test_nested_active_refs_must_resolve(self) -> None:
        route_registry = ROUTE_REGISTRY
        event = Path("examples/exceptions/events/EXC-000101.json")
        pressure_vector = Path("examples/exceptions/pressure-vectors/PV-000101.json")
        proposal = Path("examples/exceptions/adaptation-proposals/AP-000001.json")
        decision = Path("examples/exceptions/promotion-decisions/PD-000001.json")
        payloads = {
            event: {
                "exception_id": "EXC-000101",
                "schema_type": "exception-event",
                "schema_version": "v1",
                "route": {"route_id": "route.retrieval_miss.v1"},
                "trust_metadata": {"trust_level": "high"},
                "event_class": "retrieval_miss",
                "canonical_mutation_control": {
                    "allowed_action": "route_for_review",
                    "direct_mutation_attempted": False,
                },
            },
            pressure_vector: {
                "pressure_vector_id": "PV-000101",
                "schema_type": "pressure-vector",
                "schema_version": "v1",
                "derived_from_exception_ids": ["EXC-999999"],
            },
            proposal: {
                "proposal_id": "AP-000001",
                "schema_type": "adaptation-proposal",
                "schema_version": "v1",
                "source_exception_ids": ["EXC-000101"],
                "source_pressure_vector_ids": ["PV-999999"],
            },
            decision: {
                "decision_id": "PD-000001",
                "schema_type": "promotion-decision",
                "schema_version": "v1",
                "proposal_id": "AP-999999",
                "input_artifacts": {
                    "exception_event_ids": ["EXC-000101"],
                    "pressure_vector_ids": ["PV-999999"],
                },
            },
        }

        with (
            patch.object(
                validate_exception_governance,
                "iter_active_exception_json",
                return_value=[event, pressure_vector, proposal, decision],
            ),
            patch.object(
                validate_exception_governance,
                "load_json",
                side_effect=lambda path: route_registry if path == Path("registry.json") else payloads[path],
            ),
        ):
            failures = validate_exception_governance.collect_failures(
                Path("dummy"), Path("registry.json")
            )

        joined = "\n".join(failures)
        self.assertIn(
            "derived_from_exception_id 'EXC-999999' does not resolve to an active exception-event example",
            joined,
        )
        self.assertIn(
            "source_pressure_vector_id 'PV-999999' does not resolve to an active pressure-vector example",
            joined,
        )
        self.assertIn(
            "proposal_id 'AP-999999' does not resolve to an active adaptation-proposal example",
            joined,
        )
        self.assertIn(
            "input_artifacts.pressure_vector_id 'PV-999999' does not resolve to an active pressure-vector example",
            joined,
        )

    def test_synthetic_direct_mutation_fixture_fails(self) -> None:
        payloads = load_fixture_payloads("invalid_exception_direct_mutation.synthetic.json")
        paths = list(payloads.keys())

        with (
            patch.object(
                validate_exception_governance,
                "iter_active_exception_json",
                return_value=paths,
            ),
            patch.object(
                validate_exception_governance,
                "load_json",
                side_effect=lambda path: ROUTE_REGISTRY if path == Path("registry.json") else payloads[path],
            ),
        ):
            failures = validate_exception_governance.collect_failures(
                Path("dummy"), Path("registry.json")
            )

        joined = "\n".join(failures)
        self.assertIn("appears to request direct canonical mutation", joined)
        self.assertIn("registry/schema-registry.json", joined)

    def test_incomplete_chain_fixture_is_not_promotion_eligible(self) -> None:
        payloads = load_fixture_payloads("incomplete_governed_learning_chain.synthetic.json")
        paths = list(payloads.keys())

        with (
            patch.object(
                validate_exception_governance,
                "iter_active_exception_json",
                return_value=paths,
            ),
            patch.object(
                validate_exception_governance,
                "load_json",
                side_effect=lambda path: ROUTE_REGISTRY if path == Path("registry.json") else payloads[path],
            ),
        ):
            failures = validate_exception_governance.collect_failures(
                Path("dummy"), Path("registry.json")
            )

        joined = "\n".join(failures)
        self.assertIn("not promotion-eligible", joined)
        self.assertIn("proposal_id 'AP-900002' does not resolve", joined)


if __name__ == "__main__":
    unittest.main()
