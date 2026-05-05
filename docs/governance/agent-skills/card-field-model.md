# Card Field Model

This document defines the mandatory field model for canonical capability cards.

## Mandatory fields for every card

- `capability_id`
- `display_name`
- `node_type`
- `status`
- `summary`
- `primary_owner_role`
- `steward_role`
- `reviewer_role`
- `review_cadence`
- `last_reviewed`
- `next_review_due`
- `change_trigger_conditions`
- `source_authority_class`
- `platform_surface`
- `capability_taxonomy_tags`
- `project_surface_tags`
- `input_summary`
- `output_summary`
- `side_effect_posture`
- `dependency_refs`
- `edge_refs`
- `audit_requirement_class`
- `transcript_posture`
- `exceptions_lake_relevance`
- `derived_index_eligibility`
- `overlap_family`
- `notes_on_non_goals`

## Type-specific fields

### `agent` and `subagent`

- `delegation_scope`
- `handoff_boundary`
- `tool_surface_summary`

### `skill`

- `activation_pattern`
- `tool_dependency_class`
- `expected_use_context`

### `monitor`

- `observed_surface`
- `trigger_class`
- `candidate_signal_output`

### `orchestrator`

- `coordinated_node_refs`
- `subscription_scope`
- `impact_review_scope`

### `workflow`

- `ordered_step_refs`
- `entry_conditions`
- `stop_conditions`
- `human_review_points`

## Defaults

- `transcript_posture`: `no_raw_transcript_in_repo`
- `source_authority_class`: `canonical_registry_card`
- `derived_index_eligibility`: `yes_derived_not_canonical`

## Field intent

These fields are intended to capture canonical governance posture, not full runtime implementation detail. They should be enough to reason about overlap, ownership, cadence, audit posture, and future derived discovery surfaces without authorizing direct execution.
