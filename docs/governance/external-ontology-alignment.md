# External Ontology Alignment

## Purpose

This document explains how external standards should relate to the LawFirm OS Semantic Substrate.

The design rule is:

- reuse broad semantic foundations where they strengthen the system
- map to domain standards where they help
- keep substrate-native operating semantics as the design authority

## Why We Are Not Building From Scratch

Some ontology concerns are solved better by established standards than by local invention.

Examples include:
- provenance
- concept labels and controlled vocabularies
- metadata timestamps and authorship
- graph validation
- light logical semantics

Reusing these patterns lowers risk and increases interoperability.

## Why We Are Not Importing External Legal Ontologies As The Core

The pilot is about governed operating positions for intake, conflicts, and AI use.

That requires a system that can express:
- policy topics
- operating positions
- governance baselines
- scoped restrictions
- retrieval packages
- proposal and promotion workflows

Most external legal ontologies are too narrow, too formal, or too document-centric to serve as the master architecture for that operating layer.

## Adoption Categories

### Adopt now
Use when the standard is foundational, broad, low-regret, and directly supportive of the current architecture.

Adopt now standards:
- RDF / JSON-LD
- SKOS
- PROV-O
- DCTERMS
- SHACL
- OWL-light

Why:
- they solve generic semantic and governance problems already present in the repo
- they strengthen provenance, labeling, validation, and interoperability
- they do not force the repo into a narrow legal frame

### Selective
Use when the standard is valuable in bounded slices but should not be imposed across the full model yet.

Selective standards:
- ODRL
- W3C Time Ontology
- W3C ORG
- heavier OWL constructs

Why:
- they can help with permissions, effective dates, organization structure, and richer logic
- they add complexity quickly if made universal too early
- they are better introduced where the use case is already real and reviewed

### Watchlist later
Use when the standard is promising for future legal depth or interoperability but is premature for the current proof of concept.

Watchlist later standards:
- LKIF Core
- LegalRuleML
- Akoma Ntoso

Why:
- they may become useful once the substrate-native operating layer is stable
- adopting them too early would pull the pilot toward legal-document formalism and away from the immediate governance use case
- watchlist later means not rejected, but not core yet

## Substrate-Native Design Authority

The following should remain substrate-native first-class concepts:

- policy topic
- operating position
- governance baseline
- position assessment
- retrieval package
- proposal promotion
- exception request

External standards should support these concepts through mappings, not replace them.

## Revisit Triggers

Move a standard from selective or watchlist later toward broader adoption only when one or more of these become true:

- repeated pilot demand shows the concept is operationally necessary
- a stable review workflow exists for the affected object family
- the mapping reduces duplication without obscuring Law Firm semantics
- the added complexity improves decision support or interoperability in a measurable way

## Final Rule

The ontology should be standards-aligned, not standards-controlled.
