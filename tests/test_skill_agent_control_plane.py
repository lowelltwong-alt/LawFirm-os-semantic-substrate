from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path


def test_skill_agent_control_plane_workspace_validator():
    substrate = Path(__file__).resolve().parents[1]
    workspace = Path(os.environ.get("LAWFIRM_OS_WORKSPACE", substrate.parent))
    script = substrate / "scripts" / "validate_skill_agent_control_plane.py"
    result = subprocess.run(
        [sys.executable, str(script), "--workspace", str(workspace)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    assert result.returncode == 0, result.stdout
