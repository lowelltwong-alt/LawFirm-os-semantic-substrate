"""Cross-repo contract surface hash spine tests (PR-01).

These tests cover the cross-consumer agreement property that the per-repo
contract-surface drift validator does not explicitly assert. They complement
``test_contract_surface_locking.py`` (which covers surface-computation
properties) and ``validate_contract_lock_drift_workspace.py`` (which covers
per-consumer drift against the substrate).
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent

CONSUMER_REPO_ALIASES: dict[str, list[str]] = {
    "LawFirm-os-orchestrator": ["LawFirm-os-orchestrator", "LawFirm-os-orchestrator-main"],
    "LawFirm-os-exceptions-lake-runtime": [
        "LawFirm-os-exceptions-lake-runtime",
        "LawFirm-os-exceptions-lake-runtime-main",
    ],
    "LawFirm-os-legal-knowledge-runtime": [
        "LawFirm-os-legal-knowledge-runtime",
        "LawFirm-os-legal-knowledge-runtime-main",
    ],
    "LawFirm-os-skills-registry": [
        "LawFirm-os-skills-registry",
        "LawFirm-os-skills-registry-main",
    ],
}


def _find_repo(workspace: Path, logical: str) -> Path | None:
    for name in CONSUMER_REPO_ALIASES.get(logical, [logical]):
        candidate = workspace / name
        if candidate.is_dir():
            return candidate
    return None


def _read_lock(repo: Path) -> dict[str, Any] | None:
    lock_path = repo / "contracts.lock.json"
    if not lock_path.is_file():
        return None
    return json.loads(lock_path.read_text(encoding="utf-8"))


def _discover_consumer_locks() -> dict[str, dict[str, Any]]:
    locks: dict[str, dict[str, Any]] = {}
    for logical in CONSUMER_REPO_ALIASES:
        repo = _find_repo(WORKSPACE_ROOT, logical)
        if repo is None:
            continue
        data = _read_lock(repo)
        if data is None:
            continue
        locks[logical] = data
    return locks


def _surface_block(lock: dict[str, Any]) -> dict[str, Any]:
    block = lock.get("contract_surface_lock")
    assert isinstance(block, dict), "contracts.lock.json must include contract_surface_lock"
    return block


# ---------------------------------------------------------------------------
# Happy-path: cross-repo agreement on the spine
# ---------------------------------------------------------------------------


def test_all_present_consumer_locks_share_surface_sha256() -> None:
    locks = _discover_consumer_locks()
    if not locks:
        pytest.skip(
            "no consumer locks discoverable from substrate sibling layout; "
            "this test requires the LawFirm OS workspace layout"
        )
    digests = {name: _surface_block(lock).get("surface_sha256") for name, lock in locks.items()}
    distinct = sorted({d for d in digests.values() if d})
    assert len(distinct) == 1, (
        "consumer locks disagree on contract_surface_lock.surface_sha256: "
        + json.dumps(digests, sort_keys=True)
    )


def test_all_present_consumer_locks_share_surface_id() -> None:
    locks = _discover_consumer_locks()
    if not locks:
        pytest.skip("no consumer locks discoverable")
    ids = {name: _surface_block(lock).get("surface_id") for name, lock in locks.items()}
    distinct = sorted({i for i in ids.values() if i})
    assert len(distinct) == 1, (
        "consumer locks disagree on contract_surface_lock.surface_id: " + json.dumps(ids, sort_keys=True)
    )


def test_all_present_consumer_locks_share_hash_algorithm() -> None:
    locks = _discover_consumer_locks()
    if not locks:
        pytest.skip("no consumer locks discoverable")
    algos = {name: _surface_block(lock).get("hash_algorithm") for name, lock in locks.items()}
    distinct = sorted({a for a in algos.values() if a})
    assert distinct == ["lawfirm_os_contract_surface_sha256.v1"], (
        "consumer locks must use lawfirm_os_contract_surface_sha256.v1: "
        + json.dumps(algos, sort_keys=True)
    )


def test_all_four_runtime_consumers_have_locks() -> None:
    """PR-01 acceptance: every runtime consumer either has a lock or is staged with a TODO."""
    locks = _discover_consumer_locks()
    if not locks:
        pytest.skip("no consumer locks discoverable in sibling layout")
    expected = set(CONSUMER_REPO_ALIASES)
    present = set(locks)
    missing = expected - present
    assert not missing, (
        "PR-01 requires lock files in all four runtime consumers; missing: " + ", ".join(sorted(missing))
    )


def test_governance_spine_doc_exists() -> None:
    doc = REPO_ROOT / "governance" / "CONTRACT_SURFACE_HASH_SPINE.md"
    assert doc.is_file(), "PR-01 requires governance/CONTRACT_SURFACE_HASH_SPINE.md"
    body = doc.read_text(encoding="utf-8")
    assert "lawfirm_os_contract_surface_sha256.v1" in body, (
        "spine doc must reference the canonical hash algorithm name"
    )
    assert "contract_surface_lock.surface_sha256" in body, (
        "spine doc must name the per-lock field consumers must validate"
    )


# ---------------------------------------------------------------------------
# Negative cases: mismatched / missing / malformed locks fail closed
# ---------------------------------------------------------------------------


def _spine_agreement_errors(locks: dict[str, dict[str, Any]]) -> list[str]:
    """Pure helper: returns error strings if locks disagree on the spine."""
    errors: list[str] = []
    fields = ("surface_id", "surface_sha256", "hash_algorithm", "surface_registry_path")
    for field in fields:
        values = {name: _surface_block(lock).get(field) for name, lock in locks.items()}
        distinct = sorted({v for v in values.values() if v is not None})
        if len(distinct) > 1:
            errors.append(f"{field} disagreement: {json.dumps(values, sort_keys=True)}")
    for name, lock in locks.items():
        surface = _surface_block(lock)
        sha = surface.get("surface_sha256")
        if not isinstance(sha, str) or len(sha) != 64:
            errors.append(f"{name}: surface_sha256 missing or wrong length")
        algo = surface.get("hash_algorithm")
        if algo != "lawfirm_os_contract_surface_sha256.v1":
            errors.append(f"{name}: hash_algorithm not the canonical algorithm")
    return errors


def test_synthetic_mismatched_lock_is_detected() -> None:
    good = {
        "contract_surface_lock": {
            "surface_id": "lawfirm_os_semantic_substrate.consumer_contract_surface.v1",
            "surface_sha256": "a" * 64,
            "hash_algorithm": "lawfirm_os_contract_surface_sha256.v1",
            "surface_registry_path": "registry/contract-surface-registry.json",
        }
    }
    bad = {
        "contract_surface_lock": {
            "surface_id": "lawfirm_os_semantic_substrate.consumer_contract_surface.v1",
            "surface_sha256": "b" * 64,
            "hash_algorithm": "lawfirm_os_contract_surface_sha256.v1",
            "surface_registry_path": "registry/contract-surface-registry.json",
        }
    }
    errors = _spine_agreement_errors({"consumer_a": good, "consumer_b": bad})
    assert any("surface_sha256 disagreement" in e for e in errors), errors


def test_synthetic_wrong_algorithm_is_detected() -> None:
    bad = {
        "contract_surface_lock": {
            "surface_id": "lawfirm_os_semantic_substrate.consumer_contract_surface.v1",
            "surface_sha256": "a" * 64,
            "hash_algorithm": "lawfirm_os_contract_surface_sha512.v9",
            "surface_registry_path": "registry/contract-surface-registry.json",
        }
    }
    errors = _spine_agreement_errors({"consumer_x": bad})
    assert any("hash_algorithm not the canonical algorithm" in e for e in errors), errors


def test_synthetic_truncated_sha_is_detected() -> None:
    bad = {
        "contract_surface_lock": {
            "surface_id": "lawfirm_os_semantic_substrate.consumer_contract_surface.v1",
            "surface_sha256": "a" * 32,
            "hash_algorithm": "lawfirm_os_contract_surface_sha256.v1",
            "surface_registry_path": "registry/contract-surface-registry.json",
        }
    }
    errors = _spine_agreement_errors({"consumer_x": bad})
    assert any("surface_sha256 missing or wrong length" in e for e in errors), errors
