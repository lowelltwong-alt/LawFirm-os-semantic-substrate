# Readiness Gates

## Execution Control

Roadmap execution order is controlled by `docs/roadmap/READINESS_GATES.md`.
A phase advances only when the applicable readiness gate passes.

## Purpose

Define the controlling execution order for roadmap delivery using measurable,
validator-backed promotion gates.

> This document is the execution authority for phase progression. Roadmap phase
> order is descriptive; readiness gates are prescriptive.

## Gate Order (Controlling)

1. Structural Readiness
2. Governance Readiness
3. Learning Readiness
4. Retrieval Readiness

A phase may start implementation work in parallel, but **promotion to the next
phase is blocked until all pass criteria for the current gate are satisfied**.

## Gate 1  -  Structural Readiness

### Pass Criteria

- Schema and YAML integrity checks pass with zero failures.
- ID and canonical spine integrity checks pass with zero failures.
- SHACL and semantic-stack checks pass for active artifacts.

### Validators

- `python scripts/validation/validate_schema.py`
- `python scripts/validation/check_repo_yaml.py`
- `python scripts/validation/check_ids.py`
- `python scripts/validate_canonical_spine.py`
- `python scripts/validation/validate_shacl.py`
- `python scripts/validation/validate_semantic_stack.py`

### Required Artifacts

- `graphs/manifests/` entries for active pilot graph material.
- `data/contexts/*.jsonld` context artifacts for semantic resources.
- `data/projections/*.yaml` projection artifacts for governed exports.

## Gate 2  -  Governance Readiness

### Pass Criteria

- Exception events pass structural and governance-route validation with zero
  policy violations.
- Promotion/lifecycle posture remains explicit and traceable in governed action
  records.
- Monthly and quarterly governance reviews are current and complete.

### Validators

- `python scripts/validation/validate_exception_events.py`
- `python scripts/validation/validate_exception_governance.py`
- `python scripts/phase5/validate_action_types.py`
- `python scripts/phase5/validate_object_sets.py`
- `python scripts/phase5/validate_pilot_slices.py`

### Required Artifacts

- `data/action-log/*.yaml` action records for governed lifecycle decisions.
- `data/action-log/governance_review_cadence.template.yaml` review cadence
  contract (used to instantiate monthly/quarterly reviews).
- Instantiated cadence artifacts under `data/action-log/` for each period.

## Gate 3  -  Learning Readiness

### Pass Criteria

- Alignment assessment completeness checks pass.
- Learning-loop transitions validate without invalid state jumps.
- Proposal-to-promotion traces remain explainable and tied to evidence.

### Validators

- `python scripts/phase4/validate_alignment_rubric.py`
- `python scripts/phase4/check_comparison_assessments.py`
- `python scripts/validation/validate_learning_loop_transitions.py`

### Required Artifacts

- `data/comparisons/alignment_assessment*.yaml`
- `data/retrieval/RFB-*.yaml` retrieval feedback records.
- `data/retrieval/PRP-*.yaml` proposal/promotion decision records.

## Gate 4  -  Retrieval Readiness

### Pass Criteria

- Semantic stack validations pass with zero blocking failures.
- Retrieval feedback, proposals, and promotion traces are present for active
  pilot slices.
- Property graph projection and context contracts are internally coherent.

### Validators

- `python scripts/validation/validate_semantic_stack.py`
- `python scripts/validation/validate_ontology_boundary.py`
- `python scripts/validation/build_exports.py`

### Required Artifacts

- `data/projections/PGP-*.yaml` projection instances.
- `data/contexts/CTX-*.jsonld` context instances.
- `graphs/manifests/*.yaml` graph manifest instances.

## Promotion Freeze Rule (Mandatory)

Ontology expansion is frozen when either condition is true:

1. **Alignment score < 0.80** for the active governance period.
2. **Exception-route coverage < 0.95** for the active governance period.

### Metric Definitions

- **Alignment score**: `approved_alignment_assessments / total_alignment_assessments`
  using governance-period promotion outcomes.
- **Exception-route coverage**: `exception_events_with_registered_route /
  total_exception_events` using governance-period exception records.

### Evidence and Enforcement

- Threshold values must be recorded in each cadence artifact instance generated
  from `data/action-log/governance_review_cadence.template.yaml`.
- If either metric is below threshold, no new ontology-domain expansion PRs are
  eligible for promotion until the next review shows recovery above threshold.

## Governance Review Cadence (Mandatory Artifact Outputs)

Cadence artifacts must be produced on:

- **Monthly** cycle (operational drift and exception control)
- **Quarterly** cycle (promotion posture and structural governance fitness)

Each cadence artifact must include links or embedded summaries for:

1. drift report
2. exception trend report
3. promotion outcomes report

A cadence artifact is incomplete without all three outputs.
