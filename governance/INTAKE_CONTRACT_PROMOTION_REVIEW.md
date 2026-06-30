# Intake Contract Promotion Review

## Purpose

This document governs the first Semantic Substrate review docket for
`LawFirm-os-intake` candidate contracts. The machine-readable docket lives at
`registry/intake-contract-promotion-review-registry.json`.

The docket starts Phase 3 intake-to-budget promotion work without assigning
canonical schema IDs, route IDs, event classes, lifecycle terms, or runtime
authority.

## Source Package

The source package is
`cross-repo-promotion-package.intake-to-budget.v0_1` from `LawFirm-os-intake`.
Only the proposals targeting `LawFirm-os-semantic-substrate` are in scope here:

- `substrate.intake-source-and-evidence-refs.v0_1`
- `substrate.human-confirmation-and-candidates.v0_1`
- `substrate.budget-and-event-labels.v0_1`

The source package is candidate evidence. It is not promoted canon.

## Review Tracks

### Source Grounding And Evidence Refs

Compare intake source, segment, inventory, evidence-completeness, context
boundary, and review-package fields against existing Substrate source-ref,
passage-ref, claim-ref, coverage-record, verification-record, and legal context
bundle surfaces.

The main review question is which fields are general source-grounding contracts
and which should remain intake-local evaluation detail.

### Human Confirmation And Candidate Lifecycle

Review human confirmation, correction, unknown, declined/referred, human-only,
party-role, matter-family, representation-posture, deadline, and missing-info
candidate behavior against lifecycle and human approval doctrine.

The main review question is whether the candidate lifecycle needs a promoted
Substrate contract before Orchestrator or Skills Registry adoption.

### Budget Contracts And Event Label Boundaries

Review legal budget proposal, scenario set, driver, carrier guideline,
actual-cost comparison, reviewed-learning, and intake-event label candidates
against existing exception, pressure, adaptation, promotion, and route/event
surfaces.

The main review question is how to preserve the line between budget proposal,
budget approval, budget submission, conflict clearance, matter opening, Lake
admission, and governed learning.

## Required Gates

Before any candidate intake contract can become canonical:

- compare it against existing `registry/schema-registry.json` entries;
- record whether fields are canonical, intake-local, runtime-owned, or rejected;
- decide route IDs and event classes only through Substrate governance;
- require a reviewed `promotion-decision` before schema or registry mutation;
- preserve synthetic-only and no-real-data-pilot boundaries;
- preserve no external write, no budget submission, no conflict conclusion, and
  no matter-opening authority.

## Non-Authorization

This docket does not:

- promote any intake schema;
- assign canonical IDs;
- create Orchestrator routes;
- create Exception Lake admission records;
- authorize SQLite migrations;
- authorize real client or matter data;
- authorize carrier portal, billing, email, court, or document-management
  connectors;
- authorize budget submission, appeal submission, conflict clearance, matter
  opening, or engagement decisions.

## Validation

`scripts/validate_intake_contract_promotion_review.py` validates the registry
shape and checks that this governance note names the source package, every
Substrate-targeted proposal, and the non-authorization boundary.
