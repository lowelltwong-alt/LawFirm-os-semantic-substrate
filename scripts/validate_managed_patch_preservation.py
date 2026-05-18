#!/usr/bin/env python3
"""Deterministic managed patch preservation validator for LawFirm OS.

This validator catches the main failure modes seen when coding agents or patch
scripts modify governance-heavy multi-repo systems:

* generic bootstrap text replacing repo-specific doctrine;
* protected Markdown sections/headings disappearing;
* registry/schema JSON keys or IDs silently disappearing;
* public Python functions/classes being removed in protected code surfaces;
* contract locks, workflows, prompt/tool policies, and AI rules changing without
  review;
* backup files containing important content that is missing from the final file;
* broad blast-radius patch sets that should receive higher scrutiny.

It does not ban rewrites. It forces a decision: preserve-and-add, merge,
replace, delete, or regenerate, with an explicit decision record for destructive
or suspicious changes.
"""
from __future__ import annotations

import argparse
import ast
import difflib
import fnmatch
import hashlib
import json
import re
import subprocess
import sys
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

PROTECTED_ROOT_FILES = {
    "AGENTS.md",
    "AI_WORK_START_HERE.md",
    "AI_START_HERE.md",
    "README.md",
    "CLAUDE.md",
    "skill-agent-manifest.json",
    "contracts.lock.json",
    ".gitignore",
    ".pre-commit-config.yaml",
    "pyproject.toml",
    "requirements.txt",
    "requirements-dev.txt",
    "uv.lock",
    "poetry.lock",
    "Pipfile",
    "Pipfile.lock",
    "package.json",
    "package-lock.json",
    "pnpm-lock.yaml",
    "yarn.lock",
    "Makefile",
    "Dockerfile",
    "ruff.toml",
    "mypy.ini",
    "pytest.ini",
}

PROTECTED_GLOBS = [
    ".cursor/rules/*.mdc",
    ".github/copilot-instructions.md",
    ".github/workflows/*.yml",
    ".github/workflows/*.yaml",
    "governance/**/*.md",
    "docs/**/*.md",
    "docs/**/*.yml",
    "docs/**/*.yaml",
    "registry/**/*.json",
    "manifests/**/*.json",
    "exports/**/*.json",
    "schemas/**/*.json",
    "policies/**/*.json",
    "prompts/**/*.md",
    "prompts/**/*.txt",
    "scripts/**/*.py",
    "tests/**/*.py",
    "src/**/*.py",
    "skills/**/SKILL.md",
    "skills/**/SKILL_METADATA.json",
    ".agents/**/SKILL.md",
    ".agents/**/SKILL_METADATA.json",
    "**/AGENT.md",
    "**/AGENT_METADATA.json",
    "tools/**/*.json",
    "workflows/**/*.json",
    "workflow/**/*.json",
    "examples/**/*.json",
]

DOC_KEYWORDS = [
    "invariant",
    "allowed",
    "forbidden",
    "must not",
    "must:",
    "must ",
    "required",
    "require",
    "boundary",
    "validation",
    "stop condition",
    "do not",
    "read order",
    "authority",
    "canonical",
    "governance",
    "repo purpose",
    "mvp",
    "not allowed",
    "fail closed",
    "hard fail",
    "synthetic-only",
    "synthetic only",
    "real client data",
    "real matter data",
    "privilege",
    "confidential",
    "human approval",
    "approval required",
    "read-only",
    "read only",
    "contract lock",
    "manifest",
    "schema registry",
    "route registry",
    "event_class",
    "route_id",
    "semantic substrate",
    "exception lake",
    "orchestrator",
    "evidence packet",
    "idempotency",
    "trace_id",
    "run_id",
]

WEAKENING_WORDS = [
    "optional",
    "may ",
    "can ",
    "should ",
    "best effort",
    "try ",
    "not required",
    "skip",
    "disable",
    "ignore",
    "allow by default",
    "auto-approve",
]

JSON_IDENTIFIER_KEYS = {
    "id",
    "$id",
    "schema_id",
    "schema_ref",
    "registry_id",
    "route_id",
    "event_class",
    "event_class_id",
    "skill_id",
    "agent_id",
    "tool_id",
    "workflow_id",
    "bundle_type",
    "name",
    "path",
    "uri",
    "ref",
    "source_ref",
}

WORKSPACE_EXCLUDE_CONTAINS = ["patch", "seed-pack", "backup", "archive"]
LOCAL_NOISE_DIRS = {
    ".git",
    "__pycache__",
    ".pytest_cache",
    ".pytest-tmp-root",
    ".cursor",
    "codex_manual_temp",
}
BACKUP_SUFFIXES = [
    ".managed-preservation-backup",
    ".research-delta-backup",
    ".backup",
    ".bak",
    ".orig",
]

BLAST_RADIUS_THRESHOLD = 20


@dataclass(frozen=True)
class ChangeAnalysis:
    path: str
    protected_surface: bool
    old_exists: bool
    new_exists: bool
    old_nonblank_lines: int
    new_nonblank_lines: int
    removed_nonblank_lines: int
    added_nonblank_lines: int
    similarity_ratio: float
    removed_headings: list[str] = field(default_factory=list)
    removed_json_keys: list[str] = field(default_factory=list)
    removed_json_identifiers: list[str] = field(default_factory=list)
    removed_python_symbols: list[str] = field(default_factory=list)
    removed_keyword_lines: list[str] = field(default_factory=list)
    policy_weakening_lines: list[str] = field(default_factory=list)
    suspicious_reasons: list[str] = field(default_factory=list)

    @property
    def suspicious(self) -> bool:
        return bool(self.suspicious_reasons)


@dataclass(frozen=True)
class Violation:
    repo: str
    path: str
    reason: str
    decision_locations: list[str]


def run_git(repo: Path, args: list[str], *, check: bool = True) -> str:
    proc = subprocess.run(
        ["git", "-C", str(repo), *args],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if check and proc.returncode != 0:
        raise RuntimeError(
            f"git -C {repo} {' '.join(args)} failed: {proc.stderr.strip()}"
        )
    return proc.stdout


def is_git_repo(path: Path) -> bool:
    return (path / ".git").exists()


def discover_repos(workspace: Path) -> list[Path]:
    repos: list[Path] = []
    for child in sorted(workspace.iterdir()):
        if not child.is_dir():
            continue
        name = child.name
        if not name.startswith("LawFirm-os-"):
            continue
        lowered = name.lower()
        if any(piece in lowered for piece in WORKSPACE_EXCLUDE_CONTAINS):
            continue
        if is_git_repo(child):
            repos.append(child)
    return repos


def normalize_path(path: str | Path) -> str:
    return str(path).replace("\\", "/")


def is_managed_patch_decision_record(path: str | Path) -> bool:
    norm = normalize_path(path).lstrip("./")
    return norm == "registry/managed-patch-decisions" or norm.startswith("registry/managed-patch-decisions/")


def _matches_glob(norm: str, pattern: str) -> bool:
    if fnmatch.fnmatch(norm, pattern):
        return True
    if "/**/" in pattern:
        direct = pattern.replace("/**/", "/")
        if fnmatch.fnmatch(norm, direct):
            return True
    return False


def is_protected_path(path: str) -> bool:
    norm = normalize_path(path)
    if Path(norm).name in PROTECTED_ROOT_FILES and "/" not in norm:
        return True
    if Path(norm).name in PROTECTED_ROOT_FILES:
        return True
    return any(_matches_glob(norm, pattern) for pattern in PROTECTED_GLOBS)


def git_file_exists(repo: Path, ref: str, path: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(repo), "cat-file", "-e", f"{ref}:{path}"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    return proc.returncode == 0


def git_show(repo: Path, ref: str, path: str) -> str:
    if not git_file_exists(repo, ref, path):
        return ""
    return run_git(repo, ["show", f"{ref}:{path}"], check=True)


def read_worktree_file(repo: Path, path: str) -> str:
    file_path = repo / path
    if not file_path.exists() or file_path.is_dir():
        return ""
    try:
        return file_path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return ""


def changed_files(repo: Path, base_ref: str) -> set[str]:
    files: set[str] = set()
    commands = [
        ["diff", "--name-only", "--diff-filter=ACMRTD", f"{base_ref}..HEAD"],
        ["diff", "--name-only", "--diff-filter=ACMRTD"],
        ["diff", "--cached", "--name-only", "--diff-filter=ACMRTD"],
        ["ls-files", "--others", "--exclude-standard"],
    ]
    for cmd in commands:
        out = run_git(repo, cmd, check=False)
        for line in out.splitlines():
            if line.strip():
                files.add(normalize_path(line.strip()))
    return files


def last_commit_changed_files(repo: Path) -> set[str]:
    out = run_git(repo, ["diff", "--name-only", "--diff-filter=ACMRTD", "HEAD~1..HEAD"], check=False)
    return {normalize_path(line.strip()) for line in out.splitlines() if line.strip()}


def nonblank_lines(text: str) -> list[str]:
    return [line for line in text.splitlines() if line.strip()]


def removed_added_lines(old: str, new: str) -> tuple[list[str], list[str]]:
    removed: list[str] = []
    added: list[str] = []
    for line in difflib.ndiff(old.splitlines(), new.splitlines()):
        if line.startswith("- ") and line[2:].strip():
            removed.append(line[2:])
        elif line.startswith("+ ") and line[2:].strip():
            added.append(line[2:])
    return removed, added


def markdown_headings(text: str) -> list[str]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s{0,3}(#{1,6})\s+(.+?)\s*$", line)
        if match:
            heading = re.sub(r"\s+", " ", match.group(2).strip().lower())
            headings.append(heading)
    return headings


def parse_json(text: str) -> Any | None:
    if not text.strip():
        return None
    try:
        return json.loads(text)
    except Exception:
        return None


def parse_json_keys(text: str) -> set[str]:
    data = parse_json(text)
    if data is None:
        return set()
    keys: set[str] = set()

    def walk(obj: Any, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                path = f"{prefix}.{key}" if prefix else str(key)
                keys.add(path)
                walk(value, path)
        elif isinstance(obj, list):
            for value in obj:
                if isinstance(value, (dict, list)):
                    walk(value, f"{prefix}[]" if prefix else "[]")

    walk(data)
    return keys


def parse_json_identifiers(text: str) -> set[str]:
    data = parse_json(text)
    if data is None:
        return set()
    values: set[str] = set()

    def walk(obj: Any, prefix: str = "") -> None:
        if isinstance(obj, dict):
            for key, value in obj.items():
                key_lower = str(key).lower()
                path = f"{prefix}.{key}" if prefix else str(key)
                if key_lower in JSON_IDENTIFIER_KEYS or key_lower.endswith("_id") or key_lower.endswith("_path"):
                    if isinstance(value, (str, int, float, bool)):
                        values.add(f"{path}={value}")
                    elif isinstance(value, list):
                        for item in value:
                            if isinstance(item, (str, int, float, bool)):
                                values.add(f"{path}[]={item}")
                walk(value, path)
        elif isinstance(obj, list):
            for value in obj:
                if isinstance(value, (dict, list)):
                    walk(value, f"{prefix}[]" if prefix else "[]")

    walk(data)
    return values


def public_python_symbols(text: str) -> set[str]:
    if not text.strip():
        return set()
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return set()
    symbols: set[str] = set()
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if not node.name.startswith("_"):
                symbols.add(node.name)
        elif isinstance(node, ast.ClassDef):
            if not node.name.startswith("_"):
                symbols.add(node.name)
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) and not item.name.startswith("_"):
                    symbols.add(f"{node.name}.{item.name}")
    return symbols


def content_hash(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def analyze_change(path: str, old: str, new: str) -> ChangeAnalysis:
    protected = is_protected_path(path)
    old_lines = nonblank_lines(old)
    new_lines = nonblank_lines(new)
    removed, added = removed_added_lines(old, new)
    ratio = difflib.SequenceMatcher(None, old, new).ratio() if old or new else 1.0
    suspicious: list[str] = []

    old_exists = bool(old)
    new_exists = bool(new)
    removed_headings: list[str] = []
    removed_json_keys: list[str] = []
    removed_json_identifiers: list[str] = []
    removed_python_symbols: list[str] = []
    removed_keyword_lines: list[str] = []
    policy_weakening_lines: list[str] = []

    if not protected:
        return ChangeAnalysis(
            path=path,
            protected_surface=False,
            old_exists=old_exists,
            new_exists=new_exists,
            old_nonblank_lines=len(old_lines),
            new_nonblank_lines=len(new_lines),
            removed_nonblank_lines=len(removed),
            added_nonblank_lines=len(added),
            similarity_ratio=ratio,
        )

    if old_exists and not new_exists:
        suspicious.append("protected file deleted")

    if len(old_lines) >= 12 and len(removed) >= 10:
        suspicious.append(f"removed {len(removed)} nonblank lines from protected file")

    if len(old_lines) >= 12 and len(new_lines) < int(len(old_lines) * 0.75):
        suspicious.append(
            f"new file has {len(new_lines)} nonblank lines vs old {len(old_lines)}"
        )

    if len(old_lines) >= 20 and ratio < 0.55:
        suspicious.append(f"low old/new similarity ratio {ratio:.2f}")

    if path == "contracts.lock.json" and old_exists and new_exists and old != new:
        suspicious.append("contract lock changed; requires provenance and committed-substrate review")

    if path.lower().endswith((".md", ".mdc", ".txt", ".yaml", ".yml")):
        old_headings = set(markdown_headings(old))
        new_headings = set(markdown_headings(new))
        removed_headings = sorted(old_headings - new_headings)
        if removed_headings:
            suspicious.append(
                "removed markdown/headings: " + ", ".join(removed_headings[:5])
            )

        lowered_removed = [line for line in removed if any(k in line.lower() for k in DOC_KEYWORDS)]
        removed_keyword_lines = lowered_removed[:20]
        if lowered_removed:
            suspicious.append("removed governance/agent keyword-bearing lines")

        added_weak = [line for line in added if any(w in line.lower() for w in WEAKENING_WORDS)]
        if lowered_removed and added_weak:
            policy_weakening_lines = added_weak[:20]
            suspicious.append("possible policy weakening: strict lines removed while permissive language added")

        if "<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->" in new and "<!-- BEGIN REPO_SPECIFIC_INSTRUCTIONS -->" not in new:
            if len(old_lines) >= 12 or lowered_removed or old_headings:
                suspicious.append("bootstrap block present without repo-specific instruction marker")

        if "ai front door" in new.lower() and old_headings and removed_headings:
            suspicious.append("generic AI front-door text may have replaced repo-specific doctrine")

    if path.lower().endswith(".json"):
        old_keys = parse_json_keys(old)
        new_keys = parse_json_keys(new)
        removed_json_keys = sorted(old_keys - new_keys)
        if removed_json_keys:
            suspicious.append(
                "removed JSON keys: " + ", ".join(removed_json_keys[:10])
            )
        old_ids = parse_json_identifiers(old)
        new_ids = parse_json_identifiers(new)
        removed_json_identifiers = sorted(old_ids - new_ids)
        if removed_json_identifiers:
            suspicious.append(
                "removed JSON identifiers/refs: " + ", ".join(removed_json_identifiers[:10])
            )

    if path.lower().endswith(".py"):
        old_symbols = public_python_symbols(old)
        new_symbols = public_python_symbols(new)
        removed_python_symbols = sorted(old_symbols - new_symbols)
        if removed_python_symbols:
            suspicious.append(
                "removed public Python symbols: " + ", ".join(removed_python_symbols[:10])
            )

    return ChangeAnalysis(
        path=path,
        protected_surface=True,
        old_exists=old_exists,
        new_exists=new_exists,
        old_nonblank_lines=len(old_lines),
        new_nonblank_lines=len(new_lines),
        removed_nonblank_lines=len(removed),
        added_nonblank_lines=len(added),
        similarity_ratio=ratio,
        removed_headings=removed_headings,
        removed_json_keys=removed_json_keys,
        removed_json_identifiers=removed_json_identifiers,
        removed_python_symbols=removed_python_symbols,
        removed_keyword_lines=removed_keyword_lines,
        policy_weakening_lines=policy_weakening_lines,
        suspicious_reasons=suspicious,
    )


def sanitize_target_path(path: str) -> str:
    norm = normalize_path(path)
    digest = hashlib.sha256(norm.encode("utf-8")).hexdigest()[:12]
    safe = re.sub(r"[^A-Za-z0-9_.-]+", "__", norm)
    return f"{safe}.{digest}.json"


def logical_repo_name(name: str) -> str:
    if name == "LawFirm-os-exceptions-lake-runtime-main":
        return "LawFirm-os-exceptions-lake-runtime"
    return name


def decision_paths(workspace: Path, repo: Path, target_path: str) -> list[Path]:
    repo_name = repo.name
    logical_name = logical_repo_name(repo.name)
    safe = sanitize_target_path(target_path)
    return [
        workspace / "LawFirm-os-semantic-substrate" / "registry" / "managed-patch-decisions" / repo_name / safe,
        workspace / "LawFirm-os-semantic-substrate" / "registry" / "managed-patch-decisions" / logical_name / safe,
        repo / ".lawfirm-os" / "managed-patch-decisions" / safe,
    ]


def workspace_decision_paths(workspace: Path, digest: str) -> list[Path]:
    return [
        workspace / "LawFirm-os-semantic-substrate" / "registry" / "managed-patch-decisions" / "workspace" / f"blast-radius-{digest}.json"
    ]


def load_json(path: Path) -> dict[str, Any] | None:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None
    return data if isinstance(data, dict) else None


def _string_len(data: dict[str, Any], key: str) -> int:
    value = data.get(key)
    return len(value.strip()) if isinstance(value, str) else 0


def _nonempty_list(data: dict[str, Any], key: str) -> bool:
    value = data.get(key)
    return isinstance(value, list) and bool(value)


def has_valid_decision(workspace: Path, repo: Path, analysis: ChangeAnalysis, old: str = "", new: str = "") -> tuple[bool, list[str]]:
    paths = decision_paths(workspace, repo, analysis.path)
    existing = [path for path in paths if path.exists()]
    if not existing:
        return False, [str(path) for path in paths]

    for path in existing:
        data = load_json(path)
        if not data:
            continue
        if data.get("repo") not in {repo.name, logical_repo_name(repo.name), "workspace"}:
            continue
        if normalize_path(data.get("target_path", "")) != normalize_path(analysis.path):
            continue
        if data.get("old_content_reviewed") is not True:
            continue
        mode = data.get("change_mode")
        protected = bool(data.get("protected_surface"))
        reason = str(data.get("reason", ""))
        if len(reason.strip()) < 20:
            continue
        if _string_len(data, "user_intent_alignment_summary") < 20:
            continue
        if _string_len(data, "diff_review_summary") < 20:
            continue
        if not _nonempty_list(data, "alternatives_considered"):
            continue
        if not _nonempty_list(data, "automated_checks_run"):
            continue

        if old and data.get("old_content_sha256"):
            if str(data["old_content_sha256"]).replace("sha256:", "") != content_hash(old):
                continue
        if new and data.get("new_content_sha256"):
            if str(data["new_content_sha256"]).replace("sha256:", "") != content_hash(new):
                continue

        if mode in {"replace", "delete", "regenerate"} and protected:
            justification = str(data.get("replacement_justification") or "")
            if len(justification.strip()) < 30:
                continue
            if data.get("merge_considered") is not True:
                continue
            if _string_len(data, "why_merge_not_sufficient") < 20:
                continue
            if data.get("human_review_required") is not True:
                continue
            if data.get("human_review_status") != "approved":
                continue
            if data.get("model_review_level") != "extra_high":
                continue
        return True, [str(path) for path in paths]

    return False, [str(path) for path in paths]


def write_decision_stub(workspace: Path, repo: Path, analysis: ChangeAnalysis, old: str = "", new: str = "") -> Path:
    path = decision_paths(workspace, repo, analysis.path)[0]
    path.parent.mkdir(parents=True, exist_ok=True)
    mode = "delete" if not analysis.new_exists else "replace"
    data = {
        "schema_version": "managed_patch_decision.v2",
        "decision_id": f"mpd_{repo.name}_{sanitize_target_path(analysis.path).removesuffix('.json')}",
        "decision_scope": "file",
        "repo": repo.name,
        "target_path": analysis.path,
        "change_mode": mode,
        "protected_surface": analysis.protected_surface,
        "old_content_reviewed": False,
        "preservation_strategy": "replacement_intentional",
        "reason": "TODO: Explain why this file should be replaced/deleted/regenerated instead of preserving and merging existing content.",
        "user_intent_alignment_summary": "TODO: Explain how this destructive change aligns with the user's explicit design intent.",
        "diff_review_summary": "TODO: Summarize removed headings, keys, symbols, and policy-bearing lines.",
        "merge_considered": False,
        "why_merge_not_sufficient": "TODO: Explain why preserve-and-add or merge is not sufficient.",
        "replacement_justification": "TODO: Required for destructive changes to protected files.",
        "risk_tier": "protected",
        "human_review_required": True,
        "human_review_status": "pending",
        "approver": None,
        "model_review_level": "extra_high",
        "reviewer_model": "TODO: e.g., Codex extra-high or Claude high",
        "old_content_sha256": f"sha256:{content_hash(old)}" if old else None,
        "new_content_sha256": f"sha256:{content_hash(new)}" if new else None,
        "removed_content_summary": analysis.suspicious_reasons,
        "alternatives_considered": [
            "preserve_and_add",
            "merge",
            "replace/delete/regenerate",
        ],
        "automated_checks_run": [],
        "source_refs": [],
        "created_by": "validator_stub",
        "created_at": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    }
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return path


def validate_repo(workspace: Path, repo: Path, base_ref: str, include_last_commit: bool, create_stubs: bool) -> tuple[list[Violation], int, list[str]]:
    paths = changed_files(repo, base_ref)
    if include_last_commit:
        paths |= last_commit_changed_files(repo)
    violations: list[Violation] = []
    protected_changed = [
        path
        for path in sorted(paths)
        if is_protected_path(path)
        and not path.startswith(".git/")
        and not is_managed_patch_decision_record(path)
    ]

    for path in protected_changed:
        old = git_show(repo, base_ref, path)
        new = read_worktree_file(repo, path)
        if not new and git_file_exists(repo, "HEAD", path):
            new = git_show(repo, "HEAD", path)

        analysis = analyze_change(path, old, new)
        if not analysis.suspicious:
            continue
        ok, locations = has_valid_decision(workspace, repo, analysis, old=old, new=new)
        if not ok:
            if create_stubs:
                stub = write_decision_stub(workspace, repo, analysis, old=old, new=new)
                locations = [str(stub)] + locations
            violations.append(
                Violation(
                    repo=repo.name,
                    path=path,
                    reason="; ".join(analysis.suspicious_reasons),
                    decision_locations=locations,
                )
            )

    return violations, len(protected_changed), protected_changed


def backup_counterpart(path: Path) -> Path | None:
    name = path.name
    for suffix in BACKUP_SUFFIXES:
        if name.endswith(suffix):
            return path.with_name(name[: -len(suffix)])
    return None


def scan_backup_violations(workspace: Path, repo: Path, create_stubs: bool) -> list[Violation]:
    violations: list[Violation] = []
    for backup in repo.rglob("*"):
        try:
            rel_backup_path = backup.relative_to(repo)
        except ValueError:
            continue
        if any(part in LOCAL_NOISE_DIRS for part in rel_backup_path.parts):
            continue
        try:
            if backup.is_dir():
                continue
        except OSError:
            continue
        counterpart = backup_counterpart(backup)
        if counterpart is None:
            continue
        try:
            rel_counterpart = normalize_path(counterpart.relative_to(repo))
            rel_backup = normalize_path(backup.relative_to(repo))
        except ValueError:
            continue
        if not is_protected_path(rel_counterpart):
            continue
        old = read_worktree_file(repo, rel_backup)
        new = read_worktree_file(repo, rel_counterpart)
        analysis = analyze_change(rel_counterpart, old, new)
        if not analysis.suspicious:
            continue
        ok, locations = has_valid_decision(workspace, repo, analysis, old=old, new=new)
        if not ok:
            if create_stubs:
                stub = write_decision_stub(workspace, repo, analysis, old=old, new=new)
                locations = [str(stub)] + locations
            violations.append(
                Violation(
                    repo=repo.name,
                    path=rel_counterpart,
                    reason=f"backup file {rel_backup} contains protected content not preserved in final file; " + "; ".join(analysis.suspicious_reasons),
                    decision_locations=locations,
                )
            )
    return violations


def has_workspace_blast_radius_decision(workspace: Path, digest: str) -> tuple[bool, list[str]]:
    paths = workspace_decision_paths(workspace, digest)
    for path in paths:
        data = load_json(path) if path.exists() else None
        if not data:
            continue
        if data.get("decision_scope") != "workspace":
            continue
        if data.get("old_content_reviewed") is not True:
            continue
        if data.get("human_review_required") is not True:
            continue
        if data.get("human_review_status") != "approved":
            continue
        if data.get("model_review_level") != "extra_high":
            continue
        if _string_len(data, "user_intent_alignment_summary") < 20:
            continue
        if _nonempty_list(data, "automated_checks_run"):
            return True, [str(p) for p in paths]
    return False, [str(p) for p in paths]


def print_report(violations: list[Violation]) -> None:
    if not violations:
        print("Managed patch preservation validation passed.")
        return
    print("Managed patch preservation validation FAILED.")
    print()
    print("Protected content appears to have been replaced, deleted, substantially rewritten, or changed at broad blast radius.")
    print("Stop and decide whether to preserve, merge, replace, delete, or regenerate.")
    print()
    for idx, violation in enumerate(violations, start=1):
        print(f"{idx}. {violation.repo}/{violation.path}")
        print(f"   reason: {violation.reason}")
        print("   add an approved decision record at one of:")
        for loc in violation.decision_locations:
            print(f"   - {loc}")
        print()


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, default=Path("."), help="Parent LawFirm OS workspace folder.")
    parser.add_argument("--base-ref", default="HEAD", help="Git base ref to compare against. Use origin/main in PR checks.")
    parser.add_argument("--include-last-commit", action="store_true", help="Also inspect HEAD~1..HEAD for already-committed replacements.")
    parser.add_argument("--create-decision-stubs", action="store_true", help="Create pending decision stubs for violations.")
    parser.add_argument("--repo", action="append", default=None, help="Specific repo folder name to inspect. Can be repeated.")
    parser.add_argument("--no-scan-backups", action="store_true", help="Disable backup-file comparison checks.")
    parser.add_argument("--blast-radius-threshold", type=int, default=BLAST_RADIUS_THRESHOLD, help="Protected changed-file count requiring workspace decision. Set 0 to disable.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    workspace = args.workspace.resolve()
    if args.repo:
        repos = [workspace / name for name in args.repo]
    else:
        repos = discover_repos(workspace)
    missing = [repo for repo in repos if not is_git_repo(repo)]
    if missing:
        for repo in missing:
            print(f"Not a git repo or missing: {repo}")
        return 2

    all_violations: list[Violation] = []
    total_protected_changed = 0
    changed_manifest: list[str] = []
    for repo in repos:
        repo_violations, protected_count, protected_paths = validate_repo(
            workspace=workspace,
            repo=repo,
            base_ref=args.base_ref,
            include_last_commit=args.include_last_commit,
            create_stubs=args.create_decision_stubs,
        )
        all_violations.extend(repo_violations)
        total_protected_changed += protected_count
        changed_manifest.extend(f"{repo.name}/{p}" for p in protected_paths)
        if not args.no_scan_backups:
            all_violations.extend(scan_backup_violations(workspace, repo, args.create_decision_stubs))

    if args.blast_radius_threshold and total_protected_changed >= args.blast_radius_threshold:
        digest = hashlib.sha256("\n".join(sorted(changed_manifest)).encode("utf-8")).hexdigest()[:12]
        ok, locations = has_workspace_blast_radius_decision(workspace, digest)
        if not ok:
            all_violations.append(
                Violation(
                    repo="workspace",
                    path="__blast_radius__",
                    reason=f"{total_protected_changed} protected files changed; broad patch requires workspace-level review decision",
                    decision_locations=locations,
                )
            )

    print_report(all_violations)
    return 1 if all_violations else 0


if __name__ == "__main__":
    raise SystemExit(main())
