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
