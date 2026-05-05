# Agent/Skill Registry Template

Use for governed changes to the Agent/Skill Capability Graph and Registry surface.

## Route
- route: `agent_skill_capability_graph`
- mode: Plan/Edit

## Required sections

- Capability surface being added or changed
- Node types affected
- Mandatory card fields affected
- Tag axes affected
- Canonical edge types affected
- Ownership and cadence impact
- Orchestrator or workflow impact
- Audit and transcript boundary impact
- Derived-surface implications
- Relationship to governed learning and promotion path
- Explicit non-goals

## Derived-surface reminder

Generated indexes, embeddings, candidate duplicate edges, similarity neighborhoods, overlap reports, and GraphRAG summaries are derived artifacts only. They are not canonical truth.

## Governed-learning posture

Use this surface for governed recursive improvement:

`candidate signal -> assessment -> recommendation -> adaptation-proposal recommendation if reviewed -> promotion-decision only through existing authority path`

## Forbidden

- automatic merges
- automatic runtime changes
- automatic route-table rewrites beyond the scoped PR
- generated artifacts treated as canonical truth
- raw transcript capture
- autonomous repo rewriting
