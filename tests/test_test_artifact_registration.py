import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DISCOVER = ROOT / "scripts" / "discover_test_artifacts.py"
VALIDATE = ROOT / "scripts" / "validate_test_artifact_registration.py"
ONBOARD = ROOT / "scripts" / "validate_new_repo_ci_onboarding.py"

def run(*args):
    return subprocess.run([sys.executable, *map(str,args)], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def test_discovery_runs_workspace_wide():
    proc = run(DISCOVER, "--workspace", ROOT.parent)
    assert proc.returncode == 0, proc.stderr
    assert "test_artifact_discovery.v1" in proc.stdout

def test_registration_validator_passes_current_workspace():
    proc = run(VALIDATE, "--workspace", ROOT.parent)
    assert proc.returncode == 0, proc.stderr

def test_new_repo_onboarding_passes_current_workspace():
    proc = run(ONBOARD, "--workspace", ROOT.parent)
    assert proc.returncode == 0, proc.stderr

def test_repo_registry_explicit_exclusions_skip_candidate_repos(tmp_path):
    workspace = tmp_path / "workspace"
    substrate = workspace / "LawFirm-os-semantic-substrate"
    candidate = workspace / "LawFirm-os-private-candidate"
    substrate.mkdir(parents=True)
    candidate.mkdir()
    (candidate / "tests").mkdir()
    (candidate / "tests" / "test_unregistered.py").write_text("def test_candidate():\n    assert True\n", encoding="utf-8")

    for name in ["README.md", "AGENTS.md", "AI_WORK_START_HERE.md"]:
        (substrate / name).write_text("LawFirm-os-semantic-substrate\n", encoding="utf-8")
    (substrate / "skill-agent-manifest.json").write_text('{"artifacts":[]}\n', encoding="utf-8")
    (substrate / "ci-test-manifest.json").write_text(
        json.dumps(
            {
                "repo": "LawFirm-os-semantic-substrate",
                "owning_plane": "semantic_substrate",
                "test_artifacts": [],
                "no_tests_yet_rationale": "temp fixture",
                "temporary_until": "2026-12-31",
            }
        )
        + "\n",
        encoding="utf-8",
    )
    registry = {
        "repos": [
            {
                "repo_id": "lawfirm-os-semantic-substrate",
                "repo_name": "LawFirm-os-semantic-substrate",
                "owning_plane": "semantic_substrate",
                "required_root_files": [
                    "README.md",
                    "AGENTS.md",
                    "AI_WORK_START_HERE.md",
                    "skill-agent-manifest.json",
                ],
                "status": "active",
            }
        ],
        "explicit_exclusions": [
            {
                "pattern": "LawFirm-os-private-*",
                "reason": "fixture candidate repo",
            }
        ],
    }
    (substrate / "registry").mkdir()
    (substrate / "registry" / "lawfirm-os-repo-registry.json").write_text(
        json.dumps(registry) + "\n",
        encoding="utf-8",
    )

    onboarding = run(ONBOARD, "--workspace", workspace)
    registration = run(VALIDATE, "--workspace", workspace)

    assert onboarding.returncode == 0, onboarding.stderr
    assert registration.returncode == 0, registration.stderr
