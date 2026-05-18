"""Tests for the PR-05.5 controlled-vocabulary registry, its schema mirrors,
and the validator script.

These tests cover:
  - The registry file exists and is well-formed.
  - Each schema's ``enum`` array equals the corresponding vocabulary.
  - The validator returns a clean result for the current workspace.
  - The validator detects synthetic violations (AST-scan style).
"""
from __future__ import annotations

import ast
import json
import sys
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE_ROOT = REPO_ROOT.parent
SCRIPTS = REPO_ROOT / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))

from validate_runtime_reason_codes import (  # noqa: E402
    REGULATED_FIELDS,
    SCHEMA_BINDINGS,
    Finding,
    load_registry,
    scan_runtime_repo,
    validate,
    validate_schema_enums,
)


REGISTRY_PATH = REPO_ROOT / "registry" / "runtime-reason-codes-registry.json"


# ------------------------------ registry shape ------------------------------


def test_registry_file_exists() -> None:
    assert REGISTRY_PATH.is_file(), "PR-05.5 requires runtime-reason-codes-registry.json"


def test_registry_has_four_required_vocabularies() -> None:
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    vocabs = data["vocabularies"]
    expected = {
        "execution_decision.reason_codes",
        "exception_lake.admission_reason_codes",
        "defect_record.defect_classes",
        "runtime.semantic_mutation_actions",
    }
    assert set(vocabs.keys()) == expected, f"vocabularies disagree: have {set(vocabs)}"


def test_registry_values_are_lowercase_snake_strings() -> None:
    data = json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))
    for name, body in data["vocabularies"].items():
        for v in body["values"]:
            assert v == v.lower(), f"{name}: {v!r} must be lowercase"
            assert " " not in v, f"{name}: {v!r} must use snake_case"
            assert v.replace("_", "").isalnum(), f"{name}: {v!r} must be [a-z0-9_]+"


# ----------------------- schema enum / registry parity -----------------------


def test_schema_enums_equal_registry_for_each_binding() -> None:
    vocabs = load_registry(REPO_ROOT)
    errors = validate_schema_enums(REPO_ROOT, vocabs)
    assert errors == [], "\n".join(errors)


def test_each_regulated_field_has_a_schema_binding() -> None:
    bound_vocabs = {vocab for _, _, vocab in SCHEMA_BINDINGS}
    declared = {v for v in REGULATED_FIELDS.values()}
    # Regulated fields (kwarg/dict-literal scan) must have schema bindings.
    assert declared <= bound_vocabs, f"regulated fields not bound to a schema: {declared - bound_vocabs}"


# ------------------- workspace-wide validation (integration) -----------------


def _has_sibling_runtime_repos() -> bool:
    return any((WORKSPACE_ROOT / name).is_dir() for name in (
        "LawFirm-os-orchestrator",
        "LawFirm-os-exceptions-lake-runtime",
        "LawFirm-os-exceptions-lake-runtime-main",
    ))


def test_current_workspace_has_no_runtime_reason_code_violations() -> None:
    if not _has_sibling_runtime_repos():
        pytest.skip("sibling runtime repos not present; substrate-standalone CI")
    result = validate(WORKSPACE_ROOT, REPO_ROOT)
    assert result.schema_enum_mismatches == [], "\n".join(result.schema_enum_mismatches)
    assert result.findings == [], "\n".join(f.render() for f in result.findings)


# ----------------- synthetic AST-scan unit tests for the validator -----------


def test_scanner_catches_kwarg_literal_outside_vocabulary(tmp_path: Path) -> None:
    fake_repo = tmp_path / "fake-runtime"
    fake_src = fake_repo / "src" / "fake_pkg"
    fake_src.mkdir(parents=True)
    (fake_src / "__init__.py").write_text("", encoding="utf-8")
    (fake_src / "module.py").write_text(
        "def f(**kw):\n"
        "    return kw\n"
        "x = f(reason_code='totally_invented_code')\n"
        "y = f(reason_code='unknown_tool')\n",
        encoding="utf-8",
    )
    vocabs = {"execution_decision.reason_codes": {"unknown_tool"}, "exception_lake.admission_reason_codes": set(), "defect_record.defect_classes": set()}
    findings = scan_runtime_repo(fake_repo, vocabs, repo_label="fake-runtime")
    bad = [f for f in findings if f.literal == "totally_invented_code"]
    good = [f for f in findings if f.literal == "unknown_tool"]
    assert len(bad) == 1, "scanner must flag invented reason_code literals"
    assert good == [], "registered literals must not be flagged"


def test_scanner_catches_dict_literal_outside_vocabulary(tmp_path: Path) -> None:
    fake_repo = tmp_path / "fake-runtime"
    fake_src = fake_repo / "src" / "fake_pkg"
    fake_src.mkdir(parents=True)
    (fake_src / "__init__.py").write_text("", encoding="utf-8")
    (fake_src / "module.py").write_text(
        "rec = {\n"
        "    'admission_reason_code': 'invented_reason',\n"
        "}\n",
        encoding="utf-8",
    )
    vocabs = {"execution_decision.reason_codes": set(), "exception_lake.admission_reason_codes": {"passed_dry_run_admission"}, "defect_record.defect_classes": set()}
    findings = scan_runtime_repo(fake_repo, vocabs, repo_label="fake-runtime")
    assert any(f.literal == "invented_reason" and f.field == "admission_reason_code" for f in findings)


def test_scanner_ignores_non_regulated_fields(tmp_path: Path) -> None:
    fake_repo = tmp_path / "fake-runtime"
    fake_src = fake_repo / "src" / "fake_pkg"
    fake_src.mkdir(parents=True)
    (fake_src / "__init__.py").write_text("", encoding="utf-8")
    (fake_src / "module.py").write_text(
        "def f(**kw):\n    return kw\n"
        "f(some_other_field='unregistered_but_ignored')\n",
        encoding="utf-8",
    )
    vocabs = {k: set() for k in ("execution_decision.reason_codes", "exception_lake.admission_reason_codes", "defect_record.defect_classes")}
    findings = scan_runtime_repo(fake_repo, vocabs, repo_label="fake-runtime")
    assert findings == [], "scanner must only flag regulated field names"


def test_scanner_catches_subscript_assign_outside_vocabulary(tmp_path: Path) -> None:
    fake_repo = tmp_path / "fake-runtime"
    fake_src = fake_repo / "src" / "fake_pkg"
    fake_src.mkdir(parents=True)
    (fake_src / "__init__.py").write_text("", encoding="utf-8")
    (fake_src / "module.py").write_text(
        "d = {}\n"
        "d['defect_class'] = 'fully_invented_class'\n",
        encoding="utf-8",
    )
    vocabs = {"execution_decision.reason_codes": set(), "exception_lake.admission_reason_codes": set(), "defect_record.defect_classes": {"route_mismatch"}}
    findings = scan_runtime_repo(fake_repo, vocabs, repo_label="fake-runtime")
    assert any(f.literal == "fully_invented_class" and f.field == "defect_class" for f in findings)
