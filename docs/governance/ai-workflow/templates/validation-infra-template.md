# Validation Infrastructure Template

Use for changes to validators, validation documentation, CI expectations, or audit wrappers.

## Route
- route: `validation_infra`
- mode: Plan/Edit

## Required sections

- Validation surface changed
- Existing validator pattern reused
- Expected pass/fail posture
- Known fail-closed gates
- Commands run
- Exact results
- Follow-up enforcement risk

## Forbidden

- silent skips
- hiding validator failures
- converting a truthful fail-closed gate into a false pass
- broad CI rewrites in a docs-only PR
