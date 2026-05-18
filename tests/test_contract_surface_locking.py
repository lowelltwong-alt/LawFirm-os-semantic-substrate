from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from contract_surface import compute_contract_surface


def _copy_substrate(tmp_path: Path) -> Path:
    target = tmp_path / "substrate"
    for rel in ("schemas", "registry", "governance", "manifests"):
        src = REPO_ROOT / rel
        if src.exists():
            shutil.copytree(src, target / rel)
    return target


def test_managed_patch_decisions_do_not_change_contract_surface_hash(tmp_path: Path) -> None:
    substrate = _copy_substrate(tmp_path)
    before = compute_contract_surface(substrate)["surface_sha256"]
    decision = substrate / "registry" / "managed-patch-decisions" / "example" / "decision.json"
    decision.parent.mkdir(parents=True, exist_ok=True)
    decision.write_text(json.dumps({"decision": "audit only"}) + "\n", encoding="utf-8")
    after = compute_contract_surface(substrate)["surface_sha256"]
    assert after == before


def test_schema_change_changes_contract_surface_hash(tmp_path: Path) -> None:
    substrate = _copy_substrate(tmp_path)
    before = compute_contract_surface(substrate)["surface_sha256"]
    schema = next((substrate / "schemas").glob("*.schema.json"), None)
    if schema is None:
        schema = substrate / "schemas" / "synthetic.schema.json"
        schema.parent.mkdir(parents=True, exist_ok=True)
        schema.write_text("{}\n", encoding="utf-8")
    original = schema.read_text(encoding="utf-8")
    schema.write_text(original.rstrip() + "\n", encoding="utf-8")
    schema.write_text(schema.read_text(encoding="utf-8") + " ", encoding="utf-8")
    after = compute_contract_surface(substrate)["surface_sha256"]
    assert after != before


def test_contract_surface_registry_validates() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "validate_contract_surface_registry.py"), "--substrate", str(REPO_ROOT)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout


def test_contract_surface_hash_cli_outputs_lock_fields(tmp_path: Path) -> None:
    out = tmp_path / "surface.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "compute_contract_surface_hash.py"), "--substrate", str(REPO_ROOT), "--out", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["surface_sha256"]
    assert data["hash_algorithm"] == "lawfirm_os_contract_surface_sha256.v1"
    assert data["included_file_count"] > 0


def test_contract_surface_hash_cli_default_mode_is_committed_tree(tmp_path: Path) -> None:
    out = tmp_path / "surface.json"
    result = subprocess.run(
        [sys.executable, str(SCRIPTS / "compute_contract_surface_hash.py"), "--substrate", str(REPO_ROOT), "--out", str(out)],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["provenance_mode"] == "committed_tree"
    assert isinstance(data["computed_from_commit"], str) and len(data["computed_from_commit"]) == 40
    assert "provenance_warning" not in data


def test_contract_surface_hash_cli_working_tree_mode_omits_committed_provenance(tmp_path: Path) -> None:
    out = tmp_path / "surface.json"
    result = subprocess.run(
        [
            sys.executable,
            str(SCRIPTS / "compute_contract_surface_hash.py"),
            "--substrate",
            str(REPO_ROOT),
            "--working-tree",
            "--out",
            str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr + result.stdout
    data = json.loads(out.read_text(encoding="utf-8"))
    assert data["provenance_mode"] == "working_tree", (
        "Working-tree mode must declare provenance_mode = 'working_tree' so downstream consumers "
        "cannot mistake working-tree bytes for committed-tree provenance."
    )
    assert data["computed_from_commit"] is None, (
        "Working-tree output must NOT claim committed-tree provenance. "
        "computed_from_commit must be null when --working-tree is passed."
    )
    assert "provenance_warning" in data and "working-tree" in data["provenance_warning"].lower(), (
        "Working-tree output must carry an explicit warning that this hash is not suitable for "
        "consumer contracts.lock.json committed-tree pins."
    )


def test_update_consumer_contract_surface_locks_uses_committed_tree(tmp_path: Path) -> None:
    """The consumer-lock producer must hash committed Git-tree bytes, never working-tree bytes."""
    source = (SCRIPTS / "update_consumer_contract_surface_locks.py").read_text(encoding="utf-8")
    assert "compute_contract_surface_from_git_tree" in source, (
        "update_consumer_contract_surface_locks.py must use compute_contract_surface_from_git_tree "
        "(committed-tree hashing) when writing consumer locks."
    )
    assert "compute_contract_surface(substrate, args.surface_id)" not in source, (
        "update_consumer_contract_surface_locks.py must NOT use the working-tree compute_contract_surface "
        "when writing consumer locks; that path would silently claim committed-tree provenance for "
        "mutable working-tree bytes."
    )
