import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parent
SCRIPT = ROOT / "scripts" / "route_ci_tests.py"
VALIDATE = ROOT / "scripts" / "validate_ci_route_decision.py"

ACTIVE_REPOS = [
    "LawFirm-os-exceptions-lake-runtime",
    "LawFirm-os-legal-knowledge-runtime",
    "LawFirm-os-orchestrator",
    "LawFirm-os-semantic-substrate",
    "LawFirm-os-skills-registry",
]

def run(*args):
    return subprocess.run([sys.executable, *map(str, args)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def _route(tmp_path, *changed_files):
    out = tmp_path / "decision.json"
    proc = run(SCRIPT, "--workspace", WORKSPACE, *[a for cf in changed_files for a in ("--changed-file", cf)], "--out", out)
    assert proc.returncode == 0, proc.stderr
    return json.loads(out.read_text()), out

def _strict_verify(out_path, *, ran_validators=(), ran_tests=(), ran_pytest_repos=(), allow_missing=False):
    args = [VALIDATE, "--workspace", WORKSPACE, "--decision", out_path]
    if allow_missing:
        args.append("--allow-missing-run-evidence")
    for v in ran_validators:
        args += ["--ran-validator", v]
    for t in ran_tests:
        args += ["--ran-test-artifact", t]
    for r in ran_pytest_repos:
        args += ["--ran-pytest-repo", r]
    return run(*args)


def test_agents_change_routes_to_front_door_and_preservation(tmp_path):
    d, _ = _route(tmp_path, "LawFirm-os-orchestrator/AGENTS.md")
    assert "ai_instruction_change" in d["change_classes"]
    assert "validate_ai_front_door" in d["required_validators"]
    assert "validate_managed_patch_preservation" in d["required_validators"]
    assert d["risk_tier"] == "protected"


def test_contract_lock_routes_to_contract_drift(tmp_path):
    d, _ = _route(tmp_path, "LawFirm-os-orchestrator/contracts.lock.json")
    assert "contract_lock_change" in d["change_classes"]
    assert "validate_contract_lock_drift_workspace" in d["required_validators"]
    assert d["requires_human_review"] is True


def test_router_policy_change_requires_full_validation(tmp_path):
    d, _ = _route(tmp_path, "LawFirm-os-semantic-substrate/registry/ci-test-route-registry.json")
    assert "ci_router_change" in d["change_classes"]
    assert d["requires_full_workspace_tests"] is True


def test_final_verifier_fails_when_required_validator_not_run(tmp_path):
    _, out = _route(tmp_path, "LawFirm-os-orchestrator/AGENTS.md")
    proc = _strict_verify(out)
    assert proc.returncode != 0
    assert "required validators did not run" in proc.stderr


def test_strict_fails_when_required_pytest_repo_evidence_missing(tmp_path):
    d, out = _route(tmp_path, "LawFirm-os-semantic-substrate/registry/ci-test-route-registry.json")
    # Pass every required validator and every required test artifact, but no --ran-pytest-repo evidence.
    proc = _strict_verify(
        out,
        ran_validators=d["required_validators"],
        ran_tests=d["required_test_artifacts"],
        ran_pytest_repos=(),
    )
    assert proc.returncode != 0
    assert "required pytest repos did not run" in proc.stderr


def test_strict_passes_only_when_every_required_repo_pytest_proven(tmp_path):
    d, out = _route(tmp_path, "LawFirm-os-semantic-substrate/registry/ci-test-route-registry.json")
    # Drop one repo to prove that partial evidence still fails.
    partial = d["required_pytest_repos"][:-1]
    proc_partial = _strict_verify(
        out,
        ran_validators=d["required_validators"],
        ran_tests=d["required_test_artifacts"],
        ran_pytest_repos=partial,
    )
    assert proc_partial.returncode != 0
    assert "required pytest repos did not run" in proc_partial.stderr
    proc_full = _strict_verify(
        out,
        ran_validators=d["required_validators"],
        ran_tests=d["required_test_artifacts"],
        ran_pytest_repos=d["required_pytest_repos"],
    )
    assert proc_full.returncode == 0, proc_full.stderr


def test_full_workspace_tests_requires_all_active_repos_in_required_pytest_repos(tmp_path):
    # A ci_router_change forces requires_full_workspace_tests=true and expands required_pytest_repos to all active repos.
    d, out = _route(tmp_path, "LawFirm-os-semantic-substrate/scripts/route_ci_tests.py")
    assert d["requires_full_workspace_tests"] is True
    for repo in ACTIVE_REPOS:
        assert repo in d["required_pytest_repos"], f"missing active repo {repo} in required_pytest_repos"
    # Forge a decision that drops one active repo from required_pytest_repos and confirm strict mode rejects it.
    bad = json.loads(out.read_text())
    bad["required_pytest_repos"] = [r for r in bad["required_pytest_repos"] if r != "LawFirm-os-orchestrator"]
    bad_path = tmp_path / "bad_decision.json"
    bad_path.write_text(json.dumps(bad))
    proc = _strict_verify(
        bad_path,
        ran_validators=bad["required_validators"],
        ran_tests=bad["required_test_artifacts"],
        ran_pytest_repos=bad["required_pytest_repos"],
    )
    assert proc.returncode != 0
    assert "requires_full_workspace_tests=true but required_pytest_repos missing active repos" in proc.stderr


def test_unknown_change_escalates_to_protected_full_workspace_codex_human(tmp_path):
    # A path that matches no classifier (no .md, .py, .json, no governance/registry/schemas, no contracts.lock.json, etc.).
    d, _ = _route(tmp_path, "LawFirm-os-semantic-substrate/some_unclassified_area/notes.txt")
    assert "unknown_change" in d["change_classes"], d["change_classes"]
    assert d["risk_tier"] == "protected"
    assert d["requires_full_workspace_tests"] is True
    assert d["requires_cross_repo_validation"] is True
    assert d["requires_codex_review"] is True
    assert d["requires_human_review"] is True
    for repo in ACTIVE_REPOS:
        assert repo in d["required_pytest_repos"], f"unknown_change should include {repo} in required_pytest_repos"
    for v in (
        "discover_test_artifacts",
        "validate_test_artifact_registration",
        "validate_new_repo_ci_onboarding",
        "validate_ai_front_door",
        "validate_managed_patch_preservation",
        "validate_skill_agent_control_plane",
        "validate_contract_lock_drift_workspace",
    ):
        assert v in d["required_validators"], f"unknown_change must require validator {v}"


def test_ci_router_source_change_forces_full_workspace_validation(tmp_path):
    for path in (
        "LawFirm-os-semantic-substrate/scripts/route_ci_tests.py",
        "LawFirm-os-semantic-substrate/scripts/validate_ci_route_decision.py",
    ):
        d, _ = _route(tmp_path, path)
        assert "ci_router_change" in d["change_classes"], f"{path} should set ci_router_change"
        assert d["requires_full_workspace_tests"] is True, f"{path} should require full workspace tests"
        assert d["requires_codex_review"] is True
        assert d["requires_human_review"] is True


def test_architecture_surface_in_changed_area_selects_tests_covering_surface(tmp_path):
    # A change inside substrate governance/ maps to architecture surface governance_boundary.
    # The substrate test test_validate_exception_governance covers governance_boundary, so it must be selected.
    d, _ = _route(tmp_path, "LawFirm-os-semantic-substrate/governance/CI_TEST_ROUTING_BOUNDARY.md")
    assert "governance_boundary" in d["affected_architecture_surfaces"], d["affected_architecture_surfaces"]
    assert any(
        tid.endswith("test_validate_exception_governance.v1")
        for tid in d["required_test_artifacts"]
    ), d["required_test_artifacts"]


def test_downstream_dependencies_pull_dependent_repo_tests(tmp_path):
    # A substrate change (registry file) should pull dependent orchestrator tests whose
    # upstream_dependencies include LawFirm-os-semantic-substrate.
    d, _ = _route(tmp_path, "LawFirm-os-semantic-substrate/registry/schema-registry.json")
    assert "LawFirm-os-semantic-substrate" in d["affected_repos"]
    # At least one orchestrator test should be selected by the dependency-graph propagation.
    assert any(
        tid.startswith("LawFirm-os-orchestrator.")
        for tid in d["required_test_artifacts"]
    ), d["required_test_artifacts"]


def test_strict_verifier_rejects_unknown_run_evidence(tmp_path):
    d, out = _route(tmp_path, "LawFirm-os-orchestrator/AGENTS.md")
    proc = _strict_verify(
        out,
        ran_validators=list(d["required_validators"]) + ["validator_that_does_not_exist"],
        ran_tests=d["required_test_artifacts"],
        ran_pytest_repos=d["required_pytest_repos"],
    )
    assert proc.returncode != 0
    assert "unknown ran validators" in proc.stderr


def test_strict_rejects_unknown_pytest_repo_run_evidence(tmp_path):
    d, out = _route(tmp_path, "LawFirm-os-semantic-substrate/registry/ci-test-route-registry.json")
    proc = _strict_verify(
        out,
        ran_validators=d["required_validators"],
        ran_tests=d["required_test_artifacts"],
        ran_pytest_repos=list(d["required_pytest_repos"]) + ["LawFirm-os-not-a-real-repo"],
    )
    assert proc.returncode != 0
    assert "unknown ran pytest repos" in proc.stderr


def test_strict_rejects_unknown_test_artifact_run_evidence(tmp_path):
    d, out = _route(tmp_path, "LawFirm-os-orchestrator/AGENTS.md")
    proc = _strict_verify(
        out,
        ran_validators=d["required_validators"],
        ran_tests=list(d["required_test_artifacts"]) + ["made_up_test_id.v1"],
        ran_pytest_repos=d["required_pytest_repos"],
    )
    assert proc.returncode != 0
    assert "unknown ran test artifacts" in proc.stderr


def test_planning_mode_allows_missing_run_evidence(tmp_path):
    _, out = _route(tmp_path, "LawFirm-os-orchestrator/AGENTS.md")
    proc = _strict_verify(out, allow_missing=True)
    assert proc.returncode == 0, proc.stderr


def test_downstream_affected_includes_declared_upstream_repo_tests(tmp_path):
    # When the exception lake changes (unknown file class), orchestrator tests that declare the lake as
    # downstream_dependencies must be selected even though the lake is not an upstream consumer of orchestrator.
    d, _ = _route(tmp_path, "LawFirm-os-exceptions-lake-runtime/notes_unclassified.xyz")
    assert "LawFirm-os-exceptions-lake-runtime" in d["affected_repos"]
    assert any(
        tid.startswith("LawFirm-os-orchestrator.") for tid in d["required_test_artifacts"]
    ), d["required_test_artifacts"]
