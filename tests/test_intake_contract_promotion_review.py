from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from scripts.validate_intake_contract_promotion_review import (
    IntakeContractPromotionReviewError,
    validate_intake_contract_promotion_review,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "intake-contract-promotion-review-registry.json"
VALIDATOR = ROOT / "scripts" / "validate_intake_contract_promotion_review.py"


def _registry_copy(tmp_path: Path) -> Path:
    copy_path = tmp_path / "intake-contract-promotion-review-registry.json"
    copy_path.write_text(REGISTRY.read_text(encoding="utf-8"), encoding="utf-8")
    return copy_path


def _mutate_registry(tmp_path: Path, mutator) -> Path:
    path = _registry_copy(tmp_path)
    data = json.loads(path.read_text(encoding="utf-8"))
    mutator(data)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def test_intake_contract_promotion_review_registry_passes() -> None:
    registry = validate_intake_contract_promotion_review()

    assert registry["status"] == "candidate_review_docket"
    assert registry["global_controls"]["candidate_only"] is True
    assert registry["global_controls"]["canonical_schema_ids_assigned"] is False
    assert registry["global_controls"]["external_writes_authorized"] is False
    assert {item["proposal_id"] for item in registry["review_items"]} == {
        "substrate.intake-source-and-evidence-refs.v0_1",
        "substrate.human-confirmation-and-candidates.v0_1",
        "substrate.budget-and-event-labels.v0_1",
        "substrate.orchestrator-lake-packet-boundary.v0_1",
    }
    assert all(
        item["review_disposition"] == "needs_substrate_review"
        for item in registry["review_items"]
    )
    assert all(
        item["direct_promotion_authorized"] is False
        for item in registry["review_items"]
    )
    packet_item = next(
        item
        for item in registry["review_items"]
        if item["proposal_id"] == "substrate.orchestrator-lake-packet-boundary.v0_1"
    )
    assert {
        "confirm_local_workflow_labels_are_not_canonical_route_ids",
        "confirm_packet_validation_is_not_exception_lake_admission",
        "preserve_no_lake_or_sqlite_write_authority",
    }.issubset(packet_item["required_acceptance_gates"])
    assert (
        "schemas/evidence-packet.v2.schema.json"
        in packet_item["existing_substrate_surfaces_to_compare"]
    )


def test_intake_contract_promotion_review_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Intake contract promotion review validation passed" in result.stdout


def test_intake_contract_review_blocks_direct_promotion(tmp_path: Path) -> None:
    path = _mutate_registry(
        tmp_path,
        lambda data: data["review_items"][0].__setitem__(
            "direct_promotion_authorized",
            True,
        ),
    )

    with pytest.raises(IntakeContractPromotionReviewError, match="must be false"):
        validate_intake_contract_promotion_review(path)


def test_intake_contract_review_requires_all_substrate_proposals(
    tmp_path: Path,
) -> None:
    path = _mutate_registry(
        tmp_path,
        lambda data: data.__setitem__("review_items", data["review_items"][:-1]),
    )

    with pytest.raises(IntakeContractPromotionReviewError, match="proposal IDs"):
        validate_intake_contract_promotion_review(path)


def test_intake_contract_review_blocks_non_candidate_contract_ref(
    tmp_path: Path,
) -> None:
    path = _mutate_registry(
        tmp_path,
        lambda data: data["review_items"][0]["candidate_contract_refs"].__setitem__(
            0,
            "semantic-substrate://contracts/intake-source.v1",
        ),
    )

    with pytest.raises(IntakeContractPromotionReviewError, match="candidate refs"):
        validate_intake_contract_promotion_review(path)


def test_intake_contract_review_requires_packet_boundary_gates(tmp_path: Path) -> None:
    def remove_packet_gate(data: dict) -> None:
        item = next(
            item
            for item in data["review_items"]
            if item["proposal_id"] == "substrate.orchestrator-lake-packet-boundary.v0_1"
        )
        item["required_acceptance_gates"].remove(
            "preserve_no_lake_or_sqlite_write_authority"
        )

    path = _mutate_registry(tmp_path, remove_packet_gate)

    with pytest.raises(
        IntakeContractPromotionReviewError, match="packet-boundary gates"
    ):
        validate_intake_contract_promotion_review(path)
