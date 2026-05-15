from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path

from scripts.validate_managed_patch_preservation import (
    analyze_change,
    content_hash,
    has_valid_decision,
    is_managed_patch_decision_record,
    is_protected_path,
    sanitize_target_path,
    validate_repo,
)


def _valid_decision(repo_name: str, target: str, old: str = "", new: str = "") -> dict:
    return {
        "schema_version": "managed_patch_decision.v2",
        "decision_id": "mpd_example_AGENTS",
        "decision_scope": "file",
        "repo": repo_name,
        "target_path": target,
        "change_mode": "replace",
        "protected_surface": True,
        "old_content_reviewed": True,
        "preservation_strategy": "replacement_intentional",
        "reason": "The old file was intentionally replaced after a preservation review found it obsolete.",
        "user_intent_alignment_summary": "The replacement aligns with the user's explicit instruction to remove contradictory doctrine.",
        "diff_review_summary": "Removed headings and policy-bearing content were reviewed and found obsolete.",
        "merge_considered": True,
        "why_merge_not_sufficient": "Merging would preserve contradictory instructions and confuse future agents.",
        "replacement_justification": "The replacement is necessary because the old instructions contradicted the active governance boundary.",
        "risk_tier": "protected",
        "human_review_required": True,
        "human_review_status": "approved",
        "approver": "test_approver",
        "model_review_level": "extra_high",
        "reviewer_model": "Codex extra-high",
        "old_content_sha256": f"sha256:{content_hash(old)}" if old else None,
        "new_content_sha256": f"sha256:{content_hash(new)}" if new else None,
        "removed_content_summary": ["test"],
        "alternatives_considered": ["preserve_and_add", "merge", "replace"],
        "automated_checks_run": ["validate_managed_patch_preservation.py"],
        "blast_radius": None,
        "source_refs": [],
        "created_by": "pytest",
        "created_at": "2026-05-14T00:00:00Z",
    }


def _init_git_repo(repo: Path) -> None:
    subprocess.run(["git", "-C", str(repo), "init"], check=True, stdout=subprocess.PIPE)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)


def _commit_all(repo: Path, message: str) -> None:
    subprocess.run(["git", "-C", str(repo), "add", "."], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", message], check=True, stdout=subprocess.PIPE)


def _protected_digest(paths: list[str]) -> str:
    return hashlib.sha256("\n".join(sorted(paths)).encode("utf-8")).hexdigest()[:12]


def test_agents_md_is_protected() -> None:
    assert is_protected_path("AGENTS.md")
    assert is_protected_path("governance/SOMETHING.md")
    assert is_protected_path("registry/schema-registry.json")
    assert is_protected_path("src/lawfirm_os_orchestrator/policy_engine.py")
    assert is_protected_path(".github/workflows/ci.yml")
    assert is_protected_path("pyproject.toml")
    assert not is_protected_path("tmp/random.bin")


def test_markdown_replacement_is_suspicious() -> None:
    old = """
# Agent Instructions

## Repo purpose
This repo owns legal knowledge runtime behavior.

## Invariants
- Preserve source references.
- Never ingest real client data.

## Allowed MVP work
- Synthetic ingestion preflight.
- Context bundle assembly.

## Forbidden MVP work
- Live connectors.
- Production data.
"""
    new = """
<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->
Read the AI front door before editing.
<!-- END LAWFIRM_OS_BOOTSTRAP -->
"""
    result = analyze_change("AGENTS.md", old, new)
    assert result.suspicious
    assert any("removed markdown" in reason for reason in result.suspicious_reasons)
    assert any("bootstrap block" in reason for reason in result.suspicious_reasons)
    assert any("generic AI front-door" in reason for reason in result.suspicious_reasons)


def test_merge_that_preserves_headings_is_not_suspicious() -> None:
    old = """
# Agent Instructions

## Repo purpose
This repo owns legal knowledge runtime behavior.

## Invariants
- Preserve source references.
- Never ingest real client data.

## Allowed MVP work
- Synthetic ingestion preflight.

## Forbidden MVP work
- Live connectors.
"""
    new = """
<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->
Read the AI front door before editing.
<!-- END LAWFIRM_OS_BOOTSTRAP -->

<!-- BEGIN REPO_SPECIFIC_INSTRUCTIONS -->
# Agent Instructions

## Repo purpose
This repo owns legal knowledge runtime behavior.

## Invariants
- Preserve source references.
- Never ingest real client data.

## Allowed MVP work
- Synthetic ingestion preflight.

## Forbidden MVP work
- Live connectors.
<!-- END REPO_SPECIFIC_INSTRUCTIONS -->
"""
    result = analyze_change("AGENTS.md", old, new)
    assert not result.suspicious, result.suspicious_reasons


def test_json_key_and_identifier_removal_is_suspicious() -> None:
    old = json.dumps(
        {
            "schemas": {
                "a": {"id": "schema.a", "path": "schemas/a.schema.json"},
                "b": {"id": "schema.b", "path": "schemas/b.schema.json"},
            }
        }
    )
    new = json.dumps({"schemas": {"a": {"id": "schema.a", "path": "schemas/a.schema.json"}}})
    result = analyze_change("registry/schema-registry.json", old, new)
    assert result.suspicious
    assert any("removed JSON keys" in reason for reason in result.suspicious_reasons)
    assert any("removed JSON identifiers" in reason for reason in result.suspicious_reasons)


def test_public_python_symbol_removal_is_suspicious() -> None:
    old = """
def validate_policy():
    return True

class BoundaryGate:
    def enforce(self):
        return True
"""
    new = """
def validate_policy():
    return True
"""
    result = analyze_change("src/lawfirm_os_orchestrator/policy_engine.py", old, new)
    assert result.suspicious
    assert any("removed public Python symbols" in reason for reason in result.suspicious_reasons)


def test_contract_lock_change_is_suspicious() -> None:
    old = json.dumps({"contract_sha": "abc", "archive_tree_sha256": "old"})
    new = json.dumps({"contract_sha": "abc", "archive_tree_sha256": "new"})
    result = analyze_change("contracts.lock.json", old, new)
    assert result.suspicious
    assert any("contract lock changed" in reason for reason in result.suspicious_reasons)


def test_extra_high_valid_decision_allows_destructive_protected_change(tmp_path: Path) -> None:
    workspace = tmp_path
    repo = workspace / "LawFirm-os-example"
    repo.mkdir()
    target = "AGENTS.md"
    old = "# Old\n\n## Invariants\n- a\n" * 5
    new = "# New\n"
    safe = sanitize_target_path(target)
    decision_dir = workspace / "LawFirm-os-semantic-substrate" / "registry" / "managed-patch-decisions" / repo.name
    decision_dir.mkdir(parents=True)
    (decision_dir / safe).write_text(json.dumps(_valid_decision(repo.name, target, old, new)), encoding="utf-8")
    result = analyze_change(target, old, new)
    ok, _ = has_valid_decision(workspace, repo, result, old=old, new=new)
    assert ok


def test_high_but_not_extra_high_decision_does_not_allow_destructive_change(tmp_path: Path) -> None:
    workspace = tmp_path
    repo = workspace / "LawFirm-os-example"
    repo.mkdir()
    target = "AGENTS.md"
    old = "# Old\n\n## Invariants\n- a\n" * 5
    new = "# New\n"
    decision = _valid_decision(repo.name, target, old, new)
    decision["model_review_level"] = "high"
    safe = sanitize_target_path(target)
    decision_dir = workspace / "LawFirm-os-semantic-substrate" / "registry" / "managed-patch-decisions" / repo.name
    decision_dir.mkdir(parents=True)
    (decision_dir / safe).write_text(json.dumps(decision), encoding="utf-8")
    result = analyze_change(target, old, new)
    ok, _ = has_valid_decision(workspace, repo, result, old=old, new=new)
    assert not ok


def test_cli_flags_overwrite_without_decision(tmp_path: Path) -> None:
    workspace = tmp_path
    repo = workspace / "LawFirm-os-example"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init"], check=True, stdout=subprocess.PIPE)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    agents = repo / "AGENTS.md"
    agents.write_text(
        "# Agent Instructions\n\n## Repo purpose\nSpecific.\n\n## Invariants\n- one\n- two\n\n## Forbidden MVP work\n- no live data\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(repo), "add", "AGENTS.md"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "initial"], check=True, stdout=subprocess.PIPE)
    agents.write_text(
        "<!-- BEGIN LAWFIRM_OS_BOOTSTRAP -->\nRead front door.\n<!-- END LAWFIRM_OS_BOOTSTRAP -->\n",
        encoding="utf-8",
    )

    script = Path(__file__).resolve().parents[1] / "scripts" / "validate_managed_patch_preservation.py"
    proc = subprocess.run(
        ["python", str(script), "--workspace", str(workspace)],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert proc.returncode == 1
    assert "Managed patch preservation validation FAILED" in proc.stdout
    assert "AGENTS.md" in proc.stdout


def test_cli_flags_missing_backup_content(tmp_path: Path) -> None:
    workspace = tmp_path
    repo = workspace / "LawFirm-os-example"
    repo.mkdir()
    subprocess.run(["git", "-C", str(repo), "init"], check=True, stdout=subprocess.PIPE)
    subprocess.run(["git", "-C", str(repo), "config", "user.email", "test@example.com"], check=True)
    subprocess.run(["git", "-C", str(repo), "config", "user.name", "Test"], check=True)
    (repo / "README.md").write_text("# New\n", encoding="utf-8")
    (repo / "README.md.managed-preservation-backup").write_text(
        "# Original\n\n## Invariants\n- must preserve old content\n\n## Forbidden work\n- do not delete doctrine\n",
        encoding="utf-8",
    )
    subprocess.run(["git", "-C", str(repo), "add", "README.md"], check=True)
    subprocess.run(["git", "-C", str(repo), "commit", "-m", "initial"], check=True, stdout=subprocess.PIPE)

    script = Path(__file__).resolve().parents[1] / "scripts" / "validate_managed_patch_preservation.py"
    proc = subprocess.run(
        ["python", str(script), "--workspace", str(workspace), "--base-ref", "HEAD"],
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    assert proc.returncode == 1
    assert "backup file" in proc.stdout


def test_managed_patch_decision_records_are_protected_but_not_blast_radius_counted(tmp_path: Path) -> None:
    workspace = tmp_path
    repo = workspace / "LawFirm-os-semantic-substrate"
    repo.mkdir()
    _init_git_repo(repo)

    registry_file = repo / "registry" / "schema-registry.json"
    registry_file.parent.mkdir(parents=True)
    registry_file.write_text("{}\n", encoding="utf-8")
    _commit_all(repo, "initial")
    registry_file.write_text('{"added": true}\n', encoding="utf-8")

    _, count_before, paths_before = validate_repo(workspace, repo, "HEAD", False, False)
    digest_before = _protected_digest([f"{repo.name}/{path}" for path in paths_before])

    decision_path = repo / "registry" / "managed-patch-decisions" / "workspace" / "blast-radius-example.json"
    decision_path.parent.mkdir(parents=True)
    decision_path.write_text('{"decision_scope": "workspace"}\n', encoding="utf-8")

    _, count_untracked, paths_untracked = validate_repo(workspace, repo, "HEAD", False, False)
    digest_untracked = _protected_digest([f"{repo.name}/{path}" for path in paths_untracked])

    subprocess.run(["git", "-C", str(repo), "add", "registry/managed-patch-decisions/workspace/blast-radius-example.json"], check=True)
    _, count_staged, paths_staged = validate_repo(workspace, repo, "HEAD", False, False)
    digest_staged = _protected_digest([f"{repo.name}/{path}" for path in paths_staged])

    assert is_protected_path("registry/managed-patch-decisions/workspace/blast-radius-example.json")
    assert is_managed_patch_decision_record("registry/managed-patch-decisions/workspace/blast-radius-example.json")
    assert count_before == count_untracked == count_staged == 1
    assert paths_before == paths_untracked == paths_staged == ["registry/schema-registry.json"]
    assert digest_before == digest_untracked == digest_staged


def test_committed_decision_records_do_not_change_include_last_commit_digest(tmp_path: Path) -> None:
    def build_repo(workspace: Path, include_decision_record: bool) -> tuple[int, str, list[str]]:
        repo = workspace / "LawFirm-os-semantic-substrate"
        repo.mkdir(parents=True)
        _init_git_repo(repo)
        registry_file = repo / "registry" / "schema-registry.json"
        registry_file.parent.mkdir(parents=True)
        registry_file.write_text("{}\n", encoding="utf-8")
        _commit_all(repo, "initial")
        registry_file.write_text('{"added": true}\n', encoding="utf-8")
        if include_decision_record:
            decision_path = repo / "registry" / "managed-patch-decisions" / "workspace" / "blast-radius-example.json"
            decision_path.parent.mkdir(parents=True)
            decision_path.write_text('{"decision_scope": "workspace"}\n', encoding="utf-8")
        _commit_all(repo, "second")
        _, count, paths = validate_repo(workspace, repo, "HEAD", True, False)
        digest = _protected_digest([f"{repo.name}/{path}" for path in paths])
        return count, digest, paths

    count_without, digest_without, paths_without = build_repo(tmp_path / "without-decision", False)
    count_with, digest_with, paths_with = build_repo(tmp_path / "with-decision", True)

    assert count_without == count_with == 1
    assert paths_without == paths_with == ["registry/schema-registry.json"]
    assert digest_without == digest_with


def test_decision_record_lookup_still_reads_managed_patch_decisions(tmp_path: Path) -> None:
    workspace = tmp_path
    repo = workspace / "LawFirm-os-example"
    repo.mkdir()
    target = "AGENTS.md"
    old = "# Old\n\n## Invariants\n- a\n" * 5
    new = "# New\n"
    decision_dir = workspace / "LawFirm-os-semantic-substrate" / "registry" / "managed-patch-decisions" / repo.name
    decision_dir.mkdir(parents=True)
    (decision_dir / sanitize_target_path(target)).write_text(
        json.dumps(_valid_decision(repo.name, target, old, new)),
        encoding="utf-8",
    )

    result = analyze_change(target, old, new)
    ok, _ = has_valid_decision(workspace, repo, result, old=old, new=new)

    assert ok


def test_registry_json_outside_managed_patch_decisions_remains_protected_and_counted(tmp_path: Path) -> None:
    workspace = tmp_path
    repo = workspace / "LawFirm-os-semantic-substrate"
    repo.mkdir()
    _init_git_repo(repo)

    root_registry = repo / "registry" / "ordinary.json"
    nested_registry = repo / "registry" / "other-folder" / "ordinary.json"
    nested_registry.parent.mkdir(parents=True)
    root_registry.write_text("{}\n", encoding="utf-8")
    nested_registry.write_text("{}\n", encoding="utf-8")
    _commit_all(repo, "initial")

    root_registry.write_text('{"changed": true}\n', encoding="utf-8")
    nested_registry.write_text('{"changed": true}\n', encoding="utf-8")
    decision_path = repo / "registry" / "managed-patch-decisions" / "workspace" / "blast-radius-example.json"
    decision_path.parent.mkdir(parents=True)
    decision_path.write_text('{"decision_scope": "workspace"}\n', encoding="utf-8")

    _, count, paths = validate_repo(workspace, repo, "HEAD", False, False)

    assert is_protected_path("registry/ordinary.json")
    assert is_protected_path("registry/other-folder/ordinary.json")
    assert not is_managed_patch_decision_record("registry/other-folder/ordinary.json")
    assert count == 2
    assert paths == ["registry/ordinary.json", "registry/other-folder/ordinary.json"]
