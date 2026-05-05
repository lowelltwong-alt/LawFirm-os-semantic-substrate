# Ontology Boundary Contract

## Purpose

Define and enforce the boundary between:
- first-order authoritative ontology objects (canonical truth-bearing objects), and
- second-order derived/probabilistic signals (analysis, projection, feedback, promotion, or operational sidecars).

This contract prevents analytics and derived layers from silently becoming the source of ontology truth.

## First-Order Authoritative Objects

First-order objects are governed canonical artifacts that can define or update canonical ontology state when approved through normal governance paths.

Examples (by object family) include:
- `assertion_object`
- `evidence_bundle`
- `action_definition`
- `object_set_definition`
- `pilot_slice`
- canonical core entities such as `concept`, `doctrine`, `doctrine_position`, `relationship_object`, and other spine-level entities

First-order objects are expected to carry `ontology_order: first_order`.

## Second-Order Derived / Probabilistic Signals

Second-order objects are downstream or reflective layers. They can recommend, score, project, or summarize, but they cannot directly overwrite canonical truth fields.

Examples (by object family) include:
- `alignment_assessment`
- `comparison_object`
- `property_graph_projection`
- `retrieval_feedback`
- `proposal_promotion`
- `action_log_entry`

Second-order objects are expected to carry `ontology_order: second_order`.

## Forbidden Patterns

The following are forbidden because they let analytics become the truth source:

1. Second-order objects directly editing canonical values.
2. Second-order objects carrying mutation payloads intended to overwrite canonical fields.
3. Second-order objects introducing override blocks for first-order truth.

Concretely, second-order objects must not use non-empty fields such as:
- `canonical_field_overrides`
- `first_order_field_overrides`
- `overwrite_canonical_fields`
- `proposed_canonical_updates`

Second-order objects must route changes through governed first-order actions and reviewers instead of direct canonical mutation.

## Repository Linkage

This boundary contract is part of the repository operating model and is cross-linked from:
- `schema/README.md`
- `docs/architecture/PROJECT_SYSTEM_MAP.md`
- `docs/governance/REPO_OPERATING_MODEL.md`
