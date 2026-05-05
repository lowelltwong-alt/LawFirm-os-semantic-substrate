#!/usr/bin/env bash
# Single-command repository health gate.
#
# Runs the full validator stack against the working tree and exits non-zero
# on any failure. Intended for use locally before commit and from CI as a
# convenience wrapper. Each validator below is also wired into a dedicated
# .github/workflows/*.yml; this script is the human-facing equivalent.
#
# Usage: scripts/run_full_audit.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-python}"

run() {
  local label="$1"; shift
  printf '\n=== %s ===\n' "$label"
  "$@"
}

# Address layer
run "address: enforce across objects"  "$PYTHON" scripts/enforce_address_across_objects.py
run "address: enforce across schemas"  "$PYTHON" scripts/enforce_address_across_schemas.py

# Registry / coherence
run "registry: check refs"             "$PYTHON" scripts/check_registry_refs.py
run "registry: validate examples"      "$PYTHON" scripts/validate_examples_registry.py
run "source-of-truth coherence"        "$PYTHON" scripts/validation/validate_source_of_truth_coherence.py

# Schema validity / IDs
run "schema: structural validation"    "$PYTHON" scripts/validation/validate_schema.py
run "schema: ID conventions"           "$PYTHON" scripts/validation/check_ids.py
run "schema: repo YAML parse"          "$PYTHON" scripts/validation/check_repo_yaml.py

# Canonical examples & integrity
run "examples: canonical validation"   "$PYTHON" scripts/validate_examples_canonical.py
run "source ingestion manifests"       "$PYTHON" scripts/validation/validate_source_ingestion_manifests.py
run "examples: integrity"              "$PYTHON" scripts/validate_integrity.py
run "examples: claim v3 stub"          "$PYTHON" scripts/validate_examples.py

# Repository-wide governed surfaces
run "repository vNext"                 "$PYTHON" scripts/validate_repository_vnext.py
run "governed-learning examples"       "$PYTHON" scripts/validate_governed_learning_examples.py
run "exception events: structural"     "$PYTHON" scripts/validation/validate_exception_events.py
run "exception governance"             "$PYTHON" scripts/validation/validate_exception_governance.py
run "learning-loop transitions"        "$PYTHON" scripts/validation/validate_learning_loop_transitions.py

# Spine / DNA / boundaries
run "canonical spine"                  "$PYTHON" scripts/validate_canonical_spine.py
run "DNA invariants"                   "$PYTHON" scripts/validation/validate_dna_invariants.py
run "ontology boundary"                "$PYTHON" scripts/validation/validate_ontology_boundary.py
run "semantic stack"                   "$PYTHON" scripts/validation/validate_semantic_stack.py
run "canonical grounding chain"        "$PYTHON" scripts/validation/validate_canonical_grounding_chain.py
run "grounded-answer evaluation"       "$PYTHON" scripts/validation/validate_grounded_answer_evaluation_harness.py
run "gold-standard backbone"           "$PYTHON" scripts/validation/validate_gold_standard_backbone.py

# External alignment / interop
run "external alignment scaffold"      "$PYTHON" scripts/validation/validate_external_alignment.py
run "external alignment strict"        "$PYTHON" scripts/validation/validate_external_alignment_strict.py
run "interop mappings"                 "$PYTHON" scripts/validation/validate_interop_mappings.py

# SHACL
run "SHACL: seed shape parse"          "$PYTHON" scripts/validation/validate_shacl.py
run "SHACL: core shapes vs core data"  "$PYTHON" scripts/validation/run_shacl.py

# Talent intelligence extension
run "talent intelligence: examples"    "$PYTHON" scripts/validate_talent_intelligence_examples.py
run "talent intelligence: schemas"     "$PYTHON" scripts/validate_talent_intelligence_examples_against_schemas.py

# Phased loops
run "phase 3: graph partitions"        "$PYTHON" scripts/phase3/check_graph_partitions.py
run "phase 3: provenance minimum"      "$PYTHON" scripts/phase3/validate_provenance_minimum.py
run "phase 4: comparison assessment"   "$PYTHON" scripts/phase4/check_comparison_assessments.py
run "phase 4: alignment rubric"        "$PYTHON" scripts/phase4/validate_alignment_rubric.py
run "phase 5: object sets"             "$PYTHON" scripts/phase5/validate_object_sets.py
run "phase 5: action types"            "$PYTHON" scripts/phase5/validate_action_types.py
run "phase 5: pilot slices"            "$PYTHON" scripts/phase5/validate_pilot_slices.py

printf '\n=== ALL AUDIT CHECKS PASSED ===\n'
