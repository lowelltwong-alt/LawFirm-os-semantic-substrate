# Insurance-Defense Budget Learning Loop POC

## Purpose

Define a bounded synthetic POC for a JSON-first insurance-defense budget
learning loop that mirrors the output shape of a sanitized budget workbook
without checking that workbook into the repository.

This POC is:

- synthetic
- non-production
- non-canonical
- governed by the current exception-to-promotion boundary

It documents the contract posture for a separate runtime implementation. It
does not implement runtime storage, connectors, dashboards, or live ingestion
in this repository.

## Scope

Use one synthetic matter family only:

- `synthetic_auto_bi_defense_v1`

The first learning loop is:

1. synthetic matter intake
2. deterministic driver classification
3. template-shaped budget draft JSON
4. supported exception-event candidates
5. pressure-vector candidates
6. review packet
7. no promotion unless human-approved

The first output is a template-shaped JSON object, not a workbook export.

## Workbook-Shape Posture

The sanitized workbook is used only as a structural reference for:

- matter-header fields
- phase and task ordering
- budget column ordering
- original and updated budget summary labels

The runtime must:

- encode the exact task-row inventory in code or config
- preserve every template row even if unpopulated
- keep all amounts synthetic, draft, and test-only

The runtime must not:

- check in the workbook binary
- infer real Law Firm rates, hours, budgets, staffing rules, or carrier rules
- claim production budget accuracy or validated business value

## Draft Output Contract

The contract repository owns the first-pass workbook-shaped draft contract:

- `view-budget-workbook-v1`

This object is a governed presentation draft and review-packet input. It is
not canonical authority and it does not bypass the current promotion boundary.

The contract includes:

- template title and instruction note
- workbook header fields
- exact `L100`, `L200`, `L300`, `L400`, `L500`, and `E100` row ordering
- amount columns for original budget, billed to date, remaining, and new budget
- original and updated budget summary values
- learning metadata and non-claims

## Current-Contract Mapping

This first pass must reuse the current governed `exception-event` classes and
routes already defined in the repository.

| Trigger family | Current event class | Route | Pressure class | Expected review path |
|---|---|---|---|---|
| synthetic guideline lookup miss | `retrieval_miss` | `route.retrieval_miss.v1` | `retrieval_quality_pressure` | knowledge-owner review and retrieval tuning |
| supported budget workflow issue | `workflow_escalation` | `route.workflow_escalation.v1` | `workflow_friction_pressure` | operations or billing-integrity review |
| governance blocker | existing dry-run preflight path first | no new route in this pass | none in first pass | governance remediation before any final draft output |

For the first implementation:

- use `route_for_review` as the raw action
- keep `promotion_gate_required: true`
- never set direct mutation attempted
- keep outputs non-canonical

## Gold Cases

### 1. `case_01_baseline_compliant`

- expected output: template-shaped budget draft JSON only
- expected triggers: none
- expected pressure mapping: none
- expected review path: no exception candidate generated

### 2. `case_02_guideline_lookup_miss`

- expected output: budget draft JSON plus retrieval exception candidate
- expected triggers: `synthetic_guideline_lookup_miss`
- expected pressure mapping: `retrieval_quality_pressure`
- expected review path: knowledge-owner review

### 3. `case_03_missing_budget_driver`

- expected output: budget draft JSON with flagged row notes
- expected triggers: `missing_required_budget_driver`
- expected pressure mapping: `workflow_friction_pressure`
- expected review path: budget-operations review

### 4. `case_04_expert_gap`

- expected output: budget draft JSON
- expected triggers: `expert_need_not_reflected_in_L130_L340_E119`
- expected pressure mapping: `workflow_friction_pressure`
- expected review path: billing-integrity review

### 5. `case_05_deposition_and_trial_drift`

- expected output: budget draft JSON
- expected triggers: `deposition_burden_not_reflected_in_L330_E115`
- expected triggers: `trial_likelihood_not_reflected_in_L400`
- expected triggers: `amount_billed_to_date_incompatible_with_remaining_budget`
- expected pressure mapping: `workflow_friction_pressure`
- expected review path: billing-integrity and workflow review

### 6. `case_06_appeal_and_staffing_conflict`

- expected output: budget draft JSON
- expected triggers: `appeal_likelihood_not_reflected_in_L500`
- expected triggers: `staffing_mix_outside_expected_pattern`
- expected pressure mapping: `workflow_friction_pressure`
- expected review path: billing-integrity review

### 7. `case_07_unsupported_assumption_or_missing_provenance`

- expected output: no final budget draft JSON
- expected triggers: `unsupported_budget_assumption`
- expected triggers: `source_provenance_missing`
- expected pressure mapping: none in first pass
- expected review path: preflight refusal and governance remediation

### 8. `case_08_missing_allowed_use_and_owner`

- expected output: no final budget draft JSON
- expected triggers: `allowed_use_basis_missing`
- expected pressure mapping: none in first pass
- expected review path: preflight refusal

## Public Dataset Guidance

Public datasets may inform synthetic realism only.

Recommended posture:

- `UTBMS / DRI`: high usefulness for task taxonomy interpretation only
- `SALI LMSS`: medium usefulness for matter-family labeling only
- `IRC AutoBi / insuranceData`: medium usefulness for synthetic severity and attorney-involvement priors only
- `NHTSA CISS/CIREN`: medium usefulness for injury, witness, and expert-need priors only
- `FJC IDB / CourtListener RECAP`: low for first pass
- `CJSSC / NCSC Landscape`: low for first pass

No public dataset may be used to claim Law Firm budget prediction quality.

## Evaluation Expectations

The runtime implementation is correct only if all are true:

- classification matches the expected synthetic case posture
- template-shaped JSON preserves exact phase and row order from the sanitized workbook transcription
- all template rows remain present even if unpopulated
- all amounts remain synthetic placeholder values
- emitted runtime events validate against the current contract schemas and route registry
- blocked cases emit no stored event and no final budget draft
- pressure outputs are marked non-canonical candidates
- no unsupported budget or savings claims are made
- no production claims are made
- no canon mutation occurs

## Out Of Scope

This first POC does not include:

- real matters, carriers, clients, employees, policies, or incidents
- real ingestion
- real connectors
- dashboards
- deployment or operational runtime configuration
- predictive budgeting
- workbook styling fidelity work
- automatic adaptation-proposal creation
- automatic promotion-decision creation
- canon mutation

## Non-Claims

This POC does not claim:

- production matter-intake automation
- production budget governance
- production runtime Exceptions Lake behavior
- real legal-budget learning from firm operations
- real connector coverage
- approved use on real data
