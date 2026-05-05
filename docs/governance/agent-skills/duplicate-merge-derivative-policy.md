# Duplicate, Merge, and Derivative Policy

This policy defines how the registry should classify overlap without allowing automatic canonical mutation.

## Classifications

- `exact_duplicate`
- `near_duplicate`
- `derivative_variant`
- `adapter_variant`
- `workflow_wrapper`
- `experimental_fork`
- `deprecated_alias`

## Decision rules

- `exact_duplicate`
  - merge canonically and preserve alias or supersession note
- `near_duplicate`
  - keep separate only if boundary, owner, or workflow role materially differs
- `derivative_variant`
  - keep separate with `derives_from` or `specializes`
- `adapter_variant`
  - never becomes semantic authority
- `workflow_wrapper`
  - keep as workflow or orchestrator, not as duplicate skill
- `experimental_fork`
  - keep separate while status remains clearly bounded and non-authoritative
- `deprecated_alias`
  - preserve for lookup continuity while pointing to the preferred canonical card

## Derived-evidence rule

Generated overlap reports, candidate duplicate edges, similarity neighborhoods, embeddings, and GraphRAG summaries may recommend review only. They may not merge, retag, or supersede canonical cards automatically.
