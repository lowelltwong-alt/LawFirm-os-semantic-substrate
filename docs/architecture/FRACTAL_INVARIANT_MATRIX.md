# Fractal Invariant Matrix (First-Order Types)

This matrix tracks DNA invariant coverage for first-order schema types using
`schema/invariants/first_order_invariants.yaml` as the validation source of truth.

Legend: ✅ covered by explicit fields and/or linked references.

| Type | Identity | Address / Placement | Lineage / Provenance | Lifecycle / State | Trust Posture |
|---|---|---|---|---|---|
| action_definition | ✅ (`id`, `object_type`, `title`) | ✅ (`canonical_anchor_refs`) | ✅ (`canonical_anchor_refs`) | ✅ (`lifecycle_status`, `lifecycle_impact`) | ✅ (`authority_zone`) |
| action_log_entry | ✅ | ✅ | ✅ | ✅ | ✅ |
| alignment_assessment | ✅ | ✅ | ✅ (`source_refs`) | ✅ (`lifecycle_status`, `review_status`) | ✅ (`authority_zone`, `confidence_level`) |
| assertion_object | ✅ | ✅ | ✅ (`provenance_activity_refs`, `source_refs`) | ✅ (`lifecycle_status`) | ✅ (`authority_zone`, `trust_level`) |
| canon_thinker | ✅ | ✅ | ✅ | ✅ | ✅ |
| comparison_object | ✅ | ✅ | ✅ (`source_refs`) | ✅ (`lifecycle_status`, `review_status`) | ✅ (`authority_zone`, `confidence_level`) |
| concept | ✅ | ✅ | ✅ | ✅ | ✅ |
| doctrine | ✅ | ✅ | ✅ | ✅ | ✅ |
| doctrine_position | ✅ | ✅ | ✅ (`source_refs`) | ✅ (`lifecycle_status`, `review_status`) | ✅ (`authority_zone`, `trust_level`) |
| evidence_bundle | ✅ | ✅ | ✅ (`source_refs`, `derived_from_refs`) | ✅ (`lifecycle_status`) | ✅ (`authority_zone`) |
| external_standards_registry | ✅ | ✅ | ✅ | ✅ | ✅ |
| graph_object | ✅ | ✅ | ✅ (`included_node_refs`) | ✅ | ✅ |
| jsonld_context | ✅ | ✅ | ✅ (`governing_graph_manifest_refs`) | ✅ | ✅ |
| lexeme | ✅ | ✅ | ✅ (`concept_refs`) | ✅ | ✅ |
| manuscript_witness | ✅ | ✅ | ✅ (`provenance_label`) | ✅ | ✅ |
| named_graph_manifest | ✅ | ✅ | ✅ (`included_object_refs`, `included_assertion_refs`) | ✅ (`lifecycle_status`, `graph_manifest_status`) | ✅ |
| object_set | ✅ | ✅ | ✅ (`member_refs`) | ✅ | ✅ |
| object_set_definition | ✅ | ✅ | ✅ (`member_ids`) | ✅ | ✅ |
| passage_anchor | ✅ | ✅ | ✅ (`source_ref`) | ✅ | ✅ |
| pilot_slice | ✅ | ✅ | ✅ (`required_artifacts`) | ✅ (`lifecycle_status`, `pilot_slice_status`) | ✅ |
| property_graph_projection | ✅ | ✅ | ✅ (`graph_manifest_ref`) | ✅ (`lifecycle_status`, `projection_status`) | ✅ |
| proposal_promotion | ✅ | ✅ | ✅ (`source_feedback_ref`, `target_manifest_refs`) | ✅ (`lifecycle_status`, `proposal_promotion_status`) | ✅ |
| provenance_activity | ✅ | ✅ | ✅ (`input_refs`, `output_refs`) | ✅ | ✅ |
| relationship_object | ✅ | ✅ | ✅ (`source_refs`) | ✅ | ✅ (`authority_zone`, `trust_level`) |
| retrieval_feedback | ✅ | ✅ | ✅ (`graph_manifest_ref`, `supporting_query_refs`) | ✅ (`lifecycle_status`, `retrieval_feedback_status`) | ✅ |
| translation_witness | ✅ | ✅ | ✅ (`source_witness_ref`) | ✅ | ✅ |

## Enforcement

- Validation script: `scripts/validation/validate_dna_invariants.py`
- Mapping source: `schema/invariants/first_order_invariants.yaml`
- Validation fails when a type is missing any required invariant mapping.
