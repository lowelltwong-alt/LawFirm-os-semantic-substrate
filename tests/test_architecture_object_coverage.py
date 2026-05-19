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


def _run_forbidden_schema_case(coverage_cfg: dict, tmp_path: Path, schema: dict) -> CoverageResult:
    from validate_architecture_object_coverage import validate_forbidden_schema_properties

    substrate = tmp_path / "substrate"
    (substrate / "registry").mkdir(parents=True)
    (substrate / "schemas").mkdir()
    (substrate / "registry" / "architecture-flow-registry.json").write_text(
        json.dumps(
            {
                "spine": [
                    {
                        "object": "SourceRef",
                        "owning_plane": "legal_knowledge_runtime",
                        "schema_id": "source-ref-v1",
                    }
                ]
            }
        ),
        encoding="utf-8",
    )
    (substrate / "registry" / "schema-registry.json").write_text(
        json.dumps({"schemas": [{"schema_id": "source-ref-v1", "path": "schemas/source-ref.schema.json"}]}),
        encoding="utf-8",
    )
    (substrate / "schemas" / "source-ref.schema.json").write_text(json.dumps(schema), encoding="utf-8")
    result = CoverageResult()
    validate_forbidden_schema_properties(substrate, coverage_cfg, result)
    return result


@pytest.mark.parametrize(
    "property_name",
    [
        "claude_plugin_id",
        "Claude_Plugin_Id",
        "claudePluginId",
        "claude_plugin_ids",
        "mcp_server_id",
        "mcp_tool_id",
    ],
)
def test_recursive_provider_property_leakage_detected(coverage_cfg: dict, tmp_path: Path, property_name: str) -> None:
    schema = {
        "type": "object",
        "properties": {
            "outer": {
                "type": "object",
                "properties": {
                    property_name: {"type": "string"},
                },
            }
        },
    }
    result = _run_forbidden_schema_case(coverage_cfg, tmp_path, schema)
    assert not result.ok
    assert any(property_name in err for err in result.errors)


def test_recursive_provider_enum_const_array_and_combinator_leakage_detected(
    coverage_cfg: dict, tmp_path: Path
) -> None:
    schema = {
        "type": "object",
        "properties": {
            "records": {
                "type": "array",
                "items": {
                    "anyOf": [
                        {"type": "object", "properties": {"safe": {"const": "claude_plugin_fixture"}}},
                        {"type": "object", "properties": {"mode": {"enum": ["mock", "mcp_tool_fixture"]}}},
                    ]
                },
            }
        },
    }
    result = _run_forbidden_schema_case(coverage_cfg, tmp_path, schema)
    assert not result.ok
    joined = "\n".join(result.errors)
    assert "claude_plugin_fixture" in joined
    assert "mcp_tool_fixture" in joined


def test_provider_metadata_allowed_only_when_bounded_and_non_authoritative(
    coverage_cfg: dict, tmp_path: Path
) -> None:
    schema = {
        "type": "object",
        "properties": {
            "provider_metadata": {
                "type": "object",
                "maxProperties": 16,
                "propertyNames": {"pattern": "^[A-Za-z0-9_.:-]{1,80}$"},
                "additionalProperties": {"type": ["string", "number", "integer", "boolean", "null"]},
            }
        },
    }
    result = _run_forbidden_schema_case(coverage_cfg, tmp_path, schema)
    assert result.ok, result.errors


def test_provider_metadata_authority_keys_and_unbounded_values_fail(
    coverage_cfg: dict, tmp_path: Path
) -> None:
    schema = {
        "type": "object",
        "properties": {
            "provider_metadata": {
                "type": "object",
                "additionalProperties": True,
                "properties": {"route_id": {"type": "string"}},
            }
        },
    }
    result = _run_forbidden_schema_case(coverage_cfg, tmp_path, schema)
    assert not result.ok
    joined = "\n".join(result.errors)
    assert "provider_metadata" in joined
    assert "route_id" in joined


def test_provider_metadata_authority_path_read_fails(tmp_path: Path) -> None:
    from validate_architecture_object_coverage import validate_provider_metadata_authority_reads

    workspace = tmp_path / "workspace"
    target = workspace / "LawFirm-os-orchestrator" / "src" / "lawfirm_os_orchestrator" / "model_router"
    target.mkdir(parents=True)
    (target / "router.py").write_text(
        "def route(packet):\n"
        "    return packet.get('provider_metadata', {}).get('route_id')\n",
        encoding="utf-8",
    )
    result = CoverageResult()
    validate_provider_metadata_authority_reads(workspace, result)
    assert not result.ok
    assert "provider_metadata authority read" in result.errors[0]


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
