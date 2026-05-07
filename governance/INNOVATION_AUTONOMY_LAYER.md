# Innovation Autonomy Layer

The Innovation Autonomy + Harness Layer turns friction, research, internal ideas, and exception evidence into governed iteration proposals.

The required object flow is:

```text
exception-event
-> pressure-vector
-> opportunity-object
-> opportunity-scorecard
-> autonomy-decision-record
-> harness-plan
-> codex-task-packet
-> agent-review-record
-> validation-gate-record
-> scale-package-object
-> promotion-decision-object, only if canon changes
```

Core law:

```text
Risk color controls authority.
Hardness controls harness depth.
Leverage controls priority.
Stakes size controls escalation sensitivity.
Reversibility controls autonomy.
Frequency controls compounding value.
```

Hardness, leverage, stakes, reversibility, and frequency never override red/yellow/green authority. They shape priority, harness depth, and escalation sensitivity inside the authority boundary.

A technically low-risk action may still be high-stakes when blast radius, repetition, reputation exposure, client impact, privilege exposure, billing/legal finality, or semantic authority impact is high.

This repository owns the schemas, registries, policies, green-lane assumptions, red-flag triggers, harness policy, and promotion boundaries for the layer. Runtime and orchestrator repos may consume these contracts and emit evidence objects, but they must not mutate canon or invent route IDs, event classes, schemas, or promotion decisions.

Promotion decisions are required only when a proposed change affects canonical ontology, taxonomy, route/event authority, governance doctrine, or other canonical surfaces.

## Roadmap Extension

PR07 is reserved for Decision Intelligence, Stakes Model, and Research Radar Seeding.

Research Radar in PR07 is local-only and schema-first. It may seed watchlists and generate brief objects as candidate evidence and decision support. It may recommend green-to-yellow or green-to-red reclassification. It may not restore green or promote canon.

PR07 must not add live web crawling, scheduled background jobs, live model calls, external API calls, external writes, autonomous research execution, or production research automation.
