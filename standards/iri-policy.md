# IRI Policy

## Rules

- Canonical semantic identifiers must be stable.
- Version information belongs in metadata, not in canonical term IRIs.
- Labels are mutable; identifiers are not.
- New identifiers are required when meaning changes materially.
- Deprecated identifiers remain resolvable and should point to replacements where possible.

## Canonical pattern

- ontology modules: stable HTTP IRIs
- document-derived artifacts: content-addressed IDs or deterministic local IDs
- external standard alignments: keep external IRIs intact and map to Law Firm IDs

## Validation expectation

Deterministic IDs must be recomputable from canonical inputs, and CI should fail if recomputation does not match the stored identifier.
