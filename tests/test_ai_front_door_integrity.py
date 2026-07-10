from __future__ import annotations

import json
from pathlib import Path

from scripts.validate_ai_front_door import _sibling, validate_ai_front_door


def test_ai_front_door_integrity_gate_passes() -> None:
    root = Path(__file__).resolve().parents[1]
    errors = validate_ai_front_door(root)
    assert errors == [], "\n".join(errors)


def test_sibling_resolver_prefers_canonical_then_uses_declared_alias(tmp_path: Path) -> None:
    substrate = tmp_path / "LawFirm-os-semantic-substrate"
    substrate.mkdir()
    canonical = tmp_path / "LawFirm-os-exceptions-lake-runtime"
    alias = tmp_path / "LawFirm-os-exceptions-lake-runtime-main"
    alias.mkdir()
    front_door = {
        "sibling_repo_folder_names": {
            "exception_lake": canonical.name,
        },
        "sibling_repo_folder_aliases": {
            "exception_lake": [alias.name],
        },
        "sibling_repo_identity_contracts": {
            "exception_lake": {
                "manifest_path": "skill-agent-manifest.json",
                "required_fields": {
                    "owning_repo": "LawFirm-os-exceptions-lake-runtime",
                    "owning_plane": "exception_lake",
                },
            },
        },
    }
    identity = {
        "owning_repo": "LawFirm-os-exceptions-lake-runtime",
        "owning_plane": "exception_lake",
    }
    (alias / "skill-agent-manifest.json").write_text(
        json.dumps(identity),
        encoding="utf-8",
    )

    assert _sibling(substrate, front_door, "exception_lake") == alias
    canonical.mkdir()
    (canonical / "skill-agent-manifest.json").write_text(
        json.dumps(identity),
        encoding="utf-8",
    )
    assert _sibling(substrate, front_door, "exception_lake") == canonical


def test_sibling_resolver_rejects_alias_with_wrong_identity(tmp_path: Path) -> None:
    substrate = tmp_path / "LawFirm-os-semantic-substrate"
    substrate.mkdir()
    canonical = tmp_path / "LawFirm-os-exceptions-lake-runtime"
    alias = tmp_path / "LawFirm-os-exceptions-lake-runtime-main"
    alias.mkdir()
    (alias / "skill-agent-manifest.json").write_text(
        json.dumps({"owning_repo": "wrong-repo", "owning_plane": "exception_lake"}),
        encoding="utf-8",
    )
    front_door = {
        "sibling_repo_folder_names": {"exception_lake": canonical.name},
        "sibling_repo_folder_aliases": {"exception_lake": [alias.name]},
        "sibling_repo_identity_contracts": {
            "exception_lake": {
                "manifest_path": "skill-agent-manifest.json",
                "required_fields": {
                    "owning_repo": "LawFirm-os-exceptions-lake-runtime",
                    "owning_plane": "exception_lake",
                },
            },
        },
    }

    assert _sibling(substrate, front_door, "exception_lake") == canonical
