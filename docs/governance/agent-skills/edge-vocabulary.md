# Edge Vocabulary

This document defines the typed relationship vocabulary for the Agent/Skill Capability Graph.

## Canonical typed edges

- `depends_on`
- `invokes`
- `delegates_to`
- `composes`
- `specializes`
- `derives_from`
- `supersedes`
- `monitors`
- `emits_candidate_signal_to`
- `routes_to`
- `subscribes_to`
- `covered_by_workflow`
- `uses_adapter_surface`
- `impacts_surface`

## Derived-only future edges

- `similar_to`
- `overlaps_with`
- `candidate_duplicate_of`
- `embedding_neighbor_of`
- `clustered_with`
- `graphrag_summary_neighbor_of`

## Canonical versus derived distinction

Canonical edges:
- are stewarded in cards or governed supporting docs
- define reviewed dependency and impact structure
- may affect ownership, cadence, and orchestrator review

Derived edges:
- may be generated later from overlap analysis, indexes, embeddings, or GraphRAG summaries
- are discovery aids only
- may recommend review but may not directly create, merge, or mutate canonical relationships

## Edge review posture

Any change to canonical edges should consider:
- dependency impact
- orchestrator impact
- audit boundary impact
- overlap or duplicate implications
- governed-learning implications
