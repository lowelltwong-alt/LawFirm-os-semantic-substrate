from __future__ import annotations

import unittest
from pathlib import Path
from unittest.mock import patch

from scripts.validation import validate_exception_events


def build_event(exception_id: str, pressure_vector_refs: list[str]) -> dict:
    return {
        "exception_id": exception_id,
        "schema_type": "exception-event",
        "schema_version": "v1",
        "event_class": "retrieval_miss",
        "severity": "moderate",
        "event_time": "2026-04-10T14:00:00Z",
        "summary": "Example retrieval miss.",
        "origin": {"layer": "retrieval", "component": "validator", "run_id": "run-1"},
        "route": {
            "route_id": "route.retrieval_miss.v1",
            "destination_loop": "retrieval_tuning",
        },
        "trust_metadata": {"trust_level": "high"},
        "canonical_mutation_control": {
            "allowed_action": "route_for_review",
            "direct_mutation_attempted": False,
        },
        "pressure_vector_refs": pressure_vector_refs,
    }


class ValidateExceptionEventsTests(unittest.TestCase):
    def test_nested_active_events_detect_duplicate_ids_and_dangling_pressure_vectors(
        self,
    ) -> None:
        nested_event = Path("examples/exceptions/events/EXC-000101.json")
        top_level_event = Path("examples/exceptions/retrieval_miss_example.json")
        pressure_vector = Path("examples/exceptions/pressure-vectors/PV-000101.json")
        payloads = {
            nested_event: build_event("EXC-000101", ["PV-000101"]),
            top_level_event: build_event("EXC-000101", ["PV-000501"]),
            pressure_vector: {
                "pressure_vector_id": "PV-000101",
                "schema_type": "pressure-vector",
                "schema_version": "v1",
            },
        }

        with (
            patch.object(
                validate_exception_events,
                "iter_active_exception_json",
                return_value=[top_level_event, nested_event, pressure_vector],
            ),
            patch.object(
                validate_exception_events,
                "load_json",
                side_effect=lambda path: payloads[path],
            ),
        ):
            failures = validate_exception_events.collect_failures(Path("dummy"))

        joined = "\n".join(failures)
        self.assertIn("duplicate active exception_id 'EXC-000101'", joined)
        self.assertIn(
            "pressure_vector_ref 'PV-000501' does not resolve to an active pressure-vector example",
            joined,
        )


if __name__ == "__main__":
    unittest.main()
