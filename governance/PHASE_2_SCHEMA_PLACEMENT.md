# Phase 2 Schema Placement

Phase 2 uses additive schema placement.

Existing root-level Innovation OS schemas stay in place for backward compatibility and remain the canonical existing surfaces. Examples include:

- `schemas/opportunity-object.schema.json`
- `schemas/sprint-object.schema.json`
- `schemas/pilot-object.schema.json`
- `schemas/validation-gate-record.schema.json`
- `schemas/scale-package-object.schema.json`
- `schemas/discovery-signal.schema.json`

New Phase 2 schema families are grouped by concern:

- `schemas/autonomy/`
- `schemas/harness/`
- `schemas/research/`
- `schemas/innovation/` only for genuinely new Innovation OS object types

The canonical discovery surface is `registry/`. Consumers should follow registry entries instead of inferring authority from folder layout alone.

No grouped duplicate copy is created for an existing root schema by default. A grouped alias or wrapper may be added only when a compatibility need is documented, and it must be marked as non-authoritative and point back to the root canonical schema.

Future cleanup or migration of root Innovation OS schemas must be handled as a separate compatibility-preserving change with reference checks, docs, and tests.
