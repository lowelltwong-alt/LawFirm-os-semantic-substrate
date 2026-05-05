# Named Graph Manifests

This directory stores additive manifest contracts for bounded semantic graph
packages.

Each manifest should declare:

- which graph partitions are included
- which JSON-LD context governs term expansion
- what publication profile applies
- what promotion or trust-boundary rules remain in force
- any cross-partition relation semantics with required metadata:
  - `directionality`
  - `cardinality`
  - `temporal_validity`
  - `trust_evidence_carryover`

For cross-partition links, use normalized relation semantics:
`equivalence`, `composition`, `derivation`, `temporal_succession`,
`control_dependency`.
