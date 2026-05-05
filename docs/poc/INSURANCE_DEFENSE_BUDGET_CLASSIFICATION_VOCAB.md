# Insurance-Defense Budget Classification Vocabulary

## Purpose

Define the bounded synthetic classification vocabulary for a JSON-first
insurance-defense budget POC that mirrors a sanitized budget workbook shape
without claiming production budget accuracy.

This vocabulary is for:

- synthetic case fixtures
- deterministic budget-draft generation
- deterministic exception detection
- evaluation expectations

It is not for:

- real Law Firm matter intake
- real carrier or client guideline interpretation
- real budget prediction
- production staffing or billing advice

## Matter Family

Use one synthetic matter family only:

- `synthetic_auto_bi_defense_v1`

## Synthetic Driver Axes

### Injury Severity Band

- `minor`
- `moderate`
- `severe`

### Liability Clarity

- `clear`
- `mixed`
- `disputed`

### Medical Specials Band

- `low`
- `medium`
- `high`

### Claimant Attorney Involvement

- `none`
- `early_representation`
- `active_litigation_counsel`

### Uninsured Or Coverage Complication Indicator

- `none`
- `present`

### Seatbelt Or Restraint Factor

- `not_material`
- `alleged_nonuse`
- `unclear`

### Fact Witness Count Band

- `1_2`
- `3_5`
- `6_plus`

### Expert Need

- `none`
- `possible`
- `required`

### Written Discovery Burden

- `light`
- `moderate`
- `heavy`

### Deposition Burden

- `none`
- `limited`
- `heavy`

### Dispositive Motion Likelihood

- `low`
- `medium`
- `high`

### Mediation Likelihood

- `low`
- `medium`
- `high`

### Trial Likelihood

- `low`
- `medium`
- `high`

### Appeal Likelihood

- `low`
- `medium`
- `high`

### Carrier Guideline Placeholder Constraint

- `alpha`
- `beta`
- `gamma`

## Template-Shape Driver Mapping

These drivers influence row emphasis and synthetic allocation only. They do not
claim predictive budget accuracy.

- liability uncertainty and witness sprawl should raise emphasis in `L110`,
  `L120`, `L210`, and `L240`
- written discovery burden should raise emphasis in `L310` and `L320`
- deposition burden should raise emphasis in `L330` and `E115`
- expert need should raise emphasis in `L130`, `L340`, and `E119`
- mediation likelihood should raise emphasis in the settlement or ADR rows
- trial likelihood should raise emphasis in `L400`
- appeal likelihood should raise emphasis in `L500`
- guideline placeholder constraints may cap or reallocate synthetic totals and
  may produce supported exception triggers

## Budget Workflow Axes

### Budget Phase

- `initial_budget`
- `discovery_refresh`
- `adr_refresh`
- `trial_refresh`

### Staffing Assumption

- `associate_led_paralegal_supported`
- `partner_light_associate_heavy`
- `partner_deposition_heavy`
- `expert_managed`

### Budget Variance Signal

- `within_range`
- `phase_overrun_10`
- `phase_overrun_25`
- `staffing_mix_drift`
- `unsupported_assumption`
- `reflection_gap`

## Governance Axes

### Review Owner

- `synthetic_knowledge_owner`
- `synthetic_budget_ops_owner`
- `synthetic_billing_integrity_owner`
- `synthetic_governance_owner`

### Allowed-Use Basis

- `synthetic_budget_learning_eval`
- `synthetic_metadata_only_eval`

### Sensitivity Level

- `synthetic_internal`
- `synthetic_restricted_budget`
- `synthetic_policy_simulated`

### Risk Class

- `budget_integrity_low`
- `budget_integrity_medium`
- `budget_integrity_high`
- `governance_blocker`

### Canon Influence Boundary

- `exception_candidate_only`
- `pressure_candidate_only`
- `promotion_decision_required`

## Exception Trigger Vocabulary

The first POC uses these trigger labels while reusing the current governed event
classes and routes:

- `missing_required_budget_driver`
- `unsupported_budget_assumption`
- `budget_phase_missing`
- `budget_exceeds_synthetic_threshold`
- `staffing_mix_outside_expected_pattern`
- `expert_need_not_reflected_in_L130_L340_E119`
- `deposition_burden_not_reflected_in_L330_E115`
- `trial_likelihood_not_reflected_in_L400`
- `appeal_likelihood_not_reflected_in_L500`
- `amount_billed_to_date_incompatible_with_remaining_budget`
- `allowed_use_basis_missing`
- `source_provenance_missing`
- `synthetic_guideline_lookup_miss`

## Current-Contract Mapping Posture

For the first implementation:

- the runtime must reuse the current `exception-event` classes
- raw outputs remain exception candidates only
- pressure aggregation remains non-canonical
- promotion still requires reviewed human approval
- the template-shaped budget object is a governed presentation draft, not canon

| Trigger family | Current event class | Route | Pressure class | Handling posture |
|---|---|---|---|---|
| synthetic guideline lookup miss | `retrieval_miss` | `route.retrieval_miss.v1` | `retrieval_quality_pressure` | event allowed |
| supported budget workflow or reflection issue | `workflow_escalation` | `route.workflow_escalation.v1` | `workflow_friction_pressure` | event allowed |
| governance blockers such as unsupported assumption, missing allowed-use basis, or missing provenance | current preflight posture first | no new route in this pass | none in first pass | fail closed without final budget draft |

## Public Dataset Posture

Public datasets may be used only as external realism priors for synthetic driver
selection and synthetic case variety.

They may not be used to claim:

- Law Firm budget accuracy
- Law Firm staffing accuracy
- validated business value
- production matter or carrier behavior

## Non-Claims

This vocabulary does not claim:

- production budget analytics
- production Law Firm budget rates, hours, or staffing rules
- real insurer or carrier policy behavior
- real Law Firm staffing norms
- real matter economics
- real event ingestion
- canon mutation from runtime output
