#!/usr/bin/env python3
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = REPO_ROOT / "examples" / "exceptions"
ACTIVE_SKIP_DIRS = {"legacy", "archive", "__pycache__"}

ALLOWED_CLASSES = {"retrieval_miss", "workflow_escalation", "authority_conflict_override"}
ALLOWED_SEVERITY = {"low", "moderate", "high", "critical"}
ALLOWED_LOOPS = {"retrieval_tuning", "workflow_redesign", "governance_review", "cross_loop_review"}
ALLOWED_TRUST = {"low", "moderate", "high"}
ALLOWED_ACTIONS = {"route_for_review", "aggregate_pressure", "attach_evidence_only"}

REQUIRED_TOP = {
    "exception_id",
    "schema_type",
    "schema_version",
    "event_class",
    "severity",
    "event_time",
    "summary",
    "origin",
    "route",
    "trust_metadata",
    "canonical_mutation_control",
}


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def iter_active_exception_json(exceptions_dir: Path):
    for root, dirs, files in os.walk(str(exceptions_dir)):
        dirs[:] = [d for d in dirs if d not in ACTIVE_SKIP_DIRS]
        for name in files:
            if name.endswith(".json"):
                yield Path(root) / name


def collect_failures(exceptions_dir: Path = EXAMPLES_DIR):
    failures = []
    events: list[tuple[Path, dict]] = []
    pressure_vector_ids = set()

    for path in sorted(iter_active_exception_json(exceptions_dir)):
        payload = load_json(path)
        if payload.get("schema_type") == "pressure-vector" and isinstance(
            payload.get("pressure_vector_id"), str
        ):
            pressure_vector_ids.add(payload["pressure_vector_id"])
        if payload.get("schema_type") == "exception-event":
            events.append((path, payload))

    event_inventory = {}
    for path, event in events:
        exception_id = event.get("exception_id")
        if isinstance(exception_id, str):
            if exception_id in event_inventory:
                failures.append(
                    f"{path}: duplicate active exception_id '{exception_id}' also found in {event_inventory[exception_id]}"
                )
            else:
                event_inventory[exception_id] = path

    for path, event in events:
        missing = REQUIRED_TOP - set(event.keys())
        if missing:
            failures.append(f"{path}: missing fields {sorted(missing)}")
            continue

        if event["schema_type"] != "exception-event" or event["schema_version"] != "v1":
            failures.append(f"{path}: schema_type/schema_version must be exception-event/v1")

        if event["event_class"] not in ALLOWED_CLASSES:
            failures.append(f"{path}: invalid event_class {event['event_class']}")

        if event["severity"] not in ALLOWED_SEVERITY:
            failures.append(f"{path}: invalid severity {event['severity']}")

        route = event.get("route", {})
        if route.get("destination_loop") not in ALLOWED_LOOPS:
            failures.append(f"{path}: invalid route.destination_loop {route.get('destination_loop')}")

        trust = event.get("trust_metadata", {})
        if trust.get("trust_level") not in ALLOWED_TRUST:
            failures.append(f"{path}: invalid trust_metadata.trust_level {trust.get('trust_level')}")

        mutation = event.get("canonical_mutation_control", {})
        if mutation.get("allowed_action") not in ALLOWED_ACTIONS:
            failures.append(f"{path}: invalid canonical_mutation_control.allowed_action {mutation.get('allowed_action')}")

        if mutation.get("direct_mutation_attempted") is not False:
            failures.append(f"{path}: direct_mutation_attempted must be false")

        for pressure_vector_ref in event.get("pressure_vector_refs", []):
            if pressure_vector_ref not in pressure_vector_ids:
                failures.append(
                    f"{path}: pressure_vector_ref '{pressure_vector_ref}' does not resolve to an active pressure-vector example"
                )

        if not failures or not any(str(path) in f for f in failures):
            print(f"VALID structure: {path}")

    return failures


def main() -> int:
    failures = collect_failures()

    if failures:
        print("\nException event validation failures:")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("All exception examples passed structural validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
