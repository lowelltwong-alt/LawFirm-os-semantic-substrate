from pathlib import Path
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

import validate_real_work_and_simulation_boundaries as validator  # noqa: E402


def test_real_work_and_simulation_boundaries_pass() -> None:
    validator.validate_boundaries()


def test_real_work_gate_fails_closed_when_token_removed(tmp_path: Path) -> None:
    governance = tmp_path / "governance"
    governance.mkdir()
    for rel, tokens in validator.REQUIRED_TOKENS.items():
        target = tmp_path / rel
        target.parent.mkdir(parents=True, exist_ok=True)
        selected = set(tokens)
        if rel.endswith("REAL_WORK_SHADOW_MODE_PILOT_GATES.md"):
            selected.remove("connector_write_authorized_false")
        target.write_text("\n".join(sorted(selected)), encoding="utf-8")

    with pytest.raises(validator.BoundaryValidationError):
        validator.validate_boundaries(tmp_path)
