from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = REPO_ROOT.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_architecture_object_coverage import (  # noqa: E402
    CoverageResult,
    validate,
    validate_spine_objects,
)


@pytest.fixture
def coverage_cfg() -> dict:
    return json.loads((REPO_ROOT / "registry" / "architecture-object-coverage-registry.json").read_text(encoding="utf-8"))


def test_clean_workspace_passes() -> None:
    result = validate(WORKSPACE, substrate=REPO_ROOT, include_workspace_validators=False)
    assert result.ok, result.errors


def test_missing_doc_mention_fails(coverage_cfg: dict, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    substrate = tmp_path / "substrate"
    substrate.mkdir()
    (substrate / "registry").mkdir()
    (substrate / "AI_TABLE_OF_CONTENTS.md").write_text("# toc\n", encoding="utf-8")
    (substrate / "AI_WORK_START_HERE.md").write_text("# start\n", encoding="utf-8")
    (substrate / "DATA_FLOW_MAP.md").write_text("# flow\n", encoding="utf-8")
    (substrate / "ENDPOINTS_AND_COMMANDS.md").write_text("# endpoints\n", encoding="utf-8")

    flow = {
        "spine": [
            {"object": "PassageRef", "owning_plane": "legal_knowledge_runtime", "schema_id": "passage-ref-v1"}
        ]
    }
    (substrate / "registry" / "architecture-flow-registry.json").write_text(json.dumps(flow), encoding="utf-8")
    schema_reg = {
        "schemas": [
            {
                "schema_id": "passage-ref-v1",
                "path": "schemas/passage-ref.schema.json",
                "applies_to": ["passage-ref"],
            }
        ]
    }
    (substrate / "registry" / "schema-registry.json").write_text(json.dumps(schema_reg), encoding="utf-8")
    (substrate / "schemas").mkdir()
    (substrate / "schemas" / "passage-ref.schema.json").write_text(
        json.dumps(
            {
                "type": "object",
                "properties": {"schema_version": {"const": "passage_ref.v1"}},
                "required": ["schema_version"],
            }
        ),
        encoding="utf-8",
    )
    lkr_export = {
        "schemas": ["schemas/passage-ref.schema.json"],
        "allowed_runtime_outputs": ["passage-ref"],
    }
    (substrate / "registry" / "legal-knowledge-runtime-contract-export.json").write_text(
        json.dumps(lkr_export), encoding="utf-8"
    )
    (substrate / "registry" / "architecture-object-coverage-registry.json").write_text(
        json.dumps(coverage_cfg), encoding="utf-8"
    )

    result = CoverageResult()
    validate_spine_objects(substrate, coverage_cfg, result)
    assert not result.ok
    assert any("PassageRef" in err for err in result.errors)


def test_forbidden_top_level_schema_property_detected(coverage_cfg: dict, tmp_path: Path) -> None:
    from validate_architecture_object_coverage import validate_forbidden_schema_properties

    substrate = tmp_path / "substrate"
    (substrate / "registry").mkdir(parents=True)
    flow = {"spine": [{"object": "SourceRef", "owning_plane": "legal_knowledge_runtime", "schema_id": "source-ref-v1"}]}
    (substrate / "registry" / "architecture-flow-registry.json").write_text(json.dumps(flow), encoding="utf-8")
    (substrate / "registry" / "schema-registry.json").write_text(
        json.dumps({"schemas": [{"schema_id": "source-ref-v1", "path": "schemas/source-ref.schema.json"}]}),
        encoding="utf-8",
    )
    (substrate / "schemas").mkdir()
    (substrate / "schemas" / "source-ref.schema.json").write_text(
        json.dumps({"properties": {"route_id": {"type": "string"}}, "required": []}),
        encoding="utf-8",
    )
    (substrate / "registry" / "architecture-object-coverage-registry.json").write_text(
        json.dumps(coverage_cfg), encoding="utf-8"
    )
    result = CoverageResult()
    validate_forbidden_schema_properties(substrate, coverage_cfg, result)
    assert any("route_id" in err for err in result.errors)


def test_validator_script_cli_passes() -> None:
    import subprocess

    proc = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_architecture_object_coverage.py"), "--workspace", str(WORKSPACE)],
        cwd=REPO_ROOT,
        text=True,
        capture_output=True,
    )
    assert proc.returncode == 0, proc.stderr or proc.stdout


def test_coverage_report_generated() -> None:
    report_path = REPO_ROOT / "reports" / "architecture_object_coverage_report.json"
    validate(WORKSPACE, substrate=REPO_ROOT, include_workspace_validators=False)
    assert report_path.is_file()
    report = json.loads(report_path.read_text(encoding="utf-8"))
    assert report["ok"] is True
    assert report["objects_checked"]
