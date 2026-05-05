# Lifecycle Policy

## Canonical lifecycle

- proposed
- experimental
- active
- deprecated
- retired

## Rules

- Prefer deprecate over delete.
- Keep identifiers resolvable after deprecation.
- New identifiers are required when meaning changes materially.
- Runtime learning artifacts may propose change but cannot directly mutate canonical meaning.

## Transition defaults

- proposed -> experimental
- experimental -> active
- active -> deprecated
- deprecated -> retired

## Review requirements

- semantic owner review for canonical changes
- ops owner review for operating objects
- security and legal/billing review where outputs affect client-facing or billing behavior
