# Litigation Simulation Adapter Boundary

Status: control-plane boundary for future simulator adapters.

## Purpose

This boundary defines how LawFirm OS may later evaluate adapters for Albers
mock-trial style tools, ALS simulator tools, or other litigation simulation
systems.

The boundary is intentionally narrow. A simulator may support training,
scenario rehearsal, eval design, reviewer calibration, and decision-support
research. It may not become legal advice, trial-strategy authority, settlement
authority, court-facing material, or production workflow authority.

## Allowed First Use

The first allowed use is synthetic-only adapter discovery:

- inventory the external simulator's input and output shapes;
- map those shapes to LawFirm OS source, evidence, review, and eval concepts;
- run local synthetic fixtures only;
- produce reviewer packets for attorney and owner assessment;
- record gaps, risks, and open questions before any real-data pilot.

## Required Adapter Phases

1. Inventory and authority review.
2. Synthetic no-write replay.
3. Adversarial eval and source-binding review.
4. Attorney, owner, privacy, and compliance decision.
5. Shadow-mode pilot only after the real-work gate is satisfied.
6. Production connector review only after a separate promotion decision.

No phase may skip the previous phase.

## Non-Authorization

This boundary does not authorize:

- real client or matter data in any simulator;
- privileged material;
- external writes;
- client, carrier, court, filing, billing, or document-management submission;
- Exception Lake or SQLite persistence;
- conflict clearance;
- matter opening;
- budget approval or submission;
- settlement recommendation;
- trial strategy reliance;
- canonical schema, route, event-class, or policy mutation.

## Ownership

`LawFirm-os-semantic-substrate` owns this boundary and any canonical promotion
decision. `LawFirm-os-orchestrator` may later own a local no-write adapter
runner if Substrate authorizes the contract shape. Runtime repos may not treat
simulator convenience as governance, legal, compliance, or litigation authority.

## Minimum Evidence Before Adapter Work

Every candidate adapter needs:

- simulator name and version;
- vendor, license, and data-retention posture;
- input and output schema sketch;
- data classes requested by the adapter;
- jurisdiction, practice-area, and matter-stage assumptions;
- source-binding and provenance strategy;
- eval fixtures and adversarial cases;
- attorney review packet shape;
- rollback and kill-switch plan;
- explicit list of outputs that must never be used with clients, carriers,
  courts, filings, or settlement authority.

## Required Invariant Tokens

Validators and downstream mirrors may use these exact tokens to verify that the
boundary has not drifted:

- simulation_output_is_decision_support_only
- no_legal_advice_authority
- no_trial_strategy_authority
- no_settlement_authority
- no_client_or_matter_data_without_approved_real_work_gate
- no_external_write_or_connector_action
- no_exception_lake_or_sqlite_write
- attorney_review_required_before_reliance
- jurisdiction_scope_required
- provenance_and_source_binding_required
- substrate_promotion_required_before_canonical_contract
- owner_legal_compliance_decision_required_before_real_adapter_use
