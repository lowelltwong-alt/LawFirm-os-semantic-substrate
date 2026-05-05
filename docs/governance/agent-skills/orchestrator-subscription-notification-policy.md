# Orchestrator Subscription and Notification Policy

This document defines how orchestrators should reason about subscriptions and notifications at the governance layer.

## Subscription targets

Orchestrators may subscribe to:
- dependency refs
- composed node refs
- `capability_function` tags
- `project_surface` tags
- lifecycle changes
- audit-class changes
- deprecation or supersession edges
- overlap review outcomes

## Notification classes

- `watch_only`
- `review_required`
- `composition_recheck`
- `audit_reassessment`
- `deprecation_follow_up`
- `merge_overlap_review`

## Trigger conditions

- upstream dependency changes
- overlapping capability is promoted, merged, or deprecated
- audit or transcript posture changes
- owner or cadence becomes stale
- monitor emits a capability-related candidate signal
- workflow step changes under orchestrator scope

## Boundary

These notifications are governance outputs only. They may create watch items, reviews, summaries, roadmap update candidates, or adaptation-proposal recommendations. They may not directly rewrite orchestrators, workflows, or runtime behavior.
