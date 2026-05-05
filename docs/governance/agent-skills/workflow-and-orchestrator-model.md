# Workflow and Orchestrator Model

This document defines how workflows and orchestrators should be represented in the canonical registry.

## Workflow

A workflow is an ordered capability surface that coordinates steps, entry conditions, stop conditions, and human review points.

Workflow cards should focus on:
- ordered step references
- entry and stop conditions
- review checkpoints
- covered capability surfaces

## Orchestrator

An orchestrator is a coordination surface that composes or delegates across capability nodes while remaining governed by canonical cards, typed edges, ownership, cadence, and audit posture.

Orchestrator cards should focus on:
- coordinated node refs
- subscription scope
- impact review scope
- dependency and overlap awareness

## Model boundary

This is a governance model only. It does not authorize runtime orchestration engines, schedulers, or autonomous system rewrites.

## Governed-learning role

Workflows and orchestrators may become sources or recipients of candidate signals through monitors, overlap reviews, or Exceptions Lake findings, but any stronger change still follows the existing governed path.
