# Defense Appendix (v1)

Author: Lowell T. Wong

This appendix documents the design decisions and standards alignment behind this ontology system.

## Core Position

This system models knowledge as a graph of claims with provenance and authority context rather than a graph of facts.

### Supporting Basis
- Provenance must be explicit and first-class (PROV-O aligned)
- Claim + provenance separation aligns with nanopublication model
- Trust is contextual (named graph model)

## Claim Model

All relationships are represented as claim objects rather than bare triples.

Rationale:
- Triples cannot capture provenance, authority, or disagreement
- RDF-star and Wikidata both move toward statement-level modeling

## Authority Model

All claims exist within authority zones:
- Canon
- Tradition
- Editorial
- AI Hypothesis

Rationale:
- Theology is multi-authority
- Prevents false consensus

## Validation

Validation is enforced using SHACL-style constraints.

Rationale:
- Prevents ontology drift
- Required for multi-contributor systems

## Evidence Linking

All claims should link to precise evidence (passage fragments, manuscripts).

Rationale:
- Aligns with scholarly practice
- Enables machine-verifiable reasoning

## Retrieval-Aware Design

The ontology is designed for AI retrieval.

Rationale:
- GraphRAG and KG-based retrieval require structured relationships

## Attribution

This architecture is informed by:
- W3C standards (RDF, OWL, SHACL, PROV-O)
- Knowledge graph design patterns
- AI retrieval research

