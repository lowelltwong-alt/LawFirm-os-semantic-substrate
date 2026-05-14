from __future__ import annotations

from pathlib import Path

from scripts.validate_ai_front_door import validate_ai_front_door


def test_ai_front_door_integrity_gate_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    errors = validate_ai_front_door(root)
    assert errors == [], "\n".join(errors)
