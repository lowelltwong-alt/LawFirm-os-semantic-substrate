# Schema Change Template

Use when adding or modifying schema contracts, examples, or schema registry entries.

## Route
- route: `schema_change`
- mode: Plan/Edit

## Required sections

- Schema(s) touched
- Registry impact
- Example impact
- Backward compatibility notes
- Validation commands
- Failure and rollback notes
- Routing impact

## Forbidden

- production runtime changes
- real internal data
- silent validator bypass
- schema changes without matching examples or registry review when required
