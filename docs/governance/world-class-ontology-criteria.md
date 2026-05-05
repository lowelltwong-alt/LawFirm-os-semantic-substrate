# World-Class Ontology Criteria

## Purpose

This document defines what "world-class" should mean for the LawFirm OS Semantic Substrate and its semantic extensions.

The goal is not maximal abstraction.
The goal is a governed, explainable, machine-readable system that stays useful in real operational settings.

## Core Position

A world-class ontology for this repository should:

- preserve a small canonical core
- stay additive rather than destabilizing the current shell
- make provenance, authority, and lifecycle first-class concerns
- separate substrate-native operating semantics from external vocabulary mappings
- support validation, review, and promotion workflows
- remain useful for retrieval and decision support, not only classification

## Decision Record Framework

Standards and major modeling choices should be recorded using explicit decision criteria.

Each adoption decision should answer:

1. What problem does this standard solve for Law Firm right now?
2. Why is it being adopted now, used selectively, or deferred?
3. Why does it fit the current substrate-native architecture?
4. Why should it not replace the substrate-native operating model?
5. What are the risks if it is overused too early?
6. What future trigger would justify expanding its use?

## World-Class Criteria

### 1. Small canonical core
The core ontology should remain disciplined.
A small, clear kernel is stronger than broad but weak semantic sprawl.

### 2. substrate-native operating layer
The repository should keep first-class substrate-native classes for operating semantics such as policy topic, operating position, governance baseline, position assessment, retrieval package, and promotion workflow.

### 3. External standards with explicit rationale
External vocabularies should be adopted with explicit why/why-not reasoning rather than by default import.

### 4. Provenance and authority first
A world-class ontology in this context must model who asserted what, from which source, under which authority, in which state, and with what downstream trust posture.

### 5. Validation as architecture
Validation is not optional tooling.
A world-class system makes its constraints inspectable and machine-checkable.

### 6. Mappings without semantic surrender
The ontology should interoperate with external standards while keeping the substrate-native layer as the design authority for operational meaning.

### 7. Operational usefulness
The ontology should support concrete questions such as:
- what governs this answer
- what conflicts with it
- what source supports it
- what changes if this position moves

### 8. Layered extensibility
Later legal-domain depth should come through controlled mappings and bounded modules, not by replacing the canonical shell with narrow domain formalisms.

## Adoption Categories

### Adopt now
Use when a standard is foundational, broad, low-regret, and directly supportive of the current architecture.

### Selective
Use when a standard is valuable in bounded slices but would add too much complexity if imposed as universal structure.

### Watchlist later
Use when a standard may become valuable later but is premature for the pilot and could distort the core if adopted too early.

## Practical Standard

A world-class ontology here is not the ontology with the most imported standards.
It is the ontology with the clearest design authority, the strongest governance, the most durable provenance model, and the highest usefulness per unit of complexity.
