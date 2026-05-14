#!/usr/bin/env python3
"""Fail-closed integrity gate for AI TOC / AI front door / workflow atlas surfaces."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REQUIRED_ENDPOINT_FIELDS = (
    "id",
    "owning_repo",
    "owning_plane",
    "path",
    "purpose",
    "side_effect_class",
    "input_schema",
    "output_schema",
    "human_approval_required",
    "stores_raw_legal_payload",
    "allowed_data_classes",
    "related_docs",
)
OWNING_PLANES = {
    "semantic_substrate",
    "orchestrator",
    "exception_lake",
    "skills_registry",
    "legal_knowledge_runtime",
}
SIDE_EFFECTS = {"none", "read", "write", "external"}


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _substrate_root(explicit: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    return Path(__file__).resolve().parents[1]


def _workspace(substrate_root: Path) -> Path:
    return substrate_root.parent


def _sibling(substrate_root: Path, fd: dict[str, Any], key: str) -> Path:
    name = fd["sibling_repo_folder_names"][key]
    return _workspace(substrate_root) / name


def validate_ai_front_door(substrate_root: Path | None = None) -> list[str]:
    errors: list[str] = []
    root = _substrate_root(substrate_root)
    fd_path = root / "registry" / "ai-front-door-registry.json"
    if not fd_path.exists():
        return [f"missing {fd_path}"]
    fd = _read_json(fd_path)

    for sub in fd.get("toc_required_substrings", []):
        for toc_name in fd.get("toc_files_must_reference_registry", []):
            toc = root / toc_name
            if not toc.exists():
                errors.append(f"missing TOC file {toc}")
                continue
            text = toc.read_text(encoding="utf-8")
            if sub not in text:
                errors.append(f"{toc_name} missing required substring {sub!r}")

    for rel in fd.get("canonical_read_order", []):
        p = root / rel
        if not p.exists():
            errors.append(f"canonical_read_order path missing: {rel}")

    schema_reg = _read_json(root / "registry" / "schema-registry.json")
    reg_paths = {Path(e["path"]).as_posix() for e in schema_reg.get("schemas", []) if isinstance(e, dict)}

    exclusions_path = root / "registry" / "schema-surface-exclusions.json"
    if not exclusions_path.exists():
        errors.append("missing registry/schema-surface-exclusions.json")
        excl: dict[str, Any] = {}
    else:
        excl = _read_json(exclusions_path)
        if not isinstance(excl, dict):
            errors.append("schema-surface-exclusions.json must be a JSON object mapping schema paths to metadata")

    for schema_file in sorted(root.joinpath("schemas").rglob("*.json")):
        rel = schema_file.relative_to(root).as_posix()
        if rel in reg_paths:
            continue
        meta = excl.get(rel) if isinstance(excl, dict) else None
        if not isinstance(meta, dict):
            errors.append(f"schema {rel} not in schema-registry.json and not in schema-surface-exclusions.json")
            continue
        for k in ("governance_doc", "governance_reason", "exclusion_class"):
            if not meta.get(k):
                errors.append(f"schema exclusion for {rel} missing {k}")

    reg_manifest = root / "registry" / "registry-full-manifest.json"
    if not reg_manifest.exists():
        errors.append("missing registry/registry-full-manifest.json")
    else:
        declared = {_normalize_reg_path(p) for p in _read_json(reg_manifest).get("paths", [])}
        actual = {"registry/" + p.name for p in (root / "registry").glob("*.json")}
        if declared != actual:
            missing = sorted(actual - declared)
            extra = sorted(declared - actual)
            if missing:
                errors.append(f"registry-full-manifest missing entries: {missing[:10]}{'...' if len(missing)>10 else ''}")
            if extra:
                errors.append(f"registry-full-manifest stale entries: {extra[:10]}{'...' if len(extra)>10 else ''}")

    gov_manifest = root / "registry" / "governance-full-manifest.json"
    if not gov_manifest.exists():
        errors.append("missing registry/governance-full-manifest.json")
    else:
        declared_g = set(_read_json(gov_manifest).get("paths", []))
        actual_g = sorted(p.relative_to(root).as_posix() for p in (root / "governance").rglob("*.md"))
        if set(actual_g) != declared_g:
            errors.append("governance-full-manifest.json is out of sync with governance/**/*.md; regenerate it")

    ws = _workspace(root)
    folder_map = fd["sibling_repo_folder_names"]
    for anchor in fd.get("integration_path_anchors", []):
        repo = anchor["repo"]
        rel = anchor["path"]
        if repo == "semantic_substrate":
            base = root
        elif repo == "orchestrator":
            base = ws / folder_map["orchestrator"]
        elif repo == "legal_knowledge_runtime":
            base = ws / folder_map["legal_knowledge_runtime"]
        elif repo == "exception_lake":
            base = ws / folder_map["exception_lake"]
        elif repo == "skills_registry":
            base = ws / folder_map["skills_registry"]
        else:
            errors.append(f"unknown repo key in integration_path_anchors: {repo}")
            continue
        if not (base / rel).exists():
            errors.append(f"integration anchor missing file: {repo}:{rel}")

    for ep in fd.get("endpoints", []):
        for field in REQUIRED_ENDPOINT_FIELDS:
            if field not in ep:
                errors.append(f"endpoint {ep.get('id')} missing field {field}")
        if ep.get("stores_raw_legal_payload") is not False:
            errors.append(f"endpoint {ep.get('id')} must set stores_raw_legal_payload=false")
        if ep.get("side_effect_class") not in SIDE_EFFECTS:
            errors.append(f"endpoint {ep.get('id')} has invalid side_effect_class")
        if ep.get("owning_plane") not in OWNING_PLANES:
            errors.append(f"endpoint {ep.get('id')} has invalid owning_plane")
        if not isinstance(ep.get("allowed_data_classes"), list) or not ep["allowed_data_classes"]:
            errors.append(f"endpoint {ep.get('id')} must include non-empty allowed_data_classes")
        if not isinstance(ep.get("related_docs"), list) or not ep["related_docs"]:
            errors.append(f"endpoint {ep.get('id')} must include non-empty related_docs")
        for doc in ep.get("related_docs", []):
            if doc.startswith("governance/"):
                if not (root / doc).exists():
                    errors.append(f"endpoint {ep.get('id')} related_docs missing on substrate: {doc}")
            elif doc.startswith("docs/"):
                orch = ws / folder_map["orchestrator"]
                if not (orch / doc).exists():
                    errors.append(f"endpoint {ep.get('id')} related_docs missing on orchestrator: {doc}")
            else:
                errors.append(f"endpoint {ep.get('id')} related_docs must start with governance/ or docs/: {doc}")

    skills_root = ws / folder_map["skills_registry"]
    index_path = skills_root / fd.get("draft_skill_index", "registry/proposed-draft-skill-index.json")
    if not index_path.exists():
        errors.append(f"missing skills draft index {index_path}")
    else:
        dex = _read_json(index_path)
        declared_ids = {e["skill_id"] for e in dex.get("skills", []) if isinstance(e, dict)}
        for entry in dex.get("skills", []):
            if not isinstance(entry, dict):
                continue
            rel = entry.get("source_path")
            sid = entry.get("skill_id")
            if not rel or not sid:
                errors.append("draft skill index entry missing source_path or skill_id")
                continue
            skill_md = skills_root / rel / "SKILL.md"
            if not skill_md.exists():
                errors.append(f"draft skill index points to missing SKILL.md: {rel}")
        for skill_dir in (skills_root / "skills" / "draft").iterdir():
            if not skill_dir.is_dir():
                continue
            if skill_dir.name.startswith("."):
                continue
            sid = skill_dir.name
            if sid not in declared_ids:
                errors.append(f"draft skill folder {sid} not listed in {index_path.relative_to(skills_root)}")

    for ev in fd.get("event_examples", []):
        base = ws / folder_map["exception_lake"]
        rel = ev["path"]
        if not (base / rel).exists():
            errors.append(f"event example missing: {rel}")

    return errors


def _normalize_reg_path(p: str) -> str:
    return p.replace("\\", "/")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--substrate-root", type=Path, default=None)
    args = parser.parse_args(argv)
    errors = validate_ai_front_door(args.substrate_root)
    if errors:
        print("AI front door validation failed:", file=sys.stderr)
        for err in errors:
            print(f"- {err}", file=sys.stderr)
        return 1
    print("AI front door validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
