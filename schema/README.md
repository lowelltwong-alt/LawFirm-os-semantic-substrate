# Enterprise Doctrinal Comparison Substrate

This directory defines the Phase 1 substrate for enterprise doctrinal comparison.

It is intentionally machine-readable and preparatory. It does not replace the
canonical `schemas/` JSON Schema layer already used by the repository. Instead,
it provides a stable design substrate for later hardening into JSON Schema,
SHACL, LinkML, registry extensions, and governed examples.

## Design Commitments

- preserve the current repository shell and governance direction
- reuse existing authority, trust, provenance, and inference disciplines
- keep IDs distinct from canonical addresses
- treat folders as scaffolding, not ontology truth
- prepare for later validation hardening without introducing a parallel grammar

In particular, the substrate reuses current field-name direction such as
`authority_zone` and `trust_level` even where a requested enum file has a more
generic name.

## Boundary Contract

Authoritative ontology truth and derived/probabilistic signals are governed by
the ontology boundary contract:

- `governance/ONTOLOGY_BOUNDARY_CONTRACT.md`

## Layout

- `manifest.yaml`: substrate metadata and compatibility contract
- `interfaces/`: reusable interface definitions
- `types/`: doctrinal comparison type definitions
- `enums/`: controlled vocabulary seeds aligned to current repo direction
- `contracts/`: cross-scale invariant contracts for projection-safe object mappings

## Relationship To Existing Repo Structure

- canonical address and routing rules remain governed by:
  - `governance/CANONICAL_ADDRESS_CONSTITUTION.md`
- current claim discipline remains governed by:
  - `governance/CLAIM_SCHEMA.md`
- current metadata discipline remains governed by:
  - `standards/metadata-standard.md`
- current validation and runtime schemas remain under:
  - `schemas/`

This Phase 1 substrate is a preparatory schema design layer, not a replacement
for the repository's current authoritative schema shell.
