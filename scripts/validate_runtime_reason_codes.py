"""Validate that runtime repos do not invent reason_code / admission_reason_code
/ defect_class values. The source of truth is
``registry/runtime-reason-codes-registry.json`` (substrate). The validator
AST-scans each runtime repo's ``src/`` tree and asserts that every kwarg or
dict-literal value bound to a regulated field name is a registered string.

The same vocabularies are mirrored as ``enum`` arrays in three substrate
schemas; the validator additionally asserts schema-enum ↔ registry equality.

This script is the contract-side enforcement of PR-05.5. It is intended for
substrate CI but can be invoked locally:

    python scripts/validate_runtime_reason_codes.py --workspace ..

Exit code: 0 on success, 1 on any violation.
"""
from __future__ import annotations

import argparse
import ast
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable

REGULATED_FIELDS: dict[str, str] = {
    "reason_code": "execution_decision.reason_codes",
    "admission_reason_code": "exception_lake.admission_reason_codes",
    "defect_class": "defect_record.defect_classes",
}

SCHEMA_BINDINGS: list[tuple[str, str, str]] = [
    ("schemas/execution-decision.schema.json",          "reason_code",          "execution_decision.reason_codes"),
    ("schemas/exception-lake-admission-record.schema.json", "admission_reason_code", "exception_lake.admission_reason_codes"),
    ("schemas/defect-record.schema.json",               "defect_class",         "defect_record.defect_classes"),
]

REPO_ALIASES: dict[str, list[str]] = {
    "LawFirm-os-orchestrator": ["LawFirm-os-orchestrator", "LawFirm-os-orchestrator-main"],
    "LawFirm-os-exceptions-lake-runtime": [
        "LawFirm-os-exceptions-lake-runtime",
        "LawFirm-os-exceptions-lake-runtime-main",
    ],
    "LawFirm-os-legal-knowledge-runtime": [
        "LawFirm-os-legal-knowledge-runtime",
        "LawFirm-os-legal-knowledge-runtime-main",
    ],
    "LawFirm-os-skills-registry": [
        "LawFirm-os-skills-registry",
        "LawFirm-os-skills-registry-main",
    ],
}


@dataclass
class Finding:
    repo: str
    file: Path
    line: int
    field: str
    literal: str
    vocabulary: str

    def render(self) -> str:
        return (
            f"{self.repo}: {self.file.as_posix()}:{self.line}: "
            f"{self.field}={self.literal!r} is not a member of {self.vocabulary}"
        )


@dataclass
class ValidationResult:
    findings: list[Finding] = field(default_factory=list)
    schema_enum_mismatches: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.findings and not self.schema_enum_mismatches


def load_registry(substrate_root: Path) -> dict[str, set[str]]:
    path = substrate_root / "registry" / "runtime-reason-codes-registry.json"
    if not path.is_file():
        raise FileNotFoundError(f"missing controlled-vocabulary registry: {path}")
    raw = json.loads(path.read_text(encoding="utf-8"))
    vocabs: dict[str, set[str]] = {}
    for name, body in raw["vocabularies"].items():
        values = body.get("values")
        if not isinstance(values, list) or not all(isinstance(v, str) for v in values):
            raise ValueError(f"vocabulary {name} must have a list of string values")
        vocabs[name] = set(values)
    return vocabs


def find_repo(workspace: Path, logical: str) -> Path | None:
    for name in REPO_ALIASES.get(logical, [logical]):
        candidate = workspace / name
        if candidate.is_dir():
            return candidate
    return None


def _iter_py(root: Path) -> Iterable[Path]:
    src = root / "src"
    base = src if src.is_dir() else root
    for p in sorted(base.rglob("*.py")):
        parts = set(p.relative_to(base).parts)
        if "__pycache__" in parts or ".pytest_cache" in parts:
            continue
        yield p


def _walk_kwarg_literals(tree: ast.AST) -> Iterable[tuple[int, str, str]]:
    """Yield (lineno, field_name, literal_value) for every kwarg whose name
    matches a regulated field and whose value is a string literal.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            for kw in node.keywords:
                if kw.arg in REGULATED_FIELDS and isinstance(kw.value, ast.Constant) and isinstance(kw.value.value, str):
                    yield kw.lineno, kw.arg, kw.value.value


def _walk_dict_literals(tree: ast.AST) -> Iterable[tuple[int, str, str]]:
    """Yield (lineno, field_name, literal_value) for dict literals whose key
    matches a regulated field and whose value is a string literal.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for k, v in zip(node.keys, node.values):
                if isinstance(k, ast.Constant) and isinstance(k.value, str) and k.value in REGULATED_FIELDS:
                    if isinstance(v, ast.Constant) and isinstance(v.value, str):
                        yield v.lineno, k.value, v.value


def _walk_subscript_assigns(tree: ast.AST) -> Iterable[tuple[int, str, str]]:
    """Yield (lineno, field_name, literal_value) for assignments like
    ``d["reason_code"] = "literal"``.
    """
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if (
                    isinstance(target, ast.Subscript)
                    and isinstance(target.slice, ast.Constant)
                    and isinstance(target.slice.value, str)
                    and target.slice.value in REGULATED_FIELDS
                    and isinstance(node.value, ast.Constant)
                    and isinstance(node.value.value, str)
                ):
                    yield node.value.lineno, target.slice.value, node.value.value


def scan_runtime_repo(repo_root: Path, vocabs: dict[str, set[str]], repo_label: str) -> list[Finding]:
    findings: list[Finding] = []
    for py in _iter_py(repo_root):
        try:
            tree = ast.parse(py.read_text(encoding="utf-8"))
        except SyntaxError:
            continue
        for lineno, fld, literal in (
            *_walk_kwarg_literals(tree),
            *_walk_dict_literals(tree),
            *_walk_subscript_assigns(tree),
        ):
            vocab_name = REGULATED_FIELDS[fld]
            allowed = vocabs.get(vocab_name, set())
            if literal not in allowed:
                findings.append(
                    Finding(
                        repo=repo_label,
                        file=py.relative_to(repo_root),
                        line=lineno,
                        field=fld,
                        literal=literal,
                        vocabulary=vocab_name,
                    )
                )
    return findings


def validate_schema_enums(substrate_root: Path, vocabs: dict[str, set[str]]) -> list[str]:
    errors: list[str] = []
    for rel, _, vocab_name in SCHEMA_BINDINGS:
        schema_path = substrate_root / rel
        if not schema_path.is_file():
            errors.append(f"missing schema: {rel}")
            continue
        schema = json.loads(schema_path.read_text(encoding="utf-8"))
        # Navigate to the relevant property using the binding's tail.
        # All three are at properties/<field>/enum.
        properties = schema.get("properties", {})
        field_name = rel.split("/")[-1].replace(".schema.json", "")  # not used; introspect from REGULATED_FIELDS instead
        # Recover the regulated field name from REGULATED_FIELDS reverse map.
        regulated_field = next((fld for fld, v in REGULATED_FIELDS.items() if v == vocab_name), None)
        if regulated_field is None:
            errors.append(f"no regulated field maps to {vocab_name}")
            continue
        prop = properties.get(regulated_field, {})
        enum_values = prop.get("enum")
        if not isinstance(enum_values, list):
            errors.append(f"{rel}: properties.{regulated_field}.enum missing or not a list")
            continue
        if set(enum_values) != vocabs.get(vocab_name, set()):
            in_schema_only = sorted(set(enum_values) - vocabs.get(vocab_name, set()))
            in_registry_only = sorted(vocabs.get(vocab_name, set()) - set(enum_values))
            errors.append(
                f"{rel}: properties.{regulated_field}.enum disagrees with registry {vocab_name}: "
                f"in_schema_only={in_schema_only} in_registry_only={in_registry_only}"
            )
    return errors


def validate(workspace: Path, substrate_root: Path | None = None) -> ValidationResult:
    substrate_root = substrate_root or (workspace / "LawFirm-os-semantic-substrate")
    if not substrate_root.is_dir():
        raise SystemExit(f"substrate not found at {substrate_root}")
    vocabs = load_registry(substrate_root)
    result = ValidationResult()
    result.schema_enum_mismatches = validate_schema_enums(substrate_root, vocabs)
    for logical in REPO_ALIASES:
        repo = find_repo(workspace, logical)
        if repo is None:
            continue
        result.findings.extend(scan_runtime_repo(repo, vocabs, logical))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate runtime reason-code controlled vocabulary.")
    parser.add_argument("--workspace", default=".", help="workspace root containing substrate + sibling runtime repos")
    parser.add_argument("--substrate", default=None, help="path to substrate (defaults to <workspace>/LawFirm-os-semantic-substrate)")
    args = parser.parse_args()
    workspace = Path(args.workspace).resolve()
    substrate = Path(args.substrate).resolve() if args.substrate else None
    result = validate(workspace, substrate)
    if result.schema_enum_mismatches:
        print("Schema enum vs registry mismatches:", file=sys.stderr)
        for e in result.schema_enum_mismatches:
            print(f"  - {e}", file=sys.stderr)
    if result.findings:
        print("Runtime literal vs registry violations:", file=sys.stderr)
        for f in result.findings:
            print(f"  - {f.render()}", file=sys.stderr)
    if result.ok:
        print("runtime reason-codes validation passed.")
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
