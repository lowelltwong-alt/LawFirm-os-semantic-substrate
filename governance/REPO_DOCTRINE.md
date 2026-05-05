# Repo Doctrine

## Law Firm repository role

Law Firm is the canonical semantic-governance substrate and Innovation OS contract repository.

It should own:
- ontology and taxonomy meaning
- evidence and provenance contracts
- lifecycle and change governance
- runtime learning objects used for governed promotion
- retrieval and integration contracts
- evaluation and observability contracts

It should not store canonical runtime artifacts such as embeddings, vector indexes, OCR model weights, or environment-specific prompts.

## Layer separation

The repository keeps four layers explicit:
1. ontology / semantic meaning
2. evidence / provenance
3. policy / governance
4. action / workflow execution

## Canonical vs derived

Canonical artifacts:
- ontology modules
- taxonomy schemes
- SHACL shapes
- JSON schemas
- lifecycle and change policies
- canonical document/evidence model

Derived artifacts:
- chunks
- embeddings
- indexes
- GraphRAG summaries
- runtime answer caches

## Mutation boundary

Raw exceptions, pressure vectors, retrieval traces, and runtime outputs must never rewrite canonical meaning directly.
All canonical change must flow through governed promotion decisions.
