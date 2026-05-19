from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]

SCHEMA_PATHS = [
    "schemas/agent-identity.schema.json",
    "schemas/prompt-version.schema.json",
    "schemas/tool-authority.schema.json",
    "schemas/endpoint-authority.schema.json",
    "schemas/revocation-policy.schema.json",
    "schemas/agent-hostile-control-bundle.schema.json",
]

REGISTRY_PATHS = [
    "registry/prompt-registry.json",
    "registry/tool-authority-registry.json",
    "registry/endpoint-authority-registry.json",
    "registry/agent-hostile-control-registry.json",
    "registry/agent-control-contract-export.json",
]


def _json(rel: str) -> Any:
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


def _schema_ids() -> set[str]:
    return {entry["schema_id"] for entry in _json("registry/schema-registry.json")["schemas"]}


def test_agent_hostile_schemas_are_valid_json_schema() -> None:
    for rel in SCHEMA_PATHS:
        Draft202012Validator.check_schema(_json(rel))


def test_agent_hostile_registries_are_valid_json() -> None:
    for rel in REGISTRY_PATHS:
        assert isinstance(_json(rel), dict)


def test_registries_reference_existing_schema_ids() -> None:
    schema_ids = _schema_ids()
    assert {
        "agent-identity-v1",
        "prompt-version-v1",
        "tool-authority-v1",
        "endpoint-authority-v1",
        "revocation-policy-v1",
        "agent-hostile-control-bundle-v1",
    } <= schema_ids

    assert _json("registry/prompt-registry.json")["schema_ref"] in schema_ids
    assert _json("registry/tool-authority-registry.json")["schema_ref"] in schema_ids
    assert _json("registry/endpoint-authority-registry.json")["schema_ref"] in schema_ids

    bundle = _json("registry/agent-hostile-control-registry.json")
    assert set(bundle["schema_refs"]) <= schema_ids


def test_registry_examples_validate_against_declared_schemas() -> None:
    prompt_schema = _json("schemas/prompt-version.schema.json")
    tool_schema = _json("schemas/tool-authority.schema.json")
    endpoint_schema = _json("schemas/endpoint-authority.schema.json")
    bundle_schema = _json("schemas/agent-hostile-control-bundle.schema.json")

    for prompt in _json("registry/prompt-registry.json")["prompts"]:
        Draft202012Validator(prompt_schema).validate(prompt)
    for tool in _json("registry/tool-authority-registry.json")["tools"]:
        Draft202012Validator(tool_schema).validate(tool)
    for endpoint in _json("registry/endpoint-authority-registry.json")["endpoints"]:
        Draft202012Validator(endpoint_schema).validate(endpoint)
    Draft202012Validator(bundle_schema).validate(_json("registry/agent-hostile-control-registry.json"))


def test_agent_hostile_control_registry_is_discoverable() -> None:
    source = _json("registry/source-of-truth.json")
    manifest = _json("manifests/contract_manifest.v1.json")
    registry_manifest = _json("registry/registry-full-manifest.json")

    assert source["authoritative_files"]["agent_hostile_control_registry"] == "registry/agent-hostile-control-registry.json"
    assert "registry/agent-hostile-control-registry.json" in manifest["registry_refs"]
    assert "registry/agent-hostile-control-registry.json" in registry_manifest["paths"]
    assert "governance/AGENT_HOSTILE_CONTROL_BOUNDARY.md" in manifest["governance_refs"]


def test_registry_examples_do_not_contain_real_data_or_secret_looking_values() -> None:
    examples = {
        "prompts": _json("registry/prompt-registry.json")["prompts"],
        "tools": _json("registry/tool-authority-registry.json")["tools"],
        "endpoints": _json("registry/endpoint-authority-registry.json")["endpoints"],
    }
    forbidden = (
        "api_key",
        "apikey",
        "bearer ",
        "client:",
        "credential",
        "matter:",
        "password",
        "prod_",
        "secret",
        "token",
    )
    rendered = json.dumps(examples, sort_keys=True).lower()
    assert all(term not in rendered for term in forbidden)
    assert "synthetic" in rendered


def test_agent_control_contract_export_includes_new_surfaces() -> None:
    export = _json("registry/agent-control-contract-export.json")
    assert set(SCHEMA_PATHS) <= set(export["schema_paths"])
    assert {
        "registry/prompt-registry.json",
        "registry/tool-authority-registry.json",
        "registry/endpoint-authority-registry.json",
        "registry/agent-hostile-control-registry.json",
    } <= set(export["registry_paths"])
    assert "governance/AGENT_HOSTILE_CONTROL_BOUNDARY.md" in export["governance_paths"]
