# Exceptions Retrieval + Workflow Synergy

## Goal

Ensure retrieval tuning and workflow redesign are driven by the same governed exception evidence.

## Shared evidence model

- Retrieval miss events and workflow escalations are first-order exception events.
- Authority conflict/override events provide governance pressure context.
- All classes route through explicit route IDs and trust metadata.

## Synergy loops

1. **Retrieval miss -> retrieval tuning loop**
   - Improve chunk boundaries, neighborhood expansion, and ranking constraints.
2. **Workflow escalation -> workflow redesign loop**
   - Reduce unnecessary escalations, tighten handoff criteria, clarify fallback policy.
3. **Authority conflict/override -> governance review loop**
   - Resolve policy ambiguity, authority mismatch, or approval boundary confusion.

## Cross-loop learning

- Retrieval misses that repeatedly trigger workflow escalations should be co-clustered in pressure vectors.
- Authority conflicts arising from retrieval outputs should be tagged for both governance and retrieval review.
- Workflow redesign should be evaluated against retrieval miss reduction over time.

## Guardrail

No loop is allowed to write directly to canonical ontology from raw exceptions.
Any canonical change must pass reviewed promotion/rejection logic.
