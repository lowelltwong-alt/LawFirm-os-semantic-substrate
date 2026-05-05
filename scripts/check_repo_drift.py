#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import validate_integrity
from scripts.validation import (
    validate_exception_events,
    validate_exception_governance,
)


REPORT_PATH = ROOT / "reports" / "repo-drift-report.md"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def active_example_paths(root: Path) -> list[Path]:
    paths: list[Path] = []
    for path in root.rglob("*.json"):
        if {"legacy", "archive"} & set(path.parts):
            continue
        paths.append(path)
    return sorted(paths)


def active_claim_paths(claim_id: str) -> list[Path]:
    claim_paths = []
    for path in active_example_paths(ROOT / "examples" / "claims"):
        payload = load_json(path)
        if payload.get("claim_id") == claim_id:
            claim_paths.append(path.relative_to(ROOT))
    return claim_paths


def check_flat_schema_registry_state(root: Path = ROOT) -> tuple[bool, str]:
    flat_registry = root / "schemas" / "schema_registry.json"
    if not flat_registry.exists():
        return True, "The stale flat schemas/schema_registry.json compatibility file has been removed."

    try:
        registry = load_json(flat_registry)
    except Exception as exc:
        return False, f"schemas/schema_registry.json exists but cannot be parsed: {exc}"

    if not isinstance(registry, dict):
        return False, "schemas/schema_registry.json exists but is not a flat path mapping."

    malformed_entries = [
        f"{schema_key} -> {schema_path!r}"
        for schema_key, schema_path in registry.items()
        if not isinstance(schema_path, str)
    ]
    if malformed_entries:
        return False, (
            "schemas/schema_registry.json exists but contains non-string flat-registry entries: "
            + ", ".join(sorted(malformed_entries))
        )

    missing_targets = [
        f"{schema_key} -> {schema_path}"
        for schema_key, schema_path in registry.items()
        if not (root / schema_path).exists()
    ]
    if missing_targets:
        return False, (
            "schemas/schema_registry.json exists and points to missing schema targets: "
            + ", ".join(sorted(missing_targets))
        )

    return True, "schemas/schema_registry.json exists and every referenced target path resolves."


def check_state() -> tuple[list[tuple[str, bool, str]], list[str]]:
    checks: list[tuple[str, bool, str]] = []
    failures: list[str] = []

    schema_registry = {
        entry["schema_id"]: entry
        for entry in load_json(ROOT / "registry" / "schema-registry.json")["schemas"]
    }
    readme_text = load_text(ROOT / "README.md")
    scoreboard_text = load_text(ROOT / "governance" / "ALIGNMENT_SCOREBOARD.md")

    checks.append(
        (
            "CHANGELOG present",
            (ROOT / "CHANGELOG.md").exists(),
            "CHANGELOG.md should exist because the repo already tracks release history.",
        )
    )
    checks.append(
        (
            "No claim v3 template file fabricated",
            not (ROOT / "templates" / "claim-template-v3.md").exists(),
            "templates/claim-template-v3.md should remain absent until the repo defines a governed template explicitly.",
        )
    )
    checks.append(
        (
            "Claim schema statuses are truthful",
            schema_registry.get("claim-schema-v3", {}).get("status") == "active"
            and schema_registry.get("claim-schema-v2", {}).get("status") == "deprecated",
            "registry/schema-registry.json should keep claim-schema-v3 active and claim-schema-v2 deprecated.",
        )
    )
    checks.append(
        (
            "Single active claim example for CLM-000101",
            active_claim_paths("CLM-000101") == [Path("examples/claims/CLM-000101.v3.json")],
            "Only examples/claims/CLM-000101.v3.json should remain active for CLM-000101.",
        )
    )
    checks.append(
        (
            "Legacy v2 claim preserved",
            (ROOT / "examples" / "claims" / "legacy" / "CLM-000101.v2.json").exists(),
            "The deprecated v2 claim should be preserved only under examples/claims/legacy/CLM-000101.v2.json.",
        )
    )
    checks.append(
        (
            "Archived standalone exception examples removed from active path",
            not (ROOT / "examples" / "exceptions" / "retrieval_miss_example.json").exists()
            and not (ROOT / "examples" / "exceptions" / "workflow_escalation_example.json").exists()
            and not (ROOT / "examples" / "exceptions" / "authority_conflict_override_example.json").exists()
            and (ROOT / "archive" / "examples" / "exceptions" / "retrieval_miss_example.json").exists()
            and (ROOT / "archive" / "examples" / "exceptions" / "workflow_escalation_example.json").exists()
            and (ROOT / "archive" / "examples" / "exceptions" / "authority_conflict_override_example.json").exists(),
            "Standalone exception examples should live under archive/examples/exceptions once they are removed from the active governed surface.",
        )
    )
    checks.append(
        (
            "README documents local checks",
            "## Local Checks" in readme_text,
            "README.md should include a Local Checks section with the reproducible setup and validation commands.",
        )
    )

    banned_scoreboard_phrases = [
        "all 35 validators pass via `bash scripts/run_full_audit.sh`",
        "Template: `templates/claim-template-v3.md`",
        "No LICENSE, NOTICE, or CHANGELOG file exists",
    ]
    scoreboard_ok = not any(phrase in scoreboard_text for phrase in banned_scoreboard_phrases)
    checks.append(
        (
            "Scoreboard no longer repeats stale claims",
            scoreboard_ok,
            "governance/ALIGNMENT_SCOREBOARD.md should not claim a missing claim v3 template, a missing CHANGELOG, or a blanket passed-audit status without current evidence.",
        )
    )

    flat_registry_ok, flat_registry_note = check_flat_schema_registry_state(ROOT)
    checks.append(
        (
            "Flat schema registry compatibility surface is not stale",
            flat_registry_ok,
            flat_registry_note,
        )
    )

    integrity_failures = validate_integrity.collect_failures(ROOT)
    checks.append(
        (
            "Integrity validator surface is green",
            not integrity_failures,
            "scripts/validate_integrity.py should pass after active example canon and reference cleanup.",
        )
    )
    failures.extend(integrity_failures)

    exception_event_failures = validate_exception_events.collect_failures()
    checks.append(
        (
            "Exception-event surface is green",
            not exception_event_failures,
            "scripts/validation/validate_exception_events.py should pass once the active exception chain is coherent.",
        )
    )
    failures.extend(exception_event_failures)

    exception_governance_failures = validate_exception_governance.collect_failures()
    checks.append(
        (
            "Exception governance chain is green",
            not exception_governance_failures,
            "scripts/validation/validate_exception_governance.py should keep passing for the active EXC -> PV -> AP -> PD chain.",
        )
    )
    failures.extend(exception_governance_failures)

    return checks, failures


def write_report(checks: list[tuple[str, bool, str]], failures: list[str]) -> None:
    REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)

    lines = [
        "# Repo Drift Report",
        "",
        "| Check | Result | Notes |",
        "| --- | --- | --- |",
    ]
    for label, passed, note in checks:
        lines.append(f"| {label} | {'PASS' if passed else 'FAIL'} | {note} |")

    if failures:
        lines.extend(["", "## Failure Details", ""])
        for failure in failures:
            lines.append(f"- {failure}")
    else:
        lines.extend(["", "## Failure Details", "", "- None"])

    REPORT_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    checks, failures = check_state()
    write_report(checks, failures)

    failing_checks = [label for label, passed, _ in checks if not passed]
    if failing_checks or failures:
        print("Repo drift check failed.")
        for label in failing_checks:
            print(f" - {label}")
        for failure in failures:
            print(f" - {failure}")
        return 1

    print(f"Repo drift check passed. Report written to {REPORT_PATH}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
