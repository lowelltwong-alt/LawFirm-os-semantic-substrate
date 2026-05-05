# Alignment-First Roadmap

## Purpose

This roadmap defines the repo-wide execution order for reconciling the active contract surface.

Its job is to keep the repository coherent as one system instead of letting ontology, document, policy, and operating layers drift apart.

## Governing Rule

Reconcile authoritative files in place before expanding surface area.

Prefer fewer, clearer canonical entrypoints over parallel guidance files, partial registries, or competing schema families.

## Target State

The steady state is a repository where:
- source-of-truth and registries resolve the active file for every contract family
- ontology, evidence, policy, and action layers remain distinct
- raw exceptions and operating objects cannot directly mutate canonical meaning
- document, retrieval, view, and operating contracts share one coherent authority surface

## Build Order

### Phase 1 - Front Door and Authority Surfaces
Goal: make entrypoint docs, registries, and contribution guidance agree on repo role and precedence.

Primary outputs:
- `README.md`
- `CONTRIBUTING.md`
- `registry/source-of-truth.json`
- `registry/schema-registry.json`
- `registry/exceptions-schema-registry.json`
- `registry/exception-route-registry.json`

Success condition:
- a reviewer can determine what the repo is, what files outrank others, and which registry governs each active contract family.

### Phase 2 - Semantic Core and Shape Hardening
Goal: align ontology surfaces and SHACL with the current semantic core.

Primary outputs:
- `registry/ontology-registry.json`
- `shapes/core.shacl.ttl`
- ontology boundary alignment across core doctrine

Success condition:
- the semantic core parses cleanly, uses the real namespace, and no longer depends on placeholder shapes.

### Phase 3 - Document and Evidence Contract Completion
Goal: finish the canonical source-structure layer that downstream retrieval and view systems depend on.

Primary outputs:
- document, span, citation, component, and provenance contracts
- canonical document and evidence examples
- stable links from evidence contracts back to the document model

Success condition:
- document meaning and source traceability are represented without treating chunks or indexes as truth.

### Phase 4 - Retrieval, Access, and View Contract Completion
Goal: complete the consumption layer without collapsing it into ontology truth.

Primary outputs:
- retrieval request and trace contracts
- access-decision and compliance surfaces
- view schemas and output examples

Success condition:
- retrieval, access, and presentation layers are governed and testable, but clearly derived from the canonical substrate.

### Phase 5 - Governed Runtime Learning Normalization
Goal: normalize the exception and pressure family around one strict mutation boundary.

Primary outputs:
- `schemas/exception-event.schema.json`
- `schemas/pressure-vector.schema.json`
- `schemas/adaptation-proposal.schema.json`
- `schemas/promotion-decision.schema.json`
- `registry/exceptions-schema-registry.json`
- `registry/exception-route-registry.json`

Success condition:
- raw runtime evidence can be routed, aggregated, reviewed, and promoted without ever becoming direct canonical write access.

### Phase 6 - Innovation OS Action Layer Hardening
Goal: make the operating layer useful without letting it masquerade as ontology truth.

Primary outputs:
- opportunity, sprint, pilot, validation-gate, scale-package, and executive-brief contracts
- clear draft registration for action-layer families
- explicit links from pressure to action to promotion

Success condition:
- the operating layer is machine-readable, reviewable, and distinct from both canonical meaning and derived presentation.

### Phase 7 - Profiles, Mappings, and External Systems
Goal: expand adapters only after the canonical target objects are stable.

Primary outputs:
- vendor profiles
- source-to-canonical mappings
- external-system integration notes

Success condition:
- adapters map into the existing canon instead of inventing parallel semantics.

### Phase 8 - Example, Evaluation, and CI Hardening
Goal: make the reconciled contract surface self-checking.

Primary outputs:
- missing examples
- evaluation assets
- CI checks aligned to the rewritten authoritative surfaces

Success condition:
- the repository can validate the contract surface it actually claims to run.

## Current Priority

Current priority order:
1. finish Phase 1 and Phase 2 reconciliation in place
2. normalize the runtime learning surface before broadening action-layer families
3. complete document and evidence contracts before expanding vendor adapters

## Non-Negotiable Controls

- No raw exception or operating artifact may directly mutate canonical ontology, taxonomy, core schema, or governance policy.
- Draft files must be marked and registered as draft.
- If an authoritative file is stale, rewrite it in place rather than creating a shadow replacement.
- Do not add new concept families until active registries and validators cover the current families.

## Read With

Use this roadmap alongside:
- `registry/source-of-truth.json`
- `governance/SYSTEM_MAP.md`
- `governance/PHASED_INTEGRATION_BACKLOG.md`
- `governance/ONTOLOGY_BOUNDARY_CONTRACT.md`
