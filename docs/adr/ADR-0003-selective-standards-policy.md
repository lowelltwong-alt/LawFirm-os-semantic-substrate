# ADR-0003 Selective Standards Policy

## Status
Accepted

## Decision

The repository will use some standards selectively rather than universally.

Current selective standards:

- ODRL
- W3C Time Ontology
- W3C ORG
- heavier OWL constructs

## Why Selective

These standards can help in bounded slices, but they add complexity quickly if applied across the whole model too early.

## Current Fit

Use selectively when a real pilot need exists, such as:
- permissions and restrictions
- effective dates and review windows
- organization roles and stewardship
- bounded logical precision

## Why Not Universal Yet

The current proof of concept is still focused on a small substrate-native operating layer. Making these standards universal now would risk pulling the model away from the pilot use case and into premature abstraction.

## Review Trigger

Expand use only after repeated operational demand, stable stewardship, and clear evidence that the additional complexity improves decision support or interoperability.