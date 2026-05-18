from __future__ import annotations

import sys
import textwrap
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_contract_surface_provenance_modes import (  # noqa: E402
    scan_python_source,
    scan_workspace,
)


def _rules(findings) -> list[str]:
    return [f.rule_id for f in findings]


# ---------------------------------------------------------------------------
# Current-workspace regression test: the live repos must always be clean.
# ---------------------------------------------------------------------------


def test_current_workspace_has_no_provenance_mode_violations() -> None:
    workspace = REPO_ROOT.parent
    findings = scan_workspace(workspace)
    rendered = "\n".join(f.render(workspace) for f in findings)
    assert findings == [], (
        "validate_contract_surface_provenance_modes.py found risky provenance patterns "
        "in the live LawFirm OS workspace. Each finding indicates that committed-tree "
        "provenance could be backed by mutable working-tree bytes:\n" + rendered
    )


# ---------------------------------------------------------------------------
# C1: writes computed_from_commit + iterates filesystem + reads bytes, with no git plumbing.
# ---------------------------------------------------------------------------


def test_c1_flags_filesystem_hash_with_committed_tree_claim() -> None:
    source = textwrap.dedent(
        """
        import hashlib
        def buggy_compute_surface(root, commit_sha):
            items = []
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    data = path.read_bytes()
                    items.append((path.as_posix(), hashlib.sha256(data).hexdigest()))
            return {
                "surface_sha256": "x" * 64,
                "computed_from_commit": commit_sha,
            }
        """
    )
    findings = scan_python_source(source, "buggy_c1.py")
    assert "C1" in _rules(findings), findings


def test_c1_allows_git_plumbing_with_committed_tree_claim() -> None:
    source = textwrap.dedent(
        """
        import subprocess
        def safe_committed_compute(root, commit_sha):
            raw = subprocess.run(
                ["git", "ls-tree", "-r", "-z", commit_sha],
                cwd=root, capture_output=True, check=True,
            ).stdout
            return {
                "surface_sha256": "x" * 64,
                "computed_from_commit": commit_sha,
                "files": raw.decode("utf-8").split("\\0"),
            }
        """
    )
    findings = scan_python_source(source, "safe_c1.py")
    assert findings == [], findings


def test_c1_allows_filesystem_hash_when_no_committed_tree_claim() -> None:
    """Legacy filesystem hashing without computed_from_commit is acceptable."""
    source = textwrap.dedent(
        """
        import hashlib
        def legacy_compute_no_commit_claim(root):
            items = []
            for path in sorted(root.rglob("*")):
                if path.is_file():
                    data = path.read_bytes()
                    items.append((path.as_posix(), hashlib.sha256(data).hexdigest()))
            return {"surface_sha256": "x" * 64}
        """
    )
    findings = scan_python_source(source, "legacy_ok.py")
    assert findings == [], findings


def test_c1_allows_reading_specific_files_without_iteration() -> None:
    """Reading contracts.lock.json or registry JSON by name is not an included-surface hash."""
    source = textwrap.dedent(
        """
        import json
        def safe_lock_reader(lock_path, commit_sha):
            data = json.loads(lock_path.read_text(encoding="utf-8"))
            data["contract_surface_lock"] = {"computed_from_commit": commit_sha}
            return data
        """
    )
    findings = scan_python_source(source, "lock_reader.py")
    assert findings == [], findings


def test_c1_allows_git_cat_file_helper() -> None:
    source = textwrap.dedent(
        """
        def committed_with_helpers(root, commit_sha):
            blobs = _git_cat_file_batch(root, ["abcd"])
            return {
                "surface_sha256": "x" * 64,
                "computed_from_commit": commit_sha,
                "blobs": blobs,
            }
        """
    )
    findings = scan_python_source(source, "helper_safe.py")
    assert findings == [], findings


# ---------------------------------------------------------------------------
# C2: working-tree branch claims committed-tree provenance.
# ---------------------------------------------------------------------------


def test_c2_flags_working_tree_branch_setting_real_commit() -> None:
    source = textwrap.dedent(
        """
        def buggy_main(args, commit_sha):
            if args.working_tree:
                result = {"surface_sha256": "x" * 64}
                result["computed_from_commit"] = commit_sha
                return result
            return None
        """
    )
    findings = scan_python_source(source, "buggy_c2.py")
    assert "C2" in _rules(findings), findings


def test_c2_flags_working_tree_branch_dict_literal_with_commit() -> None:
    source = textwrap.dedent(
        """
        def buggy_main2(args, commit_sha):
            if args.working_tree:
                return {"surface_sha256": "x" * 64, "computed_from_commit": commit_sha}
            return None
        """
    )
    findings = scan_python_source(source, "buggy_c2b.py")
    assert "C2" in _rules(findings), findings


def test_c2_allows_working_tree_branch_setting_none() -> None:
    source = textwrap.dedent(
        """
        def safe_main(args, commit_sha):
            if args.working_tree:
                result = {"surface_sha256": "x" * 64}
                result["computed_from_commit"] = None
                result["provenance_mode"] = "working_tree"
                return result
            result = {"surface_sha256": "y" * 64}
            result["computed_from_commit"] = commit_sha
            return result
        """
    )
    findings = scan_python_source(source, "safe_c2.py")
    assert findings == [], findings


def test_c2_allows_committed_tree_only_else_branch_assignment() -> None:
    """The current fixed compute_contract_surface_hash.py pattern must pass."""
    source = textwrap.dedent(
        """
        def fixed_main(args, commit_sha):
            if args.working_tree or commit_sha is None:
                result = {"surface_sha256": "x" * 64}
                result["computed_from_repo"] = "subs"
                result["computed_from_commit"] = None
                result["provenance_mode"] = "working_tree"
                result["provenance_warning"] = "do not use"
            else:
                result = {"surface_sha256": "y" * 64}
                result["computed_from_repo"] = "subs"
                result["computed_from_commit"] = commit_sha
                result["provenance_mode"] = "committed_tree"
            return result
        """
    )
    findings = scan_python_source(source, "fixed.py")
    assert findings == [], findings


# ---------------------------------------------------------------------------
# C3: shutil.copytree fixture writes computed_from_commit without git init/archive.
# ---------------------------------------------------------------------------


def test_c3_flags_copytree_fixture_without_git_init() -> None:
    source = textwrap.dedent(
        """
        import shutil
        def buggy_fixture(src, dst, commit_sha):
            shutil.copytree(src, dst)
            return {
                "contract_surface_lock": {
                    "surface_sha256": "x" * 64,
                    "computed_from_commit": commit_sha,
                }
            }
        """
    )
    findings = scan_python_source(source, "buggy_c3.py")
    assert "C3" in _rules(findings), findings


def test_c3_allows_copytree_fixture_with_git_init() -> None:
    source = textwrap.dedent(
        """
        import shutil
        import subprocess
        def safe_fixture(src, dst, commit_sha):
            shutil.copytree(src, dst)
            subprocess.run(["git", "init"], cwd=dst, check=True)
            subprocess.run(["git", "add", "."], cwd=dst, check=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=dst, check=True)
            return {
                "contract_surface_lock": {
                    "surface_sha256": "x" * 64,
                    "computed_from_commit": commit_sha,
                }
            }
        """
    )
    findings = scan_python_source(source, "safe_c3.py")
    assert findings == [], findings


def test_c3_allows_copytree_fixture_with_init_helper() -> None:
    source = textwrap.dedent(
        """
        import shutil
        def safe_fixture_helper(src, dst, commit_sha):
            shutil.copytree(src, dst)
            _init_git_repo(dst)
            return {"contract_surface_lock": {"computed_from_commit": commit_sha}}
        """
    )
    findings = scan_python_source(source, "safe_c3b.py")
    assert findings == [], findings


def test_c3_allows_copytree_without_committed_tree_claim() -> None:
    source = textwrap.dedent(
        """
        import shutil
        def fixture_no_commit_claim(src, dst):
            shutil.copytree(src, dst)
            return {"surface_sha256": "x" * 64}
        """
    )
    findings = scan_python_source(source, "ok_copytree.py")
    assert findings == [], findings


# ---------------------------------------------------------------------------
# Relevance gate: irrelevant files are not scanned at all.
# ---------------------------------------------------------------------------


def test_relevance_gate_skips_unrelated_files(tmp_path: Path) -> None:
    irrelevant = tmp_path / "unrelated.py"
    irrelevant.write_text(
        textwrap.dedent(
            """
            import shutil, hashlib
            def some_helper(src, dst):
                shutil.copytree(src, dst)
                for p in dst.rglob("*"):
                    if p.is_file():
                        hashlib.sha256(p.read_bytes()).hexdigest()
                return {"unrelated_key": "value"}
            """
        ),
        encoding="utf-8",
    )
    from validate_contract_surface_provenance_modes import scan_python_file
    findings = scan_python_file(irrelevant)
    assert findings == [], (
        "Files that do not mention contract_surface_lock / computed_from_commit / "
        "surface_sha256 / compute_contract_surface must be skipped to avoid noise."
    )
