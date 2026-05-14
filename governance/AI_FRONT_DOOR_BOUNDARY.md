# AI Front Door Boundary

## Authority

This document governs the **AI front door integrity gate** for the Semantic Substrate control plane.

Canonical machine-readable registry: `registry/ai-front-door-registry.json`.

Supporting manifests:

- `registry/registry-full-manifest.json` — every `registry/*.json` file must be listed here so additions fail closed until the manifest is refreshed.
- `registry/governance-full-manifest.json` — every `governance/**/*.md` file must be listed here so governance drift is detected.
- `registry/schema-surface-exclusions.json` — explicit, documented exclusions for JSON Schema files under `schemas/` that are **not** yet represented in `registry/schema-registry.json` (legacy, extension, or staged backfill surfaces).

## Human read order (unchanged)

The mandatory narrative routers remain:

- `AI_WORK_START_HERE.md`
- `AI_TABLE_OF_CONTENTS.md`

Those files **must** reference this boundary and the `registry/ai-front-door-registry.json` entry so agents discover the machine gate.

## Schema surface policy

1. Every `schemas/**/*.json` file must either appear as a `path` in `registry/schema-registry.json` **or** carry an explicit exclusion entry in `registry/schema-surface-exclusions.json` with `governance_doc`, `governance_reason`, and `exclusion_class`.
2. New legal-knowledge research schemas **must** land in `registry/schema-registry.json` unless an exclusion is explicitly approved under (1).
3. The singular legacy tree `schema/` (non-plural) remains **out of scope** for this gate (see `AI_TABLE_OF_CONTENTS.md` “Schema Locations”).

## Cross-repo checks

The validator (`scripts/validate_ai_front_door.py`) resolves sibling repos from the parent workspace folder (`LawFirm-os-orchestrator`, `LawFirm-os-legal-knowledge-runtime`, `LawFirm-os-exceptions-lake-runtime-main`, `LawFirm-os-skills-registry`) and enforces:

- Legal Knowledge Runtime public CLI commands and helper modules listed in `registry/ai-front-door-registry.json`.
- Orchestrator legal-knowledge adapter surfaces.
- Exception Lake synthetic event examples referenced from the registry.
- Skills under `skills/draft/` indexed in `registry/proposed-draft-skill-index.json` (LawFirm-os-skills-registry).

## Endpoint metadata contract

Every tool/endpoint entry in `registry/ai-front-door-registry.json` must include:

`id`, `owning_repo`, `owning_plane`, `path`, `purpose`, `side_effect_class`, `input_schema`, `output_schema`, `human_approval_required`, `stores_raw_legal_payload` (must be `false` for this integration), `allowed_data_classes`, `related_docs`.

Violations fail CI via `tests/test_ai_front_door_integrity.py`.
