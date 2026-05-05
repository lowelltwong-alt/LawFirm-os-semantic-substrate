#!/usr/bin/env python3
import json
import os
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
EXAMPLES_DIR = REPO_ROOT / "examples" / "exceptions"
ROUTE_REGISTRY_PATH = REPO_ROOT / "registry" / "exception-route-registry.json"
ACTIVE_SKIP_DIRS = {"legacy", "archive", "__pycache__"}


PROHIBITED_CANONICAL_ACTIONS = {
    "canonical_ontology_write",
    "taxonomy_rewrite",
    "schema_mutation",
    "policy_overwrite",
    "address_system_mutation",
}

CANONICAL_TARGET_HINTS = (
    "ontology",
    "taxonomy",
    "schema",
    "registry/",
    "registry\\",
    "source-of-truth",
    "design-authority",
    "governance/",
    "governance\\",
    "policy",
)


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def build_route_index():
    route_registry = load_json(ROUTE_REGISTRY_PATH)
    return {route["route_id"]: route for route in route_registry.get("routes", [])}


def iter_active_exception_json(exceptions_dir: Path):
    for root, dirs, files in os.walk(str(exceptions_dir)):
        dirs[:] = [d for d in dirs if d not in ACTIVE_SKIP_DIRS]
        for name in files:
            if name.endswith(".json"):
                yield Path(root) / name


def looks_like_direct_canonical_mutation_target(target_hint: str) -> bool:
    lowered = target_hint.lower()
    return any(token in lowered for token in CANONICAL_TARGET_HINTS)


def collect_failures(
    exceptions_dir: Path = EXAMPLES_DIR, route_registry_path: Path = ROUTE_REGISTRY_PATH
):
    route_registry = (
        load_json(route_registry_path)
        if route_registry_path != ROUTE_REGISTRY_PATH
        else load_json(ROUTE_REGISTRY_PATH)
    )
    route_index = {route["route_id"]: route for route in route_registry.get("routes", [])}
    failures = []
    events: list[tuple[Path, dict]] = []
    pressure_vectors: list[tuple[Path, dict]] = []
    proposals: list[tuple[Path, dict]] = []
    decisions: list[tuple[Path, dict]] = []

    for path in sorted(iter_active_exception_json(exceptions_dir)):
        payload = load_json(path)
        schema_type = payload.get("schema_type")
        if schema_type == "exception-event":
            events.append((path, payload))
        elif schema_type == "pressure-vector":
            pressure_vectors.append((path, payload))
        elif schema_type == "adaptation-proposal":
            proposals.append((path, payload))
        elif schema_type == "promotion-decision":
            decisions.append((path, payload))

    event_ids = {
        event["exception_id"]
        for _, event in events
        if isinstance(event.get("exception_id"), str)
    }
    pressure_vector_ids = {
        payload["pressure_vector_id"]
        for _, payload in pressure_vectors
        if isinstance(payload.get("pressure_vector_id"), str)
    }
    proposal_ids = {
        payload["proposal_id"]
        for _, payload in proposals
        if isinstance(payload.get("proposal_id"), str)
    }
    proposal_index = {
        payload["proposal_id"]: payload
        for _, payload in proposals
        if isinstance(payload.get("proposal_id"), str)
    }
    pressure_vector_index = {
        payload["pressure_vector_id"]: payload
        for _, payload in pressure_vectors
        if isinstance(payload.get("pressure_vector_id"), str)
    }

    for path, event in events:

        # Rule 1: every exception has route + trust metadata.
        if "route" not in event:
            failures.append(f"{path}: missing route")
            continue
        if "trust_metadata" not in event:
            failures.append(f"{path}: missing trust_metadata")
            continue

        route_id = event["route"].get("route_id")
        if not route_id:
            failures.append(f"{path}: route.route_id missing")
            continue

        if route_id not in route_index:
            failures.append(f"{path}: route_id '{route_id}' is not in registry")
            continue

        reg = route_index[route_id]
        if event.get("event_class") != reg.get("event_class"):
            failures.append(
                f"{path}: event_class '{event.get('event_class')}' does not match registry '{reg.get('event_class')}'"
            )

        # Rule 2: no direct mutation of canonical ontology from raw exception events.
        mutation_control = event.get("canonical_mutation_control", {})
        if mutation_control.get("direct_mutation_attempted") is not False:
            failures.append(f"{path}: direct_mutation_attempted must be false")

        prohibited_from_route = set(reg.get("prohibited_direct_actions", []))
        target_hint = str(mutation_control.get("proposed_target", "")).lower()

        if looks_like_direct_canonical_mutation_target(target_hint):
            failures.append(
                f"{path}: proposed_target '{mutation_control.get('proposed_target')}' appears to request direct canonical mutation"
            )

        if prohibited_from_route & PROHIBITED_CANONICAL_ACTIONS and mutation_control.get("allowed_action") not in {
            "route_for_review",
            "aggregate_pressure",
            "attach_evidence_only",
        }:
            failures.append(
                f"{path}: allowed_action '{mutation_control.get('allowed_action')}' violates no-direct-mutation policy"
            )

    for path, pressure_vector in pressure_vectors:
        for exception_id in pressure_vector.get("derived_from_exception_ids", []):
            if exception_id not in event_ids:
                failures.append(
                    f"{path}: derived_from_exception_id '{exception_id}' does not resolve to an active exception-event example"
                )

    for path, proposal in proposals:
        for exception_id in proposal.get("source_exception_ids", []):
            if exception_id not in event_ids:
                failures.append(
                    f"{path}: source_exception_id '{exception_id}' does not resolve to an active exception-event example"
                )
        for pressure_vector_id in proposal.get("source_pressure_vector_ids", []):
            if pressure_vector_id not in pressure_vector_ids:
                failures.append(
                    f"{path}: source_pressure_vector_id '{pressure_vector_id}' does not resolve to an active pressure-vector example"
                )
                continue
            pressure_vector = pressure_vector_index[pressure_vector_id]
            derived_from_exception_ids = set(
                pressure_vector.get("derived_from_exception_ids", [])
            )
            missing_linked_exception_ids = sorted(
                set(proposal.get("source_exception_ids", [])) - derived_from_exception_ids
            )
            for exception_id in missing_linked_exception_ids:
                failures.append(
                    f"{path}: source_pressure_vector_id '{pressure_vector_id}' is not derived from linked source_exception_id '{exception_id}'"
                )

    for path, decision in decisions:
        proposal_id = decision.get("proposal_id")
        proposal = proposal_index.get(proposal_id) if isinstance(proposal_id, str) else None
        if proposal_id and proposal_id not in proposal_ids:
            failures.append(
                f"{path}: promotion-decision is not promotion-eligible because proposal_id '{proposal_id}' does not resolve to an active adaptation-proposal example"
            )
        input_artifacts = decision.get("input_artifacts", {})
        input_exception_ids = input_artifacts.get("exception_event_ids", [])
        input_pressure_vector_ids = input_artifacts.get("pressure_vector_ids", [])
        if not isinstance(input_exception_ids, list) or not input_exception_ids:
            failures.append(
                f"{path}: promotion-decision is not promotion-eligible because input_artifacts.exception_event_ids must be a non-empty list"
            )
        if not isinstance(input_pressure_vector_ids, list) or not input_pressure_vector_ids:
            failures.append(
                f"{path}: promotion-decision is not promotion-eligible because input_artifacts.pressure_vector_ids must be a non-empty list"
            )
        for exception_id in input_artifacts.get("exception_event_ids", []):
            if exception_id not in event_ids:
                failures.append(
                    f"{path}: input_artifacts.exception_event_id '{exception_id}' does not resolve to an active exception-event example"
                )
        for pressure_vector_id in input_artifacts.get("pressure_vector_ids", []):
            if pressure_vector_id not in pressure_vector_ids:
                failures.append(
                    f"{path}: input_artifacts.pressure_vector_id '{pressure_vector_id}' does not resolve to an active pressure-vector example"
                )
        if proposal:
            proposal_exception_ids = set(proposal.get("source_exception_ids", []))
            proposal_pressure_vector_ids = set(
                proposal.get("source_pressure_vector_ids", [])
            )
            missing_exception_ids = sorted(set(input_exception_ids) - proposal_exception_ids)
            for exception_id in missing_exception_ids:
                failures.append(
                    f"{path}: promotion-decision is not promotion-eligible because proposal '{proposal_id}' does not reference exception_event_id '{exception_id}'"
                )
            missing_pressure_vector_ids = sorted(
                set(input_pressure_vector_ids) - proposal_pressure_vector_ids
            )
            for pressure_vector_id in missing_pressure_vector_ids:
                failures.append(
                    f"{path}: promotion-decision is not promotion-eligible because proposal '{proposal_id}' does not reference pressure_vector_id '{pressure_vector_id}'"
                )

    return failures


def main() -> int:
    failures = collect_failures()

    if failures:
        print("Governance validation failures:")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print("All exception examples passed governance validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
