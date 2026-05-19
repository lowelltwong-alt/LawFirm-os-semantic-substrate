"""PR-09 architecture object coverage validator.

Ensures governed spine objects stay synchronized across:
  - schema-registry.json
  - architecture-flow-registry.json
  - AI front-door docs (TOC, work-start, data-flow, endpoints)
  - consumer contract exports (where applicable)
  - actionable CLI surfaces (where declared)

Also checks:
  - regulated vocabulary stays in substrate (delegates to validate_runtime_reason_codes)
  - forbidden provider-specific fields do not appear as top-level schema properties
  - SkillTrustRecord export presence
  - model policy ids in orchestrator source match model-policy-registry (when present)

Usage:
    python scripts/validate_architecture_object_coverage.py --workspace ..
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

REPO_ALIASES: dict[str, list[str]] = {
    "LawFirm-os-semantic-substrate": ["LawFirm-os-semantic-substrate"],
    "LawFirm-os-orchestrator": ["LawFirm-os-orchestrator", "LawFirm-os-orchestrator-main"],
    "LawFirm-os-exceptions-lake-runtime": [
        "LawFirm-os-exceptions-lake-runtime",
        "LawFirm-os-exceptions-lake-runtime-main",
    ],
    "LawFirm-os-legal-knowledge-runtime": [
        "LawFirm-os-legal-knowledge-runtime",
        "LawFirm-os-legal-knowledge-runtime-main",
    ],
    "LawFirm-os-skills-registry": ["LawFirm-os-skills-registry", "LawFirm-os-skills-registry-main"],
}

MODEL_POLICY_LITERAL_RE = re.compile(
    r"""(?P<field>model_policy(?:_id)?|policy_id)\s*=\s*["']([^"']+)["']""",
)
CAMEL_BOUNDARY_RE = re.compile(r"(?<=[a-z0-9])(?=[A-Z])")
SCALAR_JSON_TYPES = {"string", "number", "integer", "boolean", "null"}
PROVIDER_METADATA_AUTHORITY_READ_RE = re.compile(
    r"(provider_metadata.*(?:route_id|event_class|admission|trust|approval|model_policy|connector_authority)|"
    r"(?:route_id|event_class|admission|trust|approval|model_policy|connector_authority).*provider_metadata)",
    re.IGNORECASE,
)
PROVIDER_METADATA_VALIDATOR_PATHS = {
    "src/lawfirm_os_skills_registry/domain/trust_surface.py",
    "src/lawfirm_os_skills_registry/domain/skill_trust_record.py",
    "src/lawfirm_os_skills_registry/governance/authority_guard.py",
}
PROVIDER_NAMESPACE_FIELD_EXCEPTIONS = {
    "declared_mcp_servers",
}


@dataclass
class CoverageResult:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    objects_checked: list[dict[str, Any]] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, sort_keys=False) + "\n", encoding="utf-8")


def find_repo(workspace: Path, logical: str) -> Path | None:
    for name in REPO_ALIASES.get(logical, [logical]):
        candidate = workspace / name
        if candidate.is_dir():
            return candidate
    return None


def load_text(path: Path) -> str:
    if not path.is_file():
        return ""
    return path.read_text(encoding="utf-8", errors="replace")


def schema_registry_index(substrate: Path) -> dict[str, dict[str, Any]]:
    reg = read_json(substrate / "registry" / "schema-registry.json")
    index: dict[str, dict[str, Any]] = {}
    for entry in reg.get("schemas", []):
        if isinstance(entry, dict) and entry.get("schema_id"):
            index[str(entry["schema_id"])] = entry
    return index


def schema_keys_from_export(export: dict[str, Any], cfg: dict[str, Any]) -> set[str]:
    keys: set[str] = set()
    if cfg.get("schema_key_field"):
        for item in export.get(cfg["schema_key_field"], []) or []:
            keys.add(str(item))
    if cfg.get("schema_paths_field"):
        for item in export.get(cfg["schema_paths_field"], []) or []:
            name = Path(str(item)).name.replace(".schema.json", "")
            keys.add(name.replace("-", "_") + "-v1" if not name.endswith("-v1") else name)
            # normalize: source-ref.schema.json -> source-ref-v1 via applies_to in registry
    if cfg.get("allowed_outputs_field"):
        for item in export.get(cfg["allowed_outputs_field"], []) or []:
            slug = str(item).replace("_", "-")
            keys.add(slug + "-v1")
    return keys


def export_keys_for_plane(substrate: Path, plane: str, coverage_cfg: dict[str, Any]) -> set[str]:
    export_cfg = coverage_cfg["contract_exports"][plane]
    export_path = substrate / export_cfg["export_path"]
    if not export_path.is_file():
        return set()
    export = read_json(export_path)
    keys = schema_keys_from_export(export, export_cfg)
    if plane == "legal_knowledge_runtime":
        reg_index = schema_registry_index(substrate)
        schema_paths = {str(p) for p in export.get("schemas", []) or []}
        for sid, meta in reg_index.items():
            if str(meta.get("path", "")) in schema_paths:
                keys.add(sid)
    return keys


def doc_bundle_text(substrate: Path, coverage_cfg: dict[str, Any]) -> str:
    parts: list[str] = []
    for rel in coverage_cfg.get("doc_surfaces", []):
        parts.append(load_text(substrate / rel))
    return "\n".join(parts).lower()


def object_mentioned(name: str, aliases: list[str], haystack: str) -> bool:
    tokens = [name.lower(), *[a.lower() for a in aliases]]
    return any(token in haystack for token in tokens)


def validate_spine_objects(substrate: Path, coverage_cfg: dict[str, Any], result: CoverageResult) -> None:
    flow = read_json(substrate / coverage_cfg["architecture_flow_registry_path"])
    reg_index = schema_registry_index(substrate)
    docs = doc_bundle_text(substrate, coverage_cfg)
    aliases_map = coverage_cfg.get("object_doc_aliases", {})

    for entry in flow.get("spine", []):
        if not isinstance(entry, dict):
            continue
        obj_name = str(entry.get("object") or "")
        schema_id = entry.get("schema_id")
        plane = str(entry.get("owning_plane") or "")
        record: dict[str, Any] = {"object": obj_name, "schema_id": schema_id, "owning_plane": plane, "status": "ok"}

        if not schema_id:
            if obj_name != "contract_surface_sha256":
                result.warnings.append(f"{obj_name}: spine entry without schema_id (non-schema object)")
            result.objects_checked.append(record)
            continue

        if schema_id not in reg_index:
            result.errors.append(f"{obj_name}: schema_id {schema_id!r} missing from schema-registry.json")
            record["status"] = "error"
        else:
            schema_path = substrate / reg_index[schema_id]["path"]
            if not schema_path.is_file():
                result.errors.append(f"{obj_name}: schema file missing at {reg_index[schema_id]['path']}")
                record["status"] = "error"

        aliases = aliases_map.get(obj_name, [obj_name])
        if not object_mentioned(obj_name, aliases, docs):
            result.errors.append(
                f"{obj_name}: not mentioned in PR-09 doc surfaces ({', '.join(coverage_cfg['doc_surfaces'])})"
            )
            record["status"] = "error"

        if plane and plane in coverage_cfg.get("contract_exports", {}):
            export_keys = export_keys_for_plane(substrate, plane, coverage_cfg)
            if schema_id not in export_keys:
                # Also accept hyphen slug in allowed outputs / draft keys
                slug = schema_id.replace("-v1", "").replace("-", "_")
                if schema_id not in export_keys and not any(schema_id.split("-")[0] in k for k in export_keys):
                    result.errors.append(
                        f"{obj_name}: {schema_id} not referenced by contract export for plane {plane}"
                    )
                    record["status"] = "error"

        result.objects_checked.append(record)


def validate_actionable_commands(workspace: Path, substrate: Path, coverage_cfg: dict[str, Any], result: CoverageResult) -> None:
    endpoints = load_text(substrate / "ENDPOINTS_AND_COMMANDS.md").lower()
    for cmd in coverage_cfg.get("actionable_commands", []):
        repo = find_repo(workspace, str(cmd["repo"]))
        if repo is None:
            result.warnings.append(f"actionable command {cmd['command_id']}: repo {cmd['repo']} not found in workspace")
            continue
        for token in cmd.get("tokens", []):
            if str(token).lower() not in endpoints:
                result.errors.append(
                    f"actionable command {cmd['command_id']}: token {token!r} missing from ENDPOINTS_AND_COMMANDS.md"
                )


def _schema_tokens(value: str) -> set[str]:
    with_boundaries = CAMEL_BOUNDARY_RE.sub("_", value)
    return {token for token in re.split(r"[^A-Za-z0-9]+", with_boundaries.lower()) if token}


def _contains_namespace(value: str, namespaces: set[str]) -> bool:
    if value.lower() in PROVIDER_NAMESPACE_FIELD_EXCEPTIONS:
        return False
    tokens = _schema_tokens(value)
    return any(token == namespace or token.startswith(namespace) for token in tokens for namespace in namespaces)


def _is_authority_name(value: str, authority_names: set[str]) -> bool:
    normalized = value.lower()
    if normalized in authority_names:
        return True
    return normalized.replace("-", "_") in authority_names


def _is_provider_metadata_path(path: tuple[str, ...]) -> bool:
    return "provider_metadata" in path


def _location(path: tuple[str, ...]) -> str:
    return ".".join(path) if path else "<schema>"


def _additional_properties_scalar(additional: Any) -> bool:
    if additional is False:
        return True
    if not isinstance(additional, dict):
        return False
    typ = additional.get("type")
    if isinstance(typ, str):
        return typ in SCALAR_JSON_TYPES
    if isinstance(typ, list):
        return set(typ).issubset(SCALAR_JSON_TYPES)
    return False


def _validate_provider_metadata_schema(schema: dict[str, Any], schema_id: str, path: tuple[str, ...], result: CoverageResult) -> None:
    if schema.get("type") != "object":
        result.errors.append(f"{schema_id}: provider_metadata at {_location(path)} must be an object")
    max_props = schema.get("maxProperties")
    if not isinstance(max_props, int) or max_props > 16:
        result.errors.append(f"{schema_id}: provider_metadata at {_location(path)} must set maxProperties <= 16")
    if not _additional_properties_scalar(schema.get("additionalProperties")):
        result.errors.append(
            f"{schema_id}: provider_metadata at {_location(path)} must allow only scalar opaque values"
        )
    if "propertyNames" not in schema:
        result.errors.append(f"{schema_id}: provider_metadata at {_location(path)} must constrain property names")


def _check_schema_string(
    *,
    schema_id: str,
    value: str,
    path: tuple[str, ...],
    result: CoverageResult,
    provider_namespaces: set[str],
    authority_names: set[str],
    metadata_authority_names: set[str],
) -> None:
    in_provider_metadata = _is_provider_metadata_path(path)
    forbidden_names = authority_names | (metadata_authority_names if in_provider_metadata else set())
    if _is_authority_name(value, forbidden_names):
        result.errors.append(f"{schema_id}: forbidden authority name {value!r} at {_location(path)}")
    if not in_provider_metadata and _contains_namespace(value, provider_namespaces):
        result.errors.append(f"{schema_id}: forbidden provider namespace {value!r} at {_location(path)}")


def _walk_schema_forbidden(
    *,
    schema_id: str,
    node: Any,
    path: tuple[str, ...],
    result: CoverageResult,
    provider_namespaces: set[str],
    authority_names: set[str],
    metadata_authority_names: set[str],
) -> None:
    if "propertyNames" in path:
        return
    if isinstance(node, dict):
        if path and path[-1] == "provider_metadata":
            _validate_provider_metadata_schema(node, schema_id, path, result)
        properties = node.get("properties")
        if isinstance(properties, dict):
            for prop_name, child in properties.items():
                prop_path = path + (str(prop_name),)
                if prop_name != "provider_metadata":
                    _check_schema_string(
                        schema_id=schema_id,
                        value=str(prop_name),
                        path=prop_path,
                        result=result,
                        provider_namespaces=provider_namespaces,
                        authority_names=authority_names,
                        metadata_authority_names=metadata_authority_names,
                    )
                _walk_schema_forbidden(
                    schema_id=schema_id,
                    node=child,
                    path=prop_path,
                    result=result,
                    provider_namespaces=provider_namespaces,
                    authority_names=authority_names,
                    metadata_authority_names=metadata_authority_names,
                )
        pattern_props = node.get("patternProperties")
        if isinstance(pattern_props, dict):
            for prop_name, child in pattern_props.items():
                prop_path = path + (f"patternProperties[{prop_name}]",)
                _check_schema_string(
                    schema_id=schema_id,
                    value=str(prop_name),
                    path=prop_path,
                    result=result,
                    provider_namespaces=provider_namespaces,
                    authority_names=authority_names,
                    metadata_authority_names=metadata_authority_names,
                )
                _walk_schema_forbidden(
                    schema_id=schema_id,
                    node=child,
                    path=prop_path,
                    result=result,
                    provider_namespaces=provider_namespaces,
                    authority_names=authority_names,
                    metadata_authority_names=metadata_authority_names,
                )
        required = node.get("required")
        if isinstance(required, list):
            for item in required:
                if isinstance(item, str) and item != "provider_metadata":
                    _check_schema_string(
                        schema_id=schema_id,
                        value=item,
                        path=path + ("required", item),
                        result=result,
                        provider_namespaces=provider_namespaces,
                        authority_names=authority_names,
                        metadata_authority_names=metadata_authority_names,
                    )
        enum = node.get("enum")
        if isinstance(enum, list):
            for item in enum:
                if isinstance(item, str):
                    _check_schema_string(
                        schema_id=schema_id,
                        value=item,
                        path=path + ("enum",),
                        result=result,
                        provider_namespaces=provider_namespaces,
                        authority_names=authority_names,
                        metadata_authority_names=metadata_authority_names,
                    )
        const = node.get("const")
        if isinstance(const, str):
            _check_schema_string(
                schema_id=schema_id,
                value=const,
                path=path + ("const",),
                result=result,
                provider_namespaces=provider_namespaces,
                authority_names=authority_names,
                metadata_authority_names=metadata_authority_names,
            )
        for key in ("items", "additionalProperties", "propertyNames", "contains", "not", "if", "then", "else"):
            if key in node:
                _walk_schema_forbidden(
                    schema_id=schema_id,
                    node=node[key],
                    path=path + (key,),
                    result=result,
                    provider_namespaces=provider_namespaces,
                    authority_names=authority_names,
                    metadata_authority_names=metadata_authority_names,
                )
        for key in ("anyOf", "allOf", "oneOf", "prefixItems"):
            values = node.get(key)
            if isinstance(values, list):
                for index, child in enumerate(values):
                    _walk_schema_forbidden(
                        schema_id=schema_id,
                        node=child,
                        path=path + (f"{key}[{index}]",),
                    result=result,
                    provider_namespaces=provider_namespaces,
                    authority_names=authority_names,
                    metadata_authority_names=metadata_authority_names,
                )
    elif isinstance(node, list):
        for index, child in enumerate(node):
            _walk_schema_forbidden(
                schema_id=schema_id,
                node=child,
                path=path + (f"[{index}]",),
                result=result,
                provider_namespaces=provider_namespaces,
                authority_names=authority_names,
                metadata_authority_names=metadata_authority_names,
            )


def validate_forbidden_schema_properties(substrate: Path, coverage_cfg: dict[str, Any], result: CoverageResult) -> None:
    provider_namespaces = {str(v).lower() for v in coverage_cfg.get("forbidden_provider_namespaces", [])}
    authority_names = {str(v).lower() for v in coverage_cfg.get("forbidden_top_level_schema_properties", [])}
    metadata_authority_names = {str(v).lower() for v in coverage_cfg.get("forbidden_authority_field_names", [])}
    reg_index = schema_registry_index(substrate)
    spine_ids = {
        str(e.get("schema_id"))
        for e in read_json(substrate / coverage_cfg["architecture_flow_registry_path"]).get("spine", [])
        if e.get("schema_id")
    }
    for schema_id in spine_ids:
        meta = reg_index.get(schema_id)
        if not meta:
            continue
        schema = read_json(substrate / meta["path"])
        _walk_schema_forbidden(
            schema_id=schema_id,
            node=schema,
            path=(),
            result=result,
            provider_namespaces=provider_namespaces,
            authority_names=authority_names,
            metadata_authority_names=metadata_authority_names,
        )


def validate_trust_governance(substrate: Path, coverage_cfg: dict[str, Any], result: CoverageResult) -> None:
    trust = coverage_cfg.get("trust_governance") or {}
    schema_id = trust.get("skill_trust_schema_id")
    export_path = substrate / str(trust.get("required_schema_export", ""))
    if not export_path.is_file():
        result.errors.append("trust governance: required schema export missing")
        return
    export = read_json(export_path)
    keys = set(export.get("draft_schema_keys", []) or [])
    if schema_id not in keys:
        result.errors.append(f"trust governance: {schema_id} missing from {export_path.name}")


def validate_model_policy_literals(workspace: Path, substrate: Path, coverage_cfg: dict[str, Any], result: CoverageResult) -> None:
    registry_path = substrate / str(coverage_cfg.get("model_policy_registry_path", ""))
    if not registry_path.is_file():
        return
    registry = read_json(registry_path)
    allowed = {p["policy_id"] for p in registry.get("policies", []) if isinstance(p, dict) and p.get("policy_id")}
    orchestrator = find_repo(workspace, "LawFirm-os-orchestrator")
    if orchestrator is None:
        return
    src_root = orchestrator / "src"
    if not src_root.is_dir():
        return
    for py_file in src_root.rglob("*.py"):
        text = py_file.read_text(encoding="utf-8", errors="replace")
        for match in MODEL_POLICY_LITERAL_RE.finditer(text):
            policy_id = match.group(2)
            if policy_id not in allowed:
                result.errors.append(
                    f"model policy: {py_file.relative_to(orchestrator)} uses unregistered policy_id {policy_id!r}"
                )


def validate_provider_metadata_authority_reads(workspace: Path, result: CoverageResult) -> None:
    """Prevent runtime authority paths from treating provider_metadata as authority."""
    for logical in REPO_ALIASES:
        repo = find_repo(workspace, logical)
        if repo is None:
            continue
        src_root = repo / "src"
        if not src_root.is_dir():
            continue
        for py_file in src_root.rglob("*.py"):
            rel = py_file.relative_to(repo).as_posix()
            if rel in PROVIDER_METADATA_VALIDATOR_PATHS:
                continue
            text = py_file.read_text(encoding="utf-8", errors="replace")
            for line_number, line in enumerate(text.splitlines(), start=1):
                if PROVIDER_METADATA_AUTHORITY_READ_RE.search(line):
                    result.errors.append(
                        f"provider_metadata authority read: {repo.name}/{rel}:{line_number} must not use provider_metadata for routing, admission, trust, approval, model-policy, or connector authority"
                    )


def validate_runtime_reason_codes(workspace: Path, substrate: Path) -> list[str]:
    script = substrate / "scripts" / "validate_runtime_reason_codes.py"
    if not script.is_file():
        return ["missing validate_runtime_reason_codes.py"]
    proc = subprocess.run(
        [sys.executable, str(script), "--workspace", str(workspace)],
        cwd=substrate,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return [proc.stdout.strip() or proc.stderr.strip() or "runtime reason-code validation failed"]
    return []


def validate_lock_drift(workspace: Path, substrate: Path) -> list[str]:
    script = substrate / "scripts" / "validate_contract_lock_drift_workspace.py"
    if not script.is_file():
        return ["missing validate_contract_lock_drift_workspace.py"]
    proc = subprocess.run(
        [sys.executable, str(script), "--workspace", str(workspace)],
        cwd=substrate,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0:
        return [proc.stdout.strip() or proc.stderr.strip() or "contract lock drift validation failed"]
    return []


def validate(
    workspace: Path,
    *,
    substrate: Path | None = None,
    include_workspace_validators: bool = True,
) -> CoverageResult:
    substrate = substrate or find_repo(workspace, "LawFirm-os-semantic-substrate")
    if substrate is None:
        result = CoverageResult()
        result.errors.append("LawFirm-os-semantic-substrate not found in workspace")
        return result

    coverage_cfg_path = substrate / "registry" / "architecture-object-coverage-registry.json"
    if not coverage_cfg_path.is_file():
        result = CoverageResult()
        result.errors.append("missing registry/architecture-object-coverage-registry.json")
        return result

    coverage_cfg = read_json(coverage_cfg_path)
    result = CoverageResult()

    validate_spine_objects(substrate, coverage_cfg, result)
    validate_actionable_commands(workspace, substrate, coverage_cfg, result)
    validate_forbidden_schema_properties(substrate, coverage_cfg, result)
    validate_trust_governance(substrate, coverage_cfg, result)
    validate_model_policy_literals(workspace, substrate, coverage_cfg, result)
    validate_provider_metadata_authority_reads(workspace, result)

    if include_workspace_validators:
        result.errors.extend(validate_runtime_reason_codes(workspace, substrate))
        result.errors.extend(validate_lock_drift(workspace, substrate))

    report = {
        "schema_version": "architecture_object_coverage_report.v1",
        "workspace": str(workspace.resolve()),
        "substrate_root": str(substrate.resolve()),
        "ok": result.ok,
        "error_count": len(result.errors),
        "warning_count": len(result.warnings),
        "errors": result.errors,
        "warnings": result.warnings,
        "objects_checked": result.objects_checked,
    }
    report_path = substrate / coverage_cfg.get("report_output_path", "reports/architecture_object_coverage_report.json")
    write_json(report_path, report)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate architecture object coverage across the OS spine.")
    parser.add_argument("--workspace", default=".", help="Workspace root containing LawFirm OS repos")
    parser.add_argument("--substrate", default=None, help="Optional explicit substrate path")
    parser.add_argument(
        "--skip-workspace-validators",
        action="store_true",
        help="Only run coverage checks (skip reason-code and lock drift subprocesses)",
    )
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    substrate = Path(args.substrate).resolve() if args.substrate else None
    result = validate(
        workspace,
        substrate=substrate,
        include_workspace_validators=not args.skip_workspace_validators,
    )
    if result.warnings:
        for warning in result.warnings:
            print(f"WARNING: {warning}")
    if result.errors:
        for error in result.errors:
            print(f"ERROR: {error}")
        print(f"architecture object coverage validation failed ({len(result.errors)} error(s)).")
        return 1
    print("architecture object coverage validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
