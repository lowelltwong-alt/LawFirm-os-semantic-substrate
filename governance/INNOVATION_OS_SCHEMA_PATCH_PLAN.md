# Innovation OS Schema and Registry Patch Plan

## Purpose

This document records the next direct machine-readable changes required to move Innovation OS from governance prose into active schema and registry surfaces.

It exists because the repository already has the conceptual operating-layer documents, but the active exception and pressure registries still reflect the earlier, narrower enterprise-learning surface.

## Target files for next direct patch

### 1. `registry/source-of-truth.json`
Add authoritative references for:
- `governance/INNOVATION_OS_OPERATING_SYSTEM.md`
- `governance/EXCEPTIONS_LAKE_TO_INNOVATION_OS_MAPPING.md`
- `governance/INNOVATION_OS_DEEP_INTEGRATION_PLAN.md`
- `governance/PHASED_INTEGRATION_BACKLOG.md`
- `governance/INNOVATION_OS_CINO_READY_ARTIFACT.md`

Also update release framing so the current draft explicitly names Innovation OS as part of the active enterprise-learning layer.

### 2. `schemas/exception-event.schema.json`
Expand the current `event_class` surface beyond:
- `retrieval_miss`
- `workflow_escalation`
- `authority_conflict_override`

Recommended additions:
- `billing_exception`
- `portal_friction`
- `ar_delay`
- `guideline_compliance_failure`
- `ocg_delta_signal`
- `carrier_rule_delta`
- `vendor_roadmap_signal`
- `market_signal`
- `budget_variance_signal`

Also expand:
- `origin.layer`
- `route.destination_loop`
- `canonical_mutation_control.allowed_action`

So that raw pressure can legally route into opportunity review, pilot review, executive briefing generation, and commercial realignment review without bypassing promotion boundaries.

### 3. `schemas/pressure-vector.schema.json`
Expand `vector_class` beyond the current narrow set.

Recommended additions:
- `revenue_leakage_pressure`
- `portal_workflow_pressure`
- `pricing_budget_pressure`
- `external_delta_pressure`
- `innovation_priority_pressure`

The purpose is to let pressure vectors represent not only retrieval and workflow issues, but also the operating pressure classes required by Innovation OS.

### 4. `registry/exception-route-registry.json`
Add route families for:
- opportunity review
- sprint intake
- pilot review
- executive briefing
- commercial realignment review

Recommended examples:
- `route.billing_exception.v1`
- `route.portal_friction.v1`
- `route.ocg_delta_signal.v1`
- `route.vendor_roadmap_signal.v1`
- `route.budget_variance_signal.v1`

These routes must preserve the existing global control:

`no_direct_canonical_mutation_from_raw_exception = true`

### 5. Future schema families
Create new governed families for:
- `opportunity-object`
- `opportunity-scorecard`
- `sprint-object`
- `pilot-object`
- `validation-gate-record`
- `executive-brief-object`
- `scale-package-object`
- `gold-standard-asset`
- `commercial-realignment-object`
- `promotion-decision-object`

## Proposed mutation path

The canonical legal path remains:

`exception-event -> pressure-vector -> opportunity-object -> sprint-or-pilot -> validation-gate-record -> scale-package -> promotion-decision`

Nothing earlier in the chain may directly mutate canonical ontology truth.

## Validation implications

Once these schema and registry updates land, the repository should add validation rules for:
- required owner on opportunity and sprint objects
- required KPI hypothesis on sprint and pilot objects
- required gate records before scale-state transitions
- required provenance on external intelligence items
- forbidden direct canonical mutation from operating artifacts

## Why this matters

Without these machine-readable changes, Innovation OS remains partly outside the active contract surface.

With them, the repository can use the same governed graph to answer:
- what pressure is rising
- what work is ranked highest
- what is being tested now
- what passed gates
- what scaled
- what should become canonical truth
