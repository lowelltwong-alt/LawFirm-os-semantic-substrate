# Breakthrough Triage Policy

Use this policy when a math-intelligence item may affect Law Firm planning or governance.

## Recommendation set

- `ignore`
  - Use when the signal lacks relevance, credibility, or bounded next steps.
- `watch`
  - Use when the signal may matter later but does not justify active follow-up yet.
- `summarize`
  - Use when the signal merits a short internal briefing with explicit uncertainty.
- `deep_research`
  - Use when a scoped follow-up research task or prompt is warranted.
  - `deep_research` is not verified truth.
  - `deep_research` is not automatic canon change.
  - `deep_research` is not automatic runtime implementation.
- `prototype`
  - Use when a later bounded experiment may be worth proposing in the correct repo or planning surface.
- `update_roadmap`
  - Use when the item should become a roadmap candidate or tracked planning note.
- `create_adaptation_proposal`
  - Use when governed change may be worth proposing after review.
  - This is only a recommendation toward governed change, not the change itself.

## Gate sequence

1. Confirm source type and source status.
2. Assign proof status.
3. Assign math-domain tags.
4. Assign project-surface impact tags.
5. Decide whether the item is architecturally relevant.
6. Select the narrowest justified recommendation.

## Source and proof gates

- `rumor` and weak `preprint_claim` items should usually end at `ignore`, `watch`, or `summarize`.
- `formalized_proof`, `peer_reviewed`, `replicated`, or bounded `benchmark_result` items may justify `deep_research`, `prototype`, or `update_roadmap`.
- `disputed` items require explicit uncertainty and usually should not advance beyond `watch`, `summarize`, or carefully scoped `deep_research`.

## Governed recursive improvement

All outputs from this route are governed-learning inputs for governed recursive improvement, not autonomous changes.

Use the existing authority path:

`candidate signal -> assessment -> recommendation -> adaptation-proposal recommendation if reviewed -> promotion-decision only through existing authority path`
