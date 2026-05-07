# Phase 2 Roadmap

This roadmap extends the Phase 2 Innovation Autonomy + Harness Layer without changing the existing PR01-PR06 scopes.

Core design laws:

```text
Risk color controls authority.
Hardness controls harness depth.
Leverage controls priority.
Stakes size controls escalation sensitivity.
Reversibility controls autonomy.
Frequency controls compounding value.
```

Red/yellow/green alone is insufficient. A technically low-risk action may still be high-stakes when blast radius, repetition, reputation exposure, client impact, privilege exposure, billing/legal finality, or semantic authority impact is high.

## PR01 - Control-Plane Schemas And Policies

Add Phase 2 schema-first authority artifacts, registries, and governance policies for autonomy, harness selection, research scaffolding, and schema placement.

## PR02 - Orchestrator Autonomy Gate And Harness Selector

Add deterministic autonomy classification, hardness scoring, leverage scoring, and harness selection in the Orchestrator repo.

## PR03 - Orchestrator Green-Lane Watcher

Add local assumption watching and green-lane downgrade logic. Agents may recommend green-to-yellow or green-to-red reclassification, but humans are required to restore green.

## PR04 - Codex Task Builder And Agent Front Door

Add local Codex task packet generation and inert agent review artifacts. Packets do not execute Codex, Git, patches, model calls, or network calls.

## PR05 - Exception Lake Phase 2 Records

Add append-only storage/query support for Phase 2 opportunity, autonomy, harness, research, agent review, validation, and scale package records.

## PR06 - Research And Internal Idea Loop

Add local-only scaffolding for research and idea lifecycle objects.

Allowed PR06 scope:

- schemas;
- local object builders;
- local CLI generators;
- docs;
- tests;
- append-only storage for research and idea lifecycle records.

Forbidden PR06 scope:

- live web crawling;
- scheduled background jobs;
- live model calls;
- external API calls;
- external writes;
- autonomous idea execution;
- production research automation.

PR06 must leave decision intelligence, stakes profiles, reversibility scoring, and Research Radar watchlist seeding for PR07 unless a small compatibility hook is required.

## PR07 - Decision Intelligence, Stakes Model, And Research Radar Seeding

Add local-only, schema-first foundations for decision intelligence and Research Radar seeding.

Control-plane planned artifacts:

- `schemas/decision/decision-model.schema.json`
- `schemas/decision/stakes-profile.schema.json`
- `schemas/decision/decision-context.schema.json`
- `schemas/decision/decision-escalation-record.schema.json`
- `schemas/research/research-radar-item.schema.json`
- `schemas/research/research-radar-watchlist.schema.json`
- `schemas/research/research-radar-brief.schema.json`
- `registry/decision-model-registry.json`
- `registry/stakes-profile-registry.json`
- `registry/research-radar-registry.json`
- `governance/DECISION_INTELLIGENCE_MODEL.md`
- `governance/STAKES_AND_REVERSIBILITY_POLICY.md`
- `governance/RESEARCH_RADAR_OPERATING_MODEL.md`

Orchestrator planned artifacts:

- `decision/stakes_classifier.py`
- `decision/reversibility_classifier.py`
- `decision/decision_model_selector.py`
- `decision/escalation_selector.py`
- `research/research_radar_seed.py`
- `research/research_radar_watchlist.py`
- local-only CLI stubs for object generation.

Exception Lake planned records:

- append-only decision-context-record;
- stakes-profile-record;
- decision-escalation-record;
- research-radar-item;
- research-radar-brief;
- research-watch-trigger.

Research Radar PR07 boundaries:

- Seed now as a local-only watchlist and brief-generation foundation.
- Do not add live web crawling, scheduled jobs, model calls, external APIs, or autonomous research execution.
- Research Radar outputs are candidate evidence and decision support only.
- Research Radar may recommend green-to-yellow or green-to-red reclassification.
- Research Radar may not restore green or promote canon.

Pre-PR07 draft scaffolding already in the repository:

- `registry/research-radar-source-registry.json` exists as pre-PR07 draft scaffolding. It is metadata-only and non-authorizing, marked `non_authoritative: true` and `phase: "pre-pr07-draft"`. It does not authorize live crawling, scheduled jobs, model calls, external APIs, external writes, or production research automation. PR07 may later formalize, supersede, or reconcile it.

Initial local-only Research Radar watchlist seed set:

```json
{
  "watchlist_id": "research-radar-frontier-ai-001",
  "topic": "frontier_ai_capability",
  "why_it_matters": "May change harness intensity, autonomy assumptions, and feasible iteration cadence.",
  "affected_os_surfaces": [
    "harness-policy-registry",
    "autonomy-lane-registry",
    "green-lane-watch-policy",
    "codex-task-generation"
  ],
  "default_action": "create_research_radar_item",
  "may_downgrade_green_lanes": true,
  "human_required_for_green_restoration": true
}
```

Additional seed topics reserved for PR07:

```text
frontier_math_algorithmic_breakthrough
agent_failure_incident
ai_security_prompt_injection
legal_ai_ethics_guidance
model_provider_policy_change
coding_agent_harness_design
retrieval_eval_rag_quality
workflow_orchestration_patterns
decision_science_and_risk
creativity_with_ai
law_firm_reputation_risk
billing_guideline_and_carrier_changes
```

The detailed `research-radar-frontier-ai-001` item and the additional topics are roadmap evidence only until PR07 creates schemas and local object builders. They must not trigger crawling, scheduled jobs, live model calls, external API calls, external writes, or autonomous research execution.
