# Ownership and Review Cadence Policy

This document defines the ownership model and review posture for capability cards.

## Required roles

- `primary_owner_role`
- `steward_role`
- `reviewer_role`

## Required cadence fields

- `review_cadence`
- `last_reviewed`
- `next_review_due`
- `change_trigger_conditions`

## Cadence intent

Cadence should keep large capability inventories from becoming stale, duplicated, or silently contradictory.

Recommended review triggers include:
- upstream dependency changes
- overlap findings
- audit posture changes
- lifecycle changes
- Exceptions Lake candidate signals
- major ecosystem-mapping changes

## Stale-review handling

Stale cards should create governance review pressure, not silent deletion or automatic rewrite. Staleness may become a candidate signal for governed learning and later review.
