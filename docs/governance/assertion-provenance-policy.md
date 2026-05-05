# Assertion and Provenance Policy

Assertion objects are first-class governed objects in this repository.

They must not be treated as informal notes, free text, or unstructured
annotations when they carry meaningful interpretive or comparison weight.

## Core Rules

- every important assertion should be represented as a governed assertion object
- asserted, inferred, imported, AI-extracted, and editorial assertions must remain distinguishable
- provenance must not be flattened into generic notes
- evidence and provenance references should remain machine-readable
- review posture and trust posture should remain explicit

## Minimum Assertion Posture

A governed assertion should carry:

- stable identity
- subject, predicate, and object references
- assertion kind
- graph partition
- authority zone
- trust level
- review status
- evidence references where material
- provenance activity references

## Provenance Minimum

Every non-trivial assertion should be traceable to at least one provenance
activity or explicit source/evidence path.

Where an assertion is inferred, imported, AI-extracted, or boundary-sensitive,
the provenance trail should make that posture visible without collapsing it into
canonical asserted material.
