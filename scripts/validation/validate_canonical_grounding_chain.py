from __future__ import annotations

import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
EXAMPLES = ROOT / "examples"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def require(condition: bool, message: str, failures: list[str]) -> None:
    if not condition:
        failures.append(message)


def collect_failures(
    legal: dict,
    chunks: dict,
    answers: dict,
    gold: dict,
) -> list[str]:
    failures: list[str] = []

    document = legal["document"]
    source_artifact = legal["source_artifact"]
    document_version = legal["document_version"]
    canonical_text = legal["canonical_text"]
    components = {item["component_id"]: item for item in legal["components"]}
    span_selectors = {item["span_selector_id"]: item for item in legal["span_selectors"]}
    citation_targets = {item["citation_target_id"]: item for item in legal["citation_targets"]}
    citation_mentions = {item["citation_mention_id"]: item for item in legal["citation_mentions"]}

    chunk_set = chunks["chunk_set"]
    chunk_items = {item["chunk_id"]: item for item in chunks["chunks"]}
    embedding_set = chunks["embedding_set"]
    index_build = chunks["index_build"]
    migration_plan = chunks["index_migration_plan"]

    retrieval_request = answers["retrieval_request"]
    access_decision = answers["access_decision"]
    retrieval_trace = answers["retrieval_trace"]
    retrieval_response = answers["retrieval_response"]
    answer_event = answers["answer_event"]
    answer_evidence = {item["answer_evidence_id"]: item for item in answers["answer_evidence"]}
    gold_asset = gold["gold_standard_asset"]

    require(document["current_version_id"] == document_version["document_version_id"], "document.current_version_id must match document_version.document_version_id", failures)
    require(source_artifact["document_id"] == document["document_id"], "source_artifact.document_id must match document.document_id", failures)
    require(document_version["document_id"] == document["document_id"], "document_version.document_id must match document.document_id", failures)
    require(document_version["source_artifact_id"] == source_artifact["source_artifact_id"], "document_version.source_artifact_id must match source_artifact.source_artifact_id", failures)
    require(document_version["canonical_text_id"] == canonical_text["canonical_text_id"], "document_version.canonical_text_id must match canonical_text.canonical_text_id", failures)
    require(canonical_text["document_version_id"] == document_version["document_version_id"], "canonical_text.document_version_id must match document_version.document_version_id", failures)

    for component_id, component in components.items():
        require(component["document_version_id"] == document_version["document_version_id"], f"component {component_id} must reference the legal document version", failures)
        require(component["canonical_text_id"] == canonical_text["canonical_text_id"], f"component {component_id} must reference the legal canonical text", failures)
        for span_id in component["span_selector_ids"]:
            require(span_id in span_selectors, f"component {component_id} references missing span selector {span_id}", failures)
            if span_id in span_selectors:
                require(span_selectors[span_id].get("component_id") == component_id, f"span selector {span_id} must point back to component {component_id}", failures)
        for child_id in component.get("child_component_ids", []):
            require(child_id in components, f"component {component_id} references missing child component {child_id}", failures)
        parent_id = component.get("parent_component_id")
        if parent_id:
            require(parent_id in components, f"component {component_id} references missing parent component {parent_id}", failures)
        for mention_id in component.get("citation_mention_ids", []):
            require(mention_id in citation_mentions, f"component {component_id} references missing citation mention {mention_id}", failures)

    for span_id, selector in span_selectors.items():
        require(selector["document_version_id"] == document_version["document_version_id"], f"span selector {span_id} must reference the legal document version", failures)
        require(selector["canonical_text_id"] == canonical_text["canonical_text_id"], f"span selector {span_id} must reference the legal canonical text", failures)
        component_id = selector.get("component_id")
        if component_id:
            require(component_id in components, f"span selector {span_id} references missing component {component_id}", failures)

    for mention_id, mention in citation_mentions.items():
        require(mention["document_version_id"] == document_version["document_version_id"], f"citation mention {mention_id} must reference the legal document version", failures)
        require(mention["component_id"] in components, f"citation mention {mention_id} references missing component {mention['component_id']}", failures)
        require(mention["citation_target_id"] in citation_targets, f"citation mention {mention_id} references missing citation target {mention['citation_target_id']}", failures)
        for span_id in mention["span_selector_ids"]:
            require(span_id in span_selectors, f"citation mention {mention_id} references missing span selector {span_id}", failures)

    require(chunk_set["document_version_id"] == document_version["document_version_id"], "chunk_set.document_version_id must match the canonical document version", failures)
    require(chunk_set["canonical_text_id"] == canonical_text["canonical_text_id"], "chunk_set.canonical_text_id must match the canonical text", failures)
    for chunk_id in chunk_set["chunk_ids"]:
        require(chunk_id in chunk_items, f"chunk_set references missing chunk {chunk_id}", failures)
    for chunk_id, chunk in chunk_items.items():
        require(chunk["chunk_set_id"] == chunk_set["chunk_set_id"], f"chunk {chunk_id} must reference the example chunk set", failures)
        require(chunk["document_version_id"] == document_version["document_version_id"], f"chunk {chunk_id} must reference the canonical document version", failures)
        require(chunk["canonical_text_id"] == canonical_text["canonical_text_id"], f"chunk {chunk_id} must reference the canonical text", failures)
        for component_id in chunk["component_ids"]:
            require(component_id in components, f"chunk {chunk_id} references missing component {component_id}", failures)
        for span_id in chunk["span_selector_ids"]:
            require(span_id in span_selectors, f"chunk {chunk_id} references missing span selector {span_id}", failures)
            if span_id in span_selectors:
                require(span_selectors[span_id].get("component_id") in chunk["component_ids"], f"chunk {chunk_id} span selector {span_id} must resolve to one of the chunk components", failures)

    require(embedding_set["source_chunk_set_id"] == chunk_set["chunk_set_id"], "embedding_set.source_chunk_set_id must match chunk_set.chunk_set_id", failures)
    require(index_build["source_chunk_set_id"] == chunk_set["chunk_set_id"], "index_build.source_chunk_set_id must match chunk_set.chunk_set_id", failures)
    require(index_build["source_embedding_set_id"] == embedding_set["embedding_set_id"], "index_build.source_embedding_set_id must match embedding_set.embedding_set_id", failures)
    require(migration_plan["source_index_build_id"] == index_build["index_build_id"], "index_migration_plan.source_index_build_id must match index_build.index_build_id", failures)
    require(migration_plan["input_refs"]["source_chunk_set_id"] == chunk_set["chunk_set_id"], "index_migration_plan.input_refs.source_chunk_set_id must match chunk_set.chunk_set_id", failures)
    require(migration_plan["input_refs"]["source_embedding_set_id"] == embedding_set["embedding_set_id"], "index_migration_plan.input_refs.source_embedding_set_id must match embedding_set.embedding_set_id", failures)

    require(access_decision["target_ref"]["target_id"] == retrieval_request["retrieval_request_id"], "access_decision.target_ref.target_id must match retrieval_request.retrieval_request_id", failures)
    require(retrieval_trace["retrieval_request_id"] == retrieval_request["retrieval_request_id"], "retrieval_trace.retrieval_request_id must match retrieval_request.retrieval_request_id", failures)
    require(retrieval_trace["policy_enforcement"]["access_decision_id"] == access_decision["access_decision_id"], "retrieval_trace.policy_enforcement.access_decision_id must match access_decision.access_decision_id", failures)
    require(retrieval_response["retrieval_request_id"] == retrieval_request["retrieval_request_id"], "retrieval_response.retrieval_request_id must match retrieval_request.retrieval_request_id", failures)
    require(retrieval_response["retrieval_trace_id"] == retrieval_trace["retrieval_trace_id"], "retrieval_response.retrieval_trace_id must match retrieval_trace.retrieval_trace_id", failures)
    require(retrieval_response["access_decision_id"] == access_decision["access_decision_id"], "retrieval_response.access_decision_id must match access_decision.access_decision_id", failures)
    require(retrieval_response["index_build_id"] == index_build["index_build_id"], "retrieval_response.index_build_id must match index_build.index_build_id", failures)

    trace_chunk_ids = {item["chunk_id"] for item in retrieval_trace["result_trace"]}
    response_chunk_ids = set()
    for result in retrieval_response["ranked_results"]:
        response_chunk_ids.add(result["chunk_id"])
        require(result["chunk_id"] in chunk_items, f"retrieval_response ranked result references missing chunk {result['chunk_id']}", failures)
        require(result["document_version_id"] == document_version["document_version_id"], f"retrieval_response result {result['chunk_id']} must reference the canonical document version", failures)
        for component_id in result["component_ids"]:
            require(component_id in components, f"retrieval_response result {result['chunk_id']} references missing component {component_id}", failures)
        for span_id in result["span_selector_ids"]:
            require(span_id in span_selectors, f"retrieval_response result {result['chunk_id']} references missing span selector {span_id}", failures)
        for target_id in result.get("citation_target_ids", []):
            require(target_id in citation_targets, f"retrieval_response result {result['chunk_id']} references missing citation target {target_id}", failures)

    require(response_chunk_ids.issubset(trace_chunk_ids), "retrieval_response chunk_ids must be traceable through retrieval_trace.result_trace", failures)

    require(answer_event["retrieval_response_id"] == retrieval_response["retrieval_response_id"], "answer_event.retrieval_response_id must match retrieval_response.retrieval_response_id", failures)
    require(
        not (
            answer_event["grounding_status"] in {"grounded", "partially_grounded"}
            and not answer_event["answer_evidence_ids"]
        ),
        "grounded answer_event requires answer_evidence_ids; empty corpus answers must refuse instead of asserting internal facts",
        failures,
    )
    require("access_basis" in answer_event, "grounded answer_event must carry access_basis for governed internal support", failures)
    access_basis = answer_event.get("access_basis", {})
    if isinstance(access_basis, dict):
        require(access_basis.get("access_decision_id") == access_decision["access_decision_id"], "answer_event.access_basis.access_decision_id must match access_decision.access_decision_id", failures)
        require(access_basis.get("purpose_of_use") == access_decision["environment"]["purpose_of_use"], "answer_event.access_basis.purpose_of_use must match access_decision.environment.purpose_of_use", failures)
        source_policy_refs = set(access_basis.get("source_policy_refs", []))
        for policy_ref in access_decision["policy_basis"]["source_policy_refs"]:
            require(policy_ref in source_policy_refs, f"answer_event.access_basis.source_policy_refs must include {policy_ref}", failures)
    require(set(answer_event["answer_evidence_ids"]) == set(answer_evidence), "answer_event.answer_evidence_ids must match the answer_evidence bundle", failures)

    for evidence_id, evidence in answer_evidence.items():
        require(evidence["answer_event_id"] == answer_event["answer_event_id"], f"answer_evidence {evidence_id} must reference the answer_event", failures)
        require(evidence["retrieval_response_id"] == retrieval_response["retrieval_response_id"], f"answer_evidence {evidence_id} must reference the retrieval_response", failures)
        require(evidence["document_version_id"] == document_version["document_version_id"], f"answer_evidence {evidence_id} must reference the canonical document version", failures)
        for chunk_id in evidence["chunk_ids"]:
            require(chunk_id in chunk_items, f"answer_evidence {evidence_id} references missing chunk {chunk_id}", failures)
            require(chunk_id in response_chunk_ids, f"answer_evidence {evidence_id} chunk {chunk_id} must appear in retrieval_response.ranked_results", failures)
        for component_id in evidence["component_ids"]:
            require(component_id in components, f"answer_evidence {evidence_id} references missing component {component_id}", failures)
        for span_id in evidence["span_selector_ids"]:
            require(span_id in span_selectors, f"answer_evidence {evidence_id} references missing span selector {span_id}", failures)
        for mention_id in evidence.get("citation_mention_ids", []):
            require(mention_id in citation_mentions, f"answer_evidence {evidence_id} references missing citation mention {mention_id}", failures)

    require(gold_asset["document_id"] == document["document_id"], "gold_standard_asset.document_id must match the canonical document", failures)
    require(gold_asset["document_version_id"] == document_version["document_version_id"], "gold_standard_asset.document_version_id must match the canonical document version", failures)
    require(gold_asset["access_policy_ref"] == document["access_policy_ref"], "gold_standard_asset.access_policy_ref must match the document access_policy_ref in the example bundle", failures)
    for source_id in gold_asset["source_artifact_refs"]:
        require(source_id == source_artifact["source_artifact_id"], f"gold_standard_asset source_artifact_ref {source_id} must resolve to the canonical source artifact in the example bundle", failures)
    for component_id in gold_asset["component_ids"]:
        require(component_id in components, f"gold_standard_asset references missing component {component_id}", failures)
    for span_id in gold_asset["span_selector_ids"]:
        require(span_id in span_selectors, f"gold_standard_asset references missing span selector {span_id}", failures)
        if span_id in span_selectors:
            require(span_selectors[span_id].get("component_id") in gold_asset["component_ids"], f"gold_standard_asset span selector {span_id} must resolve to one of the asset components", failures)

    return failures


def main() -> int:
    legal = load_json(EXAMPLES / "documents" / "legal-document.example.json")
    chunks = load_json(EXAMPLES / "documents" / "chunk-set.example.json")
    answers = load_json(EXAMPLES / "documents" / "answer-trace.example.json")
    gold = load_json(EXAMPLES / "gold-standard" / "gold-standard-asset.example.json")
    failures = collect_failures(legal, chunks, answers, gold)

    if failures:
        print("CANONICAL GROUNDING CHAIN VALIDATION FAILURES:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("Canonical grounding chain validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
