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
```

Hardness and leverage never override red/yellow/green authority.

This repository owns the schemas, registries, policies, green-lane assumptions, red-flag triggers, harness policy, and promotion boundaries for the layer. Runtime and orchestrator repos may consume these contracts and emit evidence objects, but they must not mutate canon or invent route IDs, event classes, schemas, or promotion decisions.

Promotion decisions are required only when a proposed change affects canonical ontology, taxonomy, route/event authority, governance doctrine, or other canonical surfaces.
