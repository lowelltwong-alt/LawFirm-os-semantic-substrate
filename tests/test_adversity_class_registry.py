from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

from scripts.validate_adversity_class_registry import (
    AdversityClassRegistryError,
    validate_adversity_class_registry,
)


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "registry" / "adversity-class-registry.candidate.json"
VALIDATOR = ROOT / "scripts" / "validate_adversity_class_registry.py"


def _mutated_registry(tmp_path: Path, mutator) -> Path:
    payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
    mutator(payload)
    path = tmp_path / "adversity-class-registry.candidate.json"
    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return path


def test_candidate_adversity_registry_passes() -> None:
    registry = validate_adversity_class_registry()

    assert registry["status"] == "candidate_synthetic_only"
    assert registry["authority"]["canonical_adversity_classes_assigned"] is False
    assert registry["authority"]["conflict_clearance_authorized"] is False
    assert registry["authority"]["runtime_execution_authorized"] is False
    assert registry["human_decisions"][
        "hd_4_authoritative_adversity_classes_decided"
    ] is False
    assert registry["synthetic_fixture_graph"]["adversity_inference_performed"] is False


def test_candidate_adversity_registry_cli_passes() -> None:
    result = subprocess.run(
        [sys.executable, str(VALIDATOR)],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )

    assert result.returncode == 0, result.stderr
    assert "Adversity class registry validation passed" in result.stdout


def test_candidate_registry_rejects_authority_flip(tmp_path: Path) -> None:
    path = _mutated_registry(
        tmp_path,
        lambda payload: payload["authority"].__setitem__(
            "conflict_clearance_authorized",
            True,
        ),
    )

    with pytest.raises(AdversityClassRegistryError, match="schema violation"):
        validate_adversity_class_registry(path)


def test_candidate_registry_rejects_relabelled_class(tmp_path: Path) -> None:
    path = _mutated_registry(
        tmp_path,
        lambda payload: payload["synthetic_fixture_graph"]["conflict_classes"][
            0
        ].__setitem__("class_id", "synthetic-coi-class-relabelled"),
    )

    with pytest.raises(AdversityClassRegistryError, match="fixed Intake PR-LL4 digest"):
        validate_adversity_class_registry(path)


def test_candidate_registry_rejects_case_manifest_drift(tmp_path: Path) -> None:
    path = _mutated_registry(
        tmp_path,
        lambda payload: payload["synthetic_case_manifest"][0].__setitem__(
            "lesson_id",
            "synthetic-lesson-drifted",
        ),
    )

    with pytest.raises(AdversityClassRegistryError, match="case manifest"):
        validate_adversity_class_registry(path)


def test_candidate_registry_rejects_missing_non_applicability(tmp_path: Path) -> None:
    path = _mutated_registry(
        tmp_path,
        lambda payload: payload["usage_contract"].__setitem__(
            "does_not_apply_when",
            [],
        ),
    )

    with pytest.raises(AdversityClassRegistryError, match="schema violation"):
        validate_adversity_class_registry(path)


def test_candidate_registry_rejects_inferred_edge(tmp_path: Path) -> None:
    path = _mutated_registry(
        tmp_path,
        lambda payload: payload["synthetic_fixture_graph"]["adversity_edges"][
            0
        ].__setitem__("inferred_from_similarity", True),
    )

    with pytest.raises(AdversityClassRegistryError, match="schema violation"):
        validate_adversity_class_registry(path)


@pytest.mark.parametrize(
    "field",
    [
        "contains_real_data",
        "contains_private_data",
        "contains_client_data",
        "contains_matter_data",
        "contains_real_carrier_data",
        "contains_privileged_content",
        "contains_work_product",
    ],
)
def test_candidate_registry_rejects_protected_data_flags(
    tmp_path: Path,
    field: str,
) -> None:
    path = _mutated_registry(
        tmp_path,
        lambda payload: payload["synthetic_fixture_graph"].__setitem__(field, True),
    )

    with pytest.raises(AdversityClassRegistryError, match="schema violation"):
        validate_adversity_class_registry(path)
