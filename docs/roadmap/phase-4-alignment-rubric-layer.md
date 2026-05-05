# Phase 4 Alignment Rubric Layer

## Execution Control

Roadmap execution order is controlled by `docs/roadmap/READINESS_GATES.md`.
A phase advances only when the applicable readiness gate passes.

## Goal

Add a governed assessment layer above comparison objects so doctrinal
comparisons can carry scope, translation burden, evidence sufficiency,
confidence, and review posture in a machine-readable way.

## Added In This Phase

- rubric governance docs
- enums for alignment scope, translation burden, and evidence sufficiency
- first-class alignment assessment object type
- comparison object linkage to alignment assessments
- template and workflow scaffolding for rubric completeness checks

## What This Phase Preserves

- current relation verbs
- current alignment labels
- current trust zone and review status direction
- assertion and provenance separation from Phase 3

## Phase 5 Should Implement Next

- canonical examples with multiple alignment assessments per comparison family
- registry integration for assessment object families
- richer validation between comparison objects, assertions, and evidence bundles
- retrieval defaults that can filter by alignment scope and burden posture
