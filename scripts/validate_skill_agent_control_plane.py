from __future__ import annotations

import argparse
import fnmatch
import json
import sys
from pathlib import Path

FRONT_DOOR_POINTERS = [
    "ai-front-door",
    "ai_front_door",
    "AI_FRONT_DOOR",
    "LawFirm-os-semantic-substrate",
    "skill-agent-manifest",
]

REQUIRED_ROOT_FILES = ["README.md", "AGENTS.md", "AI_WORK_START_HERE.md", "skill-agent-manifest.json"]


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def is_patch_or_artifact_dir(path: Path, exclusions: list[dict]) -> bool:
    name = path.name
    for ex in exclusions:
        pat = ex.get("pattern", "")
        if fnmatch.fnmatch(name, pat):
            return True
    lowered = name.lower()
    return "seed-pack" in lowered or "patch" in lowered or lowered.endswith(".zip")


def discover_repos(workspace: Path, exclusions: list[dict]) -> list[Path]:
    repos = []
    for p in workspace.iterdir():
        if not p.is_dir():
            continue
        if not p.name.startswith("LawFirm-os-"):
            continue
        if is_patch_or_artifact_dir(p, exclusions):
            continue
        repos.append(p)
    return sorted(repos, key=lambda x: x.name.lower())


def has_front_door_pointer(path: Path) -> bool:
    text = path.read_text(encoding="utf-8", errors="ignore")
    return any(token in text for token in FRONT_DOOR_POINTERS)


def is_non_canonical_skill_or_agent_tree(path: Path) -> bool:
    """Fixture trees, patch bundles, and vendored repo snapshots are not governed skills."""
    lowered = {p.lower() for p in path.parts}
    if any(part.startswith("tmp_pytest") for part in lowered):
        return True
    if any(part in {".pytest_cache", "__pycache__", ".mypy_cache", ".ruff_cache"} for part in lowered):
        return True
    if "_patches" in lowered:
        return True
    if "repo-additions" in lowered:
        return True
    if "external_skills" in lowered:
        return True
    if ".git" in lowered:
        return True
    return False


def validate_skill_metadata_file(path: Path, errors: list[str]):
    try:
        data = load_json(path)
    except Exception as exc:
        errors.append(f"invalid skill metadata json: {path}: {exc}")
        return
    required = ["id","kind","owning_repo","owning_plane","address","version","lifecycle_state","quality_score_ref","graph_node_ref","recommended_update_policy"]
    for key in required:
        if key not in data:
            errors.append(f"skill metadata missing {key}: {path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate LawFirm OS Skill-Agent Control Plane compliance across a workspace.")
    parser.add_argument("--workspace", type=Path, default=Path.cwd().parent)
    parser.add_argument("--substrate", type=Path, default=None)
    parser.add_argument("--strict", action="store_true", default=True)
    args = parser.parse_args()

    workspace = args.workspace.resolve()
    substrate = args.substrate.resolve() if args.substrate else workspace / "LawFirm-os-semantic-substrate"
    if not substrate.exists():
        # tolerate -main fallback
        candidates = [p for p in workspace.iterdir() if p.is_dir() and p.name.startswith("LawFirm-os-semantic-substrate")]
        substrate = candidates[0] if len(candidates) == 1 else substrate

    errors: list[str] = []
    repo_registry_path = substrate / "registry" / "lawfirm-os-repo-registry.json"
    if not repo_registry_path.exists():
        print(f"FAIL missing repo registry: {repo_registry_path}")
        return 1
    repo_registry = load_json(repo_registry_path)
    exclusions = repo_registry.get("explicit_exclusions", [])
    registered = {r["repo_name"]: r for r in repo_registry.get("repos", []) if r.get("status") != "excluded"}
    discovered = discover_repos(workspace, exclusions)

    for repo in discovered:
        if repo.name not in registered and repo.name.removesuffix("-main") not in registered:
            errors.append(f"unregistered LawFirm OS repo discovered: {repo.name}")

    for repo_name, record in registered.items():
        repo = workspace / repo_name
        if not repo.exists():
            fallback = workspace / f"{repo_name}-main"
            repo = fallback if fallback.exists() else repo
        if not repo.exists():
            errors.append(f"registered repo missing from workspace: {repo_name}")
            continue
        for root_file in record.get("required_root_files", REQUIRED_ROOT_FILES):
            fp = repo / root_file
            if not fp.exists():
                errors.append(f"{repo.name} missing required root file: {root_file}")
            elif root_file in {"README.md","AGENTS.md","AI_WORK_START_HERE.md"} and not has_front_door_pointer(fp):
                errors.append(f"{repo.name}/{root_file} lacks AI front-door / skill-agent bootstrap pointer")
        manifest_path = repo / record.get("skill_agent_manifest_path", "skill-agent-manifest.json")
        if manifest_path.exists():
            try:
                manifest = load_json(manifest_path)
            except Exception as exc:
                errors.append(f"invalid skill-agent manifest: {manifest_path}: {exc}")
                continue
            if manifest.get("owning_repo") not in {repo.name, repo_name}:
                errors.append(f"{manifest_path} owning_repo mismatch")
            if "artifacts" not in manifest:
                errors.append(f"{manifest_path} missing artifacts list")

    # Check skills and agents metadata coverage.
    for repo in discovered:
        for skill_md in repo.rglob("SKILL.md"):
            if is_non_canonical_skill_or_agent_tree(skill_md):
                continue
            meta = skill_md.parent / "SKILL_METADATA.json"
            if not meta.exists():
                errors.append(f"skill missing SKILL_METADATA.json: {skill_md}")
            else:
                validate_skill_metadata_file(meta, errors)
        for agent_md in repo.rglob("AGENT.md"):
            if is_non_canonical_skill_or_agent_tree(agent_md):
                continue
            meta = agent_md.parent / "AGENT_METADATA.json"
            if not meta.exists():
                errors.append(f"agent missing AGENT_METADATA.json: {agent_md}")
            else:
                validate_skill_metadata_file(meta, errors)

    # Check graph/control registries exist and reference files exist.
    control = substrate / "registry" / "skill-agent-control-plane-registry.json"
    if not control.exists():
        errors.append("missing skill-agent-control-plane-registry.json")
    else:
        data = load_json(control)
        for key in ["canonical_schemas","canonical_registries","validators","boundary_docs"]:
            for rel in data.get(key, []):
                if not (substrate / rel).exists():
                    errors.append(f"control plane registry points to missing file: {rel}")

    graph = substrate / "registry" / "skill-agent-graph-index.json"
    if not graph.exists():
        errors.append("missing skill-agent-graph-index.json")

    workflow = substrate / "registry" / "workflow-composition-registry.json"
    if not workflow.exists():
        errors.append("missing workflow-composition-registry.json")

    if errors:
        for e in errors:
            print(f"FAIL {e}")
        return 1
    print("Skill-Agent Control Plane workspace validation passed.")
    print(f"workspace={workspace}")
    print(f"repos_discovered={len(discovered)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
