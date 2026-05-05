# Phase Dependency Map

## Execution Control

Roadmap execution order is controlled by `docs/roadmap/READINESS_GATES.md`.
A phase advances only when the applicable readiness gate passes.

## Purpose

Show how the major repository phases build on one another.

## Order

1. Canonical spine
2. Substrate definition
3. Validation hardening
4. Assertion and provenance layer
5. Alignment rubric layer
6. Operational governance and pilot slices
7. Semantic graph stack
8. Standards rationale and external alignment
9. Sponsor-ready pilot layer
10. Bounded runtime continuation

## Dependency Notes

- the canonical spine comes first because it defines design authority
- validation hardening comes early because later layers need guardrails
- provenance and trust boundaries come before graph and retrieval work
- pilot and sponsor layers depend on the earlier semantic and governance layers
- later phases should extend earlier phases rather than replace them

## Operating Rule

A later phase should only proceed when the earlier phase it depends on is still coherent with the canonical spine and validation path.
