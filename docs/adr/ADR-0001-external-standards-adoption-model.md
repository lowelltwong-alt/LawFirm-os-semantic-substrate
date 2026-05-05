# ADR-0001 External Standards Adoption Model

## Status
Accepted

## Context

The Law Firm semantic stack needs to interoperate with established ontology and metadata standards without surrendering the design authority of the substrate-native operating layer.

The pilot is intentionally focused on intake, conflicts, and AI-use governance. It is not yet a general-purpose legal-document ontology project.

## Decision

The repository will use a three-part adoption model for external standards:

- adopt now
- selective
- watchlist later

External standards will support interoperability, provenance, controlled vocabularies, validation, and bounded domain extensions.

substrate-native operating classes remain the design authority for operational meaning.

## Rationale

This model avoids two common failures:

1. rebuilding solved generic ontology problems from scratch
2. importing external domain ontologies so early that they distort the pilot and weaken local governance clarity

## Consequences

Positive:
- clearer explanation for executive, KM, and AI-architecture audiences
- lower-regret standard reuse
- stronger interoperability posture
- preserved control of Law Firm-specific operating semantics

Negative:
- requires explicit rationale maintenance over time
- introduces a governance burden for mapping and revisit decisions

## Review Trigger

Review this ADR when the pilot expands beyond intake/conflicts/AI-use into broader legal knowledge, matter operations, or client-specific rule translation.