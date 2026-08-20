# Real Work Shadow Mode Pilot Gates

Status: control-plane gate for any move from synthetic examples toward real
legal work.

## Purpose

This document defines the minimum gate before LawFirm OS components may observe
or assist real legal work in shadow mode. Shadow mode means observe-only,
proposal-only, and review-only. It does not authorize production decisions,
external writes, legal advice, client communications, carrier submissions,
court filings, billing actions, matter opening, or conflict clearance.

## Gate Stack

Before any real-work shadow-mode pilot starts, the owner must record:

- owner approval;
- attorney approval for the scoped workflow;
- privacy and compliance approval;
- jurisdiction and practice-area scope;
- data-class inventory;
- privilege and access-control review;
- vendor and trace-retention review if any model or simulator provider is used;
- conflict, engagement, and matter-opening boundary;
- eval fixture baseline and pass/fail threshold;
- reviewer checklist and escalation path;
- rollback and kill switch;
- audit and evidence-retention plan;
- blocked downstream actions.

## Required Pilot Limits

A real-work shadow-mode pilot must:

- run beside the human workflow, not inside the production decision path;
- use the narrowest approved data classes;
- default to redaction, hashing, or metadata where feasible;
- keep model and simulator outputs as proposals only;
- preserve attorney review before reliance;
- log reviewer decisions separately from model or simulator output;
- stop on privilege uncertainty, scope drift, jurisdiction uncertainty,
  connector-write requests, or attempted production reliance.

## Non-Authorization

This gate does not authorize:

- legal advice;
- client, carrier, court, filing, billing, or document-management submission;
- external connector writes;
- conflict clearance;
- matter opening;
- budget approval or submission;
- Exception Lake or SQLite writes of raw legal payloads;
- canonical route, event-class, schema, or policy mutation;
- production automation.

## Blocked Owner Decisions

These questions must remain blocked until the owner, attorney reviewer, privacy
reviewer, and compliance reviewer make a recorded decision:

- Which data classes may enter a real-work pilot?
- Which users may see outputs and reviewer packets?
- Which provider traces, logs, or telemetry are allowed?
- Which jurisdiction and practice-area assumptions are in scope?
- Which downstream actions remain manually blocked?
- Which compensating control applies if a repo cannot enforce branch
  protection?

## Required Invariant Tokens

Validators and downstream mirrors may use these exact tokens to verify that the
gate has not drifted:

- shadow_mode_is_observe_only
- real_client_or_matter_data_authorized_false_until_owner_legal_compliance_approval
- legal_advice_authorized_false
- client_carrier_court_submission_authorized_false
- connector_write_authorized_false
- conflict_clearance_authorized_false
- matter_opening_authorized_false
- budget_submission_authorized_false
- attorney_review_required
- privilege_privacy_access_control_review_required
- rollback_and_kill_switch_required
- promotion_decision_required_before_production
- intake_branch_protection_blocker_must_be_resolved_or_compensating_control_recorded
