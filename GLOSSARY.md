# Glossary

This glossary defines key repo terms in a way that is safe for humans and AI systems consuming the repository from the outside.

## Semantic control plane
The governed layer that defines meaning, contracts, precedence, and mutation rules for the repository.
In this repo, that primarily lives in `registry/`, `governance/`, `ontology/`, `shapes/`, and `schemas/`.

## Source of truth
The repo file that declares authoritative files, precedence order, layer model, schema-resolution order, and mutation boundaries.
In this repo, that is `registry/source-of-truth.json`.

## Design authority
The design posture and non-negotiables for the repository: what the repo is for, what principles govern change, and what must never be violated.
In this repo, that is `registry/design-authority.json`.

## Canonical spine
The minimum set of live canonical schemas and validation surfaces that define the active contract posture of the repo.
In this repo, see `governance/canonical_spine_manifest.json`.

## Canonical vs derived
Canonical means authoritative meaning or contract.
Derived means generated, illustrative, runtime, or downstream material built from canonical sources.
Derived artifacts must not redefine canonical meaning.

## Authority zone
A bounded part of the repo with a defined authority level and role.
Examples: canonical, operational, reference, example, supporting, historical.
See `AUTHORITY_MAP.yaml`.

## Claim container
A governed claim object, currently represented by the active claim schema in `schemas/claim_v3.schema.json` and resolved through `registry/schema-registry.json`.

## Exception event
A runtime signal that something unexpected or out of policy happened.
It is evidence for review and aggregation, not direct permission to mutate canonical files.

## Pressure vector
An aggregated signal derived from multiple exceptions or related operational evidence.
It is used to surface patterns for governed review.

## Promotion decision
The governed approval surface required before canonical change is allowed.
Raw runtime evidence, exceptions, and proposals do not directly rewrite canonical meaning.

## Schema surface
The live operational schema layer used by validators and examples.
On current `main`, active schema resolution should start with `registry/schema-registry.json`.

## Schema framework surface
The schema-set manifest and interface/invariant structure in `schema/`.
This is not the same thing as the concrete schema files in `schemas/`.

## Historical surfaces
`legacy/` and `archive/`.
These are retained for traceability and should not be treated as current active authority.
