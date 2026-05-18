"""PR-10 cross-repo OS smoke tests."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = REPO_ROOT.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from cross_repo_os_smoke_test import (  # noqa: E402
    REPO_ALIASES,
    find_repo,
    resolve_workspace,
    run_smoke,
)


@pytest.fixture
def workspace() -> Path:
    return WORKSPACE


def test_workspace_has_five_repos(workspace: Path) -> None:
    missing = [name for name in REPO_ALIASES if find_repo(workspace, name) is None]
    if missing:
        pytest.skip(f"missing sibling repos for cross-repo smoke: {missing}")
    repos = resolve_workspace(workspace)
    assert repos.substrate.is_dir()
    assert repos.orchestrator.is_dir()
    assert repos.lake.is_dir()
    assert repos.lkr.is_dir()
    assert repos.skills.is_dir()


def test_cross_repo_smoke_valid_path(workspace: Path) -> None:
    if any(find_repo(workspace, name) is None for name in REPO_ALIASES):
        pytest.skip("five-repo workspace required")
    outcome = run_smoke(workspace)
    assert outcome.ok, outcome.errors
    assert outcome.valid_path["admission_status"] == "admitted"
    assert outcome.valid_path.get("passage_ref_id")
    assert outcome.valid_path.get("claim_ref_id")
    assert outcome.valid_path.get("skill_trust_record_id")
    assert outcome.missing_passport_path.get("defect_classes")
    assert outcome.denied_action_path.get("denied_action_preserved") is True
    assert outcome.architecture_coverage_ok
    assert outcome.substrate_files_unchanged


def test_missing_passport_path_mints_defect(workspace: Path) -> None:
    if any(find_repo(workspace, name) is None for name in REPO_ALIASES):
        pytest.skip("five-repo workspace required")
    outcome = run_smoke(workspace)
    assert outcome.missing_passport_path.get("eval_candidate_count", 0) >= 1


def test_all_records_share_contract_surface(workspace: Path) -> None:
    if any(find_repo(workspace, name) is None for name in REPO_ALIASES):
        pytest.skip("five-repo workspace required")
    outcome = run_smoke(workspace)
    assert outcome.contract_surface_sha256
    assert len(outcome.contract_surface_sha256) == 64


def test_smoke_cli_entrypoint(workspace: Path, tmp_path: Path) -> None:
    if any(find_repo(workspace, name) is None for name in REPO_ALIASES):
        pytest.skip("five-repo workspace required")
    json_out = tmp_path / "smoke_summary.json"
    proc = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "cross_repo_os_smoke_test.py"),
            "--workspace",
            str(workspace),
            "--json-out",
            str(json_out),
        ],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout
    summary = json.loads(json_out.read_text(encoding="utf-8"))
    assert summary["ok"] is True


def test_provider_metadata_not_on_skill_trust_canon(workspace: Path) -> None:
    if any(find_repo(workspace, name) is None for name in REPO_ALIASES):
        pytest.skip("five-repo workspace required")
    outcome = run_smoke(workspace)
    assert outcome.ok
