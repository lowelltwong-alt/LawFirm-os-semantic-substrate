#!/usr/bin/env python3
"""Validate the intake contract promotion review docket."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "intake-contract-promotion-review-registry.json"
REQUIRED_PROPOSALS = {
    "substrate.intake-source-and-evidence-refs.v0_1",
    "substrate.human-confirmation-and-candidates.v0_1",
    "substrate.budget-and-event-labels.v0_1",
}
REQUIRED_GLOBAL_FALSE_FLAGS = {
    "canonical_schema_ids_assigned",
    "canonical_route_ids_assigned",
    "canonical_event_classes_assigned",
    "runtime_execution_authorized",
    "real_data_pilot_authorized",
    "external_writes_authorized",
    "raw_legal_payload_storage_authorized",
}
REQUIRED_ITEM_GATES = {
    "human_promotion_decision_before_canonical_schema_id",
    "human_promotion_decision_before_canonical_event_class",
}


class IntakeContractPromotionReviewError(ValueError):
    """Raised when the intake contract promotion review docket is invalid."""


def _rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def _load_json(path: Path) -> dict[str, Any]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise IntakeContractPromotionReviewError(f"{_rel(path)} unreadable: {exc}") from exc
    if not isinstance(data, dict):
        raise IntakeContractPromotionReviewError(f"{_rel(path)} must be a JSON object")
    return data


def _require_non_empty_strings(value: Any, *, label: str) -> list[str]:
    if not isinstance(value, list) or not value:
        raise IntakeContractPromotionReviewError(f"{label} must be a non-empty list")
    if not all(isinstance(item, str) and item.strip() for item in value):
        raise IntakeContractPromotionReviewError(f"{label} must contain non-empty strings")
    return value


def validate_intake_contract_promotion_review(path: Path = REGISTRY) -> dict[str, Any]:
    data = _load_json(path)
    if data.get("schema_version") != "intake_contract_promotion_review_registry.v0_1":
        raise IntakeContractPromotionReviewError("unsupported intake promotion review schema_version")
    if data.get("registry_id") != "intake-contract-promotion-review-registry.v0_1":
        raise IntakeContractPromotionReviewError("unexpected registry_id")
    if data.get("status") != "candidate_review_docket":
        raise IntakeContractPromotionReviewError("status must be candidate_review_docket")
    if data.get("owner_repo") != "LawFirm-os-semantic-substrate":
        raise IntakeContractPromotionReviewError("owner_repo must be LawFirm-os-semantic-substrate")
    if data.get("source_repo") != "LawFirm-os-intake":
        raise IntakeContractPromotionReviewError("source_repo must be LawFirm-os-intake")
    if data.get("source_package_id") != "cross-repo-promotion-package.intake-to-budget.v0_1":
        raise IntakeContractPromotionReviewError("unexpected source_package_id")

    controls = data.get("global_controls")
    if not isinstance(controls, dict):
        raise IntakeContractPromotionReviewError("global_controls must be an object")
    if controls.get("candidate_only") is not True:
        raise IntakeContractPromotionReviewError("global_controls.candidate_only must be true")
    if controls.get("promotion_decision_required_for_canonical_change") is not True:
        raise IntakeContractPromotionReviewError(
            "global_controls.promotion_decision_required_for_canonical_change must be true"
        )
    for key in REQUIRED_GLOBAL_FALSE_FLAGS:
        if controls.get(key) is not False:
            raise IntakeContractPromotionReviewError(f"global_controls.{key} must be false")

    governance_doc = data.get("governance_doc")
    if not isinstance(governance_doc, str) or not governance_doc.strip():
        raise IntakeContractPromotionReviewError("governance_doc must be a non-empty string")
    governance_path = ROOT / governance_doc
    if not governance_path.is_file():
        raise IntakeContractPromotionReviewError(f"governance_doc missing: {governance_doc}")

    items = data.get("review_items")
    if not isinstance(items, list) or not items:
        raise IntakeContractPromotionReviewError("review_items must be a non-empty list")
    proposal_ids: list[str] = []
    for index, item in enumerate(items):
        if not isinstance(item, dict):
            raise IntakeContractPromotionReviewError(f"review_items[{index}] must be an object")
        proposal_id = item.get("proposal_id")
        if not isinstance(proposal_id, str) or not proposal_id.strip():
            raise IntakeContractPromotionReviewError(f"review_items[{index}].proposal_id missing")
        proposal_ids.append(proposal_id)
        if item.get("target_repo") != "LawFirm-os-semantic-substrate":
            raise IntakeContractPromotionReviewError(f"{proposal_id} target_repo must be Semantic Substrate")
        if item.get("review_disposition") != "needs_substrate_review":
            raise IntakeContractPromotionReviewError(
                f"{proposal_id} review_disposition must be needs_substrate_review"
            )
        if item.get("promotion_decision_required") is not True:
            raise IntakeContractPromotionReviewError(
                f"{proposal_id} promotion_decision_required must be true"
            )
        if item.get("direct_promotion_authorized") is not False:
            raise IntakeContractPromotionReviewError(
                f"{proposal_id} direct_promotion_authorized must be false"
            )
        contract_refs = _require_non_empty_strings(
            item.get("candidate_contract_refs"),
            label=f"{proposal_id}.candidate_contract_refs",
        )
        if not all(ref.startswith("semantic-substrate://candidate/") for ref in contract_refs):
            raise IntakeContractPromotionReviewError(
                f"{proposal_id} candidate refs must stay under semantic-substrate://candidate/"
            )
        _require_non_empty_strings(
            item.get("candidate_artifact_refs"),
            label=f"{proposal_id}.candidate_artifact_refs",
        )
        existing_surfaces = _require_non_empty_strings(
            item.get("existing_substrate_surfaces_to_compare"),
            label=f"{proposal_id}.existing_substrate_surfaces_to_compare",
        )
        missing_surfaces = [rel for rel in existing_surfaces if not (ROOT / rel).exists()]
        if missing_surfaces:
            raise IntakeContractPromotionReviewError(
                f"{proposal_id} references missing substrate surfaces: {missing_surfaces}"
            )
        gates = set(
            _require_non_empty_strings(
                item.get("required_acceptance_gates"),
                label=f"{proposal_id}.required_acceptance_gates",
            )
        )
        if not gates.intersection(REQUIRED_ITEM_GATES):
            raise IntakeContractPromotionReviewError(
                f"{proposal_id} is missing a human promotion-decision gate"
            )
        _require_non_empty_strings(
            item.get("promotion_blockers"),
            label=f"{proposal_id}.promotion_blockers",
        )

    if set(proposal_ids) != REQUIRED_PROPOSALS:
        raise IntakeContractPromotionReviewError(
            "review_items proposal IDs do not match required Substrate intake proposals"
        )
    if len(proposal_ids) != len(set(proposal_ids)):
        raise IntakeContractPromotionReviewError("review_items contains duplicate proposal IDs")

    governance_text = governance_path.read_text(encoding="utf-8")
    required_text = [
        data["source_package_id"],
        "registry/intake-contract-promotion-review-registry.json",
        "does not",
        *sorted(REQUIRED_PROPOSALS),
    ]
    missing_text = [text for text in required_text if text not in governance_text]
    if missing_text:
        raise IntakeContractPromotionReviewError(
            f"{governance_doc} missing required text: {missing_text}"
        )
    return data


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--registry", type=Path, default=REGISTRY)
    args = parser.parse_args(argv)
    try:
        validate_intake_contract_promotion_review(args.registry)
    except IntakeContractPromotionReviewError as exc:
        print(f"Intake contract promotion review validation failed: {exc}", file=sys.stderr)
        return 1
    print("Intake contract promotion review validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
