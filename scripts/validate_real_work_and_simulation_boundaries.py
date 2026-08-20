#!/usr/bin/env python3
"""Validate simulator-adapter and real-work shadow-mode boundary docs."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

REQUIRED_TOKENS = {
    "governance/LITIGATION_SIMULATION_ADAPTER_BOUNDARY.md": {
        "simulation_output_is_decision_support_only",
        "no_legal_advice_authority",
        "no_trial_strategy_authority",
        "no_settlement_authority",
        "no_client_or_matter_data_without_approved_real_work_gate",
        "no_external_write_or_connector_action",
        "no_exception_lake_or_sqlite_write",
        "attorney_review_required_before_reliance",
        "jurisdiction_scope_required",
        "provenance_and_source_binding_required",
        "substrate_promotion_required_before_canonical_contract",
        "owner_legal_compliance_decision_required_before_real_adapter_use",
    },
    "governance/REAL_WORK_SHADOW_MODE_PILOT_GATES.md": {
        "shadow_mode_is_observe_only",
        "real_client_or_matter_data_authorized_false_until_owner_legal_compliance_approval",
        "legal_advice_authorized_false",
        "client_carrier_court_submission_authorized_false",
        "connector_write_authorized_false",
        "conflict_clearance_authorized_false",
        "matter_opening_authorized_false",
        "budget_submission_authorized_false",
        "attorney_review_required",
        "privilege_privacy_access_control_review_required",
        "rollback_and_kill_switch_required",
        "promotion_decision_required_before_production",
        "intake_branch_protection_blocker_must_be_resolved_or_compensating_control_recorded",
    },
}


class BoundaryValidationError(ValueError):
    """Raised when simulation or real-work boundaries drift."""


def validate_boundaries(root: Path = ROOT) -> None:
    for rel, tokens in REQUIRED_TOKENS.items():
        path = root / rel
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as exc:
            raise BoundaryValidationError(f"{rel} is unreadable: {exc}") from exc
        missing = sorted(token for token in tokens if token not in text)
        if missing:
            raise BoundaryValidationError(f"{rel} missing required tokens: {missing}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args(argv)
    try:
        validate_boundaries(args.root)
    except BoundaryValidationError as exc:
        print(f"Boundary validation failed: {exc}", file=sys.stderr)
        return 1
    print("Real-work and simulation boundary validation passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
