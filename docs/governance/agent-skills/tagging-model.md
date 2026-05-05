# Tagging Model

This surface uses controlled `axis:value` tags.

## Mandatory tag axes

- `node_type:*`
- `platform_surface:*`
- `capability_function:*`
- `project_surface:*`
- `domain:*`
- `risk_boundary:*`
- `lifecycle:*`
- `audit_class:*`

## Optional tag axes

- `data_posture:*`
- `overlap_family:*`
- `workflow_phase:*`
- `dependency_class:*`
- `graph_export:*`

## Tagging rules

- every card must include at least one value from each mandatory axis
- every card must have exactly one `lifecycle:*`
- every card must have exactly one `audit_class:*`
- ownership and cadence remain canonical fields, not required tags
- controlled tags support future generated indexes and discovery, but tags remain canonical only when stewarded in cards or governed supporting docs

## Why controlled tags matter

At large scale, free-form tags create drift and overlap ambiguity. Controlled tag axes reduce chaos and make future overlap reports, similarity neighborhoods, and GraphRAG summaries easier to generate without confusing derived outputs for canonical truth.
