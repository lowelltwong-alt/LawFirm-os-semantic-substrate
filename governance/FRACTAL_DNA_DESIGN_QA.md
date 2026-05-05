# Fractal DNA Design Q&A

Author: Lowell T. Wong

## Purpose

This document explains the deeper architectural logic behind the repository's recursive, fractal, and DNA-like design. It is intended to help future AI sessions, contributors, and system builders understand not only **what** was built, but **why** it was built this way.

## What does "DNA-like" mean in this repository?

It does **not** mean biology in a literal sense.

It means that the system is designed so that its major object types carry a repeatable structural grammar that tells a future system:
- what an object is
- where it is
- what it belongs to
- what it is connected to
- what it is derived from
- what state it is in
- optionally where it sits in semantic / model space

This repeating grammar is the system's DNA-like pattern.

## What makes the system recursive?

The same logic recurs across levels.

Examples:
- the repository has identity, structure, lineage, and state
- a domain model has identity, structure, lineage, and state
- an artifact has identity, structure, lineage, and state
- a claim has identity, structure, lineage, and state
- a retrieval object has identity, structure, lineage, and state

The rules recur across scales rather than being reinvented at each level.

## What makes the system fractal?

The system becomes more fractal when:
- local objects resemble the larger architecture
- the same design pattern can be repeated across domains
- new modules inherit the same grammar rather than creating their own incompatible one
- structure and governance remain coherent as the system scales

This means the ontology is not only hierarchical. It is recursively self-similar.

## Why is the fractal address system important?

A stable ID answers:
- what object is this?

The fractal address answers:
- where does this object sit in the larger architecture?

That distinction is important because identity should remain stable even when structural placement evolves.

The address system is important because it gives every governed object a machine-readable and human-auditable answer to:
- where am I?
- what layer am I in?
- what is above me?
- what is below me?
- what is beside me?

## Why not use only graph edges and skip addresses?

Graph relations are necessary, but they are not always sufficient.

Graph edges tell you about connectedness.
Addresses tell you about placement.

A serious ontology often needs both:
- graph freedom for semantic relationships
- structural placement for navigability, governance, clustering, and interpretation

## What is first-order vs second-order in this system?

### First-order objects
These are governed objects that directly participate in the ontology's core structural grammar.

Examples:
- nodes
- claims
- sources
- chunks
- artifacts
- retrieval objects
- domain models
- validation objects

They should all be able to express:
- identity
- address
- relations
- lineage
- state
- optional semantic coordinates

### Second-order objects
These are objects, signals, or derived layers that help interpret or operationalize first-order objects but do not replace them.

Examples:
- embedding clusters
- vector neighbors
- projections
- ranking scores
- generated summaries
- support/contradiction analytics

Second-order layers enrich the system, but the first-order layer remains authoritative.

## Why does trust belong in the DNA pattern?

Because ontology systems fail when they treat all objects and relationships as equally trustworthy.

Trust should apply to:
- objects
- artifacts
- claims
- edges
- retrieval outputs

Without trust-aware structure:
- AI systems flatten strong and weak sources together
- outdated artifacts look authoritative
- inferred links appear equal to asserted ones

## What are the core DNA questions every major object should answer?

A future system should be able to ask of any first-order governed object:

1. What are you?
2. Where are you?
3. What are you connected to?
4. What are you derived from?
5. What state are you in?
6. How trustworthy are you?
7. Should AI systems use you, and how strongly?
8. Do you have semantic/model-space signals associated with you?

## Why does the repository separate deterministic and probabilistic logic?

Because the system wants to support both:
- governed structural truth
- model-derived semantic enrichment

These should not collapse into each other.

Deterministic layers govern:
- identity
- address
- lineage
- authority
- validation
- lifecycle

Probabilistic layers enrich:
- similarity
- clustering
- semantic expansion
- weak-signal discovery

## Why is this important for future AI systems?

Future AI systems should be able to:
- read a governed object
- understand its role from its structure
- trace its lineage
- know how much to trust it
- know where it sits in the larger architecture
- combine symbolic and semantic reasoning without confusing the two

That is why the address system, trust system, lineage system, and artifact system all matter together.

## What should future builders preserve?

Future builders should preserve:
- the distinction between identity and address
- first-order artifact thinking
- claim-centered reasoning
- trust-aware ontology logic
- lineage and attribution chains
- deterministic / probabilistic separation
- example / non-production labeling unless intentionally changed

## Final summary

The repository's recursive / fractal / DNA-like design is an attempt to make every important object self-describing enough that future humans and future AI systems can:
- interpret it
- validate it
- connect it
- trust-rank it
- extend it

without losing architectural coherence.
