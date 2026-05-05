# Claim Schema

A claim is the core unit of knowledge.

## Structure

- claim_id
- schema_id
- template_id
- subject
- predicate
- object
- claim_type
- claim_mode
- authority_zone
- trust_level
- source_refs
- evidence_refs (optional)
- artifact_refs (optional)
- derived_from_claims (optional)
- confidence (optional)
- created_at (optional)
- created_by (optional)
- address
- address_struct

## Rules

- Every claim must have provenance
- Every claim must belong to an authority zone
- Every canonical claim must include `schema_id` and `template_id`
- Every canonical claim must include a canonical address and structured address
- `source_refs` should use canonical `SRC-...` identifiers
- `evidence_refs` should use canonical `CHK-...` identifiers
- `artifact_refs` and `derived_from_claims` should resolve to governed objects in the repository when they are internal references
- Evidence required for promotion to canonical layer
