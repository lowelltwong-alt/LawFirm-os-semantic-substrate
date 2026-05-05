# Phased Integration Backlog

## Purpose

This backlog turns the operating-layer architecture into remaining in-place integration work.

It complements the repo-wide roadmap by focusing on how the existing runtime and action families become one coherent contract surface.

## Track 1 - Runtime Evidence Normalization

Goal: keep raw exception intake and pressure aggregation bounded to evidence and learning signals.

Remaining work:
- align every governed example to canonical route registry IDs
- keep `exception-event` focused on append-only intake and routing metadata
- keep `pressure-vector` focused on aggregation, prioritization, and recommended follow-on paths

Exit condition:
- runtime evidence, route registry, and validators agree on IDs, loops, and the no-direct-mutation rule.

## Track 2 - Proposal and Promotion Governance

Goal: make reviewed change paths explicit without collapsing review into automation.

Remaining work:
- align `adaptation-proposal` and `promotion-decision` terminology to the current target layers
- require clear execution boundaries and reviewer roles on promotion decisions
- keep canonical change gated by reviewed promotion rather than raw evidence or operating artifacts

Exit condition:
- proposals and decisions say exactly what they may change, what they may not change, and what approvals are required.

## Track 3 - Action-Layer Contract Hardening

Goal: keep the Innovation OS action layer useful and distinct from semantic truth.

Remaining work:
- register opportunity, sprint, pilot, validation-gate, scale-package, and executive-brief schemas consistently
- ensure action objects point back to pressure, gate review, or promotion decisions instead of bypassing them
- keep draft action families marked as draft until examples, registries, and validators all converge

Exit condition:
- action objects are machine-readable and operationally useful without masquerading as ontology truth.

## Track 4 - Document and Evidence Bridge

Goal: complete the canonical source-structure layer that retrieval and views depend on.

Remaining work:
- finish source-artifact, canonical-text, component, citation, chunk-set, embedding-set, and index-build contracts
- align retrieval and answer schemas with the canonical document model
- make provenance explicit for parse, chunk, embedding, indexing, and answer generation steps

Exit condition:
- source structure feeds retrieval and views without becoming a parallel truth source.

## Track 5 - View, Evaluation, and Adoption Surfaces

Goal: ensure sponsor-facing outputs are derived from governed contracts rather than ad hoc prose.

Remaining work:
- complete view examples
- complete evaluation assets
- keep executive briefing outputs derived from validated evidence, runtime, and action objects

Exit condition:
- sponsor-facing packets can be generated from the governed surface without bypassing review controls.

## Track 6 - Profile and Mapping Expansion

Goal: expand adapters only after the target canon is stable.

Remaining work:
- complete additional vendor profiles
- add source-to-canonical mappings for remaining high-value systems
- preserve the distinction between adapter semantics and canonical meaning

Exit condition:
- adapters map into the existing canon instead of inventing a parallel ontology system.

## Order of Work

Recommended order:
1. Track 1
2. Track 2
3. Track 4
4. Track 3
5. Track 5
6. Track 6

## Guardrails

- Do not create parallel doctrine files to explain the same layer.
- Do not register an action object as canonical ontology truth.
- Do not treat derived views, summaries, or indexes as authoritative.
- Do not weaken the promotion boundary to speed implementation.

## Remaining Integration Gaps

- align legacy example route IDs with canonical route registry IDs
- complete missing document and evidence schemas
- register remaining active action and view schemas consistently
- replace older CI and helper script placeholders with working implementations
