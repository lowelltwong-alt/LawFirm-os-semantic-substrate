from __future__ import annotations

import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.validation.jsonschema_registry_support import build_local_schema_registry


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def collect_failures(eval_run: dict, legal: dict, answers: dict, manifest: dict) -> list[str]:
    failures: list[str] = []

    schema = load_json(ROOT / "schemas" / "evaluation-run.schema.json")
    validator = Draft202012Validator(schema, registry=build_local_schema_registry(ROOT))
    for error in sorted(validator.iter_errors(eval_run), key=lambda e: list(e.path)):
        location = ".".join(str(part) for part in error.path) or "<root>"
        failures.append(f"schema: {location}: {error.message}")
    if failures:
        return failures

    access_decision = answers["access_decision"]
    retrieval_response = answers["retrieval_response"]
    answer_event = answers["answer_event"]
    answer_evidence = {
        item["answer_evidence_id"]: item
        for item in answers["answer_evidence"]
    }

    resolvable_source_refs = {
        legal["address_struct"]["object_id"],
    }
    resolvable_evidence_refs = set(answer_evidence)
    resolvable_retrieval_response_refs = {retrieval_response["retrieval_response_id"]}
    resolvable_answer_event_refs = {answer_event["answer_event_id"]}
    resolvable_access_decision_refs = {access_decision["access_decision_id"]}
    policy_refs = {
        ref
        for ref in {
            legal["document"].get("access_policy_ref"),
            manifest.get("access_policy_ref"),
            *(access_decision["policy_basis"].get("source_policy_refs", [])),
            *(answer_event.get("access_basis", {}).get("source_policy_refs", [])),
        }
        if isinstance(ref, str)
    }

    for item in eval_run["items"]:
        label = item["evaluation_item_id"]
        response = item["candidate_response"]
        expected_behavior = item["expected_behavior"]
        response_type = response["response_type"]

        require(
            item["synthetic_status"] == "synthetic_test_only",
            f"{label}: item must remain synthetic_test_only",
            failures,
        )
        require(
            response["synthetic_status"] == "synthetic_test_only",
            f"{label}: candidate_response must remain synthetic_test_only",
            failures,
        )
        require(
            response_type == item["allowed_answer_type"],
            f"{label}: candidate_response.response_type must match allowed_answer_type",
            failures,
        )

        if expected_behavior == "grounded_answer_allowed":
            require(
                response_type == "grounded_answer",
                f"{label}: grounded-answer evaluation item must use grounded_answer response_type",
                failures,
            )

            for source_ref in item.get("expected_source_refs", []):
                require(
                    source_ref in resolvable_source_refs,
                    f"{label}: expected_source_ref '{source_ref}' does not resolve in the synthetic governed-source bundle",
                    failures,
                )
            require(
                bool(item.get("expected_source_refs")),
                f"{label}: grounded-answer evaluation item requires expected_source_refs",
                failures,
            )

            for evidence_ref in item.get("expected_evidence_refs", []):
                require(
                    evidence_ref in resolvable_evidence_refs,
                    f"{label}: expected_evidence_ref '{evidence_ref}' does not resolve in the synthetic answer-evidence bundle",
                    failures,
                )
            require(
                bool(item.get("expected_evidence_refs")),
                f"{label}: grounded-answer evaluation item requires expected_evidence_refs",
                failures,
            )

            for retrieval_ref in item.get("expected_retrieval_response_refs", []):
                require(
                    retrieval_ref in resolvable_retrieval_response_refs,
                    f"{label}: expected_retrieval_response_ref '{retrieval_ref}' does not resolve",
                    failures,
                )
            require(
                bool(item.get("expected_retrieval_response_refs")),
                f"{label}: grounded-answer evaluation item requires expected_retrieval_response_refs",
                failures,
            )

            for answer_ref in item.get("expected_answer_event_refs", []):
                require(
                    answer_ref in resolvable_answer_event_refs,
                    f"{label}: expected_answer_event_ref '{answer_ref}' does not resolve",
                    failures,
                )
            require(
                bool(item.get("expected_answer_event_refs")),
                f"{label}: grounded-answer evaluation item requires expected_answer_event_refs",
                failures,
            )

            expected_access_decisions = item.get("expected_access_decision_refs", [])
            for access_ref in expected_access_decisions:
                require(
                    access_ref in resolvable_access_decision_refs,
                    f"{label}: expected_access_decision_ref '{access_ref}' does not resolve",
                    failures,
                )
            require(
                bool(expected_access_decisions),
                f"{label}: grounded-answer evaluation item requires expected_access_decision_refs",
                failures,
            )
            require(
                access_decision["decision"] == "allow",
                f"{label}: grounded-answer evaluation item requires an allow access decision",
                failures,
            )

            required_policy_refs = set(item.get("required_source_policy_refs", []))
            require(
                bool(required_policy_refs),
                f"{label}: grounded-answer evaluation item requires required_source_policy_refs",
                failures,
            )
            missing_policy_refs = sorted(required_policy_refs - policy_refs)
            for policy_ref in missing_policy_refs:
                failures.append(
                    f"{label}: required_source_policy_ref '{policy_ref}' is not satisfied by the synthetic support bundle"
                )

            access_basis = answer_event.get("access_basis", {})
            require(
                access_basis.get("access_decision_id") == access_decision["access_decision_id"],
                f"{label}: answer_event access_basis must point to the expected access decision",
                failures,
            )
            answer_event_policy_refs = set(access_basis.get("source_policy_refs", []))
            missing_answer_event_policy_refs = sorted(required_policy_refs - answer_event_policy_refs)
            for policy_ref in missing_answer_event_policy_refs:
                failures.append(
                    f"{label}: answer_event access_basis is missing required source policy ref '{policy_ref}'"
                )

        elif expected_behavior == "refusal_required":
            require(
                response_type == "refusal",
                f"{label}: refusal-required evaluation item must use refusal response_type",
                failures,
            )
            for field_name in (
                "expected_source_refs",
                "expected_evidence_refs",
                "expected_retrieval_response_refs",
                "expected_answer_event_refs",
                "expected_access_decision_refs",
            ):
                require(
                    not item.get(field_name),
                    f"{label}: refusal-required evaluation item may not declare grounded support in {field_name}",
                    failures,
                )

        elif expected_behavior == "support_unavailable":
            require(
                response_type == "support_unavailable",
                f"{label}: support-unavailable evaluation item must use support_unavailable response_type",
                failures,
            )
            support_constraint = item.get("support_constraint")
            require(
                isinstance(support_constraint, dict),
                f"{label}: support-unavailable evaluation item requires support_constraint",
                failures,
            )

        if expected_behavior != "grounded_answer_allowed" and response_type == "grounded_answer":
            failures.append(
                f"{label}: refusal or unavailable-support evaluation item may not present a grounded answer"
            )

    return failures


def main() -> int:
    eval_run = load_json(EXAMPLES / "evaluation" / "grounded-answer-evaluation-run.example.json")
    legal = load_json(EXAMPLES / "documents" / "legal-document.example.json")
    answers = load_json(EXAMPLES / "documents" / "answer-trace.example.json")
    manifest = load_json(EXAMPLES / "documents" / "source-ingestion-manifest.example.json")

    failures = collect_failures(eval_run, legal, answers, manifest)
    if failures:
        print("GROUNDED ANSWER EVALUATION HARNESS FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Grounded answer evaluation harness validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
