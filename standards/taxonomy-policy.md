# Taxonomy Policy

## Use SKOS for

- controlled vocabularies
- preferred and alternate labels
- broader/narrower hierarchies
- mapping between schemes
- navigation and reporting views

## Use OWL for

- formal classes and properties
- relation semantics
- controlled inference
- cross-module semantic commitments

## Label rules

- one preferred label per language per concept
- alternate labels allowed for synonyms and variants
- hidden labels allowed only for search normalization

## Change rules

- do not silently relabel concepts in ways that change meaning
- deprecate or supersede instead of deleting active concepts
- keep taxonomy linearizations separate from ontology truth when they exist for UI or reporting only
